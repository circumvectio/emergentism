---
title: "Extraction Law Empirical Test"
date: 2026-07-02
status: "RUN COMPLETE"
evidence_tier: "[B] reproducible local analysis; [D] interpretation"
owner: "01_EMERGENTISM — historical experiment packet"
---

# Extraction Law Empirical Test

This packet runs one bounded empirical test instead of adding more canon.

It tests whether ultimatum-game acceptance behavior is explained by material payoff alone, or whether a fairness/coherence proxy improves out-of-sample prediction.

## Source

- Dataset: Giovanni Luca Ciampaglia, "Data for 'Power and Fairness in a Generalized Ultimatum Game'", figshare, 2014.
- DOI: <https://doi.org/10.6084/m9.figshare.1021603.v1>
- Related article: Ciampaglia, Lozano, Helbing, "Power and Fairness in a Generalized Ultimatum Game", PLOS ONE, 2014. <https://doi.org/10.1371/journal.pone.0099039>
- License: CC BY 4.0.

## Files

- `IMPLEMENTATION_PLAN.md` - bounded plan and kill criteria.
- `data/` - raw source files and checksum notes.
- `run_analysis.py` - deterministic analysis script.
- `results.json` - machine-readable output from the script.
- `VERDICT.md` - human verdict.
- `RUN_RECEIPT.md` - receipt for the exact run.

## Run

```bash
cd /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test
python3 run_analysis.py
```

Expected verdict from the committed run:

```json
{
  "best_model_by_log_loss": "payoff_plus_fairness",
  "bounded_extraction_law_proxy": "BOUNDED_SUPPORT",
  "multiplicative_single_score_proxy": "PRODUCT_ONLY_NOT_SUPPORTED"
}
```

## What Was Tested

Outcome:

- `accepted_binary = 1` when the annotated response is `Accepted`.

Material proxy:

- `responder_advantage_tasks = TRR - TRA`.
- Positive means accepting saves the responder work versus rejection.
- `material_score = (responder_advantage_tasks + 300) / 900`, clipped to 0..1.

Fairness/coherence proxy:

- `fairness_score = 1 - abs(TPA - TRA) / 300`, clipped to 0..1.
- `1` means equal accepted workload between proposer and responder.

Product proxy:

- `product_score = material_score * fairness_score`.

## Bottom Line

The bounded extraction/coherence proxy survives this dataset: fairness-aware models beat material payoff alone on held-out log loss and AUC.

The stronger product-only scalar does **not** survive this dataset: `material_score * fairness_score` alone performs essentially the same as payoff-only and is not the best model.
