#!/usr/bin/env python3
"""Verify the G2 normal-form claim through its continued-fraction dictionary.

G2 (52_THE_GENERATIVE_BASE.md, section 2) states: call a word over {S, iota}
REDUCED if it contains no 'ii' and does not begin with 'i'; then

    val : reduced words -> Q+           is a bijection.

The corpus carried this as [C] with bounded evidence. It is not open. It is the
uniqueness of the finite simple continued fraction expansion with last partial
quotient >= 2 (Hardy & Wright, Theory of Numbers, Ch. X; Khinchin section I.2 --
theorem numbering varies by edition and was not verified against a physical
copy), transported along the dictionary

    S^a0 iota S^a1 iota ... iota S^ak     |->    [ak; a(k-1), ..., a1, a0 + 1]

with a trailing iota denoting the reciprocal. Note the +1 on the LAST partial
quotient: val starts AT 1, so the leading block S^a0 contributes a0 + 1, not a0.
That off-by-one is exactly what forces the last partial quotient to be >= 2 --
which is precisely the standard normalisation that makes the expansion unique.
G2's two syntactic exclusions are therefore not bookkeeping; they ARE the
classical uniqueness normalisation, discovered independently and stated in
word form.

THIS SCRIPT DOES NOT PROVE G2. The proof is in
05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md. What this script
does is check, exhaustively inside declared bounds and with exact rational
arithmetic, that the dictionary the proof relies on actually holds of the code
-- and, via a mutation harness, that the check can FAIL. A regression that
cannot fail is not evidence. The predecessor check_generative_base.py sampled
injectivity and could not distinguish "G2 is true" from "the grammar was never
stressed"; this one pins the structural reason.

Exits 0 if every check passes, 1 otherwise.
"""

from __future__ import annotations

import sys
from fractions import Fraction as F
from itertools import product

WORD_LEN = 18       # exhaustive over ALL reduced words up to this length


def val(word: str) -> F:
    """Value of a word: its letters applied left to right to 1."""
    x = F(1)
    for c in word:
        x = x + 1 if c == "S" else 1 / x
    return x


def reduced(w: str) -> bool:
    """No 'ii' (iota is an involution) and no leading 'i' (1 is iota's fixed point)."""
    return "ii" not in w and not w.startswith("i")


def reduced_words(max_len: int):
    for n in range(max_len + 1):
        for tup in product("Si", repeat=n):
            w = "".join(tup)
            if reduced(w):
                yield w


def word_to_cf(w: str) -> tuple[list[int], bool]:
    """Dictionary: reduced word -> (partial quotients, reciprocal flag).

    Returns the continued fraction [q0; q1, ..., qm] as a list, plus a flag
    saying whether the word's value is that CF's reciprocal.
    """
    trailing = w.endswith("i")
    body = w[:-1] if trailing else w
    blocks = [len(p) for p in body.split("i")]   # [a0, a1, ..., ak]
    cf = list(reversed(blocks))                  # [ak, ..., a1, a0]
    cf[-1] += 1                                  # val starts AT 1
    return cf, trailing


def cf_value(qs: list[int]) -> F:
    x = F(qs[-1])
    for a in reversed(qs[:-1]):
        x = a + 1 / x
    return x


CHECKS = {
    1: "injectivity (the G2 claim itself)",
    2: "the continued-fraction dictionary (the structural reason it holds)",
    3: "last partial quotient >= 2 (the classical uniqueness normalisation)",
    4: "intermediate partial quotients >= 1 (same theorem's hypothesis)",
    5: "the trichotomy that reduces injectivity to the >1 branch",
}


def run_checks(reduce_pred, dictionary, valfn, label: str) -> dict[int, list[str]]:
    """Return {check_id: [failure messages]}. Parameterised so mutants can be injected.

    NOTE: this deliberately does NOT return early. An early return meant that a
    mutant tripping check (1) masked checks (3), (4) and (5) entirely, so those
    three were asserted in the PASS banner while no mutant ever exercised them.
    That is the same 'instrument published as warrant' defect this script exists
    to prevent, committed by the script itself. Failures are collected per check
    and capped, so every check is independently exercised on every run.
    """
    found: dict[int, list[str]] = {k: [] for k in CHECKS}
    seen: dict[F, str] = {}
    CAP = 3   # keep output bounded; presence, not volume, is the signal

    def note(cid: int, msg: str) -> None:
        if len(found[cid]) < CAP:
            found[cid].append(f"{label}: {msg}")

    for n in range(WORD_LEN + 1):
        for tup in product("Si", repeat=n):
            w = "".join(tup)
            if not reduce_pred(w):
                continue
            v = valfn(w)

            # (1) INJECTIVITY -- the G2 claim itself.
            if v in seen:
                note(1, f"collision val({seen[v]!r}) == val({w!r}) == {v}")
            else:
                seen[v] = w

            if w == "":
                if v != 1:
                    note(1, f"val(empty) = {v}, expected 1")
                continue

            cf, recip = dictionary(w)

            # (2) THE DICTIONARY -- the structural reason injectivity holds.
            try:
                expected = 1 / cf_value(cf) if recip else cf_value(cf)
            except ZeroDivisionError:
                expected = None
            if expected != v:
                note(2, f"dictionary mismatch on {w!r}: cf={cf} recip={recip} "
                        f"gives {expected}, val gives {v}")

            # (3) LAST PARTIAL QUOTIENT >= 2 -- the classical uniqueness normalisation.
            if cf[-1] < 2:
                note(3, f"{w!r} has last partial quotient {cf[-1]} < 2; "
                        f"the standard uniqueness hypothesis is violated")

            # (4) INTERMEDIATE PARTIAL QUOTIENTS >= 1 -- required by the same theorem.
            if any(q < 1 for q in cf[:-1]):
                note(4, f"{w!r} has a partial quotient < 1: cf={cf}")

            # (5) THE TRICHOTOMY that reduces injectivity to the >1 branch.
            if w.endswith("S") and not v > 1:
                note(5, f"{w!r} ends in S but val = {v} is not > 1")
            if w.endswith("i") and not v < 1:
                note(5, f"{w!r} ends in iota but val = {v} is not < 1")

    return found


# --------------------------------------------------------------------------
# MUTATION HARNESS
#
# Each mutant deliberately breaks one load-bearing part and DECLARES which
# checks it must trip. Two conditions are enforced:
#
#   (i)  every mutant trips the checks it declares -- else that mutant is
#        mislabelled and proves nothing about the check it claims to cover;
#   (ii) every check in CHECKS is tripped by at least one mutant -- else that
#        check is DECORATIVE: asserted in the PASS banner, never exercised.
#
# Condition (ii) is the one the first version of this script failed.
# --------------------------------------------------------------------------

def _mut_allow_leading_iota(w: str) -> bool:
    """Drop the no-leading-iota rule.

    Trips (1): val('i') == val('') == 1.
    Trips (5): 'i' ends in iota but its value is 1, not < 1.
    """
    return "ii" not in w


def _mut_allow_ii(w: str) -> bool:
    """Drop the involution rule.

    Trips (1): val('Sii') == val('S') == 2.
    Trips (4): 'Sii' splits into an EMPTY block, i.e. a partial quotient 0.
    """
    return not w.startswith("i")


def _mut_dictionary_no_plus_one(w: str) -> tuple[list[int], bool]:
    """Forget that val starts AT 1. Trips (2), and (3) once the last entry is 1."""
    trailing = w.endswith("i")
    body = w[:-1] if trailing else w
    cf = list(reversed([len(p) for p in body.split("i")]))
    return cf, trailing


def _mut_dictionary_no_reverse(w: str) -> tuple[list[int], bool]:
    """Read the blocks forwards. Trips (2) on the first asymmetric word."""
    trailing = w.endswith("i")
    body = w[:-1] if trailing else w
    cf = [len(p) for p in body.split("i")]
    cf[-1] += 1
    return cf, trailing


def _mut_dictionary_alt_last_quotient(w: str) -> tuple[list[int], bool]:
    """Use the OTHER classical expansion: [..., q] -> [..., q-1, 1].

    This is value-preserving, so it does NOT trip (2). It is the exact
    representation the uniqueness theorem excludes, so it must trip (3).
    This mutant exists to prove check (3) is real: it is the difference
    between 'the expansion' and 'the unique expansion'.
    """
    cf, trailing = word_to_cf(w)
    return cf[:-1] + [cf[-1] - 1, 1], trailing


def _mut_val_from_zero(w: str) -> F:
    """Start the evaluation at 0 instead of 1. Trips (5), the trichotomy:
    val('S') becomes 1, which ends in S yet is not > 1."""
    x = F(0)
    for c in w:
        x = x + 1 if c == "S" else (1 / x if x != 0 else F(0))
    return x


MUTANTS = [
    # name, reduce_pred, dictionary, valfn, declared targets
    ("allow leading iota", _mut_allow_leading_iota, word_to_cf, val, {1, 5}),
    ("allow ii", _mut_allow_ii, word_to_cf, val, {1, 4}),
    ("dictionary without the +1", reduced, _mut_dictionary_no_plus_one, val, {2}),
    ("dictionary without the reversal", reduced, _mut_dictionary_no_reverse, val, {2}),
    ("alternative last quotient [q] -> [q-1,1]", reduced,
     _mut_dictionary_alt_last_quotient, val, {3}),
    ("evaluation started at 0", reduced, word_to_cf, _mut_val_from_zero, {5}),
]


def main() -> int:
    found = run_checks(reduced, word_to_cf, val, "G2")
    n_words = sum(1 for _ in reduced_words(WORD_LEN))

    if any(found.values()):
        print("G2 NORMAL FORM: FAIL")
        for cid, msgs in sorted(found.items()):
            for m in msgs:
                print(f"- check ({cid}) {CHECKS[cid]}: {m}")
        return 1

    # --- The harness must be able to fail. Prove it, per check. ---
    harness_failures: list[str] = []
    covered: set[int] = set()

    for name, pred, dic, vfn, targets in MUTANTS:
        tripped = {cid for cid, msgs in run_checks(pred, dic, vfn, f"mutant[{name}]").items() if msgs}
        covered |= tripped
        missed = targets - tripped
        if missed:
            harness_failures.append(
                f"mutant {name!r} did NOT trip its declared check(s) "
                f"{sorted(missed)} -- it is mislabelled and proves nothing about them"
            )

    decorative = set(CHECKS) - covered
    if decorative:
        harness_failures.append(
            f"check(s) {sorted(decorative)} are DECORATIVE -- asserted below but "
            f"no mutant exercises them: "
            + "; ".join(f"({c}) {CHECKS[c]}" for c in sorted(decorative))
        )

    if harness_failures:
        print("G2 NORMAL FORM: FAIL (mutation harness is blind)")
        for f in harness_failures:
            print(f"- {f}")
        return 1

    print(
        f"G2 NORMAL FORM: PASS "
        f"(all {n_words} reduced words to length {WORD_LEN}, exact rationals; "
        f"0 collisions; continued-fraction dictionary exact on every word; "
        f"last partial quotient >= 2 throughout; trichotomy exceptionless)"
    )
    print(
        f"  MUTATION COVERAGE: {len(MUTANTS)} mutants, each tripping its declared "
        f"checks; all {len(CHECKS)} checks exercised (none decorative)."
    )
    print(
        "  NOTE: this is a bounded check of the dictionary, not a proof of G2. "
        "The proof is in 05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
