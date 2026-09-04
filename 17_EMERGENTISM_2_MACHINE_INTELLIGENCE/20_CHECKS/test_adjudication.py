#!/usr/bin/env python3
"""Red/green tests for ADJ-01. Mutations must fail; fixtures must pass."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from check_adjudication import HERE, validate_adjudication

FIXTURES = HERE / "fixtures"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class AdjudicationTests(unittest.TestCase):
    def test_fixtures_pass(self) -> None:
        for name in (
            "axis_mix.json",
            "constructionist.json",
            "noninvertible_as_strong.json",
            "slwp_reduced_wrap.json",
            "incomplete_mu.json",
            "mind_d5_incomplete.json",
        ):
            with self.subTest(name=name):
                errors = validate_adjudication(load(name))
                self.assertEqual(errors, [], errors)

    def test_axis_mix_missed_is_red(self) -> None:
        packet = load("axis_mix.json")
        packet["axis"] = "PASS"
        packet["verdict"] = "OPEN"
        errors = validate_adjudication(packet)
        self.assertTrue(any("axis-mix missed" in row for row in errors), errors)

    def test_world_reading_S_is_red(self) -> None:
        packet = load("incomplete_mu.json")
        packet["world_reading_tier"] = "S"
        errors = validate_adjudication(packet)
        self.assertTrue(any("never S" in row for row in errors), errors)

    def test_constructionist_left_open_is_red(self) -> None:
        packet = load("constructionist.json")
        packet["verdict"] = "OPEN"
        packet["anderson_inference"] = "NOT_USED"
        errors = validate_adjudication(packet)
        self.assertTrue(
            any("constructionist" in row for row in errors),
            errors,
        )

    def test_reduced_cannot_claim_strong(self) -> None:
        packet = load("slwp_reduced_wrap.json")
        packet["strong_emergence_established"] = True
        packet["verdict"] = "SURVIVES_BOUNDED_TEST"
        errors = validate_adjudication(packet)
        self.assertTrue(
            any("strong emergence" in row or "REDUCED" in row for row in errors),
            errors,
        )

    def test_identity_mismatch(self) -> None:
        self.assertEqual(
            validate_adjudication({"schema_id": "nope"}),
            ["Adjudication identity mismatch"],
        )

    def test_mutation_does_not_edit_fixture_bytes(self) -> None:
        original = (FIXTURES / "axis_mix.json").read_bytes()
        packet = load("axis_mix.json")
        mutated = copy.deepcopy(packet)
        mutated["axis"] = "PASS"
        validate_adjudication(mutated)
        self.assertEqual((FIXTURES / "axis_mix.json").read_bytes(), original)


if __name__ == "__main__":
    raise SystemExit(unittest.main(verbosity=2))
