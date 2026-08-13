#!/usr/bin/env python3
"""Slice the private Manifesto into a STAGED public-current-body manuscript.

This is not a public edition. It does not write under 12_PUBLIC_SITE/.
It does not retarget build_book.py CURRENT_WORK_ID.
It excludes research (ch12–15), genealogy (ch16), appendices, and Reciprocal.

G10 remains unpaid. A green extract is not a release.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFESTO = ROOT / "13_BOOKS" / "manifesto"
SOURCE = MANIFESTO / "MANIFESTO_BOOK_1.md"
OUTPUT = MANIFESTO / "PUBLIC_CURRENT_BODY_STAGED.md"
RECEIPT = MANIFESTO / "PUBLIC_CURRENT_BODY_STAGED.json"

# Inclusive start markers (first match). Exclusive end markers.
CORE_START = "# The Emergentist Manifesto"
CORE_END = "# Part IV — The Frontier Stated Honestly"
EXIT_START = "## 17. Exit, Record, and the Right to Put It Down"
EXIT_END = "# Appendices and Reader Worksheets"

FORBIDDEN = (
    "# Part IV — The Frontier Stated Honestly",
    "## 12. Titans and Finity",
    "## 13. What Translation",
    "## 14. Accountable Action",
    "## 15. Six Lenses",
    "## 16. What the Genealogy",
    "Appendix D —",
    "RIP01-",
)

BANNER = """---
title: "The Emergentist Manifesto — public current-body (STAGED)"
status: "STAGED PRIVATE EXTRACT — not public, not deployed, G10 unpaid"
authority: "projection only; K-1 through K-7 retain semantic ownership"
source: "13_BOOKS/manifesto/MANIFESTO_BOOK_1.md"
extractor: "09_TOOLS/02_COMPILERS/extract_manifesto_public_current_body.py"
public_disposition: "not_a_public_route"
---

# STAGED — do not publish

This file is the candidate **public current-body** of Book I:
Preamble + chapters 1–11 + 17.

It is **not** the 17-chapter private manuscript.
It is **not** a `/book/` replacement.
It does **not** contain research chapters 12–15, genealogy chapter 16,
appendices, or Reciprocal custody prose.

G10 (fresh-reader, hostile review, public parity, predeploy, immutable
artifact, host/DNS, explicit public-release approval) remains unpaid.
A green extract is not the Amrita. It is firewood, stacked off-stage.

---

"""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def slice_body(text: str) -> str:
    if CORE_START not in text:
        raise SystemExit(f"missing start marker: {CORE_START}")
    if CORE_END not in text:
        raise SystemExit(f"missing core end marker: {CORE_END}")
    if EXIT_START not in text:
        raise SystemExit(f"missing exit start marker: {EXIT_START}")
    if EXIT_END not in text:
        raise SystemExit(f"missing exit end marker: {EXIT_END}")

    core = text[text.index(CORE_START) : text.index(CORE_END)].rstrip() + "\n"
    exit_ch = text[text.index(EXIT_START) : text.index(EXIT_END)].rstrip() + "\n"
    body = core.rstrip() + "\n\n" + exit_ch
    # Public-slice seams: ch.17 of the full book points at research/genealogy
    # that precede it there. Those chapters are excluded here. Reseat the
    # pointers so the extract does not pretend the missing apparatus is attached.
    seams = (
        (
            "It does not ask a reader to\n"
            "accept the research proposals or historical apparatus that precede it.",
            "It does not ask a reader to\n"
            "accept research proposals or historical apparatus. Those layers live in\n"
            "the private full manuscript and are not part of this current-body extract.",
        ),
        (
            "This matters especially for a project that includes\n"
            "research and genealogy.",
            "This matters especially for a project that keeps\n"
            "research and genealogy in a private manuscript, off this current-body.",
        ),
        (
            "it does not make a\nresearch card current.",
            "it does not make a\n"
            "research card current. This extract contains no research, historical, or custody chapters.",
        ),
    )
    for old, new in seams:
        if old not in body:
            raise SystemExit(f"expected public-slice seam missing:\n{old}")
        body = body.replace(old, new, 1)
    for needle in FORBIDDEN:
        if needle in body:
            raise SystemExit(f"forbidden marker leaked into extract: {needle}")
    return body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing extract")
    args = parser.parse_args(argv)

    source = SOURCE.read_text(encoding="utf-8")
    body = slice_body(source)
    page = BANNER + body
    words = len(re.findall(r"\w+", body))
    receipt = {
        "schema": "emergentism/manifesto-public-current-body/v1",
        "status": "staged_not_public",
        "g10": "unpaid",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": sha256_bytes(source.encode("utf-8")),
        "output": str(OUTPUT.relative_to(ROOT)),
        "included": [
            "preamble_quickstart",
            "ch01_finite_predicament",
            "ch02_frames_not_furniture",
            "ch03_record_and_possibility",
            "ch04_soul_loop",
            "ch05_finity_card",
            "ch06_justice_chosen",
            "ch07_conflict_and_residue",
            "ch08_social_loop",
            "ch09_thin_coordination",
            "ch10_institutions_can_end",
            "ch11_competition_without_war",
            "ch17_right_to_leave",
        ],
        "excluded": [
            "ch12_titans_research",
            "ch13_world_contact",
            "ch14_action_and_institution_research",
            "ch15_lenses_and_immune_protocol",
            "ch16_corrections_kept",
            "appendices",
        ],
        "word_count": words,
        "output_sha256": sha256_bytes(page.encode("utf-8")),
        "public_route": None,
        "retargets_book_builder": False,
    }

    if args.check:
        if not OUTPUT.exists() or not RECEIPT.exists():
            print("extract missing")
            return 1
        current = OUTPUT.read_text(encoding="utf-8")
        logged = json.loads(RECEIPT.read_text(encoding="utf-8"))
        if current != page or logged != receipt:
            print("extract drift")
            return 1
        print(f"extract clean ({words} words, staged, not public)")
        return 0

    OUTPUT.write_text(page, encoding="utf-8")
    RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({words} words, staged, not public)")
    print(f"wrote {RECEIPT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
