#!/usr/bin/env python3
"""
tree_audit.py — enforce a subset of the Tree Constitution mechanically.

The four laws (boundary / ownership / routing / failure-mode) are codified at
01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_TREE_CONSTITUTION.md.

This script enforces the three tests that are mechanically checkable:

  1. Exclusion-clause test     — each canonical root README contains a
                                  "Does NOT contain" section (Failure-Mode Law).
  2. Single-archive-root test  — no 99_ARCHIVE/ or 90_ARCHIVE/ siblings of
                                  the canonical roots (Boundary Law: cold
                                  history is 999_ARCHIVE, full stop).
  3. Compatibility-stub decay  — */91_COMPATIBILITY/ folders > 180 days old
                                  without a redirect tombstone are flagged.

Tests 4-7 (doctrine-leak, substrate-isolation, portfolio-quarantine,
routing-precedence-citation) are normative — flagged in PR review,
not enforced here.

Exit 0 = all checks pass.
Exit 1 = at least one violation; the report lists each.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

# Canonical top-level roots after the 2026-05-29 root-alias retirement.
# Aligned with check_no_alias_paths.py and ORIENTATION.md §2; the retired
# aliases (2_SKYZAI_ORG, 3_SKYZAI_COM, 4_ENTITIES, root 999_ARCHIVE) were
# folded into 03_VENTURES and 90_ARCHIVE.
CANONICAL_ROOTS = (
    "00_START_HERE",
    "01_EMERGENTISM",
    "03_VENTURES",
    "03_VENTURES/_PORTFOLIO",
    "02_SKYZAI/06_SPECTRE",
    "02_SKYZAI/08_EVOLUTIONARY_NETWORK",
    "90_ARCHIVE",
)

EXCLUSION_PHRASES = (
    "does not contain",
    "does NOT contain",
    "Does NOT contain",
    "Does not contain",
)

COMPAT_STUB_GRACE_DAYS = 180


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "manifest.yaml").exists():
            return parent
    raise SystemExit("tree_audit: cannot locate repo root (no manifest.yaml found)")


def check_exclusion_clauses(root: Path) -> list[str]:
    violations: list[str] = []
    for r in CANONICAL_ROOTS:
        readme = root / r / "README.md"
        if not readme.exists():
            violations.append(f"{r}/README.md missing")
            continue
        text = readme.read_text(encoding="utf-8", errors="replace")
        if not any(phrase.lower() in text.lower() for phrase in EXCLUSION_PHRASES):
            violations.append(
                f"{r}/README.md missing exclusion clause "
                f'(needs a "Does NOT contain" section per Failure-Mode Law)'
            )
    return violations


def check_single_archive_root(root: Path) -> list[str]:
    violations: list[str] = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        name = entry.name
        if name.startswith("."):
            continue
        if name in CANONICAL_ROOTS:
            continue
        if name in ("99_ARCHIVE", "90_ARCHIVE", "00_ARCHIVE"):
            violations.append(
                f"top-level archive folder {name}/ should be merged into 90_ARCHIVE/"
            )
    return violations


def check_compat_stub_decay(root: Path) -> list[str]:
    violations: list[str] = []
    grace_seconds = COMPAT_STUB_GRACE_DAYS * 86_400
    now = time.time()
    for r in CANONICAL_ROOTS:
        compat = root / r / "91_COMPATIBILITY"
        if not compat.exists():
            continue
        tombstone = compat / "TOMBSTONE.md"
        readme = compat / "README.md"
        anchor = readme if readme.exists() else compat
        age_seconds = now - anchor.stat().st_mtime
        if age_seconds > grace_seconds and not tombstone.exists():
            age_days = int(age_seconds / 86_400)
            violations.append(
                f"{r}/91_COMPATIBILITY/ has aged {age_days} days "
                f"(> {COMPAT_STUB_GRACE_DAYS}) without TOMBSTONE.md — flag for L6 sweep"
            )
    return violations


def main() -> int:
    root = _repo_root()
    all_violations: list[tuple[str, list[str]]] = []

    tests = (
        ("exclusion-clause", check_exclusion_clauses),
        ("single-archive-root", check_single_archive_root),
        ("compat-stub-decay", check_compat_stub_decay),
    )

    for name, fn in tests:
        violations = fn(root)
        if violations:
            all_violations.append((name, violations))

    if not all_violations:
        print("tree_audit: all checks passed.")
        for name, _ in tests:
            print(f"  ✓ {name}")
        return 0

    print("tree_audit: violations detected.")
    for name, violations in all_violations:
        print(f"\n  ✗ {name}:")
        for v in violations:
            print(f"      {v}")
    print("\nSee 01_EMERGENTISM/08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_TREE_CONSTITUTION.md")
    return 1


if __name__ == "__main__":
    sys.exit(main())
