"""Regression of two corrected assertions, not validation of the entire lens."""
import copy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def validate(manifest, lens):
    def need(condition):
        if not condition:
            raise ValueError("kernel source correction regressed")
    need("sealed, not run" not in manifest)
    for phrase in ("23 versus 23", "primary KILL fired", "only that",
                   "one model and one grader", "No successor run"):
        need(phrase in manifest)
    score = lens["structure"]["score"]
    need("Type difference alone does not force AND-class" in score["why_AND"])
    need("structural zeros" in score["why_AND"])
    need("Pareto" in score["honest_limit"] and "comparability" in score["honest_limit"])
    need("not a derivation" in score["unification"])
    need("[A] the type argument" not in lens["tenets"][2]["tier"])
    need("target capability persists" in lens["kills"][2]["dies_if"])
    for phrase in ("23–23", "primary KILL fired", "only LENS", "Single model and single grader"):
        need(phrase in lens["provenance"]["unmeasured"])


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.manifest = (ROOT / "10_KERNEL/00_WHAT_THE_MACHINE_RECEIVES.md").read_text()
        self.lens = json.loads((ROOT / "10_KERNEL/LENS.v0.json").read_text())

    def test_current(self):
        validate(self.manifest, self.lens)

    def test_status_regression(self):
        with self.assertRaises(ValueError):
            validate(self.manifest + "sealed, not run", self.lens)

    def test_qualifications(self):
        for phrase in ("only that", "one model and one grader", "primary KILL fired"):
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                validate(self.manifest.replace(phrase, ""), self.lens)

    def test_false_derivation(self):
        changed = copy.deepcopy(self.lens)
        changed["structure"]["score"]["why_AND"] = "AND-class is forced by typing"
        with self.assertRaises(ValueError):
            validate(self.manifest, changed)

    def test_repeated_inference(self):
        self.lens["tenets"][2]["tier"] = "[A] the type argument"
        with self.assertRaises(ValueError):
            validate(self.manifest, self.lens)

    def test_unmatched_self_flaw(self):
        self.lens["provenance"]["unmeasured"] = "MID-02 proves a self-correction advantage"
        with self.assertRaises(ValueError):
            validate(self.manifest, self.lens)


if __name__ == "__main__":
    unittest.main()
