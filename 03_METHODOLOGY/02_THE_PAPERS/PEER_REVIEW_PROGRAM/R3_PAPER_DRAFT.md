# Progressive Transfers Under Mortality: A Triage Inversion of the Pigou–Dalton Principle

**Yves R. Burri**

*Draft v1 — 2026-06-10. External register. Both experiments reported here were executed on 2026-06-10; numbers are actual output of the archived scripts (`R3_SUPPORT_TRANSFER_SIM.py`, `R3_SUPPORT_TRANSFER_SIM_V2.py`; stdlib Python, deterministic, 20 seeds each). All citations require verification before submission.*

---

## Abstract

The Pigou–Dalton principle — a mean-preserving transfer from a richer to a poorer agent raises any strictly concave social welfare sum — is a static result. We study its fate in a minimal dynamic population model with three ingredients standard welfare analysis omits: continuous downward drift of individual state, an absorbing mortality boundary, and (in a second experiment) threshold regeneration, where agents above a state threshold partially or fully self-restore. Welfare is the time-integral of a concave function of state over living agents. Three findings. (1) **Triage inversion:** with drift and mortality but no regeneration, repeated progressive transfers targeted at the worst-off agent *reduce* aggregate welfare-time by ≈11% relative to no transfers, even though every individual transfer satisfies Pigou–Dalton instantaneously — rescue parks population mass at low-welfare states while consuming high-welfare donor lifetime. Mid-distribution transfers, by contrast, retain a small Jensen gain. (2) **Denomination dependence:** whether transfers are denominated in the state variable or in welfare units reverses the ranking of giving versus taking policies; the choice of transfer currency, usually left implicit, is load-bearing. (3) **Threshold restoration of the principle:** with strong regeneration (a survival cliff), targeted progressive transfers dominate every alternative — 100% survival versus 77% under no transfers and a 26% welfare-time gain — while *random* transfers recover none of this value and regressive extraction becomes catastrophic. The collective value of redistribution under mortality is determined not by the instantaneous welfare gradient but by whether transfers change recipients' *dynamics* — crossing them over the regeneration threshold — a result that parallels the asset-threshold poverty-trap literature and yields a sharp design rule for transfer policies in any system with mortality and recovery thresholds. A robustness suite shows the triage inversion holds for every welfare function tested — concave, linear, and convex (deepening with convexity; the linear control proves the effect is trajectory-driven, since lifetime welfare under drift-to-absorption is convex in initial health) — and at all transfer volumes; but it is *objective-relative*: under Rawlsian maximin the ranking reverses (needs-targeted giving maximizes the worst-off's lifetime welfare by an order of magnitude while minimizing the aggregate), and under per-capita averaging the extraction policy "wins" by culling the depleted. The choice of social objective under mortality is itself morally load-bearing, and we quantify how.

**Keywords:** Pigou–Dalton transfer principle; redistribution; mortality; poverty traps; agent-based simulation; majorization

## 1. Introduction

Dalton (1920), building on Pigou (1912), introduced the transfer principle that still anchors the measurement of inequality: a transfer from richer to poorer that preserves the mean and does not reverse ranks should not decrease social welfare. Under any strictly concave utilitarian welfare function the conclusion is immediate — it is Jensen's inequality, equivalently Schur-concavity under majorization (Marshall, Olkin & Arnold; Atkinson 1970). The principle is static: it compares two wealth vectors at an instant.

Real transfer systems operate on populations whose members are *moving* — depleting, dying, sometimes recovering. We ask the simplest version of the dynamic question: if a population drifts toward an absorbing boundary (death, exit, bankruptcy, burnout), and welfare is accumulated over time by the living, do repeated Pigou–Dalton transfers still raise aggregate welfare?

The answer, in the minimal model below, is no — and the way it fails, and the single ingredient that restores it, are both instructive.

## 2. Model

Agents i = 1…100 carry a state θᵢ ∈ [π/2, π); instantaneous welfare is B(θ) = sin θ, so B is strictly concave, maximal (B = 1) at θ = π/2 and vanishing at the absorbing boundary. Each step every living agent drifts toward the boundary, θᵢ ← θᵢ + δ (δ = 0.004); absorption (death) occurs at θ ≥ π − 0.02. Aggregate welfare is W = Σₜ Σ_{living} B(θᵢ(t)), the *welfare-time integral*. Initial states are uniform on [0.55π, 0.92π]; horizon T = 600; 20 seeds; K = 10 transfers per step.

The specific sinusoidal form arises naturally when the state respects a conjugate-product constraint (two factors with φ·ν = 1, θ the angular coordinate), but nothing below depends on it beyond concavity; we flag this as a robustness check (§6).

**Policies.** GIVE: the highest-B living agent pays, the lowest-B living agent receives. TAKE: the lowest-B agent is debited, the highest-B credited. RANDOM: a random living pair. NONE: drift only. **Currencies.** ANGLE: transfers move a fixed quantum of state (Δθ = 0.02; total θ conserved per transfer). BALANCE: transfers move a fixed quantum of welfare (ΔB = 0.01; total B conserved per transfer).

**Static check.** A single ANGLE-denominated GIVE transfer (donor near the equator, recipient near the pole) raises ΣB by +0.018 with Σθ exactly conserved — Pigou–Dalton verbatim, since equalizing a conserved state under concave B is Schur-concavity. A BALANCE-denominated transfer is ΣB-neutral by construction. The static principle holds in the model wherever it should.

## 3. Experiment 1 — drift and mortality, no recovery

| Policy | Currency | Welfare-time W (±sd) | Mean lifespan | Survivors at T |
|---|---|---|---|---|
| NONE | — | 9213 ± 788 | 204.4 | 0.0 |
| GIVE | angle | 8200 ± 800 | 204.4 | 0.0 |
| RANDOM | angle | 9590 ± 829 | 205.3 | 0.6 |
| TAKE | angle | 6931 ± 610 | 101.7 | 0.6 |
| GIVE | balance | 7380 ± 711 | 192.3 | 0.0 |
| RANDOM | balance | 9473 ± 869 | 206.4 | 0.1 |
| TAKE | balance | 8389 ± 723 | 138.4 | 1.0 |

**Finding 1 (triage inversion).** GIVE-to-the-poorest underperforms NONE by ≈11% (8200 vs 9213) under the state-denominated currency, although each individual transfer raises ΣB. Mechanism: repeatedly pulling the most-depleted agent off the boundary holds population mass at low-B states, paid for with high-B donor lifetime; the per-transfer Jensen gain (+0.018) is an order of magnitude too small to offset the trajectory reallocation. Note that mean lifespan is *unchanged* (204.4): state-conserving transfers conserve total life and reallocate it across welfare levels — toward the bottom, where it accumulates little W.

**Finding 2 (mid-distribution transfers gain modestly — but see §6).** RANDOM beats NONE modestly (9590 vs 9213). Our initial reading attributed this to the Jensen gain of equalization among the still-viable; the robustness suite (§6) corrects it: the gain persists unchanged under *linear* welfare, where no concavity effect exists, identifying the true mechanism as payment-clipping at the absorbing boundary (near-dead donors pay less than recipients receive). The qualitative triage lesson survives — the dynamically optimal recipient has remaining runway, not maximal need — but the quantitative RANDOM advantage is largely a boundary artifact, and we report it as such.

**Finding 3 (denomination dependence).** Under welfare-denominated transfers the giving/taking ranking partially inverts (TAKE 8389 > GIVE 7380): near the top a unit of B costs enormous state, near the boundary almost none, so B-for-B exchange bleeds donors dry to deliver trickles. Whether "progressive transfers help" is well-posed only after the transfer currency is fixed — an assumption the static literature never needs and dynamic applications cannot avoid.

**Finding 4 (extraction is robustly worst).** TAKE loses on every metric in both currencies, halving mean lifespan; under BALANCE it leaves a single survivor at horizon — the extractor parked at maximal welfare while its sources died. The asymmetry between redistribution and extraction survives even where naive redistribution fails.

## 4. Experiment 2 — threshold regeneration

We add one rule, registered as a directional conjecture before execution: agents with B above a threshold B_reg = 0.5 climb toward the equator at rate r; below it they only drift. Two regimes: **weak** (r = 0.002 < δ: everyone still descends, the top at half speed) and **strong** (r = 0.006 > δ: the threshold is a survival cliff — above it agents net-recover, below it they sink). A new policy **TRIAGE** targets the highest-B agent *below* the threshold (the cheapest possible dynamics conversion). Angle currency throughout.

| Regime | Policy | Welfare-time W (±sd) | Mean lifespan | Survivors at T |
|---|---|---|---|---|
| weak | NONE | 15464 ± 1518 | 291.7 | 0.0 |
| weak | GIVE | 12355 ± 2151 | 271.2 | 0.0 |
| weak | TRIAGE | 13012 ± 1676 | 281.3 | 0.0 |
| weak | RANDOM | 16154 ± 1567 | 289.4 | 5.9 |
| weak | TAKE | 9354 ± 908 | 122.4 | 1.0 |
| strong | NONE | 44389 ± 2830 | 480.6 | 76.5 |
| strong | GIVE | 56016 ± 1096 | **600.0 ± 0.0** | **100.0** |
| strong | TRIAGE | 56551 ± 678 | **600.0 ± 0.0** | **100.0** |
| strong | RANDOM | 44000 ± 3001 | 478.9 | 76.1 |
| strong | TAKE | 24341 ± 2387 | 257.8 | 32.4 |

**Finding 5 (threshold restoration).** In the strong regime, targeted progressive transfers dominate everything: +26–27% welfare-time over NONE and *zero deaths across all 20 seeds* (lifespan 600.0 ± 0.0), versus 23.5 deaths per run under NONE. Transfers convert doomed agents into self-sustaining ones; once across the cliff, recipients never need help again. GIVE-to-the-poorest and TRIAGE perform nearly identically here (at this transfer rate even the deepest agents get dragged across), with TRIAGE cheaper in variance.

**Finding 6 (targeting is the binding constraint).** RANDOM ≈ NONE in the strong regime (44000 vs 44389): with the same total transfer volume, untargeted redistribution rescues essentially no one. The entire value of the transfer system is created by *selection* of recipients relative to the threshold. And TAKE becomes catastrophic (32.4 vs 76.5 survivors): extraction now drags otherwise-viable agents below the cliff — it destroys not just welfare but the recovery capacity itself.

**Finding 7 (the weak regime still inverts).** Where regeneration exists but cannot outrun decline, rescue remains collectively negative (GIVE 12355, TRIAGE 13012 < NONE 15464). Slowing doom is not changing it; the inversion of Experiment 1 persists under partial dynamics-change.

The registered conjecture — *transfers beat non-transfers exactly when they change recipients' dynamics rather than merely their position* — is confirmed and sharpened: the change must be regime-crossing (across the cliff), and it must be targeted.

## 5. Relation to existing literature

The static engine is classical (Pigou 1912; Dalton 1920; Atkinson 1970; majorization: Marshall & Olkin). The strong-regime result is a minimal-model reproduction of the asset-threshold **poverty trap** logic: transfers large enough to cross a productive-asset threshold change households' dynamics persistently, while transfers below the threshold dissipate — consistent with the "big push" graduation-program evidence (verify and cite: Bandiera et al. 2017; Balboni, Bandiera, Burgess, Ghatak & Heil, "Why Do People Stay Poor," QJE 2022; Barrett & Carter on poverty-trap mechanisms; Kraay & McKenzie 2014 for the skeptical view). Our contribution is not the policy result but its *derivation floor*: drift + absorption + concavity + threshold recovery suffice — no production function, no credit market, no behavioral assumptions — and the same four ingredients also generate the triage inversion and the denomination dependence, which the static principle conceals. We have not found a treatment of Pigou–Dalton under absorbing mortality with the welfare-time objective; we flag this as a literature-search obligation before submission rather than a novelty claim.

## 6. Robustness experiments

A third experiment battery (12 seeds; welfare defined on normalized health s ∈ (0,1], so alternative functional forms are comparable) addressed the natural referee questions.

**6.1 Concavity.** The inversion is not a property of sin. GIVE/NONE welfare-time ratios: sin 0.881, √s 0.933, log(1+9s) 0.930, linear 0.852, s² 0.695. Two lessons. The *linear control* is diagnostic: with welfare linear in health, instantaneous transfers are welfare-neutral, yet the inversion persists at full strength — because under constant drift to absorption an agent's lifetime welfare is convex in initial health (≈ s₀²/2 per unit drift), so equalizing health lowers the population total regardless of instantaneous curvature. The inversion is a *trajectory* fact. Second, the dose-response is orderly: stronger concavity near zero (√, log) partially offsets the trajectory penalty; convexity deepens it.

**6.2 Boundary artifact identified.** RANDOM's modest advantage over NONE persists unchanged under linear welfare (ratio 1.044) — impossible for a concavity effect. The mechanism is payment-clipping at the absorbing wall: a transfer debiting a near-dead donor is truncated at the boundary while the recipient is credited in full, a small systematic creation of state that grows with transfer volume (RANDOM rises from 8877 to 9829 as volume goes from 0.1× to 1.5× of drift). We flag this as a general modeling hazard: *transfer schemes interacting with absorbing boundaries can manufacture apparent welfare gains that are artifacts of truncation accounting.*

**6.3 Volume.** GIVE-to-poorest is not rescued by scale: its welfare-time is flat (7760–7824) across transfer volumes from 0.1× to 1.5× of total drift, as the conservation argument predicts — state-denominated transfers cannot change total descent, only its distribution.

**6.4 The objective is morally load-bearing.** Under four objectives computed on identical runs (sum welfare-time; discounted at γ = 0.995; Rawlsian minimum lifetime welfare; mean per-living-capita welfare):

| Policy | W (sum) | W discounted | Rawls min | Per-capita | Mean lifespan |
|---|---|---|---|---|---|
| NONE | 8812 | 5916 | 6.8 | 0.336 | 202.2 |
| GIVE | 7760 | 5634 | **65.5** | 0.369 | 202.2 |
| RANDOM | 9191 | 5999 | 6.1 | 0.380 | 203.0 |
| TAKE | 6730 | 4825 | 0.0 | **0.644** | 100.3 |

Discounting preserves the sum ranking. But under **maximin**, the verdict on needs-targeted giving *reverses*: GIVE raises the worst-off's lifetime welfare tenfold (65.5 vs 6.8) at unchanged total lifespan — the triage inversion is a fact about aggregate objectives, and a Rawlsian evaluator should choose exactly the policy the utilitarian one rejects. And under **per-capita averaging**, the extraction policy dominates everything (0.644 vs 0.336–0.380) by the simplest possible mechanism: killing the depleted raises the average of the living. Mean-of-survivors metrics under mortality are survivorship bias as a policy instrument; any evaluation system scoring per-capita welfare without a mortality penalty will select for extraction.

## 7. Limitations

(i) Constant drift and a single threshold are the simplest dynamics; heterogeneous drift and stochastic shocks are the natural next layer. (ii) The regeneration experiment used one threshold value and two rates; a fuller sweep of the cliff geometry is future work. (iii) These are model-internal facts. The poverty-trap parallel is an echo, not a test; no claim about real transfer programs follows without empirical bridging.

## 8. Conclusion

Under mortality, the static transfer principle is not a safe guide to dynamic policy: progressive transfers targeted by need alone can reduce aggregate welfare-time (triage inversion), the implicit choice of transfer denomination can reverse rankings, and the entire collective value of redistribution can hinge on whether transfers cross recipients over a recovery threshold — in which case targeted giving dominates and extraction is doubly destructive. One sentence version: *in dying populations, give to change dynamics, not to soothe gradients — and declare your objective, because maximin blesses exactly the giving that the sum condemns, and per-capita metrics bless the extraction that kills.*

## References (ALL TO BE VERIFIED — drafted from memory)

- Atkinson, A. B. (1970). On the measurement of inequality. *Journal of Economic Theory* 2(3): 244–263.
- Balboni, C., Bandiera, O., Burgess, R., Ghatak, M., & Heil, A. (2022). Why do people stay poor? *Quarterly Journal of Economics* 137(2). [Verify pages.]
- Bandiera, O., et al. (2017). Labor markets and poverty in village economies. *Quarterly Journal of Economics* 132(2). [Verify.]
- Barrett, C. B., & Carter, M. R. — poverty traps review. [Locate exact survey, e.g., *Journal of Development Studies* 2013 or Handbook chapter.]
- Dalton, H. (1920). The measurement of the inequality of incomes. *Economic Journal* 30(119): 348–361.
- Kraay, A., & McKenzie, D. (2014). Do poverty traps exist? *Journal of Economic Perspectives* 28(3): 127–148.
- Marshall, A. W., Olkin, I., & Arnold, B. C. (2011). *Inequalities: Theory of Majorization and Its Applications*, 2nd ed. Springer.
- Pigou, A. C. (1912). *Wealth and Welfare*. Macmillan.

*Venue ladder: arXiv (physics.soc-ph / econ.TH) preprint → JASSS or* Adaptive Behavior*; an economics-facing rewrite could target a development-economics theory venue if the literature search confirms the gap.*
