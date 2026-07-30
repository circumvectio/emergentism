#!/usr/bin/env python3
"""Render breadcrumbs and prev/next into the 292 frozen-library pages.

WHY GENERATED AND NOT HAND-WRITTEN. reading-manifest.json already carries the order and
the sections. A hand-maintained pager over 292 documents would be wrong within a week,
and wrong silently — a dangling `next` looks exactly like a correct one.

WHAT IS INJECTED, between markers so the script is idempotent:

  <!--L2:CRUMB-->  Emergentism / Section / Title            at the top of the article
  <!--L2:PAGER-->  ← previous · section · next →            at the end of the article

Order is the manifest's own flat order, so a reader can go straight through all 292 rather
than being trapped inside a section. The breadcrumb carries the section; the pager carries
the sequence.

The frozen-library banner, the tier markers and the article body are never touched. This
adds navigation and removes nothing — provenance is unaffected.

Usage:
  python3 -B build_library_nav.py           write
  python3 -B build_library_nav.py --check    verify, write nothing
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "reading-manifest.json"

CRUMB_OPEN, CRUMB_CLOSE = "<!--L2:CRUMB-->", "<!--/L2:CRUMB-->"
PAGER_OPEN, PAGER_CLOSE = "<!--L2:PAGER-->", "<!--/L2:PAGER-->"

ANCHOR = '<article class="library-article">'
END = "</article>"

SECTION_LABELS = {
    "papers": "Papers", "canon": "Canon", "foundations": "Foundations",
    "trinity": "Trinity", "formal": "Formal system", "paradox": "Paradox",
    "memetic": "Memetic", "rosettad": "Rosetta D-series", "operators": "Operators",
    "will": "Teleology", "value": "Axiology", "ground": "Ontology",
    "sacred": "Theology", "method": "Method", "meta": "Meta",
}

STYLE = (
    "<style>.l2-crumb{font:400 .74rem/1.7 ui-monospace,Menlo,monospace;letter-spacing:.04em;"
    "color:#8a8577;margin:0 0 1.4rem}.l2-crumb a{color:#8a8577;text-decoration:none}"
    ".l2-crumb a:hover{color:#e8b84b}.l2-crumb b{color:#c9c4b4;font-weight:400}"
    ".l2-pager{display:flex;flex-wrap:wrap;gap:.6rem 1.2rem;justify-content:space-between;"
    "align-items:baseline;margin:3rem 0 0;padding:1.1rem 0 0;border-top:1px solid "
    "rgba(233,230,223,.14);font:400 .82rem/1.55 ui-monospace,Menlo,monospace}"
    ".l2-pager a{color:#e8b84b;text-decoration:none;max-width:46%}"
    ".l2-pager a:hover{text-decoration:underline}.l2-pager .l2-mid{color:#8a8577;"
    "font-size:.74rem;letter-spacing:.04em}.l2-pager .l2-next{text-align:right}"
    "@media(max-width:620px){.l2-pager a{max-width:100%}}</style>"
)


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def page_path(href: str) -> Path:
    return ROOT / (href.strip("/") + "/index.html")


def depth_prefix(href: str) -> str:
    """Relative path back to the site root from a library page."""
    return "../" * (len(href.strip("/").split("/")) or 1)


def crumb(doc: dict) -> str:
    up = depth_prefix(doc["href"])
    label = SECTION_LABELS.get(doc.get("section", ""), (doc.get("section") or "Library").title())
    return (
        f'{CRUMB_OPEN}{STYLE}<nav class="l2-crumb" aria-label="Breadcrumb">'
        f'<a href="{up}">Emergentism</a> / <a href="{up}read/">Library</a> / '
        f'<a href="{up}{esc(doc.get("section",""))}/">{esc(label)}</a> / '
        f'<b>{esc(doc.get("title",""))}</b></nav>{CRUMB_CLOSE}'
    )


def pager(doc: dict, prev: dict | None, nxt: dict | None, i: int, n: int) -> str:
    up = depth_prefix(doc["href"])
    left = (
        f'<a class="l2-prev" href="{up}{esc(prev["href"])}" rel="prev">&larr; {esc(prev["title"])}</a>'
        if prev else f'<a class="l2-prev" href="{up}read/">&larr; The reader map</a>'
    )
    right = (
        f'<a class="l2-next" href="{up}{esc(nxt["href"])}" rel="next">{esc(nxt["title"])} &rarr;</a>'
        if nxt else f'<a class="l2-next" href="{up}atlas/">The full atlas &rarr;</a>'
    )
    mid = f'<span class="l2-mid">{i} / {n} &middot; frozen library</span>'
    return f'{PAGER_OPEN}<nav class="l2-pager" aria-label="Document sequence">{left}{mid}{right}</nav>{PAGER_CLOSE}'


def splice(text: str, open_t: str, close_t: str, block: str, *, after: str | None = None,
           before: str | None = None) -> str | None:
    if open_t in text and close_t in text:
        a, b = text.index(open_t), text.index(close_t) + len(close_t)
        return text[:a] + block + text[b:]
    if after and after in text:
        i = text.index(after) + len(after)
        return text[:i] + "\n" + block + text[i:]
    if before and before in text:
        i = text.rindex(before)
        return text[:i] + block + "\n" + text[i:]
    return None


def main(argv: list[str]) -> int:
    docs = json.loads(MANIFEST.read_text(encoding="utf-8"))["documents"]
    live = [d for d in docs if page_path(d["href"]).exists()]
    n = len(live)
    check = "--check" in argv
    changed, missing, unanchored, dangling = 0, [], [], []

    hrefs = {d["href"] for d in live}

    for i, d in enumerate(live):
        prev = live[i - 1] if i > 0 else None
        nxt = live[i + 1] if i + 1 < n else None
        for other in (prev, nxt):
            if other and other["href"] not in hrefs:
                dangling.append(other["href"])
        p = page_path(d["href"])
        t = orig = p.read_text(encoding="utf-8")

        c = splice(t, CRUMB_OPEN, CRUMB_CLOSE, crumb(d), after=ANCHOR)
        if c is None:
            unanchored.append(d["href"])
            continue
        t = c
        g = splice(t, PAGER_OPEN, PAGER_CLOSE, pager(d, prev, nxt, i + 1, n), before=END)
        if g is None:
            unanchored.append(d["href"])
            continue
        t = g

        if t != orig:
            if check:
                missing.append(d["href"])
            else:
                p.write_text(t, encoding="utf-8")
                changed += 1

    if check:
        errors = []
        if missing:
            errors.append(f"{len(missing)} pages have stale or absent L2 nav "
                          f"(e.g. {', '.join(missing[:3])}) — rebuild with "
                          f"python3 -B build_library_nav.py")
        if unanchored:
            errors.append(f"{len(unanchored)} pages lack the expected anchors "
                          f"({ANCHOR} / {END}): {', '.join(unanchored[:3])}")
        if dangling:
            errors.append(f"dangling sequence targets: {sorted(set(dangling))[:5]}")
        if errors:
            print("LIBRARY NAV: FAIL")
            for e in errors:
                print(f"- {e}")
            return 1
        print(f"LIBRARY NAV: PASS ({n} library pages carry a breadcrumb and a pager; "
              f"0 dangling targets)")
        print("  scope: proves the nav matches reading-manifest.json's order. It does NOT "
              "prove the order is the right reading order — that is an editorial choice.")
        return 0

    print(f"library nav: {changed} pages updated of {n} in the manifest order")
    if unanchored:
        print(f"  SKIPPED (no anchor): {len(unanchored)} — {', '.join(unanchored[:4])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
