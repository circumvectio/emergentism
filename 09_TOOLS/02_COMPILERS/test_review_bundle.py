#!/usr/bin/env python3
"""Mutation controls for review-bundle readiness projection."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_review_bundle.py"
SPEC = importlib.util.spec_from_file_location("check_review_bundle", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
BUNDLE_DIR = ROOT / "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice"
MANIFEST_PATH = BUNDLE_DIR / "REVIEW_BUNDLE_v4.json"
PACKET_PATH = BUNDLE_DIR / "REVIEW_BUNDLE_v4.md"


class ReviewBundleStatusTests(unittest.TestCase):
    def test_live_packet_matches_blocked_registry(self) -> None:
        state = CHECKER.review_execution_state()
        packet = PACKET_PATH.read_text(encoding="utf-8")
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        registry, gate = CHECKER.review_gate_data()
        self.assertEqual(state, "blocked")
        self.assertEqual(CHECKER.document_status_errors(packet, state), [])
        packet_relative = PACKET_PATH.relative_to(ROOT).as_posix()
        self.assertEqual(
            manifest["files"].get(packet_relative), "sha256:" + CHECKER.sha256(PACKET_PATH)
        )
        self.assertEqual(
            CHECKER.acyclic_binding_errors(MANIFEST_PATH, manifest, registry, gate, 4),
            [],
        )

    def test_projection_excludes_runtime_but_tracks_static_contract(self) -> None:
        registry, _ = CHECKER.review_gate_data()
        runtime_mutation = copy.deepcopy(registry)
        runtime_mutation["external_state"]["reviewers_engaged"]["state"] = "present"
        runtime_mutation["gates"][1]["execution"]["prerequisites"]["bundle_manifest"]["sha256"] = "0" * 64
        self.assertEqual(
            CHECKER.review_registry_projection(runtime_mutation),
            CHECKER.review_registry_projection(registry),
        )
        static_mutation = copy.deepcopy(registry)
        static_mutation["gates"][1]["execution"]["ready_when"] += " changed"
        self.assertNotEqual(
            CHECKER.review_registry_projection(static_mutation),
            CHECKER.review_registry_projection(registry),
        )
        authority_mutation = copy.deepcopy(registry)
        authority_mutation["gates"][1]["execution"]["provenance_contract"][
            "owner_authority"
        ]["state_at_freeze"] = "selected"
        self.assertNotEqual(
            CHECKER.review_registry_projection(authority_mutation),
            CHECKER.review_registry_projection(registry),
        )

    def test_mutable_self_binding_files_are_rejected(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        forbidden = (
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/GATE_REGISTRY.json",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v4.json",
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v4_BINDING_RECEIPT.json",
        )
        for path in forbidden:
            with self.subTest(path=path):
                mutated = copy.deepcopy(manifest)
                mutated["files"][path] = "sha256:" + "0" * 64
                errors = CHECKER.acyclic_binding_errors(
                    MANIFEST_PATH, mutated, registry, gate, 4
                )
                self.assertTrue(
                    any("must not hash mutable/self-binding" in error for error in errors),
                    errors,
                )

    def test_v4_cannot_downgrade_its_binding_profile(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        downgraded = copy.deepcopy(manifest)
        downgraded["registry_binding"]["mode"] = CHECKER.BINDING_MODE_V1
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, downgraded, registry, gate, 4
        )
        self.assertTrue(
            any("bundle v4 must use" in error for error in errors), errors
        )

    def test_v4_cannot_rebind_its_contract_to_another_listed_artifact(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        rebound = copy.deepcopy(manifest)
        rebound["registry_binding"]["binding_contract"] = "01_TELEOLOGY/04_THE_LIVED_COMPASS.md"
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, rebound, registry, gate, 4
        )
        self.assertTrue(
            any("bundle v4 must bind" in error for error in errors), errors
        )

    def test_unregistered_successor_version_fails_closed(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, manifest, registry, gate, 5
        )
        self.assertTrue(
            any("bundle v5 is unsupported" in error for error in errors), errors
        )

    def test_v4_hash_locks_every_retained_historical_artifact(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        files = copy.deepcopy(manifest["files"])
        self.assertEqual(
            CHECKER.historical_custody_errors(4, files, manifest),
            [],
        )
        retained = next(iter(CHECKER.HISTORICAL_BUNDLE_CUSTODY[1]["artifacts"]))
        files[retained] = "sha256:" + "0" * 64
        errors = CHECKER.historical_custody_errors(4, files, manifest)
        self.assertTrue(
            any("does not hash-lock retained v1 artifact" in error for error in errors),
            errors,
        )

    def test_v4_historical_metadata_distinguishes_creation_and_content_commits(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        custody = manifest["historical_artifact_custody"]["versions"]
        v2_markdown = (
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
            "REVIEW_BUNDLE_v2.md"
        )
        self.assertEqual(
            custody["v2"]["version_created_commit"],
            "b7e0d00dd47d1d784b6c563a4246dc2c3e1a98f8",
        )
        self.assertEqual(
            custody["v2"]["artifacts"][v2_markdown]["content_commit"],
            "eeb7b6ac0ae294a4e65a59bfdd6dfbb10367108e",
        )

        bad_manifest = copy.deepcopy(manifest)
        bad_manifest["historical_artifact_custody"]["versions"]["v2"]["artifacts"][
            v2_markdown
        ]["content_commit"] = "b7e0d00dd47d1d784b6c563a4246dc2c3e1a98f8"
        bad_custody = copy.deepcopy(CHECKER.HISTORICAL_BUNDLE_CUSTODY)
        bad_custody[2]["artifacts"][v2_markdown]["content_commit"] = (
            "b7e0d00dd47d1d784b6c563a4246dc2c3e1a98f8"
        )
        with mock.patch.object(CHECKER, "HISTORICAL_BUNDLE_CUSTODY", bad_custody):
            errors = CHECKER.historical_custody_errors(4, manifest["files"], bad_manifest)
        self.assertTrue(
            any("content commit does not match its frozen digest" in error for error in errors),
            errors,
        )

    def test_missing_local_history_is_reported_without_invalidating_retained_bytes(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        unavailable: list[str] = []
        with mock.patch.object(
            CHECKER,
            "_git_commit_unavailable",
            side_effect=lambda _commit, label: f"{label} Git commit is not locally available",
        ):
            errors = CHECKER.historical_custody_errors(
                4,
                manifest["files"],
                manifest,
                unavailable,
            )
        self.assertEqual(errors, [])
        self.assertEqual(len(unavailable), 4)
        self.assertTrue(all("not locally available" in detail for detail in unavailable))

    def test_v4_requires_its_exact_current_packet_inventory(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            set(manifest["files"]),
            set(CHECKER.required_manifest_files(4)),
        )
        removed = copy.deepcopy(manifest)
        removed["files"].pop(
            "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
            "02_INDEPENDENT_REVIEW.md"
        )
        errors = CHECKER.acyclic_binding_errors(MANIFEST_PATH, removed, registry, gate, 4)
        self.assertTrue(
            any("exact current packet inventory; missing" in error for error in errors),
            errors,
        )
        added = copy.deepcopy(manifest)
        added["files"]["00_META/claim_cards/extra.yaml"] = "sha256:" + "0" * 64
        errors = CHECKER.acyclic_binding_errors(MANIFEST_PATH, added, registry, gate, 4)
        self.assertTrue(
            any("exact current packet inventory; unexpected" in error for error in errors),
            errors,
        )

    def test_wrong_binding_digest_and_human_prerequisites_fail_closed(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        bad_registry = copy.deepcopy(registry)
        bad_gate = bad_registry["gates"][1]
        bad_gate["execution"]["prerequisites"]["bundle_manifest"]["sha256"] = "0" * 64
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, manifest, bad_registry, bad_gate, 4
        )
        self.assertTrue(any("artifact digest drifted" in error for error in errors), errors)

        prerequisites = gate["execution"]["prerequisites"]
        self.assertEqual(prerequisites["bundle_manifest"]["state"], "satisfied")
        remaining = set(prerequisites) - {"bundle_manifest"}
        self.assertEqual(remaining, CHECKER.REMAINING_REVIEW_PREREQUISITES)
        self.assertTrue(all(prerequisites[name]["state"] == "missing" for name in remaining))
        self.assertEqual(gate["execution"]["state"], "blocked")

    def test_unset_owner_authority_rejects_generic_hash_promotion(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        promoted_registry = copy.deepcopy(registry)
        promoted_gate = promoted_registry["gates"][1]
        generic = ROOT / "00_META" / "00_FINITY_PRACTICE_CLAIM_CARD_SET_01.md"
        generic_relative = generic.relative_to(ROOT).as_posix()
        generic_digest = CHECKER.sha256(generic)
        for name in CHECKER.REMAINING_REVIEW_PREREQUISITES:
            promoted_gate["execution"]["prerequisites"][name].update(
                state="satisfied",
                artifact=generic_relative,
                sha256=generic_digest,
                receipt=generic_relative,
                receipt_sha256=generic_digest,
            )
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, manifest, promoted_registry, promoted_gate, 4
        )
        self.assertTrue(
            any("unset owner authority requires" in error for error in errors), errors
        )

    def test_locally_authored_owner_selection_is_not_a_v4_authority(self) -> None:
        registry, gate = CHECKER.review_gate_data()
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        selected_registry = copy.deepcopy(registry)
        selected_gate = selected_registry["gates"][1]
        selected_gate["execution"]["provenance_contract"]["owner_authority"].update(
            state_at_freeze="selected",
            selection={"locally_authored": True},
        )
        errors = CHECKER.acyclic_binding_errors(
            MANIFEST_PATH, manifest, selected_registry, selected_gate, 4
        )
        self.assertTrue(
            any("v4 accepts only unset owner authority" in error for error in errors),
            errors,
        )

    def test_provenance_assignment_types_are_not_coerced(self) -> None:
        registry, _ = CHECKER.review_gate_data()
        cases = (
            ("conflict_form", "requires_owner_authority", 1, "must be a JSON boolean"),
            ("bundle_manifest", "requires_owner_authority", 0, "must be a JSON boolean"),
            ("conflict_form", "requires_external_state", False, "must be a string or null"),
        )
        for name, field, value, expected in cases:
            with self.subTest(name=name, field=field, value=value):
                mutated = copy.deepcopy(registry)
                gate = mutated["gates"][1]
                gate["execution"]["provenance_contract"]["assignments"][name][field] = value
                errors = CHECKER.review_provenance_errors(mutated, gate)
                self.assertTrue(any(expected in error for error in errors), errors)

    def test_ready_to_send_cannot_hide_inside_blocked_packet(self) -> None:
        claims = (
            "READY TO SEND",
            "ready-to-send",
            "contact ready",
            "may now be sent",
        )
        for claim in claims:
            with self.subTest(claim=claim):
                packet = (
                    f"{claim}. not sent. review received: no. "
                    "The reviewer does not work here. CONTACT BLOCKED."
                )
                errors = CHECKER.document_status_errors(packet, "blocked")
                self.assertTrue(
                    any("contact readiness" in error for error in errors), errors
                )

    def test_blocked_packet_requires_explicit_boundary_phrases(self) -> None:
        errors = CHECKER.document_status_errors("CONTACT BLOCKED", "blocked")
        self.assertTrue(any("not sent" in error for error in errors), errors)
        self.assertTrue(any("review received" in error for error in errors), errors)
        self.assertTrue(any("does not work here" in error for error in errors), errors)

    def test_manifest_file_paths_cannot_escape_the_corpus(self) -> None:
        for relative in ("/tmp/outside", "../outside", "./not-canonical", "a/../../outside", "x\x00y"):
            with self.subTest(relative=relative):
                path, error = CHECKER.contained_manifest_file(relative)
                self.assertIsNone(path)
                self.assertIn("safe and repository-relative", error)

        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            corpus = temporary_root / "corpus"
            corpus.mkdir()
            outside = temporary_root / "outside.txt"
            outside.write_text("outside", encoding="utf-8")
            (corpus / "escape").symlink_to(outside)
            with mock.patch.object(CHECKER, "ROOT", corpus):
                path, error = CHECKER.contained_manifest_file("escape")
            self.assertIsNone(path)
            self.assertIn("must not traverse a symlink", error)

            real_directory = corpus / "real"
            real_directory.mkdir()
            (real_directory / "proof.json").write_text("{}", encoding="utf-8")
            (corpus / "alias").symlink_to(real_directory, target_is_directory=True)
            with mock.patch.object(CHECKER, "ROOT", corpus):
                path, error = CHECKER.contained_manifest_file("alias/proof.json")
            self.assertIsNone(path)
            self.assertIn("must not traverse a symlink", error)

            bundle_dir = corpus / "finity"
            bundle_dir.mkdir()
            (bundle_dir / "REVIEW_BUNDLE_v1.json").write_text(
                json.dumps(
                    {
                        "bundleVersion": "v1",
                        "frozen": "test",
                        "files": {"/tmp/outside": "sha256:" + "0" * 64},
                    }
                ),
                encoding="utf-8",
            )
            (bundle_dir / "REVIEW_BUNDLE_v1.md").write_text(
                "not sent; review received: no; does not work here; CONTACT BLOCKED.",
                encoding="utf-8",
            )
            output = io.StringIO()
            with (
                mock.patch.object(CHECKER, "ROOT", corpus),
                mock.patch.object(CHECKER, "DIR", bundle_dir),
                mock.patch.object(CHECKER, "review_gate_data", return_value=({}, {})),
                mock.patch.object(CHECKER, "review_execution_state", return_value="blocked"),
                redirect_stdout(output),
            ):
                self.assertEqual(CHECKER.main(), 1)
            self.assertIn("safe and repository-relative", output.getvalue())

    def test_duplicate_json_keys_and_binding_receipt_symlinks_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            duplicate = temporary_root / "duplicate.json"
            duplicate.write_text('{"state": "absent", "state": "present"}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                CHECKER.load_json_object(duplicate, "duplicate fixture")

            corpus = temporary_root / "corpus"
            bundle = corpus / "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice"
            bundle.mkdir(parents=True)
            registry, gate = CHECKER.review_gate_data()
            synthetic_gate = copy.deepcopy(gate)
            manifest_relative = (
                "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
                "REVIEW_BUNDLE_v3.json"
            )
            snapshot_relative = (
                "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
                "REVIEW_REGISTRY_SNAPSHOT_v3.json"
            )
            contract_relative = (
                "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
                "REVIEW_BUNDLE_BINDING_CONTRACT_v1.md"
            )
            receipt_relative = (
                "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/"
                "REVIEW_BUNDLE_v3_BINDING_RECEIPT.json"
            )
            contract = bundle / "REVIEW_BUNDLE_BINDING_CONTRACT_v1.md"
            contract.write_text("contract", encoding="utf-8")
            projection = CHECKER.review_registry_projection(registry, CHECKER.BINDING_MODE_V1)
            snapshot = {
                "schema": CHECKER.SNAPSHOT_SCHEMA_V1,
                "frozen": "test",
                "purpose": "test",
                "binding_contract": contract_relative,
                "projection": projection,
                "projection_sha256": hashlib.sha256(
                    CHECKER.canonical_json(projection)
                ).hexdigest(),
            }
            snapshot_path = bundle / "REVIEW_REGISTRY_SNAPSHOT_v3.json"
            snapshot_path.write_text(json.dumps(snapshot), encoding="utf-8")
            manifest = {
                "supersedes": "REVIEW_BUNDLE_v2.json",
                "files": {
                    snapshot_relative: "sha256:" + CHECKER.sha256(snapshot_path),
                    contract_relative: "sha256:" + CHECKER.sha256(contract),
                },
                "registry_binding": {
                    "mode": CHECKER.BINDING_MODE_V1,
                    "snapshot": snapshot_relative,
                    "binding_contract": contract_relative,
                    "live_registry": CHECKER.REGISTRY_REL.as_posix(),
                    "binding_receipt": receipt_relative,
                    "excludes": [CHECKER.REGISTRY_REL.as_posix(), manifest_relative, receipt_relative],
                },
            }
            manifest_path = bundle / "REVIEW_BUNDLE_v3.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            outside_receipt = temporary_root / "outside-receipt.json"
            outside_receipt.write_text("{}", encoding="utf-8")
            (bundle / "REVIEW_BUNDLE_v3_BINDING_RECEIPT.json").symlink_to(outside_receipt)
            synthetic_gate["execution"]["prerequisites"]["bundle_manifest"] = {
                "state": "satisfied",
                "artifact": manifest_relative,
                "sha256": CHECKER.sha256(manifest_path),
                "receipt": receipt_relative,
                "receipt_sha256": "0" * 64,
            }
            with mock.patch.object(CHECKER, "ROOT", corpus):
                errors = CHECKER.acyclic_binding_errors(
                    manifest_path, manifest, registry, synthetic_gate, 3
                )
            self.assertTrue(
                any("must not traverse a symlink" in error for error in errors),
                errors,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
