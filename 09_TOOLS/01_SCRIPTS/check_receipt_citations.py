#!/usr/bin/env python3
"""Fail on receipt citations that cannot be trusted.

WHY THIS EXISTS. On 2026-07-30 `52_THE_GENERATIVE_BASE.md` cited a bare 180
prefix for an event that had no matching receipt. A grep-based check PASSED it, because `180_*` matched
an unrelated April document in a different folder. THE NUMBER RESOLVED — TO THE
WRONG FILE. That is the failure this script is built to catch, and it is only
possible because receipt numbers in this corpus are not unique identifiers.

TWO CLASSES, TREATED DIFFERENTLY.

  DANGLING    a cited number matches no receipt file anywhere. Unambiguously an
              error. FAILS the build.

  AMBIGUOUS   a cited number matches more than one file and none of them declares
              supersession. The citation may be resolving to the wrong document
              and nobody can tell. These are pre-existing and numerous, so they
              are held at a BASELINE THAT MAY NOT GROW — the same device
              check_established.py uses for its guarded exclusions. Adding a new
              collision fails; fixing one and forgetting to lower the baseline
              also fails, so the number cannot quietly drift in either direction.

A receipt escapes AMBIGUOUS by declaring `superseded_by:`, `supersedes:`,
`supersession_note:`, or a `status:` naming itself superseded/disputed/not-current.
`r139` is the model: the 07-19 file is marked DISPUTED PROVENANCE [B/D] with a
pointer at the 07-20 SIGNED [S] file, and the earlier is preserved as dissent.

THE RULE THIS ENFORCES: cite receipts BY PATH, not by number.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {"90_ARCHIVE", ".git", "node_modules", "__pycache__", ".vercel", "12_PUBLIC_SITE"}

# Collisions present at the latest dated namespace snapshot. MAY NOT GROW.
# Lower it only together with a landed disambiguation.
#
# 91 counts collisions ACROSS both receipt folders, which is the number that
# matters for citation: r156 names one document in 50_AUDITS_AND_EXECUTIONS and a
# different one in 60_SESSION_PACKETS, and "r156" cannot distinguish them. An
# earlier count of 26 looked only inside 50_AUDITS and therefore understated the
# defect by more than threefold.
# The move from 91 to 94 is bound by
# 243_PUBLIC_RELEASE_PREFLIGHT_AND_CONTACT_SNAPSHOT_2026_08_09.md. It records
# already-landed physical collisions; exact-path citation remains mandatory.
AMBIGUOUS_BASELINE = 94

SUPERSESSION = re.compile(
    r"^\s*(superseded_by|supersedes|supersession_note)\s*:"
    r"|^\s*status\s*:.*(supersed|DISPUTED|NOT CURRENT|dissent|CORRECTED)",
    re.I | re.M,
)
# bare r-plus-three-digit forms and explicit receipt-number phrases — but not r1 or a 4-digit year.
#
# THE BARE FORM REQUIRES THREE DIGITS. The Rosetta Stone material uses `R10`,
# `R12`, `R14` for its ROWS (see D19a_ROSETTA_R10_GREEK_PHILOLOGY.md) — a
# different namespace that happens to share the letter. Matching two digits bare
# reported 59 "dangling receipts" that were all Rosetta rows. Two-digit receipts
# are still checked through the explicit `receipt NN` form, which is unambiguous.
CITATION = re.compile(r"\br(\d{3})\b|\breceipt[ \t]+(\d{2,3})\b", re.I)
# `[ \t]+` NOT `\s+`: \s matches a newline, so "…has >= 1 receipt\n10. K4 Grace Exit"
# was read as a citation of "receipt 10". Found by running this checker on the corpus.


# Receipts live in these two folders only. Elsewhere a leading number is the
# corpus's ordinary document-ordering prefix (00_THE_FOUNDATION.md and friends),
# NOT a receipt id. An earlier draft of this script conflated the two and reported
# "r00 -> 248 files", which is the document convention, not a collision.
# TWO LIVE LANES. A council census found a third under 11_UPLINK/90_ARCHIVE (10 numbered
# files), but SKIP_DIRS excludes 90_ARCHIVE deliberately — archived receipts are not
# citable targets. Adding it to this tuple is a NO-OP and was reverted rather than left
# in place claiming coverage it does not have.
#
# THE SHARPER FINDING, which this checker cannot fix: BOTH live lanes begin at 100 and
# run over each other for a hundred consecutive integers. That is not scatter — it is two
# independent numbering schemes sharing one namespace, and no citation convention can
# repair it. Only a path can.
RECEIPT_DIRS = (
    Path("11_UPLINK") / "50_AUDITS_AND_EXECUTIONS",
    Path("11_UPLINK") / "60_SESSION_PACKETS",
)

# A citation inside a sentence that ASSERTS THE REFERENCE IS BROKEN is not itself a
# broken reference. Without this, documenting the defect trips the guard that exists
# to find it — and the honest record would be the thing the gate punished.
NEGATED = re.compile(
    r"no such receipt|never written|does not exist|do not exist|matches no|dangling|"
    r"was never|no receipt|MISSING|non-existent|nonexistent",
    re.I,
)
CLAUSE_BREAK = re.compile(
    r"(?:[.!?;][\"')\]]*\s+|\n\s*\n|,\s+(?=(?:but|however|whereas|while)\b))",
    re.I,
)
LIST_JOINER = re.compile(r"^[\s,]*(?:(?:and|or)[\s,]*)?$", re.I)


def citation_is_negated(text: str, citation: re.Match[str]) -> bool:
    """Apply a negation only to the citation or coordinated list it governs."""
    lo, hi = 0, len(text)
    for boundary in CLAUSE_BREAK.finditer(text):
        if boundary.end() <= citation.start():
            lo = boundary.end()
        elif boundary.start() >= citation.end():
            hi = boundary.start()
            break
    clause = text[lo:hi]
    citations = list(CITATION.finditer(clause))
    negations = list(NEGATED.finditer(clause))
    target_start = citation.start() - lo
    target_index = next(
        (
            index
            for index, match in enumerate(citations)
            if match.start() == target_start
        ),
        None,
    )
    if target_index is None:
        return False

    for negation in negations:
        def distance(match: re.Match[str]) -> int:
            if match.end() <= negation.start():
                return negation.start() - match.end()
            if negation.end() <= match.start():
                return match.start() - negation.end()
            return 0

        anchor = min(range(len(citations)), key=lambda index: (distance(citations[index]), index))
        first = last = anchor
        while first > 0 and LIST_JOINER.fullmatch(
            clause[citations[first - 1].end() : citations[first].start()]
        ):
            first -= 1
        while last + 1 < len(citations) and LIST_JOINER.fullmatch(
            clause[citations[last].end() : citations[last + 1].start()]
        ):
            last += 1
        if first <= target_index <= last:
            return True
    return False


def receipt_files() -> dict[str, list[Path]]:
    """Every numbered receipt, indexed by its number."""
    by_num: dict[str, list[Path]] = defaultdict(list)
    for d in RECEIPT_DIRS:
        base = ROOT / d
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            m = re.match(r"^(\d{2,3})[_A-Za-z]", p.name)
            # `00_` inside these folders is the index/readme convention
            # (00_README.md, 00_PACKET_INDEX.md), not a receipt id. Counting it
            # reported a 4-way "collision" that is really four index files.
            if m and m.group(1) != "00":
                by_num[m.group(1)].append(p)
    return by_num


def main() -> int:
    by_num = receipt_files()

    # --- A · which numbers are ambiguous? -----------------------------------
    ambiguous: dict[str, list[Path]] = {}
    for num, paths in by_num.items():
        if len(paths) < 2:
            continue
        undeclared = [
            p for p in paths
            if not SUPERSESSION.search(p.read_text(encoding="utf-8", errors="ignore")[:2500])
        ]
        if len(undeclared) > 1:
            ambiguous[num] = undeclared

    # --- B · dangling citations, scanned across the corpus ------------------
    dangling: list[str] = []
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for m in CITATION.finditer(text):
            num = m.group(1) or m.group(2)
            if num in by_num:
                continue
            line = text[: m.start()].count("\n") + 1
            if citation_is_negated(text, m):
                continue
            rel = p.relative_to(ROOT)
            dangling.append(f"{rel}:{line} cites r{num}, which matches no receipt file")

    errors: list[str] = []
    if dangling:
        errors.extend(dangling[:20])
        if len(dangling) > 20:
            errors.append(f"...and {len(dangling) - 20} more dangling citations")

    n = len(ambiguous)
    if n > AMBIGUOUS_BASELINE:
        worst = sorted(ambiguous.items(), key=lambda kv: -len(kv[1]))[:4]
        errors.append(
            f"ambiguous receipt numbers rose to {n} (baseline {AMBIGUOUS_BASELINE}). "
            "A new collision was introduced. Give the new file a free number, or "
            "declare supersession. Worst: "
            + "; ".join(f"r{k} -> {len(v)} files" for k, v in worst)
        )
    elif n < AMBIGUOUS_BASELINE:
        errors.append(
            f"ambiguous receipt numbers FELL to {n} (baseline {AMBIGUOUS_BASELINE}) — good, "
            "but lower AMBIGUOUS_BASELINE in this file to lock the gain in. A baseline "
            "that is not tightened lets the count drift back up unnoticed."
        )

    if errors:
        print("RECEIPT CITATIONS: FAIL")
        for e in errors:
            print(f"- {e}")
        return 1

    print(
        f"RECEIPT CITATIONS: PASS (0 dangling; {n} ambiguous numbers held at baseline "
        f"{AMBIGUOUS_BASELINE}; {sum(len(v) for v in by_num.values())} receipt files scanned)"
    )
    print(
        "  scope: this proves no citation points at NOTHING. It does NOT prove a citation "
        "points at the RIGHT file — with numbers reused, only a path can do that."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
