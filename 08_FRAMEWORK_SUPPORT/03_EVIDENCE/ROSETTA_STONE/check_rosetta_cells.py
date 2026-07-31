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
  6. Every pack names rival maps, and those rivals must EXIST as declared packs.
     A placeholder like "PHIL5_rival_pending" satisfies the letter and defeats the
     purpose; a projection is only tested when something at a different cardinality
     has actually been built to compete with it.

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
    "independence_status",
]
# `rival_maps` is deliberately NOT in PACK_REQUIRED: an empty list is a legitimate
# state when paired with a dated `rival_debt`. It has its own check below.
VALID_INDEPENDENCE = {
    "independent", "partially dependent", "framework-derived", "unknown",
}


def main() -> int:
    data = json.loads(LEDGER.read_text())
    order = data["tier_order"]
    rank = {t: i for i, t in enumerate(order)}  # lower index = stronger
    problems: list[str] = []
    warnings: list[str] = []

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
        if not pack.get("rival_maps") and not pack.get("rival_debt"):
            problems.append(
                f"pack {pid}: no rival_maps and no rival_debt. A projection "
                "untested against a cheaper-cardinality rival has not earned its "
                "shape — either build one, or record the debt with a date."
            )

    # Second pass: rivals must be real. Needs every pack parsed first.
    for pack in data["packs"]:
        pid = pack.get("projection_id", "<unnamed>")
        if pack.get("role") == "counter-rival":
            continue  # a rival is not required to have rivals of its own
        for rival in pack.get("rival_maps") or []:
            if rival not in packs:
                problems.append(
                    f"pack {pid}: rival {rival!r} is not a declared pack. A named "
                    "but unbuilt rival is a placeholder — it satisfies the rule "
                    "and defeats it. Build the rival or drop the claim."
                )
            elif packs[rival].get("native_cardinality") == pack.get("native_cardinality"):
                problems.append(
                    f"pack {pid}: rival {rival!r} has the SAME native_cardinality "
                    f"({pack.get('native_cardinality')}). A same-shape rival tests "
                    "nothing about whether the shape was earned."
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

    # Debt is not a pass. It is a failure held open on purpose, printed every run
    # so it cannot quietly become the normal state.
    for pack in data["packs"]:
        if pack.get("rival_debt"):
            debt = pack["rival_debt"]
            warnings.append(
                f"pack {pack['projection_id']}: UNTESTED since {debt.get('since')} "
                f"— {debt.get('reason')}"
            )

    if warnings:
        print(f"\nrosetta cell ledger: {len(warnings)} open debt(s)\n")
        for w in warnings:
            print(f"  ! {w}")
        print()

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
