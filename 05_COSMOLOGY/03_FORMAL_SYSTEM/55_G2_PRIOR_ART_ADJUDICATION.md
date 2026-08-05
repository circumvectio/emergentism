---
title: "G2 — Prior-Art Adjudication and Proof"
status: "ACTIVE — VERDICT: KNOWN-UP-TO-REFORMULATION. G2 is not open and is not novel. It is the uniqueness of the finite simple continued fraction expansion with last partial quotient >= 2 (Hardy & Wright, Theory of Numbers, Ch. X), transported along an exact dictionary. Proof below. Tier moves [C] -> [A] inherited-with-citation."
date: 2026-08-05
evidence_tier: "[A] the dictionary, the proof, and the classical theorem; [B] the cited literature; [S] the decision to state the base in word form"
owner: "Subordinate to 52_THE_GENERATIVE_BASE.md, which owns G1-G10. This document discharges G2 only."
parents:
  - 52_THE_GENERATIVE_BASE.md
  - 53_THE_NUMBER_CHART.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/42_THE_CASE_FOR_FINITY.md
---

# G2 — Prior-Art Adjudication and Proof

> **Verdict: KNOWN-UP-TO-REFORMULATION.**
> G2 is **true**. It was never open. It is Euclid's algorithm.

The corpus carried G2 as a conjecture `[C]` with bounded evidence `[B]`, and
`52_THE_GENERATIVE_BASE.md:141` recorded that *"a complete injectivity proof is
still owed for this exact reduction grammar."* That debt is discharged here —
not by new mathematics, but by naming the theorem G2 already was.

This is the honest outcome, and it is worth more than a contested novelty
claim. The corpus's own `F1` gate (`42_THE_CASE_FOR_FINITY.md:195`) requires a
result *beyond prior art*. G2 is not beyond prior art. **F1 is not passed by
G2**, and this document says so before anyone can be misled by it.

---

## 1 · The claim, exactly as the corpus states it

From `52_THE_GENERATIVE_BASE.md:137-141`:

```text
PRIMITIVE      1
OPERATIONS     S(x) = x + 1          the successor
               ι(x) = 1 / x          the inversion

A WORD is a finite string over {S, ι}; val(w) applies its letters
left to right to 1.

A word is REDUCED if it contains no ιι and does not begin with ι.

G2:  w ↦ val(w) is a bijection from reduced words onto ℚ⁺.
```

Surjectivity is `G1` (already proved, `52:125-135`). Only **injectivity** was
owed.

## 2 · The dictionary

Every nonempty reduced word factors uniquely as

```text
w  =  S^a₀ ι S^a₁ ι ⋯ ι S^aₖ ι^ε        k ≥ 0,  ε ∈ {0,1}
```

with `a₀ ≥ 1` (no leading `ι`) and `aᵢ ≥ 1` for `1 ≤ i ≤ k` (no `ιι`). Then:

```text
val(w)  =  [aₖ; aₖ₋₁, …, a₁, a₀ + 1]                    if ε = 0
val(w)  =  1 / [aₖ; aₖ₋₁, …, a₁, a₀ + 1]                if ε = 1
```

*Proof of the dictionary, by induction on `k`.* For `k = 0`, `ε = 0`:
`val(S^a₀) = 1 + a₀ = [a₀ + 1]`. For the step, write `w = w′ ι S^aₖ` where
`w′ = S^a₀ ι ⋯ S^aₖ₋₁`. Then
`val(w) = aₖ + 1/val(w′) = aₖ + 1/[aₖ₋₁; …, a₁, a₀+1] = [aₖ; aₖ₋₁, …, a₁, a₀+1]`.
The `ε = 1` case is one further application of `ι`. ∎

**The load-bearing detail is the `+1` on the last partial quotient.** `val`
starts *at* `1`, so the leading block `S^a₀` contributes `a₀ + 1`, not `a₀`.
Since `a₀ ≥ 1`, the last partial quotient is **`≥ 2`**.

That is not a coincidence and it is not bookkeeping. **`a₀ ≥ 1` — the
no-leading-`ι` rule — is exactly the classical normalisation that makes the
continued fraction expansion unique.** The corpus derived the right constraint
from the right reason (`ι(1) = 1`, so a leading `ι` is the empty word) and did
not notice it had re-derived Hardy & Wright's hypothesis.

## 3 · The trichotomy

```text
val(ε)   = 1
w ends in S   ⟹  val(w) > 1
w ends in ι   ⟹  val(w) < 1
```

*Proof.* `S` and `ι` preserve `ℚ⁺`, so every value is positive. If `w` ends in
`S` then `val(w) = val(w′) + 1 > 1`. If `w` ends in `ι`, then — because `w` has
no `ιι` and does not begin with `ι` — that final `ι` is preceded by an `S`, so
`w = w′ι` with `w′` ending in `S`, giving `val(w) = 1/val(w′) < 1`. ∎

The three classes therefore occupy **disjoint** value ranges. Injectivity
across classes is free; and the `ι`-ending class is the reciprocal image of the
`S`-ending class, so it is injective iff that one is. **Injectivity reduces to
the `S`-ending branch.**

## 4 · The classical theorem

> **Theorem (uniqueness of the finite simple continued fraction).**
> If `[b₀; b₁, …, b_m] = [c₀; c₁, …, c_n]` with all partial quotients positive
> integers for index `≥ 1`, and `b_m ≥ 2`, `c_n ≥ 2`, then `m = n` and
> `bᵢ = cᵢ` for every `i`.

Hardy & Wright, *An Introduction to the Theory of Numbers*, Ch. X (the
continued-fraction uniqueness theorems; **exact theorem numbers vary by edition
and have not been checked against a physical copy here — cite the chapter, or
verify the number before printing it**); Khinchin, *Continued Fractions*, §I.2;
Perron, *Die Lehre von den Kettenbrüchen*. Every positive rational has exactly **two** finite
expansions — `[a₀; …, a_n]` with `a_n ≥ 2`, and `[a₀; …, a_n − 1, 1]` — and
requiring the last partial quotient `≥ 2` selects exactly one. The underlying
algorithm is Euclid's. `[A]`

## 5 · G2, proved

By §3 it suffices to treat reduced words ending in `S`. By §2 such a word
determines the tuple `(aₖ, aₖ₋₁, …, a₁, a₀ + 1)`, all entries `≥ 1` and the last
`≥ 2`, and `val(w)` is that continued fraction. By §4 the tuple is uniquely
determined by the value. The tuple determines `(a₀, …, aₖ)`, which determines
`w`. Hence `val` is injective on reduced words; with `G1` it is a bijection onto
`ℚ⁺`. ∎

**G2 is a theorem. Tier `[C]` → `[A]`, inherited, cite Hardy & Wright.**

## 6 · The other two vocabularies

The same result arrives by two further standard routes, both of which also
pre-date the corpus.

| Vocabulary | The standard object | What it says about G2 |
|---|---|---|
| **Stern–Brocot / Calkin–Wilf** | Each positive rational appears **exactly once** in the Calkin–Wilf tree; each is reached by a unique finite `L`/`R` path from `1/1`. `52:265` already notes `L(x) = x/(x+1) = ιSι` is a word and is the Calkin–Wilf second generator. | G2 is unique-path-in-the-tree. The corpus already cites Calkin–Wilf (`52:349`) for the cross-check and did not notice the citation also settles the conjecture. |
| **`PGL(2,ℤ)` word reduction** | `S = [[1,1],[0,1]]`, `ι = [[0,1],[1,0]]`; the reduced-word condition is a normal form in the group generated. `G9` (`52:244`) already computes these matrices. | G2 is normal-form uniqueness for the monoid. |

Neither adds anything G2 does not already get from §5. Both confirm the
verdict.

## 7 · What this does and does not cost

**Survives untouched.** `G1`, `G3`, `G4`, `G5`, `G6`, `G7`, `G8a`, `G9`, `G10`
are unaffected. The number chart's rows stay correct — `53_THE_NUMBER_CHART.md`
marked them THEOREM, and they now genuinely are. The reachability *order of
explanation* stays `[S]`, exactly as `53:163` already declared.

**Strengthens.** G2 moves from conjecture to theorem. The corpus is *more*
sound after this adjudication, not less. `53:37-38` ("Each has ONE reduced
word") is now backed.

**Costs.** The novelty claim. `52_THE_GENERATIVE_BASE.md` cannot present the
generative base as a new foundation for the positive rationals; it is the
continued-fraction algorithm in word notation. `42_THE_CASE_FOR_FINITY.md`'s
`F1` gate remains **OPEN** — G2 does not pass it and must not be cited as
passing it.

**What is genuinely the corpus's own here** is narrow and should be stated
narrowly: the observation that the two syntactic exclusions (`ιι = id`,
`ι(1) = 1`) are *the same constraint* as the classical `a_n ≥ 2`
normalisation — an expository identification, `[I]`, of real pedagogical value
and no theorem content.

## 8 · Machine check

`09_TOOLS/01_SCRIPTS/check_g2_normal_form.py` — **PASS**.

All `10945` reduced words to length `18`, exact `Fraction` arithmetic: zero
collisions; the §2 dictionary exact on **every** word; last partial quotient
`≥ 2` throughout; the §3 trichotomy holding without exception.

It carries a **mutation harness**: four mutants (allow leading `ι`; allow `ιι`;
drop the `+1`; drop the reversal) must each be rejected. All four are. A
regression that cannot fail is not evidence — this addresses the defect in the
predecessor `check_generative_base.py`, which sampled injectivity and could not
distinguish *"G2 is true"* from *"the grammar was never stressed."*

## 9 · Kills

| claim | kill |
|---|---|
| the §2 dictionary | exhibit a reduced word whose value differs from its stated continued fraction |
| last partial quotient `≥ 2` | exhibit a reduced word with `a₀ = 0`, i.e. a nonempty reduced word beginning with `ι` |
| the §3 trichotomy | exhibit a reduced word ending in `S` with value `≤ 1`, or ending in `ι` with value `≥ 1` |
| G2 itself | exhibit two distinct reduced words with the same value |
| **this verdict** | produce a source predating the corpus that states the word-form bijection and is **not** reducible to continued-fraction uniqueness — that would reopen novelty, in the corpus's favour |

**This document's own kill.** If `F1` is ever recorded as passed on the
strength of G2, or if `52`'s status line is amended to call the generative base
novel, this adjudication has been ignored and should be re-run.

## 10 · Sources

- Hardy & Wright, *An Introduction to the Theory of Numbers*, Ch. X — the uniqueness theorem for finite simple continued fractions. Theorem numbering differs across editions; **not verified against a physical copy in this pass.**
- A. Ya. Khinchin, *Continued Fractions*, §I.2 — same result, self-contained.
- Calkin & Wilf, ["Recounting the Rationals"](https://www2.math.upenn.edu/~wilf/website/recounting.pdf), *Amer. Math. Monthly* 107 (2000).
- K. Stange, ["An Arborist's Guide to the Rationals"](https://math.colorado.edu/~kstange/papers/CWSB.pdf) — Stern–Brocot / Calkin–Wilf correspondence and the continued-fraction reading of paths.
- Gibbons, Lester & Bird / Bogomolny, [Stern–Brocot tree](https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree) — path-uniqueness and the `0/1`, `1/0` boundary ancestors.
- [nLab, continued fraction](https://ncatlab.org/nlab/show/continued+fraction).
- Mathlib's `Mathlib.Algebra.ContinuedFractions.*` provides convergents, continuants and the convergents-equivalence theorem; a directly reusable *uniqueness-for-rationals* lemma was **not** located, so a Lean formalisation of §5 would still be original formalisation work — of a classical theorem.

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/55_G2_PRIOR_ART_ADJUDICATION.md`

•   ⊙   ○ — *the two exclusions were the classical normalisation all along.*
