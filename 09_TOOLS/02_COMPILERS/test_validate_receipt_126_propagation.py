#!/usr/bin/env python3
"""Tests for the Receipt-126 propagation manifest validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
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

    def assert_manifest_error_contains(self, manifest, marker: str) -> None:
        with self.assertRaises(self.validator.ManifestError) as caught:
            self.validator.validate_manifest(manifest)
        self.assertIn(marker, str(caught.exception))

    def test_canonical_manifest_closes_exact_scope(self) -> None:
        result = self.validator.validate_manifest(self.manifest)
        self.assertEqual(result["owners"], 26)
        self.assertEqual(result["movedOwners"], 2)
        self.assertEqual(result["mutations"], 14)
        self.assertEqual(result["derivedSeams"], 6)
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

    def test_mutation_owner_drift_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["mutations"][0]["owner"] = "00_META/00_THE_COMPASS.md"
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_historical_owner_move_omission_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["ownerRepair"]["currentPathMoves"] = mutated["ownerRepair"][
            "currentPathMoves"
        ][:-1]
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_historical_owner_move_cannot_gain_semantic_authority(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["ownerRepair"]["currentPathMoves"][0]["semanticAuthority"] = "active"
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_historical_owner_move_rejects_absolute_current_path(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        current = mutated["ownerRepair"]["currentPathMoves"][0]["currentPath"]
        mutated["ownerRepair"]["currentPathMoves"][0]["currentPath"] = str(
            ROOT / current
        )
        self.assert_manifest_error_contains(
            mutated, "must be a repository-relative POSIX path under 90_ARCHIVE"
        )

    def test_historical_owner_move_rejects_parent_traversal(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["ownerRepair"]["currentPathMoves"][0]["currentPath"] = (
            "90_ARCHIVE/../09_TOOLS/02_COMPILERS/validate_receipt_126_propagation.py"
        )
        self.assert_manifest_error_contains(mutated, "must not contain '..' traversal")

    def test_historical_owner_move_rejects_direct_symlink(self) -> None:
        archive = ROOT / "90_ARCHIVE"
        with tempfile.TemporaryDirectory(
            prefix=".receipt126-direct-", dir=archive
        ) as temporary:
            temporary_path = Path(temporary)
            target = temporary_path / "target.md"
            target.write_text("archived test custody\n", encoding="utf-8")
            link = temporary_path / "current.md"
            try:
                link.symlink_to(target.name)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {exc}")
            mutated = copy.deepcopy(self.manifest)
            mutated["ownerRepair"]["currentPathMoves"][0]["currentPath"] = (
                link.relative_to(ROOT).as_posix()
            )
            self.assert_manifest_error_contains(
                mutated, "must not contain direct or ancestor symlinks"
            )

    def test_historical_owner_move_rejects_symlink_ancestor_and_escape(self) -> None:
        archive = ROOT / "90_ARCHIVE"
        with tempfile.TemporaryDirectory(prefix="receipt126-outside-") as outside:
            outside_path = Path(outside)
            target = outside_path / "target.md"
            target.write_text("outside archive\n", encoding="utf-8")
            with tempfile.TemporaryDirectory(
                prefix=".receipt126-ancestor-", dir=archive
            ) as temporary:
                ancestor = Path(temporary) / "escaped"
                try:
                    ancestor.symlink_to(outside_path, target_is_directory=True)
                except OSError as exc:
                    self.skipTest(f"symlink creation unavailable: {exc}")
                mutated = copy.deepcopy(self.manifest)
                mutated["ownerRepair"]["currentPathMoves"][0]["currentPath"] = (
                    (ancestor / target.name).relative_to(ROOT).as_posix()
                )
                with self.assertRaises(self.validator.ManifestError) as caught:
                    self.validator.validate_manifest(mutated)
                error = str(caught.exception)
                self.assertIn("must not contain direct or ancestor symlinks", error)
                self.assertIn("resolves outside 90_ARCHIVE", error)

    def test_derived_seam_omission_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["derivedSeams"] = mutated["derivedSeams"][:-1]
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_derived_seam_marker_drift_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["derivedSeams"][0]["requiredMarkers"][0] = "missing marker"
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)

    def test_publication_authority_inflation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["authorityBoundary"] = "Publication is authorized."
        with self.assertRaises(self.validator.ManifestError):
            self.validator.validate_manifest(mutated)


if __name__ == "__main__":
    unittest.main()
