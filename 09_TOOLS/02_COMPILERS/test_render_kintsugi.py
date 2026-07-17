from __future__ import annotations

import contextlib
import dataclasses
import inspect
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

from kintsugi_kernel.codec import canonical_json_bytes, load_canonical_json, raw_hash
from kintsugi_kernel.diagnostics import KintsugiError
from kintsugi_kernel.gitstate import _transition_lock
from kintsugi_kernel.markdown import synchronize_receipt_markdown
from kintsugi_test_support import (
    build_ledger_markdown,
    build_receipt_markdown,
    build_review_markdown,
    build_synthetic_git_repository,
    build_synthetic_manifest_core,
)


CORE_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
LEDGER_PATH = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"


def phase_receipt(core: dict[str, object], phase: str = "B") -> dict[str, object]:
    matches = [
        value
        for value in core["phaseReceipts"]
        if isinstance(value, dict) and value.get("phase") == phase
    ]
    if len(matches) != 1:
        raise AssertionError(f"expected one synthetic Phase {phase} receipt")
    return matches[0]


def current_attempt(core: dict[str, object], phase: str = "B") -> dict[str, object]:
    attempt_id = phase_receipt(core, phase)["reviewAttemptId"]
    matches = [
        value
        for value in core["reviewAttempts"]
        if isinstance(value, dict) and value.get("id") == attempt_id
    ]
    if len(matches) != 1:
        raise AssertionError(f"expected one current Phase {phase} attempt")
    return matches[0]


def current_artifact(core: dict[str, object], phase: str = "B") -> dict[str, object]:
    attempt_id = current_attempt(core, phase)["id"]
    matches = [
        value
        for value in core["reviewAttemptArtifacts"]
        if isinstance(value, dict) and value.get("attemptId") == attempt_id
    ]
    if len(matches) != 1:
        raise AssertionError(f"expected one current Phase {phase} artifact")
    return matches[0]


class RendererFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(
            Path(self.temporary.name), include_phase_a_artifacts=True
        )
        self.core = build_synthetic_manifest_core(
            self.fixture, include_verified_phase_a=True
        )
        self.core_file = self.fixture.isolated_root / CORE_PATH
        self.receipt = phase_receipt(self.core)
        self.receipt_file = self.fixture.isolated_root / self.receipt["path"]
        self.ledger_file = self.fixture.isolated_root / LEDGER_PATH
        self.core_file.write_bytes(canonical_json_bytes(self.core))
        self.receipt_file.write_bytes(build_receipt_markdown(self.receipt))
        self.ledger_file.write_bytes(build_ledger_markdown([]))

    def rendering(self):
        import kintsugi_kernel.rendering as rendering

        return rendering

    def request(self, **changes: object):
        rendering = self.rendering()
        values: dict[str, object] = {
            "operation": "freeze-manifest",
            "phase": "B",
            "stage": None,
            "core_path": CORE_PATH,
            "output_path": CORE_PATH,
            "canonical_root": self.fixture.canonical_root,
            "base_ref": "MANIFEST",
            "expected_head": self.fixture.base_commit,
            "expected_core_sha256": raw_hash(self.core_file.read_bytes()),
            "logic_review_input": None,
            "btj_review_input": None,
            "finding_dispositions_input": None,
            "abandon_reason": None,
        }
        values.update(changes)
        return rendering.RenderTransactionRequest(**values)

    def write(self, request=None) -> None:
        rendering = self.rendering()
        rendering.write_rendered_value(
            self.fixture.isolated_root,
            request=self.request() if request is None else request,
        )

    def git_status(self) -> bytes:
        return subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def temp_paths(self) -> list[Path]:
        return sorted(
            path
            for path in self.fixture.isolated_root.rglob("*")
            if ".kintsugi-" in path.name and path.is_file()
        )


class RendererPublicSurfaceTests(RendererFixture):
    def test_public_surface_is_one_frozen_operation_aware_writer(self) -> None:
        rendering = self.rendering()

        self.assertEqual(
            rendering.__all__,
            ["RenderTransactionRequest", "write_rendered_value"],
        )
        self.assertTrue(dataclasses.is_dataclass(rendering.RenderTransactionRequest))
        request = self.request()
        with self.assertRaises(dataclasses.FrozenInstanceError):
            request.operation = "bundle"
        signature = inspect.signature(rendering.write_rendered_value)
        self.assertEqual(tuple(signature.parameters), ("root", "request"))
        self.assertEqual(
            signature.parameters["request"].kind,
            inspect.Parameter.KEYWORD_ONLY,
        )
        self.assertFalse(hasattr(rendering, "atomic_write_canonical"))

    def test_request_declares_the_exact_frozen_field_set(self) -> None:
        rendering = self.rendering()

        self.assertEqual(
            tuple(field.name for field in dataclasses.fields(rendering.RenderTransactionRequest)),
            (
                "operation",
                "phase",
                "stage",
                "core_path",
                "output_path",
                "canonical_root",
                "base_ref",
                "expected_head",
                "expected_core_sha256",
                "logic_review_input",
                "btj_review_input",
                "finding_dispositions_input",
                "abandon_reason",
            ),
        )

    def test_six_argument_raw_writer_call_is_impossible(self) -> None:
        rendering = self.rendering()

        with self.assertRaises(TypeError):
            rendering.write_rendered_value(
                self.fixture.isolated_root,
                "freeze-manifest",
                "B",
                CORE_PATH,
                self.fixture.base_commit,
                raw_hash(self.core_file.read_bytes()),
            )


class RendererRequestLawTests(RendererFixture):
    def assertRequestError(self, code: str, **changes: object) -> None:
        with self.assertRaises(KintsugiError) as caught:
            self.write(self.request(**changes))
        self.assertEqual(caught.exception.code, code)

    def test_operation_and_stage_matrix_is_closed(self) -> None:
        cases = (
            ({"operation": "unknown"}, "KIN-E-CLI"),
            ({"operation": "freeze-manifest", "stage": "COMPLETE"}, "KIN-E-CLI"),
            ({"operation": "review-target", "stage": "ATTESTED"}, "KIN-E-CLI"),
            ({"operation": "bundle", "stage": "VERIFIED"}, "KIN-E-CLI"),
            ({"operation": "transition-core", "stage": None}, "KIN-E-CLI"),
            ({"operation": "transition-core", "stage": "TARGET_READY"}, "KIN-E-CLI"),
        )
        for changes, code in cases:
            with self.subTest(changes=changes):
                self.assertRequestError(code, **changes)

    def test_operation_irrelevant_inputs_fail_closed(self) -> None:
        external = Path(self.temporary.name) / "external.json"
        external.write_bytes(b"[]\n")
        cases = (
            {"logic_review_input": external},
            {"btj_review_input": external},
            {"abandon_reason": "not abandoned"},
            {
                "operation": "review-target",
                "output_path": CORE_PATH,
                "finding_dispositions_input": external,
            },
            {
                "operation": "transition-core",
                "stage": "ATTESTED",
                "output_path": CORE_PATH,
                "finding_dispositions_input": external,
            },
            {
                "operation": "transition-core",
                "stage": "FAILED",
                "output_path": CORE_PATH,
                "abandon_reason": "wrong stage",
            },
        )
        for changes in cases:
            with self.subTest(changes=changes):
                self.assertRequestError("KIN-E-CLI", **changes)

    def test_abandoned_requires_a_nonempty_reason(self) -> None:
        for reason in (None, "", "   "):
            with self.subTest(reason=reason):
                self.assertRequestError(
                    "KIN-E-CLI",
                    operation="transition-core",
                    stage="ABANDONED",
                    output_path=CORE_PATH,
                    abandon_reason=reason,
                )

    def test_mutating_request_requires_well_formed_cas_expectations(self) -> None:
        for changes in (
            {"expected_head": "f" * 39},
            {"expected_head": "G" * 40},
            {"expected_core_sha256": "sha256:" + "f" * 63},
            {"expected_core_sha256": "sha256:" + "G" * 64},
        ):
            with self.subTest(changes=changes):
                self.assertRequestError("KIN-E-CLI", **changes)

    def test_output_must_be_repository_relative_allowed_and_unprotected(self) -> None:
        cases = (
            ({"output_path": "../escape.json"}, "KIN-E-PATH"),
            ({"output_path": "/tmp/escape.json"}, "KIN-E-PATH"),
            ({"output_path": "03_METHODOLOGY/not-allowed.json"}, "KIN-E-SCOPE"),
            ({"output_path": "12_PUBLIC_SITE/blocked.json"}, "KIN-E-PROTECTED"),
        )
        for changes, code in cases:
            with self.subTest(changes=changes):
                self.assertRequestError(code, **changes)

    def test_external_intake_must_remain_outside_both_worktrees(self) -> None:
        inside = self.fixture.isolated_root / "candidate-review.md"
        inside.write_bytes(b"candidate\n")
        with self.assertRaises(KintsugiError) as caught:
            self.write(self.request(finding_dispositions_input=inside))
        self.assertEqual(caught.exception.code, "KIN-E-PATH")

    def test_external_intake_rejects_leaf_parent_symlinks_and_hardlinks(self) -> None:
        candidate = Path(self.temporary.name) / "external-candidate.json"
        candidate.write_bytes(b"[]\n")
        leaf_link = Path(self.temporary.name) / "leaf-link.json"
        leaf_link.symlink_to(candidate)
        parent = Path(self.temporary.name) / "candidate-parent"
        parent.mkdir()
        nested = parent / "candidate.json"
        nested.write_bytes(b"[]\n")
        parent_link = Path(self.temporary.name) / "parent-link"
        parent_link.symlink_to(parent, target_is_directory=True)
        hardlink = Path(self.temporary.name) / "candidate-hardlink.json"
        os.link(candidate, hardlink)

        for path in (leaf_link, parent_link / "candidate.json", hardlink):
            with self.subTest(path=path):
                with self.assertRaises(KintsugiError) as caught:
                    self.write(self.request(finding_dispositions_input=path))
                self.assertEqual(caught.exception.code, "KIN-E-PATH")
        self.assertFalse(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").exists()
        )


class RendererCasAndLockTests(RendererFixture):
    def test_stale_head_and_core_are_rejected_before_write(self) -> None:
        original = self.core_file.read_bytes()
        for request in (
            self.request(expected_head="f" * 40),
            self.request(expected_core_sha256="sha256:" + "f" * 64),
        ):
            with self.subTest(request=request):
                with self.assertRaises(KintsugiError) as caught:
                    self.write(request)
                self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
                self.assertEqual(self.core_file.read_bytes(), original)
        self.assertFalse(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").exists()
        )

    def test_shared_git_common_directory_lock_is_mandatory(self) -> None:
        original = self.core_file.read_bytes()
        with _transition_lock(self.fixture.common_dir):
            with self.assertRaises(KintsugiError) as caught:
                self.write()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), original)

    def test_core_is_reloaded_inside_the_lock(self) -> None:
        rendering = self.rendering()
        original_check = rendering._check_head_core_cas
        calls = 0

        def mutate_after_precheck(*args: object, **kwargs: object) -> None:
            nonlocal calls
            calls += 1
            original_check(*args, **kwargs)
            if calls == 1:
                self.core_file.write_bytes(b"{}\n")

        with mock.patch.object(
            rendering,
            "_check_head_core_cas",
            side_effect=mutate_after_precheck,
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertGreaterEqual(calls, 2)
        self.assertFalse(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").exists()
        )


class RendererFreezeTransactionTests(RendererFixture):
    def test_freeze_installs_core_and_receipt_atomically_and_burns_one_id(self) -> None:
        rendering = self.rendering()
        owner = self.fixture.isolated_root / "03_METHODOLOGY/owner.md"
        owner_before = owner.read_bytes()
        replacements: list[tuple[Path, Path]] = []
        real_replace = os.replace

        def record_replace(source: os.PathLike[str], destination: os.PathLike[str]) -> None:
            replacements.append((Path(source), Path(destination)))
            real_replace(source, destination)

        with mock.patch.object(rendering.os, "replace", side_effect=record_replace):
            self.write()

        frozen = load_canonical_json(self.core_file)
        self.assertIsInstance(frozen, dict)
        attempt = current_attempt(frozen)
        self.assertEqual(attempt["id"], "RVA-B-001")
        self.assertEqual(attempt["status"], "PENDING")
        self.assertEqual(phase_receipt(frozen)["reviewAttemptId"], "RVA-B-001")
        synchronized = synchronize_receipt_markdown(
            self.receipt_file.read_bytes(),
            phase_receipt(frozen),
            path=str(self.receipt["path"]),
        )
        self.assertEqual(synchronized.issues, ())
        reservation = (
            self.fixture.common_dir
            / "kintsugi-attempt-reservations/RVA-B-001.json"
        )
        self.assertTrue(reservation.is_file())
        self.assertEqual(owner.read_bytes(), owner_before)
        self.assertTrue(replacements)
        self.assertTrue(all(source.parent == destination.parent for source, destination in replacements))
        self.assertEqual(self.temp_paths(), [])

    def test_final_read_set_drift_aborts_before_first_replace_and_keeps_reservation(self) -> None:
        rendering = self.rendering()
        owner = self.fixture.isolated_root / "03_METHODOLOGY/owner.md"
        core_before = self.core_file.read_bytes()
        receipt_before = self.receipt_file.read_bytes()
        real_recheck = rendering._recheck_read_set
        real_replace = os.replace
        replacements = 0

        def drift_then_recheck(*args: object, **kwargs: object) -> None:
            owner.write_bytes(b"drifted after staging\n")
            real_recheck(*args, **kwargs)

        def count_replace(*args: object, **kwargs: object) -> None:
            nonlocal replacements
            replacements += 1
            real_replace(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=drift_then_recheck
        ), mock.patch.object(rendering.os, "replace", side_effect=count_replace):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(replacements, 0)
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.receipt_file.read_bytes(), receipt_before)
        self.assertTrue(
            (
                self.fixture.common_dir
                / "kintsugi-attempt-reservations/RVA-B-001.json"
            ).is_file()
        )
        self.assertEqual(self.temp_paths(), [])

    def test_removed_read_set_member_aborts_before_replacement(self) -> None:
        rendering = self.rendering()
        owner = self.fixture.isolated_root / "03_METHODOLOGY/owner.md"
        core_before = self.core_file.read_bytes()
        real_recheck = rendering._recheck_read_set

        def remove_then_recheck(*args: object, **kwargs: object) -> None:
            owner.unlink()
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=remove_then_recheck
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertFalse(owner.exists())
        self.assertEqual(self.temp_paths(), [])

    def test_unreadable_read_set_member_aborts_before_replacement(self) -> None:
        rendering = self.rendering()
        owner = self.fixture.isolated_root / "03_METHODOLOGY/owner.md"
        core_before = self.core_file.read_bytes()
        real_snapshot = rendering._snapshot_file
        final_recheck_started = False

        def unreadable_at_final(path: Path, label: str):
            if final_recheck_started and path == owner:
                raise KintsugiError(
                    "KIN-E-CONCURRENT", label, "injected unreadable read-set member"
                )
            return real_snapshot(path, label)

        real_recheck = rendering._recheck_read_set

        def begin_final_recheck(*args: object, **kwargs: object) -> None:
            nonlocal final_recheck_started
            final_recheck_started = True
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_snapshot_file", side_effect=unreadable_at_final
        ), mock.patch.object(
            rendering, "_recheck_read_set", side_effect=begin_final_recheck
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.temp_paths(), [])

    def test_partial_replace_failure_rolls_back_every_repository_output(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        receipt_before = self.receipt_file.read_bytes()
        real_replace = os.replace
        calls = 0

        def fail_second_replace(source: os.PathLike[str], destination: os.PathLike[str]) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replacement failure")
            real_replace(source, destination)

        with mock.patch.object(rendering.os, "replace", side_effect=fail_second_replace):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.receipt_file.read_bytes(), receipt_before)
        self.assertEqual(self.temp_paths(), [])
        self.assertTrue(
            (
                self.fixture.common_dir
                / "kintsugi-attempt-reservations/RVA-B-001.json"
            ).is_file()
        )

    def test_rollback_backup_uses_the_frozen_snapshot_bytes(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        receipt_before = self.receipt_file.read_bytes()
        real_stage = rendering._stage_output
        real_replace = os.replace
        replace_calls = 0

        def transient_swap(root: Path, output, snapshot):
            if output.relative != CORE_PATH:
                return real_stage(root, output, snapshot)
            self.core_file.write_bytes(b"{}\n")
            try:
                return real_stage(root, output, snapshot)
            finally:
                self.core_file.write_bytes(core_before)

        def fail_second_replace(source, destination):
            nonlocal replace_calls
            replace_calls += 1
            if replace_calls == 2:
                raise OSError("injected replacement failure")
            real_replace(source, destination)

        with mock.patch.object(
            rendering, "_stage_output", side_effect=transient_swap
        ), mock.patch.object(
            rendering.os, "replace", side_effect=fail_second_replace
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.receipt_file.read_bytes(), receipt_before)
        self.assertEqual(self.temp_paths(), [])

    def test_new_closure_file_appearance_is_in_the_final_read_set(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        target = (
            self.fixture.isolated_root
            / "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/"
            "RVA-B-001/review_target.json"
        )
        real_recheck = rendering._recheck_read_set

        def appear_then_recheck(*args: object, **kwargs: object) -> None:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b'{"concurrent":true}\n')
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=appear_then_recheck
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(target.read_bytes(), b'{"concurrent":true}\n')
        self.assertTrue(
            (
                self.fixture.common_dir
                / "kintsugi-attempt-reservations/RVA-B-001.json"
            ).is_file()
        )
        self.assertEqual(self.temp_paths(), [])

    def test_rogue_closure_namespace_entry_aborts_before_replacement(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        rogue = (
            self.fixture.isolated_root
            / "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/ROGUE/extra.json"
        )
        real_recheck = rendering._recheck_read_set

        def inject_rogue(*args: object, **kwargs: object) -> None:
            rogue.parent.mkdir(parents=True, exist_ok=True)
            rogue.write_bytes(b'{}\n')
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=inject_rogue
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(rogue.read_bytes(), b"{}\n")
        self.assertEqual(self.temp_paths(), [])

    def test_parent_directory_inode_swap_is_in_the_final_cas(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        directory = self.fixture.isolated_root / "03_METHODOLOGY"
        original = Path(self.temporary.name) / "original-methodology"
        real_recheck = rendering._recheck_read_set

        def swap_parent(*args: object, **kwargs: object) -> None:
            directory.rename(original)
            shutil.copytree(original, directory, symlinks=True)
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=swap_parent
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.temp_paths(), [])

    def test_git_index_metadata_drift_is_in_the_final_cas(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        real_recheck = rendering._recheck_read_set

        def mutate_index(*args: object, **kwargs: object) -> None:
            subprocess.run(
                [
                    "git",
                    "update-index",
                    "--assume-unchanged",
                    "--",
                    "03_METHODOLOGY/owner.md",
                ],
                cwd=self.fixture.isolated_root,
                check=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=mutate_index
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.temp_paths(), [])

    def test_cross_phase_closure_drift_is_in_the_final_read_set(self) -> None:
        rendering = self.rendering()
        phase_a_attempt = current_attempt(self.core, "A")
        target = self.fixture.isolated_root / phase_a_attempt["reviewTargetPath"]
        core_before = self.core_file.read_bytes()
        real_recheck = rendering._recheck_read_set

        def drift_dependency(*args: object, **kwargs: object) -> None:
            target.write_bytes(b'{"drifted":true}\n')
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=drift_dependency
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(target.read_bytes(), b'{"drifted":true}\n')
        self.assertEqual(self.temp_paths(), [])

    def test_retargeted_protected_symlink_is_in_the_final_read_set(self) -> None:
        rendering = self.rendering()
        link = self.fixture.isolated_root / "12_PUBLIC_SITE/assets-link"
        self.assertTrue(link.is_symlink())
        core_before = self.core_file.read_bytes()
        real_recheck = rendering._recheck_read_set

        def retarget_then_recheck(*args: object, **kwargs: object) -> None:
            link.unlink()
            link.symlink_to(".", target_is_directory=True)
            real_recheck(*args, **kwargs)

        with mock.patch.object(
            rendering, "_recheck_read_set", side_effect=retarget_then_recheck
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(os.readlink(link), ".")
        self.assertTrue(
            (
                self.fixture.common_dir
                / "kintsugi-attempt-reservations/RVA-B-001.json"
            ).is_file()
        )
        self.assertEqual(self.temp_paths(), [])

    def test_post_replace_directory_fsync_failure_rolls_back(self) -> None:
        rendering = self.rendering()
        core_before = self.core_file.read_bytes()
        receipt_before = self.receipt_file.read_bytes()
        real_fsync = rendering._fsync_directory

        def fail_transaction_fsync(directory: Path, context: str) -> None:
            if context == "transaction":
                raise KintsugiError(
                    "KIN-E-CONCURRENT", context, "injected directory fsync failure"
                )
            real_fsync(directory, context)

        with mock.patch.object(
            rendering, "_fsync_directory", side_effect=fail_transaction_fsync
        ):
            with self.assertRaises(KintsugiError) as caught:
                self.write()

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(self.core_file.read_bytes(), core_before)
        self.assertEqual(self.receipt_file.read_bytes(), receipt_before)
        self.assertEqual(self.temp_paths(), [])

    def test_unbounded_disposition_json_is_a_controlled_error_before_reservation(self) -> None:
        candidate = Path(self.temporary.name) / "oversized-disposition.json"
        candidate.write_text("[" + "9" * 5000 + "]\n", encoding="ascii")

        with self.assertRaises(KintsugiError) as caught:
            self.write(self.request(finding_dispositions_input=candidate))

        self.assertEqual(caught.exception.code, "KIN-E-JSON")
        self.assertFalse(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").exists()
        )

    def test_stale_retry_cannot_allocate_another_attempt(self) -> None:
        request = self.request()
        self.write(request)
        with self.assertRaises(KintsugiError) as caught:
            self.write(request)
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        reservations = sorted(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").glob("*.json")
        )
        self.assertEqual([path.name for path in reservations], ["RVA-B-001.json"])


class RendererReviewLifecycleTests(RendererFixture):
    def freeze(self) -> dict[str, object]:
        self.write()
        value = load_canonical_json(self.core_file)
        self.assertIsInstance(value, dict)
        return value

    def call(
        self,
        operation: str,
        output_path: str,
        *,
        stage: str | None = None,
        logic: Path | None = None,
        btj: Path | None = None,
        reason: str | None = None,
    ) -> None:
        self.write(self.request(
            operation=operation,
            stage=stage,
            output_path=output_path,
            base_ref=None,
            logic_review_input=logic,
            btj_review_input=btj,
            abandon_reason=reason,
        ))

    def review_candidate(
        self,
        core: dict[str, object],
        kind: str,
        *,
        verdict: str = "PASS",
        severe: bool = False,
    ) -> Path:
        attempt = current_attempt(core)
        artifact = current_artifact(core)
        ordinal = attempt["id"].rsplit("-", 1)[1]
        finding_id = f"FND-B-{kind}-001"
        findings = []
        if severe:
            receipt = phase_receipt(core)
            manifests = [
                value
                for value in core["manifests"]
                if isinstance(value, dict) and value.get("phase") == "B"
            ]
            if len(manifests) != 1:
                raise AssertionError("expected one synthetic Phase B manifest")
            findings = [{
                "id": finding_id,
                "attemptId": attempt["id"],
                "reviewKind": kind,
                "category": "LOGIC" if kind == "LOGIC" else "JUSTICE",
                "severity": "MAJOR",
                "statement": "A bounded renderer integration finding.",
                "claimIds": [receipt["claimIds"][0]],
                "seamIds": [],
                "ledgerSectionIds": [],
                "receiptIds": [attempt["receiptId"]],
                "subjectPaths": [manifests[0]["finalFiles"][0]["path"]],
            }]
        attestation = {
            "id": f"ATT-{kind}-B-{ordinal}",
            "kind": kind,
            "path": attempt[
                "logicReviewPath" if kind == "LOGIC" else "btjReviewPath"
            ],
            "receiptId": attempt["receiptId"],
            "reviewerId": f"independent-{kind.lower()}",
            "reviewerRole": f"Independent {kind} reviewer",
            "independenceStatement": "No implementation role in this attempt.",
            "reviewTargetDigest": artifact["reviewTargetSha256"],
            "verdict": verdict,
            "findingIds": [finding_id] if severe else [],
            "openSevereFindingIds": [finding_id] if severe and verdict == "FAIL" else [],
            "approvedUpgradeSeamIds": [],
            "approvedGateSeamIds": [],
            "attemptId": attempt["id"],
        }
        path = Path(self.temporary.name) / f"candidate-{kind.lower()}.md"
        path.write_bytes(build_review_markdown(attestation, findings))
        return path

    def target_ready(self) -> dict[str, object]:
        core = self.freeze()
        attempt = current_attempt(core)
        self.call("review-target", attempt["reviewTargetPath"])
        ready = load_canonical_json(self.core_file)
        self.assertIsInstance(ready, dict)
        return ready

    def test_review_target_is_atomic_retry_identical_and_drift_refusing(self) -> None:
        core = self.freeze()
        attempt = current_attempt(core)
        target = self.fixture.isolated_root / attempt["reviewTargetPath"]
        reservation_count = len(list(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").glob("*.json")
        ))

        self.call("review-target", attempt["reviewTargetPath"])
        ready = load_canonical_json(self.core_file)
        target_before = target.read_bytes()
        target_inode = target.stat().st_ino
        core_inode = self.core_file.stat().st_ino
        self.assertEqual(
            current_artifact(ready)["reviewTargetSha256"],
            raw_hash(target_before),
        )
        with mock.patch.object(self.rendering().os, "replace") as replacement:
            self.call("review-target", attempt["reviewTargetPath"])
        replacement.assert_not_called()
        self.assertEqual(target.read_bytes(), target_before)
        self.assertEqual(target.stat().st_ino, target_inode)
        self.assertEqual(self.core_file.stat().st_ino, core_inode)
        self.assertEqual(
            len(list(
                (self.fixture.common_dir / "kintsugi-attempt-reservations").glob("*.json")
            )),
            reservation_count,
        )

        target.write_bytes(b'{"drifted":true}\n')
        core_before = self.core_file.read_bytes()
        with self.assertRaises(KintsugiError) as caught:
            self.call("review-target", attempt["reviewTargetPath"])
        self.assertEqual(caught.exception.code, "KIN-E-BUNDLE")
        self.assertEqual(self.core_file.read_bytes(), core_before)

    def test_unrecorded_preexisting_target_is_never_adopted(self) -> None:
        frozen = self.freeze()
        attempt = current_attempt(frozen)
        target = self.fixture.isolated_root / attempt["reviewTargetPath"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'{}\n')
        before = self.core_file.read_bytes()

        with self.assertRaises(KintsugiError) as caught:
            self.call("review-target", attempt["reviewTargetPath"])

        self.assertEqual(caught.exception.code, "KIN-E-BUNDLE")
        self.assertEqual(self.core_file.read_bytes(), before)
        self.assertEqual(target.read_bytes(), b"{}\n")

    def test_standalone_bundle_rejects_noncomplete_state(self) -> None:
        ready = self.target_ready()
        attempt = current_attempt(ready)
        bundle = self.fixture.isolated_root / attempt["validationBundlePath"]

        with self.assertRaises(KintsugiError) as caught:
            self.call("bundle", attempt["validationBundlePath"])

        self.assertEqual(caught.exception.code, "KIN-E-STATE")
        self.assertFalse(bundle.exists())

    def test_attested_complete_bundle_preflight_and_verified_sequence(self) -> None:
        ready = self.target_ready()
        attempt = current_attempt(ready)
        logic = self.review_candidate(ready, "LOGIC")
        self.call(
            "transition-core",
            CORE_PATH,
            stage="ATTESTED",
            logic=logic,
        )
        attested = load_canonical_json(self.core_file)
        self.assertEqual(current_attempt(attested)["status"], "PENDING")
        self.assertTrue(
            (self.fixture.isolated_root / attempt["logicReviewPath"]).is_file()
        )

        btj = self.review_candidate(attested, "BTJ")
        self.call(
            "transition-core",
            CORE_PATH,
            stage="COMPLETE",
            btj=btj,
        )
        complete = load_canonical_json(self.core_file)
        self.assertEqual(current_attempt(complete)["status"], "PASSED")
        self.assertEqual(phase_receipt(complete)["status"], "COMPLETE")
        bundle = self.fixture.isolated_root / attempt["validationBundlePath"]
        self.assertFalse(bundle.exists())

        self.call("bundle", attempt["validationBundlePath"])
        self.assertFalse(bundle.exists())
        self.call("transition-core", CORE_PATH, stage="VERIFIED")
        verified = load_canonical_json(self.core_file)
        self.assertEqual(phase_receipt(verified)["status"], "VERIFIED")
        self.assertEqual(
            phase_receipt(verified)["validationDigest"],
            raw_hash(bundle.read_bytes()),
        )

    def test_failed_and_zero_review_abandoned_preserve_draft_receipt(self) -> None:
        ready = self.target_ready()
        attempt = current_attempt(ready)
        failed_review = self.review_candidate(
            ready, "LOGIC", verdict="FAIL", severe=True
        )
        self.call(
            "transition-core",
            CORE_PATH,
            stage="FAILED",
            logic=failed_review,
        )
        failed = load_canonical_json(self.core_file)
        self.assertEqual(current_attempt(failed)["status"], "FAILED")
        self.assertEqual(phase_receipt(failed)["status"], "DRAFT")

        # A separate fresh fixture exercises the legal zero-review withdrawal.
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_synthetic_git_repository(
                Path(temporary), include_phase_a_artifacts=True
            )
            core = build_synthetic_manifest_core(
                fixture, include_verified_phase_a=True
            )
            receipt = phase_receipt(core)
            core_file = fixture.isolated_root / CORE_PATH
            core_file.write_bytes(canonical_json_bytes(core))
            (fixture.isolated_root / receipt["path"]).write_bytes(
                build_receipt_markdown(receipt)
            )
            (fixture.isolated_root / LEDGER_PATH).write_bytes(build_ledger_markdown([]))
            from kintsugi_kernel.rendering import RenderTransactionRequest, write_rendered_value

            def request(operation, output, stage=None, reason=None):
                return RenderTransactionRequest(
                    operation=operation,
                    phase="B",
                    stage=stage,
                    core_path=CORE_PATH,
                    output_path=output,
                    canonical_root=fixture.canonical_root,
                    base_ref=("MANIFEST" if operation == "freeze-manifest" else None),
                    expected_head=fixture.base_commit,
                    expected_core_sha256=raw_hash(core_file.read_bytes()),
                    abandon_reason=reason,
                )

            write_rendered_value(fixture.isolated_root, request=request("freeze-manifest", CORE_PATH))
            frozen = load_canonical_json(core_file)
            attempt = current_attempt(frozen)
            write_rendered_value(
                fixture.isolated_root,
                request=request("review-target", attempt["reviewTargetPath"]),
            )
            write_rendered_value(
                fixture.isolated_root,
                request=request(
                    "transition-core",
                    CORE_PATH,
                    stage="ABANDONED",
                    reason="The review transport was withdrawn explicitly.",
                ),
            )
            abandoned = load_canonical_json(core_file)
            self.assertEqual(current_attempt(abandoned)["status"], "ABANDONED")
            self.assertEqual(phase_receipt(abandoned)["status"], "DRAFT")

    def test_abandoned_preserves_one_or_two_review_inputs(self) -> None:
        for count in (1, 2):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as temporary:
                fixture = build_synthetic_git_repository(
                    Path(temporary), include_phase_a_artifacts=True
                )
                core = build_synthetic_manifest_core(
                    fixture, include_verified_phase_a=True
                )
                receipt = phase_receipt(core)
                core_file = fixture.isolated_root / CORE_PATH
                core_file.write_bytes(canonical_json_bytes(core))
                (fixture.isolated_root / receipt["path"]).write_bytes(
                    build_receipt_markdown(receipt)
                )
                (fixture.isolated_root / LEDGER_PATH).write_bytes(
                    build_ledger_markdown([])
                )
                rendering = self.rendering()

                def request(
                    operation: str,
                    output: str,
                    *,
                    stage: str | None = None,
                    logic: Path | None = None,
                    btj: Path | None = None,
                    reason: str | None = None,
                ):
                    return rendering.RenderTransactionRequest(
                        operation=operation,
                        phase="B",
                        stage=stage,
                        core_path=CORE_PATH,
                        output_path=output,
                        canonical_root=fixture.canonical_root,
                        base_ref=("MANIFEST" if operation == "freeze-manifest" else None),
                        expected_head=fixture.base_commit,
                        expected_core_sha256=raw_hash(core_file.read_bytes()),
                        logic_review_input=logic,
                        btj_review_input=btj,
                        abandon_reason=reason,
                    )

                rendering.write_rendered_value(
                    fixture.isolated_root,
                    request=request("freeze-manifest", CORE_PATH),
                )
                frozen = load_canonical_json(core_file)
                attempt = current_attempt(frozen)
                rendering.write_rendered_value(
                    fixture.isolated_root,
                    request=request("review-target", attempt["reviewTargetPath"]),
                )
                ready = load_canonical_json(core_file)
                logic = self.review_candidate(ready, "LOGIC")
                btj = self.review_candidate(ready, "BTJ") if count == 2 else None
                rendering.write_rendered_value(
                    fixture.isolated_root,
                    request=request(
                        "transition-core",
                        CORE_PATH,
                        stage="ABANDONED",
                        logic=logic,
                        btj=btj,
                        reason="The bounded review attempt was withdrawn.",
                    ),
                )
                abandoned = load_canonical_json(core_file)
                current = current_attempt(abandoned)
                self.assertEqual(current["status"], "ABANDONED")
                self.assertEqual(
                    len([
                        value
                        for value in abandoned["reviewAttestations"]
                        if value["attemptId"] == current["id"]
                    ]),
                    count,
                )
                self.assertEqual(phase_receipt(abandoned)["status"], "DRAFT")

    def test_complete_rejects_two_fresh_reviews(self) -> None:
        ready = self.target_ready()
        logic = self.review_candidate(ready, "LOGIC")
        btj = self.review_candidate(ready, "BTJ")
        before = self.core_file.read_bytes()

        with self.assertRaises(KintsugiError) as caught:
            self.call(
                "transition-core",
                CORE_PATH,
                stage="COMPLETE",
                logic=logic,
                btj=btj,
            )

        self.assertEqual(caught.exception.code, "KIN-E-STATE")
        self.assertEqual(self.core_file.read_bytes(), before)


class RendererCliTests(unittest.TestCase):
    def test_cli_maps_request_fields_without_writing_itself(self) -> None:
        import render_kintsugi as cli
        from kintsugi_kernel.rendering import RenderTransactionRequest

        captured: list[tuple[Path, RenderTransactionRequest]] = []
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(
            cli,
            "write_rendered_value",
            side_effect=lambda root, *, request: captured.append((root, request)),
        ):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = cli.main([
                    "freeze-manifest",
                    "--final",
                    "--phase", "B",
                    "--base-ref", "MANIFEST",
                    "--canonical-root", "/tmp/canonical",
                    "--expected-head", "a" * 40,
                    "--expected-core-sha256", "sha256:" + "b" * 64,
                    "--output", CORE_PATH,
                ])

        self.assertEqual(code, 0)
        self.assertEqual(len(captured), 1)
        root, request = captured[0]
        self.assertEqual(root, cli.ROOT)
        self.assertEqual(request.operation, "freeze-manifest")
        self.assertEqual(request.phase, "B")
        self.assertEqual(request.output_path, CORE_PATH)
        self.assertEqual(stdout.getvalue(), "KIN-OK render operation=freeze-manifest phase=B stage=FINAL\n")
        self.assertEqual(stderr.getvalue(), "")

    def test_cli_requires_final_for_freeze_and_reports_controlled_error(self) -> None:
        import render_kintsugi as cli

        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli.main([
                "freeze-manifest",
                "--phase", "B",
                "--base-ref", "MANIFEST",
                "--canonical-root", "/tmp/canonical",
                "--expected-head", "a" * 40,
                "--expected-core-sha256", "sha256:" + "b" * 64,
                "--output", CORE_PATH,
            ])

        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("KIN-E-CLI", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_cli_discovers_repository_independently_of_cwd(self) -> None:
        import render_kintsugi as cli

        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            try:
                os.chdir(directory)
                args = cli.build_parser().parse_args([
                    "review-target",
                    "--phase", "B",
                    "--expected-head", "a" * 40,
                    "--expected-core-sha256", "sha256:" + "b" * 64,
                    "--output", "target.json",
                ])
            finally:
                os.chdir(previous)
        self.assertTrue(cli.ROOT.is_absolute())
        self.assertEqual(args.core_path, CORE_PATH)


if __name__ == "__main__":
    unittest.main()
