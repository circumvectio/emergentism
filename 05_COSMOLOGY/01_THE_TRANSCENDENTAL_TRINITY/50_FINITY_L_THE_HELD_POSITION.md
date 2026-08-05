---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Vaiśya"
  tier: "Audit"
  regime: "Vaiśya"
  register: "[A/C]"
  canonical_phrase: "The living case pays to stay at the optimum"
title: "Finity_L — The Held Position"
status: "DRAFT [C] — conjecture with a theorem attached to a hypothesis nobody has met. The general shape is heavily owned prior art and is NOT claimed. The narrow claim in §4 is unverified. F3 remains OPEN and this document does not pass it."
date: 2026-08-05
evidence_tier: "[B] the prior-art survey in §1; [A] the theorem in §4; [C] the empirical claim in §4 and everything in §3; [I] the teleological reading in §5"
owner: "Subordinate to 42_THE_CASE_FOR_FINITY.md (F-gates) and 00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md (what may be transferred off the chart)."
parents:
  - 42_THE_CASE_FOR_FINITY.md
  - 49_THE_THREE_MODES_OF_COUNTING.md
  - ../03_FORMAL_SYSTEM/56_THE_PRODUCT_FORM_OF_THE_BALANCE.md
  - ../00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md
---

# Finity_L — The Held Position

## 1 · Prior art, first — as `55` did it

The general claim *"a living system is one that actively holds a state against
drift"* is **owned, repeatedly, and by better-known work than this corpus.**
It is written here before the claim so that nobody reads the claim first.

| Source | What it already says |
|---|---|
| Cannon, *The Wisdom of the Body* (1932) | **Homeostasis.** Living systems actively maintain internal variables against external perturbation. |
| Ashby, *Design for a Brain* (1952) | **Ultrastability.** A system with a second-order feedback loop that re-parameterises itself to return essential variables to viable bounds. |
| Maturana & Varela (1972–80) | **Autopoiesis.** The living is that which continuously produces the network that produces it. |
| Rosen, *Life Itself* (1991) | **(M,R)-systems.** Metabolism-repair closure as the criterion of the organism. |
| Sterling & Eyer (1988); Sterling (2012) | **Allostasis.** Setpoints are actively predicted and moved, not merely defended. |
| Friston (2010) | **Free-energy principle.** Organisms act to minimise the surprise of their sensory states, i.e. to remain in a small set of expected states. |

**Finity_L's general shape is none of these authors' idea and is not new.**
Any presentation that implies otherwise is warrant substitution and should be
rejected. `[B]`

**What the survey did *not* find** — and this is the whole of the opening:
in every framework above, **the setpoint is empirical.** 37 °C. pH 7.4. A
viability box whose bounds are measured and then stipulated. Ashby's essential
variables have bounds *given* to the model. Friston's expected states are
*learned*. No source located derives a setpoint as the extremum of a stated
functional under a stated constraint.

That gap — **a derived setpoint rather than a measured one** — is the only
thing this document claims, and §4 states it narrowly enough to be killed.

## 2 · The gap in the corpus that this fills

Everything the corpus has said about `⊙` so far is geometry, and **geometry
does not move.** `B` attains its maximum at the equator — but that is the
argmax of a *function*, not the fixed point of a *flow*. On a bare sphere a
point at the equator sits there for free, and so does a point anywhere else.

**Nothing published so far distinguishes the optimum dynamically.** Being at
the best place costs nothing and means nothing until something is trying to
move you. So:

```text
Finity_M   the band where counting is meaningful.
           Static. Every point equally "there".        ← 49, 53, 56
Finity_L   a position on that band that is HELD.
           Costs. Can fail.                            ← this document
```

## 3 · What a living system holds — two things, both costing `[C]`

The chart assumes `φν = 1`. **Nothing in physics enforces that.** In a real
system the two coordinates are two physical quantities — reach and reserve,
throughput and buffer, spend and store — and there is no law making them
reciprocal. Hence two distinct holdings:

**Structural holding — stay on the curve.** `ab = const`. The pair stays
coupled at all. Failure: the coordinates decouple and drift independently with
the environment. This is dissolution.

**Regulatory holding — stay at the point.** `a = b`. The position stays at the
argmax. Failure: still coupled, still running, but skewed — all reach and no
reserve. `√(ab)` looks healthy while `HM` collapses. Not death; **hollowing.**

With `s = log(a/b)`:

```text
ṡ  =  D(s)  +  C(s)                  drift + control

DEAD    C ≡ 0.  ṡ = D.  The system goes where the gradient takes it.
LIVING  D(0) ≠ 0  and  C makes s = 0 stable  ⟹  |C(0)| = |D(0)| > 0
```

**Nonzero expenditure at the optimum.** `D(0) ≠ 0` generically because the
environment is not at the system's setpoint and exchange with it pushes off.
The drift term is the second law; `C` is metabolism.

This whole section is `[C]` and it is a *model*, not a measurement. No real
`D` or `C` has been fitted to anything.

## 4 · The narrow claim

> **Theorem `[A]`.** For positive `a, b` under the constraint `√(ab) = c` fixed,
> `HM(a,b) = 2ab/(a+b)` attains its maximum `c` uniquely at `a = b`.
>
> *Proof.* `HM = GM · sech(½ log(a/b))` (`56` §4). With `GM = c` fixed, `HM` is
> `c` times a factor that is `≤ 1` with equality iff `log(a/b) = 0`. ∎

The theorem is free, elementary, and classical in content.

> **Claim `[C]` — the only unowned thing here.** Living systems regulate to
> `a = b`. Where a real biological pair is genuinely reciprocal — `ab`
> conserved to measurement precision — the observed setpoint will be the
> balance point, **derivable in advance**, and not an arbitrary measured value.

**The weak joint, stated plainly: no real biological pair has been shown to
satisfy `ab = const`.** Until one is exhibited, the theorem is attached to a
hypothesis nobody has met, and `Finity_L` is a well-formed conjecture and
nothing more. `F3` — scientific contact, `42_THE_CASE_FOR_FINITY.md` — stays
**OPEN**. This document does not pass it and must not be cited as passing it.

**What would discharge it.** One measured pair, in one organism, with `ab`
conserved across a perturbation range, whose regulated setpoint sits at
`a = b` — predicted before the measurement, not fitted after.

## 5 · The teleological reading, and the gap it does not close `[I]`

From `HM = GM × BAL`, exactly two routes to more capacity:

| route | bound | availability |
|---|---|---|
| grow — raise `√(ab)` | unbounded | competitive, costly, ongoing |
| balance — raise `BAL → 1` | **capped at 1** | **already yours**, no growth required |

**Every skewed system carries an unclaimed improvement its own size already
entitles it to.** A system at `a/b = 100` runs at ~2 % of its available
capacity. Growing while skewed multiplies `GM` and leaves the discount
untouched — which is what an extractive system looks like from inside: larger
every year, no more capable.

**The is–ought gap does not close here and is not claimed to.** "More capacity
is better" is a *hypothetical* imperative — better *if* continuation is willed.
Its one unusual feature is that the antecedent self-selects its audience: a
system not willing continuation stops, and then there is nobody to advise.
That is not a derivation of an ought. It is a reason the gap is narrower here
than in general, and the tier is `[I]`.

## 6 · Kills

| claim | kill |
|---|---|
| the §4 theorem | exhibit `a ≠ b` with `√(ab) = c` and `HM > c` |
| holding costs | exhibit a system holding `a = b` against a real environment with `C ≡ 0` |
| balance is free improvement | exhibit a system where raising `BAL` costs more `⊙` than it returns |
| **`Finity_L` itself** | one real regulated pair, reciprocal to measurement precision, whose setpoint is **not** `a = b` |
| **`Finity_L`'s novelty** | any source deriving a homeostatic setpoint as the extremum of a functional under a conserved constraint. This should be searched for **hard** before anything is printed — §1 is a survey, not a proof of absence |

**This document's own kill.** If `F3` is ever recorded as passed on the
strength of this document, or if §4's `[C]` is cited as `[A]`, it has been
misread and §4 should be re-read.

## 7 · What this does not touch

`00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md` governs. Nothing here transfers the
lowercase chart onto the uppercase node model, nothing here makes `P_node` a
product, and `φν = 1` remains a chart identity carrying no empirical content.
The pair `a, b` in §3–§4 is a **stipulated** pair in a stipulated model, not
`Φ̂₄` and `V₄`, and not `φ` and `ν`.

**Canonical path:**
`01_EMERGENTISM/05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/50_FINITY_L_THE_HELD_POSITION.md`

•   ⊙   ○ — *the mathematical case sits at the optimum for free; the living case pays rent.*
