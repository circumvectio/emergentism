#!/usr/bin/env python3
"""Regression tests for one-brand public document metadata."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


SITE = Path(__file__).resolve().parent
sys.path.insert(0, str(SITE))

import apply_frozen_library_boundary as frozen
import generate_public_library as library


class PublicTitleNormalizationTests(unittest.TestCase):
    def test_future_generator_emits_one_current_brand(self) -> None:
        self.assertEqual(
            library.public_document_title("Method — Emergentism"),
            "Method — Emergentism",
        )
        self.assertEqual(
            library.public_document_title("Rosetta D-Series — Magnum Opus"),
            "Rosetta D-Series — Emergentism",
        )
        self.assertEqual(
            library.public_document_title("Applied Emergentism"),
            "Applied Emergentism — Emergentism",
        )

    def test_frozen_overlay_changes_metadata_not_visible_prose(self) -> None:
        source = (
            "<title>Method — Emergentism — Emergentism</title>"
            '<meta property="og:title" content="Method — Emergentism — Emergentism">'
            "<h1>Method — Emergentism — Emergentism</h1>"
        )
        expected = (
            "<title>Method — Emergentism</title>"
            '<meta property="og:title" content="Method — Emergentism">'
            "<h1>Method — Emergentism — Emergentism</h1>"
        )
        self.assertEqual(frozen.normalize_brand_metadata(source), expected)

    def test_overlay_does_not_append_a_missing_brand(self) -> None:
        source = "<title>The Dasein Test</title>"
        self.assertEqual(frozen.normalize_brand_metadata(source), source)


if __name__ == "__main__":
    unittest.main()
