#!/usr/bin/env python3
"""Source-owner and authority tests for the Emergentism front door."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class VmoskFinitySourceTests(unittest.TestCase):
    def test_control_file_is_a_nonsemantic_projection(self):
        text = (ROOT / ("V" + "MOSK_A.md")).read_text(encoding="utf-8")
        for phrase in (
            'semantic_authority: "none"',
            "creates no theorem, ontology, axiology",
            "or eighth kernel owner",
        ):
            self.assertIn(phrase, text)
        for external_authority in (("PRI" + "SM"), ("private D" + "AV"), "sovereign disposes"):
            self.assertNotIn(external_authority, text)

        live = (ROOT / ("V" + "MOSK_A_v2_2026_07_31.md")).read_text(
            encoding="utf-8"
        )
        for phrase in (
            "worldview-as-parent front door",
            "Finity Card owned",
            "mostly-unbuilt",
            "Followers, applause, and AI agreement remain non-KPIs.",
        ):
            self.assertIn(phrase, live)

    def test_finity_card_has_an_active_source_and_formal_boundary(self):
        text = (ROOT / "01_TELEOLOGY" / "04_THE_LIVED_COMPASS.md").read_text(encoding="utf-8")
        for phrase in (
            "## 3B. The Finity Card — compressed decision practice",
            "smallest authorized real step",
            "Who bears cost or risk?",
            "residue remains?",
            "neither defines the formal Finity research programme",
            "decision journal, OODA/PDCA loop, premortem, or simpler checklist",
            "not a promise that every consequential move can be undone",
            "reversible where possible",
        ):
            self.assertIn(phrase, text)

    def test_public_practice_builds_a_local_two_face_receipt(self):
        text = (ROOT / "12_PUBLIC_SITE" / "practice" / "index.html").read_text(encoding="utf-8")
        for phrase in (
            'id="receipt-builder"',
            "Face 1 · commitment",
            "Face 2 · observed outcome",
            "Local only · no account · no wallet · no transmission · no execution · no recommendation",
            "This receipt is not authorization.",
            "The strongest rival is a component-matched ordinary worksheet.",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn("fetch(", text)
        self.assertNotIn("ours alone", text)

    def test_homepage_keeps_one_receipt_loop_and_no_unearned_efficacy(self):
        text = (ROOT / "12_PUBLIC_SITE" / "index.html").read_text(encoding="utf-8")
        self.assertEqual(
            text.count('aria-label="Seven movements of the Soul Loop"'), 1
        )
        self.assertNotIn('class="section method"', text)
        self.assertIn("comparative benefit untested", text)
        self.assertNotIn("Emergentism helps", text)
        self.assertNotIn("world-issued receipt", text)

    def test_public_record_reserved_id_and_label_match(self):
        text = (ROOT / "12_PUBLIC_SITE" / "record" / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="027"', text)
        self.assertIn('href="#027">№027</a>', text)
        self.assertNotIn("slot №017 is already open", text)

    def test_finity_cards_route_practice_and_comparative_adequacy_separately(self):
        document = json.loads((ROOT / "00_META" / "claim_cards" / "finity_practice.yaml").read_text(encoding="utf-8"))
        self.assertEqual(document["work_id"], "BK-FINITY-PRACTICE")
        cards = {card["card_id"]: card for card in document["cards"]}
        self.assertEqual(set(cards), {"FIN01-01", "FIN01-02"})
        self.assertEqual(cards["FIN01-01"]["claim_type"], "stipulation")
        self.assertEqual(cards["FIN01-01"]["evidence"], [{"tier": "S", "scope": "chosen worksheet and source-owned practice definition"}])
        self.assertEqual(cards["FIN01-02"]["claim_type"], "conjecture")
        self.assertEqual(cards["FIN01-02"]["evidence"][0]["tier"], "C")
        self.assertIn("simpler checklist", cards["FIN01-02"]["strongest_rival"])

    def test_projection_catalog_and_settled_boundary_name_the_practice(self):
        manifest = json.loads((ROOT / "13_BOOKS" / "book-manifest.json").read_text(encoding="utf-8"))
        work = next(item for item in manifest["works"] if item["work_id"] == "BK-FINITY-PRACTICE")
        self.assertEqual(work["claim_card_ids"], ["FIN01-01", "FIN01-02"])
        self.assertEqual(work["public_route"], "../12_PUBLIC_SITE/practice/index.html")
        registry = (ROOT / "00_META" / "00_SETTLED_CANON_REGISTRY.md").read_text(encoding="utf-8")
        self.assertIn("`KSC-27` | Practical Finity / formal Finity separation", registry)
        self.assertIn("simpler rival cannot be allowed to win", registry)


if __name__ == "__main__":
    unittest.main()
