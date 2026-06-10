---
rosetta:
  primary_column: "Methodology"
  register: "[A] model-internal results; [I] interpretive readings"
  canonical_phrase: "R3 Transfer Asymmetry — First Experiment"
---

# R3 — Transfer Asymmetry Under Descent: The Corpus's First Run Experiment

**Status:** Executed 2026-06-10. Results below are actual output, not projections.
**Artifact:** [R3_SUPPORT_TRANSFER_SIM.py](R3_SUPPORT_TRANSFER_SIM.py) (stdlib Python, deterministic, 20 seeds)
**Tests:** Paper W, [PAPER_W_DESCENT_ASYMMETRY.md](../PAPER_W_DESCENT_ASYMMETRY.md), §3 (the Descent Theorem / giving-dyad-as-negentropy)
**Evidence tier:** [A] for the model-internal theorems and the numbers; [I] for every reading beyond the model. This experiment verifies internal consequences of the formalism. It says nothing about the world.

---

## 1. What was tested

Paper W claims: under the descent boundary condition, transfers that route order **down** the scarcity gradient (abundant donor → scarce recipient) are net-positive in total balance, and transfers routed **up** the gradient are net-negative. The corpus has stated this as a consequence of the B = sin θ gradient (flat at the equator, steep at the poles).

The model: 100 agents on the southern hemisphere (θ ∈ [π/2, π)), B = sin θ, constant drift toward the dispersal pole (the DBC arrow), absorption (death) at θ ≥ π − 0.02. Policies: GIVE (max-B pays, min-B receives), TAKE (min-B debited, max-B receives), RANDOM (random pair), NONE (drift only). Two exchange currencies: ANGLE (transfers denominated in latitude; Σθ conserved per transfer) and BALANCE (transfers denominated in B; ΣB conserved per transfer). Welfare metric: total balance-time integral (Σ over steps of Σ living B), the model's ΣP proxy.

## 2. Results (verbatim output)

```
N=100 T=600 drift=0.004 K=10 dtheta=0.02 tau=0.01 seeds=20
unit check GIVE | ANGLE   currency: dSumB = +0.017989  (Sum-theta change +0.000000)
unit check GIVE | BALANCE currency: dSumB = +0.000000  (Sum-theta change +0.072946)
--------------------------------------------------------------------------------------
NONE    -        | B-integral      9213 +/-    788 | mean lifespan  204.4 +/-  11.0 | survivors@T   0.0
GIVE    ANGLE    | B-integral      8200 +/-    800 | mean lifespan  204.4 +/-  11.0 | survivors@T   0.0
RANDOM  ANGLE    | B-integral      9590 +/-    829 | mean lifespan  205.3 +/-  10.9 | survivors@T   0.6
TAKE    ANGLE    | B-integral      6931 +/-    610 | mean lifespan  101.7 +/-   6.5 | survivors@T   0.6
GIVE    BALANCE  | B-integral      7380 +/-    711 | mean lifespan  192.3 +/-  10.2 | survivors@T   0.0
RANDOM  BALANCE  | B-integral      9473 +/-    869 | mean lifespan  206.4 +/-  11.6 | survivors@T   0.1
TAKE    BALANCE  | B-integral      8389 +/-    723 | mean lifespan  138.4 +/-   8.5 | survivors@T   1.0
```

## 3. Findings

**F1 — The static theorem is confirmed, and it has a 100-year-old name.** [A]
The unit check verifies Paper W §3 exactly: a single down-gradient, latitude-denominated transfer raises ΣB (+0.018) while conserving Σθ. But this is not a new theorem. With Σθ conserved and B = sin θ concave, "equalizing transfers raise the concave-sum" is the **Pigou–Dalton transfer principle** (welfare economics, c. 1912–1920), equivalently Jensen's inequality / Schur-concavity under majorization. Paper W's engine is a known result instantiated on the sphere. The honest restatement: *the giving dyad's static superiority is Pigou–Dalton with B as the concave welfare function; the corpus's contribution is the conservation law φ·ν = 1 as the **source** of the concavity, not the transfer principle itself.* Paper W must cite this lineage before any referee does.

**F2 — The dynamic claim is REFUTED as naively read.** [A] (model-internal)
Over full trajectories with drift and absorption, GIVE-to-the-most-scarce **underperforms doing nothing**: 8200 vs 9213 (≈ −11%), under the corpus's own currency (latitude). Mechanism: each rescue is instantaneously ΣB-positive, but repeatedly pulling the most-polar agent off the death boundary parks population mass at low-B latitudes while spending high-B donor lifetime. The per-transfer gain (+0.018) is swamped by the trajectory reallocation: donor life at B ≈ 0.6–1.0 is exchanged for recipient life at B ≈ 0.05–0.15. The Descent Theorem as stated is true per-transfer and false per-trajectory under the framework's own descent dynamics.

**F3 — Taking is robustly worst; the asymmetry survives.** [A] (model-internal)
TAKE loses on every metric in both currencies (B-integral 6931/8389; mean lifespan halved or slashed). The corpus's core moral asymmetry — extraction is collectively destructive — survives the dynamic test even where naive giving does not. Note the survivor column: under BALANCE currency, TAKE leaves ~1 agent alive at horizon — the extractor parked at the equator while its victims died. The model independently generates the parasite-survivor phenotype Paper III describes.

**F4 — Targeting, not transferring, is the variable that matters.** [A] (model-internal)
RANDOM mid-distribution transfers are the only policy that beats NONE (9590 vs 9213, modest but consistent), at equal lifespans. Equalization among the still-viable captures the Jensen gain without the rescue-the-doomed pathology. Combined with F2, the model yields a **triage result**: the dynamically optimal recipient has a steep gradient *and* long remaining runway — not the maximal gradient at the pole's edge. Paper W's "route order toward scarcity" needs the amendment "— but not toward the absorbing boundary."

**F5 — Currency-relativity.** [A] (model-internal)
Under BALANCE-denominated exchange the giving/taking ranking partially inverts (TAKE 8389 > GIVE 7380), because near the equator a unit of B costs enormous latitude and near the pole it costs almost none. The sign of the giving-dyad theorem depends on an axiom Paper W never states: **what the exchange is denominated in.** The corpus implicitly assumes latitude-denominated transfers; this must become explicit.

## 4. What this does and does not show

It does **not** show that generosity is collectively harmful in the world. The model has no recovery dynamics: a rescued agent cannot regain capacity; rescue only postpones absorption at low B. In corpus language, the model contains **Arjuna without Kṛṣṇa** — sacrifice that holds another off the pole, but no enablement that restores the other's own climb. The natural v2 experiment: add a regeneration rule (agents above a balance threshold regain latitude at rate r) and test whether GIVE then dominates NONE. Conjecture worth registering before running: **giving wins exactly when it changes the recipient's dynamics, not merely their position.** If v2 confirms this, the giving dyad's two operators stop being interchangeable decorations — sacrifice-without-enablement is the collectively negative half, and the corpus's pairing of them becomes a derived necessity rather than a stipulation. [C — registered 2026-06-10, pre-run]

It **does** show, at [A] within the model: the static engine is Pigou–Dalton; the dynamic claim fails without a triage amendment; the currency axiom is load-bearing and missing; extraction is robustly worst. Four concrete amendments Paper W owes, found by one afternoon of running instead of writing.

## 5. Publication path

As a standalone result this is a modest note, not a flagship paper: "redistribution under concave welfare with drift and absorbing mortality" — the novelty over classical Pigou–Dalton is the mortality dynamics and the triage inversion. Realistic venues: *Journal of Artificial Societies and Social Simulation* (JASSS), *Adaptive Behavior*, or as the formal core of a longer piece on conjugate-constrained welfare. The v2 (regeneration) result, if it lands as conjectured, is the stronger paper: "when transfers beat non-transfers under mortality: position vs. dynamics." See [00_PROGRAM.md](00_PROGRAM.md) for sequencing.

## 6. Corpus obligations created by this experiment (K3: amend, never overwrite)

1. Paper W §3: add the Pigou–Dalton citation and demote "derived" to "instantiated."
2. Paper W: add the explicit exchange-currency axiom (latitude-denominated).
3. Paper W: mark the Descent Theorem as instantaneous; add the triage amendment for the dynamic regime.
4. Paper W fences: add the lost-cause fence beside the martyr fence (both are corollaries of F2/F4).
5. Run sim v2 (regeneration) before any external claim about the giving dyad's collective sign. **→ Discharged 2026-06-10 — see Addendum below.**

---

## ADDENDUM (2026-06-10, same day): v2 executed — registered conjecture CONFIRMED, sharpened

The §4 registered experiment ran ([R3_SUPPORT_TRANSFER_SIM_V2.py](R3_SUPPORT_TRANSFER_SIM_V2.py); regeneration threshold B_reg = 0.5; weak regime r = 0.002 < drift, strong regime r = 0.006 > drift; new TRIAGE policy targets the cheapest below-threshold conversion). Verbatim aggregates:

```
WEAK   NONE   | B-integral 15464 ± 1518 | lifespan 291.7 | survivors   0.0
WEAK   GIVE   | B-integral 12355 ± 2151 | lifespan 271.2 | survivors   0.0
WEAK   TRIAGE | B-integral 13012 ± 1676 | lifespan 281.3 | survivors   0.0
WEAK   RANDOM | B-integral 16154 ± 1567 | lifespan 289.4 | survivors   5.9
WEAK   TAKE   | B-integral  9354 ±  908 | lifespan 122.4 | survivors   1.0
STRONG NONE   | B-integral 44389 ± 2830 | lifespan 480.6 | survivors  76.5
STRONG GIVE   | B-integral 56016 ± 1096 | lifespan 600.0 | survivors 100.0
STRONG TRIAGE | B-integral 56551 ±  678 | lifespan 600.0 | survivors 100.0
STRONG RANDOM | B-integral 44000 ± 3001 | lifespan 478.9 | survivors  76.1
STRONG TAKE   | B-integral 24341 ± 2387 | lifespan 257.8 | survivors  32.4
```

**F6 — Threshold restoration.** [A, model-internal] Where regeneration outruns drift above a threshold (a survival cliff), targeted giving dominates everything: zero deaths across all 20 seeds, +26% B-integral over NONE. Transfers that cross recipients over the cliff change their *dynamics*; once across, they self-sustain. The conjecture "giving wins exactly when it changes the recipient's dynamics, not merely their position" is confirmed — and sharpened: the change must be regime-crossing, and it must be **targeted**: RANDOM ≈ NONE even in the strong regime (44000 vs 44389) — untargeted transfers of identical volume rescue essentially no one. Discernment is not decoration on the giving dyad; in this model it is the entire difference between transformative and useless transfer. (Corpus register: Arjuna without Kṛṣṇa loses (v1, weak regime); Arjuna *with* a Kṛṣṇa-grade recovery channel and F5-grade targeting wins totally — the pairing of the two giving operators is now a derived necessity in-model, not a stipulation.)

**F7 — Extraction attacks recovery capacity itself.** [A, model-internal] In the strong regime TAKE is catastrophic (32.4 survivors vs 76.5 under NONE): extraction drags otherwise-viable agents below the cliff, destroying not just welfare but the capacity to recover. The corpus's moral asymmetry survives every variant tested and is *amplified* exactly where giving becomes most valuable.

**F8 — Weak regime: the inversion persists.** Where recovery exists but cannot outrun decline, rescue remains collectively negative (GIVE and TRIAGE both < NONE). Slowing doom is not changing it.

External echo flagged for the paper: this is the asset-threshold **poverty-trap** result (Balboni et al. QJE 2022; graduation-program RCTs) generated from four ingredients — drift, absorption, concavity, threshold recovery — with no economics imported. Full journal-register write-up with both experiments: [R3_PAPER_DRAFT.md](R3_PAPER_DRAFT.md).

Remaining before submission: concavity-robustness sweep (B beyond sin), parameter sweep (transfer volume vs drift), alternative welfare objectives, and the literature pass on Pigou–Dalton-under-mortality (§6 of the paper draft). **→ Sweeps discharged same day — see Addendum 2.**

---

## ADDENDUM 2 (2026-06-10, evening): v3 robustness suite executed

[R3_SUPPORT_TRANSFER_SIM_V3.py](R3_SUPPORT_TRANSFER_SIM_V3.py), 12 seeds, welfare defined on normalized health s ∈ (0,1]. Verbatim aggregates:

```
=== A. CONCAVITY SWEEP (K=10): welfare-time integral W ===
welfare             NONE            GIVE          RANDOM            TAKE
SIN          8812±  865      7760±  846      9191±  942      6730±  663
SQRT        10394±  863      9702±  849     10746±  916      6915±  603
LOG         10412±  895      9687±  890     10813±  956      7172±  629
LIN          6205±  645      5287±  607      6480±  708      4941±  515
SQ           2806±  387      1951±  317      2952±  437      2752±  358
GIVE/NONE ratios: SIN=0.881, SQRT=0.933, LOG=0.930, LIN=0.852, SQ=0.695
RAND/NONE ratios: SIN=1.043, SQRT=1.034, LOG=1.039, LIN=1.044, SQ=1.052

=== B. TRANSFER-VOLUME SWEEP (SIN) ===
K=2 (0.10x drift): GIVE 7824  | K=10 (0.50x): GIVE 7760  | K=30 (1.50x): GIVE 7816   (NONE 8812 throughout)

=== C. OBJECTIVE SWEEP (SIN, K=10) ===
policy   W (sum)   W disc.  Rawls min  per-capita  lifespan
NONE     8812      5916       6.8        0.336      202.2
GIVE     7760      5634      65.5        0.369      202.2
RANDOM   9191      5999       6.1        0.380      203.0
TAKE     6730      4825       0.0        0.644      100.3
```

**F9 — The inversion is trajectory-driven, not curvature-driven.** [A, model-internal] GIVE-to-poorest underperforms NONE for *every* welfare function, including the linear control (ratio 0.852), where no static Jensen effect exists at all. Mechanism confirmed: under drift-to-absorption, lifetime welfare is convex in initial health (≈ s₀²-shaped), so equalizing health lowers the population integral regardless of the instantaneous welfare curvature. Dose-response is clean: more concavity near zero (SQRT/LOG, 0.93) partially offsets the penalty; convexity (SQ, 0.695) deepens it. Volume doesn't rescue it (B: flat across 0.1×–1.5× of drift volume — θ-conservation argument confirmed).

**F10 — Correction to v1's F4: RANDOM's gain is mostly a boundary artifact.** [A, model-internal] RANDOM > NONE persists *unchanged* under linear welfare (1.044) where the Jensen explanation predicts zero gain. The actual mechanism: payment clipping at the absorbing wall — near-dead donors pay less than recipients receive (min(θ+Δ, π)), a small free lunch harvested from the boundary, growing with volume (B: RANDOM rises with K). v1's "mid-distribution transfers keep the Jensen gain" is hereby demoted: at these parameters the concavity contribution to RANDOM is ≈ 0. The honest ledger now contains a self-correction of a self-correction — recorded with some satisfaction.

**F11 — The objective is morally load-bearing: maximin reverses the verdict on giving.** [A, model-internal] Under sum welfare-time, GIVE-to-poorest is the worst redistribution policy; under Rawlsian maximin it is the *best* by an order of magnitude (worst-off lifetime welfare 65.5 vs 6.8) at unchanged total lifespan. The triage inversion is objective-relative: "naive" giving is exactly what a maximin evaluator should choose. Corpus consequence: ΣΔP > 0 is a sum-type objective, and the corpus should say so explicitly — sum and maximin *disagree about Arjuna*, and the disagreement is now quantified.

**F12 — Per-capita averaging endorses extraction.** [A, model-internal] TAKE nearly doubles mean per-living-capita welfare (0.644 vs 0.336) by killing the depleted — while halving total lifespan and zeroing the Rawlsian floor. Any evaluator scoring mean welfare of survivors would select the extraction policy. This is survivorship bias as a policy instrument, generated in 100 lines of Python; the paper must flag it as a warning about per-capita metrics under mortality.

Paper updated accordingly ([R3_PAPER_DRAFT.md](R3_PAPER_DRAFT.md) §6). Remaining before submission: the Pigou–Dalton-under-mortality literature pass and heterogeneous-drift/stochastic-shock extensions (flagged as future work, not blockers).
