"""Focused type and routing gates for the Titan inversion source.

Passing these tests confirms only the declared mathematical and editorial
boundaries. It supplies no evidence for the Titan interpretation.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY"
    / "45_THE_TITAN_INVERSION_STRUCTURE.md"
)
CARD = ROOT / "00_META/claim_cards/titans_inversion.yaml"
MANIFEST = ROOT / "13_BOOKS/book-manifest.json"
EDITION = ROOT / "13_BOOKS/titans/RESEARCH_EDITION_1.md"


class TitanInversionStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.card_doc = json.loads(CARD.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.edition = EDITION.read_text(encoding="utf-8")

    def test_feature_action_is_typed_through_the_induced_map(self) -> None:
        for required in (
            "ι_* : Feature(Ĉ) → Feature(Ĉ)",
            "ι_*(Point(p))  := Point(ι(p))",
            "ι_*(Subset(A)) := Subset(ι[A])",
            "No operation acts on `TitanFrame`",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("0_P", self.source)

    def test_real_and_projective_limits_are_not_conflated(self) -> None:
        for required in (
            "The ordinary two-sided real limit",
            "`ℝP¹=ℝ∪{∞_P}` compactifies the real line",
            "`Ĉ=ℂP¹=ℂ∪{∞_P}` compactifies the complex plane",
            "both a point and the value and limit of the",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("in ℝ      ∞ is a limit", self.source)
        self.assertNotIn("not the value of an undefined limit", self.source)

    def test_ring_falsifier_names_the_missing_partial_product(self) -> None:
        self.assertIn("`0·∞_P` is undefined", self.source)
        self.assertIn("Premise (i)", self.source)
        self.assertIn("total associative ring multiplication", self.source)
        self.assertNotIn("additive absorber", self.source)
        self.assertNotIn("Premise (ii) is not a rule", self.source)

    def test_cayley_conjugate_is_explicit_and_correct(self) -> None:
        for required in (
            "C(−1):=∞_P",
            "C(∞_P):=1",
            "ι_C := C ∘ ι ∘ C⁻¹",
            "ι_C(u)=−u",
            "ι_C(0)=0",
        ):
            self.assertIn(required, self.source)

        cayley = lambda z: (z - 1) / (z + 1)
        for z in (0.25, 0.5, 2.0, 4.0, 1j, 2 + 3j):
            self.assertAlmostEqual(cayley(1 / z).real, (-cayley(z)).real)
            self.assertAlmostEqual(cayley(1 / z).imag, (-cayley(z)).imag)

    def test_positive_ray_and_class_theory_keep_their_types(self) -> None:
        for required in (
            "ordered multiplicative group `ℝ_{>0}`",
            "ordinary real points",
            "no such **set** exists",
            "SetClassFeature := EmptySetObject | SetSort | ProperClassObject",
            "they include both finite and infinite sets",
            "no theorem proves anything\nabout the Titan seat",
        ):
            self.assertIn(required, self.source)
        for forbidden in (
            "field / multiplicative line",
            "the rims become points",
            "proof that `○` is a proper class",
        ):
            self.assertNotIn(forbidden, self.source)

    def test_interpretation_card_is_pinned_to_only_the_representation(self) -> None:
        card = self.card_doc["cards"][0]
        self.assertEqual(card["card_id"], "TIT01-06")
        self.assertEqual(card["claim_type"], "interpretation_vow")
        self.assertEqual({row["tier"] for row in card["evidence"]}, {"I"})
        self.assertEqual(card["chapters"], ["typed-inversion"])

        source_bytes = SOURCE.read_bytes()
        self.assertEqual(
            self.card_doc["source"]["reviewed_source_sha256"],
            hashlib.sha256(source_bytes).hexdigest(),
        )
        lines = self.source.splitlines()
        locator = card["locator"]
        located = "\n".join(lines[locator["line_start"] - 1 : locator["line_end"]])
        self.assertIn(locator["anchor"], located)
        self.assertEqual(
            locator["fingerprint_sha256"],
            hashlib.sha256(located.encode("utf-8")).hexdigest(),
        )
        self.assertNotIn("Compactification", located)
        self.assertNotIn("Cayley", located)
        self.assertNotIn("class-theory", located)

    def test_manifest_routes_card_and_reports_exact_module_coverage(self) -> None:
        work = next(row for row in self.manifest["works"] if row["work_id"] == "BK-TITANS")
        self.assertIn("TIT01-06", work["claim_card_ids"])
        self.assertIn("typed-inversion", work["chapter_order"])

        composition = next(
            row
            for row in self.manifest["editorial_architecture"]["compositions"]
            if row["composition_id"] == "COMP-ACTIVE-02-TITANS"
        )
        module = next(
            row
            for row in composition["source_modules"]
            if row["path"].endswith("45_THE_TITAN_INVERSION_STRUCTURE.md")
        )
        self.assertEqual(module["coverage_state"], "carded")
        self.assertEqual(module["claim_card_ids"], ["TIT01-06"])

        integrity = self.manifest["editorial_architecture"]["integrity"]
        self.assertEqual(integrity["existing_claim_card_count"], 72)
        self.assertEqual(
            integrity["primary_cards_by_composition"]["COMP-ACTIVE-02-TITANS"],
            9,
        )
        self.assertEqual(integrity["total_primary_or_custody_routes"], 72)

    def test_staged_edition_retains_only_the_bounded_summary(self) -> None:
        self.assertIn("claim_cards: [TIT01-01, TIT01-02, TIT01-03, TIT01-04, TIT01-05, TIT01-06]", self.edition)
        self.assertIn("bounded interpretation", self.edition)
        self.assertIn("remain outside this staged edition until separately", self.edition)
        self.assertNotIn("Russell's class", self.edition)
        self.assertNotIn("crossed limit", self.edition)


if __name__ == "__main__":
    unittest.main()
