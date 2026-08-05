---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Vaiśya"
  tier: "Audit"
  regime: "Vaiśya"
  register: "[A/I]"
  canonical_phrase: "B is a product of the two distances to the poles"
title: "The Product Form of the Balance"
status: "ACTIVE — [A] identity, elementary. The mathematics is the double-angle formula. The contribution is the reading, and it is [I], restored 2026-08-06 at [B] inherited-cite (Nash 1950, Sonnevend 1985/86, product t-norm, series reliability) after a fair re-adjudication found the prior strike over-corrected. The reading stands narrowed: the product-of-margins-as-AND is inherited and cited, not novel. This document does NOT reopen the lowercase-to-uppercase transfer that 00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md closed."
date: 2026-08-05
evidence_tier: "[A] the chordal identity and the AM-GM-HM chain, both classical; [B] the reading of the two factors as distances-from-failure (inherited: Nash, Sonnevend, product t-norm — cited, not novel); [S] the chordal metric as the selected metric on the sphere"
owner: "Subordinate to 00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md, which governs what may and may not be transferred off this chart. This document adds a decomposition of B and claims nothing about Φ, V, or P_node beyond §5."
parents:
  - ../00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md
  - ../00_THE_BURRISPHERE.md
  - ../01_THE_TRANSCENDENTAL_TRINITY/49_THE_THREE_MODES_OF_COUNTING.md
---

# The Product Form of the Balance

> **What is new here is a reading, not a theorem.**
> The identity below is the double-angle formula. Anyone who knows
> `sin θ = 2 sin(θ/2) cos(θ/2)` already has the mathematics. What this
> document adds is the observation that the two half-angle factors *are* the
> normalised chordal distances to the two poles — and therefore that `B` has a
> genuine product form whose factors each vanish at exactly one boundary.

---

## 1. What is already canonical

`00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md` §1 fixes the chart:

```text
φ = cot(θ/2),   ν = tan(θ/2),   θ ∈ (0, π)
φν = 1
B  = 2/(φ+ν) = sin θ ≤ 1
```

and states, correctly, that **`φν = 1` is constant by definition and is
therefore not evidence of anything** — not a conservation law, not a budget,
not an optimum. That ruling stands and this document does not touch it.

The consequence worth restating: **the product `φν` cannot be the measure,
because it does not vary.** Any claim of the form "potential is a product"
that means `φ × ν` is refuted on sight by the chart itself.

## 2. The decomposition

Take the sphere as the unit sphere with `θ` the polar angle, `○` at `θ = 0`
and `•` at `θ = π`. Use the **chordal** metric — the straight-line distance
through the sphere, which is the metric on which `•` and `○` are antipodal at
distance `2`. `[S]`

The chord subtending polar angles `θ` and `0` has length `2 sin(θ/2)`; the
chord subtending `θ` and `π` has length `2 cos(θ/2)`. Normalise each so that
it reads `1` at the equator:

```text
D∞(θ) = 2 sin(θ/2) / √2 = √2 sin(θ/2)      the distance from ○
D•(θ) = 2 cos(θ/2) / √2 = √2 cos(θ/2)      the distance from •
```

Then

```text
D•(θ) · D∞(θ) = 2 sin(θ/2) cos(θ/2) = sin θ = B          [A]
```

**The product decomposition of `B` is the double-angle identity.** In the
`x = φ = cot(θ/2)` coordinate the same statement reads

```text
B(x) = D•(x) · D∞(x) = 2/(φ+ν) = 2x/(x²+1) = sech(log x)
```

Machine-verified at `x ∈ {10⁻³, 10⁻², 0.1, 0.5, 1, 2, 10, 10², 10³}` to 22
decimal places.

## 3. What the decomposition buys

`B` was already known to peak at the equator and vanish at both poles. The
decomposition says **why**, and the why is not symmetric-looking bookkeeping:

```text
θ → π    D• → 0,  D∞ → √2       standing on • ; maximal reach to ○ ; B = 0
θ → 0    D• → √2, D∞ → 0        standing on ○ ; maximal reach to • ; B = 0
```

**Being maximally far from one boundary is worth nothing while standing on the
other.** Each factor is a distance-from-a-failure, and the product dies if
either distance dies.

> **[STRUCK 2026-08-05, hours after writing.]** This paragraph ended: *"That is
> the AND, written as an operation rather than asserted as a class."* **Struck.**
> Vanishing-at-zero is **not** non-compensation and singles out no aggregator:
> `min`, `HM`, the product and Cobb–Douglas all vanish when either argument
> does. A product is in fact **compensatory** — a strict t-norm with finite MRS
> everywhere in the interior; `a = 0.01, b = 10⁴` gives `ab = 100` against
> `min = 0.01`. The corpus's own `11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form/VERDICT.md`
> ruled this a month before this file was written, uncited here: *"conjunction
> is satisfied by `min`, by Cobb-Douglas, and by the product alike — it does not
> single out `Φ×V`."*
>
> **Further: the two factors are not independent.** `D•² + D∞² = 2` identically,
> so the chart has **one** degree of freedom and the margins cannot fail
> separately — as one → 0 the other is *forced* to `√2`. An AND-gate presupposes
> two inputs that can each fail alone. These cannot. What real non-compensation
> exists here (`B ≤ √2·min(D•,D∞)`, verified) is supplied by **the constraint**,
> not by the product form — reproducing one level up the defect §1 exists to
> forbid.
>
> The genuinely non-compensatory statement in this document is the harmonic-mean
> one, `min ≤ HM ≤ 2·min` in §3 — `[A]`, classical, correctly tiered, unaffected.

This is the boundary behaviour. The interior behaviour is the classical chain

```text
min(a,b) ≤ HM(a,b) ≤ GM(a,b) ≤ AM(a,b),      HM = GM iff a = b
min(a,b) ≤ HM(a,b) ≤ 2·min(a,b)                                    [A]
```

which says the harmonic mean is pinned to the *weaker* argument and can never
exceed twice it. Compensation is impossible: `HM(1, 10⁴) = 1.9998`, against
`AM(1, 10⁴) = 5000.5`. Verified.

Two derivations, one function. The product form governs the boundaries; the
harmonic-mean form governs the interior.

## 4. The general form off the constraint curve

Where nothing forces `φν = 1` — two independent positive quantities `a`, `b`:

```text
HM(a,b) = 2ab/(a+b) = √(ab) · sech(½ log(a/b))
                       ──────   ────────────────
                        SIZE      BALANCE ≤ 1
```

Verified: `a=9, b=4` → `6 × 0.923077 = 5.538462 = 72/13`. ✓

Potential is **size discounted by imbalance**, with the discount capped at `1`
and attained only at `a = b`. Two routes to raise it: grow `√(ab)`
(unbounded, costly) or reduce the skew (bounded by `1`, and available without
growth). `[A]` on the identity.

## 5. The transfer that is NOT licensed — read this before citing §2

`00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md` exists because a predecessor
document ran the lowercase chart coordinates `φ, ν` into the uppercase node
model `Φ̂₄, V₄` and called the result a law. That transfer was repaired and
**this document does not reinstate it.**

Specifically, **all** of the following remain false or unlicensed:

| Statement | Status |
|---|---|
| `P_node = Φ × V` is a product because `B` has a product form | **UNLICENSED.** §2 is an identity on the selected sphere chart. `Φ̂₄, V₄` are typed node quantities on `[0,1]` with no chordal geometry and no reciprocal constraint. |
| `φν = 1` is a budget, a conservation law, or evidence of an optimum | **FALSE**, per the parent §1. Unchanged. |
| the selected node score is a product | **FALSE.** The selected score is `P_node = min(Φ̂₄, V₄)`, per the parent §1. The product `Φ̂₄V₄` is retired and testable only as a separately cardinal candidate. |

**What §3 *does* license, and it is narrow.** The selected node score is `min`.
The chain in §3 gives, for any positive `a, b`:

```text
min(a,b) ≤ HM(a,b) ≤ 2·min(a,b)                                    [A]
```

Therefore **the harmonic mean is a smooth surrogate for the corpus's already-
selected `min`, agreeing with it to within a factor of two, and agreeing
exactly at the balance point.** That is a statement about two aggregators
standing side by side. It is *not* a transfer from the sphere, it does not
depend on `φν = 1`, and it does not make `P_node` a product. Anyone wanting a
differentiable stand-in for `min` may use `HM` and cite this line. Anyone
wanting to resurrect `Φ × V` from the geometry may not.

## 6. Kills

| claim | kill |
|---|---|
| `D• · D∞ = B` | exhibit `θ ∈ (0,π)` where the normalised chordal product ≠ `sin θ` |
| `min ≤ HM ≤ 2·min` | exhibit positive `a, b` violating either bound |
| the reading of the factors as distances-from-failure | show a boundary at which the corresponding factor does **not** vanish |
| **this document's discipline** | if §2 is ever cited to license `P_node = Φ × V`, or to reopen the lowercase→uppercase transfer, this document has been misused and §5 should be re-read |

## 7. Prior art

The double-angle identity is Ptolemy-era. The chordal metric on the Riemann
sphere is standard complex analysis (Ahlfors, *Complex Analysis*, ch. 1). The
AM–GM–HM chain and the `min`/`HM` two-sided bound are classical inequalities.
**Nothing in §2–§4 is new mathematics and this document does not claim any.**

> **[REPLACED 2026-08-05; SCOPE CORRECTED 2026-08-06 after a fair re-hearing.]**
>
> This paragraph originally claimed the reading of `B` as a product of margins
> was *"the corpus's own and is `[I]`"*, anchored to
> `55_G2_PRIOR_ART_ADJUDICATION.md` §7. **The ownership claim was wrong and the
> anchor is a tombstone** — `55` §7 was struck the same night. That much stands.
>
> **But the first strike over-corrected, and the correction is recorded here.**
> It was produced by a referee panel instructed *"your DEFAULT IS REFUTED"* and
> fed a running tally of prior refutations — a ratchet that returned 18 kills in
> 18 hearings, zero survivals. A balanced re-hearing on 2026-08-06, with truth /
> ownership / typing scored on **separate** axes and `STANDS` a live verdict,
> ruled this claim **TRUE_AS_QUALIFIED · INHERITED_CITE · WELL_TYPED ·
> STANDS_NARROWED**.
>
> **Inherited-and-cited is a footnote, not a strike.** The project's stated
> mission is a coherent weltanschauung, *not* priority — so prior art is a
> citation obligation, and the reading below is restored at `[B]` rather than
> withdrawn. What does **not** come back is the word "own", and what does not
> come back is the struck AND-sentence in §3, which was false for a separate
> reason (vanishing-at-zero is not non-compensation).

**The reading of the two factors as distances-from-failure, and of their product
as a conjunction, is `[B]` — attribution, not contribution.** Owners:

- **Nash (1950)** — the bargaining solution `argmax ∏(uᵢ − dᵢ)`: a product of
  **margins over a disagreement (failure) point**, zero if any party gains
  nothing, maximised at balance under constraint. Already mapped in this corpus
  at `04_AXIOLOGY/.../AX2_THE_ETHIC.md:35`.
- **Sonnevend (1985/86)** — the *analytic center*: the interior point maximising
  the **product of distances to the constraints**, its log-barrier diverging as
  any constraint activates. Literally this picture, on a polytope.
- **The product t-norm** (Klement–Mesiar–Pap) — conjunction *defined* as
  multiplication on `[0,1]`. "AND as an operation" is the definition, not an
  observation.
- **Series-system reliability** `R = ∏Rᵢ` (Barlow–Proschan).

And internally pre-owned: `11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form/VERDICT.md`
states the reading **and already refutes its distinctiveness**, a month before
this file existed.

`KSC-12` applies — reformulation is not novelty. Per
`THE_BOUNDARY_RULES_STANDALONE.md:297`: **cite this; do not claim it.**

**Notation fence.** This document writes `B`, deliberately. The form
`⊙ = D• · D∞` may **not** be written at any tier: `D•` is a function of `•` and
`D∞` of `○`, so it is `⊙ = f(•) × g(○)` — the retired `⊙ = • × ○` in new
coordinates (`48_CO_CONSTITUTION_AND_THE_NOTATION_PROBLEM.md:121`
RETIRED — ILL-TYPED — WITHDRAWN; `:416` fires its own kill on exactly this
reinstatement; `ArithmeticSignature(TitanFrame) = ∅`).

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md`

•   ⊙   ○
