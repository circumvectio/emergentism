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

# --- BOUND CONTRACT -------------------------------------------------------
# 2026-08-13: the three bounds above were DECLARED and ASSERTED NOWHERE. All
# three narrowed silently and still printed PASS with exit 0 (measured, at the
# pre-repair revision: WORD_LEN 10->4 exit 0, GRID 25->5 exit 0, CW_DEPTH
# 12->4 exit 0). The gate honestly reported the smaller bound in its PASS line
# and did not treat it as a failure, so "shrink the bound to speed up CI" was
# an invisible edit. This block closes that. It continues the P1 repair queued
# at 00_HANDOFF/gate_audit/MUTATION_TEST_RECEIPT_2026_08_06.md:112 ("add
# explicit self-assertions on val, WORD_LEN, GRID"); the `val` third of that
# line already landed as the G-Spec assertions in main().
#
# Each bound is pinned twice, because either lock alone is weak:
#
#   1. STRUCTURAL — a property the gate genuinely needs AT that bound, so the
#      number is not arbitrary and the assertion is not a tautology:
#        WORD_LEN  the enumeration must contain every word the gate names as a
#                  literal witness; the longest is "S"*9+"i" (the G5 lower
#                  limit), length 10.
#        CW_DEPTH  the Calkin-Wilf tree is a CROSS-CHECK on G2, so it must
#                  cover the {S,iota} enumeration it cross-checks. Minimum
#                  depth for that is 10 (measured); 12 is declared, for margin.
#        GRID      the G1 superset direction only tests something the exhaustive
#                  enumeration did not already test if the grid reaches BEYOND
#                  it. At GRID=5 that surplus is 0 of 19 cells -- the check is
#                  decorative. At GRID=25 it is 182 of 399 (measured).
#
#   2. DECLARED-VALUE — exact equality against counts HARVESTED from a passing
#      run at the declared bounds (2026-08-13, this file's own output). The
#      structural locks alone would still let GRID drift 25->11, so the counts
#      pin the exact bound. These are measurements, not derivations: they
#      cannot be recomputed from the bound without running the enumeration.
#
# CHANGING A BOUND IS THEREFORE A TWO-PLACE EDIT: move the constant, re-run,
# and re-harvest the witness below. That is the point -- the second place is
# where a human has to look at what the new bound actually covers.
DECLARED_BOUNDS = {"WORD_LEN": 10, "CW_DEPTH": 12, "GRID": 25}

DECLARED_WITNESS = {
    "distinct_values": 232,          # |{val(w)} : |w| <= WORD_LEN|
    "unreduced_collisions": 143,     # values carrying >1 word (iota-iota twins)
    "cw_nodes": 8191,                # 2^(CW_DEPTH+1)-1 distinct Calkin-Wilf values
    "grid_cells": 399,               # distinct reduced p/q with p,q <= GRID
    "grid_beyond_enumeration": 182,  # grid cells the WORD_LEN enumeration misses
}

# Every word this script names as a literal witness. The enumeration claims to
# cover "all words to length WORD_LEN"; if a named witness falls outside that,
# the PASS line is overstating what was enumerated.
NAMED_WITNESS_WORDS = ("S", "S" * 2, "Si", "S" * 9, "S" * 9 + "i")

# Minimum Calkin-Wilf depth that covers the WORD_LEN=10 enumeration (measured
# 2026-08-13; the closure first contains all 232 values at depth 10).
CW_MIN_DEPTH_FOR_COVERAGE = 10


def declared_bound_failures() -> list[str]:
    """Bound-contract checks that need no computation. Run FIRST, fail fast.

    Cheap and early on purpose: an inflated bound (CW_DEPTH 12 -> 20 is 2^21
    nodes) must be rejected before the expensive loops build it, not after.
    """
    out: list[str] = []
    for name, actual in (("WORD_LEN", WORD_LEN), ("CW_DEPTH", CW_DEPTH), ("GRID", GRID)):
        declared = DECLARED_BOUNDS[name]
        if actual != declared:
            out.append(
                f"BOUND: {name} is {actual} but the bound contract declares "
                f"{declared}. A bound may not move silently -- re-run the gate, "
                f"re-harvest DECLARED_WITNESS, and update DECLARED_BOUNDS in the "
                f"same edit."
            )
    longest = max(len(w) for w in NAMED_WITNESS_WORDS)
    if WORD_LEN < longest:
        out.append(
            f"BOUND: WORD_LEN={WORD_LEN} is shorter than the longest named "
            f"witness word ({longest} letters); the enumeration would not "
            f"contain the words this gate tests by name"
        )
    if CW_DEPTH < CW_MIN_DEPTH_FOR_COVERAGE:
        out.append(
            f"BOUND: CW_DEPTH={CW_DEPTH} is below {CW_MIN_DEPTH_FOR_COVERAGE}, "
            f"the minimum depth whose closure covers the WORD_LEN enumeration; "
            f"the Calkin-Wilf tree would no longer cross-check G2"
        )
    return out


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

    # --- bound contract, before any expensive work ---------------------------
    bound_failures = declared_bound_failures()
    if bound_failures:
        print("GENERATIVE BASE: FAIL")
        for f in bound_failures:
            print(f"- {f}")
        return 1

    # --- enumerate every word up to WORD_LEN ---------------------------------
    by_value: dict[F, list[str]] = defaultdict(list)
    for n in range(WORD_LEN + 1):
        for tup in product("Si", repeat=n):
            w = "".join(tup)
            by_value[val(w)].append(w)

    # --- WORD_LEN witness: the enumeration is the declared one ---------------
    if len(by_value) != DECLARED_WITNESS["distinct_values"]:
        failures.append(
            f"BOUND/WORD_LEN: enumeration to length {WORD_LEN} produced "
            f"{len(by_value)} distinct values, contract declares "
            f"{DECLARED_WITNESS['distinct_values']}"
        )
    for w in NAMED_WITNESS_WORDS:
        # .get, never [] -- by_value is a defaultdict and a missing witness must
        # not be silently created as an empty bucket, which would itself corrupt
        # the collision counts below.
        if w not in by_value.get(val(w), []):
            failures.append(
                f"BOUND/WORD_LEN: named witness word {w!r} (length {len(w)}) is "
                f"not in the enumeration to length {WORD_LEN}"
            )

    # --- G-Spec: the corpus's defining operation IS x+1 ------------------------
    # 2026-08-06: check_generative_base was SOUND-BUT-BLIND. Changing the
    # successor from x+1 to x+2 produced a byte-identical PASS — the
    # aggregate checks (positive values, no zero, grid coverage) all still
    # hold. The sibling check_g2_normal_form.py catches the same mutation
    # because it pins the continued-fraction dictionary; this gate now adds
    # three specific G-Spec assertions that any future successor change must
    # violate. (A gate that cannot fail on a substantive mutation is not a
    # gate; the lesson is the same one check_g2_normal_form carries in its
    # own header.)
    if val("S") != F(2):
        failures.append(
            f"G-Spec: val('S') must be 2 (i.e. S(1)=1+1), got {val('S')}; "
            f"the successor is not the corpus's defining +1"
        )
    if val("S" * 2) != F(3):
        failures.append(
            f"G-Spec: val('SS') must be 3, got {val('S' * 2)}"
        )
    if val("Si") != F(1, 2):
        failures.append(
            f"G-Spec: val('Si') must be 1/2 (i.e. iota(1)=1/1), got {val('Si')}; "
            f"iota is not 1/x"
        )

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
    if unreduced_multi != DECLARED_WITNESS["unreduced_collisions"]:
        failures.append(
            f"BOUND/WORD_LEN: {unreduced_multi} unreduced collisions at length "
            f"{WORD_LEN}, contract declares "
            f"{DECLARED_WITNESS['unreduced_collisions']}"
        )

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

    # --- CW_DEPTH witness ----------------------------------------------------
    # n_words is DERIVED from CW_DEPTH, so the check above is self-consistent at
    # any depth and cannot detect a change to it. These two can.
    if len(cw) != DECLARED_WITNESS["cw_nodes"]:
        failures.append(
            f"BOUND/CW_DEPTH: tree to depth {CW_DEPTH} has {len(cw)} nodes, "
            f"contract declares {DECLARED_WITNESS['cw_nodes']}"
        )
    uncovered = set(by_value) - set(cw)
    if uncovered:
        failures.append(
            f"BOUND/CW_DEPTH: the Calkin-Wilf cross-check at depth {CW_DEPTH} "
            f"misses {len(uncovered)} of the {len(by_value)} enumerated values "
            f"(e.g. {sorted(uncovered)[:3]}); it is no longer cross-checking G2 "
            f"over the words G2 was tested on"
        )

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

    # --- GRID witness --------------------------------------------------------
    # "grid is reachable" is satisfied trivially by a small grid, because a small
    # grid sits entirely inside the exhaustive word enumeration and so tests
    # nothing the enumeration did not already test. The surplus is what makes
    # this the SUPERSET direction rather than a restatement of the subset one.
    if len(grid) != DECLARED_WITNESS["grid_cells"]:
        failures.append(
            f"BOUND/GRID: {GRID}x{GRID} holds {len(grid)} distinct fractions, "
            f"contract declares {DECLARED_WITNESS['grid_cells']}"
        )
    beyond = grid - set(by_value)
    if len(beyond) != DECLARED_WITNESS["grid_beyond_enumeration"]:
        failures.append(
            f"BOUND/GRID: {len(beyond)} grid cells lie beyond the WORD_LEN="
            f"{WORD_LEN} enumeration, contract declares "
            f"{DECLARED_WITNESS['grid_beyond_enumeration']}"
        )
    if not beyond:
        failures.append(
            f"BOUND/GRID: every cell of the {GRID}x{GRID} grid is already inside "
            f"the exhaustive enumeration — the G1 superset direction is testing "
            f"nothing the subset direction did not already cover"
        )

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
        f"grid {GRID}x{GRID} reachable; 0 unattained; "
        f"{len(beyond)} grid cells beyond the enumeration)"
    )
    print(
        f"BOUND CONTRACT: PASS "
        f"(WORD_LEN={WORD_LEN}, CW_DEPTH={CW_DEPTH}, GRID={GRID} each pinned to "
        f"a declared value and a harvested witness; narrowing any of the three "
        f"is a FAIL, not a quieter PASS)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
