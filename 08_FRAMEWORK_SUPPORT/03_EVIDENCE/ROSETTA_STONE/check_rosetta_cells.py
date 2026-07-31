#!/usr/bin/env python3
"""Make the Rosetta's own laws bind.

The cell audit schema (10_CELL_AUDIT_SCHEMA_2026_04_25.md) already requires a kill
criterion, an independence status, and separate fact/mapping tiers. Nothing enforced
any of it, so those requirements were intentions rather than constraints.

This validates rosetta_cells.json against the rules the protocol already states:

  1. Every cell carries a non-empty kill_criterion. A mapping that cannot fail is
     not a claim.
  2. cell_tier never exceeds fact_tier or mapping_tier. An established fact placed
     speculatively stays speculative — this is the rule that stops a strong source
     laundering a weak placement.
  3. independence_status is declared. "unknown" is allowed and honest; absent is not.
  4. Every cell names its projection_id. Bare row talk is what let PHIL7 and GEN7
     put teleology at opposite ends of the same notation.
  5. Every pack declares native_cardinality and normalization_steps BEFORE any
     mapping — a five-part native system must remain five until someone says, in
     writing, what they did to it.
  6. Every pack names rival maps. A seven-row projection with no five- or six-row
     rival has not been tested against the cheapest explanation of its own fit.

Exit 1 on any violation. Run:  python3 check_rosetta_cells.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

LEDGER = Path(__file__).parent / "rosetta_cells.json"

CELL_REQUIRED = [
    "cell_id", "projection_id", "row", "column_class", "domain_expression",
    "fact_tier", "mapping_tier", "cell_tier", "independence_status",
    "kill_criterion", "downgrade_path", "audit_status",
]
PACK_REQUIRED = [
    "projection_id", "native_cardinality", "normalization_steps",
    "independence_status", "rival_maps",
]
VALID_INDEPENDENCE = {
    "independent", "partially dependent", "framework-derived", "unknown",
}


def main() -> int:
    data = json.loads(LEDGER.read_text())
    order = data["tier_order"]
    rank = {t: i for i, t in enumerate(order)}  # lower index = stronger
    problems: list[str] = []

    packs = {p["projection_id"]: p for p in data["packs"]}

    for pack in data["packs"]:
        pid = pack.get("projection_id", "<unnamed>")
        for field in PACK_REQUIRED:
            if not pack.get(field):
                problems.append(f"pack {pid}: missing required field `{field}`")
        if pack.get("independence_status") not in VALID_INDEPENDENCE:
            problems.append(
                f"pack {pid}: independence_status "
                f"{pack.get('independence_status')!r} not one of {sorted(VALID_INDEPENDENCE)}"
            )
        if not pack.get("rival_maps"):
            problems.append(
                f"pack {pid}: no rival_maps. A projection untested against a "
                "cheaper-cardinality rival has not earned its shape."
            )

    for cell in data["cells"]:
        cid = cell.get("cell_id", "<unnamed>")

        for field in CELL_REQUIRED:
            value = cell.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                problems.append(f"{cid}: missing or empty `{field}`")

        if cell.get("projection_id") not in packs:
            problems.append(
                f"{cid}: projection_id {cell.get('projection_id')!r} has no declared pack"
            )

        # Rule 2 — the one that stops tier laundering.
        fact, mapping, final = (
            cell.get("fact_tier"), cell.get("mapping_tier"), cell.get("cell_tier")
        )
        if all(t in rank for t in (fact, mapping, final)):
            weakest = max(rank[fact], rank[mapping])
            if rank[final] < weakest:
                problems.append(
                    f"{cid}: cell_tier [{final}] is STRONGER than its weakest input "
                    f"(fact [{fact}], mapping [{mapping}]). A cell inherits its "
                    f"weakest link — expected [{order[weakest]}] or lower."
                )
        else:
            bad = [t for t in (fact, mapping, final) if t not in rank]
            problems.append(f"{cid}: tier(s) {bad} not in tier_order {order}")

        if cell.get("independence_status") not in VALID_INDEPENDENCE:
            problems.append(
                f"{cid}: independence_status {cell.get('independence_status')!r} "
                f"not one of {sorted(VALID_INDEPENDENCE)}"
            )

        # A cell_id that does not carry its namespace invites bare citation.
        if not str(cid).startswith(str(cell.get("projection_id", "")) + "__"):
            problems.append(
                f"{cid}: cell_id must be prefixed with its projection_id, so it "
                "cannot be quoted without its namespace."
            )

    if problems:
        print(f"\nrosetta cell ledger: FAIL — {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  - {p}")
        print()
        return 1

    print(
        f"rosetta cell ledger: PASS "
        f"({len(data['cells'])} cells, {len(data['packs'])} packs)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
