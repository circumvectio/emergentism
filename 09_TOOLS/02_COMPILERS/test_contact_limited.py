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
        subprocess.run(
            ["git", "-C", str(repo), "commit", "-qm", message], check=True
        )

    def create_receipt_lanes(self, repo: Path) -> None:
        for relative_lane in CHECKER.RECEIPT_LANES:
            (repo / relative_lane).mkdir(parents=True, exist_ok=True)

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

    def test_live_contract_passes_with_exact_scope(self) -> None:
        report = CHECKER.check(ROOT)
        self.assertEqual(
            report["receipt_namespace"]["target_files"],
            self.state["receipt_namespace"]["target_files"],
        )
        self.assertEqual(report["receipt_namespace"]["bare_unsafe_reused_prefixes"], 97)
        self.assertEqual(report["public_lifecycle"]["counts"]["total"], 398)
        self.assertEqual(report["claim_disposition"]["w_rows"], 17)
        self.assertEqual(report["claim_disposition"]["reopened_rows"], 9)
        self.assertEqual(report["owner_held"], 2)
        self.assertEqual(report["world_contact"]["state"], "OPEN")

    def test_public_artifact_disappearance_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["public_lifecycle"]["unclassified"].pop()
        self.assert_invalid(state)

    def test_double_claim_classification_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["w_scope"]["internal_disposition"].append("W2")
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

    def test_git_history_unavailable_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.committed_receipt_bytes(
                    Path(directory), Path("236_RECEIPT_2026_08_01.md")
                )

    def test_w3_mapping_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["w_scope"]["internal_disposition"].remove("W3")
        self.assert_invalid(state)

    def test_reopened_question_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["claim_disposition"]["reopened_scope"]["ids"].remove("RQ-09")
        state["claim_disposition"]["reopened_scope"]["rows"] -= 1
        self.assert_invalid(state)

    def test_count_preserving_per_id_status_swap_fails(self) -> None:
        claims = copy.deepcopy(self.computed["compute_claim_disposition"])
        statuses = claims["w_scope"]["statuses"]
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

    def test_legacy_91_cannot_be_presented_as_safe(self) -> None:
        state = copy.deepcopy(self.state)
        state["receipt_namespace"]["bare_numeric_boundary"] = (
            "The 91 legacy heuristic prefixes are safe."
        )
        self.assert_invalid(state)

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

    def test_conflict_copy_pattern_matches_root_and_nested_files(self) -> None:
        pattern = "**/* 2.*"
        self.assertTrue(CHECKER._vercelignore_matches("page 2.html", pattern))
        self.assertTrue(CHECKER._vercelignore_matches("nested/page 2.html", pattern))
        self.assertFalse(CHECKER._vercelignore_matches("page.html", pattern))

    def test_gitignore_negation_reincludes_public_build_wing(self) -> None:
        patterns = ["build/", "!build/", "!build/**"]
        self.assertFalse(CHECKER._is_vercel_ignored("build/index.html", patterns))

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

    def test_alias_collision_deletion_fails(self) -> None:
        state = copy.deepcopy(self.state)
        state["public_lifecycle"]["delivery_contract"]["alias_collisions"] = []
        self.assert_invalid(state)

    def test_alias_lifecycle_disagreement_fails(self) -> None:
        public = copy.deepcopy(self.computed["compute_public_lifecycle"])
        public["alias_collisions"][0]["shared_raw_lifecycle"] = "current"
        self.assert_invalid(self.state, compute_public_lifecycle=public)

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
        current[current.index("about/index.html")] = "amrita/index.html"
        provisional[provisional.index("amrita/index.html")] = "about/index.html"
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
                "source": "/amrita/(.*)",
                "headers": [{"key": "X-Robots-Tag", "value": "noindex"}],
            }
        )
        public = self.compute_public_with_vercel(vercel)
        self.assertTrue(
            any(
                row["classes"] == ["frozen", "provisional"]
                and "amrita/index.html" in row["artifacts"]
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
            ("amrita/index.html", "provisional", {"none"}),
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
            with self.assertRaises(CHECKER.ContractError):
                CHECKER.compute_public_lifecycle(ROOT)

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
        state["claim_disposition"]["w3_guard"]["evidence"][1] = "missing.md"
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
