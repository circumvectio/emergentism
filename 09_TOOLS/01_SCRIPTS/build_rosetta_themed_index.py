#!/usr/bin/env python3
"""Render the full themed Rosetta from the harvested column ledger.

Cells are copied from the harvest; nothing here re-reads or re-interprets a
source table. The ONLY authored content is the theme assignment in THEME_BY_FILE
and META_COLUMNS, which is an [S] selection and is declared as such in the
output.

Usage:
    python3 harvest_rosetta_columns.py --out cols.jsonl
    python3 build_rosetta_themed_index.py --ledger cols.jsonl --out 37_....md
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import OrderedDict
from pathlib import Path

# --- authored [S] selection -------------------------------------------------

THEMES = OrderedDict([
    ("spine",        "I · The spine — the native seats and their operators"),
    ("formal",       "II · The chart — angle, reciprocal coordinates, balance"),
    ("epistemic",    "III · Knowing — pramāṇa, discipline, question"),
    ("governance",   "IV · Governance — regime, varṇa, economy"),
    ("life",         "V · Life — replicator layers and ecological cascade"),
    ("mind",         "VI · Mind — development, virtue, brain"),
    ("strategy",     "VII · Strategy — computation and game theory"),
    ("symbol",       "VIII · Symbol — myth, language, music"),
    ("practice",     "IX · Practice — contemplative and initiatory traditions"),
    ("civilisation", "X · Civilisation — long-horizon reading"),
    ("audit",        "XI · The audit apparatus — columns that grade the mapping"),
])

THEME_BY_FILE = {
    "D_SERIES_ROWS/00_GENERATIVE_TABLE.md": "spine",
    "ROSETTA_REPLICATOR.md": "life",
    "04_BALANCE_OF_HOUSES_TROPHIC_COEVOLUTION_CONTRACT.md": "life",
    "D_SERIES_DOMAINS/D32_MATHEMATICS.md": "formal",
    "D_SERIES_ROWS/D22_ROSETTA_R13_HEXAGRAM.md": "formal",
    "00_THE_SEVEN_OLOGIES_PER_THE_ROSETTA.md": "epistemic",
    "D_SERIES_DOMAINS/D30_SOCIAL_POLITICAL.md": "governance",
    "16_PLATO_LAKOTA_NEUROSCIENCE_2026_04_25.md": "governance",
    "D_SERIES_DOMAINS/D24_PSYCHOLOGY.md": "mind",
    "D_SERIES_DOMAINS/D25_NEUROSCIENCE.md": "mind",
    "ROSETTA_PSYCHOLOGY.md": "mind",
    "ROSETTA_NEUROSCIENCE.md": "mind",
    "D_SERIES_DOMAINS/D26_COMPUTATION.md": "strategy",
    "D_SERIES_DOMAINS/D27_GAME_THEORY.md": "strategy",
    "ROSETTA_COMPUTATION.md": "strategy",
    "D_SERIES_DOMAINS/D28_MYTHOLOGY.md": "symbol",
    "ROSETTA_MYTHOLOGY.md": "symbol",
    "ROSETTA_MUSIC.md": "symbol",
    "D_SERIES_ROWS/D24_ROSETTA_R14_PIE_COMPARATIVE_LINGUISTICS.md": "symbol",
    "D_SERIES_DOMAINS/D29_SPIRITUAL.md": "practice",
    "00_THREE_NON_WESTERN_TRADITIONS_AND_THE_L_LEVELS.md": "practice",
    "05_NON_WEIRD_SWEEP_2026_04_25.md": "practice",
    "10_INDIGENOUS_AMERICAN_AND_TAHITIAN_2026_04_25.md": "practice",
    "ROSETTA_INDIGENOUS_AMERICAN.md": "practice",
    "D_SERIES_DOMAINS/D31_CIVILISATIONAL.md": "civilisation",
    "ROSETTA_CIVILISATIONAL.md": "civilisation",
    "07_MIRROR_SYMMETRY_FALSIFICATION_TEST_2026_04_25.md": "audit",
    "08_MIRROR_TEST_EXTENSION_AND_FAILED_MAPPINGS_2026_04_25.md": "audit",
    "17_CELL_AUDIT_PSYCHOLOGY_2026_04_25.md": "audit",
}

# Columns that grade a mapping rather than describe a world, wherever they appear.
META_COLUMNS = {
    "mapping tier", "rigor", "standing", "verdict", "weight", "strength",
    "mirror partner", "cell",
}

# Columns that belong to the spine wherever they appear.
SPINE_COLUMNS = {"operator", "operator projection", "stable source key", "projected g7 symbol"}
FORMAL_COLUMNS = {
    "colatitude", "phi/nu ratio", "θ", "θ/2", "b = sin θ", "angle",
    "φ = cot(θ/2)", "ν = tan(θ/2)",
}

# Never harvest the index into itself.
EXCLUDE_FILES = {"36_THE_ROSETTA_IN_THEMES_2026_08_13.md"}

SEATS = [f"L{i}" for i in range(1, 8)]


def theme_of(rec: dict) -> str:
    col = rec["column"].strip().lower()
    if col in META_COLUMNS:
        return "audit"
    if col in SPINE_COLUMNS:
        return "spine"
    if col in FORMAL_COLUMNS:
        return "formal"
    return THEME_BY_FILE.get(rec["file"], "audit")


def esc(v):
    if not v:
        return "—"
    return v.replace("|", "\\|")


def render(records: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {k: [] for k in THEMES}
    for r in records:
        grouped[theme_of(r)].append(r)

    total = len(records)
    files = sorted({r["file"] for r in records})
    out: list[str] = []
    w = out.append

    w("---")
    w("rosetta:")
    w("  primary_level: L3")
    w("  primary_column: Meta")
    w('  operator: "Kṛṣṇa ◇"')
    w('  tier: "Audit"')
    w('  regime: "Vaiśya"')
    w('  register: "[S]"')
    w('  canonical_phrase: "The full Rosetta — every harvested L1-L7 column, grouped'
      ' into eleven themes (generated catalogue; grouping selected, cells interpretive)"')
    w("  d_register: 4")
    w('title: "The Full Rosetta, Grouped in Themes"')
    w('status: "ACTIVE — GENERATED CATALOGUE. Do not hand-edit; re-run the two scripts'
      ' named below. It creates no mapping and promotes no cell."')
    w("date: 2026-08-13")
    w('evidence_tier: "[S] the eleven-theme grouping; [B] the harvest is mechanical and'
      ' re-runnable; [I] inherited unchanged on every cross-domain cell"')
    w('owner: "Subordinate to 00_THE_MASTER_ROSETTA.md. Where this catalogue and a source'
      ' table differ, the source table governs and this file is the defect."')
    w("parents:")
    w("  - 00_THE_MASTER_ROSETTA.md")
    w("  - 36_THE_ROSETTA_IN_THEMES_2026_08_13.md")
    w("  - D_SERIES_ROWS/00_GENERATIVE_TABLE.md")
    w("---\n")
    w("# The Full Rosetta, Grouped in Themes\n")
    w("> **Generated.** Every cell below was copied by")
    w("> `09_TOOLS/01_SCRIPTS/harvest_rosetta_columns.py` from a markdown table in")
    w("> the Rosetta lane keyed `L1`–`L7`, and rendered by")
    w("> `09_TOOLS/01_SCRIPTS/build_rosetta_themed_index.py`. **Do not hand-edit —")
    w("> re-run the two scripts.** A missing seat is rendered `—`; no cell is inferred.\n")
    w(f"**{total} columns** harvested from **{len(files)} files**, grouped into")
    w(f"**{len(THEMES)} themes**. The grouping is `[S]` — an authored selection living in")
    w("`THEME_BY_FILE`. Every *cell* keeps the tier its source gave it, and the")
    w("source's tier column travels with it in theme XI where one exists.\n")
    w("---\n")
    w("## The three lines, before any table\n")
    w("1. **The geometry is `[A]`, given the selection.** `B = sin θ`;")
    w("   `B(θ)=B(π−θ)` forces palindromic pairing, `L4` is the unique argmax,")
    w("   the extremes go to `0`. Identities, not findings.")
    w("2. **The count is `[S]`, selected — not derived.** 3, 5 or 9 stations satisfy")
    w("   every symmetry in line 1 equally well.")
    w("3. **Every cross-domain cell below is `[I]`.** It inherits neither the truth")
    w("   nor the evidence tier of the domain it came from.\n")
    w("**Varṇa and regime are attributed historical analogies, never classes of human")
    w("worth, and never assigned by birth** (`KSC-24`, `KSC-25`).\n")
    w("---\n")

    for key, title in THEMES.items():
        recs = grouped[key]
        if not recs:
            continue
        w(f"## {title}\n")
        w(f"*{len(recs)} columns.*\n")
        by_file: dict[str, list[dict]] = OrderedDict()
        for r in recs:
            by_file.setdefault(r["file"], []).append(r)
        for fname, cols in by_file.items():
            w(f"**`{fname}`**\n")
            for chunk_start in range(0, len(cols), 5):
                chunk = cols[chunk_start:chunk_start + 5]
                w("| seat | " + " | ".join(esc(c["column"]) for c in chunk) + " |")
                w("|---|" + "---|" * len(chunk))
                for s in SEATS:
                    w(f"| `{s}` | " + " | ".join(esc(c["cells"][s]) for c in chunk) + " |")
                w("")
        w("---\n")

    w("## Kills\n")
    w("| claim | what refutes it |")
    w("|---|---|")
    w("| this document matches the lane | re-run both scripts; any diff is a defect here |")
    w("| the harvest is complete | exhibit an `L1`–`L7` markdown table in the lane absent from the ledger |")
    w("| no cell was inferred | exhibit a cell here that is not verbatim in its source table |")
    w("| the grouping is `[S]` and nothing more | show a theme assignment that changes what a cell claims |")
    return "\n".join(out) + "\n"


# Columns carrying venture/product vocabulary. They stay in the corpus catalogue
# (provenance) but are withheld from the public projection, which is pure
# worldview: "Product, venture, company, runtime, and external-governance
# systems are neither premises nor authorities here."
PUBLIC_WITHHELD_COLUMNS = {"helios product"}


def hesc(v) -> str:
    if not v:
        return "—"
    return (v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_html(records: list[dict]) -> str:
    grouped: dict[str, list[dict]] = {k: [] for k in THEMES}
    withheld = 0
    for r in records:
        if r["column"].strip().lower() in PUBLIC_WITHHELD_COLUMNS:
            withheld += 1
            continue
        grouped[theme_of(r)].append(r)

    total = sum(len(v) for v in grouped.values())
    out: list[str] = []
    w = out.append
    w('    <details class="comparative-appendix reveal" style="margin-top:1.6rem">')
    w(f'      <summary>Open the full themed catalogue — {total} columns, '
      f'{len(THEMES)} themes [I]</summary>')
    w('      <div class="comparative-body">')
    w('        <p class="symbolic-fence"><b>Every cell below is interpretive.</b> '
      'Each column is a directional projection into the seven seats, copied verbatim '
      'from its source table and carrying neither the truth nor the evidence tier of '
      'the domain it came from. Columns are grouped by an authored selection; the '
      'grouping changes no cell. Varṇa and regime are attributed historical analogies, '
      'never classes of human worth and never assigned by birth.'
      + (f' {withheld} column(s) carrying venture vocabulary are withheld from this '
         'public projection and remain in the source lane.' if withheld else '') +
      '</p>')
    for key, title in THEMES.items():
        recs = grouped[key]
        if not recs:
            continue
        w(f'        <h3 style="margin:1.8rem 0 .4rem;font-weight:500">{hesc(title)}</h3>')
        by_file: dict[str, list[dict]] = OrderedDict()
        for r in recs:
            by_file.setdefault(r["file"], []).append(r)
        for fname, cols in by_file.items():
            w(f'        <p class="pk" style="margin:.9rem 0 .3rem">{hesc(fname)}</p>')
            for start in range(0, len(cols), 5):
                chunk = cols[start:start + 5]
                w('        <div class="tblwrap"><table style="min-width:0">')
                w('          <thead><tr><th>seat</th>'
                  + "".join(f"<th>{hesc(c['column'])}</th>" for c in chunk)
                  + '</tr></thead>')
                w('          <tbody>')
                for s in SEATS:
                    w(f'            <tr><td class="level">{s}</td>'
                      + "".join(f"<td>{hesc(c['cells'][s])}</td>" for c in chunk)
                      + '</tr>')
                w('          </tbody></table></div>')
    w('      </div>')
    w('    </details>')
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--html", action="store_true",
                    help="emit the public HTML fragment instead of the corpus markdown")
    args = ap.parse_args()

    records = [json.loads(l) for l in args.ledger.open(encoding="utf-8")]
    records = [r for r in records if r["file"] not in EXCLUDE_FILES]
    text = render_html(records) if args.html else render(records)

    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out} ({len(text):,} bytes, {len(records)} columns)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
