---
title: "Receipt 181 — false attestation in commit 1d60ef19, and two pre-existing test failures it exposed"
date: 2026-07-29
status: "CORRECTION — recorded, not amended away"
evidence_tier: "[B] the test runs and the worktree comparison are reproducible"
---

# Receipt 181 — a false attestation, and what it uncovered

## §1 · The false attestation

Commit `1d60ef19` states, of `09_TOOLS/02_COMPILERS/test_dimension_first_canon.py`:

> *"the suite passes."*

**It does not.** The suite reports `FAILED (failures=2)`. The claim was written
before the test output was read, and the commit was chained to run regardless of
the result.

Per r177's precedent — where `"CLAIM_STATUS.yaml untouched — it was already
correct"` was likewise false and was recorded rather than amended — this is
logged, not rewritten. **A corpus that edits its false attestations away has no
record of how often it makes them.**

## §2 · What the comparison actually showed

Measured by checking out `HEAD~1` in a detached worktree and running the same suite:

```text
HEAD~1 (before the five rulings)   FAILED (failures=4)
HEAD   (after)                     FAILED (failures=2)
```

The five-rulings commit **reduced** failures from four to two. Both survivors
pre-date it:

- `test_active_owners_do_not_operationalize_titan_arithmetic`
  `42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md:415` contains `0×∞=1` on an active
  owner surface — a `KSC-04` violation (`ArithmeticSignature(TitanFrame) = ∅`).

- `test_retired_titan_infix_is_absent_from_live_nonhistorical_surfaces`
  The infix `⊙ = • × ○` appears on **ten live surfaces**, including
  `00_META/00_THE_FIVE_PLUS_ONE_CONSTITUTION.md:90`.

The two that were fixed were fixed incidentally, not deliberately.

## §3 · The second failure is a real seam, not a stale test `[S]`

This is the part worth the owner's attention, and it is **not** repaired here.

The test asserts the Titan infix is **retired** from live surfaces. But
`00_THE_FOUNDATION.md`'s BASE now states, as posit `B1`:

```text
B1  ⊙ = • × ○
```

So the corpus simultaneously **retires the infix** (the test, and `KSC-04`'s
signature emptiness) and **posits it as the first line of its base**. Both cannot
be right as written. Three readings, none chosen here:

1. **The test is stale.** The infix was retired as *arithmetic*; `B1` states a
   *relation among seats*, which `KSC-04` permits. Then the test needs a scope
   clause, not the corpus a repair.
2. **`B1` violates `KSC-04`.** Then the base needs re-notation — which is exactly
   `G-0` exit B-i (neutral letters `e, a, b`), still open.
3. **Both are right in different registers** and the corpus has never said which
   register the test ranges over.

Reading 1 is the likeliest and would be the cheapest. **It is not adopted here**,
because deciding it decides part of `G-0`, which is the owner's.

## §4 · The process defect, which is the more useful finding

The failure was not that a test broke. It is that **a verification command and a
commit were chained in one invocation**, so the commit could not be conditioned on
the result. Every commit today that claimed a green check ran the check first and
*read it*; this one did not.

**Repair:** never chain `test && commit` where the commit message asserts the test
result. Run, read, then commit.

•   ⊙   ○ — *the attestation was cheap because nothing made it expensive.*
