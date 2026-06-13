#!/usr/bin/env python3
"""Build atlas/site_index.json — the navigable tree of every public page.

Scans the static site for index.html pages, extracts each page's title, and
groups them into the weltanschauung tree (overview surfaces first, then the
twelve deep-library sections). The JSON feeds assets/js/atlas-drawer.js (the
gitbook-style tree + search drawer present on every page) and the /atlas/
knowledge home. Regenerable: run after adding or retitling pages.

Usage: python3 -B build_atlas_index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "atlas" / "site_index.json"

# (section key, label, list of page dirs) — overview surfaces, curated order.
OVERVIEW = [
    ("unfolding", "The Unfolding · D0–D6", ["0", "1", "2", "3", "4", "5", "6"]),
    ("doctrine", "Doctrine", ["synthesis", "axioms", "soul-loop", "game", "rosetta", "moat"]),
    ("reading", "Reading", ["read", "book", "routes"]),
]

# Deep-library sections (generated pages, frozen): label per directory.
LIBRARY = [
    ("papers", "Papers"),
    ("canon", "Canon"),
    ("formal", "Formal System"),
    ("paradox", "Paradox Dissolutions"),
    ("memetic", "Memetics"),
    ("rosettad", "Rosetta Domains"),
    ("operators", "Operators"),
    ("will", "Will / Teleology"),
    ("value", "Value / Axiology"),
    ("ground", "Ground / Ontology"),
    ("sacred", "Sacred / Theology"),
    ("method", "Method"),
    ("meta", "Meta"),
]

TITLE_RE = re.compile(r"<title>([^<]+)</title>", re.IGNORECASE)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def page_title(path: Path) -> str:
    try:
        head = path.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return path.parent.name
    m = H1_RE.search(head) or TITLE_RE.search(head)
    if not m:
        return path.parent.name.replace("-", " ")
    text = TAG_RE.sub("", m.group(1))
    text = re.sub(r"\s+", " ", text).strip()
    # strip site-name suffixes like " — Emergentism"
    return re.sub(r"\s*[—|·-]\s*Emergentism.*$", "", text) or path.parent.name


def collect(dirname: str):
    base = ROOT / dirname
    pages = []
    idx = base / "index.html"
    if idx.exists():
        pages.append({"href": f"/{dirname}/", "title": page_title(idx)})
    for sub in sorted(p for p in base.iterdir() if p.is_dir()):
        sidx = sub / "index.html"
        if sidx.exists():
            pages.append({"href": f"/{dirname}/{sub.name}/", "title": page_title(sidx)})
    return pages


def main() -> int:
    tree = []
    for key, label, dirs in OVERVIEW:
        pages = []
        for d in dirs:
            idx = ROOT / d / "index.html"
            if idx.exists():
                pages.append({"href": f"/{d}/", "title": page_title(idx)})
        if pages:
            tree.append({"key": key, "label": label, "pages": pages})
    for dirname, label in LIBRARY:
        pages = collect(dirname)
        if pages:
            tree.append({"key": dirname, "label": f"{label} ({len(pages)})", "pages": pages})
    total = sum(len(s["pages"]) for s in tree)
    OUT.write_text(json.dumps({"generated": "build_atlas_index.py", "total": total,
                               "tree": tree}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"site_index.json: {total} pages in {len(tree)} sections -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
