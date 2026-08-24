#!/usr/bin/env python3
"""Adversarial checks for the Fourth Churning public projection."""

from __future__ import annotations

import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent
PACKET = ROOT / "14_THE_DISTILLATION" / "08_THE_FOURTH_CHURNING_2026_08_24"


class FourthChurningPublicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = json.loads((PACKET / "FourthChurningCorpus.v1.json").read_text())
        cls.diagnoses = json.loads((SITE / "questions/diagnoses.json").read_text())
        cls.collisions = json.loads((SITE / "questions/collisions.json").read_text())
        cls.page = (SITE / "questions/diagnoses/index.html").read_text()
        cls.atlas = (SITE / "questions/index.html").read_text()

    def test_deterministic_builder_is_read_only_in_check_mode(self) -> None:
        before = {path: path.read_bytes() for path in self._outputs()}
        run = subprocess.run(
            ["python3", "-B", str(SITE / "build_fourth_churning.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in self._outputs()})

    def test_exact_public_denominator_and_candidate_counts(self) -> None:
        self.assertEqual(len(self.collisions), 12)
        self.assertEqual(len(self.diagnoses), 54)
        self.assertEqual(
            Counter(row["diagnosis_state"] for row in self.diagnoses),
            Counter({"TYPE_COLLISION": 1, "PARTIAL_TYPE_COLLISION": 46, "NO_COLLISION": 2, "UNDERDETERMINED": 5}),
        )
        self.assertTrue(all(row["earned_effect"] == "NO_INCREMENT" for row in self.diagnoses))

    def test_seven_axes_and_nulls_are_real_outputs(self) -> None:
        self.assertEqual(
            {row["axis"] for row in self.collisions},
            {"LEVEL", "MODAL", "TEMPORAL", "REPRESENTATIONAL", "EPISTEMIC", "NORMATIVE", "BEARER"},
        )
        by_id = {row["problem_id"]: row for row in self.diagnoses}
        self.assertEqual(by_id["PQA54@0.1:SCI:BELL"]["diagnosis_state"], "NO_COLLISION")
        self.assertEqual(by_id["PQA54@0.1:ULT:EVIL"]["diagnosis_state"], "NO_COLLISION")
        for problem_id in (
            "PQA54@0.1:MIN:CONSCIOUSNESS",
            "PQA54@0.1:MET:TIME",
            "PQA54@0.1:AXI:BEAUTY",
            "PQA54@0.1:AXI:DEATH",
            "PQA54@0.1:ULT:HIDDENNESS",
        ):
            self.assertEqual(by_id[problem_id]["diagnosis_state"], "UNDERDETERMINED")

    def test_no_collision_and_underdetermined_never_invent_a_join(self) -> None:
        nulls = [row for row in self.diagnoses if row["diagnosis_state"] in {"NO_COLLISION", "UNDERDETERMINED"}]
        self.assertTrue(all(row["alleged_invalid_join"] is None for row in nulls))

    def test_split_is_explicitly_contaminated(self) -> None:
        self.assertEqual(self.corpus["held_out_integrity"], "CONTAMINATED_FOR_FOURTH_USE")
        self.assertTrue(all(row["split_integrity"] == "CONTAMINATED_FOR_FOURTH_USE" for row in self.diagnoses))

    def test_source_and_public_ids_align(self) -> None:
        source = json.loads((PACKET / "data/mystery_diagnoses.v1.json").read_text())
        self.assertEqual([row["diagnosis_id"] for row in source], [row["diagnosis_id"] for row in self.diagnoses])

    def test_schema_copies_are_byte_identical(self) -> None:
        for name in ("TypeCollision.v1.schema.json", "MysteryDiagnosis.v1.schema.json", "FourthChurningCorpus.v1.schema.json"):
            self.assertEqual(
                (PACKET / "contracts" / name).read_bytes(),
                (SITE / "questions/schemas" / name).read_bytes(),
            )

    def test_public_language_keeps_the_boundary(self) -> None:
        sentence = "Emergentism proposes that many perennial problems contain malformed joins between types. It does not claim that every mystery is a type error."
        self.assertIn(sentence, self.page)
        self.assertIn(sentence, self.atlas)
        folded = (self.page + self.atlas).lower()
        self.assertNotIn("most philosophy solved", folded)
        self.assertNotIn("all mysteries are type errors", folded)
        self.assertIn("Fifty-four diagnoses. Zero earned resolutions.", self.page)
        self.assertIn("candidate Type Atlas · [D] [I] [C]", self.page)

    def test_third_and_fourth_writers_are_disjoint(self) -> None:
        third = json.loads((ROOT / "14_THE_DISTILLATION/07_THE_THIRD_CHURNING_2026_08_23/ThirdChurningCorpus.v1.json").read_text())
        self.assertTrue(set(third["output_map"].values()).isdisjoint(self.corpus["public_output_map"].values()))

    @staticmethod
    def _outputs() -> list[Path]:
        return [
            SITE / "questions/diagnoses/index.html",
            SITE / "questions/collisions.json",
            SITE / "questions/diagnoses.json",
            SITE / "questions/fourth-churning.json",
            SITE / "questions/schemas/TypeCollision.v1.schema.json",
            SITE / "questions/schemas/MysteryDiagnosis.v1.schema.json",
            SITE / "questions/schemas/FourthChurningCorpus.v1.schema.json",
        ]


if __name__ == "__main__":
    unittest.main()
