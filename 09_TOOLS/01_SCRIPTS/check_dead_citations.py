#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_dead_citations.py — live documents selling dead ones (2026-07-22).

THE PATHOLOGY THIS CATCHES. Protocol 54 §4 names the corpus's single failure
mode: a document reading healthy over a source that is broken or superseded.
An all-lanes caste audit on 2026-07-22 found the same shape in lane after lane:

  01_TELEOLOGY/02_THE_DERIVATION/README.md sold six rows as live results;
    the targets' own headers read "Kintsugi Tombstone / SUPERSEDED IN PLACE".
  03_METHODOLOGY falsifier #8 reported "Status: Open challenge" on three
    proofs whose headers read "ACTIVE TOMBSTONE — invalid uniqueness proof".
  08_FRAMEWORK_SUPPORT PD_00_INDEX claimed "All planned paradox dissolutions
    now exist"; nine targets are 15-line stubs reading "SUPERSEDED".

Every instance is the same mechanical fact: **a LIVE document links to a target
whose OWN FRONTMATTER declares itself dead, and says nothing about it.**

WHAT COUNTS AS DEAD (read from the target's own first ~1500 chars):
  SUPERSEDED · TOMBSTONE · RETRACTED · DISPUTED · DEPRECATED ·
  "no current semantic authority" · "not current ... authority"

WHAT IS NOT A FINDING:
  - the citing document is itself a stub, an archive file, or audit machinery
    (a tombstone may freely cite tombstones)
  - the citing line ALREADY discloses the status — it contains one of the dead
    words, or "was", "formerly", "retired", "grave", "historical", "provenance"
  - the link points into 90_ARCHIVE (archival links are honest by construction)

USAGE
  python3 check_dead_citations.py [DIR ...]
  Exit 0 = clean · 1 = undisclosed dead citations found
"""

import os
import re
import sys

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+\.md)[^)]*\)")
DEAD_RE = re.compile(
    r"SUPERSEDED|TOMBSTONE|RETRACTED|DISPUTED|DEPRECATED|"
    r"no current semantic authority|not current .{0,24}authority", re.I)
DISCLOSED_RE = re.compile(
    r"SUPERSEDED|TOMBSTONE|RETRACTED|DISPUTED|DEPRECATED|\bwas\b|formerly|"
    r"retired|grave|historical|provenance|archived|dead|killed|withdrawn", re.I)
STUB_RE = re.compile(
    r"FORWARDING STUB|Compatibility stub|forwarding-stub|HISTORICAL FORWARDING", re.I)
MACHINERY_RE = re.compile(r"AUDIT|RECEIPT|TIDY_PLAN|CENSUS|_LEDGER|HANDOFF|CITATION", re.I)
SKIP_DIRS = {"90_ARCHIVE", "node_modules", ".git", ".lake",
             ".codex-worktrees", "book-pwa", ".vercel", "__pycache__"}
HEAD = 1500


def read(path, n=None):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(n) if n else fh.read()
    except OSError:
        return ""


def is_dead(path):
    """A target is dead only if its own DECLARED STATUS says so.

    Scanning free prose was wrong: a document that merely DISCUSSES supersession
    (the Settled Canon Registry, any audit, any tombstone catalogue) would read
    as dead itself. Only the frontmatter status/title fields — the document's
    own self-declaration — count.
    """
    head = read(path, HEAD)
    fields = re.findall(r'^(?:status|title):\s*"?([^"\n]*)', head, re.M)
    # an H1 that literally announces a tombstone also counts as self-declaration
    h1 = re.findall(r'^#\s+(.{0,80})$', head, re.M)
    return any(DEAD_RE.search(f) for f in fields + h1)


def check(root):
    problems, scanned = [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            body = read(p)
            head = body[:HEAD]
            # a stub, an archive file, or audit machinery may cite the dead freely
            if STUB_RE.search(head) or MACHINERY_RE.search(rel) or is_dead(p):
                continue
            scanned += 1
            for lineno, line in enumerate(body.splitlines(), 1):
                for target in LINK_RE.findall(line):
                    if target.startswith("http") or "90_ARCHIVE" in target:
                        continue
                    tp = os.path.normpath(os.path.join(dirpath, target))
                    if not os.path.exists(tp) or not is_dead(tp):
                        continue
                    if DISCLOSED_RE.search(line):
                        continue                      # the citer already says so
                    status = ""
                    m = re.search(r'^(?:status|title):\s*"?([^"\n]{0,70})',
                                  read(tp, HEAD), re.M)
                    if m:
                        status = m.group(1).strip()
                    problems.append((rel, lineno, os.path.relpath(tp, root), status))
    return scanned, problems


def main(argv):
    roots = argv[1:] or [os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))]
    total, allp = 0, []
    for r in roots:
        if not os.path.isdir(r):
            print(f"not a directory: {r}", file=sys.stderr)
            return 2
        s, p = check(r)
        total += s
        allp.extend(p)
    if not allp:
        print(f"check_dead_citations: clean — {total} live document(s), "
              f"no undisclosed citation of a superseded target")
        return 0
    for rel, ln, tgt, status in allp:
        print(f"{rel}:{ln}: cites {tgt}")
        print(f"    which declares: {status[:70]}")
    print(f"\ncheck_dead_citations: {len(allp)} undisclosed dead citation(s) "
          f"across {total} live document(s)")
    print("A live index that sells a tombstone as a result is the corpus's named pathology.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
