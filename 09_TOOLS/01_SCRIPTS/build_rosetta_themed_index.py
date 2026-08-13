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

# Reader-facing names. The public surface names a reading, never a file path.
# Provenance stays in the corpus catalogue and in the title= attribute.
SOURCE_LABEL = {
    "D_SERIES_ROWS/00_GENERATIVE_TABLE.md": "The generative table",
    "D_SERIES_DOMAINS/D32_MATHEMATICS.md": "The chart",
    "D_SERIES_ROWS/D22_ROSETTA_R13_HEXAGRAM.md": "Hexagram",
    "00_THE_SEVEN_OLOGIES_PER_THE_ROSETTA.md": "The seven questions",
    "D_SERIES_DOMAINS/D30_SOCIAL_POLITICAL.md": "Regimes and governance",
    "16_PLATO_LAKOTA_NEUROSCIENCE_2026_04_25.md": "Plato, Lakota, brain",
    "ROSETTA_REPLICATOR.md": "Replicator layers",
    "04_BALANCE_OF_HOUSES_TROPHIC_COEVOLUTION_CONTRACT.md": "Ecological cascade",
    "D_SERIES_DOMAINS/D24_PSYCHOLOGY.md": "Developmental psychology",
    "ROSETTA_PSYCHOLOGY.md": "Psychology, second reading",
    "D_SERIES_DOMAINS/D25_NEUROSCIENCE.md": "Neuroscience",
    "ROSETTA_NEUROSCIENCE.md": "Neuroscience, second reading",
    "D_SERIES_DOMAINS/D26_COMPUTATION.md": "Computation",
    "ROSETTA_COMPUTATION.md": "Computation, second reading",
    "D_SERIES_DOMAINS/D27_GAME_THEORY.md": "Game theory",
    "D_SERIES_DOMAINS/D28_MYTHOLOGY.md": "Mythology",
    "ROSETTA_MYTHOLOGY.md": "Mythology, second reading",
    "ROSETTA_MUSIC.md": "Music",
    "D_SERIES_ROWS/D24_ROSETTA_R14_PIE_COMPARATIVE_LINGUISTICS.md": "Proto-Indo-European",
    "D_SERIES_DOMAINS/D29_SPIRITUAL.md": "Contemplative practice",
    "00_THREE_NON_WESTERN_TRADITIONS_AND_THE_L_LEVELS.md": "Sufi and Chinese stages",
    "05_NON_WEIRD_SWEEP_2026_04_25.md": "Bhūmi stages",
    "10_INDIGENOUS_AMERICAN_AND_TAHITIAN_2026_04_25.md": "Aztec and Tahitian readings",
    "ROSETTA_INDIGENOUS_AMERICAN.md": "Lakota rites",
    "D_SERIES_DOMAINS/D31_CIVILISATIONAL.md": "Civilisational stages",
    "ROSETTA_CIVILISATIONAL.md": "Civilisation, second reading",
    "07_MIRROR_SYMMETRY_FALSIFICATION_TEST_2026_04_25.md": "The mirror test",
    "08_MIRROR_TEST_EXTENSION_AND_FAILED_MAPPINGS_2026_04_25.md": "The mirror test, extended",
    "17_CELL_AUDIT_PSYCHOLOGY_2026_04_25.md": "Psychology cell audit",
}

# seat -> (varṇa, B label, mirror partner or None, hue token)
SEAT_META = OrderedDict([
    ("L1", ("Caṇḍāla", "0", "L7", "m1")),
    ("L2", ("Śūdra", "0.5", "L6", "m2")),
    ("L3", ("Vaiśya", "√3⁄2", "L5", "m3")),
    ("L4", ("Kṣatriya", "1", None, "gold")),
    ("L5", ("Brāhmaṇa", "√3⁄2", "L3", "m3")),
    ("L6", ("Sādhu", "0.5", "L2", "m2")),
    ("L7", ("Ṛṣi", "0", "L1", "m1")),
])

# Columns that grade the mapping become a badge on the reading, not a row of data.
TIER_COLUMNS = {"mapping tier", "rigor", "standing", "verdict", "weight", "strength"}
# Redundant in the seat view — the rail already shows the pairing.
SEAT_VIEW_DROP = {"mirror partner"}


def hesc(v) -> str:
    if not v:
        return "—"
    return v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def label_of(fname: str) -> str:
    return SOURCE_LABEL.get(fname, fname.rsplit("/", 1)[-1].replace(".md", ""))


def _dome_path() -> str:
    import math
    pts = []
    for i in range(0, 109):
        t = i / 108
        x = 70 + t * 540
        y = 130 - 90 * math.sin(math.pi * t)
        pts.append(f"{x:.1f},{y:.1f}")
    return "M" + "L".join(pts)


def _seat_xy(idx: int) -> tuple[float, float]:
    import math
    t = idx / 6
    return 70 + t * 540, 130 - 90 * math.sin(math.pi * t)


ROSETTA_CSS = """
.rstone{margin:0 0 1.4rem}
.rstone .rail{width:100%;max-width:680px;margin:0 auto .4rem;display:block}
.rstone .nseat{cursor:pointer}
.rstone .nseat circle{transition:r .18s ease,fill-opacity .18s ease}
.rstone .nseat:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.rstone .nlab{font-family:var(--mono);font-size:11px;fill:var(--bone-ghost);letter-spacing:.1em}
.rstone .nseat.is-active .nlab{fill:var(--bone)}
.rstone .nseat.is-mirror .nlab{fill:var(--bone-dim)}
.rstone .railhint{font-family:var(--mono);font-size:10px;fill:var(--bone-ghost);letter-spacing:.18em;text-transform:uppercase}
.rstone .pane{display:none}
.rstone .pane.is-on{display:block}
.rstone .seathead{display:flex;align-items:baseline;gap:.9rem;flex-wrap:wrap;
  padding:.9rem 0 .7rem;border-bottom:1px solid var(--line)}
.rstone .sglyph{font-family:var(--mono);font-size:1.5rem;letter-spacing:.16em;font-weight:500}
.rstone .svarna{font-size:1.9rem;font-weight:200;letter-spacing:-.02em;margin:0;color:var(--bone)}
.rstone .smeta{font-family:var(--mono);font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--bone-ghost);margin:0 0 0 auto}
.rstone .reg{padding:1.1rem 0;border-bottom:1px solid var(--line-soft)}
.rstone .regname{font-family:var(--mono);font-size:.66rem;letter-spacing:.24em;
  text-transform:uppercase;color:var(--gold-deep);margin:0 0 .7rem}
.rstone .src{margin:0 0 .9rem}
.rstone .srcname{font-size:.86rem;color:var(--bone);margin:0 0 .25rem;font-weight:500}
.rstone .tier{font-family:var(--mono);font-size:.62rem;letter-spacing:.1em;color:var(--bone-ghost);
  border:1px solid var(--line);border-radius:2px;padding:.05rem .3rem;margin-left:.4rem}
.rstone dl{display:grid;grid-template-columns:minmax(8.5rem,auto) 1fr;gap:.18rem .9rem;margin:0}
.rstone dt{font-family:var(--mono);font-size:.7rem;letter-spacing:.06em;color:var(--bone-ghost);
  text-transform:lowercase;padding-top:.12rem}
.rstone dd{margin:0;color:var(--bone-dim);font-size:.92rem;font-weight:300}
@media (max-width:640px){
  .rstone dl{grid-template-columns:1fr;gap:0 0}
  .rstone dt{margin-top:.4rem}
  .rstone .smeta{margin:.3rem 0 0}
}
@media (prefers-reduced-motion:reduce){.rstone .nseat circle{transition:none}}
"""


def render_html(records: list[dict]) -> str:
    withheld = 0
    kept: list[dict] = []
    for r in records:
        if r["column"].strip().lower() in PUBLIC_WITHHELD_COLUMNS:
            withheld += 1
            continue
        kept.append(r)

    out: list[str] = []
    w = out.append
    w("<!-- ROSETTA-CATALOGUE:START -->")
    w(f"    <style>{ROSETTA_CSS}    </style>")
    w('    <div class="rstone reveal" id="rstone" data-seat="L4">')

    # --- the rail: height is balance -------------------------------------
    w('      <svg class="rail" viewBox="0 0 680 168" role="tablist" '
      'aria-label="Choose a seat to read across every domain">')
    w(f'        <path d="{_dome_path()}" fill="none" stroke="var(--line)" stroke-width="1"/>')
    w('        <line x1="70" y1="130" x2="610" y2="130" stroke="var(--line-soft)" stroke-width="1"/>')
    w('        <line class="mlink" x1="0" y1="0" x2="0" y2="0" stroke="var(--line)" '
      'stroke-width="1" stroke-dasharray="3 4" opacity="0"/>')
    for i, (seat, (varna, b, mirror, hue)) in enumerate(SEAT_META.items()):
        x, y = _seat_xy(i)
        w(f'        <g class="nseat" data-seat="{seat}" data-x="{x:.1f}" data-y="{y:.1f}" '
          f'role="tab" tabindex="0" aria-label="{seat}, {varna}, balance {b}">')
        w(f'          <circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="var(--{hue})" fill-opacity=".35"/>')
        w(f'          <text class="nlab" x="{x:.1f}" y="154" text-anchor="middle">{seat}</text>')
        w('        </g>')
    w('        <text class="railhint" x="340" y="16" text-anchor="middle">height is balance</text>')
    w('      </svg>')

    # --- one pane per seat -----------------------------------------------
    for seat, (varna, b, mirror, hue) in SEAT_META.items():
        on = " is-on" if seat == "L4" else ""
        mtxt = f"mirrors {mirror}" if mirror else "no mirror · the equator"
        w(f'      <div class="pane{on}" data-seat="{seat}" role="tabpanel" aria-label="{seat} {varna}">')
        w('        <div class="seathead">')
        w(f'          <span class="sglyph" style="color:var(--{hue})">{seat}</span>')
        w(f'          <h3 class="svarna">{hesc(varna)}</h3>')
        w(f'          <p class="smeta">B = {b} · {mtxt}</p>')
        w('        </div>')

        for key, title in THEMES.items():
            if key == "audit":
                continue
            recs = [r for r in kept if theme_of(r) == key]
            by_file: dict[str, list[dict]] = OrderedDict()
            for r in recs:
                by_file.setdefault(r["file"], []).append(r)
            block: list[str] = []
            for fname, cols in by_file.items():
                pairs, badge = [], None
                for c in cols:
                    cname = c["column"].strip().lower()
                    val = c["cells"][seat]
                    if not val:
                        continue
                    if cname in TIER_COLUMNS:
                        badge = val
                        continue
                    if cname in SEAT_VIEW_DROP:
                        continue
                    pairs.append((c["column"], val))
                if not pairs:
                    continue
                block.append(f'          <div class="src">')
                block.append(f'            <p class="srcname" title="{hesc(fname)}">'
                             f'{hesc(label_of(fname))}'
                             + (f'<span class="tier">{hesc(badge)}</span>' if badge else '')
                             + '</p>')
                block.append('            <dl>')
                for k, v in pairs:
                    block.append(f'              <dt>{hesc(k)}</dt><dd>{hesc(v)}</dd>')
                block.append('            </dl>')
                block.append('          </div>')
            if block:
                short = title.split("·", 1)[1].split("—")[0].strip() if "·" in title else title
                w('        <section class="reg">')
                w(f'          <p class="regname">{hesc(short)}</p>')
                out.extend(block)
                w('        </section>')
        w('      </div>')

    w('    </div>')
    w("""    <script>
    (function(){
      var root=document.getElementById('rstone'); if(!root) return;
      var tabs=[].slice.call(root.querySelectorAll('.nseat'));
      var panes=[].slice.call(root.querySelectorAll('.pane'));
      var link=root.querySelector('.mlink');
      var pairs={L1:'L7',L2:'L6',L3:'L5',L5:'L3',L6:'L2',L7:'L1'};
      function pick(seat){
        root.dataset.seat=seat;
        panes.forEach(function(p){p.classList.toggle('is-on',p.dataset.seat===seat);});
        var m=pairs[seat]||null, a=null, bnode=null;
        tabs.forEach(function(t){
          var s=t.dataset.seat, act=s===seat, mir=s===m;
          t.classList.toggle('is-active',act); t.classList.toggle('is-mirror',mir);
          t.setAttribute('aria-selected',act?'true':'false');
          t.setAttribute('tabindex',act?'0':'-1');
          var c=t.querySelector('circle');
          c.setAttribute('r',act?8:(mir?6:5));
          c.setAttribute('fill-opacity',act?'1':(mir?'.7':'.35'));
          if(act)a=t; if(mir)bnode=t;
        });
        if(a&&bnode){
          link.setAttribute('x1',a.dataset.x);link.setAttribute('y1',a.dataset.y);
          link.setAttribute('x2',bnode.dataset.x);link.setAttribute('y2',bnode.dataset.y);
          link.setAttribute('opacity','1');
        } else { link.setAttribute('opacity','0'); }
      }
      tabs.forEach(function(t,i){
        t.addEventListener('click',function(){pick(t.dataset.seat);});
        t.addEventListener('keydown',function(e){
          if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(t.dataset.seat);}
          if(e.key==='ArrowRight'||e.key==='ArrowLeft'){
            e.preventDefault();
            var n=tabs[(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length];
            n.focus();pick(n.dataset.seat);
          }
        });
      });
      pick('L4');
    })();
    </script>""")
    w("<!-- ROSETTA-CATALOGUE:END -->")
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
