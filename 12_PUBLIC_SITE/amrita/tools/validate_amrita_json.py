#!/usr/bin/env python3
"""Validate amrita/amrita.json against the drop schema and confirm every source path exists."""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # -> amrita/
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))                       # -> 01_EMERGENTISM/
VALID_TIERS = {"[A]", "[B]", "[S]", "[I]", "[C]", "halahala"}
REQUIRED = ("id", "group", "tier", "title", "body", "source")

def main() -> int:
    data = json.load(open(os.path.join(HERE, "amrita.json"), encoding="utf-8"))
    if not isinstance(data, list) or not data:
        print("FAIL: amrita.json must be a non-empty array"); return 1
    seen, n_nectar, n_poison = set(), 0, 0
    for d in data:
        for k in REQUIRED:
            if k not in d or d[k] in (None, ""):
                print(f"FAIL: missing/empty '{k}' in {d.get('id','?')}"); return 1
        if d["group"] not in ("nectar", "halahala"):
            print(f"FAIL: bad group '{d['group']}' in {d['id']}"); return 1
        if d["tier"] not in VALID_TIERS:
            print(f"FAIL: bad tier '{d['tier']}' in {d['id']}"); return 1
        if d["id"] in seen:
            print(f"FAIL: duplicate id '{d['id']}'"); return 1
        seen.add(d["id"])
        src = os.path.join(ROOT, d["source"].lstrip("/"))
        if not os.path.exists(src):
            print(f"FAIL: source not found for {d['id']}: {d['source']}"); return 1
        n_nectar += d["group"] == "nectar"; n_poison += d["group"] == "halahala"
    print(f"OK: {len(data)} drops ({n_nectar} nectar, {n_poison} halahala), all sources exist")
    return 0

if __name__ == "__main__":
    sys.exit(main())
