from __future__ import annotations

import subprocess
import tempfile
import unittest
import os
import copy
import json
import threading
from pathlib import Path
from unittest import mock

from kintsugi_kernel import (
    KintsugiError,
    freeze_manifest_value,
    inspect_git_state,
    resolve_git_common_dir,
    validate_manifest,
)
from kintsugi_kernel.codec import canonical_json_bytes, raw_hash
from kintsugi_kernel.records import attempt_paths
from kintsugi_test_support import (
    ATTEMPT_ID,
    CLAIM_ID,
    build_committed_predecessor_fixture,
    build_ledger_markdown,
    build_receipt_markdown,
    build_review_attempt,
    build_review_finding_disposition,
    build_review_markdown,
    build_synthetic_git_repository,
    build_synthetic_manifest_core,
)


def current_file_record(root: Path, relative: str) -> dict[str, str]:
    path = root / relative
    if path.is_symlink():
        return {"path": relative, "kind": "SYMLINK", "sha256": raw_hash(os.readlink(path).encode("utf-8"))}
    return {"path": relative, "kind": "FILE", "sha256": raw_hash(path.read_bytes())}


class GitManifestSurfaceTests(unittest.TestCase):
    def test_task_five_public_surface_is_importable(self) -> None:
        from kintsugi_kernel import (
            freeze_manifest_value,
            inspect_git_state,
            resolve_git_common_dir,
            validate_manifest,
        )

        self.assertTrue(callable(inspect_git_state))
        self.assertTrue(callable(resolve_git_common_dir))
        self.assertTrue(callable(validate_manifest))
        self.assertTrue(callable(freeze_manifest_value))


class SyntheticGitRepositoryTests(unittest.TestCase):
    def test_factory_builds_main_and_linked_isolated_worktrees(self) -> None:
        from kintsugi_test_support import build_synthetic_git_repository

        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_synthetic_git_repository(Path(temporary))

            self.assertEqual(
                subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=fixture.canonical_root,
                    check=True,
                    stdout=subprocess.PIPE,
                ).stdout,
                b"main\n",
            )
            self.assertEqual(
                subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=fixture.isolated_root,
                    check=True,
                    stdout=subprocess.PIPE,
                ).stdout.decode("ascii").strip(),
                fixture.base_commit,
            )
            self.assertEqual(
                (fixture.canonical_root / "03_METHODOLOGY/owner.md").read_bytes(),
                b"# Synthetic owner\n",
            )
            self.assertTrue((fixture.isolated_root / "12_PUBLIC_SITE/assets-link").is_symlink())
            self.assertTrue((fixture.canonical_root / "scratch/preexisting.txt").exists())
            self.assertTrue((fixture.isolated_root / "scratch/preexisting.txt").exists())

    def test_factory_contains_reserved_control_vessel_and_excluded_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = build_synthetic_git_repository(Path(temporary))

            for relative in (
                "03_METHODOLOGY/excluded.md",
                "03_METHODOLOGY/phase-b-inventory-review.md",
                "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json",
                "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md",
                "11_UPLINK/50_AUDITS_AND_EXECUTIONS/109_ACTIVE_CORPUS_KINTSUGI_RECEIPT_2026_07_11.md",
            ):
                self.assertTrue((fixture.canonical_root / relative).is_file(), relative)
                self.assertTrue((fixture.isolated_root / relative).is_file(), relative)


class GitStateInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))

    def git(self, root: Path, *argv: str) -> bytes:
        return subprocess.run(
            ["git", *argv],
            cwd=root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def test_common_directory_and_clean_state_are_resolved_without_display_parsing(self) -> None:
        isolated = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)
        canonical = inspect_git_state(self.fixture.canonical_root, self.fixture.base_commit)

        self.assertEqual(resolve_git_common_dir(self.fixture.isolated_root), self.fixture.common_dir)
        self.assertEqual(isolated.common_dir, canonical.common_dir)
        self.assertEqual(isolated.base_commit, self.fixture.base_commit)
        self.assertEqual(isolated.head, self.fixture.base_commit)
        self.assertEqual(isolated.branch, "isolated")
        self.assertEqual(canonical.branch, "main")
        self.assertEqual(isolated.committed_paths, ())
        self.assertEqual(isolated.staged_paths, ())
        self.assertEqual(isolated.unstaged_paths, ())
        self.assertEqual(
            tuple(record.path for record in isolated.untracked_records),
            ("scratch/preexisting.txt",),
        )

    def test_diff_parsing_keeps_both_rename_names_and_tab_newline_paths(self) -> None:
        renamed = "03_METHODOLOGY/support\tnew\n.md"
        self.git(
            self.fixture.isolated_root,
            "mv",
            "03_METHODOLOGY/support.md",
            renamed,
        )
        (self.fixture.isolated_root / "03_METHODOLOGY/owner.md").write_bytes(
            b"# Synthetic owner changed\n"
        )
        (self.fixture.isolated_root / "12_PUBLIC_SITE/index.html").unlink()
        untracked = "scratch/tab\tline\n.txt"
        (self.fixture.isolated_root / untracked).write_bytes(b"odd filename\n")

        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)

        self.assertEqual(
            state.staged_paths,
            ("03_METHODOLOGY/support\tnew\n.md", "03_METHODOLOGY/support.md"),
        )
        self.assertEqual(
            state.unstaged_paths,
            ("03_METHODOLOGY/owner.md", "12_PUBLIC_SITE/index.html"),
        )
        self.assertEqual(
            tuple(record.path for record in state.untracked_records),
            ("scratch/preexisting.txt", "scratch/tab\tline\n.txt"),
        )

    def test_committed_paths_are_measured_from_the_selected_base(self) -> None:
        path = self.fixture.isolated_root / "03_METHODOLOGY/committed.md"
        path.write_bytes(b"committed candidate\n")
        self.git(self.fixture.isolated_root, "add", "--", "03_METHODOLOGY/committed.md")
        self.git(self.fixture.isolated_root, "commit", "-m", "candidate commit")

        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)

        self.assertEqual(state.committed_paths, ("03_METHODOLOGY/committed.md",))
        self.assertNotEqual(state.head, self.fixture.base_commit)

    def test_untracked_executable_mode_is_captured_with_its_hashed_file(self) -> None:
        executable = self.fixture.isolated_root / "scratch/executable.sh"
        executable.write_bytes(b"#!/bin/sh\nexit 0\n")
        executable.chmod(0o755)

        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)

        self.assertIn("scratch/executable.sh", state.unrepresentable_mode_paths)
        self.assertIn(
            "scratch/executable.sh",
            {record.path for record in state.untracked_records},
        )

    def test_base_blob_and_registered_worktree_inventories_are_frozen(self) -> None:
        from kintsugi_kernel.gitstate import _base_blob_records, _list_worktrees

        original = {
            record.path: record
            for record in _base_blob_records(
                self.fixture.isolated_root, self.fixture.base_commit
            )
        }
        (self.fixture.isolated_root / "03_METHODOLOGY/owner.md").write_bytes(
            b"working tree drift does not change the base blob\n"
        )
        repeated = {
            record.path: record
            for record in _base_blob_records(
                self.fixture.isolated_root, self.fixture.base_commit
            )
        }
        worktrees = _list_worktrees(self.fixture.isolated_root)

        self.assertEqual(original, repeated)
        self.assertEqual(original["12_PUBLIC_SITE/assets-link"].kind, "SYMLINK")
        self.assertEqual(
            {(record.root, record.branch) for record in worktrees},
            {
                (self.fixture.canonical_root, "main"),
                (self.fixture.isolated_root, "isolated"),
            },
        )

    def test_registered_detached_worktree_is_reported_with_no_branch(self) -> None:
        from kintsugi_kernel.gitstate import _list_worktrees

        detached = Path(self.temporary.name) / "detached"
        self.git(
            self.fixture.canonical_root,
            "worktree",
            "add",
            "--detach",
            str(detached),
            self.fixture.base_commit,
        )

        records = _list_worktrees(self.fixture.isolated_root)

        self.assertIn((detached.resolve(), None), {
            (record.root, record.branch) for record in records
        })

    def test_safe_read_rejects_parent_swap_after_directory_open(self) -> None:
        from kintsugi_kernel.gitstate import _read_regular_no_symlinks

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            inside_parent = root / "a"
            outside_parent = Path(temporary) / "outside"
            inside_parent.mkdir(parents=True)
            outside_parent.mkdir()
            (inside_parent / "secret").write_bytes(b"INSIDE\n")
            (outside_parent / "secret").write_bytes(b"OUTSIDE\n")
            real_open = os.open
            real_lstat = os.lstat
            swapped = False

            def swap_parent() -> None:
                nonlocal swapped
                if swapped:
                    return
                swapped = True
                inside_parent.rename(root / "a-real")
                inside_parent.symlink_to(
                    outside_parent,
                    target_is_directory=True,
                )

            def swap_after_parent_open(
                path: object,
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                descriptor = real_open(path, flags, mode, dir_fd=dir_fd)
                if not swapped and dir_fd is not None and path == "a":
                    swap_parent()
                return descriptor

            def swap_after_parent_lstat(path: object) -> os.stat_result:
                metadata = real_lstat(path)
                if not swapped and Path(path).name == "a":
                    swap_parent()
                return metadata

            with mock.patch(
                "kintsugi_kernel.gitstate.os.open",
                side_effect=swap_after_parent_open,
            ), mock.patch(
                "kintsugi_kernel.gitstate.os.lstat",
                side_effect=swap_after_parent_lstat,
            ), self.assertRaises(KintsugiError) as caught:
                _read_regular_no_symlinks(root, "a/secret")

            self.assertTrue(swapped)
            self.assertEqual(caught.exception.code, "KIN-E-SCOPE")

    def test_safe_read_rejects_scan_to_open_directory_replacement(self) -> None:
        from kintsugi_kernel.gitstate import _read_regular_no_symlinks

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            inside_parent = root / "a"
            replacement_parent = Path(temporary) / "replacement"
            inside_parent.mkdir(parents=True)
            replacement_parent.mkdir()
            (inside_parent / "secret").write_bytes(b"INSIDE\n")
            (replacement_parent / "secret").write_bytes(b"OUTSIDE\n")
            real_open = os.open
            swapped = False

            def replace_before_parent_open(
                path: object,
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                nonlocal swapped
                if not swapped and dir_fd is not None and path == "a":
                    swapped = True
                    inside_parent.rename(root / "a-real")
                    replacement_parent.rename(inside_parent)
                return real_open(path, flags, mode, dir_fd=dir_fd)

            with mock.patch(
                "kintsugi_kernel.gitstate.os.open",
                side_effect=replace_before_parent_open,
            ), self.assertRaises(KintsugiError) as caught:
                _read_regular_no_symlinks(root, "a/secret")

            self.assertTrue(swapped)
            self.assertEqual(caught.exception.code, "KIN-E-SCOPE")

    def test_safe_hash_rejects_parent_swap_after_directory_open(self) -> None:
        from kintsugi_kernel.gitstate import _hash_regular_or_symlink

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            inside_parent = root / "a"
            replacement_parent = Path(temporary) / "replacement"
            inside_parent.mkdir(parents=True)
            replacement_parent.mkdir()
            (inside_parent / "secret").write_bytes(b"INSIDE\n")
            (replacement_parent / "secret").write_bytes(b"OUTSIDE\n")
            real_open = os.open
            real_lstat = os.lstat
            swapped = False

            def swap_parent() -> None:
                nonlocal swapped
                if swapped:
                    return
                swapped = True
                inside_parent.rename(root / "a-real")
                replacement_parent.rename(inside_parent)

            def swap_after_parent_open(
                path: object,
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                descriptor = real_open(path, flags, mode, dir_fd=dir_fd)
                if not swapped and dir_fd is not None and path == "a":
                    swap_parent()
                return descriptor

            def swap_after_parent_lstat(path: object) -> os.stat_result:
                metadata = real_lstat(path)
                if not swapped and Path(path).name == "a":
                    swap_parent()
                return metadata

            with mock.patch(
                "kintsugi_kernel.gitstate.os.open",
                side_effect=swap_after_parent_open,
            ), mock.patch(
                "kintsugi_kernel.gitstate.os.lstat",
                side_effect=swap_after_parent_lstat,
            ), self.assertRaises(KintsugiError) as caught:
                _hash_regular_or_symlink(root, "a/secret")

            self.assertTrue(swapped)
            self.assertEqual(caught.exception.code, "KIN-E-SCOPE")

    def test_single_link_read_rechecks_link_count_after_payload_read(self) -> None:
        from kintsugi_kernel.gitstate import _read_regular_no_symlinks

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            control = root / "control"
            alias = root / "alias"
            root.mkdir()
            control.write_bytes(b"CONTROL\n")
            real_read = os.read
            linked = False

            def link_during_read(descriptor: int, count: int) -> bytes:
                nonlocal linked
                if not linked:
                    linked = True
                    os.link(control, alias)
                return real_read(descriptor, count)

            with mock.patch(
                "kintsugi_kernel.gitstate.os.read",
                side_effect=link_during_read,
            ), self.assertRaises(KintsugiError) as caught:
                _read_regular_no_symlinks(
                    root,
                    "control",
                    code="KIN-E-SCOPE",
                    require_single_link=True,
                )

            self.assertTrue(linked)
            self.assertEqual(control.stat().st_nlink, 2)
            self.assertEqual(caught.exception.code, "KIN-E-SCOPE")

    def test_protected_snapshot_rejects_root_swap_after_directory_open(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            protected = root / "protected"
            outside = Path(temporary) / "outside"
            protected.mkdir(parents=True)
            outside.mkdir()
            (protected / "secret").write_bytes(b"INSIDE\n")
            (outside / "secret").write_bytes(b"OUTSIDE\n")
            real_open = os.open
            real_lstat = os.lstat
            swapped = False

            def swap_root() -> None:
                nonlocal swapped
                if swapped:
                    return
                swapped = True
                protected.rename(root / "protected-real")
                protected.symlink_to(outside, target_is_directory=True)

            def swap_after_protected_open(
                path: object,
                flags: int,
                mode: int = 0o777,
                *,
                dir_fd: int | None = None,
            ) -> int:
                descriptor = real_open(path, flags, mode, dir_fd=dir_fd)
                if not swapped and dir_fd is not None and path == "protected":
                    swap_root()
                return descriptor

            def swap_after_protected_lstat(path: object) -> os.stat_result:
                metadata = real_lstat(path)
                if not swapped and Path(path).name == "protected":
                    swap_root()
                return metadata

            with mock.patch(
                "kintsugi_kernel.gitstate.os.open",
                side_effect=swap_after_protected_open,
            ), mock.patch(
                "kintsugi_kernel.gitstate.os.lstat",
                side_effect=swap_after_protected_lstat,
            ), self.assertRaises(KintsugiError) as caught:
                _snapshot_protected_tree(root, ("protected",))

            self.assertTrue(swapped)
            self.assertEqual(caught.exception.code, "KIN-E-PROTECTED")


class ProtectedTreeSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))

    def test_recursive_snapshot_hashes_files_and_symlink_targets_without_following(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        records = _snapshot_protected_tree(
            self.fixture.isolated_root,
            ("12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"),
        )

        by_path = {record.path: record for record in records}
        self.assertEqual(
            tuple(by_path),
            (
                "12_PUBLIC_SITE/assets-link",
                "12_PUBLIC_SITE/assets/base.css",
                "12_PUBLIC_SITE/index.html",
                "90_ARCHIVE/history.txt",
                "91_COMPATIBILITY/legacy.txt",
            ),
        )
        self.assertEqual(by_path["12_PUBLIC_SITE/assets-link"].kind, "SYMLINK")
        self.assertEqual(
            by_path["12_PUBLIC_SITE/assets-link"].sha256,
            "sha256:8bf729ffe074caee622c02928173467e658e19e28233cff8a445819e3cae4d50",
        )

    def test_replacing_a_visited_leaf_before_directory_close_fails_closed(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            protected = root / "protected"
            protected.mkdir(parents=True)
            secret = protected / "secret"
            replacement = Path(temporary) / "replacement"
            secret.write_bytes(b"INSIDE\n")
            replacement.write_bytes(b"OUTSIDE\n")
            real_stat = os.stat
            swapped = False

            def swap_after_leaf_check(
                path: object,
                *,
                dir_fd: int | None = None,
                follow_symlinks: bool = True,
            ) -> os.stat_result:
                nonlocal swapped
                metadata = real_stat(
                    path,
                    dir_fd=dir_fd,
                    follow_symlinks=follow_symlinks,
                )
                if not swapped and dir_fd is not None and path == "secret":
                    swapped = True
                    secret.unlink()
                    replacement.rename(secret)
                return metadata

            with mock.patch(
                "kintsugi_kernel.gitstate.os.stat",
                side_effect=swap_after_leaf_check,
            ), self.assertRaises(KintsugiError) as caught:
                _snapshot_protected_tree(root, ("protected",))

            self.assertTrue(swapped)
            self.assertEqual(secret.read_bytes(), b"OUTSIDE\n")
            self.assertEqual(caught.exception.code, "KIN-E-PROTECTED")

    def test_symlink_target_drift_changes_the_snapshot(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        link = self.fixture.isolated_root / "12_PUBLIC_SITE/assets-link"
        link.unlink()
        link.symlink_to("../03_METHODOLOGY", target_is_directory=True)

        isolated = _snapshot_protected_tree(
            self.fixture.isolated_root, ("12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY")
        )
        canonical = _snapshot_protected_tree(
            self.fixture.canonical_root, ("12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY")
        )

        self.assertNotEqual(isolated, canonical)

    def test_symlink_hashes_preserve_raw_non_utf8_target_bytes(self) -> None:
        from kintsugi_kernel.gitstate import (
            _hash_regular_or_symlink,
            _snapshot_protected_tree,
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "root"
            protected = root / "protected"
            protected.mkdir(parents=True)
            link = protected / "link"
            target = b"raw-\xff-target"
            os.symlink(target, os.fsencode(link))

            ordinary = _hash_regular_or_symlink(root, "protected/link")
            protected_records = _snapshot_protected_tree(root, ("protected",))

            self.assertEqual(ordinary.kind, "SYMLINK")
            self.assertEqual(ordinary.sha256, raw_hash(target))
            self.assertEqual(protected_records, (ordinary,))

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO creation is not supported")
    def test_special_file_is_refused(self) -> None:
        from kintsugi_kernel import KintsugiError
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        os.mkfifo(self.fixture.isolated_root / "12_PUBLIC_SITE/not-a-file")

        with self.assertRaises(KintsugiError) as caught:
            _snapshot_protected_tree(
                self.fixture.isolated_root,
                ("12_PUBLIC_SITE", "90_ARCHIVE", "91_COMPATIBILITY"),
            )
        self.assertEqual(caught.exception.code, "KIN-E-PROTECTED")


class AttemptAndConcurrencyPrimitiveTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))
        self.core = build_synthetic_manifest_core(self.fixture)
        self.core_relative = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"

    def git(self, root: Path, *argv: str) -> bytes:
        return subprocess.run(
            ["git", *argv],
            cwd=root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def test_canonical_attempt_number_round_trips_without_padding_aliases(self) -> None:
        from kintsugi_kernel.gitstate import _canonical_attempt_number

        for attempt_id, number in (
            ("RVA-B-001", 1),
            ("RVA-B-010", 10),
            ("RVA-B-999", 999),
            ("RVA-B-1000", 1000),
        ):
            self.assertEqual(_canonical_attempt_number(attempt_id, "B"), number)
        for attempt_id in ("RVA-B-000", "RVA-B-0001", "RVA-A-001", "RVA-B-01", "RVA-B-one"):
            with self.subTest(attempt_id=attempt_id), self.assertRaises(KintsugiError) as caught:
                _canonical_attempt_number(attempt_id, "B")
            self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_smallest_unused_attempt_scans_core_worktrees_history_and_reservations(self) -> None:
        from kintsugi_kernel.gitstate import _plan_next_attempt, _used_attempt_ids

        predecessor = build_review_attempt("FAILED", logic_attestation_id="ATT-LOGIC-001")
        self.core["reviewAttempts"] = [predecessor]
        self.core["phaseReceipts"][0]["reviewAttemptId"] = ATTEMPT_ID

        untracked = self.fixture.canonical_root / attempt_paths("RVA-B-003")[0]
        untracked.parent.mkdir(parents=True, exist_ok=True)
        untracked.write_bytes(b"untracked attempt collision\n")

        historical = self.fixture.isolated_root / attempt_paths("RVA-B-004")[0]
        historical.parent.mkdir(parents=True, exist_ok=True)
        historical.write_bytes(b"historical attempt collision\n")
        self.git(self.fixture.isolated_root, "add", "--", attempt_paths("RVA-B-004")[0])
        self.git(self.fixture.isolated_root, "commit", "-m", "historical attempt")
        historical.unlink()
        self.git(self.fixture.isolated_root, "add", "--", attempt_paths("RVA-B-004")[0])
        self.git(self.fixture.isolated_root, "commit", "-m", "remove historical attempt")

        reservations = self.fixture.common_dir / "kintsugi-attempt-reservations"
        reservations.mkdir()
        (reservations / "RVA-B-005.json").write_bytes(canonical_json_bytes({
            "id": "RVA-B-005",
            "phase": "B",
            "receiptId": "REC-B-109",
            "expectedHead": self.git(self.fixture.isolated_root, "rev-parse", "HEAD").decode("ascii").strip(),
            "expectedCoreSha256": raw_hash(
                (self.fixture.isolated_root / self.core_relative).read_bytes()
            ),
        }))

        used = _used_attempt_ids(self.fixture.isolated_root, self.core, "B")
        plan = _plan_next_attempt(
            self.fixture.isolated_root,
            self.core,
            "B",
            "REC-B-109",
        )

        self.assertEqual(used, ("RVA-B-001", "RVA-B-003", "RVA-B-004", "RVA-B-005"))
        self.assertEqual(plan.id, "RVA-B-002")
        self.assertEqual(plan.predecessor_id, "RVA-B-001")
        self.assertEqual(plan.paths, attempt_paths("RVA-B-002"))

    def test_ignored_attempt_path_still_burns_its_attempt_id(self) -> None:
        from kintsugi_kernel.gitstate import _plan_next_attempt

        ignored_path = attempt_paths("RVA-B-001")[0]
        exclude = self.fixture.common_dir / "info/exclude"
        exclude.write_bytes(exclude.read_bytes() + ignored_path.encode("utf-8") + b"\n")
        target = self.fixture.isolated_root / ignored_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"ignored collision\n")

        plan = _plan_next_attempt(
            self.fixture.canonical_root,
            self.core,
            "B",
            "REC-B-109",
        )

        self.assertEqual(plan.id, "RVA-B-002")

    def test_empty_directory_at_a_derived_role_burns_the_attempt_id(self) -> None:
        from kintsugi_kernel.gitstate import _plan_next_attempt

        obstruction = self.fixture.isolated_root / attempt_paths("RVA-B-001")[0]
        obstruction.mkdir(parents=True)

        plan = _plan_next_attempt(
            self.fixture.isolated_root,
            self.core,
            "B",
            "REC-B-109",
        )

        self.assertEqual(plan.id, "RVA-B-002")

    def test_noncanonical_attempt_path_or_malformed_reservation_fails_closed(self) -> None:
        from kintsugi_kernel.gitstate import _used_attempt_ids

        malformed_path = (
            self.fixture.canonical_root
            / "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts/RVA-B-000/review_target.json"
        )
        malformed_path.parent.mkdir(parents=True)
        malformed_path.write_bytes(b"malformed attempt id\n")
        with self.assertRaises(KintsugiError) as caught:
            _used_attempt_ids(self.fixture.isolated_root, self.core, "B")
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

        malformed_path.unlink()
        reservations = self.fixture.common_dir / "kintsugi-attempt-reservations"
        reservations.mkdir()
        (reservations / "RVA-B-001.json").write_bytes(b"{}\n")
        with self.assertRaises(KintsugiError) as caught:
            _used_attempt_ids(self.fixture.isolated_root, self.core, "B")
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_nonfinite_reservation_value_keeps_concurrency_diagnostic(self) -> None:
        from kintsugi_kernel.gitstate import _used_attempt_ids

        reservations = self.fixture.common_dir / "kintsugi-attempt-reservations"
        reservations.mkdir()
        (reservations / "RVA-B-001.json").write_bytes(
            b'{"expectedCoreSha256":"sha256:0000000000000000000000000000000000000000000000000000000000000000",'
            b'"expectedHead":NaN,"id":"RVA-B-001","phase":"B","receiptId":"REC-B-109"}\n'
        )

        with self.assertRaises(KintsugiError) as caught:
            _used_attempt_ids(self.fixture.isolated_root, self.core, "B")

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_reservations_are_ordered_by_canonical_attempt_number(self) -> None:
        from kintsugi_kernel.gitstate import _reservation_records

        reservations = self.fixture.common_dir / "kintsugi-attempt-reservations"
        reservations.mkdir()
        expected_head = self.git(
            self.fixture.isolated_root, "rev-parse", "HEAD"
        ).decode("ascii").strip()
        for attempt_id in ("RVA-B-1000", "RVA-B-999"):
            (reservations / f"{attempt_id}.json").write_bytes(
                canonical_json_bytes({
                    "id": attempt_id,
                    "phase": "B",
                    "receiptId": "REC-B-109",
                    "expectedHead": expected_head,
                    "expectedCoreSha256": "sha256:" + "0" * 64,
                })
            )

        records = _reservation_records(self.fixture.common_dir)

        self.assertEqual(
            tuple(record["id"] for record in records),
            ("RVA-B-999", "RVA-B-1000"),
        )

    def test_attempt_cycle_without_a_unique_leaf_cannot_plan_a_successor(self) -> None:
        from kintsugi_kernel.gitstate import _plan_next_attempt

        first = build_review_attempt("FAILED", logic_attestation_id="ATT-LOGIC-001")
        first["supersedesAttemptId"] = "RVA-B-002"
        second = build_review_attempt("ABANDONED")
        second["id"] = "RVA-B-002"
        second["supersedesAttemptId"] = "RVA-B-001"
        second["reviewTargetPath"], second["logicReviewPath"], second["btjReviewPath"], second[
            "validationBundlePath"
        ] = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"] = [first, second]

        with self.assertRaises(KintsugiError) as caught:
            _plan_next_attempt(
                self.fixture.isolated_root,
                self.core,
                "B",
                "REC-B-109",
            )
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_disconnected_attempt_cycle_cannot_hide_behind_a_unique_leaf(self) -> None:
        from kintsugi_kernel.gitstate import _plan_next_attempt

        attempts = []
        for attempt_id, predecessor_id in (
            ("RVA-B-001", "RVA-B-002"),
            ("RVA-B-002", "RVA-B-001"),
            ("RVA-B-003", None),
        ):
            attempt = build_review_attempt("ABANDONED")
            attempt["id"] = attempt_id
            attempt["supersedesAttemptId"] = predecessor_id
            (
                attempt["reviewTargetPath"],
                attempt["logicReviewPath"],
                attempt["btjReviewPath"],
                attempt["validationBundlePath"],
            ) = attempt_paths(attempt_id)
            attempts.append(attempt)
        self.core["reviewAttempts"] = attempts

        with self.assertRaises(KintsugiError) as caught:
            _plan_next_attempt(
                self.fixture.isolated_root,
                self.core,
                "B",
                "REC-B-109",
            )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_shared_transition_lock_is_exclusive_and_always_cleans_up(self) -> None:
        from kintsugi_kernel.gitstate import _transition_lock

        entered = threading.Event()
        release = threading.Event()
        failures: list[BaseException] = []

        def holder() -> None:
            try:
                with _transition_lock(self.fixture.common_dir):
                    entered.set()
                    release.wait(5)
            except BaseException as exc:  # test thread must report every failure
                failures.append(exc)

        thread = threading.Thread(target=holder)
        thread.start()
        self.assertTrue(entered.wait(5))
        with self.assertRaises(KintsugiError) as caught:
            with _transition_lock(resolve_git_common_dir(self.fixture.canonical_root)):
                self.fail("a second linked worktree acquired the shared lock")
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        release.set()
        thread.join(5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(failures, [])
        self.assertFalse((self.fixture.common_dir / ".kintsugi-transition.lock").exists())

        with self.assertRaises(RuntimeError):
            with _transition_lock(self.fixture.common_dir):
                raise RuntimeError("synthetic transaction failure")
        self.assertFalse((self.fixture.common_dir / ".kintsugi-transition.lock").exists())

    def test_crash_residue_lock_is_never_stolen_or_expired(self) -> None:
        from kintsugi_kernel.gitstate import _transition_lock

        lock = self.fixture.common_dir / ".kintsugi-transition.lock"
        lock.write_bytes(b"crash residue\n")

        with self.assertRaises(KintsugiError) as caught:
            with _transition_lock(self.fixture.common_dir):
                self.fail("crash residue was stolen")

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(lock.read_bytes(), b"crash residue\n")

    def test_lock_write_failure_is_controlled_and_cleans_up(self) -> None:
        from kintsugi_kernel.gitstate import _transition_lock

        with mock.patch(
            "kintsugi_kernel.gitstate.os.write",
            side_effect=OSError("synthetic lock write failure"),
        ):
            with self.assertRaises(KintsugiError) as caught:
                with _transition_lock(self.fixture.common_dir):
                    self.fail("a lock with unwritten identity bytes was yielded")

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertFalse(
            (self.fixture.common_dir / ".kintsugi-transition.lock").exists()
        )

    def test_replaced_lock_inode_is_preserved_and_fails_closed(self) -> None:
        from kintsugi_kernel.gitstate import _transition_lock

        foreign = b"foreign lock replacement\n"
        with self.assertRaises(KintsugiError) as caught:
            with _transition_lock(self.fixture.common_dir) as lock:
                lock.unlink()
                lock.write_bytes(foreign)

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(
            (self.fixture.common_dir / ".kintsugi-transition.lock").read_bytes(),
            foreign,
        )

    def test_reservation_is_canonical_exclusive_and_burned_after_failure(self) -> None:
        from kintsugi_kernel.gitstate import (
            _plan_next_attempt,
            _reserve_attempt_id,
            _transition_lock,
        )

        expected_head = self.git(
            self.fixture.isolated_root, "rev-parse", "HEAD"
        ).decode("ascii").strip()
        expected_core = raw_hash(
            (self.fixture.isolated_root / self.core_relative).read_bytes()
        )
        plan = _plan_next_attempt(
            self.fixture.isolated_root, self.core, "B", "REC-B-109"
        )

        with self.assertRaises(RuntimeError):
            with _transition_lock(self.fixture.common_dir):
                reservation_path = _reserve_attempt_id(
                    self.fixture.common_dir,
                    plan,
                    expected_head,
                    expected_core,
                )
                raise RuntimeError("failure after durable reservation")

        expected = {
            "id": "RVA-B-001",
            "phase": "B",
            "receiptId": "REC-B-109",
            "expectedHead": expected_head,
            "expectedCoreSha256": expected_core,
        }
        self.assertEqual(reservation_path.read_bytes(), canonical_json_bytes(expected))
        self.assertFalse((self.fixture.common_dir / ".kintsugi-transition.lock").exists())
        before = reservation_path.read_bytes()
        with _transition_lock(self.fixture.common_dir):
            with self.assertRaises(KintsugiError) as caught:
                _reserve_attempt_id(
                    self.fixture.common_dir,
                    plan,
                    expected_head,
                    expected_core,
                )
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(reservation_path.read_bytes(), before)

    def test_zero_byte_reservation_write_fails_controlled_and_burns_the_id(self) -> None:
        from kintsugi_kernel.gitstate import (
            _plan_next_attempt,
            _reserve_attempt_id,
            _transition_lock,
        )

        plan = _plan_next_attempt(
            self.fixture.isolated_root, self.core, "B", "REC-B-109"
        )
        expected_head = self.fixture.base_commit
        expected_core = raw_hash(
            (self.fixture.isolated_root / self.core_relative).read_bytes()
        )
        with _transition_lock(self.fixture.common_dir):
            with mock.patch("kintsugi_kernel.gitstate.os.write", return_value=0):
                with self.assertRaises(KintsugiError) as caught:
                    _reserve_attempt_id(
                        self.fixture.common_dir,
                        plan,
                        expected_head,
                        expected_core,
                    )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        burned = (
            self.fixture.common_dir
            / "kintsugi-attempt-reservations/RVA-B-001.json"
        )
        self.assertTrue(burned.exists())

    def test_head_and_raw_core_compare_and_swap_checks_before_and_inside_lock(self) -> None:
        from kintsugi_kernel.gitstate import _check_head_core_cas, _transition_lock

        expected_head = self.git(
            self.fixture.isolated_root, "rev-parse", "HEAD"
        ).decode("ascii").strip()
        core_path = self.fixture.isolated_root / self.core_relative
        expected_core = raw_hash(core_path.read_bytes())

        _check_head_core_cas(
            self.fixture.isolated_root,
            self.core_relative,
            expected_head,
            expected_core,
        )
        with _transition_lock(self.fixture.common_dir):
            _check_head_core_cas(
                self.fixture.isolated_root,
                self.core_relative,
                expected_head,
                expected_core,
            )
            core_path.write_bytes(b'{"stale":true}\n')
            with self.assertRaises(KintsugiError) as caught:
                _check_head_core_cas(
                    self.fixture.isolated_root,
                    self.core_relative,
                    expected_head,
                    expected_core,
                )
            self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_core_compare_and_swap_rejects_a_symlinked_parent(self) -> None:
        from kintsugi_kernel.gitstate import _check_head_core_cas

        expected_head = self.git(
            self.fixture.isolated_root, "rev-parse", "HEAD"
        ).decode("ascii").strip()
        core_path = self.fixture.isolated_root / self.core_relative
        expected_core = raw_hash(core_path.read_bytes())
        parent = core_path.parent
        relocated = parent.with_name("01_THE_DERIVATION-real")
        parent.rename(relocated)
        parent.symlink_to(relocated.name, target_is_directory=True)

        with self.assertRaises(KintsugiError) as caught:
            _check_head_core_cas(
                self.fixture.isolated_root,
                self.core_relative,
                expected_head,
                expected_core,
            )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_stale_head_is_rejected_by_compare_and_swap(self) -> None:
        from kintsugi_kernel.gitstate import _check_head_core_cas

        expected_head = self.fixture.base_commit
        core_path = self.fixture.isolated_root / self.core_relative
        expected_core = raw_hash(core_path.read_bytes())
        candidate = self.fixture.isolated_root / "03_METHODOLOGY/head-move.md"
        candidate.write_bytes(b"move HEAD\n")
        self.git(self.fixture.isolated_root, "add", "--", "03_METHODOLOGY/head-move.md")
        self.git(self.fixture.isolated_root, "commit", "-m", "move HEAD")

        with self.assertRaises(KintsugiError) as caught:
            _check_head_core_cas(
                self.fixture.isolated_root,
                self.core_relative,
                expected_head,
                expected_core,
            )
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")


class PredecessorFenceTests(unittest.TestCase):
    def setUp(self) -> None:
        from kintsugi_test_support import build_committed_predecessor_fixture

        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))
        self.core = build_committed_predecessor_fixture(self.fixture)
        self.core_relative = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"

    def git(self, *argv: str) -> bytes:
        return subprocess.run(
            ["git", *argv],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def commit_core(self, message: str) -> None:
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative)
        self.git("commit", "-m", message)

    def validate_fence(self) -> None:
        from kintsugi_kernel.gitstate import _validate_predecessor_fence

        _validate_predecessor_fence(
            self.fixture.isolated_root,
            self.core,
            "B",
            "REC-B-109",
            self.core_relative,
        )

    def test_terminal_failed_predecessor_bytes_are_committed_and_immutable(self) -> None:
        self.validate_fence()

    def test_terminal_abandoned_predecessor_may_have_no_target_or_reviews(self) -> None:
        from kintsugi_test_support import build_committed_predecessor_fixture

        fresh_temporary = tempfile.TemporaryDirectory()
        self.addCleanup(fresh_temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(fresh_temporary.name))
        self.core = build_committed_predecessor_fixture(
            self.fixture,
            terminal_status="ABANDONED",
        )

        self.validate_fence()

    def test_uncommitted_core_receipt_target_or_review_rewrite_is_rejected(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        paths = (
            self.core_relative,
            self.core["phaseReceipts"][0]["path"],
            attempt["reviewTargetPath"],
            attempt["logicReviewPath"],
        )
        for relative in paths:
            with self.subTest(relative=relative):
                path = self.fixture.isolated_root / relative
                original = path.read_bytes()
                path.write_bytes(original + b"uncommitted rewrite\n")
                with self.assertRaises(KintsugiError) as caught:
                    self.validate_fence()
                self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
                path.write_bytes(original)

    def test_symlinked_intermediate_artifact_parent_is_rejected(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        target = self.fixture.isolated_root / attempt["reviewTargetPath"]
        canonical_parent = target.parent
        moved_parent = canonical_parent.with_name(canonical_parent.name + "-moved")
        canonical_parent.rename(moved_parent)
        canonical_parent.symlink_to(moved_parent.name, target_is_directory=True)

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_broken_symlink_at_absent_artifact_role_is_rejected(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        bundle = self.fixture.isolated_root / attempt["validationBundlePath"]
        bundle.parent.mkdir(parents=True, exist_ok=True)
        bundle.symlink_to("missing-validation-bundle.json")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_missing_artifact_hash_and_passed_predecessor_are_rejected(self) -> None:
        self.core["reviewAttemptArtifacts"][0]["logicReviewSha256"] = None
        self.commit_core("remove predecessor artifact hash")
        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

        self.core["reviewAttemptArtifacts"][0]["logicReviewSha256"] = raw_hash(
            (self.fixture.isolated_root / self.core["reviewAttempts"][0]["logicReviewPath"]).read_bytes()
        )
        self.core["reviewAttempts"][0]["status"] = "PASSED"
        self.commit_core("make predecessor passed")
        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_second_chain_leaf_is_rejected(self) -> None:
        second = build_review_attempt("ABANDONED")
        second["id"] = "RVA-B-002"
        second["reviewTargetPath"], second["logicReviewPath"], second["btjReviewPath"], second[
            "validationBundlePath"
        ] = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"].append(second)
        self.core["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        self.commit_core("add second terminal leaf")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_every_terminal_ancestor_artifact_remains_committed_and_immutable(self) -> None:
        second = build_review_attempt("ABANDONED")
        second.update({
            "id": "RVA-B-002",
            "supersedesAttemptId": ATTEMPT_ID,
        })
        (
            second["reviewTargetPath"],
            second["logicReviewPath"],
            second["btjReviewPath"],
            second["validationBundlePath"],
        ) = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"].append(second)
        self.core["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        receipt = self.core["phaseReceipts"][0]
        receipt["reviewAttemptId"] = "RVA-B-002"
        receipt_path = self.fixture.isolated_root / receipt["path"]
        receipt_path.write_bytes(build_receipt_markdown(receipt))
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative, receipt["path"])
        self.git("commit", "-m", "append abandoned successor")

        ancestor_logic = (
            self.fixture.isolated_root
            / self.core["reviewAttempts"][0]["logicReviewPath"]
        )
        ancestor_logic.write_bytes(ancestor_logic.read_bytes() + b"rewritten ancestor\n")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_artifact_rewrite_and_restore_in_artifact_only_commits_is_rejected(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        relative = attempt["logicReviewPath"]
        path = self.fixture.isolated_root / relative
        original = path.read_bytes()

        path.write_bytes(original + b"committed transient rewrite\n")
        self.git("add", "--", relative)
        self.git("commit", "-m", "rewrite terminal artifact only")

        path.write_bytes(original)
        self.git("add", "--", relative)
        self.git("commit", "-m", "restore terminal artifact only")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_git_replace_cannot_hide_terminal_artifact_history(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        relative = attempt["logicReviewPath"]
        path = self.fixture.isolated_root / relative
        original = path.read_bytes()
        terminal = self.git("rev-parse", "HEAD").decode("ascii").strip()

        path.write_bytes(original + b"replacement-hidden rewrite\n")
        self.git("add", "--", relative)
        self.git("commit", "-m", "rewrite terminal artifact before replacement")
        path.write_bytes(original)
        self.git("add", "--", relative)
        self.git("commit", "-m", "restore terminal artifact before replacement")
        restored = self.git("rev-parse", "HEAD").decode("ascii").strip()
        replacement = self.git(
            "commit-tree",
            f"{restored}^{{tree}}",
            "-p",
            terminal,
            "-m",
            "replacement skips terminal rewrite",
        ).decode("ascii").strip()
        self.git("replace", restored, replacement)

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_legacy_graft_cannot_hide_terminal_artifact_history(self) -> None:
        attempt = self.core["reviewAttempts"][0]
        relative = attempt["logicReviewPath"]
        path = self.fixture.isolated_root / relative
        original = path.read_bytes()
        terminal = self.git("rev-parse", "HEAD").decode("ascii").strip()

        path.write_bytes(original + b"graft-hidden rewrite\n")
        self.git("add", "--", relative)
        self.git("commit", "-m", "rewrite terminal artifact before graft")
        path.write_bytes(original)
        self.git("add", "--", relative)
        self.git("commit", "-m", "restore terminal artifact before graft")
        restored = self.git("rev-parse", "HEAD").decode("ascii").strip()
        grafts = self.fixture.common_dir / "info/grafts"
        grafts.write_bytes(f"{restored} {terminal}\n".encode("ascii"))

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_core_delete_and_restore_is_rejected(self) -> None:
        core_path = self.fixture.isolated_root / self.core_relative
        original = core_path.read_bytes()

        self.git("rm", "--", self.core_relative)
        self.git("commit", "-m", "delete terminal core only")

        core_path.parent.mkdir(parents=True, exist_ok=True)
        core_path.write_bytes(original)
        self.git("add", "--", self.core_relative)
        self.git("commit", "-m", "restore terminal core only")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_reachable_terminal_chain_cannot_be_erased_and_restarted(self) -> None:
        former_attempt = self.core["reviewAttempts"][0]
        reset_core = build_synthetic_manifest_core(self.fixture)
        reset_receipt = reset_core["phaseReceipts"][0]
        (self.fixture.isolated_root / reset_receipt["path"]).write_bytes(
            build_receipt_markdown(reset_receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(reset_core)
        )
        self.git(
            "rm",
            "--",
            former_attempt["reviewTargetPath"],
            former_attempt["logicReviewPath"],
        )
        self.git("add", "--", self.core_relative, reset_receipt["path"])
        self.git("commit", "-m", "erase terminal chain and reset receipt")

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            reset_core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in issues})
        with self.assertRaises(KintsugiError) as caught:
            freeze_manifest_value(
                self.fixture.isolated_root,
                self.fixture.canonical_root,
                reset_core,
                "B",
                "MANIFEST",
                True,
            )
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_validate_manifest_rejects_disconnected_terminal_restart(self) -> None:
        second = build_review_attempt("ABANDONED")
        second.update({
            "id": "RVA-B-002",
            "supersedesAttemptId": None,
        })
        (
            second["reviewTargetPath"],
            second["logicReviewPath"],
            second["btjReviewPath"],
            second["validationBundlePath"],
        ) = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"].append(second)
        self.core["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        receipt = self.core["phaseReceipts"][0]
        receipt["reviewAttemptId"] = "RVA-B-002"
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        manifest = self.core["manifests"][0]
        second_paths = set(attempt_paths("RVA-B-002"))
        manifest["closureOnlyPaths"] = sorted(
            set(manifest["closureOnlyPaths"]) | second_paths
        )
        manifest["allowedChangePaths"] = sorted(
            set(manifest["allowedChangePaths"]) | second_paths
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative, receipt["path"])
        self.git("commit", "-m", "append disconnected terminal restart")

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in issues})

    def test_terminal_ancestor_is_anchored_to_its_first_terminal_commit(self) -> None:
        second = build_review_attempt("ABANDONED")
        second.update({
            "id": "RVA-B-002",
            "supersedesAttemptId": ATTEMPT_ID,
        })
        (
            second["reviewTargetPath"],
            second["logicReviewPath"],
            second["btjReviewPath"],
            second["validationBundlePath"],
        ) = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"].append(second)
        self.core["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        receipt = self.core["phaseReceipts"][0]
        receipt["reviewAttemptId"] = "RVA-B-002"
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative, receipt["path"])
        self.git("commit", "-m", "append abandoned successor for anchor test")

        target_path = self.core["reviewAttempts"][0]["reviewTargetPath"]
        target = self.fixture.isolated_root / target_path
        target.write_bytes(b'{"rewritten":"after terminal"}\n')
        rewritten_hash = raw_hash(target.read_bytes())
        self.core["reviewAttempts"][0]["reviewSubjectDigest"] = rewritten_hash
        self.core["reviewAttemptArtifacts"][0]["reviewTargetSha256"] = rewritten_hash
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative, target_path)
        self.git("commit", "-m", "rewrite terminal ancestor after the fact")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_anchor_scans_full_reachable_merge_history(self) -> None:
        self.git("switch", "-c", "discarded-terminal", self.fixture.base_commit)
        alternate = copy.deepcopy(self.core)
        alternate_target = b'{"fixture":"discarded terminal branch"}\n'
        alternate_target_hash = raw_hash(alternate_target)
        alternate["reviewAttempts"][0]["reviewSubjectDigest"] = alternate_target_hash
        alternate["reviewAttemptArtifacts"][0]["reviewTargetSha256"] = (
            alternate_target_hash
        )
        alternate["reviewAttestations"][0]["reviewTargetDigest"] = (
            alternate_target_hash
        )
        alternate_review = build_review_markdown(
            alternate["reviewAttestations"][0],
            alternate["reviewFindings"],
        )
        alternate["reviewAttemptArtifacts"][0]["logicReviewSha256"] = raw_hash(
            alternate_review
        )
        attempt = alternate["reviewAttempts"][0]
        target_path = self.fixture.isolated_root / attempt["reviewTargetPath"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(alternate_target)
        review_path = self.fixture.isolated_root / attempt["logicReviewPath"]
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_bytes(alternate_review)
        receipt = alternate["phaseReceipts"][0]
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(alternate)
        )
        self.git(
            "add",
            "--",
            self.core_relative,
            receipt["path"],
            attempt["reviewTargetPath"],
            attempt["logicReviewPath"],
        )
        self.git("commit", "-m", "discarded alternate terminal evidence")
        self.git("switch", "isolated")
        self.git(
            "merge",
            "--no-ff",
            "-s",
            "ours",
            "discarded-terminal",
            "-m",
            "merge while retaining current terminal evidence",
        )

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_anchor_scans_all_reachable_refs(self) -> None:
        self.git("switch", "-c", "unmerged-terminal", self.fixture.base_commit)
        alternate = copy.deepcopy(self.core)
        alternate_target = b'{"fixture":"unmerged terminal branch"}\n'
        alternate_target_hash = raw_hash(alternate_target)
        alternate["reviewAttempts"][0]["reviewSubjectDigest"] = alternate_target_hash
        alternate["reviewAttemptArtifacts"][0]["reviewTargetSha256"] = (
            alternate_target_hash
        )
        alternate["reviewAttestations"][0]["reviewTargetDigest"] = (
            alternate_target_hash
        )
        alternate_review = build_review_markdown(
            alternate["reviewAttestations"][0],
            alternate["reviewFindings"],
        )
        alternate["reviewAttemptArtifacts"][0]["logicReviewSha256"] = raw_hash(
            alternate_review
        )
        attempt = alternate["reviewAttempts"][0]
        target_path = self.fixture.isolated_root / attempt["reviewTargetPath"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(alternate_target)
        review_path = self.fixture.isolated_root / attempt["logicReviewPath"]
        review_path.parent.mkdir(parents=True, exist_ok=True)
        review_path.write_bytes(alternate_review)
        receipt = alternate["phaseReceipts"][0]
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(alternate)
        )
        self.git(
            "add",
            "--",
            self.core_relative,
            receipt["path"],
            attempt["reviewTargetPath"],
            attempt["logicReviewPath"],
        )
        self.git("commit", "-m", "retain conflicting unmerged terminal evidence")
        self.git("switch", "isolated")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_passed_attempt_cannot_be_rewritten_as_failed_predecessor(self) -> None:
        failed = copy.deepcopy(self.core)
        attempt = failed["reviewAttempts"][0]
        target_bytes = (
            self.fixture.isolated_root / attempt["reviewTargetPath"]
        ).read_bytes()
        review_bytes = (
            self.fixture.isolated_root / attempt["logicReviewPath"]
        ).read_bytes()
        self.git("switch", "-c", "passed-then-failed", self.fixture.base_commit)

        passed = copy.deepcopy(failed)
        passed["reviewAttempts"][0]["status"] = "PASSED"
        for value, payload in (
            (attempt["reviewTargetPath"], target_bytes),
            (attempt["logicReviewPath"], review_bytes),
        ):
            path = self.fixture.isolated_root / value
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        receipt = passed["phaseReceipts"][0]
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(passed)
        )
        self.git(
            "add",
            "--",
            self.core_relative,
            receipt["path"],
            attempt["reviewTargetPath"],
            attempt["logicReviewPath"],
        )
        self.git("commit", "-m", "record passed terminal attempt")

        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(failed)
        )
        self.git("add", "--", self.core_relative)
        self.git("commit", "-m", "illegally downgrade passed attempt to failed")
        self.core = failed

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_attestation_is_anchored_to_its_first_terminal_commit(self) -> None:
        self.core["reviewAttestations"][0]["reviewerRole"] = (
            "Rewritten reviewer role after terminal disposition"
        )
        self.commit_core("rewrite terminal attestation after the fact")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_finding_is_anchored_to_its_first_terminal_commit(self) -> None:
        self.core["reviewFindings"][0]["statement"] = (
            "Rewritten finding after terminal disposition."
        )
        self.commit_core("rewrite terminal finding after the fact")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")

    def test_terminal_successor_disposition_is_history_anchored(self) -> None:
        second = build_review_attempt("ABANDONED")
        second.update({
            "id": "RVA-B-002",
            "supersedesAttemptId": ATTEMPT_ID,
        })
        (
            second["reviewTargetPath"],
            second["logicReviewPath"],
            second["btjReviewPath"],
            second["validationBundlePath"],
        ) = attempt_paths("RVA-B-002")
        self.core["reviewAttempts"].append(second)
        self.core["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        self.core["reviewFindingDispositions"].append(
            build_review_finding_disposition()
        )
        receipt = self.core["phaseReceipts"][0]
        receipt["reviewAttemptId"] = "RVA-B-002"
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (self.fixture.isolated_root / self.core_relative).write_bytes(
            canonical_json_bytes(self.core)
        )
        self.git("add", "--", self.core_relative, receipt["path"])
        self.git("commit", "-m", "record abandoned successor disposition")

        self.core["reviewFindingDispositions"][0]["rationale"] = (
            "Rewritten disposition rationale after terminal disposition."
        )
        self.commit_core("rewrite terminal successor disposition")

        with self.assertRaises(KintsugiError) as caught:
            self.validate_fence()
        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")


class ManifestInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))
        self.core = build_synthetic_manifest_core(self.fixture)

    def git_status(self, root: Path) -> bytes:
        return subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def review_ready_core(self) -> dict[str, object]:
        core = build_synthetic_manifest_core(self.fixture)
        attempt = build_review_attempt()
        core["reviewAttempts"] = [attempt]
        core["reviewAttemptArtifacts"] = [{
            "attemptId": ATTEMPT_ID,
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        }]
        core["phaseReceipts"][0]["reviewAttemptId"] = ATTEMPT_ID
        manifest = core["manifests"][0]
        manifest["finalFiles"] = [
            current_file_record(self.fixture.isolated_root, record["path"])
            for record in manifest["includedFiles"]
        ]
        manifest["finalFileCount"] = len(manifest["finalFiles"])
        manifest["closureOnlyPaths"] = sorted(attempt_paths(ATTEMPT_ID))
        manifest["allowedChangePaths"] = sorted(set(
            manifest["allowedChangePaths"] + manifest["closureOnlyPaths"]
        ))
        return core

    def test_valid_pre_review_draft_has_exact_base_partitions_and_empty_final_snapshot(self) -> None:
        before_isolated = self.git_status(self.fixture.isolated_root)
        before_canonical = self.git_status(self.fixture.canonical_root)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        frozen = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            False,
        )

        self.assertEqual(issues, [])
        self.assertIsNot(frozen, self.core)
        self.assertEqual(frozen, self.core)
        manifest = frozen["manifests"][0]
        self.assertEqual(
            [record["path"] for record in manifest["candidateFiles"]],
            [
                "03_METHODOLOGY/excluded.md",
                "03_METHODOLOGY/owner.md",
                "03_METHODOLOGY/support.md",
            ],
        )
        self.assertEqual(
            [record["path"] for record in manifest["includedFiles"]],
            ["03_METHODOLOGY/owner.md", "03_METHODOLOGY/support.md"],
        )
        self.assertEqual(
            manifest["excludedPaths"],
            [{"path": "03_METHODOLOGY/excluded.md", "reason": "Synthetic exclusion."}],
        )
        self.assertEqual(manifest["candidateFileCount"], 3)
        self.assertEqual(manifest["eligibleFileCount"], 2)
        self.assertEqual(manifest["scannedFileCount"], 2)
        self.assertEqual(manifest["finalFiles"], [])
        self.assertEqual(manifest["finalFileCount"], 0)
        self.assertEqual(self.git_status(self.fixture.isolated_root), before_isolated)
        self.assertEqual(self.git_status(self.fixture.canonical_root), before_canonical)

    def test_complete_or_verified_receipt_requires_a_current_attempt(self) -> None:
        for status in ("COMPLETE", "VERIFIED"):
            with self.subTest(status=status):
                core = build_synthetic_manifest_core(self.fixture)
                receipt = core["phaseReceipts"][0]
                receipt["status"] = status
                self.assertIsNone(receipt["reviewAttemptId"])

                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )

                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_manifest_freeze_is_byte_deterministic_and_does_not_mutate_the_input(self) -> None:
        original = copy.deepcopy(self.core)
        first = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            False,
        )
        second = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            False,
        )

        self.assertEqual(first, second)
        self.assertEqual(self.core, original)

    def test_root_and_base_relationships_fail_closed(self) -> None:
        swapped = validate_manifest(
            self.fixture.canonical_root,
            self.fixture.isolated_root,
            self.core,
            "B",
            "MANIFEST",
        )
        wrong_base = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "f" * 40,
        )

        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in swapped})
        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in wrong_base})

    def test_reserved_control_cannot_follow_an_intermediate_symlink(self) -> None:
        relative_parent = "03_METHODOLOGY/01_THE_DERIVATION"
        canonical_parent = self.fixture.isolated_root / relative_parent
        outside_parent = Path(self.temporary.name) / "outside-controls"
        canonical_parent.rename(outside_parent)
        canonical_parent.symlink_to(outside_parent, target_is_directory=True)
        manifest = self.core["manifests"][0]
        manifest["allowedChangePaths"] = sorted({
            *manifest["allowedChangePaths"],
            relative_parent,
            f"{relative_parent}/02_KINTSUGI_SCHEMA.json",
        })
        manifest["allowedPreexistingUntracked"]["isolated"].append(
            current_file_record(self.fixture.isolated_root, relative_parent)
        )
        manifest["allowedPreexistingUntracked"]["isolated"].sort(
            key=lambda value: value["path"]
        )

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn(
            "KIN-E-MANIFEST",
            {issue.code for issue in issues},
            issues,
        )

    def test_inventory_review_path_must_name_a_regular_repository_file(self) -> None:
        manifest = self.core["manifests"][0]
        missing = "03_METHODOLOGY/does-not-exist.md"
        manifest["inventoryReviewPaths"] = [missing]
        manifest["allowedChangePaths"] = sorted({
            *manifest["allowedChangePaths"],
            missing,
        })

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_inventory_review_cannot_case_alias_a_reserved_control(self) -> None:
        alias = "03_methodology/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
        manifest = self.core["manifests"][0]
        manifest["inventoryReviewPaths"] = [alias]
        manifest["allowedChangePaths"] = sorted({
            *manifest["allowedChangePaths"],
            alias,
        })

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_inventory_review_cannot_hardlink_a_reserved_control(self) -> None:
        manifest = self.core["manifests"][0]
        review_relative = manifest["inventoryReviewPaths"][0]
        core_relative = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
        for root in (self.fixture.isolated_root, self.fixture.canonical_root):
            review = root / review_relative
            review.unlink()
            os.link(root / core_relative, review)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_canonical_candidate_owner_dirt_is_never_absorbed_by_allowance(self) -> None:
        (self.fixture.canonical_root / "03_METHODOLOGY/owner.md").write_bytes(
            b"unresolved canonical owner dirt\n"
        )

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_staged_index_bytes_must_equal_the_reviewed_worktree_bytes(self) -> None:
        relative = "03_METHODOLOGY/owner.md"
        target = self.fixture.isolated_root / relative
        target.write_bytes(b"staged payload A\n")
        subprocess.run(
            ["git", "add", "--", relative],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        target.write_bytes(b"reviewed payload B\n")
        self.core["sources"][0]["sha256"] = raw_hash(target.read_bytes())

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_executable_mode_change_is_not_representable_and_fails_closed(self) -> None:
        relative = "03_METHODOLOGY/owner.md"
        target = self.fixture.isolated_root / relative
        target.chmod(0o755)
        subprocess.run(
            ["git", "add", "--", relative],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_core_filemode_false_cannot_hide_executable_mode_change(self) -> None:
        relative = "03_METHODOLOGY/owner.md"
        target = self.fixture.isolated_root / relative
        subprocess.run(
            ["git", "config", "core.fileMode", "false"],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        target.chmod(target.stat().st_mode | 0o100)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_index_visibility_bits_cannot_hide_out_of_scope_mutation(self) -> None:
        relative = "03_METHODOLOGY/excluded.md"
        target = self.fixture.isolated_root / relative
        pristine = target.read_bytes()
        cases = (
            ("--assume-unchanged", "--no-assume-unchanged"),
            ("--skip-worktree", "--no-skip-worktree"),
        )
        for enabled, disabled in cases:
            with self.subTest(flag=enabled):
                subprocess.run(
                    ["git", "update-index", enabled, "--", relative],
                    cwd=self.fixture.isolated_root,
                    check=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                target.write_bytes(pristine + b"hidden out-of-scope mutation\n")

                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    self.core,
                    "B",
                    "MANIFEST",
                )

                self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})
                target.write_bytes(pristine)
                subprocess.run(
                    ["git", "update-index", disabled, "--", relative],
                    cwd=self.fixture.isolated_root,
                    check=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

    def test_protected_file_drift_in_either_root_cannot_be_refrozen_as_a_new_baseline(self) -> None:
        original = copy.deepcopy(self.core)
        for root in (self.fixture.isolated_root, self.fixture.canonical_root):
            with self.subTest(root=root.name):
                target = root / "12_PUBLIC_SITE/index.html"
                pristine = target.read_bytes()
                target.write_bytes(b"concurrent protected drift\n")
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    self.core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})
                with self.assertRaises(KintsugiError) as caught:
                    freeze_manifest_value(
                        self.fixture.isolated_root,
                        self.fixture.canonical_root,
                        self.core,
                        "B",
                        "MANIFEST",
                        True,
                    )
                self.assertEqual(caught.exception.code, "KIN-E-PROTECTED")
                self.assertEqual(self.core, original)
                target.write_bytes(pristine)

    def test_protected_symlink_target_drift_cannot_be_refrozen(self) -> None:
        original = copy.deepcopy(self.core)
        link = self.fixture.isolated_root / "12_PUBLIC_SITE/assets-link"
        link.unlink()
        link.symlink_to("../03_METHODOLOGY", target_is_directory=True)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})
        with self.assertRaises(KintsugiError) as caught:
            freeze_manifest_value(
                self.fixture.isolated_root,
                self.fixture.canonical_root,
                self.core,
                "B",
                "MANIFEST",
                True,
            )
        self.assertEqual(caught.exception.code, "KIN-E-PROTECTED")
        self.assertEqual(self.core, original)

    def test_preexisting_untracked_allowance_requires_exact_path_kind_and_hash(self) -> None:
        original = copy.deepcopy(self.core)
        allowance = self.fixture.isolated_root / "scratch/preexisting.txt"
        allowance.write_bytes(b"retargeted allowance bytes\n")

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})
        with self.assertRaises(KintsugiError) as caught:
            freeze_manifest_value(
                self.fixture.isolated_root,
                self.fixture.canonical_root,
                self.core,
                "B",
                "MANIFEST",
                True,
            )
        self.assertEqual(caught.exception.code, "KIN-E-SCOPE")
        self.assertEqual(self.core, original)

    def test_root_specific_protected_preexisting_baseline_is_valid(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        relative = "12_PUBLIC_SITE/docs/superpowers/preexisting.md"
        target = self.fixture.canonical_root / relative
        target.parent.mkdir(parents=True)
        target.write_bytes(b"canonical-only phase-start bytes\n")
        manifest = self.core["manifests"][0]
        manifest["allowedPreexistingUntracked"]["canonical"].append(
            current_file_record(self.fixture.canonical_root, relative)
        )
        manifest["allowedPreexistingUntracked"]["canonical"].sort(
            key=lambda value: value["path"]
        )
        manifest["protectedTreeSnapshots"]["canonical"] = [
            {"path": value.path, "kind": value.kind, "sha256": value.sha256}
            for value in _snapshot_protected_tree(
                self.fixture.canonical_root,
                tuple(manifest["protectedPaths"]),
            )
        ]

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertEqual(issues, [])

    def test_preexisting_untracked_allowance_cannot_gain_executable_mode(self) -> None:
        allowance = self.fixture.isolated_root / "scratch/preexisting.txt"
        allowance.chmod(0o755)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_unexpected_untracked_and_protected_untracked_paths_fail_separately(self) -> None:
        ordinary = self.fixture.isolated_root / "outside.txt"
        ordinary.write_bytes(b"scope escape\n")
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})
        ordinary.unlink()

        protected = self.fixture.canonical_root / "90_ARCHIVE/untracked.txt"
        protected.write_bytes(b"protected untracked drift\n")
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})

    def test_ignored_untracked_path_cannot_escape_scope(self) -> None:
        relative = "03_METHODOLOGY/hidden-escape.md"
        exclude = self.fixture.common_dir / "info/exclude"
        exclude.write_bytes(exclude.read_bytes() + f"{relative}\n".encode("utf-8"))
        (self.fixture.isolated_root / relative).write_bytes(b"ignored scope escape\n")

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-SCOPE", {issue.code for issue in issues})

    def test_full_file_and_exact_span_provenance_are_byte_bound(self) -> None:
        manifest = self.core["manifests"][0]
        manifest["protectedProvenance"][0]["sha256"] = "sha256:" + "f" * 64
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})

        self.core = build_synthetic_manifest_core(self.fixture)
        self.core["manifests"][0]["protectedProvenance"][1]["exactSpan"] = (
            "span absent from the protected file"
        )
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})

        self.core = build_synthetic_manifest_core(self.fixture)
        outside_record = self.core["manifests"][0]["protectedProvenance"][0]
        outside_record.update({
            "path": "03_METHODOLOGY/owner.md",
            "mode": "FULL_FILE",
            "sha256": raw_hash(
                (self.fixture.isolated_root / "03_METHODOLOGY/owner.md").read_bytes()
            ),
        })
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})

    def test_protected_provenance_cannot_follow_an_intermediate_symlink(self) -> None:
        from kintsugi_kernel.gitstate import _snapshot_protected_tree

        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        secret = outside / "secret.txt"
        secret.write_bytes(b"outside repository bytes\n")
        manifest = self.core["manifests"][0]
        for label, root in (
            ("isolated", self.fixture.isolated_root),
            ("canonical", self.fixture.canonical_root),
        ):
            link = root / "12_PUBLIC_SITE/provlink"
            link.symlink_to(outside, target_is_directory=True)
            manifest["allowedPreexistingUntracked"][label].append(
                current_file_record(root, "12_PUBLIC_SITE/provlink")
            )
            manifest["allowedPreexistingUntracked"][label].sort(
                key=lambda value: value["path"]
            )
            manifest["protectedTreeSnapshots"][label] = [
                {"path": value.path, "kind": value.kind, "sha256": value.sha256}
                for value in _snapshot_protected_tree(
                    root, tuple(manifest["protectedPaths"])
                )
            ]
        manifest["protectedProvenance"].append({
            "path": "12_PUBLIC_SITE/provlink/secret.txt",
            "mode": "FULL_FILE",
            "sha256": raw_hash(secret.read_bytes()),
        })

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-PROTECTED", {issue.code for issue in issues})

    def test_candidate_included_excluded_partitions_and_counts_are_exact(self) -> None:
        mutations = {
            "candidate omission": lambda manifest: manifest["candidateFiles"].pop(),
            "candidate count": lambda manifest: manifest.__setitem__("candidateFileCount", 99),
            "included omission": lambda manifest: manifest["includedFiles"].pop(),
            "eligible count": lambda manifest: manifest.__setitem__("eligibleFileCount", 99),
            "scanned count": lambda manifest: manifest.__setitem__("scannedFileCount", 99),
            "excluded omission": lambda manifest: manifest.__setitem__("excludedPaths", []),
            "overlap": lambda manifest: manifest["includedFiles"].append(
                copy.deepcopy(manifest["candidateFiles"][0])
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                core = build_synthetic_manifest_core(self.fixture)
                mutate(core["manifests"][0])
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_discovery_parser_and_base_blob_records_are_enforced(self) -> None:
        mutations = {
            "wrong parser": lambda manifest: manifest["discoveryRules"][0].__setitem__("parser", "HTML"),
            "unknown include": lambda manifest: manifest["discoveryRules"][0]["includeGlobs"].append(
                "03_METHODOLOGY/absent.md"
            ),
            "wrong base hash": lambda manifest: manifest["candidateFiles"][1].__setitem__(
                "sha256", "sha256:" + "f" * 64
            ),
            "wrong base kind": lambda manifest: manifest["includedFiles"][0].__setitem__(
                "kind", "SYMLINK"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                core = build_synthetic_manifest_core(self.fixture)
                mutate(core["manifests"][0])
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_reserved_control_paths_cannot_reenter_any_source_inventory(self) -> None:
        core_path = "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
        for field in ("candidateFiles", "includedFiles", "finalFiles"):
            with self.subTest(field=field):
                core = build_synthetic_manifest_core(self.fixture)
                manifest = core["manifests"][0]
                manifest[field].append(current_file_record(self.fixture.isolated_root, core_path))
                if field == "candidateFiles":
                    manifest["candidateFileCount"] += 1
                if field == "finalFiles":
                    manifest["finalFileCount"] += 1
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        core = build_synthetic_manifest_core(self.fixture)
        core["manifests"][0]["excludedPaths"].append({
            "path": core_path,
            "reason": "Disguised control path.",
        })
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        core = build_synthetic_manifest_core(self.fixture)
        core["sources"].append({
            "id": "SRC-B-CONTROL",
            "path": core_path,
            "kind": "RECEIPT",
            "phases": ["B"],
            "sha256": current_file_record(
                self.fixture.isolated_root, core_path
            )["sha256"],
            "authorityRole": "PROVENANCE",
        })
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        core = build_synthetic_manifest_core(self.fixture)
        core["sources"].append({
            "id": "SRC-B-CONTROL-ALIAS",
            "path": "03_methodology/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json",
            "kind": "RECEIPT",
            "phases": ["B"],
            "sha256": raw_hash(b"case-aliased control"),
            "authorityRole": "PROVENANCE",
        })
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_missing_reserved_control_path_is_rejected(self) -> None:
        receipt_path = self.core["phaseReceipts"][0]["path"]
        (self.fixture.isolated_root / receipt_path).unlink()

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_reserved_control_paths_must_exist_in_both_linked_roots(self) -> None:
        ledger = (
            self.fixture.canonical_root
            / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
        )
        ledger.unlink()

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_pre_review_and_review_ready_final_snapshot_laws_are_exact(self) -> None:
        core = build_synthetic_manifest_core(self.fixture)
        manifest = core["manifests"][0]
        manifest["finalFiles"] = copy.deepcopy(manifest["includedFiles"])
        manifest["finalFileCount"] = len(manifest["finalFiles"])
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        core = self.review_ready_core()
        self.assertNotIn(
            "KIN-E-MANIFEST",
            {issue.code for issue in validate_manifest(
                self.fixture.isolated_root,
                self.fixture.canonical_root,
                core,
                "B",
                "MANIFEST",
            )},
        )
        (self.fixture.isolated_root / "03_METHODOLOGY/owner.md").write_bytes(
            b"stale after final freeze\n"
        )
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_attempt_receipt_ownership_and_selected_chain_leaf_are_exact(self) -> None:
        wrong_receipt = self.review_ready_core()
        wrong_receipt["reviewAttempts"][0]["receiptId"] = "REC-A-108"
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            wrong_receipt,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        split_chain = self.review_ready_core()
        second = build_review_attempt()
        second.update({
            "id": "RVA-B-002",
            "supersedesAttemptId": None,
        })
        (
            second["reviewTargetPath"],
            second["logicReviewPath"],
            second["btjReviewPath"],
            second["validationBundlePath"],
        ) = attempt_paths("RVA-B-002")
        split_chain["reviewAttempts"].append(second)
        split_chain["reviewAttemptArtifacts"].append({
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        split_chain["phaseReceipts"][0]["reviewAttemptId"] = "RVA-B-002"
        manifest = split_chain["manifests"][0]
        manifest["closureOnlyPaths"] = sorted({
            *attempt_paths(ATTEMPT_ID),
            *attempt_paths("RVA-B-002"),
        })
        manifest["allowedChangePaths"] = sorted({
            *manifest["allowedChangePaths"],
            *manifest["closureOnlyPaths"],
        })
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            split_chain,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

        hidden_chain = self.review_ready_core()
        hidden_chain["phaseReceipts"][0]["reviewAttemptId"] = None
        hidden_manifest = hidden_chain["manifests"][0]
        hidden_manifest["finalFiles"] = []
        hidden_manifest["finalFileCount"] = 0
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            hidden_chain,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_declared_attempt_roles_cannot_launder_semantic_paths(self) -> None:
        mutations = {
            "role swap": lambda attempt: attempt.update({
                "logicReviewPath": attempt["btjReviewPath"],
                "btjReviewPath": attempt["logicReviewPath"],
            }),
            "owner as review": lambda attempt: attempt.__setitem__(
                "logicReviewPath", "03_METHODOLOGY/owner.md"
            ),
            "duplicate target role": lambda attempt: attempt.__setitem__(
                "validationBundlePath", attempt["reviewTargetPath"]
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                core = self.review_ready_core()
                mutate(core["reviewAttempts"][0])
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_undeclared_attempt_namespace_bytes_cannot_be_laundered_as_closure(self) -> None:
        rogue = attempt_paths("RVA-B-999")[0]
        target = self.fixture.isolated_root / rogue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"undeclared attempt artifact\n")
        self.core["manifests"][0]["allowedChangePaths"].append(rogue)
        self.core["manifests"][0]["allowedChangePaths"].sort()

        allowed_issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in allowed_issues})

        self.core["manifests"][0]["allowedChangePaths"].remove(rogue)
        exclude = self.fixture.common_dir / "info/exclude"
        exclude.write_bytes(exclude.read_bytes() + rogue.encode("utf-8") + b"\n")
        ignored_issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in ignored_issues})

    def test_attempt_namespace_root_cannot_be_an_allowed_regular_file(self) -> None:
        rogue = "09_TOOLS/08_AUDIT_ARTIFACTS/kintsugi_review_attempts"
        target = self.fixture.isolated_root / rogue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"namespace root obstruction\n")
        self.core["manifests"][0]["allowedChangePaths"].append(rogue)
        self.core["manifests"][0]["allowedChangePaths"].sort()

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in issues})

    def test_case_aliased_attempt_namespace_is_rejected_portably(self) -> None:
        rogue = "09_TOOLS/08_AUDIT_ARTIFACTS/KINTSUGI_REVIEW_ATTEMPTS"
        target = self.fixture.isolated_root / rogue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"case-aliased namespace obstruction\n")
        self.core["manifests"][0]["allowedChangePaths"].append(rogue)
        self.core["manifests"][0]["allowedChangePaths"].sort()

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in issues})

    def test_directory_obstruction_at_a_derived_role_is_rejected(self) -> None:
        obstruction = self.fixture.isolated_root / attempt_paths("RVA-B-001")[0]
        obstruction.mkdir(parents=True)

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-CONCURRENT", {issue.code for issue in issues})

    def test_harvest_trial_exclusion_partition_and_source_membership_are_exact(self) -> None:
        mutations = {
            "trial omission": lambda core: core["manifests"][0].__setitem__("trialedClaimIds", []),
            "trial count": lambda core: core["manifests"][0].__setitem__("trialedClaimCount", 0),
            "receipt claim omission": lambda core: core["phaseReceipts"][0].__setitem__(
                "claimIds", []
            ),
            "source raw hash": lambda core: core["sources"][0].__setitem__(
                "sha256", "sha256:" + "f" * 64
            ),
            "harvest exclusion overlap": lambda core: core["manifests"][0]["excludedClaimIds"].append({
                "claimId": CLAIM_ID,
                "reason": "Illegal overlap.",
            }),
            "source outside included": lambda core: core["sources"][0].__setitem__(
                "path", "03_METHODOLOGY/excluded.md"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                core = build_synthetic_manifest_core(self.fixture)
                mutate(core)
                issues = validate_manifest(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                )
                self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})


class FinalManifestFreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))
        self.core = build_synthetic_manifest_core(self.fixture)
        receipt = self.core["phaseReceipts"][0]
        (self.fixture.isolated_root / receipt["path"]).write_bytes(
            build_receipt_markdown(receipt)
        )
        (
            self.fixture.isolated_root
            / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
        ).write_bytes(build_ledger_markdown([]))

    def git_status(self) -> bytes:
        return subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=self.fixture.isolated_root,
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout

    def test_final_freeze_returns_a_deterministic_prospective_full_core(self) -> None:
        original = copy.deepcopy(self.core)
        status_before = self.git_status()

        first = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        second = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )

        self.assertEqual(first, second)
        self.assertEqual(self.core, original)
        self.assertEqual(self.git_status(), status_before)
        self.assertFalse(
            (self.fixture.common_dir / ".kintsugi-transition.lock").exists()
        )
        self.assertFalse(
            (self.fixture.common_dir / "kintsugi-attempt-reservations").exists()
        )

        receipt = first["phaseReceipts"][0]
        manifest = first["manifests"][0]
        attempt = first["reviewAttempts"][0]
        artifact = first["reviewAttemptArtifacts"][0]
        expected_paths = attempt_paths("RVA-B-001")
        self.assertEqual(receipt["reviewAttemptId"], "RVA-B-001")
        self.assertEqual(
            {
                "id": attempt["id"],
                "phase": attempt["phase"],
                "receiptId": attempt["receiptId"],
                "supersedesAttemptId": attempt["supersedesAttemptId"],
                "status": attempt["status"],
                "abandonReason": attempt["abandonReason"],
                "logicAttestationId": attempt["logicAttestationId"],
                "btjAttestationId": attempt["btjAttestationId"],
            },
            {
                "id": "RVA-B-001",
                "phase": "B",
                "receiptId": "REC-B-109",
                "supersedesAttemptId": None,
                "status": "PENDING",
                "abandonReason": None,
                "logicAttestationId": None,
                "btjAttestationId": None,
            },
        )
        self.assertEqual(
            tuple(attempt[field] for field in (
                "reviewTargetPath",
                "logicReviewPath",
                "btjReviewPath",
                "validationBundlePath",
            )),
            expected_paths,
        )
        self.assertRegex(attempt["reviewSubjectDigest"], r"^sha256:[0-9a-f]{64}$")
        self.assertNotEqual(attempt["reviewSubjectDigest"], "sha256:" + "0" * 64)
        self.assertEqual(artifact, {
            "attemptId": "RVA-B-001",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        self.assertEqual(first["reviewFindingDispositions"], [])
        self.assertEqual(manifest["closureOnlyPaths"], sorted(expected_paths))
        self.assertTrue(set(expected_paths).issubset(manifest["allowedChangePaths"]))
        self.assertEqual(
            [record["path"] for record in manifest["finalFiles"]],
            [record["path"] for record in manifest["includedFiles"]],
        )
        self.assertEqual(manifest["finalFileCount"], len(manifest["finalFiles"]))

    def test_review_subject_digest_changes_with_semantics_not_placeholder_data(self) -> None:
        baseline = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        changed = copy.deepcopy(self.core)
        changed["claims"][0]["proposition"] += " Material semantic change."
        changed_result = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            changed,
            "B",
            "MANIFEST",
            True,
        )

        self.assertNotEqual(
            baseline["reviewAttempts"][0]["reviewSubjectDigest"],
            changed_result["reviewAttempts"][0]["reviewSubjectDigest"],
        )

    def test_final_freeze_recomputes_subject_after_validation_and_rejects_transient_reads(self) -> None:
        from kintsugi_kernel.manifest import _subject_target_value as real_target

        calls = 0

        def transient_first_target(*args: object, **kwargs: object) -> dict[str, object]:
            nonlocal calls
            calls += 1
            target = real_target(*args, **kwargs)
            if calls == 1:
                target["receiptNarrativeRawSha256"] = "sha256:" + "f" * 64
            return target

        with mock.patch(
            "kintsugi_kernel.manifest._subject_target_value",
            side_effect=transient_first_target,
        ):
            with self.assertRaises(KintsugiError) as caught:
                freeze_manifest_value(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    self.core,
                    "B",
                    "MANIFEST",
                    True,
                )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(calls, 2)

    def test_final_freeze_rejects_transient_bytes_spanning_both_subject_reads(self) -> None:
        from kintsugi_kernel.manifest import _subject_target_value as real_target

        receipt = self.core["phaseReceipts"][0]
        receipt_path = self.fixture.isolated_root / receipt["path"]
        original = receipt_path.read_bytes()
        alternate = build_receipt_markdown(
            receipt,
            prefix=b"# Synthetic receipt\n\nTransient synchronized narrative.\n",
        )
        calls = 0

        def spanning_transient(*args: object, **kwargs: object) -> dict[str, object]:
            nonlocal calls
            if calls == 0:
                receipt_path.write_bytes(alternate)
            calls += 1
            target = real_target(*args, **kwargs)
            if calls == 2:
                receipt_path.write_bytes(original)
            return target

        with mock.patch(
            "kintsugi_kernel.manifest._subject_target_value",
            side_effect=spanning_transient,
        ):
            with self.assertRaises(KintsugiError) as caught:
                freeze_manifest_value(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    self.core,
                    "B",
                    "MANIFEST",
                    True,
                )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(calls, 3)
        self.assertEqual(receipt_path.read_bytes(), original)

    def test_final_freeze_revalidates_included_bytes_after_settled_subject(self) -> None:
        from kintsugi_kernel.manifest import _subject_target_value as real_target

        owner = self.fixture.isolated_root / "03_METHODOLOGY/owner.md"
        reviewed = b"reviewed owner version A\n"
        stale = b"unreviewed owner version B\n"
        owner.write_bytes(reviewed)
        self.core["sources"][0]["sha256"] = raw_hash(reviewed)
        calls = 0

        def mutate_after_second_target(
            *args: object,
            **kwargs: object,
        ) -> dict[str, object]:
            nonlocal calls
            calls += 1
            target = real_target(*args, **kwargs)
            if calls == 2:
                owner.write_bytes(stale)
            return target

        with mock.patch(
            "kintsugi_kernel.manifest._subject_target_value",
            side_effect=mutate_after_second_target,
        ):
            with self.assertRaises(KintsugiError) as caught:
                freeze_manifest_value(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    self.core,
                    "B",
                    "MANIFEST",
                    True,
                )

        self.assertEqual(caught.exception.code, "KIN-E-CONCURRENT")
        self.assertEqual(calls, 3)
        self.assertEqual(owner.read_bytes(), stale)

    def test_subject_target_excludes_unreferenced_records_outside_receipt_closure(self) -> None:
        from kintsugi_kernel.gitstate import GitState
        from kintsugi_kernel.manifest import _subject_target_value

        prospective = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        manifest = prospective["manifests"][0]
        attempt_id = prospective["reviewAttempts"][0]["id"]
        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)
        self.assertIsInstance(state, GitState)

        target = _subject_target_value(
            self.fixture.isolated_root,
            prospective,
            manifest,
            self.core["phaseReceipts"][0],
            "B",
            attempt_id,
            state,
        )

        self.assertEqual(
            [source["id"] for source in target["sources"]],
            ["SRC-B-001"],
        )

    def test_subject_closure_follows_all_claim_and_rosetta_edges_and_rejects_cycles(self) -> None:
        from kintsugi_kernel.manifest import _semantic_record_closure

        core = build_synthetic_manifest_core(self.fixture)
        root = core["claims"][0]
        added = []
        for number in range(2, 7):
            claim = copy.deepcopy(root)
            claim["id"] = f"CLM-B-{number:03d}"
            claim["dependencyClaimIds"] = []
            claim["supportLinks"] = []
            claim["survivingIfKilled"] = {
                "claimIds": [],
                "rationale": "Synthetic closure endpoint.",
            }
            added.append(claim)
        core["claims"].extend(added)
        root["dependencyClaimIds"] = ["CLM-B-002"]
        root["supportLinks"] = [{"supportingClaimId": "CLM-B-003"}]
        root["survivingIfKilled"] = {
            "claimIds": ["CLM-B-004"],
            "rationale": "Synthetic survivor edge.",
        }
        seam = {"id": "KIN-B-001", "claimId": CLAIM_ID, "receiptId": "REC-B-109"}
        core["seams"] = [seam]
        core["phaseReceipts"][0]["seamIds"] = [seam["id"]]
        core["antibodies"] = [{
            "id": "ANT-B-001",
            "seamId": seam["id"],
            "semanticEvaluator": "ROSETTA_TRANSFER",
        }]
        core["fixtures"] = [{
            "id": "FIX-B-001",
            "payloadKind": "JSON",
            "payload": json.dumps({
                "targetClaimId": "CLM-B-005",
                "bridgeClaimId": "CLM-B-006",
            }),
            "seamIds": [seam["id"]],
            "antibodyIds": ["ANT-B-001"],
        }]
        manifest = core["manifests"][0]
        manifest["harvestedClaimIds"] = [claim["id"] for claim in core["claims"]]
        receipt = core["phaseReceipts"][0]

        closure = _semantic_record_closure(core, manifest, receipt)

        self.assertEqual(
            [claim["id"] for claim in closure["claims"]],
            [f"CLM-B-{number:03d}" for number in range(1, 7)],
        )
        self.assertEqual([fixture["id"] for fixture in closure["fixtures"]], ["FIX-B-001"])

        cyclic = copy.deepcopy(core)
        cyclic["claims"][3]["dependencyClaimIds"] = [CLAIM_ID]
        with self.assertRaises(KintsugiError) as caught:
            _semantic_record_closure(
                cyclic,
                cyclic["manifests"][0],
                cyclic["phaseReceipts"][0],
            )
        self.assertEqual(caught.exception.code, "KIN-E-MANIFEST")

    def test_rosetta_fixture_attached_only_through_antibody_enters_claim_closure(self) -> None:
        from kintsugi_kernel.manifest import _semantic_record_closure

        core = build_synthetic_manifest_core(self.fixture)
        root = core["claims"][0]
        endpoint = copy.deepcopy(root)
        endpoint["id"] = "CLM-B-002"
        endpoint["dependencyClaimIds"] = []
        endpoint["supportLinks"] = []
        endpoint["survivingIfKilled"] = {
            "claimIds": [],
            "rationale": "Synthetic Rosetta endpoint.",
        }
        core["claims"].append(endpoint)
        core["manifests"][0]["harvestedClaimIds"].append(endpoint["id"])
        seam = {"id": "KIN-B-001", "claimId": CLAIM_ID, "receiptId": "REC-B-109"}
        core["seams"] = [seam]
        core["phaseReceipts"][0]["seamIds"] = [seam["id"]]
        core["antibodies"] = [{
            "id": "ANT-B-001",
            "seamId": seam["id"],
            "semanticEvaluator": "ROSETTA_TRANSFER",
        }]
        core["fixtures"] = [{
            "id": "FIX-B-NEG",
            "payloadKind": "JSON",
            "payload": json.dumps({
                "targetClaimId": endpoint["id"],
                "bridgeClaimId": None,
            }),
            "seamIds": [],
            "antibodyIds": ["ANT-B-001"],
        }]

        closure = _semantic_record_closure(
            core, core["manifests"][0], core["phaseReceipts"][0]
        )

        self.assertEqual(
            [claim["id"] for claim in closure["claims"]],
            [CLAIM_ID, endpoint["id"]],
        )
        self.assertEqual(
            [fixture["id"] for fixture in closure["fixtures"]],
            ["FIX-B-NEG"],
        )

    def test_subject_closure_uses_declared_receipt_membership_not_matching_receipt_id(self) -> None:
        from kintsugi_kernel.manifest import _semantic_record_closure

        core = build_synthetic_manifest_core(self.fixture)
        selected_seam = {
            "id": "KIN-B-001",
            "claimId": CLAIM_ID,
            "receiptId": "REC-B-109",
        }
        rogue_seam = {
            "id": "KIN-B-999",
            "claimId": CLAIM_ID,
            "receiptId": "REC-B-109",
        }
        rogue_trial = copy.deepcopy(core["trials"][0])
        rogue_trial.update({"id": "TRL-B-999", "seamId": rogue_seam["id"]})
        rogue_propagation = {
            "id": "PRP-B-999",
            "seamId": selected_seam["id"],
            "receiptId": "REC-B-109",
            "derivativeSourceId": "SRC-B-001",
        }
        core["seams"] = [selected_seam, rogue_seam]
        core["trials"].append(rogue_trial)
        core["propagations"] = [rogue_propagation]
        core["phaseReceipts"][0]["seamIds"] = [selected_seam["id"]]

        closure = _semantic_record_closure(
            core, core["manifests"][0], core["phaseReceipts"][0]
        )

        self.assertEqual([trial["id"] for trial in closure["trials"]], ["TRL-B-001"])
        self.assertEqual([seam["id"] for seam in closure["seams"]], ["KIN-B-001"])
        self.assertEqual(closure["propagations"], [])

    def test_subject_target_validates_global_ledger_then_projects_selected_sections(self) -> None:
        from kintsugi_kernel.gitstate import GitState
        from kintsugi_kernel.manifest import _subject_target_value

        prospective = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        selected = {
            "id": "KIN-B-001",
            "claimId": CLAIM_ID,
            "receiptId": "REC-B-109",
        }
        unrelated = {
            "id": "KIN-A-999",
            "claimId": CLAIM_ID,
            "receiptId": "REC-A-108",
        }
        current_receipt = copy.deepcopy(self.core["phaseReceipts"][0])
        current_receipt["seamIds"] = [selected["id"]]
        prospective["seams"] = [selected, unrelated]
        prospective["phaseReceipts"][0]["seamIds"] = [selected["id"]]
        (self.fixture.isolated_root / current_receipt["path"]).write_bytes(
            build_receipt_markdown(current_receipt)
        )
        ledger_path = (
            self.fixture.isolated_root
            / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAM_LEDGER.md"
        )
        ledger_path.write_bytes(build_ledger_markdown([selected, unrelated]))
        manifest = prospective["manifests"][0]
        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)
        self.assertIsInstance(state, GitState)

        target = _subject_target_value(
            self.fixture.isolated_root,
            prospective,
            manifest,
            current_receipt,
            "B",
            prospective["reviewAttempts"][0]["id"],
            state,
        )

        self.assertEqual([section["id"] for section in target["ledgerSemanticSections"]], ["KIN-B-001"])

    def test_dependency_receipts_are_complete_acyclic_validated_and_digest_bound(self) -> None:
        from kintsugi_kernel.manifest import _semantic_record_closure, _subject_target_value
        from kintsugi_kernel.schema import validate_named_definition

        prospective = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        manifest = prospective["manifests"][0]
        state = inspect_git_state(self.fixture.isolated_root, self.fixture.base_commit)
        target = _subject_target_value(
            self.fixture.isolated_root,
            prospective,
            manifest,
            self.core["phaseReceipts"][0],
            "B",
            prospective["reviewAttempts"][0]["id"],
            state,
        )
        target["reviewSubjectDigest"] = prospective["reviewAttempts"][0][
            "reviewSubjectDigest"
        ]
        schema_path = (
            Path(__file__).resolve().parents[2]
            / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SCHEMA.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(
            validate_named_definition(schema, "reviewTarget", target),
            [],
        )
        closure = _semantic_record_closure(
            prospective,
            manifest,
            self.core["phaseReceipts"][0],
        )
        self.assertEqual(closure["dependencyReceipts"], [{
            "id": "REC-A-108",
            "validationDigest": "sha256:" + "0" * 64,
        }])

        missing = copy.deepcopy(self.core)
        missing["phaseReceipts"] = [missing["phaseReceipts"][0]]
        with self.assertRaises(KintsugiError):
            _semantic_record_closure(
                missing, missing["manifests"][0], missing["phaseReceipts"][0]
            )

        cyclic = copy.deepcopy(self.core)
        cyclic["phaseReceipts"][1]["dependsOnReceiptIds"] = ["REC-B-109"]
        with self.assertRaises(KintsugiError):
            _semantic_record_closure(
                cyclic, cyclic["manifests"][0], cyclic["phaseReceipts"][0]
            )

        unvalidated = copy.deepcopy(self.core)
        unvalidated["phaseReceipts"][1]["validationDigest"] = ""
        unvalidated["phaseReceipts"][1]["validationBundlePath"] = ""
        with self.assertRaises(KintsugiError):
            _semantic_record_closure(
                unvalidated,
                unvalidated["manifests"][0],
                unvalidated["phaseReceipts"][0],
            )

    def test_review_subject_digest_ignores_attempt_number_from_a_durable_reservation(self) -> None:
        baseline = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )
        reservations = self.fixture.common_dir / "kintsugi-attempt-reservations"
        reservations.mkdir()
        (reservations / "RVA-B-001.json").write_bytes(canonical_json_bytes({
            "id": "RVA-B-001",
            "phase": "B",
            "receiptId": "REC-B-109",
            "expectedHead": self.fixture.base_commit,
            "expectedCoreSha256": raw_hash(
                (
                    self.fixture.isolated_root
                    / "03_METHODOLOGY/01_THE_DERIVATION/02_KINTSUGI_SEAMS.json"
                ).read_bytes()
            ),
        }))

        renumbered = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            self.core,
            "B",
            "MANIFEST",
            True,
        )

        self.assertEqual(renumbered["reviewAttempts"][0]["id"], "RVA-B-002")
        self.assertEqual(
            baseline["reviewAttempts"][0]["reviewSubjectDigest"],
            renumbered["reviewAttempts"][0]["reviewSubjectDigest"],
        )

    def test_successor_expands_process_invalid_disposition_atomically(self) -> None:
        core = build_committed_predecessor_fixture(self.fixture)
        predecessor = core["reviewAttempts"][0]
        artifact = core["reviewAttemptArtifacts"][0]
        disposition_input = {
            "findingId": "FND-B-001",
            "disposition": "PROCESS_INVALID",
            "rationale": "The predecessor review process was invalidated by its bound artifact.",
            "claimIds": [],
            "seamIds": [],
            "ledgerSectionIds": [],
            "receiptIds": [],
            "subjectPaths": [],
            "discriminatorIds": [],
            "evidenceFiles": [{
                "path": predecessor["logicReviewPath"],
                "sha256": artifact["logicReviewSha256"],
            }],
        }

        prospective = freeze_manifest_value(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
            True,
            [disposition_input],
        )

        successor = prospective["reviewAttempts"][-1]
        successor_artifact = prospective["reviewAttemptArtifacts"][-1]
        self.assertEqual(successor["id"], "RVA-B-002")
        self.assertEqual(successor["supersedesAttemptId"], "RVA-B-001")
        self.assertEqual(successor["status"], "PENDING")
        self.assertEqual(successor_artifact, {
            "attemptId": "RVA-B-002",
            "reviewTargetSha256": None,
            "logicReviewSha256": None,
            "btjReviewSha256": None,
        })
        self.assertEqual(
            prospective["reviewFindingDispositions"][-1],
            {
                "id": "RFD-RVA-B-002-001",
                "fromAttemptId": "RVA-B-001",
                "successorAttemptId": "RVA-B-002",
                **disposition_input,
            },
        )
        self.assertEqual(
            prospective["phaseReceipts"][0]["reviewAttemptId"],
            "RVA-B-002",
        )
        self.assertEqual(
            prospective["manifests"][0]["closureOnlyPaths"],
            sorted(attempt_paths("RVA-B-001") + attempt_paths("RVA-B-002")),
        )

    def test_successor_dispositions_fail_closed_without_exact_bound_process_evidence(self) -> None:
        core = build_committed_predecessor_fixture(self.fixture)
        predecessor = core["reviewAttempts"][0]
        artifact = core["reviewAttemptArtifacts"][0]
        process_input = {
            "findingId": "FND-B-001",
            "disposition": "PROCESS_INVALID",
            "rationale": "Bound process evidence is required.",
            "claimIds": [],
            "seamIds": [],
            "ledgerSectionIds": [],
            "receiptIds": [],
            "subjectPaths": [],
            "discriminatorIds": [],
            "evidenceFiles": [{
                "path": predecessor["logicReviewPath"],
                "sha256": artifact["logicReviewSha256"],
            }],
        }
        addressed = copy.deepcopy(process_input)
        addressed.update({
            "disposition": "ADDRESSED",
            "claimIds": [CLAIM_ID],
            "evidenceFiles": [],
        })
        bad_hash = copy.deepcopy(process_input)
        bad_hash["evidenceFiles"][0]["sha256"] = "sha256:" + "f" * 64

        for label, inputs in (
            ("missing exact finding coverage", []),
            ("semantic delta not yet proven", [addressed]),
            ("unbound process evidence", [bad_hash]),
        ):
            with self.subTest(label=label), self.assertRaises(KintsugiError) as caught:
                freeze_manifest_value(
                    self.fixture.isolated_root,
                    self.fixture.canonical_root,
                    core,
                    "B",
                    "MANIFEST",
                    True,
                    inputs,
                )
            self.assertEqual(caught.exception.code, "KIN-E-MANIFEST")


class PhaseABindingManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        from kintsugi_test_support import build_synthetic_phase_a_manifest_core

        self.build_phase_a = build_synthetic_phase_a_manifest_core
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.fixture = build_synthetic_git_repository(Path(self.temporary.name))

    def validate(self, core: dict[str, object]) -> list[object]:
        return validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "A",
            "MANIFEST",
        )

    def test_exact_phase_a_bootstrap_is_the_only_empty_trial_exception(self) -> None:
        core = self.build_phase_a(self.fixture, bootstrap=True)
        manifest = core["manifests"][0]

        self.assertEqual(self.validate(core), [])
        self.assertTrue(core["claims"])
        self.assertEqual(len(manifest["requiredClaimBindings"]), 7)
        self.assertEqual(core["trials"], [])
        self.assertEqual(core["phaseReceipts"][0]["trialIds"], [])
        self.assertEqual(manifest["trialedClaimIds"], [])
        self.assertEqual(manifest["finalFiles"], [])
        self.assertEqual(manifest["closureOnlyPaths"], [])

        phase_b = build_synthetic_manifest_core(self.fixture)
        phase_b["trials"] = []
        phase_b["phaseReceipts"][0]["trialIds"] = []
        phase_b["manifests"][0]["trialedClaimIds"] = []
        phase_b["manifests"][0]["trialedClaimCount"] = 0
        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            phase_b,
            "B",
            "MANIFEST",
        )
        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})

    def test_all_seven_frozen_binding_dimensions_are_enforced(self) -> None:
        mutations = {
            "missing requirement": lambda core: core["manifests"][0]["requiredClaimBindings"].pop(),
            "duplicate claim": lambda core: core["manifests"][0]["requiredClaimBindings"][1].__setitem__(
                "claimId", core["manifests"][0]["requiredClaimBindings"][0]["claimId"]
            ),
            "wrong owner id": lambda core: core["manifests"][0]["requiredClaimBindings"][0].__setitem__(
                "ownerSourceId", core["sources"][-1]["id"]
            ),
            "wrong anchor": lambda core: core["manifests"][0]["requiredClaimBindings"][0].__setitem__(
                "ownerAnchor", "## Relabeled broad heading"
            ),
            "wrong fingerprint": lambda core: core["manifests"][0]["requiredClaimBindings"][0].__setitem__(
                "targetHash", "sha256-text-lf:" + "f" * 64
            ),
            "wrong owner path": lambda core: core["sources"][0].__setitem__(
                "path", "05_COSMOLOGY/unrelated.md"
            ),
            "excluded binding": lambda core: core["manifests"][0]["excludedClaimIds"].append({
                "claimId": core["manifests"][0]["requiredClaimBindings"][0]["claimId"],
                "reason": "Illegal exclusion.",
            }),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                core = self.build_phase_a(self.fixture, bootstrap=True)
                mutate(core)
                self.assertIn(
                    "KIN-E-MANIFEST", {issue.code for issue in self.validate(core)}
                )

    def test_nonbootstrap_binding_requires_one_matching_owned_trial(self) -> None:
        core = self.build_phase_a(self.fixture, bootstrap=False)
        self.assertEqual(self.validate(core), [])

        core["trials"][0]["triedHash"] = "sha256-text-lf:" + "f" * 64
        self.assertIn(
            "KIN-E-MANIFEST", {issue.code for issue in self.validate(core)}
        )

    def test_nonbootstrap_binding_rejects_a_second_matching_trial(self) -> None:
        core = self.build_phase_a(self.fixture, bootstrap=False)
        duplicate = copy.deepcopy(core["trials"][0])
        duplicate["id"] = "TRL-A-008"
        core["trials"].append(duplicate)
        core["phaseReceipts"][0]["trialIds"].append("TRL-A-008")

        self.assertIn(
            "KIN-E-MANIFEST",
            {issue.code for issue in self.validate(core)},
        )

    def test_phase_b_and_c_may_not_claim_phase_a_bindings(self) -> None:
        core = build_synthetic_manifest_core(self.fixture)
        phase_a = self.build_phase_a(self.fixture, bootstrap=True)
        core["manifests"][0]["requiredClaimBindings"] = copy.deepcopy(
            phase_a["manifests"][0]["requiredClaimBindings"]
        )

        issues = validate_manifest(
            self.fixture.isolated_root,
            self.fixture.canonical_root,
            core,
            "B",
            "MANIFEST",
        )

        self.assertIn("KIN-E-MANIFEST", {issue.code for issue in issues})


if __name__ == "__main__":
    unittest.main()
