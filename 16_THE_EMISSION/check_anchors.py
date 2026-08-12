#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_anchors.py — the anchor gate for 16_THE_EMISSION.

THE LAW THIS GATE ENFORCES
--------------------------
    NO line-number citations. EVER. QUOTE-ANCHORED ONLY: path + the exact string.

The corpus wrote this rule for itself and did not apply it to itself.
`14_THE_DISTILLATION/01_WHAT_IS_PROVED.md` says:

    "for a sentence this load-bearing, cite by unique path plus a quoted string,
     never by a bare line range"

A quoted anchor survives insertion, reflow, frontmatter and reordering.
A line number survives none of them.

WHAT THIS GATE DOES
-------------------
1. Reads every .md under the emission root and extracts every citation into the
   frozen tree: a PATH token paired with a QUOTED STRING.
2. Resolves the path against the frozen corpus and confirms the quoted string
   occurs in that file. Exact match, whitespace-normalised.
3. FAILS (exit 1) if any anchor does not resolve — listing source file and quote.
4. FAILS (exit 1) on ANY line-number citation form found in the emission's own
   prose.
5. FAILS (exit 1) if a frozen-tree path is cited with no quoted string attached
   (an unanchored citation is the banned form with the number left off).
6. FAILS (exit 1) if it finds nothing to check. A gate that passes on empty input
   is the failure mode this gate exists to prevent.
7. Exits 0 with a PASS line and the counts when everything resolves.

ANCHOR GRAMMAR ACCEPTED
-----------------------
A PATH token is a corpus-relative path, normally in backticks:
    `05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md`
A QUOTE token is the exact string, in straight quotes, curly quotes, guillemets,
or a markdown blockquote.
The two must sit within PAIR_WINDOW characters of each other; either order works:
    `path.md` — "the exact string"
    "the exact string" — `path.md`
    `path.md`
    > the exact string
One path may carry several quotes; every one of them is checked.

WHAT IS DELIBERATELY NOT SCANNED, AND WHY
-----------------------------------------
* The interior of a quoted anchor. Quoted material is verbatim inheritance from a
  tree that is full of line citations; banning the emission from quoting it would
  ban the emission from telling the truth. Hits inside quotes are still COUNTED
  AND PRINTED as warnings — masked, never hidden.
* Fenced code blocks. Same treatment: warned, not hidden.
* This file. It contains the banned patterns as regexes. Only text-bearing
  documents are scanned; .py is excluded and the exclusion is printed.

KNOWN BLIND SPOT, NAMED ON PURPOSE
----------------------------------
The form `N:NN` where both sides are one or two digits is reported as a WARNING,
not a failure, because it is ambiguous with a clock time. A two-digit document
number with a two-digit line number would slip through as a warning. It is
printed every run so it cannot slip through silently.

USAGE
-----
    python3 check_anchors.py                 # check the tree this file sits in
    python3 check_anchors.py --root DIR      # check another copy
    python3 check_anchors.py --corpus DIR    # point at a different frozen tree
    python3 check_anchors.py --verbose       # list every anchor checked
    python3 check_anchors.py --self-test     # prove the gate can go red, then run

This file writes nothing outside a temp directory, and only under --self-test.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------

FALLBACK_CORPUS = Path("/Users/Yves/Documents/01_EMERGENTISM")

# how far apart a path token and its quote may sit, in characters
PAIR_WINDOW = 500

# an anchor quote shorter than this cannot identify anything
MIN_QUOTE_CHARS = 8

# extensions scanned for the banned form (.py excluded: this file is a .py and
# holds the banned patterns as regexes)
SCANNED_EXT = {".md", ".txt", ".jsonl", ".json", ".yaml", ".yml"}

# extensions a citation may target
CITABLE_EXT = "md|py|txt|jsonl|json|yaml|yml|csv|html|js|ts|toml|cfg|sh"

# --------------------------------------------------------------------------
# normalisation
# --------------------------------------------------------------------------

_WS = re.compile(r"\s+")
_SOFT = {" ": " ", " ": " ", " ": " ", "​": "", "﻿": ""}


def norm_ws(s: str) -> str:
    """Whitespace-normalised exact form. This is the matching contract."""
    s = unicodedata.normalize("NFC", s)
    for k, v in _SOFT.items():
        s = s.replace(k, v)
    return _WS.sub(" ", s).strip()


def norm_lenient(s: str) -> str:
    """Same, plus markdown emphasis and escapes removed from BOTH sides.

    Used only as a second attempt, and a match found this way is reported as a
    warning, never as a clean pass.
    """
    s = norm_ws(s)
    s = re.sub(r"\\(.)", r"\1", s)
    s = s.replace("*", "").replace("_", "").replace("`", "")
    return _WS.sub(" ", s).strip()


# --------------------------------------------------------------------------
# token extraction
# --------------------------------------------------------------------------

FENCE_RE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.S | re.M)
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*\n", re.S)

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PATH_SHAPE_RE = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_./+\-]*\.(?:" + CITABLE_EXT + r")$"
)
BARE_PATH_RE = re.compile(
    r"(?<![\w`/.])"
    r"((?:[A-Za-z0-9_][A-Za-z0-9_.+\-]*/)+[A-Za-z0-9_][A-Za-z0-9_.+\-]*"
    r"\.(?:" + CITABLE_EXT + r")"
    r"|[A-Za-z0-9_][A-Za-z0-9_.+\-]*\.md)"
    r"(?![\w`])"
)

QUOTE_RES = [
    re.compile(r"“([^”]{1,600}?)”", re.S),
    re.compile(r"«([^»]{1,600}?)»", re.S),
]
BLOCKQUOTE_RE = re.compile(r"(?:^[ \t]*>[^\n]*\n?)+", re.M)
LIST_START_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]")

# --- the banned forms ------------------------------------------------------
# B1  path with an extension, then :line          FILE.md:124   FILE.md:15-26
BAN_EXT_LINE = re.compile(
    r"[A-Za-z0-9_][A-Za-z0-9_./+\-]*\.(?:" + CITABLE_EXT + r"):\d+"
)
# B2  bare colon-line                             at `:246`   , :82-83
BAN_BARE_COLON = re.compile(
    r"(?:^|[\s`(\[{«\"'—–,;→>])(:\d+(?:\s*[-–,]\s*\d+)*)"
)
# B3  identifier or 3+ digit number, then :line   RUNGS:722   193:15-17   55:156
BAN_IDENT_LINE = re.compile(
    r"(?<![\w:])(?:[A-Za-z_][A-Za-z0-9_]*|\d{3,}):\d+(?:\s*[-–,]\s*\d+)*"
    r"|(?<![\w:])\d{1,2}:\d+\s*[-–,]\s*\d+"
    r"|(?<![\w:])\d{1,2}:\d{3,}"
)
HARD_BANS = [("B1 path:line", BAN_EXT_LINE),
             ("B2 bare :line", BAN_BARE_COLON),
             ("B3 ident:line", BAN_IDENT_LINE)]

# --- warned, not failed: the named blind spot ------------------------------
WARN_CLOCKLIKE = re.compile(r"(?<![\w:])\d{1,2}:\d{2}(?![\d:])")
WARN_LINE_WORD = re.compile(r"\blines?\s+\d+(?:\s*[-–]\s*\d+)?\b", re.I)

# B3 fires on ordinary URLs and a few prose shapes; exempt those exactly.
BAN_EXEMPT = re.compile(r"^(?:https?|ftp|file|mailto|git|ssh)$", re.I)

# A DECLARED DROP: the document names a file and states that no string in it
# could be verified, so no anchor was written. That is a disclosure, not a
# citation. Failing it would push the author to delete the disclosure — the gate
# would then be destroying the honesty it exists to protect. Exempt, but every
# one is COUNTED AND ITEMISED in the output, so the escape cannot be used
# quietly. The exemption is line-scoped: it covers only the line that carries
# the marker.
DECLARED_DROP_RE = re.compile(
    r"\{no-anchor\}"
    r"|no anchor (?:was )?written"
    r"|citations? dropped"
    r"|dropped as unverifiable"
    r"|named but not anchored"
    r"|unverifiable[^.\n]{0,40}no anchor",
    re.I,
)


def line_span(text: str, pos: int):
    a = text.rfind("\n", 0, pos) + 1
    b = text.find("\n", pos)
    return a, (len(text) if b == -1 else b)


def block_span(text: str, pos: int):
    """The blank-line-delimited block containing pos.

    The declared-drop marker is scoped to this block, so one caption can cover
    the rows of one table. Wider than a line, and still bounded and itemised.
    """
    a = text.rfind("\n\n", 0, pos)
    a = 0 if a == -1 else a + 2
    b = text.find("\n\n", pos)
    return a, (len(text) if b == -1 else b)


class Tok:
    __slots__ = ("kind", "text", "start", "end")

    def __init__(self, kind, text, start, end):
        self.kind, self.text, self.start, self.end = kind, text, start, end

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"<{self.kind} {self.start}:{self.end} {self.text[:40]!r}>"


class QGroup:
    """One quotation site, with every defensible reading of it.

    Straight double quotes nest in this corpus — a heading being quoted may
    itself contain a quoted phrase:

        - `path.md` — "### P-22 · DF-22 — "the escorted number""

    No quote-delimited grammar parses that unambiguously, so the gate does not
    guess. It carries BOTH readings and requires one of them to resolve whole:
      alt 1 — consecutive inner pairs, ALL of which must resolve
      alt 2 — outermost open to outermost close, which must resolve
    A site where no reading resolves is a failure, reported with the longest
    candidate so the author can see what was attempted.
    """
    __slots__ = ("start", "end", "alts", "ambiguous")

    def __init__(self, start, end, alts, ambiguous=False):
        self.start, self.end = start, end
        self.alts = [a for a in alts if a]
        self.ambiguous = ambiguous

    @property
    def longest(self):
        best = ""
        for alt in self.alts:
            for q in alt:
                if len(q) > len(best):
                    best = q
        return best

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"<QGroup {self.start}:{self.end} {self.longest[:40]!r}>"


def _straight_quote_groups(scan: str):
    """Line-scoped parse of straight double quotes, plus wrapped-line pairs."""
    groups = []
    lines = scan.split("\n")
    offs, pos = [], 0
    for ln in lines:
        offs.append(pos)
        pos += len(ln) + 1

    singles = []  # (line_index, offset_of_quote_char)
    for i, (ln, off) in enumerate(zip(lines, offs)):
        qs = [j for j, ch in enumerate(ln) if ch == '"']
        if len(qs) == 1:
            singles.append((i, off + qs[0]))
            continue
        if len(qs) < 2:
            continue
        inner = []
        for k in range(0, len(qs) - 1, 2):
            body = ln[qs[k] + 1:qs[k + 1]]
            if body.strip():
                inner.append(body)
        outer = ln[qs[0] + 1:qs[-1]]
        alts = []
        if inner:
            alts.append(inner)
        if outer.strip() and (not inner or [outer] != inner):
            alts.append([outer])
        if alts:
            groups.append(QGroup(off + qs[0], off + qs[-1] + 1, alts,
                                 ambiguous=len(qs) % 2 == 1 or len(qs) > 2))

    # a quote wrapped over a line break: exactly one " on each of two lines,
    # with nothing structural in between
    used = set()
    for a in range(len(singles) - 1):
        if a in used:
            continue
        li, pa = singles[a]
        lj, pb = singles[a + 1]
        if lj - li > 3:
            continue
        between = lines[li + 1:lj]
        if any(not b.strip() for b in between):
            continue
        if any(LIST_START_RE.match(b) or b.lstrip().startswith("#")
               for b in between):
            continue
        body = scan[pa + 1:pb]
        if "`" in body and re.search(r"\.\w{2,5}`", body):
            continue  # a path token inside: this is a cascade, not a quote
        if body.strip():
            groups.append(QGroup(pa, pb + 1, [[body]]))
            used.add(a)
            used.add(a + 1)
    return groups


def mask_spans(text: str, spans):
    """Blank out spans, preserving offsets and newlines."""
    out = list(text)
    for a, b in spans:
        for i in range(a, min(b, len(out))):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def line_of(text: str, pos: int) -> int:
    """Only ever used to point a human at a failure. Never emitted as a citation."""
    return text.count("\n", 0, pos) + 1


HEADING_RE = re.compile(r"^[ \t]*#{1,6}[ \t]", re.M)


def extract_tokens(text: str):
    """Return (path_tokens, quote_tokens, fence_spans, frontmatter_span).

    Fenced blocks and YAML frontmatter are masked before tokenising: neither is
    a citation site. They are still scanned for the banned form.
    """
    fence_spans = [m.span() for m in FENCE_RE.finditer(text)]
    fm = FRONTMATTER_RE.match(text)
    fm_span = fm.span() if fm else None

    scan = mask_spans(text, fence_spans + ([fm_span] if fm_span else []))

    quotes = _straight_quote_groups(scan)
    taken = [(g.start, g.end) for g in quotes]
    for rx in QUOTE_RES:
        for m in rx.finditer(scan):
            body = m.group(1)
            if "\n\n" in body:
                continue
            if any(a < m.end() and m.start() < b for a, b in taken):
                continue
            taken.append(m.span())
            quotes.append(QGroup(m.start(), m.end(), [[body]]))
    for m in BLOCKQUOTE_RE.finditer(scan):
        if any(a < m.end() and m.start() < b for a, b in taken):
            continue
        body = "\n".join(
            re.sub(r"^[ \t]*>[ \t]?", "", ln) for ln in m.group(0).splitlines()
        ).strip()
        if body:
            taken.append(m.span())
            quotes.append(QGroup(m.start(), m.end(), [[body]]))

    paths = []
    seen = []
    for m in BACKTICK_RE.finditer(scan):
        raw = m.group(1).strip()
        cand = re.split(r"\s+[§#]", raw)[0].strip()
        cand = cand.split("#")[0].strip()
        if PATH_SHAPE_RE.match(cand):
            if any(a < m.end() and m.start() < b for a, b in taken):
                continue  # inside a quotation: quoted material, not a citation
            paths.append(Tok("path", cand, m.start(), m.end()))
            seen.append(m.span())
    for m in BARE_PATH_RE.finditer(scan):
        if any(a <= m.start() and m.end() <= b for a, b in seen):
            continue
        if any(a <= m.start() and m.end() <= b for a, b in taken):
            continue  # inside a quote: that is quoted material, not a citation
        paths.append(Tok("path", m.group(1), m.start(), m.end()))

    quotes.sort(key=lambda t: t.start)
    paths.sort(key=lambda t: t.start)
    return paths, quotes, fence_spans, fm_span


LEADIN_ONLY_RE = re.compile(r"^[\s\-—–:·•>*_]*$")


def pair(paths, quotes, text=""):
    """Attach quotes to paths. Returns (pairs, unanchored_paths).

    ATTACHMENT IS TIGHT ON PURPOSE. A quote belongs to a path only when the two
    are written as one citation:

      * on the SAME LINE, in either order, or
      * the quote opens in the block IMMEDIATELY following the path, with at
        most a short lead-in (<=120 chars, <=2 newlines, no heading) between
        them — the "`path.md` states it exactly:" + blockquote form.

    Anything looser lets ordinary prose — an editorial blockquote, a sentence
    that happens to quote something — be mistaken for an anchor, and the gate
    then fails the document for the gate's own parsing. Quotes that attach to no
    path are prose and are ignored; a PATH with no attached quote is the failure.
    NEAREST WINS among attachable candidates.
    """
    claimed = {id(p): [] for p in paths}
    for q in quotes:
        best, bestd = None, None
        for p in paths:
            if p.end <= q.start:
                gap = text[p.end:q.start]
                if "\n" in gap and not (
                        gap.count("\n") <= 2 and len(gap) <= 120
                        and not re.search(r"^[ \t]*#", gap, re.M)):
                    continue
                d = q.start - p.end
            elif q.end <= p.start:
                gap = text[q.end:p.start]
                if "\n" in gap:
                    continue
                d = p.start - q.end
            else:
                continue  # overlapping: a path inside a quote is quoted material
            if d > PAIR_WINDOW:
                continue
            if bestd is None or d < bestd:
                best, bestd = p, d
        if best is not None:
            claimed[id(best)].append(q)

    pairs, unanchored = [], []
    for p in paths:
        qs = claimed[id(p)]
        if qs:
            pairs.extend((p, q) for q in qs)
        else:
            unanchored.append(p)
    return pairs, unanchored


# --------------------------------------------------------------------------
# resolution
# --------------------------------------------------------------------------

class Resolver:
    def __init__(self, corpus: Path, emission: Path):
        self.corpus = corpus
        self.emission = emission
        self._basenames = None
        self._cache = {}

    def _index(self):
        if self._basenames is None:
            idx = {}
            for dirpath, dirnames, filenames in os.walk(self.corpus):
                dirnames[:] = [d for d in dirnames if d != ".git"]
                for fn in filenames:
                    if Path(fn).suffix.lstrip(".") in CITABLE_EXT.split("|"):
                        idx.setdefault(fn, []).append(Path(dirpath) / fn)
            self._basenames = idx
        return self._basenames

    def resolve(self, raw: str):
        """-> (status, path_or_none, note)

        status in {frozen, frozen_by_basename, intra, missing, ambiguous}
        """
        if raw in self._cache:
            return self._cache[raw]
        res = self._resolve(raw)
        self._cache[raw] = res
        return res

    def _resolve(self, raw: str):
        rel = raw.lstrip("./")
        # intra-emission first: those are not citations into the frozen tree
        for base in (self.emission,):
            cand = base / rel
            if cand.is_file():
                return ("intra", cand, "inside the emission")
        if rel.startswith("16_THE_EMISSION/"):
            cand = self.emission / rel[len("16_THE_EMISSION/"):]
            if cand.is_file():
                return ("intra", cand, "inside the emission")
        cand = self.corpus / rel
        if cand.is_file():
            return ("frozen", cand, "")
        if "/" not in rel:
            hits = self._index().get(rel, [])
            if len(hits) == 1:
                return ("frozen_by_basename", hits[0],
                        "resolved by unique basename; prefer the full "
                        "corpus-relative path")
            if len(hits) > 1:
                return ("ambiguous", None,
                        f"{len(hits)} files share this basename")
            return ("missing", None, "no such file under the frozen tree")
        # tolerate a leading 01_EMERGENTISM/
        if rel.startswith("01_EMERGENTISM/"):
            cand = self.corpus / rel[len("01_EMERGENTISM/"):]
            if cand.is_file():
                return ("frozen", cand, "")
        return ("missing", None, "no such file under the frozen tree")


_file_cache = {}


def read_text(p: Path) -> str:
    key = str(p)
    if key not in _file_cache:
        try:
            _file_cache[key] = p.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover
            _file_cache[key] = ""
            print(f"  ! could not read {p}: {exc}", file=sys.stderr)
    return _file_cache[key]


# --------------------------------------------------------------------------
# the check
# --------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.failures = []   # (kind, source, detail)
        self.warnings = []   # (kind, source, detail)
        self.counts = {}

    def fail(self, kind, source, detail):
        self.failures.append((kind, source, detail))

    def warn(self, kind, source, detail):
        self.warnings.append((kind, source, detail))


def closest_hint(quote: str, target_text: str) -> str:
    """On a miss, show what the target ACTUALLY says where the quote nearly matches.

    Diagnosis only. It never turns a failure into a pass — it exists so that a
    red gate is fixable instead of merely loud.
    """
    import difflib
    qn = norm_lenient(quote)
    cn = norm_lenient(target_text)
    if len(qn) < 8 or not cn:
        return ""
    sm = difflib.SequenceMatcher(None, cn, qn, autojunk=False)
    m = sm.find_longest_match(0, len(cn), 0, len(qn))
    if m.size < max(10, len(qn) // 4):
        return "no comparable text found in the target — wrong file?"
    lo = max(0, m.a - m.b - 30)
    hi = min(len(cn), m.a - m.b + len(qn) + 30)
    return (f"target actually says (longest common run {m.size}/{len(qn)} chars): "
            f"...{cn[lo:hi]}...")


def quote_resolves(quote: str, target: Path):
    """-> (ok, mode, occurrences). mode: 'exact' | 'lenient' | 'short' | None."""
    content = read_text(target)
    qn = norm_ws(quote)
    if len(qn) < MIN_QUOTE_CHARS:
        return (False, "short", 0)
    cn = norm_ws(content)
    if qn in cn:
        return (True, "exact", cn.count(qn))
    ql, cl = norm_lenient(quote), norm_lenient(content)
    if ql and ql in cl:
        return (True, "lenient", cl.count(ql))
    return (False, None, 0)


def check_quote(quote: str, target: Path, report: Report, src: str, disp: str):
    """Single-quote check, used by the ledger. -> True if it resolves."""
    ok, mode, n = quote_resolves(quote, target)
    qn = norm_ws(quote)
    if ok:
        if mode == "lenient":
            report.warn("matched only after markdown emphasis stripped", src,
                        f"{disp} :: {qn[:90]!r}")
        if n > 1:
            report.warn("anchor quote not unique in target", src,
                        f"{disp} :: appears {n}x :: {qn[:80]!r}")
        return True
    if mode == "short":
        report.fail("anchor quote too short", src,
                    f"{disp} :: {qn!r} is {len(qn)} chars; "
                    f"an anchor needs at least {MIN_QUOTE_CHARS}")
        return False
    hint = closest_hint(quote, read_text(target))
    report.fail("ANCHOR DOES NOT RESOLVE", src,
                f"{disp} :: quote not found :: {qn[:160]!r}"
                + (f"\n      {hint}" if hint else ""))
    return False


def check_group(g: "QGroup", target: Path, report: Report, src: str, disp: str):
    """Check one quotation site. -> list of quotes that resolved (empty = fail)."""
    best_alt, best_score = None, -1
    for alt in g.alts:
        results = [quote_resolves(q, target) for q in alt]
        if all(r[0] for r in results):
            for q, (_, mode, n) in zip(alt, results):
                if mode == "lenient":
                    report.warn("matched only after markdown emphasis stripped",
                                src, f"{disp} :: {norm_ws(q)[:90]!r}")
                if n > 1:
                    report.warn("anchor quote not unique in target", src,
                                f"{disp} :: appears {n}x :: {norm_ws(q)[:80]!r}")
            if g.ambiguous and len(g.alts) > 1:
                report.warn("nested quote characters at this anchor", src,
                            f"{disp} :: the site parses more than one way; the "
                            f"reading that resolved was "
                            f"{[norm_ws(q)[:60] for q in alt]} — consider "
                            f"single-nesting so the anchor has one reading")
            return alt
        score = sum(1 for r in results if r[0])
        if score > best_score:
            best_alt, best_score = alt, score
    q = g.longest
    ok, mode, _ = quote_resolves(q, target)
    if mode == "short" and len(g.alts) == 1:
        report.fail("anchor quote too short", src,
                    f"{disp} :: {norm_ws(q)!r} is {len(norm_ws(q))} chars; "
                    f"an anchor needs at least {MIN_QUOTE_CHARS}")
        return []
    hint = closest_hint(q, read_text(target))
    extra = ""
    if len(g.alts) > 1:
        extra = (f"\n      site parses {len(g.alts)} ways; none resolved whole. "
                 f"best partial: {best_score}/{len(best_alt or [])} parts")
    report.fail("ANCHOR DOES NOT RESOLVE", src,
                f"{disp} :: quote not found :: {norm_ws(q)[:160]!r}"
                + (f"\n      {hint}" if hint else "") + extra)
    return []


def scan_banned(text: str, quotes, fence_spans, path_disp, report: Report):
    """Hard-fail on line-number citation forms in the emission's own prose."""
    quote_spans = [(q.start, q.end) for q in quotes]
    masked = mask_spans(text, list(fence_spans) + quote_spans)

    hits = []  # one occurrence -> one failure, even when several patterns fire
    for label, rx in HARD_BANS:
        for m in rx.finditer(masked):
            head = m.group(0).split(":")[0].strip(" `([{\"'")
            if BAN_EXEMPT.match(head):
                continue
            hits.append((m.start(), m.end(), label,
                         (m.group(1) if m.lastindex else m.group(0)).strip()))
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    kept = []
    for h in hits:
        if any(k[0] <= h[0] and h[1] <= k[1] for k in kept):
            continue
        kept.append(h)
    for a, b, label, hit in kept:
        report.fail("BANNED LINE-NUMBER CITATION", path_disp,
                    f"{label} :: {hit!r} "
                    f"(document line {line_of(text, a)}) :: "
                    f"context: {masked[max(0, a - 60):b + 40].strip()!r}")

    for m in WARN_CLOCKLIKE.finditer(masked):
        report.warn("possible line citation (N:NN, ambiguous with a clock time)",
                    path_disp,
                    f"{m.group(0)!r} at document line {line_of(text, m.start())} "
                    f"— confirm it is a time, not a citation")
    for m in WARN_LINE_WORD.finditer(masked):
        report.warn("prose line reference", path_disp,
                    f"{m.group(0)!r} at document line {line_of(text, m.start())} "
                    f"— a named 'Line 4' is fine, a line number is not")

    # masked regions: counted and printed, never hidden
    inq = 0
    for a, b in quote_spans:
        seg = text[a:b]
        inq += sum(len(rx.findall(seg)) for _, rx in HARD_BANS)
    infence = 0
    for a, b in fence_spans:
        seg = text[a:b]
        infence += sum(len(rx.findall(seg)) for _, rx in HARD_BANS)
    if inq:
        report.warn("banned form inside quoted material", path_disp,
                    f"{inq} occurrence(s) — verbatim inheritance, not this "
                    f"document's own citation form; not failed, but counted")
    if infence:
        report.warn("banned form inside a fenced block", path_disp,
                    f"{infence} occurrence(s) — not failed, but counted")
    return inq + infence


def check_anchors_jsonl(path: Path, resolver: Resolver, report: Report, drops):
    """Validate the anchor ledger if one exists. Schema-tolerant on purpose."""
    checked = []
    PATH_KEYS = ("to_path", "path", "target_path", "target", "to", "file",
                 "doc", "locator", "source_path")
    QUOTE_KEYS = ("quote", "anchor", "text", "string", "exact", "exact_string",
                  "quoted_string")
    src = path.name
    raw = read_text(path)
    records = 0
    for i, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            report.fail("ANCHORS.jsonl is not valid JSONL", src,
                        f"record {i}: {exc}")
            continue
        if not isinstance(obj, dict):
            report.fail("ANCHORS.jsonl record is not an object", src,
                        f"record {i}")
            continue
        records += 1
        pk = next((k for k in PATH_KEYS if isinstance(obj.get(k), str)), None)
        qk = next((k for k in QUOTE_KEYS if isinstance(obj.get(k), str)), None)
        if pk is None or qk is None:
            report.fail("ANCHORS.jsonl record has no path+quote", src,
                        f"record {i}: keys={sorted(obj)} — need one of "
                        f"{PATH_KEYS} and one of {QUOTE_KEYS}")
            continue
        p, q = obj[pk], obj[qk]
        declared = obj.get("resolved") is False
        if not q.strip():
            if declared:
                drops.append((src, p, f"record {i}"))
            else:
                report.fail("ANCHORS.jsonl record has an empty quote", src,
                            f"record {i}: {p!r} — an empty anchor is not an "
                            f"anchor; either quote the target or mark the "
                            f"record resolved:false as a declared drop")
            continue
        if BAN_EXT_LINE.search(p) or ":" in p.rsplit("/", 1)[-1]:
            report.fail("BANNED LINE-NUMBER CITATION", src,
                        f"record {i}: path field carries a line number: {p!r}")
            continue
        status, target, note = resolver.resolve(p)
        if status in ("missing", "ambiguous"):
            report.fail("ANCHOR PATH DOES NOT RESOLVE", src,
                        f"record {i}: {p!r} — {note}")
            continue
        if status == "frozen_by_basename":
            report.warn("path resolved by basename", src, f"record {i}: {p!r}")
        if status == "intra":
            report.warn("ledger record points inside the emission", src,
                        f"record {i}: {p!r}")
        if declared:
            # the record says it does not resolve. Verify that claim too: a
            # quote that DOES resolve while flagged unresolved is a mislabel.
            ok, _, _ = quote_resolves(q, target)
            if ok:
                report.warn("ledger record marked resolved:false but the quote "
                            "resolves", src, f"record {i} -> {p}: {q[:80]!r}")
            else:
                drops.append((src, p, f"record {i}"))
            continue
        ok = check_quote(q, target, report, src, f"record {i} -> {p}")
        if ok:
            checked.append((norm_ws(p), norm_ws(q)))
    if records == 0:
        report.fail("ANCHORS.jsonl is empty", src,
                    "an anchor ledger that records nothing is worse than none")
    return checked, records


def run(emission: Path, corpus: Path, verbose: bool = False) -> int:
    report = Report()
    print("=" * 72)
    print("check_anchors.py — quote-anchored citation gate")
    print(f"  emission : {emission}")
    print(f"  corpus   : {corpus}")
    print("=" * 72)

    if not emission.is_dir():
        print(f"\nFAIL — emission root does not exist: {emission}")
        return 1
    if not corpus.is_dir():
        print(f"\nFAIL — frozen corpus root does not exist: {corpus}")
        return 1

    resolver = Resolver(corpus, emission)

    md_files = sorted(p for p in emission.rglob("*.md") if ".git" not in p.parts)
    other_scanned = sorted(
        p for p in emission.rglob("*")
        if p.is_file() and p.suffix in SCANNED_EXT and p.suffix != ".md"
        and ".git" not in p.parts
    )

    n_anchor_ok = 0
    n_frozen_paths = 0
    n_intra_paths = 0
    n_quotes = 0
    n_masked_hits = 0
    n_frontmatter_paths = 0
    md_anchor_keys = set()
    declared_drops = []          # prose: path named, no anchor written
    declared_drops_ledger = []   # ledger: record marked resolved:false

    for f in md_files:
        rel = f.relative_to(emission).as_posix()
        text = read_text(f)
        paths, quotes, fences, fm_span = extract_tokens(text)
        n_quotes += len(quotes)
        if fm_span:
            fmtxt = text[fm_span[0]:fm_span[1]]
            fmp = [m.group(1) for m in BACKTICK_RE.finditer(fmtxt)
                   if PATH_SHAPE_RE.match(m.group(1).strip())]
            fmp += [m.group(1) for m in BARE_PATH_RE.finditer(fmtxt)]
            if fmp:
                n_frontmatter_paths += len(fmp)
                report.warn("path in frontmatter is exempt from the anchor rule",
                            rel, f"{len(fmp)} path(s): {fmp[:4]} — frontmatter "
                                 f"is metadata, not a citation site; nothing "
                                 f"else in the document is exempt")
        n_masked_hits += scan_banned(text, quotes, fences, rel, report)

        pairs, unanchored = pair(paths, quotes, text)
        by_path = {}
        for p, q in pairs:
            by_path.setdefault(id(p), (p, []))[1].append(q)

        for p in paths:
            status, target, note = resolver.resolve(p.text)
            qs = by_path.get(id(p), (p, []))[1]

            if status == "intra":
                n_intra_paths += 1
                continue
            if status in ("missing", "ambiguous"):
                report.fail("CITED PATH DOES NOT RESOLVE", rel,
                            f"{p.text!r} — {note} "
                            f"(document line {line_of(text, p.start)})")
                continue

            n_frozen_paths += 1
            if status == "frozen_by_basename":
                report.warn("path resolved by basename", rel,
                            f"{p.text!r} — {note}")
            if not qs:
                a, b = block_span(text, p.start)
                if DECLARED_DROP_RE.search(text[a:b]):
                    declared_drops.append(
                        (rel, p.text, line_of(text, p.start)))
                    continue
                report.fail("UNANCHORED CITATION (no quoted string)", rel,
                            f"{p.text!r} at document line "
                            f"{line_of(text, p.start)} — cite by path plus a "
                            f"quoted string, always. If this reference is "
                            f"deliberately unanchored, say so in its block "
                            f"with {{no-anchor}} and it will be exempted and "
                            f"itemised.")
                continue
            for g in qs:
                for q in check_group(g, target, report, rel, p.text):
                    n_anchor_ok += 1
                    md_anchor_keys.add((norm_ws(p.text), norm_ws(q)))
                    if verbose:
                        print(f"  ok  {rel}  ->  {p.text}")
                        print(f"      {norm_ws(q)[:110]!r}")

    for f in other_scanned:
        if f.name == "ANCHORS.jsonl":
            continue
        rel = f.relative_to(emission).as_posix()
        text = read_text(f)
        _, quotes, fences, _ = extract_tokens(text)
        n_masked_hits += scan_banned(text, quotes, fences, rel, report)

    ledger = emission / "ANCHORS.jsonl"
    ledger_records = 0
    ledger_keys = []
    if ledger.is_file():
        ledger_keys, ledger_records = check_anchors_jsonl(
            ledger, resolver, report, declared_drops_ledger)
        lk = set(ledger_keys)
        missing = [k for k in md_anchor_keys if k not in lk]
        if missing:
            report.warn("anchors in prose but not in ANCHORS.jsonl",
                        "ANCHORS.jsonl",
                        f"{len(missing)} of {len(md_anchor_keys)} prose anchors "
                        f"are absent from the ledger")
    else:
        report.warn("no ANCHORS.jsonl", "-",
                    "no anchor ledger found at the emission root")

    total_checked = n_anchor_ok + len(ledger_keys)
    if not md_files:
        report.fail("NOTHING CHECKED", "-",
                    "no .md files under the emission root")
    elif total_checked == 0 and not report.failures:
        report.fail("NOTHING CHECKED", "-",
                    "no anchors into the frozen tree were found; a gate that "
                    "passes on empty input is the failure mode this gate exists "
                    "to prevent")

    # ---------------- output ----------------
    if report.warnings:
        print(f"\nWARNINGS ({len(report.warnings)}) — not fatal, printed so "
              f"nothing is silent:")
        for kind, src, detail in report.warnings:
            print(f"  ~ [{kind}] {src}")
            print(f"      {detail}")

    if report.failures:
        print(f"\nFAILURES ({len(report.failures)}):")
        for kind, src, detail in report.failures:
            print(f"  X [{kind}] {src}")
            print(f"      {detail}")
        tally = {}
        for kind, src, _ in report.failures:
            tally[(kind, src)] = tally.get((kind, src), 0) + 1
        print("\nFAILURES BY KIND AND FILE")
        for (kind, src), n in sorted(tally.items(), key=lambda kv: -kv[1]):
            print(f"  {n:4d}  {kind}  —  {src}")

    if declared_drops or declared_drops_ledger:
        n = len(declared_drops) + len(declared_drops_ledger)
        print(f"\nDECLARED DROPS ({n}) — the document names these targets and "
              f"states it could\nverify no string in them, so it wrote no anchor. "
              f"Exempt from the anchor rule,\nitemised here so the exemption is "
              f"never silent:")
        for rel, ptxt, ln in declared_drops:
            print(f"  - {rel} (document line {ln}) -> {ptxt}")
        for src, ptxt, rec in declared_drops_ledger:
            print(f"  - {src} {rec} -> {ptxt}")

    print("\nCOUNTS")
    print(f"  .md files scanned                : {len(md_files)}")
    print(f"  other text files scanned         : {len(other_scanned)}")
    print(f"  .py files scanned                : 0  (excluded: this gate holds "
          f"the banned patterns as regexes)")
    print(f"  quotation sites seen             : {n_quotes}")
    print(f"  frozen-tree path citations       : {n_frozen_paths}")
    print(f"  intra-emission path refs (skipped): {n_intra_paths}")
    print(f"  frontmatter paths (exempt)       : {n_frontmatter_paths}")
    print(f"  declared drops (prose)           : {len(declared_drops)}")
    print(f"  declared drops (ledger)          : {len(declared_drops_ledger)}")
    print(f"  anchors verified in prose        : {n_anchor_ok}")
    print(f"  ANCHORS.jsonl records            : {ledger_records}")
    print(f"  anchors verified in ledger       : {len(ledger_keys)}")
    print(f"  banned forms inside quotes/fences: {n_masked_hits}  (warned)")
    print(f"  warnings                         : {len(report.warnings)}")
    print(f"  failures                         : {len(report.failures)}")

    if report.failures:
        print(f"\nFAIL — {len(report.failures)} failure(s). "
              f"Exit 1. No anchor may be papered over.")
        return 1
    print(f"\nPASS — {total_checked} anchor(s) resolved, "
          f"0 line-number citations, 0 unresolved paths. Exit 0.")
    return 0


# --------------------------------------------------------------------------
# self-test: prove the gate can go red before trusting it green
# --------------------------------------------------------------------------

def _self_test(emission: Path, corpus: Path) -> int:
    """Mutate copies in a temp dir and require RED. Never touches the emission."""
    import io
    import contextlib

    def run_quiet(root):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = run(root, corpus)
        return rc, buf.getvalue()

    ok = True
    with tempfile.TemporaryDirectory(prefix="anchor_selftest_") as td:
        base = Path(td)

        # (a) corrupt one quote
        a = base / "corrupt_quote"
        shutil.copytree(emission, a)
        target = None
        for f in sorted(a.rglob("*.md")):
            text = f.read_text(encoding="utf-8", errors="replace")
            paths, quotes, fences, _ = extract_tokens(text)
            prs, _ = pair(paths, quotes, text)
            if prs:
                _, q = prs[0]
                bad = text[:q.start] + '"THIS STRING IS NOT IN THE TARGET FILE ' \
                                       'AND MUST GO RED"' + text[q.end:]
                f.write_text(bad, encoding="utf-8")
                target = f.relative_to(a).as_posix()
                break
        if target is None:
            print("  self-test (a) SKIPPED — no prose anchor to corrupt")
        else:
            rc, out = run_quiet(a)
            verdict = "RED (correct)" if rc == 1 else "GREEN (GATE IS BROKEN)"
            print(f"  self-test (a) corrupted a quote in {target}: {verdict}")
            ok = ok and rc == 1

        # (b) insert a banned line citation
        b = base / "banned_form"
        shutil.copytree(emission, b)
        mds = sorted(b.rglob("*.md"))
        if not mds:
            print("  self-test (b) SKIPPED — no .md files")
        else:
            with mds[0].open("a", encoding="utf-8") as fh:
                fh.write("\n\nInjected by the self-test: see somefile.md"
                         + chr(58) + "42 for the claim.\n")
            rc, out = run_quiet(b)
            verdict = "RED (correct)" if rc == 1 else "GREEN (GATE IS BROKEN)"
            print(f"  self-test (b) injected a banned line citation: {verdict}")
            ok = ok and rc == 1

    print(f"  self-test verdict: "
          f"{'the gate can go red on both classes' if ok else 'THE GATE FAILED TO FAIL'}")
    return 0 if ok else 1


def main(argv=None) -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--root", type=Path, default=here,
                    help="emission root to check (default: this file's directory)")
    ap.add_argument("--corpus", type=Path, default=None,
                    help="frozen corpus root (default: auto-detect 01_EMERGENTISM)")
    ap.add_argument("--verbose", action="store_true", help="list every anchor")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the gate can go red, then run it for real")
    args = ap.parse_args(argv)

    emission = args.root.resolve()
    corpus = args.corpus
    if corpus is None:
        env = os.environ.get("EMERGENTISM_ROOT")
        if env:
            corpus = Path(env)
        else:
            corpus = None
            for anc in [emission] + list(emission.parents):
                if anc.name == "01_EMERGENTISM":
                    corpus = anc
                    break
            if corpus is None:
                corpus = FALLBACK_CORPUS
    corpus = Path(corpus).resolve()

    if args.self_test:
        print("SELF-TEST — the gate must be able to fail before it may be "
              "trusted to pass")
        st = _self_test(emission, corpus)
        print()
        rc = run(emission, corpus, args.verbose)
        return rc if st == 0 else 1

    return run(emission, corpus, args.verbose)


if __name__ == "__main__":
    sys.exit(main())
