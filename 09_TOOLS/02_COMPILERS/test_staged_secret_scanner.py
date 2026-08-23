#!/usr/bin/env python3
"""Regression tests for the staged-secret scanner's generic fallback."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCANNER = ROOT / "09_TOOLS/01_SCRIPTS/check_no_secrets_staged.py"
SPEC = importlib.util.spec_from_file_location("staged_secret_scanner", SCANNER)
assert SPEC is not None and SPEC.loader is not None
scanner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scanner)


def added_line(content: str, path: str = "fixture.txt") -> str:
    return f"diff --git a/{path} b/{path}\n+++ b/{path}\n+{content}\n"


class StagedSecretScannerTests(unittest.TestCase):
    def test_explicit_sha256_custody_is_not_a_secret(self) -> None:
        digest = "a1" * 32
        diff = added_line(f'{{"sha256":"{digest}"}}', "register.json")
        self.assertEqual(scanner.scan(diff), [])

    def test_hash_file_custody_is_not_a_secret(self) -> None:
        digest = "b2" * 32
        diff = added_line(f"{digest}  conditions.json", "BATTERY_FROZEN_SHA256.txt")
        self.assertEqual(scanner.scan(diff), [])

    def test_typed_hash_field_is_not_a_secret(self) -> None:
        digest = "d4" * 32
        for field in ("atlas_hash", "trial_hash", "fixture_hash"):
            with self.subTest(field=field):
                diff = added_line(f'{{"{field}":"{digest}"}}', "receipt.json")
                self.assertEqual(scanner.scan(diff), [])

    def test_bare_64_hex_token_remains_suspicious(self) -> None:
        token = "c3" * 32
        findings = scanner.scan(added_line(token))
        self.assertEqual(findings[0]["pattern_name"], scanner.GENERIC_PATTERN_NAME)

    def test_human_receipt_and_test_identifiers_are_not_secrets(self) -> None:
        for identifier in (
            "234_FULL_CORPUS_ADJUDICATION_AND_COHERENCE_CALIBRATION_2026_08_01",
            "test_missing_tracked_path_blocks_both_modes_until_staged_deletion",
        ):
            with self.subTest(identifier=identifier):
                self.assertEqual(scanner.scan(added_line(identifier)), [])

    def test_provider_key_shapes_still_fail(self) -> None:
        token = "sk-proj-" + ("Ab7_" * 14)
        findings = scanner.scan(added_line(f'TOKEN="{token}"'))
        self.assertEqual(findings[0]["pattern_name"], "OpenAI project")

    def test_unknown_generic_token_still_fails(self) -> None:
        token = ("aB3z9Q7x" * 9)[:68]
        findings = scanner.scan(added_line(token))
        self.assertEqual(findings[0]["pattern_name"], scanner.GENERIC_PATTERN_NAME)


if __name__ == "__main__":
    unittest.main()
