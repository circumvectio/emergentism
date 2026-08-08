#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_ruling_landed.py — gate that fails while carriers of a ruling remain.

A "ruling made" is a K2 disposition; a "ruling landed" is the same
disposition propagated to all surfaces that carried the pre-ruling
content. The corpus has no μ₄ for its own decisions: this gate binds
the verdict to the contradiction census (``check_contradiction_census.py``),
so the verdict is machine-verifiable, not editorial.

Per ruling, the gate:
  1. Looks up the ruling's pre-state pattern and target category
     in a built-in ruling table.
  2. Runs the contradiction census (``scan()``) against the corpus.
  3. Counts carriers in the target category.
  4. Exits 0 if carriers ≤ threshold, 1 if > threshold, 2 if errored.

The default threshold is 0 (strict "ruling fully landed" reading). Raise
it to allow known residual carriers (e.g. meta-references in corrections
pages that have been audited) without rewriting the gate.

REGISTERED RULINGS
------------------
WO-D1-2026-07-19  — Retired Titan infix ``⊙ = • × ○`` (type error).
                    Target category: ``public_html``. The 0 target means
                    no HTML page in ``12_PUBLIC_SITE/`` may still carry
                    the form, even as a meta-reference. The looser
                    ``public_html_doctrinal`` category is what a
                    "no live doctrine" reading would use; it is not the
                    default for this ruling.

USAGE
-----
    python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py \\
        --ruling-id WO-D1-2026-07-19
    python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py \\
        --ruling-id WO-D1-2026-07-19 --threshold 2
    python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py --list
    python3 09_TOOLS/01_SCRIPTS/check_ruling_landed.py \\
        --ruling-id WO-D1-2026-07-19 --root /path/to/01_EMERGENTISM

EXIT CODES
----------
    0  ruling landed (carriers ≤ threshold)
    1  ruling NOT yet landed (carriers > threshold)
    2  errored (unknown ruling, scan failed, bad args, missing root)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Locate and import the census. Adding the script's directory to
# sys.path keeps the import explicit and avoids relying on a stale
# PYTHONPATH. The census file is a sibling — both live in
# 09_TOOLS/01_SCRIPTS/.
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import check_contradiction_census as census  # noqa: E402


# Ruling table: the durable registry of the corpus's own decisions.
#
# Each entry pins a ruling_id to:
#   - pattern:   the regex matching the pre-state content
#   - category:  which census scan() key to count
#                (one of: total / live / public /
#                 public_html / public_html_doctrinal)
#   - description: human-readable context for the audit trail
#
# Add a row when a new K2 disposition lands. Do not delete rows; the
# ruling history is provenance, not active state, and the registry
# must remain queryable long after the carrier set has dropped to
# zero. Each new ruling requires a pattern and a category; the
# description is the audit-trail anchor for the K2 packet that
# registered it.
RULING_TABLE: dict[str, dict] = {
    "WO-D1-2026-07-19": {
        "pattern": census.RETIRED_TITAN_INFIX,
        "category": "public_html",
        "description": (
            "Retired Titan infix ⊙ = • × ○ (K2 disposition WO-D1, "
            "2026-07-19). Type error: realm mark presented as a product "
            "of boundary marks. Default category public_html — any HTML "
            "page in 12_PUBLIC_SITE/ that still carries the form, even "
            "as a meta-reference, is a residual carrier. The looser "
            "public_html_doctrinal category is a 'no live doctrine' "
            "reading and is not the default."
        ),
    },
}


def list_rulings() -> int:
    """Print the registered rulings; return 0."""
    print("RULING TABLE — registered corpus dispositions")
    print()
    if not RULING_TABLE:
        print("  (no rulings registered)")
        return 0
    for rid, spec in sorted(RULING_TABLE.items()):
        print(f"  {rid}")
        print(f"    pattern:   {spec['pattern'].pattern}")
        print(f"    category:  {spec['category']}")
        print(f"    {spec['description']}")
        print()
    return 0


def run_gate(ruling_id: str, threshold: int, root: Path) -> int:
    """Run the gate for a given ruling; return the exit code.

    Exits 0 if carriers ≤ threshold (LANDED), 1 if > threshold
    (NOT_LANDED), 2 if any precondition fails (unknown ruling,
    invalid threshold, missing root, scan error).
    """
    if threshold < 0:
        print(f"ERROR: threshold must be >= 0 (got {threshold})", file=sys.stderr)
        return 2
    spec = RULING_TABLE.get(ruling_id)
    if spec is None:
        print(f"ERROR: unknown ruling_id: {ruling_id!r}", file=sys.stderr)
        print(
            f"  known rulings: "
            f"{', '.join(sorted(RULING_TABLE)) or '(none registered)'}",
            file=sys.stderr,
        )
        print("  use --list to see registered rulings", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"ERROR: root not a directory: {root}", file=sys.stderr)
        return 2

    try:
        counts = census.scan(root)
    except Exception as exc:  # noqa: BLE001 — gate must fail loudly
        print(f"ERROR: census scan failed: {exc}", file=sys.stderr)
        return 2

    category = spec["category"]
    if category not in counts:
        print(
            f"ERROR: category {category!r} not in census output "
            f"(known: {sorted(counts)})",
            file=sys.stderr,
        )
        return 2
    carriers = counts[category]
    n = len(carriers)
    landed = n <= threshold
    status = "LANDED" if landed else "NOT_LANDED"
    exit_code = 0 if landed else 1

    ts = census.now_ict()
    print(f"RULING LANDED GATE — {ts}")
    print()
    print(f"Ruling:        {ruling_id}")
    print(f"Pattern:       {spec['pattern'].pattern}")
    print(f"Category:      {category}")
    print(f"Root:          {root}")
    print(f"Threshold:     {threshold}")
    print(f"Carriers:      {n}")
    print()
    cmp = "≤" if landed else ">"
    print(f"Status:        {status}  (carriers {n} {cmp} threshold {threshold})")
    print()
    if carriers:
        print(f"Residual carriers ({n}):")
        for rel in carriers:
            print(f"  {rel.as_posix()}")
        print()
    print(f"GATE: {status}  (exit {exit_code})")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Gate that fails while carriers of a ruling remain. "
            "Bind the verdict to the contradiction census."
        ),
    )
    parser.add_argument(
        "--ruling-id",
        help=(
            "The K2 disposition to check (e.g. WO-D1-2026-07-19). "
            "Use --list to see registered rulings."
        ),
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        help="Maximum number of residual carriers allowed (default: 0).",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Corpus root (default: grandparent of this script, "
            "i.e. 01_EMERGENTISM)."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the registered rulings and exit.",
    )
    args = parser.parse_args()

    if args.list:
        return list_rulings()

    if not args.ruling_id:
        parser.error(
            "--ruling-id is required (or use --list to see registered rulings)"
        )

    if args.root is not None:
        root = args.root.resolve()
    else:
        # Default root: grandparent of this script (01_EMERGENTISM).
        # We do NOT use census.script_root() because it reads sys.argv[1],
        # which is the gate's argv, not the census's — and would swallow
        # --ruling-id as a path.
        root = Path(__file__).resolve().parents[2]
    return run_gate(args.ruling_id, args.threshold, root)


if __name__ == "__main__":
    raise SystemExit(main())
