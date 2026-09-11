#!/usr/bin/env python3
"""Render the corpus as one infinite outline, in apu.bot's import format.

WHY THIS EXISTS
---------------
`build_corpus_index.py` names the corpus's failure mode: not falsity but
UNFINDABILITY. It harvests what every document declares about itself into
`00_META/registers/CORPUS_INDEX.jsonl` -- and then nothing renders it. A JSONL
register is not a place a person can stand and look around.

apu.bot is a WorkFlowy: one infinite document, zoom, collapse, type-to-filter.
That is the reading surface the register has never had. This script is the
bridge, and it is only a bridge.

DISCIPLINE
----------
This renderer RENDERS. It does not infer, score, classify, or edit the corpus.

  * Every seat assignment is copied from the document's own `primary_level`.
    A document with no declared seat is rendered as UNFILED, never guessed into
    a seat.
  * The seven seats' cells are quoted from `38_THE_FULL_ROSETTA_CORRECTED.md`
    section 1. They are not re-derived here.
  * Graves are parsed from the `DF-` table of the claim status register. Their
    verdicts are copied, never re-adjudicated.
  * Counts are measured at run time and printed. Nothing is estimated.

FORMAT CONTRACT (apu.bot `src/lib/markdown.ts`, `importOutlineMarkdown`)
------------------------------------------------------------------------
The first `# ` line is consumed as the root node's title. After that the tree
is bullets only, nested by two-space indentation -- because the importer's
`bulletParentId(0)` returns `"root"` unconditionally, so a bullet can never
become a child of a heading. Headings parent only headings. Using bullets for
the whole tree is therefore the only way to control depth, and it is also
exactly WorkFlowy's own semantics.

`- [ ]` renders a todo, `- [x]` a completed todo. Open loops are todos because
they are work; graves are completed todos because they are work that ended --
archived, never silently erased (E9).

Usage:
    python3 -B 09_TOOLS/01_SCRIPTS/build_apu_outline.py [--out PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "00_META" / "registers" / "CORPUS_INDEX.jsonl"
REGISTER = ROOT / "00_META" / "00_THE_CLAIM_STATUS_REGISTER.md"
OUT_DEFAULT = ROOT / "00_META" / "registers" / "EMERGENTISM_OUTLINE.md"

SEATS = ("L1", "L2", "L3", "L4", "L5", "L6", "L7")

# Quoted from 38_THE_FULL_ROSETTA_CORRECTED.md section 1. Not re-derived.
ROW = {
    "L1": dict(varna="Caṇḍāla", operator="Kali 🎲", g7="kali_take_phi",
               pramana="Pratyakṣa", rep6="— external ground / firewall; no REP6@1 term",
               vmoska="— (outside the letters)", b="→0 (limiting)", inference="dialectical",
               ology="objective-function", regime="tyranny", deploy="yes"),
    "L2": dict(varna="Śūdra", operator="Kālī 💀", g7="kali_take_v",
               pramana="Upamāna", rep6="genotype", vmoska="A · Agents",
               b="½", inference="inductive", ology="epistemology",
               regime="democracy", deploy="yes"),
    "L3": dict(varna="Vaiśya", operator="Kṛṣṇa ◇", g7="krishna_give_v",
               pramana="Anumāna", rep6="epigenotype", vmoska="K · measured triggers",
               b="√3⁄2", inference="deductive", ology="methodology",
               regime="oligarchy", deploy="yes"),
    "L4": dict(varna="Kṣatriya", operator="Arjuna ⚔", g7="arjuna_give_phi",
               pramana="Arthāpatti", rep6="phenotype", vmoska="S · Strategies",
               b="1 (the peak; its own mirror)", inference="abductive",
               ology="axiology", regime="timocracy", deploy="yes"),
    "L5": dict(varna="Brāhmaṇa", operator="Brahmā ○", g7="brahma_create",
               pramana="Śabda", rep6="extended phenotype", vmoska="O · Objectives",
               b="√3⁄2", inference="systematic", ology="ontology",
               regime="aristocracy", deploy="NO — a frame cannot be staffed"),
    "L6": dict(varna="Sādhu", operator="Śiva •", g7="shiva_dissolve",
               pramana="Anupalabdhi", rep6="memotype", vmoska="M · Mission",
               b="½", inference="apophatic", ology="metaphysics",
               regime="anarchy", deploy="NO — a frame cannot be staffed"),
    "L7": dict(varna="Ṛṣi", operator="Viṣṇu ⊙", g7="vishnu_preserve",
               pramana="Pratibhā", rep6="egregoreotype", vmoska="V · Vision",
               b="→0 (limiting)", inference="transcendental", ology="teleology",
               regime="theocracy", deploy="NO — a frame cannot be staffed"),
}

CELL_ORDER = ("varna", "operator", "g7", "pramana", "rep6", "vmoska",
              "b", "inference", "ology", "regime", "deploy")
CELL_LABEL = {"varna": "Varṇa", "operator": "Operator", "g7": "G7@1 cell",
              "pramana": "Pramāṇa", "rep6": "REP6@1", "vmoska": "VMOSK-A [I/C]",
              "b": "B = sin θ", "inference": "Inference", "ology": "-ology",
              "regime": "Regime", "deploy": "Deploy"}

OPEN_LOOP_MARKS = ("UNSIGNED", "STAGED", "PENDING", "BLOCKED", "AWAITING", "UNDISPOSED")


def clean(value, limit: int = 300) -> str:
    """One safe line of bullet content.

    Collapses newlines, strips markers the importer would otherwise read as
    structure, and truncates. A cell that would start a fence, divider, heading
    or todo is neutralised, because content must never become syntax.
    """
    if value is None:
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    text = text.replace("`", "'").replace("```", "'")
    text = re.sub(r"^[-#>\s]+", "", text)          # no leading marker
    if re.fullmatch(r"-{3,}", text):
        text = "(divider)"
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text


def seat_of(row: dict) -> str | None:
    """The seat a document DECLARES, or None. Never inferred."""
    raw = row.get("l_level")
    if not raw:
        return None
    match = re.match(r"\s*\"?\s*(L[1-7])\b", str(raw))
    return match.group(1) if match else None


def label(row: dict) -> str:
    """Best self-description the document offers, in its own words."""
    for key in ("canonical_phrase", "title"):
        if row.get(key):
            return clean(row[key])
    return clean(Path(row["path"]).stem.replace("_", " "))


def tier_badge(row: dict) -> str:
    tiers = row.get("tiers") or []
    return " ".join(f"[{t.strip('[]')}]" for t in tiers[:3]) if tiers else ""


def is_open_loop(row: dict) -> bool:
    status = (row.get("status") or "").upper()
    return any(mark in status for mark in OPEN_LOOP_MARKS)


def parse_graves() -> list[tuple[str, str, str, str]]:
    """(id, claim, verdict, successor) rows from the register's DF- table."""
    if not REGISTER.exists():
        return []
    graves = []
    for line in REGISTER.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        ident = cells[0].strip("`* ")
        if not re.fullmatch(r"DF-\d+", ident):
            continue
        graves.append((ident, clean(cells[1], 120), clean(cells[2], 60),
                       clean(cells[4] if len(cells) > 4 else "", 140)))
    return graves


def build(rows: list[dict]) -> tuple[list[str], dict]:
    out: list[str] = ["# Emergentism", ""]
    w = out.append

    by_seat: dict[str, list[dict]] = defaultdict(list)
    unfiled: list[dict] = []
    for row in rows:
        seat = seat_of(row)
        (by_seat[seat] if seat else unfiled).append(row)

    graves = parse_graves()
    loops = [r for r in rows if is_open_loop(r)]
    unfindable = [r for r in rows
                  if not r.get("canonical_phrase") and not r.get("tiers")]

    stats = dict(total=len(rows), filed=sum(len(v) for v in by_seat.values()),
                 unfiled=len(unfiled), graves=len(graves), loops=len(loops),
                 unfindable=len(unfindable),
                 per_seat={s: len(by_seat.get(s, [])) for s in SEATS})

    # ---- the frame -------------------------------------------------------
    w("- •  ⊙  ○ — the frame")
    w("  - A Titan is a seat in the vocabulary you use to talk about a boundary, held at a different level from everything it talks about.")
    w("  - ArithmeticSignature(TitanFrame) = the empty set. A frame is never an operand.")
    w("  - V · M · O are the three Titan-frame projections, and exactly the three seats that cannot be deployed.")
    w("  - S · K · A are the three deployable operators inside the realm.")
    w("  - L1 carries no VMOSK-A letter. The off-by-one between six letters and seven seats is the firewall.")
    w("  - Read the display as interval notation: lower bound | realm | upper bound. Inserting an operator between the marks destroys it.")

    # ---- the seven seats -------------------------------------------------
    w("- The seven seats")
    w(f"  - {stats['filed']} of {stats['total']} live documents declare a seat. The rest are unfiled below, never guessed into one.")
    for seat in SEATS:
        docs = sorted(by_seat.get(seat, []), key=lambda r: (r.get("lane") or "", r["path"]))
        cells = ROW[seat]
        w(f"  - {seat} · {cells['varna']} · {cells['operator']} · {cells['ology']} — {len(docs)} documents")
        w("    - cells, quoted from 38 section 1")
        for key in CELL_ORDER:
            w(f"      - {CELL_LABEL[key]} — {clean(cells[key])}")
        if not docs:
            w("    - no document declares this seat")
            continue
        w(f"    - documents filed here ({len(docs)})")
        by_lane: dict[str, list[dict]] = OrderedDict()
        for row in docs:
            by_lane.setdefault(row.get("lane") or "(root)", []).append(row)
        for lane, lane_docs in by_lane.items():
            w(f"      - {clean(lane)} ({len(lane_docs)})")
            for row in lane_docs:
                badge = tier_badge(row)
                suffix = f" {badge}" if badge else ""
                w(f"        - {label(row)} — {clean(row['path'], 200)}{suffix}")

    # ---- unfiled ---------------------------------------------------------
    w(f"- Unfiled — {len(unfiled)} documents declare no seat")
    w("  - Absence of metadata is reported as absence. Nothing here is guessed into a seat.")
    lanes = Counter(r.get("lane") or "(root)" for r in unfiled)
    for lane, count in lanes.most_common():
        lane_docs = sorted((r for r in unfiled if (r.get("lane") or "(root)") == lane),
                           key=lambda r: r["path"])
        w(f"  - {clean(lane)} ({count})")
        for row in lane_docs:
            badge = tier_badge(row)
            suffix = f" {badge}" if badge else ""
            w(f"    - {label(row)} — {clean(row['path'], 200)}{suffix}")

    # ---- open loops ------------------------------------------------------
    w(f"- Open loops — {len(loops)} documents declare themselves unsettled")
    w("  - An unclosed loop is the mechanism by which a cone fills with phantoms that cannot be seen from inside it.")
    for row in sorted(loops, key=lambda r: r["path"]):
        w(f"  - [ ] {label(row)} — {clean(row['path'], 200)} — {clean(row.get('status'), 120)}")

    # ---- the graves ------------------------------------------------------
    w(f"- The graves — {len(graves)} refuted claims, archived and never erased")
    w("  - Kills fire in public. The dead are archived, never silently erased (E9).")
    w("  - A grave never returns as the claim it was. Only a named weaker successor, or a new RQ row.")
    for ident, claim, verdict, successor in graves:
        tail = f" — successor: {successor}" if successor else ""
        w(f"  - [x] {ident} · {claim} — {verdict}{tail}")

    # ---- the findability gap --------------------------------------------
    w(f"- The findability gap — {len(unfindable)} documents carry neither a canonical phrase nor a tier")
    w("  - The corpus's failure mode is not falsity. It is unfindability: the knowledge is written down, and being written down does not stop the next reader from re-deriving it.")
    for row in sorted(unfindable, key=lambda r: r["path"])[:400]:
        w(f"  - [ ] {clean(row['path'], 200)}")
    if len(unfindable) > 400:
        w(f"  - {len(unfindable) - 400} further unfindable documents not listed here — raise the cap in the renderer to see them all")

    return out, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, default=INDEX)
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()

    if not args.index.exists():
        print(f"index not found: {args.index}\nrun build_corpus_index.py first",
              file=sys.stderr)
        return 2

    rows = [json.loads(line) for line in
            args.index.read_text(encoding="utf-8").splitlines() if line.strip()]
    rows = [r for r in rows if r.get("path")]

    lines, stats = build(rows)
    text = "\n".join(lines).rstrip() + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")

    print(f"documents rendered      {stats['total']:5d}")
    print(f"  filed at a seat       {stats['filed']:5d}")
    for seat in SEATS:
        print(f"    {seat}                  {stats['per_seat'][seat]:5d}")
    print(f"  unfiled               {stats['unfiled']:5d}")
    print(f"open loops (todo)       {stats['loops']:5d}")
    print(f"graves (done)           {stats['graves']:5d}")
    print(f"unfindable              {stats['unfindable']:5d}")
    print(f"\nwritten: {args.out.relative_to(ROOT)}  "
          f"({len(text):,} bytes, {len(lines):,} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
