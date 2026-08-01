#!/usr/bin/env python3
"""Contract tests for the typed coherence-profile validator."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_coherence_profile.py"
SPEC = importlib.util.spec_from_file_location("check_coherence_profile", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class CoherenceProfileTests(unittest.TestCase):
    def make_fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path, dict]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "receipt.md").write_text(
            " ".join(
                (
                    "ROUTING-PASS_WITH_DEBT",
                    "ROUTING-QUARANTINE",
                    "ROUTING-BLOCK",
                    "SEMANTIC-HOLD",
                    "HIDDEN-DEBT",
                )
            ),
            encoding="utf-8",
        )
        (root / "wip.md").write_text("fixture WIP", encoding="utf-8")
        (root / "observation.md").write_text("external observation custody", encoding="utf-8")
        (root / "replication.md").write_text("independent replication custody", encoding="utf-8")
        (root / "review.md").write_text("external review custody", encoding="utf-8")
        profile = {
            "schema": CHECKER.SCHEMA,
            "profile_id": "fixture",
            "scope": "fixture scope",
            "authority_refs": ["receipt.md", "wip.md"],
            "axes": {
                "semantic": {
                    "state": "PASS",
                    "basis_refs": ["receipt.md"],
                    "debt_ids": [],
                },
                "routing": {
                    "state": "PASS",
                    "basis_refs": ["receipt.md"],
                    "debt_ids": [],
                },
                "operational": {
                    "state": "PASS",
                    "basis_refs": ["receipt.md"],
                    "debt_ids": [],
                },
                "world_contact": {
                    "state": "OPEN",
                    "evidence": [],
                    "open_requirements": ["independent observation"],
                },
            },
            "overall": {"scope": "internal", "state": "PASS"},
        }
        return temp, root, profile

    def test_internal_pass_does_not_close_world_contact(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        self.assertEqual(CHECKER.validate_profile(profile, root), ("PASS", "OPEN"))

    def test_internal_overall_uses_worst_axis_state(self) -> None:
        for state, expected in (
            ("PASS", "PASS"),
            ("PASS_WITH_DEBT", "PASS_WITH_DEBT"),
            ("QUARANTINE", "QUARANTINE"),
            ("BLOCK", "BLOCK"),
        ):
            with self.subTest(state=state):
                temp, root, profile = self.make_fixture()
                try:
                    profile["axes"]["routing"]["state"] = state
                    profile["axes"]["routing"]["debt_ids"] = (
                        [] if state == "PASS" else [f"ROUTING-{state}"]
                    )
                    profile["overall"]["state"] = expected
                    self.assertEqual(CHECKER.validate_profile(profile, root)[0], expected)
                finally:
                    temp.cleanup()

    def test_mismatched_overall_state_fails(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["semantic"].update(
            state="QUARANTINE",
            debt_ids=["SEMANTIC-HOLD"],
        )
        with self.assertRaisesRegex(CHECKER.ProfileError, "computed QUARANTINE"):
            CHECKER.validate_profile(profile, root)

    def test_pass_cannot_hide_declared_debt(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["semantic"]["debt_ids"] = ["HIDDEN-DEBT"]
        with self.assertRaisesRegex(CHECKER.ProfileError, "PASS cannot retain"):
            CHECKER.validate_profile(profile, root)

    def test_debt_must_be_named_by_basis_authority(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["semantic"].update(
            state="PASS_WITH_DEBT",
            debt_ids=["UNOWNED-DEBT"],
        )
        profile["overall"]["state"] = "PASS_WITH_DEBT"
        with self.assertRaisesRegex(CHECKER.ProfileError, "not named by a basis authority"):
            CHECKER.validate_profile(profile, root)

    def test_internal_gate_is_not_world_contact_evidence(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["world_contact"] = {
            "state": "PARTIAL",
            "evidence": [
                {"kind": "internal_gate", "ref": "gate-run", "outcome": "supports"}
            ],
            "open_requirements": ["external observation"],
        }
        with self.assertRaisesRegex(CHECKER.ProfileError, "internal gates are inadmissible"):
            CHECKER.validate_profile(profile, root)

    def test_established_world_contact_requires_observation_and_replication(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["world_contact"] = {
            "state": "ESTABLISHED",
            "evidence": [
                {"kind": "external_review", "ref": "review.md", "outcome": "supports"}
            ],
            "open_requirements": [],
        }
        with self.assertRaisesRegex(CHECKER.ProfileError, "requires external observation"):
            CHECKER.validate_profile(profile, root)

    def test_established_world_contact_positive_contract(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["world_contact"] = {
            "state": "ESTABLISHED",
            "evidence": [
                {
                    "kind": "external_observation",
                    "ref": "observation.md",
                    "outcome": "supports",
                },
                {
                    "kind": "independent_replication",
                    "ref": "replication.md",
                    "outcome": "supports",
                },
            ],
            "open_requirements": [],
        }
        self.assertEqual(CHECKER.validate_profile(profile, root), ("PASS", "ESTABLISHED"))

    def test_world_contact_requires_repository_custody(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["axes"]["world_contact"] = {
            "state": "PARTIAL",
            "evidence": [
                {
                    "kind": "external_review",
                    "ref": "missing-review.md",
                    "outcome": "mixed",
                }
            ],
            "open_requirements": ["independent replication"],
        }
        with self.assertRaisesRegex(CHECKER.ProfileError, "missing authority file"):
            CHECKER.validate_profile(profile, root)

    def test_missing_authority_reference_fails_closed(self) -> None:
        temp, root, profile = self.make_fixture(); self.addCleanup(temp.cleanup)
        profile["authority_refs"].append("missing.md")
        with self.assertRaisesRegex(CHECKER.ProfileError, "missing authority file"):
            CHECKER.validate_profile(profile, root)


if __name__ == "__main__":
    unittest.main()
