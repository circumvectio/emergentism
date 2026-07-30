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
    total = sum(len(s["pages"]) for s in tree)

    return {
        "schemaVersion": 1,
        "status": "frozen-library-only",
        "boundary": (
            "These routes are served noindex, follow. They are excluded from "
            "atlas/site_index.json by design and must never be merged into it. This index "
            "exists so a reader already on the site can find a document; it grants no "
            "current-surface status and creates no authority."
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
