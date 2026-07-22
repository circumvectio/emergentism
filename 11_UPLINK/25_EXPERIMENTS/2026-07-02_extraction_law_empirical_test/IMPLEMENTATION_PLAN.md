---
title: "Implementation Plan - Extraction Law Empirical Test"
date: 2026-07-02
status: "HISTORICAL PLAN — executed 2026-07-02"
evidence_tier: "[D] plan; outputs may become [B] only for reproducible analysis execution"
owner: "01_EMERGENTISM — historical experiment packet"
---

# Implementation Plan - Extraction Law Empirical Test

## Goal

Run one bounded empirical test against a public ultimatum-game dataset, then write a verdict that can support, weaken, or kill the local proxy claim without re-deriving doctrine.

This packet does **not** prove the full Extraction Law. It tests whether a simple material-payoff model is outperformed by models that include fairness/coherence gates in an ultimatum-game acceptance domain.

## Source Dataset

- Dataset: Giovanni Luca Ciampaglia, "Data for 'Power and Fairness in a Generalized Ultimatum Game'", figshare, 2014.
- DOI: https://doi.org/10.6084/m9.figshare.1021603.v1
- API: https://api.figshare.com/v2/articles/1021603
- Raw file: `data.tsv`, MD5 `e0564d3b0f49a97592a3823cd9cd2803`
- Secondary file: `prefs.annotated.csv`, MD5 `3056166bf0f30278127b54b008865a32`

## Bounded Claim

In this domain, acceptance behavior should not be explained by material payoff alone. A fairness/coherence proxy, alone or interacting with payoff, should improve out-of-sample prediction.

## Kill Criteria

The bounded proxy claim fails in this dataset if:

1. A payoff-only model matches or beats the fairness/coherence and interaction models on held-out log loss and AUC.
2. The apparent improvement depends on arbitrary preprocessing choices that cannot be stated and reproduced.
3. The dataset does not expose enough columns to reconstruct offer, payoff, and accept/reject outcomes.
4. The script cannot reproduce the published packet outputs from local raw data.

## Tasks

1. Create the packet scaffold under `11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test/`.
2. Download raw figshare files into `data/` and verify their MD5 hashes.
3. Inspect the dataset columns and encode a transparent variable map.
4. Implement `run_analysis.py` with deterministic preprocessing and cross-validated model comparison.
5. Write machine-readable `results.json`.
6. Write `README.md`, `RUN_RECEIPT.md`, and `VERDICT.md` from the actual results.
7. Run the script from a clean command line and verify the packet can be reproduced.
8. Commit only this packet on the `codex/extraction-law-empirical-test` branch.

## Expected Model Ladder

The final script should choose the strongest feasible ladder supported by the actual columns:

1. Payoff-only baseline.
2. Fairness/coherence-only model.
3. Additive model.
4. Multiplicative proxy model.
5. Full interaction benchmark.

Primary metrics: held-out log loss, AUC, and accuracy with fixed-seed stratified cross-validation when the outcome is binary.

## Non-Goals

- Do not rewrite canon.
- Do not claim the framework is proven.
- Do not alter any external application tree.
- Do not promote any document above its evidence tier.
- Do not stage or commit the unrelated untracked doctrine drafts already present in `01_EMERGENTISM`.
