#!/usr/bin/env python3
"""Harvest every L1..L7 column in the Rosetta lane into one machine-readable ledger.

Harvest, never infer. A column is emitted only when a markdown table in the lane
carries rows keyed L1..L7 (or L-1..L-7 / Level 1..7) in one of its cells. The
header text is copied verbatim; nothing is normalised, renamed, or filled in.

A row that is absent is emitted as null. `null` beats a plausible value.

Usage:
    python3 harvest_rosetta_columns.py [--lane PATH] [--out PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LANE_DEFAULT = Path(__file__).resolve().parents[2] / "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE"

# A cell counts as an L-key if, once stripped of markdown emphasis, links and
# backticks, it is exactly one of these forms.
L_KEY = re.compile(r"^(?:GEN7@1:)?L[\s\-–—]?([1-7])$", re.I)
L_KEY_WORDY = re.compile(r"^level[\s\-–—]?([1-7])$", re.I)

CLEAN = re.compile(r"[*_`]|\[([^\]]*)\]\([^)]*\)")
SEP_ROW = re.compile(r"^[\s|:\-–—+]+$")


def clean_cell(text: str) -> str:
    text = CLEAN.sub(lambda m: m.group(1) or "", text)
    return " ".join(text.split()).strip()


def l_index(cell: str) -> int | None:
    c = clean_cell(cell)
    for pat in (L_KEY, L_KEY_WORDY):
        m = pat.match(c)
        if m:
            return int(m.group(1))
    return None


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [clean_cell(c) for c in line.split("|")]


def tables_in(lines: list[str]):
    """Yield (header_cells, body_rows, start_line) for each markdown table."""
    i = 0
    n = len(lines)
    while i < n - 1:
        if "|" in lines[i] and SEP_ROW.match(lines[i + 1]) and "|" in lines[i + 1]:
            header = split_row(lines[i])
            body = []
            j = i + 2
            while j < n and "|" in lines[j] and lines[j].strip():
                body.append(split_row(lines[j]))
                j += 1
            if body:
                yield header, body, i + 1
            i = j
        else:
            i += 1


def harvest(lane: Path):
    records = []
    skipped = []
    for path in sorted(lane.rglob("*.md")):
        rel = path.relative_to(lane).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError) as exc:
            skipped.append({"file": rel, "reason": str(exc)})
            continue

        for t_idx, (header, body, line_no) in enumerate(tables_in(lines)):
            # Which column holds the L-keys?
            key_col, seats = None, {}
            for col in range(len(header)):
                found = {}
                for row in body:
                    if col < len(row):
                        li = l_index(row[col])
                        if li is not None:
                            found[li] = row
                if len(found) > len(seats):
                    key_col, seats = col, found
            if key_col is None or len(seats) < 4:
                continue  # not an L-keyed table

            for col in range(len(header)):
                if col == key_col:
                    continue
                name = header[col]
                if not name:
                    continue
                cells = {}
                for li in range(1, 8):
                    row = seats.get(li)
                    cells[f"L{li}"] = (row[col] if row and col < len(row) and row[col] else None)
                if not any(cells.values()):
                    continue
                records.append({
                    "file": rel,
                    "table_index": t_idx,
                    "line": line_no,
                    "column": name,
                    "seats_present": sorted(seats),
                    "cells": cells,
                })
    return records, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", type=Path, default=LANE_DEFAULT)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    if not args.lane.is_dir():
        print(f"lane not found: {args.lane}", file=sys.stderr)
        return 2

    records, skipped = harvest(args.lane)

    files = sorted({r["file"] for r in records})
    full = [r for r in records if len(r["seats_present"]) == 7]
    print(f"files with L-keyed tables : {len(files)}")
    print(f"columns harvested         : {len(records)}")
    print(f"  of which all 7 seats    : {len(full)}")
    print(f"  partial (4-6 seats)     : {len(records) - len(full)}")
    if skipped:
        print(f"unreadable files          : {len(skipped)}")

    if args.out:
        with args.out.open("w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
