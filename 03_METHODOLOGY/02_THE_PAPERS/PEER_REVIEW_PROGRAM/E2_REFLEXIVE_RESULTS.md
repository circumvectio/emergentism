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

**V3 UPDATE (2026-06-15) — the open fork is now run (§7).** Depth-vs-depth mutual
modeling does **not** recover R10b. It yields a **positional arms race**: depth is
a strictly relative good (a total order — deeper always wins), both agents run to
the boundary, and the advantage is **competed to zero** at the reflexive
equilibrium. R10a's product form and the exact zero-factor reproduce a **third**
time; F-E2-4 strengthens to a strict total order. The depth-axis route to a
conserved `φ·ν` law is now **closed** — what survives at contact is, triply, the
product form and its catastrophe, never the conservation.

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

## 6. Limitations and the open fork (V3 — now RUN, see §7)

1. Both games use **fixed** opponent populations; true depth-vs-depth mutual
   modeling (the spec's sender–receiver-with-nested-beliefs option, or k vs
   k_opp tournaments) might unsaturate Φ where fixed automata cannot. That is
   the remaining live route for R10b. Pre-registered expectation if run:
   relational depth effects (F-E2-4) strengthen; a conserved product remains
   unlikely. **RUN 2026-06-15 (§7): the expectation held in both directions —
   relational depth strengthened to a strict total order, and the conserved
   product is still absent. Φ did *un*saturate (depth now strictly dominates,
   the opposite of V2), but toward a positional arms race, not a conservation
   law. R10b's depth-axis route closed.**
2. The receding-horizon parity oscillation is an instrument property of
   finite-horizon DP as much as a phenomenon; a discounted-infinite-horizon
   planner would remove it (and likely flatten the k-axis further, against
   R10b).
3. Quantization (Game A) makes V non-monotone in `c` at low bits — real but
   it adds fit noise; the contour extractor failed on plateaued regions of
   the smooth payoff (reported as ambiguous, not forced).

## 7. V3 — depth-vs-depth mutual modeling: the arms race, not the conservation law

**Status:** Executed 2026-06-15, the open fork of §6 item 1.
[E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V3.py](E2_SUPPORT_REFLEXIVE_EMPOWERMENT_SIM_V3.py)
— a 2-player p-beauty cognitive-hierarchy tournament (my depth `k_A` vs opponent
depth `k_B`) plus a depth-mixed trembling population for the surface and budget
legs. Registered predictions in the docstring, written before first run.
Deterministic, stdlib, no sampling. **Verdict: R10b is still NOT recovered — and
now we see why mutual modeling structurally cannot supply a conservation law. The
second modeler creates a POSITIONAL ARMS RACE, not a conserved product: depth is
a strictly relative good, both agents run to the boundary, and the advantage is
competed to zero at the reflexive equilibrium. R10a's product form and the exact
zero-factor reproduce a third time; F-E2-4 strengthens from "one step ahead" to a
strict total order.**

### Results (verbatim, key lines)

```
L1 tournament W(k_A,k_B) [P(A closer to target)+½P(tie), no trembles]:
   W = 1.00 whenever k_A > k_B, 0.50 on the diagonal, 0.00 whenever k_A < k_B
   argmax_k_A per k_B = [1,2,3,4,5,6,6]; diagonal all 0.50 (ties)
   => DEPTH IS A STRICT TOTAL ORDER: payoff is a function of sign(k_A − k_B) alone

L2 surface me=(k,c) vs Poisson(1.5) depth-mixed pop (executes at c=3):
   monotone increasing in BOTH k and c; best at k=6 for every c (NO interior peak)
   zero-factor at c=0 (ε=1): k-lift = +0.000000 EXACT  → V(any depth, no-exec)=V(naive)
   fits: additive 0.805 | Cobb-Douglas 0.852 (a,b=.50,.25) | CES 0.905 ρ=+0.25
   optimal-depth ridge: k*=6 flat, slope +0.00; line R²=1.00 vs hyperbola R²<0
   budget leg (cost(k)=k+1 vs channel c): corner optima everywhere, interior 0.00

L3 reflexive best-response orbit from k=0: [0,1,2,3,4,5,6,6,6]
   ratchets +1/step to the boundary k=6, where W(6,6)=0.50 (advantage competed to 0)
```

### Findings

**F-E2-6 — Relational depth is a strict total order. `[A]` within model.** The
2-player CH tournament matrix is exactly triangular: deeper wins, always; equal
depth ties; the payoff depends only on the **sign of the depth difference**, not
on absolute depth. F-E2-4's "one step deeper than the other" is the *minimal*
winning move (`argmax = k_B+1`), but any greater depth wins too. This is the
sharpest possible form of reflexive, positional empowerment — and it is precisely
the structure single-agent reach (R6) cannot express, because it has no "other"
to be relative to.

**F-E2-7 — The product form and the zero-factor reproduce a third time. `[A]`
within model.** Against the depth-mixed population the surface is
complementary/multiplicative (CES ρ̂ = +0.25; Cobb-Douglas beats additive), and at
full tremble (`ε = 1`) the value of *every* depth collapses to the naive baseline
**exactly** (`k`-lift = 0.000000). Plan × execution, existentially conjunctive,
once more. R10a is now robust across three independent game families: memory-1 PD
(V1), depth-graded automata (V2), and p-beauty mutual modeling (V3).

**F-E2-8 — Still no conserved product — and mutual modeling cannot supply one.
`[A]` within model; the decisive half.** A conserved `φ·ν = const` law requires
the system to **select an interior point on a hyperbola** — a conjugate trade
where more depth buys less reliability at equal value. V3 refuses this on every
leg: the optimal-depth ridge is **flat at the maximum** (slope 0; a hyperbola
fits with R² < 0), the budget optima are **all corners** (interior fraction 0.00
— every marginal unit is spent pushing depth *up*, never trading it), and the
reflexive dynamics **ratchet to the boundary** (L3) rather than to an interior
fixed point. The mechanism is **new** relative to V2: V2 had no conserved product
because depth *saturated* (deeper was worthless); V3 has none because depth is a
**positional good in an arms race** (deeper is always worth more, so both run to
the wall — the Nash floor where all guesses → 0 — and **the advantage cancels**).
What is conserved at the reflexive equilibrium is not `φ·ν`; it is the **zero-sum
cancellation** of a purely relative advantage. That is the ZSRE register, not the
sphere.

### Scoring the registered predictions (the discipline, again)

| Prediction | Outcome |
|---|---|
| P-V3a relational depth (interior best-reply, rises in `k_B`, diagonal ties) | **RIGHT, and stronger** — a strict total order, not merely a single-peaked best-reply. |
| P-V3b "single-peaked in `k`, ρ̂ > 0.3, no conserved product" | **SPLIT** — the *no-conserved-product* conclusion is **RIGHT** (flat-at-max ridge, corner budgets), but the *mechanism* is **WRONG**: depth does not peak/saturate, it strictly dominates (peak at `k_max`), and ρ̂ = +0.25 is *more* multiplicative than predicted. My deflationary "interior peak" bias **under-estimated relational depth**. Recorded as missed. |
| P-V3c reflexive ratchet, no interior fixed point, advantage → 0 | **RIGHT** — orbit 0→1→…→6→6; `W(6,6) = 0.50`. |
| KILL/UPGRADE (hyperbolic ridge + interior budget + ρ̂ ≤ 0 ⇒ upgrade R10b) | **Did not fire** — ridge anti-hyperbolic, budget corners. R10b stays `[C]`. |

P-V3b's mechanism joins V1-P1 and V2-P-V2a in the "wrong, reported as wrong"
column — **three E2 misses, all in the same direction: the author under-rating
the reflexive register.** The pre-registration earns its keep precisely by
catching that bias.

### What this moves

- **R10b's depth-axis route is now closed.** The two natural ways depth could
  have supplied a conserved product — *saturation balanced against reliability*
  (V2) and *mutual modeling* (V3) — have both been run and both fail, for
  **opposite** reasons (worthless vs purely-positional). The conjugate
  conservation law `φ·ν = 1` does not live in the empowerment/teleology register
  at the agent scale. What survives across V1–V3 is **R10a**: the product *form*
  and its *catastrophe*, robust; never the *conservation*.
- **The Dyadic Coupling Law:** its reflexive-contact witness is now corroborated
  a **third** time across a third game family (the p-beauty strict total order +
  exact zero-factor), and its **boundary** is sharpened: at reflexive contact the
  coupling is multiplicative but **positional**, so it **dissipates at
  equilibrium** rather than conserving — exactly where the law hands off to the
  Zero-Sum Resolution register.
- **The honest scoreboard:** "mutual modeling might rescue the sphere" — §6's
  last live hope for R10b — is **retired**. It does not. The teleology thread's
  single positive formal result remains R10a (interaction), now scoped *triply*
  to the product form, never the conservation law.

### Limitations (V3's own)

1. CH-ladder guesses (`g_k = 50·p^k`) are the canonical homogeneous-population
   best-responses, not the exact 2-player nested-belief best-responses; the
   strict total order is a property of the ladder-vs-ladder comparison. A full
   nested-belief solver could soften the triangularity — it would **not** create
   a conserved product (the positional logic is robust to it).
2. "Execution = revert to the anchor" is one tremble model; a revert-to-uniform
   model would blunt the exact zero-factor at `ε = 1` into an approximate one
   (the *form* survives; the *exactness* is model-specific — as already noted for
   Game A vs B).
3. The arms race is bounded by `K_MAX = 6`; the unbounded game has the same logic
   (ratchet to the Nash floor, advantage → 0) without a terminal tie cell.
