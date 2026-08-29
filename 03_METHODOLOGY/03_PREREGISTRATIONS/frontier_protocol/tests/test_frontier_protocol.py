from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import sys

PACKAGE = Path(__file__).resolve().parents[1]
if str(PACKAGE) not in sys.path:
    sys.path.insert(0, str(PACKAGE))

from frontier_core import (  # noqa: E402
    LIVE_SERVICE_NULL,
    ROOT,
    ROUTING_REL,
    W7_REL,
    build_graph,
    canonical_bytes,
    output_payloads,
    validate_graph,
    validate_world_receipt,
)


class FrontierProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = build_graph(ROOT)

    def test_launch_graph_is_twelve_and_zero_elsewhere(self) -> None:
        self.assertEqual(len(self.graph["gaps"]), 12)
        self.assertEqual(
            self.graph["counts"],
            {
                "gaps": 12,
                "candidates": 0,
                "frozen_tests": 0,
                "world_receipts": 0,
                "revisions": 0,
            },
        )
        self.assertFalse(self.graph["completeness_claim"])
        self.assertEqual(self.graph["world_contact_accepted"], 0)
        self.assertEqual(self.graph["live_service"], LIVE_SERVICE_NULL)

    def test_state_axes_are_not_collapsed(self) -> None:
        rows = {row["source_gap_id"]: row for row in self.graph["gaps"]}
        self.assertEqual(rows["GP-03"]["execution_requirement"], "scale-contract-required")
        self.assertEqual(
            rows["GP-03"]["public_routing_state"]["execution"],
            "discriminator-or-nonidentifiability-required",
        )
        self.assertEqual(
            rows["GP-10"]["execution_requirement"],
            "24-permutation-preregistration-draft",
        )
        self.assertEqual(
            rows["GP-10"]["public_routing_state"]["execution"],
            "native-row-maps-missing",
        )

    def test_every_gap_has_rival_discriminator_kill_survivor_and_sources(self) -> None:
        for row in self.graph["gaps"]:
            self.assertTrue(row["no_placement_rival"].strip())
            self.assertTrue(row["held_out_incremental_prediction"].strip())
            self.assertTrue(row["kill_criterion"].strip())
            self.assertTrue(row["survivor"].strip())
            self.assertEqual(len(row["source_refs"]), 2)
            self.assertEqual(row["candidate_ids"], [])
            self.assertEqual(row["receipt_ids"], [])

    def test_deterministic_outputs(self) -> None:
        first = output_payloads(ROOT)
        second = output_payloads(ROOT)
        self.assertEqual(first, second)
        self.assertEqual(canonical_bytes(self.graph), first[next(path for path in first if path.name == "catalog.json")])

    def test_source_hash_drift_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in (W7_REL, ROUTING_REL):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, target)
            graph = build_graph(root)
            route = root / ROUTING_REL
            route.write_bytes(route.read_bytes() + b" ")
            errors = validate_graph(graph, root=root)
            self.assertTrue(any("source hash drift" in error for error in errors))

    def test_unknown_top_level_field_fails(self) -> None:
        bad = copy.deepcopy(self.graph)
        bad["truth"] = "promoted"
        self.assertIn("FrontierGraph.v1 field set drift", validate_graph(bad, root=ROOT))

    def test_launch_result_inflation_fails(self) -> None:
        bad = copy.deepcopy(self.graph)
        bad["counts"]["world_receipts"] = 1
        bad["world_contact_accepted"] = 1
        errors = validate_graph(bad, root=ROOT)
        self.assertTrue(any("launch counts" in error for error in errors))
        self.assertTrue(any("world contact" in error for error in errors))

    def test_test_actor_cannot_self_certify_world_receipt(self) -> None:
        invalid = {
            "schema_id": "FrontierWorldReceiptRef.v1",
            "custodian": "same actor",
            "test_actor": "same actor",
            "custodian_independent_of_test_actor": False,
            "adjudicates_claim": True,
        }
        errors = validate_world_receipt(invalid)
        self.assertEqual(len(errors), 3)

    def test_schema_has_five_lifecycle_defs_and_closed_root(self) -> None:
        schema = json.loads((PACKAGE / "FrontierGraph.v1.schema.json").read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        for name in (
            "FrontierGap",
            "FrontierCandidate",
            "FrontierFrozenTest",
            "FrontierWorldReceiptRef",
            "FrontierRevision",
        ):
            self.assertIn(name, schema["$defs"])

    def test_public_html_is_no_js_meaningful_and_has_exit(self) -> None:
        outputs = output_payloads(ROOT)
        html_path = next(path for path in outputs if path.name == "index.html" and path.parent.name == "frontier")
        text = outputs[html_path].decode("utf-8")
        self.assertEqual(text.count('class="fr-socket"'), 12)
        self.assertIn("Every intelligence", text)
        self.assertIn("No model is connected", text)
        self.assertIn('href="/exit/"', text)
        self.assertNotIn("requestAnimationFrame", text)
        self.assertNotIn("WebSocket", text)


if __name__ == "__main__":
    unittest.main()
