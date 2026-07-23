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

WHAT COUNTS AS DEAD — read from the target's own `status:` field, which is
authoritative. A title is a NAME, not a declared state.

  DEAD    SUPERSEDED · TOMBSTONE · RETRACTED · DISPUTED · DEPRECATED ·
          leading HISTORICAL · "not current ..." · "no current semantic authority"

  ALIVE   a status OPENING with ACTIVE / CURRENT / CANONICAL / LIVE — the dead
          word then names what this document REPLACES, not itself. This covers
          the Kintsugi pattern, which is the corpus's normal repair: the file
          keeps its historical path so inbound links survive, tombstones its own
          former blob, and carries the live content. "ACTIVE TOMBSTONE" is a
          LIVE OWNER. Also alive: "live owner repaired", "former X superseded",
          "KINTSUGI SUCCESSOR".

  EXCEPT  an explicit disclaimer beats every liveness marker: 25_STEEL_THREAD
          is repaired AND says "not current semantic authority" — dead.

Getting this wrong in the ALIVE direction is worse than missing a finding: it
sends readers away from the live owner, which is the very defect being hunted.
A thirteen-case suite over real corpus files pins both directions.

WHAT IS NOT A FINDING:
  - the citing document is itself a stub, an archive file, or audit machinery
    (a tombstone may freely cite tombstones)
  - the citing line ALREADY discloses the status — it contains one of the dead
    words, or "was", "formerly", "retired", "stub", "legacy", "historical", ...
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
    # "HISTORICAL — not current force canon" disclaims authority without ever
    # using the word "authority"; requiring that word let 09A read as live.
    r"^HISTORICAL\b|\bnot current\b|no current semantic authority", re.I)
DISCLOSED_RE = re.compile(
    r"SUPERSEDED|TOMBSTONE|RETRACTED|DISPUTED|DEPRECATED|\bwas\b|formerly|"
    r"retired|grave|historical|provenance|archived|dead|killed|withdrawn|"
    r"\bstubs?\b|no longer|not current|absorbed|legacy", re.I)
ALIVE_RE = re.compile(r"(ACTIVE|CURRENT|CANONICAL|LIVE)\b", re.I)
# the dead word names something OTHER than this file, or this file is the owner
LIVE_MARK_RE = re.compile(r"\blive owner\b|\bformer\b|KINTSUGI SUCCESSOR", re.I)
# an explicit disclaimer of authority beats every liveness marker
DISCLAIMS_RE = re.compile(
    r"no current semantic authority|\bnot current\b|not canonical authority", re.I)
STUB_RE = re.compile(
    # SINGULAR only. A self-declaration is "forwarding stub"; a receipt
    # describing its own work says "20 files, each leaving a forwarding
    # stubs" / "Compatibility stubs are not clutter" — plural, about
    # stubs in general, not about itself. Two 2026-07-22 false positives
    # (a 26-line execution receipt and a 237-line packet) turned on this.
    r"FORWARDING STUB(?!S)|Compatibility stub(?!s)|forwarding-stub(?!s)|"
    r"HISTORICAL FORWARDING", re.I)
MACHINERY_RE = re.compile(r"AUDIT|RECEIPT|TIDY_PLAN|CENSUS|_LEDGER|HANDOFF|CITATION", re.I)
SKIP_DIRS = {"90_ARCHIVE", "node_modules", ".git", ".lake",
             ".codex-worktrees", ".claude", "book-pwa", ".vercel", "__pycache__"}
# .claude holds nested git worktrees (.claude/worktrees/<name>/) — full repo
# mirrors. Scanning one doubles every count and re-surfaces already-repaired
# findings from the mirror as if they were live corpus. A worktree is never
# the live tree. .codex-worktrees is a SIBLING of the repo so it was never
# walked; .claude sits INSIDE the root and was, until 2026-07-23.
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
    # STATUS is authoritative. A title is a NAME, not a declared state:
    # 21_TRIADIC is titled "… — Kintsugi Tombstone" while its status reads
    # "ACTIVE TOMBSTONE", and the file is 55 lines of live mathematics. Judging
    # by whichever field matched first made the name outrank the declaration.
    status = re.findall(r'^status:\s*"?([^"\n]*)', head, re.M)
    if status:
        fields = status
    else:
        fields = (re.findall(r'^title:\s*"?([^"\n]*)', head, re.M)
                  + re.findall(r'^#\s+(.{0,80})$', head, re.M))
    for f in fields:
        if not DEAD_RE.search(f):
            continue
        # A status that OPENS with ACTIVE/CURRENT/CANONICAL is alive, and any
        # dead word after it describes what this document SUPERSEDES, not
        # itself: "ACTIVE — E1-E10 successor axiom set; A1-A7 is superseded".
        #
        # This includes "ACTIVE TOMBSTONE" and "ACTIVE KINTSUGI TOMBSTONE".
        # Kintsugi in this corpus means REPAIRED IN PLACE: the file keeps its
        # historical path so inbound links survive, tombstones its own former
        # blob, and carries the live content. 21_TRIADIC_STABILITY reads
        # "ACTIVE TOMBSTONE — invalid uniqueness proof superseded" and is 55
        # lines of live mathematics with a kill criterion. Calling it a grave
        # sends readers away from the live owner — the exact inversion of the
        # defect this gate exists to catch.
        #
        # Same for a status naming the dead thing as FORMER ("former
        # Titan-operation reading superseded"), or declaring a LIVE OWNER
        # ("KINTSUGI-SUPERSEDED PROOF — live owner repaired 2026-07-17").
        #
        # A repaired file is still dead if it explicitly disclaims authority:
        # 25_STEEL_THREAD carries date_repaired AND says "not current semantic
        # authority". That disclaimer wins over every liveness marker.
        if DISCLAIMS_RE.search(f):
            return True
        if ALIVE_RE.match(f.strip()) or LIVE_MARK_RE.search(f):
            continue
        return True
    return False


def _positions(hay, needle):
    """every index at which needle occurs in hay"""
    out, i = [], hay.find(needle)
    while i != -1:
        out.append(i)
        i = hay.find(needle, i + 1)
    return out


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
            lines = body.splitlines()
            for lineno, line in enumerate(lines, 1):
                for target in LINK_RE.findall(line):
                    if target.startswith("http") or "90_ARCHIVE" in target:
                        continue
                    tp = os.path.normpath(os.path.join(dirpath, target))
                    if not os.path.exists(tp) or not is_dead(tp):
                        continue
                    if DISCLOSED_RE.search(line):
                        continue                      # the citer already says so
                    # A table of four rows all pointing at the same grave does
                    # not want four identical footnotes. One route note above
                    # the table is better writing, and the reader meets it
                    # BEFORE any link. Accept it — but only when the note names
                    # this same target, so a disclosure about one file can never
                    # silently clear a different one.
                    # Real route notes wrap: the filename lands on one line and
                    # "SUPERSEDED" on the next. Requiring both on a single line
                    # missed every hand-written block. Join the window and bind
                    # them by PROXIMITY — a disclosure word within 240 chars of
                    # the target's name — so a disclosure about one file still
                    # cannot clear a different one further down the page.
                    name = os.path.basename(target)
                    # span the whole sentence: a disclosure can land either side of a
# wrapped link ("This pointer formerly named [X]\n as the active
# owner. That is no longer accurate: ...").
                    # BACKWARD ONLY, deliberately. Widening the window forward
                    # to catch a disclosure that lands after a wrapped link
                    # made a note about one file clear the NEXT row pointing at
                    # a different grave — proximity alone cannot tell which
                    # target a nearby sentence is about. A missed finding is
                    # cheap; a silently cleared one is the defect itself.
                    window = "\n".join(lines[max(0, lineno - 16):lineno - 1])
                    if any(DISCLOSED_RE.search(window, max(0, i - 240), i + 240)
                           for i in _positions(window, name)):
                        continue
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
