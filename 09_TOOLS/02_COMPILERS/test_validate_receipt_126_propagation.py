#!/usr/bin/env python3
"""Tests for the Receipt-126 propagation manifest validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "09_TOOLS/02_COMPILERS/validate_receipt_126_propagation.py"
MANIFEST_PATH = (
    ROOT
    / "03_METHODOLOGY/01_THE_DERIVATION/03_RECEIPT_126_PROPAGATION_MANIFEST.json"
)


def load_validator():
    spec = importlib.util.spec_from_file_location("receipt126_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Receipt-126 validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class Receipt126PropagationValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_canonical_manifest_closes_exact_scope(self) -> None:
        result = self.validator.validate_manifest(self.manifest)
        self.assertEqual(result["owners"], 26)
        self.assertEqual(result["mutations"], 14)
        self.assertEqual(result["propagationPaths"], 345)
        self.assertEqual(result["activeMutationHits"], 0)
        self.assertEqual(result["frozenScope"], "clean")
        self.assertEqual(result["authority"], "staged-only")

    def test_open_status_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["status"] = "open"
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_path_count_drift_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["derivedPropagation"]["pathCount"] = 344
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_mutation_omission_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["mutations"] = mutated["mutations"][:-1]
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_publication_authority_inflation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["authorityBoundary"] = "Publication is authorized."
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)


if __name__ == "__main__":
    unittest.main()
