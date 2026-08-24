#!/usr/bin/env python3
"""Focused standard-library tests for the Fourth Churning source packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PQA = (
    ROOT
    / "14_THE_DISTILLATION"
    / "07_THE_THIRD_CHURNING_2026_08_23"
    / "data"
    / "problem_adjudications.v1.json"
)
THIRD = (
    ROOT
    / "14_THE_DISTILLATION"
    / "07_THE_THIRD_CHURNING_2026_08_23"
    / "ThirdChurningCorpus.v1.json"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FourthChurningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.collisions = load(HERE / "data" / "type_collisions.v1.json")
        cls.diagnoses = load(HERE / "data" / "mystery_diagnoses.v1.json")
        cls.corpus = load(HERE / "FourthChurningCorpus.v1.json")
        cls.by_problem = {row["problem_id"]: row for row in cls.diagnoses}

    def test_01_denominator_and_earned_state_remain_frozen(self) -> None:
        self.assertEqual(len(self.diagnoses), 54)
        self.assertEqual(len(self.by_problem), 54)
        self.assertEqual(
            self.corpus["pqa_state"],
            {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0},
        )
        self.assertTrue(all(row["earned_effect"] == "NO_INCREMENT" for row in self.diagnoses))
        self.assertTrue(all(row["result_state"] == "SELECTED_UNREVIEWED" for row in self.diagnoses))
        self.assertEqual(sha(PQA), "7618139f3ab376c017ececaa64c88e33c097cdb0efd245f3b2453f65d78c4b8a")  # pragma: allow-secret

    def test_02_grammar_has_seven_axes_and_twelve_subtypes(self) -> None:
        self.assertEqual(len(self.collisions), 12)
        self.assertEqual(
            {row["axis"] for row in self.collisions},
            {"LEVEL", "MODAL", "TEMPORAL", "REPRESENTATIONAL", "EPISTEMIC", "NORMATIVE", "BEARER"},
        )
        self.assertEqual([row["collision_id"] for row in self.collisions], [f"TCX-{n:02d}" for n in range(1, 13)])

    def test_03_nulls_and_underdetermination_are_real_outputs(self) -> None:
        self.assertEqual(
            self.corpus["candidate_counts"],
            {"TYPE_COLLISION": 1, "PARTIAL_TYPE_COLLISION": 46, "NO_COLLISION": 2, "UNDERDETERMINED": 5},
        )
        for row in self.diagnoses:
            if row["diagnosis_state"] in {"NO_COLLISION", "UNDERDETERMINED"}:
                self.assertIsNone(row["alleged_invalid_join"])
        self.assertEqual(self.by_problem["PQA54@0.1:SCI:BELL"]["diagnosis_state"], "NO_COLLISION")
        self.assertEqual(self.by_problem["PQA54@0.1:ULT:EVIL"]["diagnosis_state"], "NO_COLLISION")
        self.assertEqual(self.by_problem["PQA54@0.1:MIN:CONSCIOUSNESS"]["diagnosis_state"], "UNDERDETERMINED")

    def test_04_only_canonical_ids_join_the_overlay(self) -> None:
        pqa_rows = load(PQA)
        self.assertEqual(
            [row["problem_id"] for row in pqa_rows],
            [row["problem_id"] for row in self.diagnoses],
        )
        liar = next(row for row in pqa_rows if row["problem_id"].endswith(":LOG:LIAR"))
        russell = next(row for row in pqa_rows if row["problem_id"].endswith(":LOG:RUSSELL"))
        self.assertIn("LEGACY:PD-08", liar["aliases"])
        self.assertIn("LEGACY:PD-08", russell["aliases"])
        self.assertNotIn("aliases", self.diagnoses[0])

    def test_05_schema_objects_cannot_self_award_dissolution(self) -> None:
        self.assertNotIn("review_count", self.collisions[0])
        self.assertNotIn("earned_effect", self.collisions[0])
        self.assertNotIn("TYPE_DISSOLUTION", {row["proposed_effect"] for row in self.diagnoses})
        self.assertEqual(self.by_problem["PQA54@0.1:LOG:RUSSELL"]["diagnosis_state"], "TYPE_COLLISION")
        self.assertEqual(self.by_problem["PQA54@0.1:LOG:RUSSELL"]["proposed_effect"], "FORMAL_CORRECTION")

    def test_06_contaminated_split_is_never_called_held_out(self) -> None:
        self.assertEqual(self.corpus["held_out_integrity"], "CONTAMINATED_FOR_FOURTH_USE")
        self.assertTrue(all(row["split_integrity"] == "CONTAMINATED_FOR_FOURTH_USE" for row in self.diagnoses))
        self.assertFalse(self.corpus["global_philosophy_claim_allowed"])

    def test_07_third_and_fourth_public_outputs_are_disjoint(self) -> None:
        third_outputs = set(load(THIRD)["output_map"].values())
        fourth_outputs = set(self.corpus["public_output_map"].values())
        self.assertTrue(third_outputs.isdisjoint(fourth_outputs))
        self.assertTrue(self.corpus["third_churning_immutable"])

    def test_08_builder_check_is_read_only_and_deterministic(self) -> None:
        tracked = [
            HERE / "data" / "type_collisions.v1.json",
            HERE / "data" / "mystery_diagnoses.v1.json",
            HERE / "FourthChurningCorpus.v1.json",
        ]
        before = {path: sha(path) for path in tracked}
        result = subprocess.run(
            ["python3", "-B", str(HERE / "build_type_atlas.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, {path: sha(path) for path in tracked})

    def test_09_closed_contract_validation_rejects_unknown_fields(self) -> None:
        spec = importlib.util.spec_from_file_location("fourth_builder", HERE / "build_type_atlas.py")
        self.assertIsNotNone(spec)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        hostile = dict(self.collisions[0])
        hostile["earned_result"] = "TYPE_DISSOLUTION"
        with self.assertRaises(ValueError):
            module.validate_closed(hostile, HERE / "contracts" / "TypeCollision.v1.schema.json", "hostile")


if __name__ == "__main__":
    unittest.main()
