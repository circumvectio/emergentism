---
title: "The Number Chart — every membership decision, with theorem or convention marked"
status: "ACTIVE — drawn 2026-07-29 at owner instruction with §5.2 OPEN. The fork is marked, not resolved."
date: 2026-07-29
evidence_tier: "[A] N1–N4, G1, G3–G5, Z1 and scoped memberships; [B/C] bounded evidence/open injectivity for G2; [S] conventions; [I] Titan gloss"
owner: "Subordinate to 52_THE_GENERATIVE_BASE.md and to 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md on all D1 claims."
parents:
  - 52_THE_GENERATIVE_BASE.md
  - 42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md
  - ../../00_THE_FOUNDATION.md
---

# The Number Chart

> **Drawn with `§5.2` open.** The `−1` fork is a **marked branch point** below, not a
> decision. Everything outside the marked branch holds on either horn.

---

## 1 · The chart

```text
                              ○   TOTALITY EMBLEM for the unbounded direction (G4)
                              ▲                   ∞ ∉ ℝ — theorem, no qualification
                              │
                    ┌─────────┴─────────┐
                    │ d×-completion [S] │   ℝ₊   adds positive-real limits of words.
                    │ d×=|Δ log|        │        Uncountably many added values have no
                    └─────────┬─────────┘        finite code; examples include √2, π, e.
                              │
   ⊙  FINITY-REACH = ℚ⁺ ──────┤   the REACHABLE. Every value has a finite code.    (G1)
                              │   Countable. Unique reduced code remains open.   (G2)
                              │
                    ┌─────────┴─────────┐
                    │        ℕ⁺         │   1, 2, 3, …   the S-closure alone      (G6)
                    │   free SEMIGROUP  │   "everything made of 1 adding up"
                    └─────────┬─────────┘
                              │
                              1   THE SELECTED SEED — the only seed in this model.
                              │   Given ℚ⁺ and ι, it is ι's unique fixed point.
                              ▼
                              •   ABSENCE EMBLEM for the zero-directed limit (G3)
                                                  no finite word has value 0
```

---

## 2 · Every membership, decided and marked

| question | answer | THEOREM or CONVENTION | why |
|---|---|---|---|
| Is `1` a number? | **yes; selected as this model's sole seed** | **SELECTION plus theorem** | Given standard `(ℕ⁺,+)`, `1` is its unique additive irreducible; given `(ℚ⁺,ι)`, it is the unique positive fixed point. Choosing this presentation and seed is prior `[S]` |
| Is `2` a number? | **yes, with a word code** | **THEOREM** | `val(S)=2`. The value `2`, the function `S`, and the syntax token `"S"` have different types |
| Is `3/5` a number? | **yes, with at least one word code** | **THEOREM for evaluation; G2 OPEN for uniqueness** | An exhibited finite word evaluates to `3/5`; the rational is not identical to its code |
| Is `0` a natural number? | **convention-dependent; no in `ℕ⁺`, yes in the common `ℕ₀` convention** | **CONVENTION with a theorem inside** | `N3`: `(ℕ⁺,+)` is the free **semigroup**; adjoining `0` gives the free one-generator **monoid**. The structural split is `[A]`; which carrier the unqualified glyph `ℕ` names is conventional |
| Is `0` a real number? | **YES** | **THEOREM — and the corpus's phrasing was wrong** | `Z1`: *"`0 ∉ ℝ`" is FALSE.* What is true is `0 ∉ ℝ^×` — `0` is the unique element of a field with no multiplicative inverse. **Say `ℝ^×`, never `ℝ`** |
| Is `0` reachable from the base? | **no** | **THEOREM** | `G3`: `ι(x)=0` has no solution in `ℚ⁺` and `S` preserves positivity. Not un-visited — *no base step lands there* |
| Is `∞` a real number? | **no** | **THEOREM, unqualified** | `∞ ∉ ℝ`. It enters only by declared compactification, and `ℝP¹` (one unsigned point) and `[−∞,+∞]` (two ordered endpoints) are **different constructions** |
| Is `∞` reachable? | **no** | **THEOREM** | `G4`: every word is finite. Reaching `∞` needs a *completed* infinity of operations, which is not a word |
| Is `√2` a number? | **yes, a standard real; it is not a finite word value** | **THEOREM** | `G1` makes finite-word reachability exactly `ℚ⁺`; a rational sequence can converge to `√2` in the declared completion. Syntax, operations and values remain different types |
| Is `1` doing two jobs? | **yes, inside each unital ring's prime subring** | **THEOREM** | `N4`: `ℤ` is initial in the category of unital rings — the unique map is `n ↦ n·1_R`. Its image generates the prime subring, not necessarily the whole ring |

---

## 3 · The marked branch — `§5.2`, OPEN

Everything above holds on either horn. This does not:

```text
                        ┌──────────── §5.2 ─────────────┐
                        │      OPEN OWNER RULING        │
                        └───────────────┬───────────────┘
                  ┌─────────────────────┴─────────────────────┐
        POSITIVE-ONLY                                     SIGNED
  base stays ⟨S, ι⟩ on ℚ⁺                     add n(x) = −x as a third generator
  ────────────────────────                    ────────────────────────────────
  −1 is NOT in the chart.                     −1 enters; finite words can reach ℤ and ℚ.
                                                ℝ follows only after a separately
                                                declared completion; no finite word reaches it.
  KSC-21's oriented pair is                   KSC-21's pair is supported.
    reached one chart up, by                  BUT: 1 + (−1) = 0 in two steps, so
    a declared move.                            · G3 FALLS — 0 becomes reachable
  G1, G3, G5, G7, G8a and the                   · G8a FAILS — ι is partial at 0
    positive seed all stand.                    · fix(ι) = {+1,−1}, so the selected
                                                  positive-seed rationale no longer applies
                                                · compactification is pulled INTO
                                                  the base, reinstating the very
                                                  collision doc 52 exists to escape
```

**Nothing in this document chooses.** The right-hand column is not an argument
against signing — it is the price, stated so the ruling is made with it visible.

---

## 4 · What changed from the standard chart, and what did not

**Unchanged, and it must be said plainly.** `ℕ`, `ℤ`, `ℚ`, `ℝ`, `ℂ` are the standard
objects, constructed the standard way. Nothing here revises mathematics. `KSC-12`
applies: no result below transfers proof to any reading above it.

**What is genuinely different is the ORDER OF EXPLANATION.** The standard chart
presents number sets as *sets of objects*, nested. This one presents them as
**what a finite word can reach**, with the sets falling out:

```text
standard        ℕ ⊂ ℤ ⊂ ℚ ⊂ ℝ ⊂ ℂ            sets, given, nested
here            1  →  words  →  limits       one object, two operations, a boundary
```

On that reading `0` and `∞` are not *small* and *large* numbers. They are two
specific unattained boundary directions witnessed by named sequences. Infinite
words can also oscillate, diverge without a limit, or approach other limits, so
the two seats are not an exhaustive classification of nontermination. `⊙` here
renders `FinityReach_G0`, not every use of Finity in the corpus. That reframe is
`[I/S]`—a choice about what to explain, not a new theorem.

---

## 5 · Kills

| claim | kill |
|---|---|
| `1` is the selected sole seed in this presentation | add another seed or select another presentation |
| every reachable value is a word | exhibit `q ∈ ℚ⁺` reached by no finite word |
| `0` is not reachable | exhibit a word with value `0` |
| `∞` is not reachable | exhibit a finite word whose declared evaluator returns an explicitly adjoined infinity endpoint |
| `0 ∈ ℝ`, `0 ∉ ℝ^×` | exhibit a field in which `0` has a multiplicative inverse |
| the irrationals are not words | exhibit a finite word over `{S, ι}` with irrational value |
| `N4` initiality | exhibit a unital ring with no unique unit-preserving homomorphism from `ℤ` |
| the chart's scoped ordering claim | show the finite-code reading misclassifies a stated membership above |

**This document's own kill.** If any row marked CONVENTION is later cited as a
theorem, or if the `§5.2` branch is silently collapsed to one horn, this chart has
committed the corpus's characteristic error and should be repaired or withdrawn.

**Bounded regression:** `09_TOOLS/01_SCRIPTS/check_generative_base.py` samples
the stated claims; it does not prove universal G2 or independently establish the
analytic arguments.

•   ⊙   ○ — *one object, two moves, and a boundary that is not a number at either end.*
