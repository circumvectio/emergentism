#!/usr/bin/env python3
"""Adversarial tests for the bounded Receipt-126 propagation validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
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
    module_name = "_test_receipt126_propagation_validator"
    sys.modules.pop(module_name, None)
    spec = importlib.util.spec_from_file_location(module_name, VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Receipt-126 propagation validator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class Receipt126PropagationValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def assert_rejected(self, mutated: dict[str, object]) -> None:
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated, frozen_probe=None)

    def test_canonical_manifest_closes_only_registered_contract(self) -> None:
        result = self.validator.validate_manifest(self.manifest)
        self.assertEqual(result["status"], "registered_contract_pass")
        self.assertEqual(result["substantiveTruth"], "not_assessed")
        self.assertEqual(result["registeredSurfaces"], 76)
        self.assertEqual(result["semanticRequirements"], 10)
        self.assertEqual(result["mutations"], 14)
        self.assertEqual(result["frozenScope"], "clean")
        self.assertEqual(result["scope"], "registered_paths_and_tests_only")

    def test_unknown_schema_field_including_self_hash_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["manifestSha256"] = "self-referential-authority-fiction"
        self.assert_rejected(mutated)

    def test_open_status_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["status"] = "open"
        self.assert_rejected(mutated)

    def test_tier_inflation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["evidenceTier"] = "[A] corpus-wide truth"
        self.assert_rejected(mutated)

    def test_duplicate_surface_id_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["surfaces"][1]["id"] = mutated["surfaces"][0]["id"]
        self.assert_rejected(mutated)

    def test_duplicate_mutation_id_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["mutations"][1]["id"] = mutated["mutations"][0]["id"]
        self.assert_rejected(mutated)

    def test_missing_registered_path_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["surfaces"][0]["path"] = "05_COSMOLOGY/DOES_NOT_EXIST.md"
        self.assert_rejected(mutated)

    def test_missing_required_marker_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["surfaces"][0]["requiredMarkers"][0] = "ABSENT-MARKER-126"
        self.assert_rejected(mutated)

    def test_live_forbidden_regex_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["surfaces"][0]["forbiddenPatterns"][0] = (
            r"These are \*\*chart facts only\*\*\."
        )
        self.assert_rejected(mutated)

    def test_invalid_forbidden_regex_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["surfaces"][0]["forbiddenPatterns"][0] = "(unclosed"
        self.assert_rejected(mutated)

    def test_mutation_omission_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["mutations"] = mutated["mutations"][:-1]
        self.assert_rejected(mutated)

    def test_semantic_requirement_omission_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["semanticRequirements"] = mutated["semanticRequirements"][:-1]
        self.assert_rejected(mutated)

    def test_unknown_semantic_surface_reference_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["semanticRequirements"][0]["surfaceIds"][0] = "phantom-surface"
        self.assert_rejected(mutated)

    def test_frozen_prefix_touch_fails_closed(self) -> None:
        def probe(_root, _base, _prefixes):
            return ("12_PUBLIC_SITE/index.html",)

        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(self.manifest, frozen_probe=probe)

    def test_cli_json_is_deterministic_and_denies_truth_verdict(self) -> None:
        command = [sys.executable, str(VALIDATOR_PATH), "--json"]
        first = subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout
        second = subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout
        self.assertEqual(first, second)
        payload = json.loads(first)
        self.assertEqual(payload["status"], "registered_contract_pass")
        self.assertEqual(payload["substantiveTruth"], "not_assessed")

    def test_registered_markdown_has_no_control_bytes(self) -> None:
        allowed = {9, 10, 13}
        for surface in self.manifest["surfaces"]:
            path = ROOT / surface["path"]
            if path.suffix.lower() != ".md":
                continue
            invalid = [
                (offset, byte)
                for offset, byte in enumerate(path.read_bytes())
                if (byte < 32 and byte not in allowed) or byte == 127
            ]
            self.assertEqual(invalid, [], msg=f"control bytes in {path}")

    def test_repaired_operator_formulas_are_exact_text(self) -> None:
        expected = {
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/"
            "MF_290_The_Ektropic_Radius_v2.md": (
                r"\mathcal H(a)=(\mathcal B(a),T,\mathcal I,\mathcal U),"
            ),
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/"
            "MF_295_c_Bounds_the_Moral_Circle.md": (
                r"\lVert x-x_0\rVert \le c(t-t_0)."
            ),
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/"
            "MF_297_Alpha_Is_the_Coupling.md": (
                r"\alpha=\frac{e^2}{4\pi\varepsilon_0\hbar c},"
            ),
        }
        for relative, formula in expected.items():
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(formula, text, msg=relative)


if __name__ == "__main__":
    unittest.main()
