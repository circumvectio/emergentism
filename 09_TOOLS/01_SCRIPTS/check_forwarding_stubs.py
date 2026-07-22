#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_forwarding_stubs.py — the stub integrity check (2026-07-22).

WHY THIS EXISTS. On 2026-07-22 a Rosetta caste sweep found that the root's
"0 broken stubs" measurement was technically true and semantically false:
fourteen stubs declared a `canonical_target` that pointed either straight into
`90_ARCHIVE/` or at another file that was itself a tombstone. A reader
following a citation labelled "canonical home" landed on a grave. Target
EXISTENCE was being checked; target STATUS was not.

THE FOUR RULES ENFORCED (from the caste-adjudicated stub template):

  R1  A stub must declare at least one target, and it must resolve.
  R2  `canonical_target` means a LIVE owner. It must NOT start with
      `90_ARCHIVE/` and must NOT point at another forwarding stub.
      If nothing live absorbs the document, omit the field and use
      `historical_target` — do not point canon at a grave.
  R3  `historical_target` means preserved bytes. It MAY be in `90_ARCHIVE/`.
  R4  No chains. A stub points at its terminus, not at another stub.

USAGE
  python3 check_forwarding_stubs.py [DIR ...]     # default: repo root
  Exit 0 = clean · 1 = violations · 2 = usage error
"""

import os
import re
import sys

STUB_RE = re.compile(
    r"FORWARDING STUB|Compatibility stub|forwarding-stub|HISTORICAL FORWARDING", re.I)
TARGET_RE = re.compile(
    r"^(canonical_target|historical_target|archive_target):\s*(\S+)\s*$", re.M)
SKIP_DIRS = {"90_ARCHIVE", "91_COMPATIBILITY", "node_modules", ".git",
             ".codex-worktrees", "book-pwa", ".vercel", "__pycache__"}
HEAD = 1500


def head_of(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(HEAD)
    except OSError:
        return ""


def is_stub(path):
    return bool(STUB_RE.search(head_of(path)))


def targets(path):
    return TARGET_RE.findall(head_of(path))


def check(root):
    problems = []
    checked = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            if not is_stub(p):
                continue
            checked += 1
            found = targets(p)
            rel = os.path.relpath(p, root)
            if not found:
                problems.append((rel, "R1", "declares no target field"))
                continue
            for key, val in found:
                # a target may be written relative to the FILE or to the repo root;
                # accept either, preferring file-relative (the common convention)
                cand = [os.path.normpath(os.path.join(dirpath, val)),
                        os.path.normpath(os.path.join(root, val))]
                abs_t = next((c for c in cand if os.path.exists(c)), cand[0])
                if not os.path.exists(abs_t):
                    problems.append((rel, "R1", f"{key} does not resolve: {val}"))
                    continue
                if key == "archive_target":
                    problems.append(
                        (rel, "R3", "field `archive_target` is retired — use `historical_target`"))
                if key == "canonical_target":
                    if "90_ARCHIVE/" in os.path.relpath(abs_t, root):
                        problems.append(
                            (rel, "R2", f"canonical_target points at a GRAVE: {val} "
                                        f"— rename the field to historical_target"))
                    elif is_stub(abs_t):
                        onward = targets(abs_t)
                        nxt = onward[0][1] if onward else "?"
                        problems.append(
                            (rel, "R4", f"canonical_target points at another STUB: {val} "
                                        f"(which forwards to {nxt}) — collapse the chain"))
    return checked, problems


def main(argv):
    roots = argv[1:] or [os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))]
    total, allp = 0, []
    for r in roots:
        if not os.path.isdir(r):
            print(f"not a directory: {r}", file=sys.stderr)
            return 2
        c, p = check(r)
        total += c
        allp.extend(p)
    if not allp:
        print(f"check_forwarding_stubs: clean — {total} stub(s), "
              f"all resolve, none points at a grave or another stub")
        return 0
    for rel, rule, msg in allp:
        print(f"{rel}: [{rule}] {msg}")
    print(f"\ncheck_forwarding_stubs: {len(allp)} violation(s) across {total} stub(s)")
    print("A stub holds a path, not a claim. Canon never points at a grave.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
