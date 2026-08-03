#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""demand_census.py — who actually cites what (2026-07-22).

THE TEST THIS IMPLEMENTS. On 2026-07-22 a root audit counted inbound citations
per file, got 2-33 each, and concluded nothing could move. The count was an
artifact: five tidy passes had generated their own audit trail, and those audits
name every file they touched. The machinery was citing its own output.

So a citation only counts as DEMAND when the citer is live doctrine. Excluded:

  - the file itself
  - 90_ARCHIVE/ and any nested 90_ARCHIVE/ (cold provenance)
  - 91_COMPATIBILITY/ (forwarding paths only)
  - 00_HANDOFF/ (dated in-flight packets, not doctrine)
  - forwarding stubs (a stub citing a file is a redirect, not demand)
  - tidy/audit machinery: TIDY_PLAN, *AUDIT*, *RECEIPT*, L<n>_* caste reports,
    CITATION passes, and the numbered receipt ledger

A file cited ONLY by the pass that created it is not load-bearing. It is an echo.

USAGE
  python3 demand_census.py [--json OUT] [ROOT]
  Prints a per-lane summary and the zero-demand list.
"""

import json
import os
import re
import sys
from collections import defaultdict

STUB_RE = re.compile(
    r"FORWARDING STUB|Compatibility stub|forwarding-stub|HISTORICAL FORWARDING", re.I)
MACHINERY_RE = re.compile(
    r"TIDY_PLAN|AUDIT|RECEIPT|CITATION|^L\d|/L\d[._]|_LEDGER|CENSUS|HANDOFF", re.I)
EXCLUDE_DIR = ("90_ARCHIVE", "91_COMPATIBILITY", "00_HANDOFF",
               "node_modules", "__pycache__", ".git")
SCAN_EXT = (".md", ".html", ".py", ".json", ".yaml", ".yml")
HEAD = 1500


def is_excluded(rel):
    parts = rel.split(os.sep)
    return any(p in EXCLUDE_DIR for p in parts)


def build(root):
    """returns (docs, text_by_rel, stub_set)"""
    docs, text, stubs = [], {}, set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", ".claude", ".codex-worktrees", "node_modules", "__pycache__")]
        for fn in filenames:
            if not fn.endswith(SCAN_EXT):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    body = fh.read()
            except OSError:
                continue
            text[rel] = body
            if fn.endswith(".md") and not is_excluded(rel):
                docs.append(rel)
                if STUB_RE.search(body[:HEAD]):
                    stubs.add(rel)
    return docs, text, stubs


def census(root):
    docs, text, stubs = build(root)
    basename = defaultdict(list)
    for rel in docs:
        basename[os.path.basename(rel)].append(rel)

    demand = {rel: [] for rel in docs}
    for citer, body in text.items():
        if is_excluded(citer) or citer in stubs or MACHINERY_RE.search(citer):
            continue                              # not a source of demand
        for name, targets in basename.items():
            if name not in body:
                continue
            if len(targets) == 1:
                # unique basename — a bare mention unambiguously names this file
                t = targets[0]
                if t != citer:
                    demand[t].append(citer)
            else:
                # AMBIGUOUS basename (README.md, AGENTS.md, CLAUDE.md, ...):
                # a bare mention names no particular file. Require a path-
                # qualified reference — at least the parent directory — or the
                # citation is not evidence that THIS file is wanted.
                for t in targets:
                    if t == citer:
                        continue
                    parent = os.path.basename(os.path.dirname(t))
                    qualified = (t in body) or (parent and f"{parent}/{name}" in body)
                    if qualified:
                        demand[t].append(citer)
    return docs, demand, stubs


def main(argv):
    out_json = None
    args = [a for a in argv[1:]]
    if "--json" in args:
        i = args.index("--json")
        out_json = args[i + 1]
        del args[i:i + 2]
    root = args[0] if args else os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    docs, demand, stubs = census(root)
    zero = sorted([d for d in docs if not demand[d]])

    per_lane = defaultdict(lambda: [0, 0])
    for d in docs:
        lane = d.split(os.sep)[0] if os.sep in d else "(root)"
        per_lane[lane][0] += 1
        if not demand[d]:
            per_lane[lane][1] += 1

    print(f"DEMAND CENSUS — {len(docs)} live documents under {os.path.basename(root)}\n")
    print(f"{'lane':<26}{'docs':>7}{'zero-demand':>14}{'':>3}")
    print("-" * 52)
    for lane in sorted(per_lane):
        tot, z = per_lane[lane]
        pct = (100 * z / tot) if tot else 0
        print(f"{lane:<26}{tot:>7}{z:>14}   {pct:>5.1f}%")
    print("-" * 52)
    print(f"{'TOTAL':<26}{len(docs):>7}{len(zero):>14}   "
          f"{100*len(zero)/max(len(docs),1):>5.1f}%")
    print(f"\nstubs among them: {len(stubs)}")

    if out_json:
        json.dump({"root": root, "total": len(docs), "zero": zero,
                   "demand": {k: v for k, v in demand.items()},
                   "stubs": sorted(stubs)}, open(out_json, "w"))
        print(f"\nfull census written to {out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
