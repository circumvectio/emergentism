#!/usr/bin/env python3
"""Build the receipt disambiguation index — and keep it honest.

WHY. Receipt numbers in this corpus are NOT unique identifiers. Both live lanes
(50_AUDITS_AND_EXECUTIONS, 60_SESSION_PACKETS) begin at 100 and run over each other for a
hundred consecutive integers, so `r150` names four different documents across two lanes.
A citation convention cannot repair that; only a path can. This index exists so that a
numeric citation already in the corpus can be resolved BY HAND, and so the scale of the
problem is a number somebody can look at rather than a feeling.

Ruled 2026-07-31 (see 193_FIVE_RULINGS_SIGNED_2026_07_31.md, Q3 mechanism half — advisory,
executed without countersignature because it asserts no new claim).

WHAT THIS IS NOT. It does not make numbers unique. It does not authorise citing by number.
The rule stands: CITE RECEIPTS BY PATH.

DEFAULTS TO --check. gate.sh invokes checkers with no arguments, and a gate that MUTATES
the tree it is checking is not a gate — it would have quietly regenerated this index on
every run and always passed. Writing requires an explicit --write.

Usage: python3 -B build_receipt_disambiguation.py          verify (default)
       python3 -B build_receipt_disambiguation.py --write  regenerate
"""
from __future__ import annotations
import collections, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LANES = ("50_AUDITS_AND_EXECUTIONS", "60_SESSION_PACKETS")
OUT = ROOT / "11_UPLINK" / "50_AUDITS_AND_EXECUTIONS" / "00_RECEIPT_DISAMBIGUATION_INDEX.json"

SUP = re.compile(
    r"^\s*(superseded_by|supersedes|supersession_note)\s*:"
    r"|^\s*status\s*:.*(supersed|DISPUTED|NOT CURRENT|dissent|CORRECT)", re.I | re.M)
TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)

NOTE = ("Receipt numbers in this corpus are NOT unique identifiers. Both live lanes begin "
        "at 100 and run over each other for a hundred consecutive integers. This index lists "
        "every number naming more than one document, so an existing numeric citation can be "
        "resolved by hand. It does not make numbers unique and does not replace the rule: "
        "CITE BY PATH.")


def build() -> dict:
    by: dict[str, list[Path]] = collections.defaultdict(list)
    for lane in LANES:
        d = ROOT / "11_UPLINK" / lane
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*.md")):
            m = re.match(r"^(\d{2,3})[_A-Za-z]", f.name)
            if m and m.group(1) != "00":       # 00_ is the index/readme convention
                by[m.group(1)].append(f)

    rows = []
    for num in sorted(by, key=lambda x: int(x)):
        v = by[num]
        if len(v) < 2:
            continue
        entries = []
        for p in v:
            head = p.read_text(encoding="utf-8", errors="ignore")[:2500]
            t = TITLE.search(head)
            entries.append({
                "path": str(p.relative_to(ROOT)),
                "lane": p.parts[len(p.parts) - 2] if p.parent.name not in LANES else p.parent.name,
                "declares_supersession": bool(SUP.search(head)),
                "title": (t.group(1) if t else p.stem)[:90],
            })
        rows.append({"number": num, "count": len(v), "entries": entries})

    return {"schemaVersion": 1, "generated": "build_receipt_disambiguation.py",
            "note": NOTE, "ambiguousNumbers": len(rows),
            "worst": max((r["count"] for r in rows), default=0), "rows": rows}


def main(argv: list[str]) -> int:
    data = build()
    if "--write" not in argv:
        if not OUT.exists():
            print("RECEIPT DISAMBIGUATION: FAIL\n- index has not been built")
            return 1
        on_disk = json.loads(OUT.read_text(encoding="utf-8"))
        for k in ("ambiguousNumbers", "rows"):
            if on_disk.get(k) != data.get(k):
                print(f"RECEIPT DISAMBIGUATION: FAIL\n- '{k}' differs from the tree. "
                      f"Rebuild: python3 -B build_receipt_disambiguation.py")
                return 1
        print(f"RECEIPT DISAMBIGUATION: PASS ({on_disk['ambiguousNumbers']} ambiguous numbers "
              f"indexed; worst names {on_disk['worst']} documents)")
        print("  scope: proves the index matches the tree. It does NOT make numbers unique, "
              "and it does not license citing by number.")
        return 0
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"receipt disambiguation: {data['ambiguousNumbers']} ambiguous numbers, "
          f"worst names {data['worst']} documents -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
