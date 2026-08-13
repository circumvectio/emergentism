"""Focused type and routing gates for the Titan inversion source.

Passing these tests confirms only the declared mathematical and editorial
boundaries. It supplies no evidence for the Titan interpretation.
"""

from __future__ import annotations

import hashlib
import json
import math
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

    def test_projective_action_never_coerces_the_titan_frame(self) -> None:
        for required in (
            "ι_P([z:w]) := [w:z]",
            "ι_P(0_P)=∞_P",
            "ι_P(∞_P)=0_P",
            "NoCoercion(TitanFrame, ProjectivePoint)",
            "none of these facts defines an operation on `TitanFrame`",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("ι_P(0_T)", self.source)
        self.assertNotIn("ι_P(∞_T)", self.source)

    def test_real_and_projective_limits_are_not_conflated(self) -> None:
        for required in (
            "In `ℝ`, infinity is not an element.",
            "In the projective extension, `∞_P` is a",
            "ordinary division by zero stays undefined",
            "`ι_P(0_P)=∞_P` remains a lawful projective-map statement",
            "coupled boundary limit is not an endpoint multiplication",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("0_T=0_P", self.source)
        self.assertNotIn("∞_T=∞_P", self.source)

    def test_endpoint_product_is_explicitly_denied(self) -> None:
        for required in (
            "no global multiplication or division extends the affine field laws",
            "the coupled boundary limit is not an endpoint multiplication",
            "endpoint multiplication is not thereby defined",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("0_P·∞_P=1_N", self.source)

    def test_reciprocal_chart_and_log_conjugate_are_explicit(self) -> None:
        for required in (
            "ν := tan(θ/2)",
            "φ := cot(θ/2)",
            "φν=1",
            "s=log x",
            "reciprocal inversion becomes `s↦−s`",
        ):
            self.assertIn(required, self.source)

        for value in (0.25, 0.5, 2.0, 4.0):
            self.assertAlmostEqual(-math.log(value), math.log(1 / value))

    def test_positive_ray_and_titan_roles_keep_their_types(self) -> None:
        for required in (
            "positive reals",
            "positive reciprocal fixed point",
            "no Titan role becomes a point, set, class, number, or group element",
            "no mathematical neighbor forces the selected three-role vocabulary",
        ):
            self.assertIn(required, self.source)
        for forbidden in (
            "TitanFrame := Number",
            "TitanFrame := ProjectivePoint",
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
        self.assertIn("Compactification does not convert a Titan frame", located)
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
            7,
        )
        self.assertEqual(
            integrity["primary_cards_by_nonbook_home"]["historical_custody_only"],
            7,
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
