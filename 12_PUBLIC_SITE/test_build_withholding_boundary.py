#!/usr/bin/env python3
"""Regression tests for public-withholding builder ownership boundaries."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent
FROZEN_HEADER = [{"key": "X-Robots-Tag", "value": "noindex, follow"}]


def load_builder():
    spec = importlib.util.spec_from_file_location("withholding_builder_test", ROOT / "build_withholding_boundary.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WithholdingBoundaryBuilderTests(unittest.TestCase):
    def setUp(self):
        self.builder = load_builder()

    def test_policy_scan_excludes_vercel_runtime_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            source = site / "retired" / "index.html"
            runtime = site / ".vercel" / "output" / "static" / "retired" / "index.html"
            source.parent.mkdir(parents=True)
            runtime.parent.mkdir(parents=True)
            source.write_text("D6 = D0", encoding="utf-8")
            runtime.write_text("D6 = D0", encoding="utf-8")

            self.builder.SITE = site
            self.builder.FORCED_ARTIFACTS = {}
            matches = self.builder._policy_matches(set())

            self.assertEqual(set(matches), {"retired/index.html"})

    def test_omitted_legacy_list_preserves_existing_legacy_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            parity = site / "public_semantic_parity.json"
            vercel = site / "vercel.json"
            parity.write_text(json.dumps({"frozenLibraryRoots": ["papers"]}), encoding="utf-8")
            vercel.write_text(
                json.dumps(
                    {
                        "headers": [
                            {"source": "/papers/(.*)", "headers": FROZEN_HEADER},
                            {"source": "/legacy/(.*)", "headers": FROZEN_HEADER},
                        ],
                        "redirects": [],
                    }
                ),
                encoding="utf-8",
            )

            self.builder.PARITY = parity
            self.builder.VERCEL = vercel
            generated = self.builder._build_vercel([])

            sources = [row["source"] for row in generated["headers"]]
            self.assertEqual(sources.count("/papers/(.*)"), 1)
            self.assertIn("/legacy/(.*)", sources)

    def test_check_mode_accepts_schema_v2_without_legacy_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            registry = site / "withheld-routes.json"
            parity = site / "public_semantic_parity.json"
            reading = site / "reading-manifest.json"
            ignored = site / ".vercelignore"
            vercel = site / "vercel.json"
            registry.write_text(json.dumps({"artifacts": []}), encoding="utf-8")
            parity.write_text(
                json.dumps({"currentSurfaces": [], "currentInfrastructureSurfaces": [], "frozenLibraryRoots": []}),
                encoding="utf-8",
            )
            reading.write_text(json.dumps({"documents": []}), encoding="utf-8")
            ignored.write_text(
                "prefix\n# BEGIN GENERATED EXACT WITHHOLDING\n# END GENERATED EXACT WITHHOLDING\n",
                encoding="utf-8",
            )
            vercel.write_text(
                json.dumps({"headers": [{"source": "/legacy/(.*)", "headers": FROZEN_HEADER}], "redirects": []}),
                encoding="utf-8",
            )

            self.builder.SITE = site
            self.builder.REGISTRY = registry
            self.builder.PARITY = parity
            self.builder.READING = reading
            self.builder.VERCEL_IGNORE = ignored
            self.builder.VERCEL = vercel
            self.builder.FORCED_ARTIFACTS = {}

            desired_registry = self.builder._build_registry()
            registry.write_text(json.dumps(desired_registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            ignored.write_text(self.builder._build_ignore([]), encoding="utf-8")
            vercel.write_text(
                json.dumps(self.builder._build_vercel([]), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            with patch.object(sys, "argv", ["build_withholding_boundary.py", "--check"]):
                self.assertEqual(self.builder.main(), 0)

    def test_explicit_legacy_list_requires_clean_artifacts(self):
        with self.assertRaisesRegex(ValueError, "list of non-empty artifacts"):
            self.builder._frozen_legacy_surfaces({"frozenLegacySurfaces": ["ok/index.html", ""]})
        with self.assertRaisesRegex(ValueError, "must not contain duplicates"):
            self.builder._frozen_legacy_surfaces({"frozenLegacySurfaces": ["ok/index.html", "ok/index.html"]})

    def test_current_dasein_surface_fails_closed_on_retired_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            page = site / "dasein" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("<main>D6 = D0</main>", encoding="utf-8")
            self.builder.SITE = site
            self.builder.FORCED_ARTIFACTS = {}
            with self.assertRaisesRegex(
                ValueError,
                "current surface matches retired withholding policy.*dasein/index.html",
            ):
                self.builder._policy_matches({"dasein/index.html"})

    def test_clean_current_dasein_is_removed_from_policy_and_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            page = site / "dasein" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("<main>D6 is nonclosure, not D0.</main>", encoding="utf-8")
            registry = site / "withheld-routes.json"
            parity = site / "public_semantic_parity.json"
            reading = site / "reading-manifest.json"
            ignored = site / ".vercelignore"
            vercel = site / "vercel.json"
            registry.write_text(
                json.dumps(
                    {
                        "artifacts": [{
                            "artifact": "dasein/index.html",
                            "reason": "matches public semantic prohibition: literal D6 identity.",
                            "policyRuleIds": ["semantic-literal-d6-identity"],
                            "publicRoutes": ["/dasein", "/dasein/", "/dasein/index.html"],
                        }]
                    }
                ),
                encoding="utf-8",
            )
            parity.write_text(
                json.dumps(
                    {
                        "currentSurfaces": ["dasein/index.html"],
                        "currentInfrastructureSurfaces": [],
                        "infrastructureRoutes": {"routes": []},
                        "declaredProvisional": {"routes": []},
                        "frozenLibraryRoots": [],
                        "frozenLegacySurfaces": [],
                    }
                ),
                encoding="utf-8",
            )
            reading.write_text(json.dumps({"documents": []}), encoding="utf-8")
            ignored.write_text(
                "prefix\n# BEGIN GENERATED EXACT WITHHOLDING\ndasein/index.html\n# END GENERATED EXACT WITHHOLDING\n",
                encoding="utf-8",
            )
            vercel.write_text(
                json.dumps(
                    {
                        "redirects": [{
                            "source": "/dasein/",
                            "destination": "/historical-boundary/",
                            "permanent": False,
                        }],
                        "headers": [{
                            "source": "/dasein(.*)",
                            "headers": [{
                                "key": "X-Robots-Tag",
                                "value": "noindex, noarchive, nosnippet, nofollow",
                            }],
                        }],
                    }
                ),
                encoding="utf-8",
            )
            self.builder.SITE = site
            self.builder.REGISTRY = registry
            self.builder.PARITY = parity
            self.builder.READING = reading
            self.builder.VERCEL_IGNORE = ignored
            self.builder.VERCEL = vercel
            self.builder.FORCED_ARTIFACTS = {}

            desired = self.builder._build_registry()
            self.assertEqual(desired["artifacts"], [])
            self.assertNotIn("dasein/index.html", self.builder._build_ignore([]))
            delivery = self.builder._build_vercel([])
            self.assertFalse(any("dasein" in row.get("source", "") for row in delivery["redirects"]))
            self.assertFalse(any("dasein" in row.get("source", "") for row in delivery["headers"]))

    def test_curated_reason_survives_policy_rebuild_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            page = site / "legacy" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text("<main>D6 = D0</main>", encoding="utf-8")
            registry = site / "withheld-routes.json"
            parity = site / "public_semantic_parity.json"
            reading = site / "reading-manifest.json"
            registry.write_text(
                json.dumps(
                    {
                        "artifacts": [{
                            "artifact": "legacy/index.html",
                            "reason": "Curated historical custody.",
                            "curatedReason": "Curated historical custody.",
                            "publicRoutes": ["/legacy", "/legacy/", "/legacy/index.html"],
                        }]
                    }
                ),
                encoding="utf-8",
            )
            parity.write_text(
                json.dumps(
                    {
                        "currentSurfaces": [],
                        "currentInfrastructureSurfaces": [],
                        "infrastructureRoutes": {"routes": []},
                        "declaredProvisional": {"routes": []},
                    }
                ),
                encoding="utf-8",
            )
            reading.write_text(json.dumps({"documents": []}), encoding="utf-8")
            self.builder.SITE = site
            self.builder.REGISTRY = registry
            self.builder.PARITY = parity
            self.builder.READING = reading
            self.builder.FORCED_ARTIFACTS = {}

            first = self.builder._build_registry()
            registry.write_text(json.dumps(first), encoding="utf-8")
            second = self.builder._build_registry()
            self.assertEqual(first, second)
            row = first["artifacts"][0]
            self.assertEqual(row["curatedReason"], "Curated historical custody.")
            self.assertIn("retired-literal-d6-identity", row["policyRuleIds"])


if __name__ == "__main__":
    unittest.main()
