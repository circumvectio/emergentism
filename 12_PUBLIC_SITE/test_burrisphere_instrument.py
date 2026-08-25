#!/usr/bin/env python3
"""Regression contracts for the corrected Burrisphere bottom-plane topology."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parent
ROOT = SITE.parent


class BurrisphereInstrumentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = (ROOT / "00_THE_WELTANSCHAUUNG_ONE_SITTING.md").read_text(encoding="utf-8")
        cls.g7_source = (ROOT / "05_COSMOLOGY/00_D5_THE_SEVEN_GENERATIVE_ACTIONS.md").read_text(encoding="utf-8")
        cls.parity = json.loads((SITE / "public_semantic_parity.json").read_text(encoding="utf-8"))
        cls.atlas = (SITE / "burrisphere/index.html").read_text(encoding="utf-8")
        cls.instrument = (SITE / "burrisphere/instrument/index.html").read_text(encoding="utf-8")
        cls.script = (SITE / "assets/js/burrisphere-instrument.js").read_text(encoding="utf-8")
        cls.css = (SITE / "assets/css/burrisphere-instrument.css").read_text(encoding="utf-8")

    def test_source_locates_m4_below_and_f3_on_the_vertical_axis(self) -> None:
        self.assertIn("one bottom\naction/projection plane", self.source)
        self.assertIn("not longitudinal\nsphere territories", self.source)
        self.assertIn("F3 alone occupies the world-vertical axis", self.source)
        self.assertIn("the rising sphere path itself carries no transfer", self.source)
        self.assertIn("The Titan axis carries three frames; the bottom plane carries four transfers", self.source)

    def test_d5_construction_does_not_prejudge_the_verdict(self) -> None:
        construction = self.g7_source.split("## 2. Construction", 1)[1].split("## 3.", 1)[0]
        self.assertIn("two taking forms + two giving forms", construction)
        self.assertNotIn("demon-polar", construction)
        self.assertNotIn("god-polar", construction)
        self.assertIn("## 5. Demon/god verdict layer `[I]`", self.g7_source)

    def test_projection_v2_is_explicit_and_fail_closed(self) -> None:
        d5 = next(row for row in self.parity["levels"] if row["id"] == "D5")
        projection = d5["stone"]["projection"]
        self.assertEqual(projection["schema"], "emergentism/G7Projection.v2")
        self.assertEqual(
            projection["planeAxes"],
            {
                "bearerDirection": "self-facing to other-facing",
                "powerChannel": "raised Phi5 channel to raised V4 channel",
                "planePosition": "bottom action/projection plane",
                "tier": "[I]",
            },
        )
        topology = projection["burrisphereG7"]
        self.assertEqual(topology["actionPlanePosition"], "bottom-projection-plane")
        self.assertEqual(topology["titanAxisPosition"], "world-vertical")
        self.assertFalse(topology["transfersOnSphereSurface"])
        self.assertTrue(topology["coLocatedWithLowerChart"])
        self.assertFalse(topology["identicalToLowerChart"])
        path = projection["displayPath"]
        self.assertEqual(path["schema"], "emergentism/G7DisplayPath.v2")
        self.assertEqual(path["phaseCarrier"], "bottom-action-plane-trace")
        self.assertTrue(path["bottomPlaneTraceTraversesM4"])
        self.assertFalse(path["spherePathCarriesTransfers"])

    def test_webgl_uses_planar_sectors_and_no_sphere_territories(self) -> None:
        self.assertIn("const bottomActionPlane = new THREE.Group()", self.script)
        self.assertIn("new THREE.CircleGeometry(ACTION_RADIUS", self.script)
        self.assertIn("bottomActionPlane.position.y = -R", self.script)
        self.assertIn("const sectorMeshes = []", self.script)
        self.assertIn("const phaseCursor", self.script)
        self.assertNotIn("territorySurface", self.script)
        self.assertNotIn("actionTerritories", self.script)
        self.assertNotRegex(self.script, r"thetaSteps\s*=.*territ")

    def test_titan_axis_is_visible_and_separate(self) -> None:
        self.assertIn('titanGlyph("•"', self.script)
        self.assertIn('titanGlyph("⊙"', self.script)
        self.assertIn('titanGlyph("○"', self.script)
        self.assertIn('titanGlyphs.name = "F3 Titan axis [I]"', self.script)
        self.assertIn("• Śiva; ⊙ Viṣṇu; ○ Brahmā", self.instrument)
        self.assertIn("F3 alone occupies the vertical axis", self.atlas)

    def test_static_atlas_keeps_all_m4_labels_on_the_bottom_plane(self) -> None:
        self.assertIn("M4 · BOTTOM ACTION/PROJECTION PLANE", self.atlas)
        self.assertIn("NOT SPHERE TERRITORIES", self.atlas)
        self.assertIn("SPHERE ITINERARY [I] · NO TRANSFER", self.atlas)
        self.assertIn("bottom-plane phase trace", self.atlas)
        self.assertNotIn("front of M4 path", self.atlas)
        self.assertNotIn("winding path carries four transfers", self.atlas)

    def test_homepage_uses_the_corrected_bottom_plane_topology(self) -> None:
        home = (SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("M4 · BOTTOM ACTION/PROJECTION PLANE", home)
        self.assertIn("sphere path carries no transfer", home)
        self.assertIn("bottom-plane phase trace", home)
        self.assertNotIn("front of M4 path", home)
        self.assertNotIn("winding path carries four fully typed transfers", home)

    def test_accessibility_and_failure_modes_remain_text_complete(self) -> None:
        self.assertIn('aria-label="M4 bottom action plane.', self.instrument)
        self.assertIn('aria-describedby="slider-help"', self.instrument)
        self.assertIn("updateSliderAccessibleText", self.script)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertIn(".bi-fallback[hidden] { display: none; }", self.css)
        self.assertIn("The 3D instrument could not start.", self.instrument)
        self.assertIn("The selected overlay is also static in meaning", self.instrument)
        self.assertNotRegex(self.instrument, r'<(?:script|img)\b[^>]*\bsrc=["\']https?://')


if __name__ == "__main__":
    unittest.main()
