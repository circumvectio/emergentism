#!/usr/bin/env python3
"""Build atlas/library_index.json — a searchable index of the FROZEN library.

WHY THIS IS A SECOND INDEX AND NOT AN EXTENSION OF THE FIRST.

atlas/site_index.json is `current-cleared-surfaces-only` by design: build_atlas_index.py
states that "frozen library roots and withheld artifacts stay in byte custody but never
enter this index." That boundary is deliberate and this script does not touch it.

But the frozen library is served `noindex, follow` by vercel.json. `noindex` governs
search ENGINES. `follow` is an explicit instruction to traverse the links. A reader who
is already on the site being unable to find a document among 292 is not a publication
boundary — it is a missing table of contents. So: a second index, separately named,
separately labelled in the UI, and never merged into the current-surface tree.

WHAT IS AND IS NOT INCLUDED
  · included: the documents listed in reading-manifest.json, which is the corpus's own
    ordered spine for the frozen library
  · excluded: anything in withheld-routes.json, checked by artifact path AND by route
  · excluded: anything already in the current-surface index — no page appears twice
  · excluded: any route whose file does not exist on disk

Usage: python3 -B build_library_index.py        (writes atlas/library_index.json)
       python3 -B build_library_index.py --check (verifies without writing)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "atlas" / "library_index.json"
MANIFEST = ROOT / "reading-manifest.json"
PARITY = ROOT / "public_semantic_parity.json"
WITHHELD = ROOT / "withheld-routes.json"

SECTION_LABELS = {
    "papers": "Papers",
    "canon": "Canon",
    "foundations": "Foundations",
    "trinity": "Trinity",
    "formal": "Formal system",
    "paradox": "Paradox",
    "memetic": "Memetic",
    "rosettad": "Rosetta D-series",
    "operators": "Operators",
    "will": "Teleology",
    "value": "Axiology",
    "ground": "Ontology",
    "sacred": "Theology",
    "method": "Method",
    "meta": "Meta",
}


# Routes that EXIST, are real content, and were findable from nowhere: neither declared
# current (so absent from the nav, the current index and the sitemap) nor a document inside
# the frozen library (so absent from that index too). They fell through both nets. Reported
# by the owner as "the website doesn't have dimensions and not have ologies and titans" —
# dimensions was fine; these were not.
#
# Including them here changes NO page's noindex status and promotes nothing to a current
# surface. It only makes them reachable from the drawer, which is what `follow` is for.
EXTRA_SECTIONS = [
    ("sections", "Library sections", [
        "papers", "canon", "foundations", "trinity", "formal", "paradox", "memetic",
        "rosettad", "operators", "will", "value", "ground", "sacred", "method", "meta",
        "sources",
    ]),
    ("disciplines", "The disciplines", [
        "axiology", "ontology", "theology", "cosmology", "epistemology", "methodology",
        "teleology",
    ]),
    ("instruments", "Instruments and studies", [
        "titans", "riemann", "suda", "suda-notes", "egg", "saturation", "synthesis",
        "soul-loop", "burrisphere", "log-realignment", "geometric-ontology",
        "finity-papers", "rosetta-d-series", "halahala", "amrita", "game", "atlas",
    ]),
]

# Deliberately NOT included: infrastructure (offline, test, build, home, r/0..r/6,
# historical-boundary) and everything in withheld-routes.json.
INFRASTRUCTURE = {"offline", "test", "build", "home", "historical-boundary", "404", "app"}


def build() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    parity = json.loads(PARITY.read_text(encoding="utf-8"))
    withheld_raw = WITHHELD.read_text(encoding="utf-8")
    withheld = json.loads(withheld_raw)

    current = {p for p in parity["currentSurfaces"] if p.endswith("index.html")}
    current_routes = {"/" + p[: -len("index.html")] for p in current}
    withheld_artifacts = {a["artifact"] for a in withheld.get("artifacts", [])}

    sections: dict[str, list[dict]] = {}
    skipped = {"withheld": 0, "already_current": 0, "missing_file": 0}

    for doc in manifest.get("documents", []):
        href = doc.get("href", "").strip()
        if not href:
            continue
        rel = href.rstrip("/") + "/index.html" if not href.endswith(".html") else href
        route = "/" + href.lstrip("/")

        if rel in withheld_artifacts or route.rstrip("/") in withheld_raw:
            skipped["withheld"] += 1
            continue
        if rel in current or route in current_routes:
            skipped["already_current"] += 1
            continue
        if not (ROOT / rel).exists():
            skipped["missing_file"] += 1
            continue

        sec = doc.get("section") or "other"
        sections.setdefault(sec, []).append(
            {"href": route, "title": (doc.get("title") or route).strip()}
        )

    tree = [
        {"key": k, "label": SECTION_LABELS.get(k, k.replace("-", " ").title()), "pages": v}
        for k, v in sorted(sections.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]

    def title_of(route: str) -> str:
        f = ROOT / route / "index.html"
        try:
            head = f.read_text(encoding="utf-8", errors="replace")[:4000]
        except OSError:
            return route
        m = re.search(r"<h1[^>]*>(.*?)</h1>", head, re.I | re.S) or \
            re.search(r"<title>([^<]+)</title>", head, re.I)
        if not m:
            return route
        txt = re.sub(r"<[^>]+>", "", m.group(1))
        return re.sub(r"\s+", " ", txt).split("\u2014")[0].strip() or route

    for key, label, routes in EXTRA_SECTIONS:
        pages = []
        for r in routes:
            if r in INFRASTRUCTURE:
                continue
            rel = f"{r}/index.html"
            route = f"/{r}/"
            if rel in withheld_artifacts or route.rstrip("/") in withheld_raw:
                skipped["withheld"] += 1
                continue
            if rel in current or route in current_routes:
                skipped["already_current"] += 1
                continue
            if not (ROOT / rel).exists():
                skipped["missing_file"] += 1
                continue
            pages.append({"href": route, "title": title_of(r)})
        if pages:
            tree.append({"key": key, "label": label, "pages": pages})
    total = sum(len(s["pages"]) for s in tree)

    return {
        "schemaVersion": 1,
        "status": "frozen-library-and-undeclared-routes",
        "boundary": (
            "Frozen-library documents plus routes that are declared neither current nor "
            "frozen. Most are served noindex; none is a current surface. They are excluded "
            "from atlas/site_index.json by design and must never be merged into it. This "
            "index exists so a reader already on the site can find a page; it grants no "
            "current-surface status, changes no header, and creates no authority."
        ),
        "source": "reading-manifest.json",
        "excludes": "withheld-routes.json artifacts, current surfaces, missing files",
        "skipped": skipped,
        "total": total,
        "tree": tree,
    }


def main(argv: list[str]) -> int:
    data = build()
    if "--check" in argv:
        if not OUT.exists():
            print("LIBRARY INDEX: FAIL\n- atlas/library_index.json has not been built")
            return 1
        on_disk = json.loads(OUT.read_text(encoding="utf-8"))
        # compare only the parts that must not drift
        for key in ("total", "tree", "status"):
            if on_disk.get(key) != data.get(key):
                print(
                    f"LIBRARY INDEX: FAIL\n- '{key}' differs from what reading-manifest.json "
                    f"now produces. Rebuild with `python3 -B build_library_index.py`."
                )
                return 1
        print(
            f"LIBRARY INDEX: PASS ({on_disk['total']} frozen-library pages in "
            f"{len(on_disk['tree'])} sections; matches reading-manifest.json)"
        )
        print(
            "  scope: proves the index matches the manifest and excludes withheld and "
            "current routes. It does NOT change any page's noindex status."
        )
        return 0

    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"library index: {data['total']} pages, {len(data['tree'])} sections -> {OUT.relative_to(ROOT)}")
    print(f"  skipped: {data['skipped']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
