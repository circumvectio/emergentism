#!/usr/bin/env python3
"""Mutation controls for review-bundle readiness projection."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "09_TOOLS/01_SCRIPTS/check_review_bundle.py"
SPEC = importlib.util.spec_from_file_location("check_review_bundle", CHECKER_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ReviewBundleStatusTests(unittest.TestCase):
    def test_live_packet_matches_blocked_registry(self) -> None:
        state = CHECKER.review_execution_state()
        packet = (
            ROOT
            / "03_METHODOLOGY/03_PREREGISTRATIONS/finity_practice/REVIEW_BUNDLE_v2.md"
        ).read_text(encoding="utf-8")
        self.assertEqual(state, "blocked")
        self.assertEqual(CHECKER.document_status_errors(packet, state), [])

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
