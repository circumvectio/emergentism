#!/usr/bin/env python3
"""Regression contracts for the corrected Burrisphere bottom-plane topology."""

from __future__ import annotations

import json
import math
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
        self.assertIn('aria-describedby="polar-angle-help"', self.instrument)
        self.assertIn('aria-describedby="axial-rotation-help"', self.instrument)
        self.assertIn(
            'aria-label="Polar angle theta from selected south boundary to north boundary"',
            self.instrument,
        )
        self.assertIn('aria-label="Axial bearing psi around the sphere"', self.instrument)
        short_mobile = self.css.split(
            "@media (max-width: 700px) and (max-height: 700px)", 1
        )[1].split("@media (prefers-reduced-motion", 1)[0]
        self.assertNotIn(".bi-thesis { display: none; }", short_mobile)
        self.assertNotIn(".bi-boundary { display: none; }", short_mobile)
        self.assertIn("updateSliderAccessibleText", self.script)
        self.assertIn("prefers-reduced-motion: reduce", self.css)
        self.assertIn(".bi-fallback[hidden] { display: none; }", self.css)
        self.assertIn("The 3D instrument could not start.", self.instrument)
        self.assertIn("The selected overlay is also static in meaning", self.instrument)
        self.assertNotRegex(self.instrument, r'<(?:script|img)\b[^>]*\bsrc=["\']https?://')

    def test_angle_and_rotation_are_independent_controls(self) -> None:
        self.assertIn('id="polar-angle" type="range" min="0" max="180"', self.instrument)
        self.assertIn('id="axial-rotation" type="range" min="-90" max="270"', self.instrument)
        self.assertIn("let manualTheta", self.script)
        self.assertIn("let manualAzimuth", self.script)
        self.assertIn("updateGeometry(manualTheta, manualAzimuth, true)", self.script)
        self.assertIn("function updatePhase(azimuth, atPole)", self.script)
        self.assertIn("phaseIndexForAzimuth(azimuth)", self.script)
        self.assertNotIn("function updatePhase(theta)", self.script)
        self.assertIn("Theta changes phi, nu, and B but leaves axial bearing unchanged.", self.instrument)
        self.assertIn("leaves theta, phi, nu, and B unchanged.", self.instrument)

    def test_projection_uses_one_line_direction_and_collinear_clipping(self) -> None:
        self.assertIn("function intersectLineWithHorizontalPlane(source, through, planeY)", self.script)
        self.assertIn("source.clone().addScaledVector(direction, distance)", self.script)
        self.assertIn("function clipRayToRadialWindow(source, exact)", self.script)
        self.assertIn("source.clone().lerp(exact, scale)", self.script)
        self.assertIn("setLinePoints(lowerRay, [NORTH, lower.vector])", self.script)
        self.assertIn("setLinePoints(upperRay, [SOUTH, upper.vector])", self.script)
        self.assertNotIn("clipRadial", self.script)
        self.assertNotIn("[NORTH, shared, lower.vector]", self.script)
        self.assertNotIn("[SOUTH, shared, upper.vector]", self.script)
        self.assertIn("never bent", self.instrument)

    def test_sampled_dual_projection_is_reciprocal_and_collinear(self) -> None:
        radius = 1.08
        limit = 8.4 * 0.46

        def subtract(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
            return tuple(x - y for x, y in zip(a, b))

        def cross(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
            return (
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0],
            )

        def norm(vector: tuple[float, float, float]) -> float:
            return math.sqrt(sum(value * value for value in vector))

        for theta in (0.01, 0.2, 0.8, math.pi / 2, 2.3, math.pi - 0.01):
            phi = 1 / math.tan(theta / 2)
            nu = math.tan(theta / 2)
            self.assertAlmostEqual(phi * nu, 1.0, places=12)
            self.assertAlmostEqual(2 / (phi + nu), math.sin(theta), places=12)
            for azimuth in (-math.pi / 2, -0.2, 1.1, 3.7):
                point = (
                    radius * math.sin(theta) * math.cos(azimuth),
                    -radius * math.cos(theta),
                    radius * math.sin(theta) * math.sin(azimuth),
                )
                projections = (
                    ((0.0, radius, 0.0), (2 * radius * nu * math.cos(azimuth), -radius, 2 * radius * nu * math.sin(azimuth))),
                    ((0.0, -radius, 0.0), (2 * radius * phi * math.cos(azimuth), radius, 2 * radius * phi * math.sin(azimuth))),
                )
                for source, exact in projections:
                    radial = math.hypot(exact[0], exact[2])
                    scale = min(1.0, limit / radial) if radial else 1.0
                    visible = tuple(source[i] + scale * (exact[i] - source[i]) for i in range(3))
                    first = subtract(point, source)
                    second = subtract(visible, source)
                    error = norm(cross(first, second)) / (norm(first) * norm(second))
                    self.assertLess(error, 1e-12)

    def test_selected_itinerary_is_one_shot_and_manual_input_exits_it(self) -> None:
        self.assertIn("manualTheta = Math.PI * itineraryProgress", self.script)
        self.assertIn("manualAzimuth = -Math.PI / 2 + TAU * itineraryProgress", self.script)
        self.assertIn('motionState = "complete"', self.script)
        self.assertIn("polarSlider.addEventListener", self.script)
        self.assertIn("bearingSlider.addEventListener", self.script)
        self.assertIn("enterFreeMode()", self.script)
        self.assertNotIn("Math.sin((now - start)", self.script)
        self.assertIn("One-turn itinerary disabled by reduced-motion preference", self.script)


if __name__ == "__main__":
    unittest.main()
