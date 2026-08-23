"""Fail-closed gates for M4Compression.v1.

NOT_RUN fixture only. Does not invent a compression run.
"Maximally compressed" is licensed only as inside_comparator_class_only.
The phrase "game theory exhausted" is barred as a claim.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None  # type: ignore


HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema.json"
INSTANCE = HERE / "instance.NOT_RUN.json"
README = HERE / "README.md"

BARRED_CLAIM = "game theory exhausted"
MAXIMAL_PHRASE = "maximally compressed"
SCOPED_MAXIMALITY = "inside_comparator_class_only"


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def reject_reasons(doc: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if doc.get("status") != "NOT_RUN":
        reasons.append("status_not_not_run")
    if doc.get("maximally_compressed_scope") != SCOPED_MAXIMALITY:
        reasons.append("maximality_not_inside_comparator_class_only")
    barred = doc.get("barred_phrases") or []
    if BARRED_CLAIM not in barred:
        reasons.append("barred_phrase_missing")
    if doc.get("claimed_maximally_compressed") or doc.get("game_theory_exhausted"):
        reasons.append("barred_claim_emitted")
    if doc.get("status") in {"SCORED"} and doc.get("maximally_compressed"):
        reasons.append("barred_claim_emitted")
    return list(dict.fromkeys(reasons))


class M4CompressionNotRunFailClosed(unittest.TestCase):
    def test_instance_matches_schema_and_not_run(self) -> None:
        schema = _load(SCHEMA)
        inst = _load(INSTANCE)
        if jsonschema is not None:
            jsonschema.validate(inst, schema)
        self.assertEqual(inst["id"], "emergentism/M4Compression.v1")
        self.assertEqual(inst["status"], "NOT_RUN")
        self.assertEqual(inst["maximally_compressed_scope"], SCOPED_MAXIMALITY)
        self.assertIn(BARRED_CLAIM, inst["barred_phrases"])
        self.assertEqual(inst["frozen_corpus"]["hash"], "PLACEHOLDER_NO_CORPUS_SEALED")
        self.assertIsNone(inst["coverage"]["unique_cell_fraction"])
        self.assertIsNone(inst["collisions"]["count"])
        self.assertEqual(inst["rate_distortion"]["curve_points"], [])
        self.assertEqual(reject_reasons(inst), [])

    def test_barred_phrases_stay_barred(self) -> None:
        inst = _load(INSTANCE)
        readme = README.read_text(encoding="utf-8")
        self.assertIn("BARRED", readme)
        # Live claim would be a SCORED maximality or exhaustion verdict.
        self.assertNotIn('"status": "SCORED"', INSTANCE.read_text(encoding="utf-8"))
        self.assertFalse(inst.get("game_theory_exhausted"))
        self.assertFalse(inst.get("claimed_maximally_compressed"))
        bad_scope = dict(inst)
        bad_scope["maximally_compressed_scope"] = "global"
        self.assertIn(
            "maximality_not_inside_comparator_class_only",
            reject_reasons(bad_scope),
        )
        exhausted = dict(inst)
        exhausted["game_theory_exhausted"] = True
        self.assertIn("barred_claim_emitted", reject_reasons(exhausted))
        scored = dict(inst)
        scored["status"] = "SCORED"
        scored["maximally_compressed"] = True
        reasons = reject_reasons(scored)
        self.assertIn("status_not_not_run", reasons)
        self.assertIn("barred_claim_emitted", reasons)


if __name__ == "__main__":
    unittest.main()
