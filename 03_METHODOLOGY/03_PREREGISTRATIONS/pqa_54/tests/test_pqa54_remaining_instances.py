"""UNRUN sibling instances load; increment and smuggle fail closed."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from test_pqa54_fail_closed import (
    LAUNCH,
    TYPE_DISSOLUTION_FIELDS,
    NORMATIVE_BRIDGE_FIELDS,
    coverage,
    reject_reasons,
)


PQA54 = Path(__file__).resolve().parents[1]
CONTRACTS = PQA54 / "contracts"

REMAINING = (
    "TypeDissolution.v1",
    "PQANormativeBridge.v1",
    "Guardianship.v1",
    "CoAgency.v1",
    "FrameworkObjectivity.v1",
    "PQANativeReview.v1",
    "PQAQuestionTrial.v1",
    "PQAScoreReceipt.v1",
)

SCORE_OR_RESULT_KEYS = (
    "native_result",
    "result_state",
    "score",
    "score_vector",
    "eub_score",
    "primary_scalar",
    "measure",
    "reviewer_a",
    "reviewer_b",
    "domain_qualified",
    "independent",
    "revision_or_transfer",
    "normative_conclusion",
    "authority",
    "original_types",
    "illegal_join",
    "conservative_repair",
    "rival",
)


def _load(name: str) -> dict:
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


def _instance(interface: str) -> dict:
    return _load(f"{interface}.instance.json")


def _unrun_value(value) -> bool:
    return value in (None, "unrun")


class RemainingUnrunInstances(unittest.TestCase):
    def test_schema_stubs_stay_frozen_field_names_only(self) -> None:
        for interface in REMAINING:
            stub = _load(f"{interface}.json")
            self.assertEqual(stub["status"], "frozen_schema_unrun", interface)
            self.assertEqual(stub["interface"], interface)
            self.assertNotIn("launch_counts", stub)
            self.assertNotIn("score_vector", stub)
            for field in stub["required_fields"]:
                self.assertNotIn(field, stub, f"{interface} stub must not hold {field}")

    def test_instances_have_required_fields_and_unrun_results(self) -> None:
        for interface in REMAINING:
            stub = _load(f"{interface}.json")
            inst = _instance(interface)
            self.assertEqual(inst["interface"], interface)
            self.assertTrue(str(inst["status"]).startswith("UNRUN"))
            self.assertTrue(inst["schema_stub_untouched"])
            self.assertEqual(inst["schema_stub"], f"{interface}.json")
            self.assertEqual(inst["launch_counts"], LAUNCH)
            self.assertFalse(inst["increments_resolved"])
            self.assertEqual(inst["result_state"], "unrun")
            self.assertFalse(inst["evaluated"])
            self.assertTrue(inst["forbid_score_or_truth_transfer"])
            self.assertFalse(inst["writes_eub_scores"])
            self.assertFalse(inst["transfers_truth"])
            for field in stub["required_fields"]:
                self.assertIn(field, inst, f"{interface} missing {field}")
            for key in SCORE_OR_RESULT_KEYS:
                if key in inst:
                    self.assertTrue(_unrun_value(inst[key]), f"{interface}.{key}={inst[key]!r}")

    def test_type_dissolution_is_not_a_fake_receipt(self) -> None:
        inst = _instance("TypeDissolution.v1")
        for field in TYPE_DISSOLUTION_FIELDS:
            self.assertIn(field, inst)
        self.assertEqual(inst["native_result"], "unrun")
        self.assertEqual(inst["residual"], "open")
        self.assertEqual(inst["effect_kind"], "no increment")
        self.assertNotEqual(str(inst["residual"]).lower(), "none")

    def test_guardianship_is_not_authority(self) -> None:
        inst = _instance("Guardianship.v1")
        self.assertTrue(inst["not_proved_by_RCAB"])
        self.assertFalse(inst["is_authority"])
        self.assertFalse(inst["confers_authority"])
        self.assertTrue(inst["named_bearers"])

    def test_hidden_bearers_are_not_empty_slots(self) -> None:
        fo = _instance("FrameworkObjectivity.v1")
        nb = _instance("PQANormativeBridge.v1")
        g = _instance("Guardianship.v1")
        self.assertTrue(fo["bearers"])
        self.assertTrue(nb["bearers"])
        self.assertTrue(g["named_bearers"])
        self.assertFalse(fo.get("syntropic"))
        self.assertFalse(nb["guardianship_extension"])
        self.assertIsNone(nb["normative_premises"])
        self.assertIsNone(nb["normative_conclusion"])

    def test_native_review_and_score_receipt_unrun(self) -> None:
        nr = _instance("PQANativeReview.v1")
        sr = _instance("PQAScoreReceipt.v1")
        qt = _instance("PQAQuestionTrial.v1")
        self.assertEqual(nr["independently_reviewed"], 0)
        self.assertIsNone(nr["reviewer_a"])
        self.assertIsNone(nr["reviewer_b"])
        self.assertIsNone(sr["score_vector"])
        self.assertTrue(sr["no_primary_scalar"])
        self.assertIsNone(qt["revision_or_transfer"])
        ca = _instance("CoAgency.v1")
        self.assertTrue(ca["forbids_conflation_of_personhood_consent_authority_protection"])

    def test_live_instances_are_launch_legal_extras(self) -> None:
        cov = coverage()
        extras = {
            "PQANormativeBridge": _instance("PQANormativeBridge.v1"),
            "PQAEUBCompanion": _load("PQAEUBCompanion.v1.instance.json"),
            "Guardianship": _instance("Guardianship.v1"),
            "FrameworkObjectivity": _instance("FrameworkObjectivity.v1"),
            "bearers": _instance("FrameworkObjectivity.v1")["bearers"],
        }
        self.assertEqual(reject_reasons(cov, extras), [])


class RemainingInstanceSmuggleFailClosed(unittest.TestCase):
    def setUp(self) -> None:
        self.cov = coverage()

    def test_increment_resolved_on_any_instance_fails_closed(self) -> None:
        for interface in REMAINING:
            bad = copy.deepcopy(_instance(interface))
            bad["increments_resolved"] = True
            bad["launch_counts"] = {**LAUNCH, "resolved": 1}
            reasons = reject_reasons(self.cov, {"increments_resolved": True})
            self.assertIn("crosswalk_must_not_increment_resolved", reasons, interface)
            self.assertNotEqual(bad["launch_counts"], LAUNCH)

    def test_eub_smuggle_via_score_receipt_fails_closed(self) -> None:
        bad = copy.deepcopy(_instance("PQAScoreReceipt.v1"))
        bad["eub_score"] = 0.91
        bad["transfers_truth"] = True
        self.assertIn(
            "eub_score_or_truth_transfer",
            reject_reasons(self.cov, {"eub_score": bad["eub_score"], "truth_transfer": True}),
        )
        qt = copy.deepcopy(_instance("PQAQuestionTrial.v1"))
        qt["revision_or_transfer"] = "eub_truth"
        self.assertIn(
            "eub_score_or_truth_transfer",
            reject_reasons(self.cov, {"truth_transfer": True}),
        )

    def test_guardianship_as_authority_smuggle_fails_closed(self) -> None:
        bad = copy.deepcopy(_instance("Guardianship.v1"))
        bad["is_authority"] = True
        bad["confers_authority"] = True
        bad["not_proved_by_RCAB"] = False
        self.assertIn("guardianship_as_authority", reject_reasons(self.cov, {"Guardianship": bad}))

    def test_hidden_bearers_plus_syntropic_fails_closed(self) -> None:
        fo = copy.deepcopy(_instance("FrameworkObjectivity.v1"))
        fo["bearers"] = []
        fo["syntropic"] = True
        self.assertIn(
            "hidden_harmed_bearers",
            reject_reasons(self.cov, {"FrameworkObjectivity": fo, "syntropic": True}),
        )
        g = copy.deepcopy(_instance("Guardianship.v1"))
        g["named_bearers"] = []
        self.assertIn(
            "hidden_harmed_bearers",
            reject_reasons(self.cov, {"Guardianship": g, "syntropic_claim": True}),
        )

    def test_is_ought_smuggle_without_premises_fails_closed(self) -> None:
        nb = copy.deepcopy(_instance("PQANormativeBridge.v1"))
        extras = {"normative_conclusion": "therefore one ought", "PQANormativeBridge": nb}
        self.assertIn("is_ought_smuggle", reject_reasons(self.cov, extras))

    def test_fake_dissolution_on_coverage_fails_closed(self) -> None:
        bad = copy.deepcopy(self.cov)
        bad["questions"][0]["effect_kind"] = "type dissolution"
        bad["questions"][0]["residual_state"] = "none"
        bad["questions"][0]["result_state"] = "unrun"
        self.assertIn("fake_dissolution", reject_reasons(bad))


if __name__ == "__main__":
    unittest.main()
