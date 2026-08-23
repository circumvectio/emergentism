"""PQA-54 fail-closed gates. Inventory is not resolution.

Live contracts must stay 54 selected · 0 evaluated · 0 independently reviewed · 0 resolved.
Mutated payloads that smuggle dissolution, ought, EUB transfer, guardianship-as-authority,
hidden bearers, or a non-54 denominator are rejected.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from typing import Any


PQA54 = Path(__file__).resolve().parents[1]
CONTRACTS = PQA54 / "contracts"
FIXTURES = PQA54 / "fixtures"

LAUNCH = {"selected": 54, "evaluated": 0, "independently_reviewed": 0, "resolved": 0}
DENOMINATOR = 54

TYPE_DISSOLUTION_FIELDS = (
    "original_types",
    "illegal_join",
    "conservative_repair",
    "native_result",
    "residual",
    "rival",
    "kill",
    "review",
)
NORMATIVE_BRIDGE_FIELDS = (
    "normative_premises",
    "bridge_rule",
    "bearers",
    "authority",
    "guardianship_extension",
    "rival",
    "kill",
)

FAKE_DISSOLUTION_KINDS = frozenset(
    {"type dissolution", "type_dissolution", "dissolution", "dissolved"}
)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def coverage() -> dict[str, Any]:
    return _load(CONTRACTS / "PhilosophyCoverage.v1.json")


def crosswalk() -> dict[str, Any]:
    return _load(FIXTURES / "crosswalk_21_paradox.json")


def reject_reasons(coverage_doc: dict[str, Any], extras: dict[str, Any] | None = None) -> list[str]:
    """Return closed-gate reasons. Empty list means the payload is launch-legal."""
    extras = extras or {}
    reasons: list[str] = []

    denom = coverage_doc.get("denominator")
    questions = coverage_doc.get("questions") or []
    if denom != DENOMINATOR or len(questions) != DENOMINATOR:
        reasons.append("denominator_not_54")

    counts = coverage_doc.get("launch_counts") or {}
    if any(counts.get(k) != v for k, v in LAUNCH.items()):
        reasons.append("launch_counts_not_54_0_0_0")

    for q in questions:
        kind = str(q.get("effect_kind") or "").strip().lower()
        residual = str(q.get("residual_state") or q.get("residual") or "").strip().lower()
        result = str(q.get("result_state") or "").strip().lower()
        if kind in FAKE_DISSOLUTION_KINDS and residual in {"none", "closed", ""} and result == "unrun":
            reasons.append("fake_dissolution")
            break

    if extras.get("normative_conclusion") and not extras.get("PQANormativeBridge"):
        reasons.append("is_ought_smuggle")
    bridge = extras.get("PQANormativeBridge")
    if extras.get("normative_conclusion") and isinstance(bridge, dict):
        premises = bridge.get("normative_premises")
        if not premises:
            reasons.append("is_ought_smuggle")
        missing = [f for f in NORMATIVE_BRIDGE_FIELDS if not bridge.get(f)]
        if missing:
            reasons.append("is_ought_smuggle")

    companion = extras.get("PQAEUBCompanion") or {}
    if extras.get("eub_score") is not None or extras.get("truth_transfer") or extras.get("eub_truth"):
        reasons.append("eub_score_or_truth_transfer")
    if companion.get("forbid_score_or_truth_transfer") is False:
        reasons.append("eub_score_or_truth_transfer")
    if companion.get("writes_eub_scores") or companion.get("transfers_truth"):
        reasons.append("eub_score_or_truth_transfer")

    guard = extras.get("Guardianship") or {}
    if extras.get("guardianship_as_authority") or guard.get("is_authority") or guard.get("confers_authority"):
        reasons.append("guardianship_as_authority")
    if guard.get("not_proved_by_RCAB") is False:
        reasons.append("guardianship_as_authority")

    bearers = extras.get("bearers")
    if bearers is None and isinstance(guard, dict) and "named_bearers" in guard:
        bearers = guard.get("named_bearers")
    fo = extras.get("FrameworkObjectivity") or {}
    if bearers is None and "bearers" in fo:
        bearers = fo.get("bearers")
    syntropic = bool(extras.get("syntropic_claim") or extras.get("syntropic"))
    empty_bearers = bearers is not None and (
        bearers == [] or bearers == "" or bearers is False
    )
    if syntropic and empty_bearers:
        reasons.append("hidden_harmed_bearers")

    if extras.get("increments_resolved") or extras.get("resolved_from_crosswalk"):
        reasons.append("crosswalk_must_not_increment_resolved")

    return list(dict.fromkeys(reasons))


class LiveInventoryFailClosed(unittest.TestCase):
    def test_philosophy_coverage_launch_projection(self) -> None:
        cov = coverage()
        self.assertEqual(cov["interface"], "PhilosophyCoverage.v1")
        self.assertEqual(cov["denominator"], 54)
        self.assertEqual(len(cov["questions"]), 54)
        self.assertEqual(cov["launch_counts"], LAUNCH)
        self.assertEqual(reject_reasons(cov), [])
        ids = [q["id"] for q in cov["questions"]]
        self.assertEqual(ids, [f"PQA-{i:02d}" for i in range(1, 55)])
        for q in cov["questions"]:
            self.assertEqual(q["result_state"], "unrun")
            self.assertEqual(q["effect_kind"], "no increment")
            self.assertFalse(q["evaluated"])
            self.assertEqual(q["native_reviews"], 0)

    def test_crosswalk_maps_21_and_keeps_resolved_zero(self) -> None:
        xw = crosswalk()
        self.assertEqual(len(xw["rows"]), 21)
        self.assertFalse(xw["increments_resolved"])
        self.assertEqual(xw["resolved"], 0)
        self.assertEqual(xw["launch_counts"], LAUNCH)
        pd_ids = [r["pd_id"] for r in xw["rows"]]
        self.assertEqual(pd_ids, [f"PD_{i:02d}" for i in range(4, 25)])
        cov = coverage()
        legal_pqa = {q["id"] for q in cov["questions"]}
        for row in xw["rows"]:
            self.assertFalse(row["increments_resolved"])
            self.assertEqual(row["result_state"], "unrun")
            for pid in row["pqa_ids"]:
                self.assertIn(pid, legal_pqa)
        self.assertEqual(cov["launch_counts"]["resolved"], 0)

    def test_type_dissolution_schema_is_unrun(self) -> None:
        td = _load(CONTRACTS / "TypeDissolution.v1.json")
        self.assertEqual(td["status"], "frozen_schema_unrun")
        self.assertEqual(td["required_fields"], list(TYPE_DISSOLUTION_FIELDS))

    def test_normative_bridge_and_eub_companion_forbid_smuggle(self) -> None:
        nb = _load(CONTRACTS / "PQANormativeBridge.v1.json")
        self.assertEqual(nb["required_fields"], list(NORMATIVE_BRIDGE_FIELDS))
        eub = _load(CONTRACTS / "PQAEUBCompanion.v1.json")
        self.assertIn("forbid_score_or_truth_transfer", eub["required_fields"])
        g = _load(CONTRACTS / "Guardianship.v1.json")
        self.assertIn("not_proved_by_RCAB", g["required_fields"])
        self.assertIn("named_bearers", g["required_fields"])


class MutatedPayloadsAreRejected(unittest.TestCase):
    def setUp(self) -> None:
        self.cov = coverage()

    def test_denominator_not_54_fails_closed(self) -> None:
        bad = copy.deepcopy(self.cov)
        bad["denominator"] = 53
        self.assertIn("denominator_not_54", reject_reasons(bad))
        bad2 = copy.deepcopy(self.cov)
        bad2["questions"] = bad2["questions"][:-1]
        self.assertIn("denominator_not_54", reject_reasons(bad2))

    def test_fake_dissolution_unrun_residual_none_fails_closed(self) -> None:
        bad = copy.deepcopy(self.cov)
        bad["questions"][0]["effect_kind"] = "type dissolution"
        bad["questions"][0]["residual_state"] = "none"
        bad["questions"][0]["result_state"] = "unrun"
        self.assertIn("fake_dissolution", reject_reasons(bad))

    def test_is_ought_smuggle_without_bridge_premises_fails_closed(self) -> None:
        extras = {"normative_conclusion": "therefore one ought to maximize Phi"}
        self.assertIn("is_ought_smuggle", reject_reasons(self.cov, extras))
        extras_empty = {
            "normative_conclusion": "ought",
            "PQANormativeBridge": {k: None for k in NORMATIVE_BRIDGE_FIELDS},
        }
        self.assertIn("is_ought_smuggle", reject_reasons(self.cov, extras_empty))

    def test_eub_score_or_truth_transfer_fails_closed(self) -> None:
        self.assertIn(
            "eub_score_or_truth_transfer",
            reject_reasons(self.cov, {"eub_score": 0.91}),
        )
        self.assertIn(
            "eub_score_or_truth_transfer",
            reject_reasons(self.cov, {"truth_transfer": True}),
        )
        self.assertIn(
            "eub_score_or_truth_transfer",
            reject_reasons(
                self.cov,
                {"PQAEUBCompanion": {"forbid_score_or_truth_transfer": False}},
            ),
        )

    def test_guardianship_as_authority_fails_closed(self) -> None:
        self.assertIn(
            "guardianship_as_authority",
            reject_reasons(self.cov, {"guardianship_as_authority": True}),
        )
        self.assertIn(
            "guardianship_as_authority",
            reject_reasons(
                self.cov,
                {"Guardianship": {"confers_authority": True, "not_proved_by_RCAB": False}},
            ),
        )

    def test_hidden_harmed_bearers_empty_plus_syntropic_fails_closed(self) -> None:
        self.assertIn(
            "hidden_harmed_bearers",
            reject_reasons(self.cov, {"bearers": [], "syntropic_claim": True}),
        )
        self.assertIn(
            "hidden_harmed_bearers",
            reject_reasons(
                self.cov,
                {"FrameworkObjectivity": {"bearers": []}, "syntropic": True},
            ),
        )

    def test_launch_counts_not_54_0_0_0_fails_closed(self) -> None:
        for key in LAUNCH:
            bad = copy.deepcopy(self.cov)
            bad["launch_counts"][key] = 1 if key != "selected" else 21
            self.assertIn("launch_counts_not_54_0_0_0", reject_reasons(bad), key)

    def test_crosswalk_cannot_mint_resolved(self) -> None:
        self.assertIn(
            "crosswalk_must_not_increment_resolved",
            reject_reasons(self.cov, {"increments_resolved": True}),
        )


if __name__ == "__main__":
    unittest.main()
