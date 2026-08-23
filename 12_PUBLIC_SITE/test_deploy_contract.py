#!/usr/bin/env python3
"""Offline negative controls for the two-phase Vercel release contract."""

from __future__ import annotations

import io
import json
import os
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from subprocess import TimeoutExpired

import deploy_release_contract as contract


def archive_bytes(name: str, payload: bytes, *, kind: bytes = tarfile.REGTYPE) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        info = tarfile.TarInfo(name)
        info.type = kind
        info.mode = 0o644
        info.size = len(payload) if kind == tarfile.REGTYPE else 0
        archive.addfile(info, io.BytesIO(payload) if payload else None)
    return buffer.getvalue()


class DeployReleaseContractTests(unittest.TestCase):
    def test_archive_manifest_is_content_addressed(self) -> None:
        rows = contract._inspect_archive(archive_bytes("index.html", b"hello\n"))
        self.assertEqual(rows[0]["path"], "index.html")
        self.assertEqual(rows[0]["size"], 6)
        self.assertEqual(rows[0]["sha256"], contract._sha256_bytes(b"hello\n"))

    def test_archive_traversal_is_rejected(self) -> None:
        with self.assertRaises(contract.ReleaseContractError):
            contract._inspect_archive(archive_bytes("../escape", b"x"))

    def test_archive_symlink_is_rejected(self) -> None:
        with self.assertRaises(contract.ReleaseContractError):
            contract._inspect_archive(archive_bytes("link", b"", kind=tarfile.SYMTYPE))

    def test_json_parser_accepts_only_a_trailing_object(self) -> None:
        self.assertEqual(
            contract._parse_json_object('progress\n{"status":"ok"}'),
            {"status": "ok"},
        )
        with self.assertRaises(contract.ReleaseContractError):
            contract._parse_json_object("no json here")

    def test_receipt_integrity_detects_tamper(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "receipt.json"
            contract._write_receipt(path, {"schema": contract.SCHEMA, "state": "TEST"})
            self.assertEqual(contract._load_receipt(path)["state"], "TEST")
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["state"] = "TAMPERED"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(contract.ReleaseContractError):
                contract._load_receipt(path)

    def test_stage_manifest_rejects_symlink_and_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "target").write_text("x", encoding="utf-8")
            (root / "link").symlink_to(root / "target")
            with self.assertRaises(contract.ReleaseContractError):
                contract._stage_rows(root)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".env.backup").write_text("TOKEN=x", encoding="utf-8")
            with self.assertRaises(contract.ReleaseContractError):
                contract._stage_rows(root)

    def test_control_directory_rejects_every_extra_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            control = root / ".vercel"
            control.mkdir()
            (control / "project.json").write_text("{}", encoding="utf-8")
            contract._verify_control_dir(root)
            (control / ".env.production.local").write_text(
                "TOKEN=forbidden", encoding="utf-8"
            )
            with self.assertRaises(contract.ReleaseContractError):
                contract._verify_control_dir(root)

    def test_command_timeout_is_typed_indeterminate(self) -> None:
        with patch.object(
            contract.subprocess,
            "run",
            side_effect=TimeoutExpired(cmd=["vercel", "promote"], timeout=1),
        ):
            with self.assertRaises(contract.CommandTimeoutError):
                contract._run(["vercel", "promote"], cwd=contract.SITE_ROOT, timeout=1)

    def test_release_lock_refuses_a_second_local_command(self) -> None:
        with patch.dict(
            os.environ,
            {
                contract.PROJECT_PIN_ENV: "project-pin-lock-test",
                contract.ORG_PIN_ENV: "org-pin-lock-test",
            },
            clear=False,
        ):
            with contract._exclusive_release_lock():
                with self.assertRaises(contract.ReleaseContractError):
                    with contract._exclusive_release_lock():
                        self.fail("second release lock unexpectedly succeeded")

    def test_stage_never_calls_promote(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipt.json"
            stage_dir = root / "stage"
            stage_dir.mkdir()
            contract._write_receipt(
                receipt_path,
                {
                    "schema": contract.SCHEMA,
                    "state": "PREPARED",
                    "release_nonce": "a" * 32,
                    "critical_sha256": {},
                },
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(
                    contract,
                    "_current_production",
                    return_value=("dpl_previous", "previous.vercel.app"),
                ),
                patch.object(
                    contract,
                    "_observe_critical_live",
                    return_value={"/": "previous"},
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(contract, "_require_production_identity"),
                patch.object(contract, "_verify_stage", return_value=stage_dir),
                patch.object(
                    contract,
                    "_deploy_held",
                    return_value=("dpl_new", "https://new.vercel.app"),
                ),
                patch.object(contract, "_strict_audit", return_value="audit"),
                patch.object(contract, "_verify_critical_live", return_value={}),
                patch.object(contract, "_promote") as promote_call,
            ):
                result = contract.stage(receipt_path)
            self.assertEqual(result["state"], "STAGED_VERIFIED")
            promote_call.assert_not_called()

    def test_stage_dispatch_timeout_reconciles_nonce_without_redeploy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipt.json"
            stage_dir = root / "stage"
            stage_dir.mkdir()
            contract._write_receipt(
                receipt_path,
                {
                    "schema": contract.SCHEMA,
                    "state": "PREPARED",
                    "release_nonce": "b" * 32,
                    "critical_sha256": {},
                },
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(
                    contract,
                    "_current_production",
                    return_value=("dpl_previous", "previous.vercel.app"),
                ),
                patch.object(
                    contract,
                    "_observe_critical_live",
                    return_value={"/": "previous"},
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(
                    contract,
                    "_deploy_held",
                    side_effect=contract.CommandTimeoutError("timeout"),
                ),
            ):
                with self.assertRaises(contract.CommandTimeoutError):
                    contract.stage(receipt_path)
            self.assertEqual(
                contract._load_receipt(receipt_path)["state"], "STAGE_DISPATCHING"
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(
                    contract,
                    "_find_deployment_by_release_nonce",
                    return_value=("dpl_new", "https://new.vercel.app"),
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(contract, "_verify_stage", return_value=stage_dir),
                patch.object(contract, "_require_production_identity"),
                patch.object(contract, "_strict_audit", return_value="audit"),
                patch.object(contract, "_verify_critical_live", return_value={}),
                patch.object(contract, "_deploy_held") as deploy_call,
            ):
                result = contract.stage(receipt_path)
            self.assertEqual(result["state"], "STAGED_VERIFIED")
            deploy_call.assert_not_called()

    def test_promotion_timeout_is_receipted_without_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipt.json"
            stage_dir = root / "stage"
            stage_dir.mkdir()
            contract._write_receipt(
                receipt_path,
                {
                    "schema": contract.SCHEMA,
                    "state": "STAGED_VERIFIED",
                    "release_nonce": "a" * 32,
                    "deployment_id": "dpl_new",
                    "deployment_url": "https://new.vercel.app",
                    "critical_sha256": {},
                    "previous_deployment_id": "dpl_previous",
                    "held_verified_production_id": "dpl_previous",
                },
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(contract, "_strict_audit", return_value="audit"),
                patch.object(contract, "_verify_critical_live", return_value={}),
                patch.object(contract, "_verify_stage", return_value=stage_dir),
                patch.object(contract, "_require_production_identity"),
                patch.object(
                    contract,
                    "_promote",
                    side_effect=contract.CommandTimeoutError("timeout"),
                ) as promote_call,
                patch.object(contract, "_wait_for_production") as wait_call,
            ):
                with self.assertRaises(contract.ReleaseContractError):
                    contract.promote(receipt_path)
            self.assertEqual(contract._load_receipt(receipt_path)["state"], "PROMOTION_INDETERMINATE")
            self.assertEqual(promote_call.call_count, 1)
            wait_call.assert_not_called()

    def test_promotion_predecessor_guard_runs_before_remote_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipt.json"
            stage_dir = root / "stage"
            stage_dir.mkdir()
            contract._write_receipt(
                receipt_path,
                {
                    "schema": contract.SCHEMA,
                    "state": "STAGED_VERIFIED",
                    "release_nonce": "a" * 32,
                    "deployment_id": "dpl_new",
                    "deployment_url": "https://new.vercel.app",
                    "critical_sha256": {},
                    "previous_deployment_id": "dpl_previous",
                    "held_verified_production_id": "dpl_previous",
                },
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(contract, "_strict_audit", return_value="audit"),
                patch.object(contract, "_verify_critical_live", return_value={}),
                patch.object(contract, "_verify_stage", return_value=stage_dir),
                patch.object(
                    contract,
                    "_require_production_identity",
                    side_effect=contract.ReleaseContractError("predecessor changed"),
                ),
                patch.object(contract, "_promote") as promote_call,
            ):
                with self.assertRaises(contract.ReleaseContractError):
                    contract.promote(receipt_path)
            promote_call.assert_not_called()
            self.assertEqual(
                contract._load_receipt(receipt_path)["state"], "STAGED_VERIFIED"
            )

    def test_rollback_uses_vercel_rollback_not_promote(self) -> None:
        with patch.object(contract, "_run") as run_call:
            contract._rollback("dpl_previous")
        self.assertEqual(
            run_call.call_args.args[0],
            ["vercel", "rollback", "dpl_previous", "--yes"],
        )

    def test_rollback_dispatch_reconciles_predecessor_without_reissuing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipt_path = root / "receipt.json"
            stage_dir = root / "stage"
            stage_dir.mkdir()
            contract._write_receipt(
                receipt_path,
                {
                    "schema": contract.SCHEMA,
                    "state": "ROLLBACK_DISPATCHING",
                    "release_nonce": "c" * 32,
                    "deployment_id": "dpl_new",
                    "deployment_url": "https://new.vercel.app",
                    "previous_deployment_id": "dpl_previous",
                    "critical_sha256": {},
                },
            )
            with (
                patch.object(
                    contract, "_validate_phase", return_value=("a" * 40, stage_dir)
                ),
                patch.object(contract, "_deployment_api", return_value={}),
                patch.object(contract, "_validate_deployment_api"),
                patch.object(contract, "_strict_audit", return_value="audit"),
                patch.object(contract, "_verify_critical_live", return_value={}),
                patch.object(contract, "_verify_stage", return_value=stage_dir),
                patch.object(
                    contract,
                    "_current_production",
                    return_value=("dpl_previous", "previous.vercel.app"),
                ),
                patch.object(
                    contract, "_verified_rollback_hashes", return_value={}
                ),
                patch.object(contract, "_rollback") as rollback_call,
            ):
                with self.assertRaises(contract.ReleaseContractError):
                    contract.promote(receipt_path)
            self.assertEqual(
                contract._load_receipt(receipt_path)["state"],
                "ROLLED_BACK_VERIFIED_AFTER_FAILED_PROMOTION",
            )
            rollback_call.assert_not_called()

    def test_deployment_api_requires_ready_pinned_held_target(self) -> None:
        payload = {
            "id": "dpl_test",
            "readyState": "READY",
            "target": "production",
            "url": "test.vercel.app",
            "projectId": "project-pin",
            "team": {"id": "org-pin"},
            "alias": ["automatic.vercel.app"],
        }
        with patch.dict(
            os.environ,
            {
                contract.PROJECT_PIN_ENV: "project-pin",
                contract.ORG_PIN_ENV: "org-pin",
            },
            clear=False,
        ):
            contract._validate_deployment_api(payload, "dpl_test", require_held=True)
            branded = dict(payload, alias=["emergentism.org"])
            with self.assertRaises(contract.ReleaseContractError):
                contract._validate_deployment_api(branded, "dpl_test", require_held=True)
            wrong_state = dict(payload, readyState="BLOCKED")
            with self.assertRaises(contract.ReleaseContractError):
                contract._validate_deployment_api(wrong_state, "dpl_test", require_held=True)
            with self.assertRaises(contract.ReleaseContractError):
                contract._validate_deployment_api(
                    payload,
                    "dpl_test",
                    require_held=True,
                    expected_url="https://different.vercel.app",
                )

    def test_receipt_must_live_outside_repository(self) -> None:
        inside = contract.REPO_ROOT / "receipt.json"
        with self.assertRaises(contract.ReleaseContractError):
            contract._assert_external_receipt(inside)


if __name__ == "__main__":
    unittest.main()
