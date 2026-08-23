#!/usr/bin/env python3
"""Adversarial tests for M4, SLWP and force-permutation contracts."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
sys.path.insert(0, str(PACKAGE))

from research_contracts import (  # noqa: E402
    force_fixture,
    validate_force,
    validate_m4,
    validate_slwp,
)


def load(name: str) -> dict[str, object]:
    return json.loads((PACKAGE / "fixtures" / name).read_text(encoding="utf-8"))


class M4Tests(unittest.TestCase):
    def test_valid_fixture_is_unrun_and_comparator_complete(self) -> None:
        value = load("m4_dev.json")
        self.assertEqual([], validate_m4(value))
        self.assertEqual("UNRUN", value["result_state"])

    def test_missing_comparator_fails(self) -> None:
        value = load("m4_dev.json")
        value["comparators"].pop()
        self.assertTrue(any("comparator class drift" in row for row in validate_m4(value)))

    def test_global_exhaustion_and_unbounded_maximality_fail(self) -> None:
        value = load("m4_dev.json")
        value["global_game_theory_exhausted"] = True
        value["maximality_scope"] = "ALL_GAME_THEORY"
        errors = validate_m4(value)
        self.assertTrue(any("exhaust game theory" in row for row in errors))
        self.assertTrue(any("comparator-class relative" in row for row in errors))


class SLWPTests(unittest.TestCase):
    def test_reducible_fixture_proves_projection_only(self) -> None:
        value = load("slwp_dev.json")
        self.assertEqual([], validate_slwp(value))
        self.assertEqual("PROJECTION_ASYMMETRY_PROVEN", value["projection_result"])
        self.assertEqual("REDUCED", value["ontology_result"])
        self.assertFalse(value["strong_emergence_established"])

    def test_reverse_identity_drift_kills_projection_claim(self) -> None:
        value = load("slwp_dev.json")
        value["recovery_result"]["s_after_U_identity"] = True
        self.assertTrue(any("projection asymmetry" in row for row in validate_slwp(value)))

    def test_fiber_lemma_cannot_establish_open_ontology(self) -> None:
        value = load("slwp_dev.json")
        value["ontology_result"] = "OPEN"
        value["strong_emergence_established"] = True
        self.assertTrue(any("cannot establish strong emergence" in row for row in validate_slwp(value)))


class ForceTests(unittest.TestCase):
    def test_generator_contains_all_24_bijections_once(self) -> None:
        value = force_fixture()
        self.assertEqual([], validate_force(value))
        assignments = {
            tuple(row["assignment"][register] for register in value["registers"])
            for row in value["candidates"]
        }
        self.assertEqual(24, len(assignments))

    def test_burri_agreement_never_counts_as_correctness(self) -> None:
        value = force_fixture()
        value["agreement_with_burri_counts_as_correctness"] = True
        self.assertTrue(any("cannot count as correctness" in row for row in validate_force(value)))

    def test_duplicate_and_nonbijective_candidate_fail(self) -> None:
        value = force_fixture()
        value["candidates"][1]["candidate_id"] = value["candidates"][0]["candidate_id"]
        value["candidates"][1]["assignment"]["D4"] = value["candidates"][1]["assignment"]["D3"]
        errors = validate_force(value)
        self.assertTrue(any("duplicate force candidate" in row for row in errors))
        self.assertTrue(any("not bijective" in row for row in errors))

    def test_required_rivals_and_d3_gate_cannot_be_removed(self) -> None:
        value = force_fixture()
        value["rivals"] = value["rivals"][:1]
        value["d3_quantum_specific_gate"]["generic_quantumness_sufficient"] = True
        errors = validate_force(value)
        self.assertTrue(any("missing no-map" in row for row in errors))
        self.assertTrue(any("generic quantumness" in row for row in errors))

    def test_fixture_is_deterministic(self) -> None:
        self.assertEqual(force_fixture(), load("force_24.json"))


class SchemaTests(unittest.TestCase):
    def test_schema_files_are_valid_json_draft_2020_12(self) -> None:
        for path in sorted((PACKAGE / "schemas").glob("*.schema.json")):
            with self.subTest(path=path.name):
                value = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("https://json-schema.org/draft/2020-12/schema", value["$schema"])


if __name__ == "__main__":
    unittest.main()
