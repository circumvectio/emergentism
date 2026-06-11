---
rosetta:
  primary_column: "Methodology"
  register: "[A] within the stated game models; [I] readings; [C] what remains of R10"
  canonical_phrase: "E2 Reflexive Empowerment — R10's Kill Criterion, Executed"
---

# E2 — Does the Coupling Appear When the Second Agent Arrives? R10's Test, Executed

**Status:** Executed 2026-06-12, per the pre-registered protocol in
[00_NEXT_EXPERIMENTS_SPECS.md §E2](00_NEXT_EXPERIMENTS_SPECS.md). Two games from
the spec's own menu (2-player p-beauty cognitive hierarchy; bounded-lookahead
iterated PD vs trembling execution), plus one documented instrument refinement
(V2: depth-graded opponents). Deterministic, stdlib, no sampling anywhere.
**Verdict: SPLIT, with teeth. The INTERACTION half of R10 is supported — the
reflexive register is complementary/multiplicative exactly where R6's
solipsistic register was additive, with the zero-factor catastrophe appearing
literally. The CONSERVATION half is not recovered — Φ-as-depth saturates and
oscillates, no conserved hyperbola family, and real budgets buy reliability,
not depth. R10 splits into R10a (supported) and R10b (open, weakened).**

**Artifacts:** [E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM.py](E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM.py)
(V1: both games), [E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V2.py](E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V2.py)
(V2: contact game, depth-graded opponents). Registered predictions in each
docstring, written before each first run.

## 1. The formal core

- **Game A (relational accuracy):** me `(k, c)` vs a fixed Poisson(τ=1.5) CH
  population; `k` = belief-recursion depth, `c` = action-channel bits
  (quantization). Both capacities feed one scalar distance to the target
  `t = p·mean`.
- **Game B (contact):** me `(k, c)` vs five reactive automata; `k` =
  receding-horizon planning depth (DP against the known automaton; `k=0` =
  myopic defection), `c` = execution reliability (tremble `ε = 2^-c`). The
  plan is realized only *through* execution against a retaliating other.
  V2 replaces the population with depth-graded automata (TF2T, SLEEPY-GRIM,
  FORGIVE-GRIM + TFT, GRIM) to probe deeper `k`.
- **Fits:** additive vs symmetric-product vs Cobb-Douglas vs CES (ρ̂ is the
  one-number verdict: ρ≈1 additive, ρ≈0 multiplicative, ρ<0 complementary);
  direct iso-contour line-vs-hyperbola; budget leg with **measured** think-cost
  (operation counters) against linear channel cost — interior optimum on a
  linear budget is the complementarity signature.

## 2. Results (verbatim, key lines)

```
GAME A (accuracy):  CES rho=+0.50 (smooth) / +0.75 (win); CD ~ additive
  argmax_k per c: [1, 3, 2, 3, 4, 6, 5, 5]   (optimal depth is population-relative)
  win-payoff iso-contours: hyperbola 0.949 vs line 0.750
  budget leg: interior optima at B=6,8,10 (fraction 0.60)

GAME B V1 (contact, memory-1 opponents):
  k-lift at c=1 (eps=.5): 0.0000 exactly  ->  V(plan, coin-flip) = V(no-plan, coin-flip)
  k-lift at c=8:          +0.73
  CES rho=+0.01 (Cobb-Douglas), CD 0.898 vs additive 0.718
  LIMITATION: k-rows identical for k>=1 (memory-1 opponents saturate depth)

GAME B V2 (contact, depth-graded opponents):
  k=0 row FALLS with reliability: 1.79 -> 1.34   (reliable defection locks in punishment)
  k>=1 rows RISE with reliability: 1.79 -> 3.32  (sign-crossing in dV/dc)
  k-lift at c=1: -0.000 exactly (zero-factor again); at c=8: +1.78
  depth-lift (k=6 vs k=1): NEGATIVE (-0.06..-0.20), parity oscillation
  CES rho=-0.25, CD 0.876 vs additive 0.542
  budget leg: corner optima everywhere (k*=1, all marginal budget -> c)
```

## 3. Findings

**F-E2-1 — The coupling DOES appear when the second agent arrives. `[A]` within
the stated models.** R6's solipsistic register was additive (iso-lines, sum
conserved 6–10× better than product). The contact register is decisively NOT
additive: Cobb-Douglas/CES beat the additive fit by ΔR² ≈ 0.18–0.36, and V2
exhibits a **sign-crossing** — `∂V/∂c > 0` for planners, `∂V/∂c < 0` for the
non-planner — which **no additive surface can produce** (additivity forces
`∂V/∂c` independent of `k`). Reliability does not add value; it **amplifies the
plan, including its badness**. This is the multiplicative/conjunctive class of
the Dyadic Coupling Law, appearing exactly where R10 predicted: at contact.

**F-E2-2 — The zero-factor catastrophe is literal, twice. `[A]` within models.**
At coin-flip execution (`ε = 0.5`) the entire value of planning is erased to
the fourth decimal, in both V1 and V2 (`k-lift = 0.000` at `c=1`). *"Everybody
has a plan until they get punched in the mouth"* is, in this model, an exact
statement: `V(plan, no-execution) = V(no-plan, no-execution)`. The street
register and the sim agree.

**F-E2-3 — But there is no conserved product: Φ-as-depth saturates and
oscillates. `[A]` within models; the honest half.** Lookahead beyond `k=1`
adds nothing against memory-1 opponents (V1) and is *negative with parity
oscillation* against depth-graded opponents (V2: even-horizon plans overharvest
into retaliation — the myopic-tail end-effect of receding-horizon DP). The
`k`-axis is not a smooth conjugate coordinate in these games; effective Φ is
closer to **plan-quality (≈ binary: sees retaliation or not)** than to a depth
continuum. No `φ·ν = const` hyperbola family exists on this surface, and the
budget leg buys reliability, not depth (corner optima, interior fraction 0.00
in B). Game A honors the conjugate trade better (interior optima 0.60, win-payoff
iso-contours hyperbolic 0.949 vs 0.750) but its overall shape is intermediate
(ρ̂ = +0.5/+0.75), not the sphere.

**F-E2-4 — Reflexivity makes Φ relational, not absolute. `[A]` within models.**
In Game A the optimal depth varies with the channel and tracks the population
(`argmax_k` per `c` = 1..6, non-monotone): being *deeper* is not better —
being **one step deeper than the other** is. A depth that overshoots the
population loses value. This is structure single-agent empowerment cannot
express (R6's register has no "other" to be relative to), and it is evidence
that the reflexive register is a genuinely different object — while also being
*another* reason the simple conserved-product geometry does not fit it.

**F-E2-5 — The verdict against the spec's decision table: neither row fires
cleanly; the honest outcome is a SPLIT. `[S]`** Row 1 (lines everywhere → R10
refuted) does NOT fire — additivity is decisively beaten at contact. Row 2
(hyperbolae + forced conjugate cost → R10 supported) does NOT fully fire — the
conjugate budget trade fails in B and the hyperbola family does not exist on
the realized surfaces. Therefore **R10 splits**:

- **R10a — reflexive interaction (SUPPORTED `[A]` within models):** the
  multiplicative/complementary coupling of foresight and execution appears in
  multi-agent contact, with the zero-factor catastrophe, where the single-agent
  register was additive. The arrival of the second agent creates the coupling
  R6 could not find. The agency gloss has formal teeth *at this level*.
- **R10b — reflexive conservation (`φ·ν = 1` as a conserved law: NOT
  SUPPORTED here; stays `[C]`, weakened):** no conserved product, no smooth
  conjugate trade-off, depth saturates. What survives of the sphere at contact
  is the *product form and its catastrophe*, not the *conservation law*.

## 4. Scoring the registered predictions (the program's discipline)

| Prediction | Outcome |
|---|---|
| V1-P1: Game A additive | **WRONG in part** — intermediate (ρ̂ +0.5/+0.75), win-register iso-contours hyperbolic. Pre-registration caught the author's own deflationary bias. |
| V1-P2: Game B multiplicative | **RIGHT** — CD/CES win decisively, both versions. |
| V1-P3 / V2-P-V2c: real budgets force a conjugate trade | **WRONG for B** (corner optima; depth not worth buying), partially right for A (interior 0.60). |
| V2-P-V2a: depth-graded opponents unsaturate Φ | **FAILED** — saturation persists with parity oscillation; recorded as a finding (F-E2-3), not hidden. |
| V2-P-V2b: interaction persists, ρ ≤ 0.3 | **RIGHT** — ρ̂ = −0.25, zero-factor exact. |

Two of five registered predictions were wrong and are reported as wrong. The
spec's instruction — *"Do not pre-judge; run it"* — was honored in both
directions.

## 5. What this moves

- **The findings ledger:** R10 row → split into R10a (supported `[A]` within
  models) and R10b (open `[C]`, weakened). The teleology thread now has its
  first *positive* formal result since the R6 kill — scoped to interaction,
  not conservation.
- **The Dyadic Coupling Law:** gains a fifth witness — the contact game's
  sign-crossing and exact zero-factor (existentially conjunctive: plan AND
  execution), with the *boundary* honestly marked (no conservation law at
  contact).
- **The honest scoreboard:** "the sphere survives at contact" is now a **half-
  truth to be retired**: the *product* survives; the *conserved product* does
  not (in these games).

## 6. Limitations and the open fork (V3, designed, NOT run)

1. Both games use **fixed** opponent populations; true depth-vs-depth mutual
   modeling (the spec's sender–receiver-with-nested-beliefs option, or k vs
   k_opp tournaments) might unsaturate Φ where fixed automata cannot. That is
   the remaining live route for R10b. Pre-registered expectation if run:
   relational depth effects (F-E2-4) strengthen; a conserved product remains
   unlikely.
2. The receding-horizon parity oscillation is an instrument property of
   finite-horizon DP as much as a phenomenon; a discounted-infinite-horizon
   planner would remove it (and likely flatten the k-axis further, against
   R10b).
3. Quantization (Game A) makes V non-monotone in `c` at low bits — real but
   it adds fit noise; the contour extractor failed on plateaued regions of
   the smooth payoff (reported as ambiguous, not forced).
