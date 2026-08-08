#!/usr/bin/env python3
"""Negative controls for the Foundation's Titan/algebra type firewall."""

from __future__ import annotations

import importlib.util
import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "09_TOOLS/01_SCRIPTS/check_foundation.py"
SPEC = importlib.util.spec_from_file_location("check_foundation", CHECKER)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def copy_checker_fixture(temp_root: Path) -> None:
    """Copy every surface the checker requires into an isolated corpus."""

    surfaces = dict.fromkeys(
        (
            *MODULE.REQUIRED_SURFACES,
            *MODULE.ACTIVE_EXTRA_TYPE_SURFACES,
            MODULE.HISTORICAL_SIGNED_TITAN_RECORD,
            MODULE.ADDITIVE_TITAN_CORRECTION,
        )
    )
    for rel in surfaces:
        source = ROOT / rel
        target = temp_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def forbidden(text: str) -> bool:
    return bool(MODULE.titan_arithmetic_matches(text))


class FoundationTypeFirewallTests(unittest.TestCase):
    def test_retired_glyph_product_is_rejected(self) -> None:
        self.assertTrue(forbidden("⊙ = • × ○"))

    def test_retired_glyph_quotient_is_rejected(self) -> None:
        self.assertTrue(forbidden("• = ⊙ / ○"))

    def test_mixed_witness_equality_is_rejected(self) -> None:
        self.assertTrue(forbidden("e = 1_T"))
        self.assertTrue(forbidden("a ↦ •"))

    def test_operator_and_function_bypasses_are_rejected(self) -> None:
        examples = (
            "• + ○",
            "• · ○",
            "• ^ ○",
            "0_T + 1_N",
            "mul_T(0_T,1_T)",
            "log_T(1_T)",
            "e := 1_T",
            "a ≅ 0_T",
            "1_T + y",
            "y + 1_T",
            "sqrt(1_T)",
            "cast_Number(1_T)",
            "1_T**2",
            "1_T ⊗ v",
            "1_T ∈ Number",
        )
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(forbidden(example))

    def test_reciprocal_identity_cannot_be_called_titan_equation(self) -> None:
        self.assertTrue(forbidden("φ · ν = 1 is the equation ⊙ = • × ○"))

    def test_titan_geometry_coercions_are_rejected(self) -> None:
        examples = (
            "• and ○ are antipodal",
            "•, ○ form the metric poles",
            "The chordal distance between • and ○ is 2",
            "• is at θ = 0",
            "○ is on the south chart pole theta = pi",
            "NoCoercion(TitanFrame, ProjectivePoint) remains open",
        )
        for example in examples:
            with self.subTest(example=example):
                self.assertTrue(forbidden(example))

    def test_typed_geometry_denials_are_allowed(self) -> None:
        examples = (
            "• and ○ are not antipodal chart points",
            "No metric, pole, or antipodality claim transfers to • and ○.",
            "Ill-typed expression: d(•, ○) = 2",
            "NoCoercion(TitanFrame, ProjectivePoint) is settled: no coercion exists.",
            "Only p_N and p_S are chart poles.",
        )
        for example in examples:
            with self.subTest(example=example):
                self.assertFalse(forbidden(example))

    def test_typed_group_algebra_is_allowed(self) -> None:
        self.assertFalse(forbidden("a · b = e; b = a⁻¹ inside G"))

    def test_numeric_and_operator_free_forms_are_allowed(self) -> None:
        self.assertFalse(forbidden("φ · ν = 1; ι_P(0_P)=∞_P; •  ⊙  ○"))

    def test_explicit_denial_is_allowed(self) -> None:
        self.assertFalse(forbidden("φ · ν = 1 is not the equation ⊙ = • × ○"))

    def test_unrelated_retirement_cannot_shield_live_arithmetic(self) -> None:
        self.assertTrue(
            forbidden("The old node product is retired; • + ○ is selected here.")
        )

    def test_unrelated_denial_clause_cannot_shield_live_arithmetic(self) -> None:
        bypasses = (
            "Titan arithmetic is forbidden; • + ○ is selected here.",
            "mul_T is undefined historically; 1_T + 1_N = 2_N is active.",
            "The old form is invalid, but cast_Number(1_T) is current.",
        )
        for example in bypasses:
            with self.subTest(example=example):
                self.assertTrue(forbidden(example))

    def test_markup_and_line_wrapping_cannot_hide_arithmetic(self) -> None:
        bypasses = (
            "<span>1_T</span> + y",
            "<span>1_T</span> &isin; Number",
            "•\n+\n○",
            "cast_Number(\n1_T\n)",
        )
        for example in bypasses:
            with self.subTest(example=example):
                self.assertTrue(forbidden(example))

    def test_same_clause_unrelated_denial_cannot_shield(self) -> None:
        self.assertTrue(forbidden("• + ○ is selected because the old form is invalid"))

    def test_same_type_equality_and_rendering_are_allowed(self) -> None:
        self.assertFalse(forbidden("1_T = 0_T is false in TitanFrame"))
        self.assertFalse(forbidden("render(1_T) uses the selected glyph ⊙"))

    def test_repository_filename_is_not_a_titan_token(self) -> None:
        self.assertFalse(
            forbidden("φ·ν=1 is documented in 05_COSMOLOGY/00_THE_FORMULA.md")
        )

    def test_full_checker_catches_mutated_owner_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            copy_checker_fixture(temp_root)

            with mock.patch.object(MODULE, "ROOT", temp_root):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(MODULE.main(), 0)
                owner = temp_root / MODULE.FORMAL_DOCS[0]
                owner.write_text(
                    owner.read_text(encoding="utf-8") + "\n• + ○\n",
                    encoding="utf-8",
                )
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(MODULE.main(), 1)

    def test_full_checker_catches_wrapped_owner_and_current_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            copy_checker_fixture(temp_root)

            public_manifest = temp_root / MODULE.PUBLIC_PARITY_MANIFEST
            public_manifest.parent.mkdir(parents=True, exist_ok=True)
            public_manifest.write_text(
                '{"currentSurfaces":["index.html"]}\n', encoding="utf-8"
            )
            public_page = temp_root / "12_PUBLIC_SITE/index.html"
            public_page.write_text("<span>1_T</span> + y\n", encoding="utf-8")
            owner = temp_root / MODULE.FORMAL_DOCS[0]
            owner.write_text(
                owner.read_text(encoding="utf-8") + "\n•\n+\n○\n",
                encoding="utf-8",
            )

            with mock.patch.object(MODULE, "ROOT", temp_root):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(MODULE.main(), 1)

    def test_record_ledger_is_scanned_and_forbidden_arithmetic_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            copy_checker_fixture(temp_root)

            with mock.patch.object(MODULE, "ROOT", temp_root):
                self.assertIn(
                    MODULE.RECORD_LEDGER,
                    MODULE.active_foundation_scan_paths(temp_root),
                )
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(MODULE.main(), 0)

                ledger = temp_root / MODULE.RECORD_LEDGER
                ledger.write_text(
                    ledger.read_text(encoding="utf-8") + "\n• + ○\n",
                    encoding="utf-8",
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn(MODULE.RECORD_LEDGER.as_posix(), output.getvalue())

    def test_missing_required_active_extra_surface_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            copy_checker_fixture(temp_root)
            (temp_root / MODULE.RECORD_LEDGER).unlink()

            output = io.StringIO()
            with mock.patch.object(MODULE, "ROOT", temp_root):
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
            self.assertIn(
                f"missing required active Foundation type surface: "
                f"{MODULE.RECORD_LEDGER.as_posix()}",
                output.getvalue(),
            )

    def test_signed_historical_infix_requires_exact_bytes_and_correction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            copy_checker_fixture(temp_root)

            with mock.patch.object(MODULE, "ROOT", temp_root):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(MODULE.main(), 0)

                record = temp_root / MODULE.HISTORICAL_SIGNED_TITAN_RECORD
                original_record = record.read_text(encoding="utf-8")
                record.write_text(original_record + "\n", encoding="utf-8")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn("historical signed Titan record digest drift", output.getvalue())
                record.write_text(original_record, encoding="utf-8")

                correction = temp_root / MODULE.ADDITIVE_TITAN_CORRECTION
                original_correction = correction.read_text(encoding="utf-8")
                correction.write_text(
                    original_correction.replace(
                        "## Additive historical correction",
                        "## Historical note",
                    ),
                    encoding="utf-8",
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn("additive Titan correction lost required marker", output.getvalue())
                correction.write_text(original_correction, encoding="utf-8")

                correction.write_text(
                    original_correction
                    + "\n\n## Current formula\n\n⊙ = • × ○\n",
                    encoding="utf-8",
                )
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn(MODULE.ADDITIVE_TITAN_CORRECTION.as_posix(), output.getvalue())
                self.assertIn("forbidden Titan arithmetic", output.getvalue())
                correction.write_text(original_correction, encoding="utf-8")

                uplink = temp_root / "11_UPLINK"
                real_uplink = temp_root / "11_UPLINK_REAL"
                uplink.rename(real_uplink)
                uplink.symlink_to(real_uplink, target_is_directory=True)
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn("symlink component", output.getvalue())
                uplink.unlink()
                real_uplink.rename(uplink)

                outside = temp_root / "05_COSMOLOGY/03_FORMAL_SYSTEM/ZZ_MUTATION.md"
                outside.parent.mkdir(parents=True, exist_ok=True)
                outside.write_text("⊙ = " + "• × ○\n", encoding="utf-8")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(MODULE.main(), 1)
                self.assertIn("ZZ_MUTATION.md", output.getvalue())

    def test_public_generator_uses_the_shared_firewall(self) -> None:
        generator_path = ROOT / "12_PUBLIC_SITE/generate_public_library.py"
        spec = importlib.util.spec_from_file_location("generate_public_library", generator_path)
        assert spec and spec.loader
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        with self.assertRaises(ValueError):
            generator.assert_titan_type_safe(
                "<span>1_T</span> + y",
                ROOT / "12_PUBLIC_SITE/read/index.html",
            )


if __name__ == "__main__":
    unittest.main()
