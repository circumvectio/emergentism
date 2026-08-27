---
rosetta:
  primary_level: L3
  primary_column: Formal system — lemma
  secondary:
    - level: L1
      column: Boundary
      role: "both premises shown necessary by boundary counterexample; neither may be dropped"
    - level: L2
      column: Method
      role: "the stronger claim (unimodality) is delimited by a valid counterexample, not asserted away"
  operator: "Kṛṣṇa ◇"
  tier: "Executive"
  regime: "Vaiśya"
  register: "[A] the lemma within its stated premises; [C] every application to a natural register"
  canonical_phrase: "SAT-01 — a costly stabiliser whose absence is fatal forces an interior optimum; the mechanism that enables a freedom consumes it at saturation"
type: formal-result
title: "The Saturation Lemma — SAT-01"
date: 2026-08-27
status: "[A/C] ACTIVE — the lemma is elementary and proved within its premises. Its APPLICATION to any physical, biological, or institutional register is [C] and separately owed. PRIORITY IS UNESTABLISHED: a four-lane prior-art sweep was launched before this was written and had not returned at the time of writing. No novelty is claimed."
evidence_tier: "[A] the lemma, its closed form, and both counterexamples — machine-verified; [I] the reading of W19's pole clause as this structure; [C] every register application"
proposer: "Yves R. Burri — the pole clause, stated 2026-08-22: 'at its extreme the compensator consumes the freedom it services.'"
assistance: "Formalization, proof, numerical verification and adversarial probing by the session AI. No AI coauthor, authority, or priority."
parents:
  - ../../06_ONTOLOGY/13_THE_COMPENSATION_WAGER_2026_08_22.md
  - 59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md
  - ../../00_THE_WELTANSCHAUUNG_BY_REGISTER_2026_08_27.md
---

# The Saturation Lemma — SAT-01

> **What this is.** `W19`'s pole clause — *"at its extreme, a compensator consumes
> the freedom it services"* — made exact. It becomes a two-premise lemma with an
> elementary proof, an exact closed form on a natural family, and a counterexample
> delimiting the stronger claim that was tempting and is false.
>
> **What this is not.** Not a claim about nature. The lemma says what follows *if*
> the two premises hold in a register. Whether they hold anywhere is `[C]` and is
> owed separately, register by register.

## 1 · Statement

Let a register carry a **freedom** `F` (a measurable capacity) and a **compensator**
`C ∈ [0,1]` (a mechanism maintaining an invariant the freedom would otherwise
violate). Write the realised freedom as a product of two continuous, non-negative
factors:

```text
F(c) = A(c) · S(c)
```

- **`A(c)` — available capacity.** What remains for the freedom after compensation
  is paid.
- **`S(c)` — persistence.** The fraction of the freedom that survives, given
  compensation `c`.

**Premise P1 — compensation is costly, and exhausts.**
`A` is non-increasing on `[0,1]` with **`A(1) = 0`**.

**Premise P2 — uncompensated freedom does not persist.**
`S` is non-decreasing on `[0,1]` with **`S(0) = 0`**.

> **SAT-01.** Under P1 and P2, if `F(c) > 0` for some `c ∈ (0,1)`, then `F` attains
> its maximum at an **interior** point. The compensator that enables the freedom
> consumes it at saturation.

## 2 · Proof `[A]`

`F = A·S` is continuous on the compact `[0,1]`, so by the extreme value theorem it
attains a maximum. At the endpoints:

- `F(0) = A(0)·S(0) = A(0)·0 = 0` — by **P2**.
- `F(1) = A(1)·S(1) = 0·S(1) = 0` — by **P1**.

Since `F` is non-negative and positive somewhere in `(0,1)` by hypothesis, the
maximum exceeds `0` and therefore cannot be attained at either endpoint. It is
attained in the interior. ∎

The proof is elementary. **That is a feature, not an apology**: the content is not
mathematical depth but the identification of *which two premises* force the
structure — and the demonstration below that neither can be dropped.

## 3 · The closed form on the natural family `[A]`

For `A(c) = (1−c)^a` and `S(c) = c^b` with `a, b > 0`:

```text
argmax F  =  b / (a + b)
```

Verified numerically at 200 001 sample points: `a=1,b=1 → 0.50000`;
`a=2,b=1 → 0.33333`; `a=1,b=3 → 0.75000`; `a=5,b=2 → 0.28571` — each matching the
closed form to five decimals. **The optimum is the ratio of the persistence
exponent to the total.** A freedom whose survival depends steeply on compensation
optimises at high compensation; one whose capacity is expensive optimises at low.

## 4 · What the lemma does NOT give — and the counterexample that proves it `[A]`

It is tempting to conclude that `F` is **unimodal** — a single clean inverted U.
**That is false, and the temptation is exactly where an overclaim would enter.**

**Counterexample, with both premises strictly satisfied:**

```text
A(c) = 1 − c                          decreasing, A(1) = 0            ✓ P1
S(c) = c + 0.995·sin(40c)/40          S′ = 1 + 0.995·cos(40c) ≥ 0.005 > 0,
                                      so S is strictly increasing, S(0) = 0  ✓ P2
```

Machine-checked over 200 001 points: both premises hold, and `F = A·S` has **five
distinct interior maxima.** An interior optimum is guaranteed; *a single* interior
optimum is not.

**What buys unimodality:** log-concavity of `A` and `S`. Log-concavity is closed
under multiplication, so `log F` is concave and `F` has one peak. Verified on the
power family — every case returns exactly one interior maximum. **Anyone invoking
"the inverted U" rather than "an interior optimum" is silently assuming
log-concavity and owes that assumption.**

## 5 · Both premises are load-bearing `[A]`

Neither may be weakened; each failure moves the optimum to a boundary, machine-checked:

| premise relaxed | consequence | argmax |
|---|---|---|
| `A(1) > 0` — compensation never exhausts the budget | no saturation penalty | `c = 1.0000` (boundary) |
| `S(0) > 0` — the freedom persists uncompensated | no necessity of compensation | `c = 0.0000` (boundary) |

**This is the lemma's real content.** The interior optimum is not a general fact
about freedoms and constraints. It appears exactly when a stabiliser is *both*
**necessary** (P2) *and* **exhausting** (P1) — and a register that fails either
premise has a boundary optimum, correctly.

## 6 · Reading, and the fence `[I]`

The lemma formalises `W19`'s pole clause and explains its two-faced structure: the
same mechanism enables (`S` rising) and consumes (`A` falling), so *enabling and
constraining are not two effects — they are one function seen on either side of its
peak.*

It also proposes a **structural account of a widespread empirical pattern**:
wherever a capacity requires a costly stabiliser, an interior optimum is *forced*
rather than observed. Whether that account is new is **unestablished** — see §8.

**Fences, each load-bearing:**

- **Nothing physical is derived.** The lemma is about products of real functions.
  Applying it to gravity, confinement, audit, or any register requires
  independently measuring `A`, `S`, and `F` in that register, and is `[C]`.
- **The decomposition is a modelling choice**, not a discovery. Writing a realised
  freedom as `capacity × persistence` must be *defended per register*, not assumed.
  A register where the two factors are not separable is outside scope.
- **`W19`'s gauge language is untouched.** This lemma supplies no gauge structure
  and does not advance the gauge-form admission test.
- **The graves hold.** Nothing here revives `φν = 1` as a discovery, the force
  bijection, the retired arithmetic, or the kernel→ethics warrant. In particular
  the interior optimum here is **not** the chart's equator: it is derived from P1
  and P2, not from a coordinate identity, and `DF-05` is untouched.

## 7 · Discriminators — how a register earns the lemma

For a candidate register, independently:

1. Name and measure `F`, `A`, `S` **without** using one to define another.
2. Show `A(1) = 0` — that saturating compensation leaves no capacity.
3. Show `S(0) = 0` — that the uncompensated freedom does not persist.
4. Predict `argmax` **before** measuring it, and test the prediction held out.

**First target, because the data already exists:** the verification register.
`A` = the fraction of budget left for acting after auditing; `S` = the survival of
claims under audit. `A(1) = 0` is the total-audit case — all verification, no
action. `S(0) = 0` is the unverified case — the 2026-08-27 adversary result
measured eight of eight gates admitting artifacts that pass while violating what
they certify, which is direct evidence that unverified claims do not persist as
true. Both premises are *plausible* there and neither is yet *measured*.

## 8 · Priority — unestablished, and deliberately so

A four-lane prior-art sweep (inverted-U ubiquity; physics saturation; control and
audit economics; philosophy of enabling constraint) was **launched before this
document was written** and had not returned at the time of writing. Strong
candidate occupants are already named and must be cited when the sweep lands:
Yerkes–Dodson; Calabrese on hormesis; Grant & Schwartz (2011) on the inverted U;
life-history theory's cost/benefit tradeoffs; optimal-monitoring results in agency
economics; Deacon and Juarrero on enabling constraint.

**Six candidate contributions were audited on 2026-08-22 and all six were
pre-empted.** The prior on this one being unowned is therefore low, and this
document claims nothing. If the sweep finds an occupant, SAT-01 becomes a citation
with a machine-verified counterexample attached — which is worth having either way.

## 9 · Kills

| claim | dies if |
|---|---|
| SAT-01 itself | a continuous `F = A·S` is exhibited satisfying P1 and P2 whose maximum is on a boundary |
| the necessity of P1 | an interior optimum is forced with `A(1) > 0` |
| the necessity of P2 | an interior optimum is forced with `S(0) > 0` |
| the unimodality delimitation | the five-peak counterexample is shown to violate a premise |
| the structural reading (§6) | the widespread inverted-U pattern is shown to arise mostly where the two premises fail |
| **priority** | the sweep finds an occupant — then this is cited, not mourned |

**Verification:** `09_TOOLS/01_SCRIPTS/check_saturation_lemma.py` — re-runnable;
2 000 random admissible pairs, the closed form at 200 001 points, the five-peak
counterexample with premise checks, and both boundary cases.

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/03_FORMAL_SYSTEM/60_SATURATION_LEMMA_SAT_01.md`

•   ⊙   ○ — *what holds a thing up, held to its extreme, takes it down.*
