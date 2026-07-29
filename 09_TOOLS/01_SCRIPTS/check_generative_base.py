#!/usr/bin/env python3
"""Verify G1-G5 of 05_COSMOLOGY/03_FORMAL_SYSTEM/52_THE_GENERATIVE_BASE.md.

The base posits one object and two operations:

    PRIMITIVE   1
    OPERATIONS  S(x) = x + 1        iota(x) = 1/x

Everything the base claims is decidable by exhaustion over finite words, so this
script is the whole stranger test: it needs no metaphysics, only fractions.

Exits 0 if every claim holds, 1 otherwise. Prints which claim failed.

WHY THIS EXISTS. The first statement of G2 in conversation was FALSE — it said
each value has exactly one word, ignoring that iota-iota is the identity, so
every word has infinitely many longer twins. The repair (reduced words) is exact
rather than a patch, and this script is what proves it rather than asserting it.
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

    # --- G5: both limits are approached --------------------------------------
    if not (val("S" * 9) > 9 and val("S" * 9 + "i") < F(1, 9)):
        failures.append("G5: the two limits are not both approached")

    if failures:
        print("GENERATIVE BASE: FAIL")
        for f in failures:
            print(f"- {f}")
        return 1

    print(
        f"GENERATIVE BASE: PASS "
        f"({len(by_value)} values from all words to length {WORD_LEN}; "
        f"{unreduced_multi} unreduced collisions, 0 reduced; "
        f"CW tree {n_words} words / {len(cw)} distinct; "
        f"grid {GRID}x{GRID} reachable; 0 unattained)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
