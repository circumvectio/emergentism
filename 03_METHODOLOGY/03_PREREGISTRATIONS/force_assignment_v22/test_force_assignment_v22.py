"""Protocol tests for the v2.2 D1–D4 force-assignment harness."""

from __future__ import annotations

import sys
import unittest
from itertools import permutations
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from force_assignment import (
    F5_FORK,
    FORCES,
    FOUNDER_PRIOR_ID,
    FOUNDER_PRIOR_TUPLE,
    LEG_PHYSICS,
    PACKET_GATES,
    REGISTERS,
    bijection_assignments,
    comparison_universe,
    founder_prior,
    protocol_corpus_paths,
    rival_universe,
    score_packet,
    weak_gate_requirements,
)

# Phrase the protocol must not use as a D3/W justification.
BARRED_SLOGAN = "the quantum realm"


class ForceAssignmentV22Tests(unittest.TestCase):
    def test_all_permutations_exist(self):
        rows = bijection_assignments()
        expected = {("W7-4P-" + "".join(mapping), mapping) for mapping in permutations(FORCES)}
        got = {(row["id"], row["tuple"]) for row in rows}
        self.assertEqual(len(rows), 24)
        self.assertEqual(got, expected)
        ids = [row["id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        founder_rows = [row for row in rows if row["is_founder_prior"]]
        self.assertEqual(len(founder_rows), 1)
        self.assertEqual(founder_rows[0]["id"], FOUNDER_PRIOR_ID)
        self.assertEqual(founder_rows[0]["prior_status"], "PRIOR_ONLY")

    def test_rivals_include_nomap_m2m_electroweak_joint(self):
        rivals = rival_universe()
        kinds = {item["kind"] for item in rivals}
        ids = {item["id"] for item in rivals}
        self.assertIn("no-mapping", kinds)
        self.assertIn("many-to-many", kinds)
        self.assertIn("electroweak-joint", kinds)
        self.assertIn("R-NOMAP", ids)
        self.assertIn("R-M2M", ids)
        self.assertIn("R-EWJ", ids)
        self.assertEqual(len(comparison_universe()), 27)

    def test_founder_match_does_not_increment_score(self):
        empty = {}
        founder_empty = score_packet(FOUNDER_PRIOR_TUPLE, empty)
        rival_empty = score_packet(("E", "S", "W", "G"), empty)
        self.assertEqual(founder_empty["score"], 0)
        self.assertEqual(rival_empty["score"], 0)
        self.assertEqual(founder_empty["founder_agreement_points"], 0)
        self.assertTrue(founder_empty["founder_match"])
        self.assertFalse(rival_empty["founder_match"])

        claimed = {
            "agrees_with_founder": True,
            "founder_bonus": 10,
            "truth_bonus": 5,
            "f5_preferred": "F5-R",
        }
        founder_claimed = score_packet(dict(zip(REGISTERS, FOUNDER_PRIOR_TUPLE)), claimed)
        rival_claimed = score_packet({"D1": "G", "D2": "E", "D3": "W", "D4": "S"}, claimed)
        self.assertEqual(founder_claimed["score"], rival_claimed["score"])
        self.assertEqual(founder_claimed["score"], 0)
        self.assertEqual(founder_claimed["founder_agreement_points"], 0)
        self.assertEqual(founder_claimed["truth_bonus"], 0)

        complete = {gate: True for gate in PACKET_GATES}
        founder_complete = score_packet(FOUNDER_PRIOR_TUPLE, complete)
        other_complete = score_packet(("G", "W", "E", "S"), complete)
        self.assertEqual(founder_complete["score"], other_complete["score"])
        self.assertEqual(founder_complete["score"], len(PACKET_GATES))
        self.assertEqual(founder_complete["founder_agreement_points"], 0)
        prior = founder_prior()
        self.assertEqual(prior["status"], "PRIOR_ONLY")
        self.assertEqual(prior["agreement_score"], 0)

    def test_barred_slogan_absent(self):
        hits = []
        for path in protocol_corpus_paths():
            text = path.read_text(encoding="utf-8")
            if BARRED_SLOGAN in text.lower() or BARRED_SLOGAN in text:
                hits.append(str(path))
        self.assertEqual(hits, [], f"barred slogan present in {hits}")

    def test_d3_weak_demands_force_specific_physics(self):
        weak = weak_gate_requirements()
        required = " ".join(weak["required"]).lower()
        for token in ("chirality", "parity violation", "flavor change", "electroweak"):
            self.assertIn(token, required)
        for force, requirements in LEG_PHYSICS.items():
            self.assertTrue(requirements, force)
        self.assertIn("generic quantum state", weak["insufficient"])

    def test_f5_three_arm_fork_preserved_without_truth_bonus(self):
        arms = {arm["id"]: arm["kind"] for arm in F5_FORK["arms"]}
        self.assertEqual(set(arms), {"F5-W", "F5-N", "F5-R"})
        self.assertIn("present modeled futures", arms["F5-W"])
        self.assertIn("verification", arms["F5-N"].lower())
        self.assertIn("controller", arms["F5-N"].lower())
        self.assertIn("future-boundary", arms["F5-R"])
        self.assertEqual(F5_FORK["truth_bonus"], 0)


if __name__ == "__main__":
    unittest.main()
