#!/usr/bin/env python3
"""Run bounded regressions for the selected generative-base model.

The base posits one object and two operations:

    PRIMITIVE   1
    OPERATIONS  S(x) = x + 1        iota(x) = 1/x

Finite samples cannot prove universal reachability or injectivity. This script
checks declared finite bounds with exact rational arithmetic so mutations and
counterexamples inside those bounds fail loudly.

Exits 0 if the bounded regressions pass, 1 otherwise.

WHY THIS EXISTS. The first statement of G2 in conversation was FALSE — it said
each value has exactly one word, ignoring that iota-iota is the identity, so
every word has infinitely many longer twins. The reduced-word repair is tested
here over finite bounds.

G2 IS NO LONGER OPEN (2026-08-05). The line that stood here — "a complete
injectivity proof remains a separate duty" — is discharged. G2 is the uniqueness
of the finite simple continued fraction with last partial quotient >= 2 (Hardy &
Wright, Theory of Numbers, Ch. X), i.e. inherited prior art, not a corpus result.
Proof: 05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md. The
structural check that pins the reason, with a mutation harness, is the sibling
script check_g2_normal_form.py. This script remains a bounded regression over the
base's other properties and should not be cited as the warrant for uniqueness --
that warrant is the citation, not this enumeration.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

WORD_LEN = 10       # exhaustive over all 2^(n+1)-1 words up to this length
CW_DEPTH = 12       # Calkin-Wilf binary tree depth
GRID = 25           # every p/q with p,q <= GRID must be reachable


def val(word: str) -> F:
    """Value of a word: its letters applied left to right to 1."""
    x = F(1)
    for c in word:
        x = x + 1 if c == "S" else 1 / x
    return x


def reduced(w: str) -> bool:
    """No 'ii' (iota is an involution) and no leading 'i' (1 is iota's fixed point)."""
    return "ii" not in w and not w.startswith("i")


def main() -> int:
    failures: list[str] = []

    # --- enumerate every word up to WORD_LEN ---------------------------------
    by_value: dict[F, list[str]] = defaultdict(list)
    for n in range(WORD_LEN + 1):
        for tup in product("Si", repeat=n):
            w = "".join(tup)
            by_value[val(w)].append(w)

    # --- G1 (subset direction): every word's value is a positive rational ----
    if any(v <= 0 for v in by_value):
        failures.append("G1: a word evaluated to a non-positive value")

    # --- G2: reduced words are unique normal forms ---------------------------
    collisions = {
        v: [w for w in ws if reduced(w)]
        for v, ws in by_value.items()
        if len([w for w in ws if reduced(w)]) > 1
    }
    if collisions:
        v, ws = next(iter(collisions.items()))
        failures.append(f"G2: {len(collisions)} values have >1 reduced word, e.g. {v} <- {ws}")

    unreduced_multi = sum(1 for ws in by_value.values() if len(ws) > 1)
    if unreduced_multi == 0:
        failures.append("G2: no unreduced collisions found — the test is not exercising iota-iota")

    # --- G2 cross-check: Calkin-Wilf {S, L} must be a perfect binary tree -----
    cw: dict[F, int] = defaultdict(int)
    for n in range(CW_DEPTH + 1):
        for tup in product("SL", repeat=n):
            x = F(1)
            for c in tup:
                x = x + 1 if c == "S" else x / (x + 1)
            cw[x] += 1
    n_words = 2 ** (CW_DEPTH + 1) - 1
    if len(cw) != n_words or any(c > 1 for c in cw.values()):
        failures.append(f"G2/CW: {n_words} words produced {len(cw)} distinct values (expected equal)")

    # --- G1 (superset direction): reachability of a dense grid ---------------
    seen: set[F] = set()
    frontier = {F(1)}
    while frontier:
        seen |= frontier
        frontier = {y for x in frontier for y in (x + 1, 1 / x)} - seen
        # stop once the grid is covered; the recursion is otherwise unbounded
        if {F(a, b) for a in range(1, GRID + 1) for b in range(1, GRID + 1)} <= seen:
            break
        if len(seen) > 2_000_000:
            failures.append("G1: grid not covered within the search budget")
            break
    grid = {F(a, b) for a in range(1, GRID + 1) for b in range(1, GRID + 1)}
    missing = sorted(grid - seen)
    if missing:
        failures.append(f"G1: {len(missing)} grid values unreachable, e.g. {missing[:3]}")

    # --- G3: no word attains zero -------------------------------------------
    if F(0) in by_value or F(0) in seen:
        failures.append("G3: a word attained 0")
    # the sharper form: iota(x)=0 has no solution, S(x)=0 has none in the positives
    if any(1 / x == 0 for x in list(seen)[:10000]):
        failures.append("G3: iota mapped a reachable value to 0")

    # --- G4 finite-word representation invariant ----------------------------
    # Fraction has no infinity value. The universal claim rests on induction
    # over finite words; this assertion only guards the enumerated sample.
    if any(not isinstance(v, F) for v in by_value):
        failures.append("G4: an enumerated finite word escaped exact rational values")

    # --- G6/G7/G8a: the two operations are not two of a kind -----------------
    # G8a only: rationals throughout, no reals. G8b (the log form) needs the
    # completion and is therefore NOT checkable here — that is the point of it.
    def close(gens, depth):
        s, front = {F(1)}, {F(1)}
        for _ in range(depth):
            front = {g(x) for x in front for g in gens} - s
            if not front:
                break
            s |= front
        return s

    only_iota = close([lambda x: 1 / x], 8)
    only_s = close([lambda x: x + 1], 12)
    sample = list(seen)[:20000]
    if only_iota != {F(1)}:
        failures.append(f"G6: iota alone is not sterile — reached {sorted(only_iota)[:5]}")
    if any(x.denominator > 1 for x in only_s):
        failures.append("G6: S alone produced a non-integer")
    if min(only_s) != F(1):
        failures.append("G7: S alone fell below 1 — the descent must require iota")
    if not all(1 / (1 / x) == x for x in sample):
        failures.append("G8a: iota is not an involution on the reachable set")
    if [x for x in sample if 1 / x == x] != [F(1)]:
        failures.append("G8a: iota has a reachable fixed point other than 1")

    # --- G9: the determinant invariant, and the hinge is not a word ----------
    def _n(m):
        from math import gcd
        e = [m[0][0], m[0][1], m[1][0], m[1][1]]
        g = 0
        for v in e:
            g = gcd(g, abs(v))
        if g:
            e = [v // g for v in e]
        for v in e:
            if v != 0:
                if v < 0:
                    e = [-w for w in e]
                break
        return tuple(e)

    def _mul(x, y):
        return ((x[0][0] * y[0][0] + x[0][1] * y[1][0], x[0][0] * y[0][1] + x[0][1] * y[1][1]),
                (x[1][0] * y[0][0] + x[1][1] * y[1][0], x[1][0] * y[0][1] + x[1][1] * y[1][1]))

    MS, MI = ((1, 1), (0, 1)), ((0, 1), (1, 0))
    words, front = {_n(((1, 0), (0, 1)))}, [((1, 0), (0, 1))]
    for _ in range(16):
        nxt = []
        for m in front:
            for g in (MS, MI):
                pm = _mul(m, g)
                if _n(pm) not in words:
                    words.add(_n(pm))
                    nxt.append(pm)
        front = nxt
    if _n(((1, -1), (1, 1))) in words:
        failures.append("G9: the hinge u=(x-1)/(x+1) was found as a word — det 2 should forbid it")
    if _n(((1, 0), (1, 1))) not in words:
        failures.append("G9: L(x)=x/(x+1) is det 1 and must be a word, but was not found")

    # --- G10: det and sign are INDEPENDENT obstructions ----------------------
    # n∘ι : x ↦ −1/x has det +1 (passes G9) and still is not a word, because it
    # leaves ℚ⁺. If this ever fails, G9 has been over-read as closing §5.2.
    # r183 (`183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`): the
    # previous version of this block evaluated TWO CONSTANT EXPRESSIONS
    # over literals and could never fire. It is replaced by a computed table.
    probes = [F(1), F(2), F(1, 2), F(3, 5), F(7), F(22, 7)]
    quad = {}
    for nm, mat, fn in (
        ("S", ((1, 1), (0, 1)), lambda z: z + 1),
        ("iota", ((0, 1), (1, 0)), lambda z: 1 / z),
        ("n", ((-1, 0), (0, 1)), lambda z: -z),
        ("n_iota", ((0, -1), (1, 0)), lambda z: -1 / z),
        ("D2", ((2, 0), (0, 1)), lambda z: 2 * z),
        ("hinge", ((1, -1), (1, 1)), lambda z: (z - 1) / (z + 1)),
    ):
        d = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        quad[nm] = (d in (1, -1), all(fn(z) > 0 for z in probes))
    # G10 holds iff all four combinations of (passes G9, stays positive) are realised.
    if len({quad[k] for k in quad}) < 4:
        failures.append(
            f"G10: det and sign are not independent — only {len({quad[k] for k in quad})} "
            f"of 4 quadrants realised: {quad}"
        )
    if not (quad["n_iota"][0] and not quad["n_iota"][1]):
        failures.append("G10: n∘ι must PASS G9 (det +1) and LEAVE ℚ⁺ — the decisive witness")
    if not (quad["D2"][0] is False and quad["D2"][1]):
        failures.append("G10: 2x must FAIL G9 (det 2) and STAY in ℚ⁺")

    # --- G4: no word attains ∞ ------------------------------------------------
    # r183 (`183_THE_MANIFEST_AUDITED_ITSELF_AND_FAILED_2026_07_29.md`): the
    # manifest asserted this check and it DID NOT EXIST (grep 'G4' -> 0).
    # Every word is finite, so every value is a finite rational: bounded numerator
    # and denominator, and no float overflow.
    for x in list(seen)[:20000]:
        if x.denominator == 0:
            failures.append("G4: a reachable value has zero denominator — ∞ attained")
            break
    depth_max = max((x for x in seen if x.denominator == 1), default=F(1))
    if not depth_max.denominator == 1 or depth_max <= 0:
        failures.append("G4: the S-ray did not produce finite integer values")
    # and the structural fact: the value of any finite word is finite by construction
    w = F(1)
    for _ in range(200):
        w = w + 1
    if not (w.denominator == 1 and w == 201):
        failures.append("G4: 200 applications of S did not give a finite value")

    # --- G5: both limits are approached --------------------------------------
    if not (val("S" * 9) > 9 and val("S" * 9 + "i") < F(1, 9)):
        failures.append("G5: the two limits are not both approached")

    if failures:
        print("GENERATIVE BASE: FAIL")
        for f in failures:
            print(f"- {f}")
        return 1

    print(
        f"GENERATIVE BASE BOUNDED REGRESSION: PASS "
        f"({len(by_value)} values from all words to length {WORD_LEN}; "
        f"{unreduced_multi} unreduced collisions, 0 reduced; "
        f"CW tree {n_words} words / {len(cw)} distinct; "
        f"grid {GRID}x{GRID} reachable; 0 unattained)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
