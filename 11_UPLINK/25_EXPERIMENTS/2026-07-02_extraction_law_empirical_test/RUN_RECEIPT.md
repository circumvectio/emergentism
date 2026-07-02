---
title: "Run Receipt - Extraction Law Empirical Test"
date: 2026-07-02
status: "RUN COMPLETE"
evidence_tier: "[B] command-run receipt; [D] interpretation"
owner: "K2-staged; not signed"
---

# Run Receipt

## Command

```bash
cd /Users/Yves/Documents/01_EMERGENTISM/11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test
python3 run_analysis.py
```

## Output

```json
{
  "best_model_by_log_loss": "payoff_plus_fairness",
  "bounded_extraction_law_proxy": "BOUNDED_SUPPORT",
  "multiplicative_single_score_proxy": "PRODUCT_ONLY_NOT_SUPPORTED"
}
```

The command wrote:

- `results.json`

## Raw Checksums

| File | Expected MD5 | Actual MD5 | Result |
|---|---:|---:|---|
| `data.tsv` | `e0564d3b0f49a97592a3823cd9cd2803` | `e0564d3b0f49a97592a3823cd9cd2803` | pass |
| `prefs.annotated.csv` | `3056166bf0f30278127b54b008865a32` | `3056166bf0f30278127b54b008865a32` | pass |

## Dataset Shape

- Annotated games: 93
- Accepted: 70
- Rejected: 23

## Reproducibility

The run is deterministic under:

- Python 3 local environment
- `pandas`
- `numpy`
- `scikit-learn`
- Seed `20260702`
- Repeated stratified 5-fold cross-validation, 50 repeats

This receipt verifies a local reproducible analysis, not a K2-signed doctrine update.

