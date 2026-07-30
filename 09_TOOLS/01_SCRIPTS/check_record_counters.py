#!/usr/bin/env python3
"""Guard the /record/ readout against the drift that has now happened three times.

The page computes its three counters from the ledger rows at load:
    put('c-tested',  rows.length)
    put('c-against', cut + refuted + retracted)
    put('c-fenced',  fenced)
The static `data-count` attributes are the no-JS fallback. Every time a row is added
they go stale, and a reader without JavaScript sees a different, smaller, flattering
number than a reader with it. It drifted to 12|12|0 while the runtime said 27|16|7, and
twice more the same day while rows were being added.

This recomputes the JS tally from the HTML and requires the static values to match.
Exits 0 on agreement, 1 otherwise.
"""
from __future__ import annotations
import re, sys
from collections import Counter
from pathlib import Path

PAGE = Path(__file__).resolve().parents[2] / "12_PUBLIC_SITE" / "record" / "index.html"
AGAINST = ("cut", "refuted", "retracted")


def main() -> int:
    if not PAGE.exists():
        print("RECORD COUNTERS: FAIL\n- 12_PUBLIC_SITE/record/index.html is missing")
        return 1
    html = PAGE.read_text(encoding="utf-8")

    # rows the JS counts: every article.case that is not the reserved placeholder
    # Rows carry extra classes — "case v-fenced", "case v-cut struck" — so match on the
    # class LIST containing `case`, and exclude the reserved placeholder. An earlier
    # version required class="case" exactly and found 15 of 29.
    rows = [
        (m.group(1), m.group(3))
        for m in re.finditer(
            r'<article id="(\d+)" class="([^"]*\bcase\b[^"]*)"[^>]*data-verdict="([a-z]+)"', html
        )
        if "reserved" not in m.group(2)
    ]
    tally = Counter(v for _id, v in rows)
    expect = {
        "c-tested": len(rows),
        "c-against": sum(tally[k] for k in AGAINST),
        "c-fenced": tally["fenced"],
    }

    errors = []
    for cid, want in expect.items():
        m = re.search(rf'id="{cid}" data-count="(\d+)">(\d+)<', html)
        if not m:
            errors.append(f"{cid}: no static fallback found")
            continue
        attr, shown = int(m.group(1)), int(m.group(2))
        if attr != want or shown != want:
            errors.append(
                f"{cid}: static says data-count={attr}/text={shown}, the rows compute {want}. "
                "A no-JS reader would see the wrong number."
            )
    if not rows:
        errors.append("no ledger rows parsed — the regex or the markup changed")

    if errors:
        print("RECORD COUNTERS: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(
        f"RECORD COUNTERS: PASS ({len(rows)} rows; "
        f"{expect['c-against']} against; {expect['c-fenced']} fenced; static matches runtime)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
