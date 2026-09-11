#!/usr/bin/env python3
"""Ask the corpus whether it already said this, BEFORE you write it down.

WHY THIS EXISTS
---------------
`00_HANDOFF/THE_EXECUTION_PLAN_2026_08_05.md` ranks findability joint-first among
all work streams, on the grounds that it "stops re-derivation", and it attaches a
kill to the claim that the index already prevents re-derivation:

    "exhibit a query a reasonable author would run that misses ..."

On 2026-09-11 a session exhibited five. A reader with grep, a full working day
and thirty-six subagents proposed five things the corpus had already written
down, two of which it had also formally excluded. The failure was never falsity.
It was that the prior art was phrased in vocabulary the author did not guess.

So this tool inverts the query. Instead of asking the author to guess the
corpus's words, it takes the author's words and reports what the corpus already
holds nearby -- canonical phrases, settled canon, and above all GRAVES, because
re-proposing a dead claim is the most expensive mistake available here.

WHAT IT IS NOT
--------------
NOT A GATE. It always exits 0 and it blocks nothing. On 2026-08-05 L6 refused a
new checker for this lane -- "a gate authored where gates already don't run" --
and that refusal is honoured: this is a lookup for people, not an enforcement.

It also commissions no canon. It reads; it writes nothing.

Usage:
    python3 -B prior_art_check.py "the balance score is the harmonic mean"
    python3 -B prior_art_check.py --self-test
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "00_META" / "registers" / "CORPUS_INDEX.jsonl"
REGISTER = ROOT / "00_META" / "00_THE_CLAIM_STATUS_REGISTER.md"
CANON = ROOT / "00_META" / "00_SETTLED_CANON_REGISTRY.md"
SKIP_DIRS = {"90_ARCHIVE", ".git", "node_modules", "__pycache__", ".vercel"}

STOP = set("""a an and are as at be because been before being between both but by can cannot could did do does
doing done down during each either else every for from further had has have having he her here hers him his how
i if in into is it its itself just let me more most must my no nor not of off on once only or other our out over
own same she should so some such than that the their them then there these they this those through to too under
until up very was we were what when where which while who whom why will with would you your it's we've
its not one two three four five six seven also may might shall about above after again against all am any""".split())

VERDICTS = ("FORMALLY-REFUTED", "EMPIRICALLY-REFUTED", "CATEGORY-ERROR",
            "NOT-WELL-POSED", "NARROWED", "OPEN-EMPIRICAL", "RETIRED")


def tokens(text: str) -> list[str]:
    raw = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ_-]{2,}", text.lower())
    return [t for t in raw if t not in STOP]


def quoted_phrases(text: str) -> list[str]:
    return [m.strip() for m in re.findall(r'"([^"]{4,})"', text)]


def walk_md():
    for path in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def corpus_frequency(terms: list[str], files: list[Path]) -> dict[str, int]:
    """How many live files contain each term. Rare terms are the useful ones."""
    freq = dict.fromkeys(terms, 0)
    for path in files:
        try:
            low = path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        for t in terms:
            if t in low:
                freq[t] += 1
    return freq


def search_phrases(terms: set[str], phrases: list[str]):
    """Canonical phrases that overlap the claim, scored by shared rare terms."""
    if not INDEX.exists():
        return []
    hits = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        phrase = row.get("canonical_phrase") or row.get("title")
        if not phrase:
            continue
        low = phrase.lower()
        shared = terms & set(tokens(phrase))
        score = len(shared)
        for p in phrases:
            if p.lower() in low:
                score += 5
        if score >= 2:
            hits.append((score, row["path"], phrase, sorted(shared)))
    hits.sort(key=lambda h: (-h[0], h[1]))
    return hits


def search_graves(terms: set[str], idf: dict[str, float]):
    """Register rows carrying a verdict, scored against the claim's terms."""
    if not REGISTER.exists():
        return []
    out = []
    for i, line in enumerate(REGISTER.read_text(encoding="utf-8").splitlines(), 1):
        if not line.lstrip().startswith("|"):
            continue
        verdict = next((v for v in VERDICTS if v in line), None)
        if not verdict:
            continue
        shared = terms & set(tokens(line))
        # Rarity-weighted: one rare term beats two common ones. A grave row is
        # short, so raw overlap counts undersell it -- that is how "no ethics"
        # missed DF-21 on 2026-09-11 with a single shared token.
        score = sum(idf.get(t, 1.0) for t in shared)
        if shared and score >= 2.0:
            cells = [c.strip(" `*") for c in line.strip().strip("|").split("|")]
            out.append((round(score, 2), cells[0] if cells else "?", verdict,
                        cells[1][:110] if len(cells) > 1 else "", i, sorted(shared)))
    out.sort(key=lambda h: -h[0])
    return out


def search_text(terms: set[str], idf: dict[str, float], files: list[Path], cap: int = 10):
    """Lines scored by the rarity-weighted mass of claim terms they carry.

    Deliberately NOT "the two rarest terms must co-occur". That rule missed
    41_THE_GLYPH_TRANSFORMATIONS.md:80 on 2026-09-11 -- the target line carried
    "harmonic" but not "reciprocal", so an and-of-two-rarest never reached it.
    Scoring by mass lets one very rare term surface a line on its own.
    """
    if not terms:
        return []
    scored = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = text.lower()
        present = {t for t in terms if t in low}
        if sum(idf.get(t, 1.0) for t in present) < 3.0:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            ll = line.lower()
            hit = {t for t in present if t in ll}
            if len(hit) < 2:
                continue
            score = sum(idf.get(t, 1.0) for t in hit)
            if score >= 3.0:
                scored.append((score, str(path.relative_to(ROOT)), n, line.strip()[:170]))
    scored.sort(key=lambda h: -h[0])
    return [(p, n, l) for _, p, n, l in scored[:cap]]


def report(claim: str, quiet: bool = False) -> dict:
    files = list(walk_md())
    terms = tokens(claim)
    phrases = quoted_phrases(claim)
    tset = set(terms)

    freq = corpus_frequency(sorted(tset), files)
    n_files = max(len(files), 1)
    # inverse document frequency: a term in 3 files is worth far more than one
    # in 900. This is the whole fix -- rarity, not raw overlap, finds prior art.
    idf = {t: math.log(n_files / (1 + freq.get(t, 0))) for t in tset}
    rare = sorted((t for t in tset if freq.get(t, 0) > 0),
                  key=lambda t: (-idf[t], t))

    ph = search_phrases(tset, phrases)
    gr = search_graves(tset, idf)
    tx = search_text(tset, idf, files)

    if not quiet:
        print(f'CLAIM: "{claim}"')
        print(f"live files scanned: {len(files)}")
        print(f"distinctive terms : {', '.join(f'{t}({freq[t]})' for t in rare[:8]) or '(none)'}\n")

        if gr:
            print("GRAVES AND REGISTER ROWS — re-proposing one of these is the expensive mistake")
            for score, ident, verdict, claim_text, ln, shared in gr[:6]:
                print(f"  [{verdict}] {ident} — {claim_text}")
                print(f"        register line {ln}   shared: {', '.join(shared[:6])}")
            print()

        if ph:
            print("CANONICAL PHRASES ALREADY ON DISK")
            for score, path, phrase, shared in ph[:8]:
                print(f"  {path}")
                print(f"        \"{phrase[:150]}\"")
                print(f"        shared: {', '.join(shared[:6])}")
            print()

        if tx:
            print("LITERAL LINES carrying the rarest terms together")
            for path, n, line in tx:
                print(f"  {path}:{n}")
                print(f"        {line}")
            print()

        if not (gr or ph or tx):
            print("No prior art surfaced. That is not proof of absence — it means")
            print("this tool's vocabulary did not reach it. Grep before you assert.")

    return {"terms": rare, "graves": gr, "phrases": ph, "text": tx}


# --------------------------------------------------------------------------
# self-test: the five re-derivations of 2026-09-11
# --------------------------------------------------------------------------

CASES = [
    {"claim": "the balance score B is the harmonic mean of a reciprocal pair and equals sin theta",
     "want": "41_THE_GLYPH_TRANSFORMATIONS.md"},
    {"claim": "the regime row runs Plato's degeneration chain reversed as an ascent",
     "want": "36_THE_ROSETTA_IN_THEMES_2026_08_13.md"},
    {"claim": "a proper class is not a member of any class therefore it cannot be an operand",
     "want": "THE_BOUNDARY_RULES_STANDALONE.md"},
    # Expected target corrected 2026-09-11 after the first self-test run. The
    # original fixture named the claim register; the actual prior art is the
    # axiom itself -- E9 - The Correction, Layer III CONDUCT, at 03_THE_EMERGENT
    # _AXIOMS.md:221. The tool was right and the fixture was wrong. Recorded here
    # rather than silently swapped, because tuning a tool to hit a mis-specified
    # target is the failure this whole script exists to catch.
    {"claim": "the corpus has no ethics and no conduct axiom",
     "want": "03_THE_EMERGENT_AXIOMS.md"},
    {"claim": "VMOSK-A splits V M O against S K A along the same line",
     "want": "42_VMOSKA_BOUNDARY_DISCIPLINE_2026_09_03.md"},
]


def self_test() -> int:
    print("SELF-TEST — the five re-derivations of 2026-09-11\n")
    print("Each claim was actually proposed that day by a reader who had grep,")
    print("a full session and 36 subagents, and who missed the prior art.\n")
    hits = 0
    for i, case in enumerate(CASES, 1):
        res = report(case["claim"], quiet=True)
        found = set()
        for _, path, _, _ in res["phrases"]:
            found.add(Path(path).name)
        for path, _, _ in res["text"]:
            found.add(Path(path).name)
        for *_, in ():
            pass
        if res["graves"]:
            found.add(REGISTER.name)
        ok = case["want"] in found
        hits += ok
        print(f"  {i}. {'HIT ' if ok else 'MISS'}  want {case['want']}")
        print(f"        claim: {case['claim'][:88]}")
        if not ok:
            near = sorted(found)[:4]
            print(f"        surfaced instead: {', '.join(near) if near else '(nothing)'}")
    print(f"\nrecall on the 2026-09-11 failure set: {hits}/{len(CASES)}")
    print("\nThis number is the tool's only warrant. It is advisory, never a gate,")
    print("and a miss here is a finding about the tool, not about the corpus.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("claim", nargs="*", help="the claim you are about to write down")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.claim:
        ap.print_help()
        return 0
    report(" ".join(args.claim))
    return 0        # always 0 — advisory, never a gate


if __name__ == "__main__":
    raise SystemExit(main())
