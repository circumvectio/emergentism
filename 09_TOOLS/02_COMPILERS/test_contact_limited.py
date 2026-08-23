#!/usr/bin/env python3
"""Mutation controls for the contact-limited completion ratchet."""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_contact_limited.py"
SPEC = importlib.util.spec_from_file_location("check_contact_limited", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
PREDEPLOY_PATH = ROOT / "12_PUBLIC_SITE/predeploy_check.py"
PREDEPLOY_SPEC = importlib.util.spec_from_file_location(
    "predeploy_check_for_contact_tests", PREDEPLOY_PATH
)
assert PREDEPLOY_SPEC and PREDEPLOY_SPEC.loader
PREDEPLOY = importlib.util.module_from_spec(PREDEPLOY_SPEC)
PREDEPLOY_SPEC.loader.exec_module(PREDEPLOY)


class ContactLimitedRatchetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.state = CHECKER.load_json(ROOT / CHECKER.STATE_PATH)
        cls.computed = {
            "compute_receipt_namespace": CHECKER.compute_receipt_namespace(ROOT),
            "compute_public_lifecycle": CHECKER.compute_public_lifecycle(ROOT),
            "compute_claim_disposition": CHECKER.compute_claim_disposition(ROOT),
            "compute_owner_debts": CHECKER.compute_owner_debts(ROOT),
            "compute_world_contact": CHECKER.compute_world_contact(ROOT),
        }

    def validate_fast(self, state, **overrides):
        values = {name: copy.deepcopy(value) for name, value in self.computed.items()}
        values.update(overrides)
        with contextlib.ExitStack() as stack:
            for name, value in values.items():
                stack.enter_context(mock.patch.object(CHECKER, name, return_value=value))
            return CHECKER.validate_state(state, ROOT)

    def assert_invalid(self, state, **overrides) -> None:
        with self.assertRaises(CHECKER.ContractError):
            self.validate_fast(state, **overrides)

    def init_git_repo(self, repo: Path) -> None:
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.email", "ratchet@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(repo), "config", "user.name", "Ratchet Test"],
            check=True,
        )

    def commit_all(self, repo: Path, message: str) -> None:
        subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True)
        # This disposable fixture needs Git history, not the workstation's
        # corpus pre-commit hook (which would recursively run the outer gate).
        subprocess.run(
            ["git", "-C", str(repo), "commit", "--no-verify", "-qm", message],
            check=True,
        )

    def create_receipt_lanes(self, repo: Path) -> None:
        for relative_lane in CHECKER.RECEIPT_LANES:
            (repo / relative_lane).mkdir(parents=True, exist_ok=True)

    def create_topology_tombstones(self, repo: Path) -> None:
        for relative in CHECKER.HELD_TOPOLOGY_TOMBSTONES:
            target = repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT / relative).read_bytes())

    def receipt_bytes_for_state(self, state) -> bytes:
        digest = CHECKER.canonical_state_digest(state)
        return (
            f"contact_limited_state_canonical_sha256: {digest}\n"
        ).encode("utf-8")

    def compute_public_with_vercel(self, vercel):
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.VERCEL_CONFIG:
                return vercel
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            return CHECKER.compute_public_lifecycle(ROOT)

    def test_repo_file_rejects_direct_file_symlink_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            outside = fixture / "outside.txt"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "owner.txt").symlink_to(outside)
            errors: list[str] = []
            self.assertIsNone(
                CHECKER.repo_file(root, "owner.txt", "synthetic owner", errors)
            )
        self.assertTrue(any("must not traverse a symlink" in error for error in errors), errors)

    def test_repo_file_rejects_parent_directory_symlink_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            outside = fixture / "outside"
            outside.mkdir()
            (outside / "owner.txt").write_text("outside\n", encoding="utf-8")
            (root / "owners").symlink_to(outside, target_is_directory=True)
            errors: list[str] = []
            self.assertIsNone(
                CHECKER.repo_file(
                    root, "owners/owner.txt", "synthetic owner", errors
                )
            )
        self.assertTrue(any("must not traverse a symlink" in error for error in errors), errors)

    def test_claim_status_loader_rejects_direct_file_symlink_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            sentinel = fixture / "executed"
            outside = fixture / "outside_policy.py"
            outside.write_text(
                f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n",
                encoding="utf-8",
            )
            (root / "claim_policy.py").symlink_to(outside)
            with self.assertRaisesRegex(RuntimeError, "claim-status policy.*symlink"):
                CHECKER._load_claim_status_policy(root, Path("claim_policy.py"))
            self.assertFalse(sentinel.exists())

    def test_claim_status_loader_rejects_parent_symlink_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            sentinel = fixture / "executed"
            outside = fixture / "outside"
            outside.mkdir()
            (outside / "claim_policy.py").write_text(
                f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('ran')\n",
                encoding="utf-8",
            )
            (root / "policies").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(RuntimeError, "claim-status policy.*symlink"):
                CHECKER._load_claim_status_policy(
                    root, Path("policies/claim_policy.py")
                )
            self.assertFalse(sentinel.exists())

    def test_check_rejects_direct_state_file_symlink_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            state_parent = root / CHECKER.STATE_PATH.parent
            state_parent.mkdir(parents=True)
            outside = fixture / "CONTACT_LIMITED_STATE.json"
            outside.write_text("{}\n", encoding="utf-8")
            (root / CHECKER.STATE_PATH).symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "contact-limited state owner.*symlink"
            ):
                CHECKER.check(root)

    def test_check_rejects_state_parent_directory_symlink_before_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            outside = fixture / "outside-meta"
            outside.mkdir()
            (outside / CHECKER.STATE_PATH.name).write_text("{}\n", encoding="utf-8")
            (root / CHECKER.STATE_PATH.parent).symlink_to(
                outside, target_is_directory=True
            )
            with self.assertRaisesRegex(
                CHECKER.ContractError, "contact-limited state owner.*symlink"
            ):
                CHECKER.check(root)

    def test_live_contract_passes_with_exact_scope(self) -> None:
        report = CHECKER.check(ROOT)
        self.assertEqual(
            report["receipt_namespace"]["target_files"],
            self.state["receipt_namespace"]["target_files"],
        )
        self.assertEqual(report["receipt_namespace"]["target_files"], 321)
        self.assertEqual(
            report["receipt_namespace"]["prefixed_markdown_including_00_convention"],
            334,
        )
        self.assertEqual(report["receipt_namespace"]["unique_prefixes"], 195)
        self.assertEqual(
            report["receipt_namespace"]["bare_unsafe_reused_prefixes"],
            CHECKER.EXPECTED_REUSED_PREFIXES,
        )
        self.assertEqual(
            report["public_lifecycle"]["ignore_counts"],
            {
                "present_html": 424,
                "ignored_html": 207,
                "deployable_html": 217,
                "withheld_artifacts_added_back": 195,
            },
        )
        self.assertEqual(report["public_lifecycle"]["counts"]["total"], 412)
        self.assertEqual(report["public_lifecycle"]["counts"]["current"], 54)
        self.assertEqual(report["public_lifecycle"]["counts"]["unclassified"], 0)
        self.assertEqual(
            report["public_lifecycle"]["matcher_conformance"]["mismatches"], []
        )
        self.assertEqual(report["claim_disposition"]["lifecycle_rows"], 50)
        self.assertEqual(report["claim_disposition"]["current_rows"], 28)
        self.assertEqual(report["claim_disposition"]["direct_contact"], 16)
        self.assertEqual(report["claim_disposition"]["merged_contact"], 4)
        self.assertEqual(report["claim_disposition"]["internal"], 8)
        self.assertEqual(report["claim_disposition"]["external_contracts"], 19)
        self.assertEqual(report["claim_disposition"]["ambiguous"], 0)
        self.assertEqual(report["owner_held"], 2)
        self.assertEqual(report["world_contact"]["state"], "OPEN")

    def test_claim_projection_uses_investigations_not_legacy_reopened(self) -> None:
        source = copy.deepcopy(
            CHECKER._CLAIM_STATUS_POLICY.load_document(ROOT / CHECKER.CLAIM_SOURCE)
        )
        source["reopened"] = source.pop("investigations")
        with mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "check", return_value=[]
        ), mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "load_document", return_value=source
        ):
            with self.assertRaisesRegex(CHECKER.ContractError, "investigations"):
                CHECKER.compute_claim_disposition(ROOT)

    def test_typed_survivor_cannot_enter_the_50_row_lifecycle(self) -> None:
        source = copy.deepcopy(
            CHECKER._CLAIM_STATUS_POLICY.load_document(ROOT / CHECKER.CLAIM_SOURCE)
        )
        source["open"][-1] = copy.deepcopy(source["typed_survivors"][0])
        with mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "check", return_value=[]
        ), mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "load_document", return_value=source
        ):
            with self.assertRaisesRegex(CHECKER.ContractError, "outside the 50-row"):
                CHECKER.compute_claim_disposition(ROOT)

    def test_claim_lifecycle_cannot_be_coordinately_rebaselined_to_51(self) -> None:
        source = copy.deepcopy(
            CHECKER._CLAIM_STATUS_POLICY.load_document(ROOT / CHECKER.CLAIM_SOURCE)
        )
        source["open"].append(copy.deepcopy(source["open"][0]))
        with mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "check", return_value=[]
        ), mock.patch.object(
            CHECKER._CLAIM_STATUS_POLICY, "load_document", return_value=source
        ):
            with self.assertRaisesRegex(CHECKER.ContractError, "exactly 50"):
                CHECKER.compute_claim_disposition(ROOT)

    def test_public_artifact_disappearance_fails(self) -> None:
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["counts"]["total"] -= 1
        public["counts"]["current"] -= 1
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_reopening_matcher_conformance_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["public_lifecycle"]["deploy_ignore_contract"][
            "matcher_conformance"
        ]["state"] = "OPEN_INTERNAL_DRIFT"
        self.assert_invalid(state)

    def test_nonzero_unclassified_rebaseline_still_fails_closure(self) -> None:
        state = copy.deepcopy(self.state)
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["counts"]["unclassified"] = 1
        public["unclassified"] = ["synthetic-unclassified.html"]
        state["public_lifecycle"]["counts"]["unclassified"] = 1
        state["public_lifecycle"]["unclassified"] = [
            "synthetic-unclassified.html"
        ]
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "requires zero unclassified" in error
                for error in raised.exception.errors
            )
        )

    def test_double_claim_classification_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["current_scope"]["internal_terminal"].append("W1")
        self.assert_invalid(state)

    def test_stale_count_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["public_lifecycle"]["counts"]["total"] += 1
        self.assert_invalid(state)

    def test_old_section_receipt_cannot_authorize_new_snapshot(self) -> None:
        state = copy.deepcopy(self.state)
        state["public_lifecycle"]["receipt_ref"] = (
            "11_UPLINK/50_AUDITS_AND_EXECUTIONS/235_INTERNAL_COMPLETION_HARDENING_AND_RECURSIVE_ROADMAP_2026_08_01.md"
        )
        self.assert_invalid(state)

    def test_synthetic_artifact_rebaseline_needs_new_receipt_digest(self) -> None:
        state = copy.deepcopy(self.state)
        public_state = state["public_lifecycle"]
        public_state["counts"]["total"] += 1
        public_state["counts"]["unclassified"] += 1
        public_state["unclassified"].append("synthetic-contact-ratchet.html")
        public_state["deploy_ignore_contract"]["present_html"] += 1
        public_state["deploy_ignore_contract"]["deployable_html"] += 1

        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["counts"]["total"] += 1
        public["counts"]["unclassified"] += 1
        public["unclassified"].append("synthetic-contact-ratchet.html")
        public["ignore_counts"]["present_html"] += 1
        public["ignore_counts"]["deployable_html"] += 1
        self.assert_invalid(state, compute_public_lifecycle=public)

    def test_unchanged_committed_snapshot_receipt_passes_binding(self) -> None:
        receipt_ref = self.state["receipt_namespace"]["receipt_ref"]
        receipt_bytes = (ROOT / receipt_ref).read_bytes()
        self.assertEqual(
            CHECKER.snapshot_binding_errors(self.state, receipt_bytes, receipt_bytes), []
        )

    def test_same_committed_receipt_digest_rewrite_fails(self) -> None:
        original = (
            ROOT / self.state["receipt_namespace"]["receipt_ref"]
        ).read_bytes()
        mutated = copy.deepcopy(self.state)
        mutated["public_lifecycle"]["counts"]["total"] += 1
        new_digest = CHECKER.canonical_state_digest(mutated)
        rewritten = CHECKER.STATE_DIGEST_LINE.sub(
            f"contact_limited_state_canonical_sha256: {new_digest}",
            original.decode("utf-8"),
        ).encode("utf-8")
        errors = CHECKER.snapshot_binding_errors(mutated, rewritten, original)
        self.assertFalse(any("digest mismatch" in error for error in errors))
        self.assertTrue(any("committed HEAD bytes" in error for error in errors))

    def test_new_uncommitted_receipt_can_bind_next_snapshot(self) -> None:
        original = (
            ROOT / self.state["receipt_namespace"]["receipt_ref"]
        ).read_bytes()
        mutated = copy.deepcopy(self.state)
        mutated["public_lifecycle"]["counts"]["total"] += 1
        new_digest = CHECKER.canonical_state_digest(mutated)
        new_receipt = CHECKER.STATE_DIGEST_LINE.sub(
            f"contact_limited_state_canonical_sha256: {new_digest}",
            original.decode("utf-8"),
        ).encode("utf-8")
        self.assertEqual(
            CHECKER.snapshot_binding_errors(mutated, new_receipt, None), []
        )

    def test_git_custody_distinguishes_committed_and_new_receipt_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            receipt = repo / "236_RECEIPT_2026_08_01.md"
            receipt.write_bytes(b"committed baseline\n")
            self.commit_all(repo, "baseline")
            self.assertEqual(
                CHECKER.committed_receipt_bytes(repo, Path(receipt.name)),
                b"committed baseline\n",
            )
            receipt.write_bytes(b"rewritten working copy\n")
            self.assertEqual(
                CHECKER.committed_receipt_bytes(repo, Path(receipt.name)),
                b"committed baseline\n",
            )
            self.assertIsNone(
                CHECKER.committed_receipt_bytes(
                    repo, Path("237_NEXT_BASELINE_2026_08_02.md")
                )
            )

    def test_initial_new_receipt_commit_passes_parent_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            state = {"snapshot": 1}
            rel = Path("236_RECEIPT_2026_08_01.md")
            working = self.receipt_bytes_for_state(state)
            (repo / rel).write_bytes(working)
            self.commit_all(repo, "initial receipt")
            head, parent = CHECKER.receipt_history_bytes(repo, rel)
            self.assertEqual(head, working)
            self.assertIsNone(parent)
            self.assertEqual(
                CHECKER.snapshot_binding_errors(state, working, head, parent), []
            )

    def test_later_unchanged_receipt_commit_passes_parent_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            state = {"snapshot": 1}
            rel = Path("236_RECEIPT_2026_08_01.md")
            working = self.receipt_bytes_for_state(state)
            (repo / rel).write_bytes(working)
            self.commit_all(repo, "initial receipt")
            (repo / "base.txt").write_text("unrelated\n", encoding="utf-8")
            self.commit_all(repo, "unrelated")
            head, parent = CHECKER.receipt_history_bytes(repo, rel)
            self.assertEqual(head, parent)
            self.assertEqual(
                CHECKER.snapshot_binding_errors(state, working, head, parent), []
            )

    def test_later_same_path_receipt_rewrite_commit_fails_parent_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            rel = Path("236_RECEIPT_2026_08_01.md")
            old_state = {"snapshot": 1}
            (repo / rel).write_bytes(self.receipt_bytes_for_state(old_state))
            self.commit_all(repo, "initial receipt")
            new_state = {"snapshot": 2}
            working = self.receipt_bytes_for_state(new_state)
            (repo / rel).write_bytes(working)
            self.commit_all(repo, "forbidden rewrite")
            head, parent = CHECKER.receipt_history_bytes(repo, rel)
            errors = CHECKER.snapshot_binding_errors(
                new_state, working, head, parent
            )
            self.assertTrue(any("first parent" in error for error in errors))

    def test_unavailable_first_parent_history_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            clone = Path(directory) / "shallow"
            source.mkdir()
            self.init_git_repo(source)
            (source / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(source, "base")
            rel = Path("236_RECEIPT_2026_08_01.md")
            (source / rel).write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(source, "receipt")
            subprocess.run(
                [
                    "git",
                    "clone",
                    "-q",
                    "--depth",
                    "1",
                    source.resolve().as_uri(),
                    str(clone),
                ],
                check=True,
            )
            with self.assertRaisesRegex(
                CHECKER.ContractError, "first-parent history unavailable"
            ):
                CHECKER.receipt_history_bytes(clone, rel)

    def test_new_marker_rebaseline_preserves_old_marker_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            self.create_receipt_lanes(repo)
            lane = repo / CHECKER.RECEIPT_LANES[0]
            old = lane / "236_BASELINE_2026_08_01.md"
            old.write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(repo, "old baseline")
            new = lane / "237_BASELINE_2026_08_02.md"
            new.write_bytes(self.receipt_bytes_for_state({"snapshot": 2}))
            self.commit_all(repo, "new baseline")
            self.assertEqual(CHECKER.marker_receipt_custody_errors(repo), [])

    def test_new_marker_rebaseline_cannot_rewrite_old_marker_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            self.create_receipt_lanes(repo)
            lane = repo / CHECKER.RECEIPT_LANES[0]
            old = lane / "236_BASELINE_2026_08_01.md"
            old.write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(repo, "old baseline")
            old.write_bytes(self.receipt_bytes_for_state({"snapshot": "rewritten"}))
            new = lane / "237_BASELINE_2026_08_02.md"
            new.write_bytes(self.receipt_bytes_for_state({"snapshot": 2}))
            self.commit_all(repo, "malicious rebaseline")
            errors = CHECKER.marker_receipt_custody_errors(repo)
            self.assertTrue(any("first-parent bytes" in error for error in errors))

    def test_new_marker_rebaseline_cannot_delete_old_marker_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            self.commit_all(repo, "base")
            self.create_receipt_lanes(repo)
            lane = repo / CHECKER.RECEIPT_LANES[0]
            old = lane / "236_BASELINE_2026_08_01.md"
            old.write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(repo, "old baseline")
            old.unlink()
            new = lane / "237_BASELINE_2026_08_02.md"
            new.write_bytes(self.receipt_bytes_for_state({"snapshot": 2}))
            self.commit_all(repo, "malicious deletion")
            errors = CHECKER.marker_receipt_custody_errors(repo)
            self.assertTrue(any("deleted from HEAD" in error for error in errors))

    def test_marker_receipt_custody_rejects_direct_file_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            self.create_receipt_lanes(repo)
            marker = (
                repo
                / CHECKER.RECEIPT_LANES[0]
                / "236_BASELINE_2026_08_01.md"
            )
            marker.write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(repo, "marker baseline")
            outside = repo / "outside-marker.md"
            outside.write_bytes(marker.read_bytes())
            marker.unlink()
            marker.symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "marker-receipt custody entry.*symlink"
            ):
                CHECKER.marker_receipt_custody_errors(repo)

    def test_marker_receipt_custody_rejects_parent_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.init_git_repo(repo)
            self.create_receipt_lanes(repo)
            parent = repo / CHECKER.RECEIPT_LANES[0] / "nested"
            parent.mkdir()
            marker = parent / "236_BASELINE_2026_08_01.md"
            marker.write_bytes(self.receipt_bytes_for_state({"snapshot": 1}))
            self.commit_all(repo, "nested marker baseline")
            outside = repo / "outside-marker-parent"
            parent.rename(outside)
            parent.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "marker-receipt custody entry.*symlink"
            ):
                CHECKER.marker_receipt_custody_errors(repo)

    def test_git_history_unavailable_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.committed_receipt_bytes(
                    Path(directory), Path("236_RECEIPT_2026_08_01.md")
                )

    def test_w3_merged_mapping_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["current_scope"]["merged_contact"].remove("W3")
        self.assert_invalid(state)

    def test_investigation_question_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["current_scope"]["internal_narrowed"].remove("RQ-09")
        self.assert_invalid(state)

    def test_count_preserving_per_id_status_swap_fails(self) -> None:
        claims = copy.deepcopy(self.computed["compute_claim_disposition"])
        statuses = claims["current_scope"]["statuses"]
        statuses["W0-CROWN"], statuses["W2"] = statuses["W2"], statuses["W0-CROWN"]
        self.assert_invalid(self.state, compute_claim_disposition=claims)

    def test_owner_debt_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["owner_held"]["debts"].pop()
        self.assert_invalid(state)

    def test_count_preserving_owner_debt_substitution_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["owner_held"]["debts"][0]["id"] = "PASS-WITH-DEBT"
        substituted = {"PASS-WITH-DEBT", "OWNER_GATE_OPEN_TOPOLOGY"}
        self.assert_invalid(state, compute_owner_debts=substituted)

    def test_owner_profile_cannot_hide_unset_debts_behind_pass(self) -> None:
        profile = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.COHERENCE_SOURCE))
        profile["axes"]["routing"]["state"] = "PASS"
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.COHERENCE_SOURCE:
                return profile
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            with self.assertRaisesRegex(CHECKER.ContractError, "PASS_WITH_DEBT"):
                CHECKER.compute_owner_debts(ROOT)

    def test_owner_profile_cannot_drop_one_unset_debt(self) -> None:
        profile = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.COHERENCE_SOURCE))
        profile["axes"]["routing"]["debt_ids"].pop()
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.COHERENCE_SOURCE:
                return profile
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            with self.assertRaisesRegex(CHECKER.ContractError, "two unset owner debts"):
                CHECKER.compute_owner_debts(ROOT)

    def test_public_doc_debt_preserves_identical_non_deployable_copies(self) -> None:
        self.assertEqual(
            CHECKER.public_doc_owner_debt_errors(
                ROOT, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            ),
            [],
        )
        errors = CHECKER.public_doc_owner_debt_errors(
            ROOT,
            CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE | {"00_META/unrelated.md"},
        )
        self.assertTrue(
            any("must exactly match" in error for error in errors), errors
        )
        _left, right = sorted(CHECKER.PUBLIC_DOC_EVIDENCE)
        original_read_bytes = Path.read_bytes

        def divergent_read_bytes(path):
            if path == ROOT / right:
                return b"synthetic divergence"
            return original_read_bytes(path)

        with mock.patch.object(
            Path, "read_bytes", autospec=True, side_effect=divergent_read_bytes
        ):
            errors = CHECKER.public_doc_owner_debt_errors(
                ROOT, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
        self.assertTrue(
            any("no longer byte-identical" in error for error in errors), errors
        )

        with mock.patch.object(CHECKER, "_is_vercel_ignored", return_value=False):
            errors = CHECKER.public_doc_owner_debt_errors(
                ROOT, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
        self.assertTrue(
            any("path is no longer ignored" in error for error in errors), errors
        )

        with mock.patch.object(
            CHECKER._PREDEPLOY_POLICY, "is_vercel_ignored", return_value=False
        ):
            errors = CHECKER.public_doc_owner_debt_errors(
                ROOT, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
        self.assertTrue(
            any("predeploy matcher" in error for error in errors), errors
        )

    def test_public_doc_debt_requires_each_parent_exclusion(self) -> None:
        patterns = CHECKER._load_vercelignore(ROOT / CHECKER.VERCEL_IGNORE)
        for (
            path,
            required_pattern,
        ) in CHECKER.PUBLIC_DOC_EXACT_IGNORE_PATTERNS.items():
            site_relative = Path(path).relative_to(CHECKER.PUBLIC_DIR).as_posix()
            self.assertIn(required_pattern, patterns)
            self.assertTrue(
                CHECKER._is_vercel_ignored(site_relative, [required_pattern])
            )
            self.assertTrue(
                PREDEPLOY.is_vercel_ignored(site_relative, [required_pattern])
            )

    def test_public_doc_debt_rejects_ancestor_symlink_or_lost_index_custody(self) -> None:
        left, right = sorted(CHECKER.PUBLIC_DOC_EVIDENCE)
        docs_path = next(
            path for path in CHECKER.PUBLIC_DOC_EVIDENCE if "/docs/" in path
        )
        plans_path = next(
            path for path in CHECKER.PUBLIC_DOC_EVIDENCE if "/_PLANS/" in path
        )
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            target = corpus / "retained-docs/superpowers/specs"
            target.mkdir(parents=True)
            (target / Path(docs_path).name).write_bytes(b"same custody bytes\n")
            plans = corpus / Path(plans_path)
            plans.parent.mkdir(parents=True)
            plans.write_bytes(b"same custody bytes\n")
            docs = corpus / "12_PUBLIC_SITE/docs"
            docs.parent.mkdir(parents=True, exist_ok=True)
            docs.symlink_to(target.parents[1], target_is_directory=True)
            ignore = corpus / CHECKER.VERCEL_IGNORE
            ignore.parent.mkdir(parents=True, exist_ok=True)
            ignore.write_text("docs/\n_PLANS/\n", encoding="utf-8")
            errors = CHECKER.public_doc_owner_debt_errors(
                corpus, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
        self.assertTrue(
            any("must not traverse a symlink" in error for error in errors), errors
        )

        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            for path in (left, right):
                target = corpus / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"same custody bytes\n")
            ignore = corpus / CHECKER.VERCEL_IGNORE
            ignore.write_text("docs/\n_PLANS/\n", encoding="utf-8")
            self.init_git_repo(corpus)
            self.commit_all(corpus, "add public-document custody")
            self.assertEqual(
                CHECKER.public_doc_owner_debt_errors(
                    corpus, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
                ),
                [],
            )
            for path in (left, right):
                (corpus / path).write_bytes(b"new but still identical custody bytes\n")
            errors = CHECKER.public_doc_owner_debt_errors(
                corpus, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
            self.assertTrue(
                any(
                    "lacks exact regular-file Git index custody" in error
                    for error in errors
                ),
                errors,
            )
            for path in (left, right):
                (corpus / path).write_bytes(b"same custody bytes\n")
            subprocess.run(
                ["git", "-C", str(corpus), "rm", "--cached", "-q", left],
                check=True,
            )
            errors = CHECKER.public_doc_owner_debt_errors(
                corpus, CHECKER.PUBLIC_DOC_OWNER_DEBT_EVIDENCE
            )
        self.assertTrue(
            any("lacks exact regular-file Git index custody" in error for error in errors),
            errors,
        )

    def test_unresolved_topology_inventory_rejects_expansion_or_disappearance(self) -> None:
        self.assertEqual(CHECKER.unresolved_topology_errors(ROOT), [])
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            self.create_topology_tombstones(corpus)
            self.init_git_repo(corpus)
            self.commit_all(corpus, "add exact topology tombstones")
            self.assertEqual(CHECKER.unresolved_topology_errors(corpus), [])
            (corpus / "07_EXTRA/00_META").mkdir(parents=True)
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("unexpected=07_EXTRA/00_META" in error for error in errors),
                errors,
            )

        with tempfile.TemporaryDirectory() as directory:
            errors = CHECKER.unresolved_topology_errors(Path(directory))
        self.assertTrue(
            any("missing=08_FRAMEWORK_SUPPORT/00_META" in error for error in errors),
            errors,
        )

        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            target = corpus / "target"
            target.mkdir()
            held = corpus / "08_FRAMEWORK_SUPPORT/00_META"
            held.parent.mkdir(parents=True)
            held.symlink_to(target, target_is_directory=True)
            errors = CHECKER.unresolved_topology_errors(corpus)
        self.assertTrue(
            any("symlink=08_FRAMEWORK_SUPPORT/00_META" in error for error in errors),
            errors,
        )

        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            broken = corpus / "05_COSMOLOGY/00_META"
            broken.parent.mkdir(parents=True)
            broken.symlink_to(corpus / "missing", target_is_directory=True)
            errors = CHECKER.unresolved_topology_errors(corpus)
        self.assertTrue(
            any("unexpected=05_COSMOLOGY/00_META" in error for error in errors),
            errors,
        )
        self.assertTrue(
            any("symlink=05_COSMOLOGY/00_META" in error for error in errors),
            errors,
        )

        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            wrong_type = corpus / "05_COSMOLOGY/00_META"
            wrong_type.parent.mkdir(parents=True)
            wrong_type.write_text("not a directory\n", encoding="utf-8")
            errors = CHECKER.unresolved_topology_errors(corpus)
        self.assertTrue(
            any("non-directory=05_COSMOLOGY/00_META" in error for error in errors),
            errors,
        )

    def test_unresolved_topology_requires_exact_evidence_and_route_boundary(self) -> None:
        self.assertEqual(
            CHECKER.topology_owner_debt_errors(
                ROOT, CHECKER.TOPOLOGY_OWNER_DEBT_EVIDENCE
            ),
            [],
        )
        errors = CHECKER.topology_owner_debt_errors(
            ROOT,
            CHECKER.TOPOLOGY_OWNER_DEBT_EVIDENCE | {"00_META/unrelated.md"},
        )
        self.assertTrue(
            any("must exactly match" in error for error in errors), errors
        )

        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            self.create_topology_tombstones(corpus)
            self.init_git_repo(corpus)
            self.commit_all(corpus, "add exact topology tombstones")
            self.assertEqual(CHECKER.unresolved_topology_errors(corpus), [])
            tombstone = corpus / CHECKER.HELD_TOPOLOGY_TOMBSTONES[0]
            original = tombstone.read_text(encoding="utf-8")
            tombstone.write_text(
                original.replace("Nothing here owns doctrine.", ""),
                encoding="utf-8",
            )
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("lost its exact title/no-doctrine frontmatter" in error for error in errors),
                errors,
            )

            tombstone.write_text(
                original + "\nThis lane owns doctrine.\n",
                encoding="utf-8",
            )
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("asserts active canon/doctrine/governance ownership" in error for error in errors),
                errors,
            )

            tombstone.write_text(
                original + "\nThis path is now structurally authoritative.\n",
                encoding="utf-8",
            )
            self.commit_all(corpus, "seed coordinated tombstone authority drift")
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("SHA-256 drifted" in error for error in errors),
                errors,
            )
            tombstone.write_text(original, encoding="utf-8")
            self.commit_all(corpus, "restore exact tombstone custody")

            tombstone.write_text(original, encoding="utf-8")
            unexpected = tombstone.parent / "README.md"
            unexpected.write_text("unexpected active route\n", encoding="utf-8")
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("tombstone inventory drifted" in error for error in errors),
                errors,
            )
            unexpected.unlink()

            tombstone.write_text(original + "\nneutral uncommitted drift\n", encoding="utf-8")
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("lacks exact regular-file Git index custody" in error for error in errors),
                errors,
            )

            tombstone.unlink()
            outside = corpus / "outside.md"
            outside.write_text(original, encoding="utf-8")
            tombstone.symlink_to(outside)
            errors = CHECKER.unresolved_topology_errors(corpus)
            self.assertTrue(
                any("regular, non-symlink" in error for error in errors),
                errors,
            )

    def test_owner_dockets_remain_exactly_unset(self) -> None:
        self.assertEqual(CHECKER.owner_docket_unset_errors(ROOT), [])
        for docket_id, contract in CHECKER.OWNER_DOCKET_UNSET_CONTRACT.items():
            with self.subTest(docket_id=docket_id), tempfile.TemporaryDirectory() as directory:
                corpus = Path(directory)
                target = corpus / CHECKER.OWNER_DOCKET
                target.parent.mkdir(parents=True)
                target.write_bytes((ROOT / CHECKER.OWNER_DOCKET).read_bytes())
                self.init_git_repo(corpus)
                self.commit_all(corpus, "add unset owner docket")
                body = target.read_text(encoding="utf-8")
                target.write_text(
                    body.replace(
                        contract["principal"],
                        "- **Principal:** selected without an owner ruling.",
                        1,
                    ),
                    encoding="utf-8",
                )
                errors = CHECKER.owner_docket_unset_errors(corpus)
                self.assertTrue(
                    any(
                        docket_id in error and "UNSET principal" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_topology_debt_cannot_be_reworded_as_present_conformance(self) -> None:
        state = copy.deepcopy(self.state)
        debt = next(
            row
            for row in state["owner_held"]["debts"]
            if row["id"] == "OWNER_GATE_OPEN_TOPOLOGY"
        )
        debt["question"] = "Is the current non-root path already conforming?"
        debt["close_when"] = "The existing files are declared complete."
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state)
        self.assertTrue(
            any(
                "OWNER_GATE_OPEN_TOPOLOGY" in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_fenced_code_cannot_counterfeit_an_unset_owner_docket(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            target = corpus / CHECKER.OWNER_DOCKET
            target.parent.mkdir(parents=True)
            body = (ROOT / CHECKER.OWNER_DOCKET).read_text(encoding="utf-8")
            contract = CHECKER.OWNER_DOCKET_UNSET_CONTRACT["D-OWNER-01"]
            section_start = body.index("## D-OWNER-01")
            section_end = body.index("## D-OWNER-02")
            hidden_section = body[section_start:section_end]
            body = body[:section_start] + body[section_end:]
            body = body.replace(contract["status_row"] + "\n", "", 1)
            body += (
                "\n```markdown\n"
                + contract["status_row"]
                + "\n"
                + hidden_section
                + "```\n"
            )
            target.write_text(body, encoding="utf-8")
            self.init_git_repo(corpus)
            self.commit_all(corpus, "add counterfeit fenced docket")
            errors = CHECKER.owner_docket_unset_errors(corpus)
            self.assertTrue(
                any("D-OWNER-01" in error for error in errors),
                errors,
            )

    def test_fabricated_world_evidence_fails_even_if_state_matches(self) -> None:
        state = copy.deepcopy(self.state)
        state["world_contact"]["state"] = "ESTABLISHED"
        state["world_contact"]["accepted_evidence_records"] = 2
        state["world_contact"]["open_requirements"] = []
        fabricated = {
            "state": "ESTABLISHED",
            "accepted_evidence_records": 2,
            "open_requirements": [],
        }
        self.assert_invalid(state, compute_world_contact=fabricated)

    def test_world_transition_gate_cannot_admit_internal_receipts(self) -> None:
        state = copy.deepcopy(self.state)
        state["world_contact"]["transition_gate"]["inadmissible_inputs"].remove(
            "internal receipts"
        )
        self.assert_invalid(state)

    def test_legacy_heuristic_cannot_be_presented_as_safe(self) -> None:
        state = copy.deepcopy(self.state)
        state["receipt_namespace"]["bare_numeric_boundary"] = (
            "The 91 legacy heuristic prefixes are safe."
        )
        self.assert_invalid(state)

    def test_reused_prefix_boundary_cannot_be_rebaselined_below_101(self) -> None:
        state = copy.deepcopy(self.state)
        receipt_state = state["receipt_namespace"]
        receipt_state["reused_prefixes"] = 100
        receipt_state["bare_unsafe_reused_prefixes"] = 100
        receipt_state["bare_numeric_boundary"] = (
            "All 100 reused prefixes remain unsafe as bare citations. "
            f"The live legacy heuristic marks "
            f"{receipt_state['legacy_heuristic_dangerous_prefixes']} dangerous prefixes "
            "but proves no target, direction, reciprocity, or cross-lane disambiguation."
        )
        receipts = copy.deepcopy(self.computed["compute_receipt_namespace"])
        receipts["reused_prefixes"] = 100
        receipts["bare_unsafe_reused_prefixes"] = 100
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_receipt_namespace=receipts)
        self.assertTrue(
            any("exactly 101" in error for error in raised.exception.errors),
            raised.exception.errors,
        )

    def test_mixed_negated_and_positive_missing_citations_are_separate(self) -> None:
        text = "Receipt 999 does not exist. Receipt 998 establishes the result."
        citations = list(CHECKER.CITATION.finditer(text))
        self.assertTrue(CHECKER.citation_is_negated(text, citations[0]))
        self.assertFalse(CHECKER.citation_is_negated(text, citations[1]))

    def test_coordinated_missing_citation_list_shares_negation(self) -> None:
        text = "r999 and r998 were never written."
        citations = list(CHECKER.CITATION.finditer(text))
        self.assertTrue(all(CHECKER.citation_is_negated(text, item) for item in citations))

    def test_receipt_target_disappearance_fails(self) -> None:
        state = copy.deepcopy(self.state)
        receipts = copy.deepcopy(self.computed["compute_receipt_namespace"])
        receipts["target_files"] -= 1
        self.assert_invalid(state, compute_receipt_namespace=receipts)

    def test_count_preserving_unique_receipt_target_swap_fails(self) -> None:
        receipts = copy.deepcopy(self.computed["compute_receipt_namespace"])
        receipts["identity_hashes"]["citable_targets_sha256"] = CHECKER.path_set_sha256(
            {"11_UPLINK/50_AUDITS_AND_EXECUTIONS/999_SYNTHETIC_2026_08_01.md"}
        )
        receipts["identity_hashes"]["prefixed_including_00_sha256"] = (
            CHECKER.path_set_sha256(
                {"11_UPLINK/50_AUDITS_AND_EXECUTIONS/999_SYNTHETIC_2026_08_01.md"}
            )
        )
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(self.state, compute_receipt_namespace=receipts)
        self.assertTrue(
            any("identity hashes drifted" in error for error in raised.exception.errors)
        )

    def test_receipt_namespace_rejects_direct_file_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.create_receipt_lanes(repo)
            outside = repo / "outside-receipt.md"
            outside.write_text("receipt\n", encoding="utf-8")
            linked = repo / CHECKER.RECEIPT_LANES[0] / "236_LINK_2026_08_01.md"
            linked.symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "receipt namespace entry.*symlink"
            ):
                CHECKER.compute_receipt_namespace(repo)

    def test_receipt_namespace_rejects_parent_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.create_receipt_lanes(repo)
            outside = repo / "outside-receipts"
            outside.mkdir()
            (outside / "236_LINK_2026_08_01.md").write_text(
                "receipt\n", encoding="utf-8"
            )
            parent = repo / CHECKER.RECEIPT_LANES[0] / "linked"
            parent.symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "receipt namespace entry.*symlink"
            ):
                CHECKER.compute_receipt_namespace(repo)

    def test_path_set_hash_is_unambiguous_for_newline_paths(self) -> None:
        self.assertNotEqual(
            CHECKER.path_set_sha256({"a\nb", "c"}),
            CHECKER.path_set_sha256({"a", "b\nc"}),
        )

    def test_nested_archive_ignore_rule_is_load_bearing(self) -> None:
        patterns = CHECKER._load_vercelignore(ROOT / CHECKER.VERCEL_IGNORE)
        patterns.remove("_archive/")
        with mock.patch.object(CHECKER, "_load_vercelignore", return_value=patterns):
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.compute_public_lifecycle(ROOT)

    def test_nested_archive_directory_semantics_match_public_predeploy(self) -> None:
        paths = (
            "_archive/index.html",
            "compass/_archive/index_2026_07_12_pre_restructure.html",
            "a/b/_archive/c.html",
            "A/B/_ARCHIVE/C.HTML",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue(CHECKER._vercelignore_matches(path, "_archive/"))
                self.assertTrue(PREDEPLOY.vercelignore_matches(path, "_archive/"))

    def test_archive_directory_rule_does_not_overmatch(self) -> None:
        paths = (
            "_archiveish/index.html",
            "compass/_archiveish/index.html",
            "compass/archive/index.html",
            "_archive.html",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertFalse(CHECKER._vercelignore_matches(path, "_archive/"))
                self.assertFalse(PREDEPLOY.vercelignore_matches(path, "_archive/"))

    def test_anchored_directory_rule_stays_at_the_site_root(self) -> None:
        pattern = "/_archive/"
        for matcher in (
            CHECKER._vercelignore_matches,
            PREDEPLOY.vercelignore_matches,
        ):
            with self.subTest(matcher=matcher.__module__):
                self.assertTrue(matcher("_archive/index.html", pattern))
                self.assertFalse(matcher("nested/_archive/index.html", pattern))

    def test_directory_globs_use_the_same_component_grammar(self) -> None:
        cases = (
            ("foo*/", "foobar/index.html", True),
            ("foo*/", "nested/foobar/index.html", True),
            ("foo?/", "fooa/index.html", True),
            ("foo?/", "foo/index.html", False),
            ("root/foo*/", "root/foobar/index.html", True),
            ("root/foo*/", "nested/root/foobar/index.html", False),
        )
        for pattern, path, expected in cases:
            with self.subTest(pattern=pattern, path=path):
                self.assertEqual(
                    CHECKER._vercelignore_matches(path, pattern), expected
                )
                self.assertEqual(PREDEPLOY.vercelignore_matches(path, pattern), expected)

    def test_directory_character_classes_fail_closed(self) -> None:
        with self.assertRaises(CHECKER.ContractError):
            CHECKER._vercelignore_matches("fooa/index.html", "foo[ab]/")
        with self.assertRaises(ValueError):
            PREDEPLOY.vercelignore_matches("fooa/index.html", "foo[ab]/")

    def test_ignored_parent_cannot_be_reincluded_by_child_only(self) -> None:
        patterns = ["_archive/", "!compass/_archive/index.html"]
        path = "compass/_archive/index.html"
        self.assertTrue(CHECKER._is_vercel_ignored(path, patterns))
        self.assertTrue(PREDEPLOY.is_vercel_ignored(path, patterns))

    def test_reincluded_parent_allows_reincluded_child(self) -> None:
        patterns = [
            "_archive/",
            "!compass/_archive/",
            "!compass/_archive/index.html",
        ]
        path = "compass/_archive/index.html"
        self.assertFalse(CHECKER._is_vercel_ignored(path, patterns))
        self.assertFalse(PREDEPLOY.is_vercel_ignored(path, patterns))

    def test_conflict_copy_pattern_matches_root_and_nested_files(self) -> None:
        pattern = "**/* 2.*"
        self.assertTrue(CHECKER._vercelignore_matches("page 2.html", pattern))
        self.assertTrue(CHECKER._vercelignore_matches("nested/page 2.html", pattern))
        self.assertFalse(CHECKER._vercelignore_matches("page.html", pattern))
        self.assertTrue(PREDEPLOY.vercelignore_matches("page 2.html", pattern))
        self.assertTrue(PREDEPLOY.vercelignore_matches("nested/page 2.html", pattern))
        self.assertFalse(PREDEPLOY.vercelignore_matches("page.html", pattern))

    def test_gitignore_negation_reincludes_public_build_wing(self) -> None:
        patterns = ["build/", "!build/", "!build/**"]
        self.assertFalse(CHECKER._is_vercel_ignored("build/index.html", patterns))
        self.assertFalse(PREDEPLOY.is_vercel_ignored("build/index.html", patterns))

    def test_publication_matchers_agree_on_every_present_site_file(self) -> None:
        patterns = CHECKER._load_vercelignore(ROOT / CHECKER.VERCEL_IGNORE)
        predeploy_patterns = PREDEPLOY.load_vercelignore_patterns()
        self.assertEqual(patterns, predeploy_patterns)
        site = ROOT / CHECKER.PUBLIC_DIR
        paths = sorted(
            path.relative_to(site).as_posix()
            for path in site.rglob("*")
            if path.is_file()
        )
        mismatches = [
            path
            for path in paths
            if CHECKER._is_vercel_ignored(path, patterns)
            != PREDEPLOY.is_vercel_ignored(path, predeploy_patterns)
        ]
        self.assertEqual(mismatches, [])

    def test_publication_matcher_drift_fails_lifecycle_computation(self) -> None:
        original = CHECKER._PREDEPLOY_POLICY.is_vercel_ignored

        def drifted(path, patterns):
            if path == "compass/_archive/index_2026_07_12_pre_restructure.html":
                return False
            return original(path, patterns)

        with mock.patch.object(
            CHECKER._PREDEPLOY_POLICY,
            "is_vercel_ignored",
            side_effect=drifted,
        ):
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.compute_public_lifecycle(ROOT)

    def test_public_lifecycle_rejects_symlinked_machine_owner_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            site = root / CHECKER.PUBLIC_DIR
            site.mkdir(parents=True)
            outside = fixture / "public_semantic_parity.json"
            outside.write_text("{}\n", encoding="utf-8")
            (root / CHECKER.PUBLIC_PARITY).symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "public lifecycle entry.*symlink"
            ):
                CHECKER.compute_public_lifecycle(root)

    def test_public_lifecycle_rejects_symlinked_site_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            root.mkdir()
            outside = fixture / "site"
            outside.mkdir()
            (root / CHECKER.PUBLIC_DIR).symlink_to(
                outside, target_is_directory=True
            )
            with self.assertRaisesRegex(
                CHECKER.ContractError, "public lifecycle root.*symlink"
            ):
                CHECKER.compute_public_lifecycle(root)

    def test_public_lifecycle_rejects_symlinked_html_inventory_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            root = fixture / "repo"
            site = root / CHECKER.PUBLIC_DIR
            site.mkdir(parents=True)
            outside = fixture / "outside.html"
            outside.write_text("<html></html>\n", encoding="utf-8")
            (site / "index.html").symlink_to(outside)
            with self.assertRaisesRegex(
                CHECKER.ContractError, "public lifecycle entry.*symlink"
            ):
                CHECKER.compute_public_lifecycle(root)

    def test_sitemap_exactly_matches_indexable_html_classes(self) -> None:
        contract = self.computed["compute_public_lifecycle"]["sitemap_contract"]
        self.assertEqual(contract["classes"], ["current", "provisional"])
        self.assertEqual(contract["routes"], 57)

    def test_vercel_runtime_html_does_not_change_source_census(self) -> None:
        entries = CHECKER._strict_tree_entries(
            ROOT, CHECKER.PUBLIC_DIR, "public lifecycle"
        )
        synthetic = (
            ROOT
            / CHECKER.PUBLIC_DIR
            / ".vercel/output/static/synthetic-runtime/index.html"
        )
        with mock.patch.object(
            CHECKER, "_strict_tree_entries", return_value=[*entries, synthetic]
        ):
            observed = CHECKER.compute_public_lifecycle(ROOT)
        self.assertEqual(
            observed["ignore_counts"],
            self.computed["compute_public_lifecycle"]["ignore_counts"],
        )
        self.assertEqual(
            observed["counts"],
            self.computed["compute_public_lifecycle"]["counts"],
        )

    def test_sitemap_extra_frozen_route_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sitemap = root / CHECKER.SITEMAP
            sitemap.parent.mkdir(parents=True)
            sitemap.write_text(
                """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://emergentism.org/</loc></url>
  <url><loc>https://emergentism.org/build/</loc></url>
</urlset>
""",
                encoding="utf-8",
            )
            with self.assertRaises(CHECKER.ContractError):
                CHECKER._exact_sitemap_contract(root, {"/"})

    def test_withheld_artifact_requires_real_hash_bound_regular_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            body = b"<html>held</html>\n"
            (site / "held.html").write_bytes(body)
            rows = [
                {
                    "artifact": "held.html",
                    "bytes": len(body),
                    "sha256": CHECKER.hashlib.sha256(body).hexdigest(),
                }
            ]
            self.assertEqual(
                CHECKER._validated_withheld_artifacts(site, rows), {"held.html"}
            )

    def test_withheld_artifact_rejects_direct_file_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            site = fixture / "site"
            site.mkdir()
            body = b"<html>held</html>\n"
            outside = fixture / "outside.html"
            outside.write_bytes(body)
            (site / "held.html").symlink_to(outside)
            rows = [
                {
                    "artifact": "held.html",
                    "bytes": len(body),
                    "sha256": CHECKER.hashlib.sha256(body).hexdigest(),
                }
            ]
            with self.assertRaisesRegex(
                CHECKER.ContractError, "withheld artifact.*symlink"
            ):
                CHECKER._validated_withheld_artifacts(site, rows)

    def test_withheld_artifact_rejects_parent_directory_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory)
            site = fixture / "site"
            site.mkdir()
            body = b"<html>held</html>\n"
            outside = fixture / "outside"
            outside.mkdir()
            (outside / "held.html").write_bytes(body)
            (site / "nested").symlink_to(outside, target_is_directory=True)
            rows = [
                {
                    "artifact": "nested/held.html",
                    "bytes": len(body),
                    "sha256": CHECKER.hashlib.sha256(body).hexdigest(),
                }
            ]
            with self.assertRaisesRegex(
                CHECKER.ContractError, "withheld artifact.*symlink"
            ):
                CHECKER._validated_withheld_artifacts(site, rows)

    def test_count_preserving_withheld_deletion_substitution_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            replacement = b"<html>replacement</html>\n"
            (site / "ignored-replacement.html").write_bytes(replacement)
            rows = [
                {
                    "artifact": "deleted-held.html",
                    "bytes": len(replacement),
                    "sha256": CHECKER.hashlib.sha256(replacement).hexdigest(),
                }
            ]
            with self.assertRaisesRegex(CHECKER.ContractError, "missing or not a regular file"):
                CHECKER._validated_withheld_artifacts(site, rows)

    def test_withheld_artifact_path_escape_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(CHECKER.ContractError, "unsafe or not HTML"):
                CHECKER._validated_withheld_artifacts(
                    Path(directory),
                    [{"artifact": "../escape.html", "bytes": 0, "sha256": "0" * 64}],
                )

    def test_alias_collision_insertion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        collision = {
            "route": "/synthetic/",
            "artifacts": ["synthetic.html", "synthetic/index.html"],
            "shared_raw_lifecycle": "frozen",
        }
        state["public_lifecycle"]["delivery_contract"]["alias_collisions"] = [
            {**collision, "evidence": ["12_PUBLIC_SITE/vercel.json"]}
        ]
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["alias_collisions"] = [collision]
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "alias-collision baseline changed" in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_zero_alias_collision_source_contract_is_exact(self) -> None:
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        self.assertEqual(public["alias_collisions"], [])
        self.assertEqual(CHECKER.EXPECTED_ALIAS_COLLISIONS, [])

    def test_withheld_public_alias_cannot_name_two_artifacts(self) -> None:
        registry = CHECKER.load_json(ROOT / CHECKER.WITHHELD_REGISTRY)
        registry = copy.deepcopy(registry)
        registry["artifacts"][0]["publicRoutes"].append("/dasein/")
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.WITHHELD_REGISTRY:
                return registry
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.compute_public_lifecycle(ROOT)

    def test_count_preserving_withheld_alias_duplication_fails(self) -> None:
        registry = CHECKER.load_json(ROOT / CHECKER.WITHHELD_REGISTRY)
        registry = copy.deepcopy(registry)
        routes = registry["artifacts"][0]["publicRoutes"]
        routes[routes.index("/app/")] = "/app"
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.WITHHELD_REGISTRY:
                return registry
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.compute_public_lifecycle(ROOT)

    def test_count_preserving_current_provisional_membership_swap_fails(self) -> None:
        parity = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.PUBLIC_PARITY))
        current = parity["currentSurfaces"]
        provisional = parity["declaredProvisional"]["routes"]
        current[current.index("about/index.html")] = "egg/index.html"
        provisional[provisional.index("egg/index.html")] = "about/index.html"
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.PUBLIC_PARITY:
                return parity
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            public = CHECKER.compute_public_lifecycle(ROOT)
        self.assertEqual(
            public["counts"], self.computed["compute_public_lifecycle"]["counts"]
        )
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(self.state, compute_public_lifecycle=public)
        self.assertTrue(
            any("membership hashes drifted" in error for error in raised.exception.errors)
        )

    def test_count_preserving_frozen_current_membership_hash_swap_fails(self) -> None:
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        hashes = public["membership_hashes"]["category_sha256"]
        hashes["current_sha256"], hashes["frozen_sha256"] = (
            hashes["frozen_sha256"],
            hashes["current_sha256"],
        )
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(self.state, compute_public_lifecycle=public)
        self.assertTrue(
            any("membership hashes drifted" in error for error in raised.exception.errors)
        )

    def test_new_current_noindex_overlap_fails(self) -> None:
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["raw_overlaps"].append(
            {"classes": ["current", "frozen"], "artifacts": ["index.html"]}
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_raw_overlap_class_pair_cannot_be_coordinately_added(self) -> None:
        state = copy.deepcopy(self.state)
        row = {
            "classes": ["current", "frozen"],
            "artifacts": ["index.html"],
        }
        state["public_lifecycle"]["delivery_contract"]["allowed_raw_overlaps"].append(
            {**row, "evidence": ["12_PUBLIC_SITE/vercel.json"]}
        )
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["raw_overlaps"].append(row)
        public["raw_overlaps"].sort(key=lambda item: tuple(item["classes"]))
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "must retain exactly the frozen/infrastructure and frozen/withheld"
                in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_frozen_withheld_overlap_insertion_cannot_be_coordinately_rebaselined(
        self,
    ) -> None:
        state = copy.deepcopy(self.state)
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        inserted = "z-reviewer-overlap-insertion/index.html"
        for rows in (
            state["public_lifecycle"]["delivery_contract"]["allowed_raw_overlaps"],
            public["raw_overlaps"],
        ):
            row = next(
                item
                for item in rows
                if item["classes"] == ["frozen", "withheld"]
            )
            row["artifacts"].append(inserted)
            row["artifacts"].sort()
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "frozen/withheld overlap inventory drifted" in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_frozen_withheld_overlap_removal_cannot_be_coordinately_rebaselined(
        self,
    ) -> None:
        state = copy.deepcopy(self.state)
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        removed = "atlas/index.html"
        for rows in (
            state["public_lifecycle"]["delivery_contract"]["allowed_raw_overlaps"],
            public["raw_overlaps"],
        ):
            row = next(
                item
                for item in rows
                if item["classes"] == ["frozen", "withheld"]
            )
            row["artifacts"].remove(removed)
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "frozen/withheld overlap inventory drifted" in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_exact_current_route_bare_noindex_becomes_forbidden_overlap(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/about/",
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assertTrue(
            any(
                row["classes"] == ["current", "frozen"]
                and "about/index.html" in row["artifacts"]
                for row in public["raw_overlaps"]
            )
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_nested_provisional_route_bare_noindex_becomes_forbidden_overlap(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/egg/(.*)",
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assertTrue(
            any(
                row["classes"] == ["frozen", "provisional"]
                and "egg/index.html" in row["artifacts"]
                for row in public["raw_overlaps"]
            )
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_broad_bare_noindex_fails_public_lifecycle_baseline(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/(.*)",
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_robots_none_expands_to_withholding(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/about/",
                "headers": [{"key": "X-Robots-Tag", "value": "none"}],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assertTrue(
            any(
                row["classes"] == ["current", "withheld"]
                and "about/index.html" in row["artifacts"]
                for row in public["raw_overlaps"]
            )
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_duplicate_robots_headers_cannot_erase_noindex(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/about/",
                "headers": [
                    {"key": "X-Robots-Tag", "value": "noindex"},
                    {"key": "X-Robots-Tag", "value": "index"},
                ],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assertTrue(
            any(
                row["classes"] == ["current", "frozen"]
                and "about/index.html" in row["artifacts"]
                for row in public["raw_overlaps"]
            )
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_robots_meta_parser_tolerates_attribute_order_case_and_quotes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "surface.html"
            path.write_text(
                "<html><head><META content='NoIndex, follow' NAME=\"RoBoTs\"></head></html>",
                encoding="utf-8",
            )
            self.assertEqual(
                CHECKER._meta_robots_directives(path), {"noindex", "follow"}
            )

    def test_current_and_provisional_cannot_self_declare_search_hiding(self) -> None:
        original = CHECKER._meta_robots_directives
        cases = (
            ("about/index.html", "current", {"noindex"}),
            ("egg/index.html", "provisional", {"none"}),
        )
        for artifact, asserted_class, injected in cases:
            with self.subTest(artifact=artifact):
                target = ROOT / CHECKER.PUBLIC_DIR / artifact

                def mutated(path, *, target=target, injected=injected):
                    return injected if path == target else original(path)

                with mock.patch.object(
                    CHECKER, "_meta_robots_directives", side_effect=mutated
                ):
                    with self.assertRaisesRegex(
                        CHECKER.ContractError,
                        rf"{asserted_class} artifact {artifact} self-declares",
                    ):
                        CHECKER.compute_public_lifecycle(ROOT)

    def test_current_route_nofollow_header_becomes_forbidden_overlap(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/about/",
                "headers": [
                    {"key": "X-Robots-Tag", "value": "noindex, nofollow"}
                ],
            }
        )
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.VERCEL_CONFIG:
                return vercel
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            public = CHECKER.compute_public_lifecycle(ROOT)
        self.assertTrue(
            any(
                row["classes"] == ["current", "withheld"]
                and "about/index.html" in row["artifacts"]
                for row in public["raw_overlaps"]
            )
        )
        self.assert_invalid(self.state, compute_public_lifecycle=public)

    def test_broad_nofollow_header_fails_public_lifecycle(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["headers"].append(
            {
                "source": "/(.*)",
                "headers": [
                    {"key": "X-Robots-Tag", "value": "noindex, nofollow"}
                ],
            }
        )
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.VERCEL_CONFIG:
                return vercel
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            public = CHECKER.compute_public_lifecycle(ROOT)
        with self.assertRaises(CHECKER.ContractError) as raised:
            self.validate_fast(self.state, compute_public_lifecycle=public)
        self.assertTrue(
            any(
                "raw lifecycle overlap ledger drifted" in error
                for error in raised.exception.errors
            ),
            raised.exception.errors,
        )

    def test_current_route_redirect_fails_public_lifecycle(self) -> None:
        vercel = copy.deepcopy(CHECKER.load_json(ROOT / CHECKER.VERCEL_CONFIG))
        vercel["redirects"].append(
            {
                "source": "/about/",
                "destination": "/historical-boundary/",
                "permanent": False,
            }
        )
        original_load = CHECKER.load_json

        def mutated_load(path):
            if Path(path) == ROOT / CHECKER.VERCEL_CONFIG:
                return vercel
            return original_load(path)

        with mock.patch.object(CHECKER, "load_json", side_effect=mutated_load):
            with self.assertRaisesRegex(CHECKER.ContractError, "effective redirect"):
                CHECKER.compute_public_lifecycle(ROOT)

    def test_missing_nested_evidence_path_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["owner_held"]["debts"][0]["evidence"][1] = "missing.md"
        self.assert_invalid(state)

    def test_malformed_state_is_contract_failure_not_traceback(self) -> None:
        self.assert_invalid({"schema": "emergentism/contact-limited-state/v1"})
        output = io.StringIO()
        with mock.patch.object(
            CHECKER, "check", side_effect=CHECKER.ContractError("malformed state")
        ), contextlib.redirect_stdout(output):
            self.assertEqual(CHECKER.main(), 1)
        self.assertIn("CONTACT-LIMITED RATCHET: FAIL", output.getvalue())

    def test_duplicate_key_state_json_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "CONTACT_LIMITED_STATE.json"
            path.write_text(
                '{"schema":"first","schema":"hidden replacement"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                CHECKER.ContractError, "duplicate JSON object key 'schema'"
            ):
                CHECKER.load_json(path)


if __name__ == "__main__":
    unittest.main()
