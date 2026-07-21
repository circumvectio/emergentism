#!/usr/bin/env python3
"""Generate the public atlas from the deny-by-default release manifest."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "release-manifest.json"
OUTPUT = ROOT / "atlas" / "site_index.json"

CATEGORIES = [
    ("door", "Start · discovery and plain language", ("/", "/discoveries/", "/fable/", "/plainly/", "/about/")),
    ("practice", "Use · decide, act, and return", ("/practice/", "/compass/", "/map/", "/journey/", "/build/")),
    ("trial", "Test · claims, failures, and receipts", ("/axioms/", "/test/", "/halahala/", "/record/")),
    ("ladder", "Ladder · D0 through D6", tuple(f"/{i}/" for i in range(7))),
    ("freedom", "Freedom · constraints and exit", ("/five-plus-one/", "/exit/")),
]


def title_for(path: Path) -> str:
    body = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"<title>(.*?)</title>", body, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return path.parent.name or "Emergentism"
    title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", match.group(1))).strip()
    return html.unescape(title).split(" · Emergentism", 1)[0]


def build() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = {row["path"]: row for row in manifest["routes"]}
    tree = []
    seen: set[str] = set()
    for key, label, prefixes in CATEGORIES:
        pages = []
        for route in manifest["routes"]:
            href = route["path"]
            belongs = any(href == prefix or (prefix == "/discoveries/" and href.startswith(prefix)) for prefix in prefixes)
            if not belongs or href in seen:
                continue
            seen.add(href)
            pages.append({"href": href, "title": title_for(ROOT / route["file"])})
        if pages:
            tree.append({"key": key, "label": label, "pages": pages})
    return {
        "schemaVersion": 1,
        "generatedFrom": "release-manifest.json",
        "total": sum(len(section["pages"]) for section in tree),
        "tree": tree,
    }


def encoded() -> str:
    return json.dumps(build(), indent=1, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = encoded()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("atlas/site_index.json drifted from release-manifest.json")
            return 1
        print("atlas index: clean")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"atlas index: {build()['total']} routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
