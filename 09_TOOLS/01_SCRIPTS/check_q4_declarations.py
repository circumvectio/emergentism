#!/usr/bin/env python3
"""Assert that ruling Q4's route declarations are still on the pages they govern.

WHY THIS EXISTS — a signed ruling was silently reverted and the gate said nothing.

On 2026-07-31 ruling Q4 (receipt 193, executed in receipt 232) put a visible declaration
on five routes: four DECLARED-PROVISIONAL and one INFRASTRUCTURE. The declarations were
written into the HTML by hand. But `12_PUBLIC_SITE/build_pwa.py` OWNS `offline/index.html`
and rewrites it wholesale, so the very next run of that script deleted the INFRASTRUCTURE
declaration.

The gate did not catch it. It failed — but only on `sw.js`'s content hash and a stale
social card, both derived artifacts whose error messages tell you to run a rebuild. Run
those two rebuilds and the gate returns PASS with the ruling reverted and no trace.

That is the failure this repository has already written down as forbidden: never build a
gate that can pass a property it does not test. So this checker tests the property.

WHAT IT CHECKS, AND WHAT IT DOES NOT
  · that each governed route still carries its declaration text and its robots meta
  · that the four provisional routes are `index, follow` and `/offline/` is `noindex`
  · that `build_pwa.py`'s own template still contains the declaration it must emit —
    because checking only the OUTPUT would pass right up until someone regenerates it
It does NOT check what a live host returns. Headers are `vercel.json`'s job and are only
observable against the deployed domain.

Usage: python3 check_q4_declarations.py   (no arguments — gate.sh invokes it bare)
"""

from __future__ import annotations

import html as html_lib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "12_PUBLIC_SITE"

# route -> (expected status token, expected robots directive)
GOVERNED = {
    "amrita": ("DECLARED-PROVISIONAL", "index, follow"),
    "egg": ("DECLARED-PROVISIONAL", "index, follow"),
    "riemann": ("DECLARED-PROVISIONAL", "index, follow"),
    "suda": ("DECLARED-PROVISIONAL", "index, follow"),
    "offline": ("INFRASTRUCTURE", "noindex, follow"),
}

# Generators that OWN a governed route's file. Editing the output alone is not durable:
# the next run of the generator wins. The generator's source must carry the declaration.
OWNED_BY_GENERATOR = {
    "amrita": SITE / "build_churning.py",
    "offline": SITE / "build_pwa.py",
}

RECEIPT = "11_UPLINK/50_AUDITS_AND_EXECUTIONS/232_FIVE_RULINGS_EXECUTED_2026_07_31.md"


def main() -> int:
    problems: list[str] = []
    checked = 0

    for route, (token, robots) in GOVERNED.items():
        page = SITE / route / "index.html"
        if not page.exists():
            problems.append(f"{route}/index.html is missing entirely")
            continue
        html = page.read_text(encoding="utf-8", errors="replace")
        declaration_text = html_lib.unescape(html)
        for dash in "‐‑‒–—−":
            declaration_text = declaration_text.replace(dash, "-")
        checked += 1

        if "q4decl" not in html:
            problems.append(
                f"/{route}/ has lost its ruling-Q4 declaration block (no .q4decl element). "
                f"If a generator overwrote it, fix the GENERATOR, not the output."
            )
        elif token not in declaration_text:
            problems.append(
                f"/{route}/ has a declaration block but not the '{token}' status word"
            )

        m = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
        if not m:
            problems.append(f"/{route}/ has no robots meta; Q4 requires '{robots}'")
        elif m.group(1).strip().lower() != robots:
            problems.append(
                f"/{route}/ robots is '{m.group(1).strip()}' but Q4 declared '{robots}'"
            )

    for route, gen in OWNED_BY_GENERATOR.items():
        if not gen.exists():
            problems.append(f"generator {gen.name} for /{route}/ is missing")
            continue
        src = gen.read_text(encoding="utf-8", errors="replace")
        token = GOVERNED[route][0]
        if "q4decl" not in src or token not in src:
            problems.append(
                f"{gen.name} OWNS /{route}/index.html but its template no longer emits the "
                f"Q4 '{token}' declaration. The page on disk may look correct right now and "
                f"will lose the declaration the next time this script runs."
            )

    if problems:
        print("Q4 DECLARATIONS: FAIL")
        for p in problems:
            print(f"- {p}")
        print(f"  authority: {RECEIPT}")
        return 1

    print(
        f"Q4 DECLARATIONS: PASS ({checked} governed routes carry their declaration and "
        f"robots directive; {len(OWNED_BY_GENERATOR)} owning generator verified)"
    )
    print(
        "  scope: proves the declarations are in the SOURCE and in the generators that own "
        "it. It does not prove what the live host returns — that is vercel.json's job and "
        "is only checkable against the deployed domain."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
