---
title: "Verdict — Pooled GFS: multiplicative (φ×ν) vs additive (φ+ν) flourishing"
date: 2026-07-02
status: "VERDICT ISSUED — STAGED for K2, not signed"
evidence_tier: "[B] reproducible re-pooling of on-disk per-country fits; [I] interpretation"
provenance: "Executes test #1 of the Seven-Operator K2 packet (101_...), the pooled analysis deferred by Wave-1 (00_GFS_WAVE1_RESULTS.md Next Steps #1). Ran run_pooled.py over 09_TOOLS/04_DATA_PIPELINES/gfs_results_20260409.csv."
---

# Verdict — The Multiplicative Wager, Pooled

## Result

**The framework-consistent multiplicative structure (`flourishing = φ × ν`, positive interaction) is NOT supported in the pooled test. Kill-criterion FAILED.**

The audit's kill-criterion asked for a framework-consistent multiplicative win in **≥ 15/23** countries. Observed: **8/23 (35%)**. The pooled (n-weighted) interaction coefficient is **negative** (β = −0.134) — the average direction across the corpus points *against* the framework, not for it.

> ## ⚠ Post-verdict correction — operationalization (2026-07-02, appended per K3)
>
> **This test used the *well-being* reading of φ/ν, not the *agency* reading — and that materially narrows the verdict.** GFS mapped **φ → meaning/coherence** survey items, **ν → financial/health** items, outcome → **self-reported life-satisfaction**. But the framework's canonical agency gloss (D5 Register, 2026-06-12) defines **φ = worldline-foresight / knowing-how** and **ν = means-at-the-boundary (body, tool, energy, access, execution)**, with the outcome being **action-capacity / task output** — *"knowing how to fell a tree = φ; having and swinging the axe = ν; a chainsaw is higher ν but demands more φ; knowledge with no axe = φ×0 = 0."* Life-satisfaction × money is simply **not** foresight × means-to-act.
>
> **Therefore this result does NOT falsify the agency-register φ×ν.** What it decisively kills is the *survey-operationalized well-being* wager (and that reading was arguably never the right test). Revised status of the agency claim: **untested by any instrument that exists** — not confirmed, not refuted.
>
> **Two disciplines this correction forces, or the claim becomes unfalsifiable:**
> 1. **Pin one operationalization + one pre-registered kill.** This is now the 3rd φ/ν reading (well-being, agency, sphere-coordinate); a claim that relocates its own definition each time a test bites is unfalsifiable, which is *worse* than "failed one test." Wave-1's instrument caveat and audit claim #94 already flagged this escape hatch.
> 2. **The axe example strains the *product itself*.** "The chainsaw needs more φ to operate" means φ **gates** usable ν — a **threshold/min** structure (`≈ min(φ, capacity(ν))`), not two independent multiplicands. The zero-factor catastrophe (need both) only proves **conjunction**, which `min(φ,ν)`, Cobb-Douglas `φ^a·ν^b`, *and* the product `φ·ν` all satisfy. It does **not** single out the product the `B = sin θ` / L4-apex superstructure requires.
>
> **Right test (superseding this one for the agency claim):** a **production-function comparison** on real skill×tool→output data — fit *additive* vs *Leontief min* vs *Cobb-Douglas φ^a ν^b* vs *CES* vs *pure product φ·ν*, cross-validated. See sibling experiment `2026-07-02_production_function_form/`. Economics has fit these for a century; the pure product rarely wins outright, so this is a real, killable test — not a defense.

## Numbers (reproducible from `run_pooled.py`)

23 countries · **128,868** respondents.

| Test | Result | Reading |
|---|---:|---|
| Interaction term improves AIC (any sign) | **20/23** | trivially true — an extra parameter + large n; **direction-blind, not evidence for the φ×ν ontology** |
| **Framework-consistent** (improves AIC **and** β > 0) | **8/23 (35%)** | the *real* claim — **FAILS** the ≥15/23 kill |
| Significant interactions (p<0.05) | 8/23 | of which **4 positive / 4 negative** — a coin flip on sign |
| n-weighted mean interaction β | **−0.134** | pooled direction is anti-framework (prior random-effects meta on disk: β=−0.053, p=0.60, I²=75.8%) |
| Pooled ΣAIC: additive vs multiplicative | m2 better by 1,186 | again the direction-blind "a term helps fit" effect only |

## What this kills

- **"Flourishing follows a multiplicative φ×ν structure across human populations."** Not supported: framework-consistent in only 8/23, pooled β negative, significant effects split 50/50 in sign. Where the interaction is strong and significant it is **as often the wrong sign** (high-φ + high-ν together predicting *less* flourishing).
- The teleological bridge (geometry → value via multiplicative flourishing) does **not** earn the `[I] → [B]` upgrade it was staked on. It stays `[I]`, and is now empirically strained, not merely unproven.

## What survives / what this does NOT kill

- A generic **interaction between the proxies exists** (20/23 improve fit) — but the framework cannot claim it, because the sign is null-to-negative on average. "There is *some* non-additivity" is true and weak; "it is the framework's positive φ×ν" is not.
- **The abstract identity `φ·ν = 1` on S² is untouched** — but only because (per the seven-operator audit, claim #39/#87) it is a *definitional tautology* (`cot·tan ≡ 1`), not an empirical claim this test could reach.
- **Instrument-validity caveat stands** (Wave-1 §"Instrument Validity", VanderWeele GFS not designed for this): survey proxies may not capture theoretical φ/ν. This cuts **both ways** — it blocks a clean *kill* of the ontology as much as a clean *confirmation*. What died is the **survey-operationalized** wager, decisively; the abstract wager retreats to "untested by any instrument that exists."

## Data-integrity finding (new)

The canonical Wave-1 doc headlines **n = 207,920**; the per-country fits it cites sum to **128,868**. The audit flagged this discrepancy (~79k, ~61% overstatement); this run **confirms** the analyzed n is 128,868. `00_GFS_WAVE1_RESULTS.md` should reconcile or correct its headline n. (Reconciliation at the microdata level needs the raw file, not on disk — that stays open.)

## Honest limit

This is a **re-pooling of existing per-country fits**, not a fresh fit on raw microdata. It executes the pooled comparison Wave-1 deferred and issues the direction-aware verdict Wave-1's own "mixed" framing softened. It does not resolve proxy validity, and it cannot test the first-person (Pratyaksha) claim, which is unfalsifiable by construction.

## Bottom line

Run to a pooled verdict, the framework's central empirical wager **loses on the direction that matters**. Per the seven-operator audit's own closing: the framework should retreat, honestly, from "the geometry is the territory of human flourishing" to **"a correctly-tiered coordinate geometry with an unproven — and now empirically strained — moral overlay."** That retreat is not a defeat; it is the A7 the framework says it lives by, finally paid in data instead of coherence.

*— Staged for K2. Sign, hold, or return. Nothing here is canon until you sign it.*
