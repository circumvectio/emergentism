#!/usr/bin/env python3
"""Tests for marketplace_discipline_check and a7_receipt_validator."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPTS = Path(__file__).resolve().parent
DISCIPLINE = SCRIPTS / "marketplace_discipline_check.py"
A7 = SCRIPTS / "a7_receipt_validator.py"


def run(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    return proc.returncode, proc.stdout, proc.stderr


def test_discipline_passes_on_seeded_catalog():
    code, stdout, _ = run(["python3", str(DISCIPLINE)])
    assert code == 0, f"discipline check failed:\n{stdout}"
    assert "All listings comply" in stdout


def test_discipline_strict_passes_on_seeded_catalog():
    code, _, _ = run(["python3", str(DISCIPLINE), "--strict"])
    assert code == 0


def test_a7_default_passes_with_only_warnings():
    """Default mode: only ERRORS fail. Warnings are advisory."""
    code, _, _ = run(["python3", str(A7)])
    assert code == 0


def test_a7_strict_flags_unresolved_warnings():
    """Strict mode: any warnings fail. Confirms the validator is finding signal."""
    code, _, _ = run(["python3", str(A7), "--strict"])
    # Currently we expect warnings but no errors — strict should flag
    assert code == 1


def test_listings_have_titles():
    """Every listing must start with # Title (mandatory field 1)."""
    catalog = REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "03_PRODUCTS" / "skyzai_marketplace"
    for f in sorted(catalog.glob("[0-9][0-9]_*.md")):
        if f.name.startswith("00_"):
            continue
            
        first = f.read_text(encoding="utf-8").splitlines()[0]
        assert first.startswith("# "), f"{f.name} missing # title"


def test_manifest_exists_and_links_resolve():
    manifest = REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "03_PRODUCTS" / "00_SKYZAI_COM_PRODUCT_MANIFEST.md"
    assert manifest.exists()
    text = manifest.read_text(encoding="utf-8")
    # spot-check key cross-refs from the manifest
    refs = [
        "PHI_SPLIT_AFFILIATE_DOCTRINE.md",
        "API_PAY_FEE_DOCTRINE.md",
        "COMMERCIAL_STRATEGY_2026_05_09.md",
        "07_PUBLIC_SURFACE_DOUBLET.md",
    ]
    for r in refs:
        assert r in text, f"manifest missing reference to {r}"


def test_cross_entity_receipt_traversal_passes():
    """Cross-entity receipt protocol functional test (Goal 3 step 2)."""
    traversal_script = SCRIPTS / "test_cross_entity_receipt_traversal.py"
    code, stdout, stderr = run(["python3", str(traversal_script)])
    assert code == 0, f"Cross-entity receipt traversal failed: {stdout}\n{stderr}"


def main() -> int:
    tests = [
        test_discipline_passes_on_seeded_catalog,
        test_discipline_strict_passes_on_seeded_catalog,
        test_a7_default_passes_with_only_warnings,
        test_a7_strict_flags_unresolved_warnings,
        test_listings_have_titles,
        test_manifest_exists_and_links_resolve,
        test_cross_entity_receipt_traversal_passes,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"✅ {t.__name__}")
        except AssertionError as e:
            print(f"❌ {t.__name__}: {e}")
            failures += 1
        except Exception as e:
            print(f"💥 {t.__name__}: {type(e).__name__}: {e}")
            failures += 1
    print()
    if failures == 0:
        print(f"{len(tests)}/{len(tests)} tests passed ✅")
        return 0
    print(f"{len(tests) - failures}/{len(tests)} passed; {failures} failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
