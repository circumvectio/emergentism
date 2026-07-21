#!/usr/bin/env python3
"""marketplace_discipline_check — A7 catalog discipline enforcer.

Walks 02_SKYZAI/01_NOOSPHERE/03_PRODUCTS/skyzai_marketplace/ and verifies every listing
01_*.md through 06_*.md (and any 0N_*.md added later) carries the 13 mandatory
schema fields per `00_API_SERVICE_MARKETPLACE.md` §"Catalog discipline schema".

Exit code:
  0 = all listings compliant
  1 = one or more listings non-compliant; details printed

Usage:
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/marketplace_discipline_check.py

  # CI/precommit:
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/marketplace_discipline_check.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

REPO = Path(__file__).resolve().parents[3]
CATALOG = REPO / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "03_PRODUCTS" / "skyzai_marketplace"

# 13 mandatory fields per 00_API_SERVICE_MARKETPLACE.md §"Catalog discipline schema"
# Each entry: (slug, regex pattern that proves the field is present, human description)
REQUIRED_FIELDS: list[tuple[str, str, str]] = [
    ("title",            r"^# .+",                                  "1. # Title (top-level heading)"),
    ("status",           r"\*\*Status:\*\*\s+`(LOCAL_PROOF|SPEC|SPEC→PROOF|EXTERNAL_PROOF)`", "2. Status (LOCAL_PROOF/SPEC/SPEC→PROOF/EXTERNAL_PROOF)"),
    ("buyer_value",      r"\*\*Buyer-visible value sentence:\*\*",  "3. Buyer-visible value sentence"),
    ("wedge",            r"\*\*Wedge dependency:\*\*",              "4. Wedge dependency"),
    ("what_does",        r"^##\s*What it does",                     "5. What it does (## section)"),
    ("pricing",          r"^##\s*Pricing",                          "6. Pricing (## section)"),
    ("modularity",       r"^##\s*Modularity",                       "7. Modularity (## section)"),
    ("k4_portability",   r"^##\s*K4 portability",                   "8. K4 portability (## section)"),
    ("eta_zero",         r"^##\s*η=0 boundary",                     "9. η=0 boundary (## section)"),
    ("k2_scope",         r"^##\s*K2 scope",                         "10. K2 scope (## section)"),
    ("evidence",         r"^##\s*Evidence per claim",               "11. Evidence per claim (## section)"),
    ("integration",      r"^##\s*Integration time",                 "12. Integration time estimate (## section)"),
    ("open_questions",   r"^##\s*Open questions",                   "13. Open questions (## section)"),
]


class CheckResult(NamedTuple):
    file: Path
    field: str
    description: str
    found: bool


def check_listing(path: Path) -> list[CheckResult]:
    """Return one CheckResult per required field."""
    text = path.read_text(encoding="utf-8")
    return [
        CheckResult(
            file=path,
            field=slug,
            description=desc,
            found=bool(re.search(pattern, text, re.MULTILINE)),
        )
        for slug, pattern, desc in REQUIRED_FIELDS
    ]


def discover_listings() -> list[Path]:
    """Find listing files: 01_*.md through 0N_*.md (skip 00_*)."""
    return sorted(
        p for p in CATALOG.glob("[0-9][0-9]_*.md")
        if not p.name.startswith("00_")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="A7 catalog discipline check")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any non-compliance (for CI / pre-commit)",
    )
    args = parser.parse_args()

    if not CATALOG.exists():
        print(f"ERROR: catalog not found at {CATALOG}", file=sys.stderr)
        return 1

    listings = discover_listings()
    if not listings:
        print(f"ERROR: no listings found in {CATALOG}", file=sys.stderr)
        return 1

    print(f"Marketplace discipline check: {len(listings)} listing(s) under audit\n")
    total_failures = 0

    for path in listings:
        results = check_listing(path)
        missing = [r for r in results if not r.found]
        rel = path.relative_to(REPO)
        if not missing:
            print(f"✅ {rel}  ({len(results)}/{len(results)} fields)")
        else:
            print(f"❌ {rel}  ({len(results) - len(missing)}/{len(results)} fields)")
            for r in missing:
                print(f"   missing: {r.description}")
            total_failures += len(missing)

    print()
    if total_failures == 0:
        print("All listings comply with catalog discipline ✅")
        return 0

    print(f"Total non-compliances: {total_failures}")
    print("Per `00_API_SERVICE_MARKETPLACE.md` §Listing change protocol:")
    print("  1. Manifest update first (SKYZAI_COM_PRODUCT_MANIFEST.md §2)")
    print("  2. K2 envelope for status/pricing/η=0 changes")
    print("  3. A7 audit (this script)")
    print("  4. PWA refresh (07_PWAs/skyzai_com/index.html)")

    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
