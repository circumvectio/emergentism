#!/usr/bin/env python3
"""Build atlas/site_index.json — the navigable tree of current public pages.

The current-surface registry is authoritative for inclusion. Frozen library
roots and withheld artifacts stay in byte custody but never enter this index.
The JSON feeds assets/js/atlas-drawer.js and the /atlas/ knowledge home.

Usage: python3 -B build_atlas_index.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "atlas" / "site_index.json"
WITHHELD_REGISTRY = ROOT / "withheld-routes.json"
PARITY_MANIFEST = ROOT / "public_semantic_parity.json"


def load_boundaries() -> tuple[set[str], set[str], set[str]]:
    parity = json.loads(PARITY_MANIFEST.read_text(encoding="utf-8"))
    withheld = json.loads(WITHHELD_REGISTRY.read_text(encoding="utf-8"))
    current = {path for path in parity["currentSurfaces"] if path.endswith("index.html")}
    frozen = set(parity["frozenLibraryRoots"])
    artifacts = {item["artifact"] for item in withheld["artifacts"]}
    return current, frozen, artifacts


CURRENT_PAGES, FROZEN_ROOTS, WITHHELD_ARTIFACTS = load_boundaries()


def is_current(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    root_name = relative.split("/", 1)[0]
    return (
        relative in CURRENT_PAGES
        and relative not in WITHHELD_ARTIFACTS
        and root_name not in FROZEN_ROOTS
    )

# (section key, label, list of page dirs) — overview surfaces, curated order.
OVERVIEW = [
    # /established/ and /read/ were declared current surfaces but appeared in no section
    # list, so the drawer could not find them by search. Found by searching for
    # "established" on production and getting zero hits.
    ("start", "Start and practice", ["", "plainly", "dasein", "practice", "established", "record", "read", "book", "about", "exit"]),
    ("unfolding", "The Unfolding · D0–D6", ["0", "1", "2", "3", "4", "5", "6"]),
    ("method", "Map and method", ["dimensions", "axioms", "check", "rosetta", "ecology", "journey", "fable", "compass"]),
    ("participate", "Open research", ["f5", "map", "lab", "record/eub-1", "questions", "ethics", "record/pqa-54", "contribute"]),
]

COLLECTIONS = [("discoveries", "Discoveries")]

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
    if idx.exists() and is_current(idx):
        pages.append({"href": f"/{dirname}/", "title": page_title(idx)})
    for sub in sorted((p for p in base.iterdir() if p.is_dir()), key=lambda path: path.name):
        sidx = sub / "index.html"
        if sidx.exists() and is_current(sidx):
            pages.append({"href": f"/{dirname}/{sub.name}/", "title": page_title(sidx)})
    return pages


def build_payload() -> dict:
    tree = []
    for key, label, dirs in OVERVIEW:
        pages = []
        for d in dirs:
            idx = ROOT / "index.html" if not d else ROOT / d / "index.html"
            if idx.exists() and is_current(idx):
                href = "/" if not d else f"/{d}/"
                pages.append({"href": href, "title": page_title(idx)})
        if pages:
            tree.append({"key": key, "label": label, "pages": pages})
    for dirname, label in COLLECTIONS:
        pages = collect(dirname)
        if pages:
            tree.append({"key": dirname, "label": label, "pages": pages})
    total = sum(len(s["pages"]) for s in tree)
    return {
        "schemaVersion": 2,
        "status": "current-cleared-surfaces-only",
        "generated": "build_atlas_index.py",
        "source": "public_semantic_parity.json",
        "exclusions": {
            "frozenLibraryRoots": sorted(FROZEN_ROOTS),
            "withheldRegistry": "withheld-routes.json",
        },
        "total": total,
        "tree": tree,
    }


def canonical_payload(payload: dict) -> str:
    """Return the exact bytes emitted for the generated atlas artifact."""

    return json.dumps(payload, ensure_ascii=False, indent=1) + "\n"


def main(argv: list[str] | None = None) -> int:
    import sys as _sys

    argv = _sys.argv[1:] if argv is None else argv
    payload = build_payload()
    total = payload["total"]
    tree = payload["tree"]
    # --check exists because this artifact went stale unnoticed: /established/ and /read/
    # were added to currentSurfaces and the index was never rebuilt, so the drawer's
    # search returned zero hits for the site's own flagship page.
    if "--check" in argv:
        if not OUT.exists():
            print("ATLAS INDEX: FAIL\n- atlas/site_index.json has not been built")
            return 1
        if OUT.read_text(encoding="utf-8") != canonical_payload(payload):
            print(
                "ATLAS INDEX: FAIL\n"
                "- atlas/site_index.json differs from the deterministic payload, including "
                "its source and exclusion provenance. Rebuild: python3 -B build_atlas_index.py"
            )
            return 1
        print(f"ATLAS INDEX: PASS ({total} current pages in {len(tree)} sections; "
              f"matches public_semantic_parity.json)")
        return 0

    OUT.write_text(canonical_payload(payload), encoding="utf-8")
    print(f"site_index.json: {total} pages in {len(tree)} sections -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
