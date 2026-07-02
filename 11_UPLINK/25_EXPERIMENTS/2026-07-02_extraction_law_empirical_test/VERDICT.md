---
title: "Verdict - Extraction Law Empirical Test"
date: 2026-07-02
status: "VERDICT ISSUED"
evidence_tier: "[B] reproducible local result; [D] theoretical interpretation"
owner: "K2-staged; not signed"
---

# Verdict

## Result

**Bounded extraction/coherence proxy: SUPPORTED in this dataset only.**

**Product-only multiplicative proxy: NOT SUPPORTED in this dataset.**

The best held-out model was `payoff_plus_fairness`, not `payoff_only` and not `multiplicative_proxy`.

## Metrics

Repeated 5-fold stratified cross-validation, 50 repeats, seed `20260702`, `n = 93` annotated games:

| Model | Log loss | AUC | Accuracy | Delta vs payoff-only | Log-loss win rate vs payoff-only |
|---|---:|---:|---:|---:|---:|
| `payoff_plus_fairness` | 0.513350 | 0.688671 | 0.780129 | +0.033200 | 0.760 |
| `fairness_only` | 0.514167 | 0.692171 | 0.775684 | +0.032384 | 0.700 |
| `interaction_full` | 0.516260 | 0.683800 | 0.779906 | +0.030291 | 0.748 |
| `multiplicative_proxy` | 0.546540 | 0.602614 | 0.752456 | +0.000011 | 0.468 |
| `payoff_only` | 0.546551 | 0.636243 | 0.770199 | 0.000000 | 0.000 |

Lower log loss is better. Higher AUC, accuracy, and win rate are better.

## Interpretation

This result rejects the simplest material-payoff-only reading in this ultimatum-game domain. Acceptance is better predicted when fairness/coherence is included.

It also rejects a stronger overcompressed reading: the single product score `material_score * fairness_score` is not enough here. The better empirical shape is a fairness gate or additive fairness-plus-payoff model, not a lone multiplicative scalar.

## What Dies

- "Extraction is always forbidden" remains wrong; this experiment does not test that moral absolutism.
- "Material payoff alone explains acceptance" fails here.
- "The product-only scalar is the best behavioral predictor" fails here.

## What Survives

- The bounded eta rewrite receives local support only: extraction/taking should be modeled with fairness/coherence and material gain, not material gain alone.
- The local proxy claim survives: a fairness/coherence variable adds predictive power over payoff-only.

## Limit

This is one small public dataset in a generalized ultimatum-game domain. It is evidence against payoff-only reduction and against product-only overcompression; it is not a proof of the full Extraction Law.
