## Summary

Read only the five named files. No edits made.

Surviving pilot claims are bounded, not canonical: fairness/coherence improves prediction over payoff-only in one ultimatum-game dataset; product-only `material * fairness` does not survive; extraction is not "forbidden," but must be measured by target, gate, boundary, time horizon, and long-run `Sigma-delta-P`.

## Test Backlog

| Test / Meter | What It Tests | Concrete Meter |
|---|---|---|
| Repeated Exchange Meter | Mutualism Limit: clean repeated exchange should lower coordination cost and preserve V gain | per-round verification time, contract length, dispute rate, repeat rate, V-surplus |
| Fairness Gate Replication | Fairness/coherence adds predictive power beyond material payoff | held-out log loss / Brier / AUC: `payoff_only` vs `payoff_plus_fairness` |
| Extraction Event Ledger | Ungated extraction creates later substrate cost | local V gain vs later churn, resistance, dispute, depletion, support burden |
| Gate Targeting Test | Gated taking differs from indiscriminate extraction | target class: cooperator / defector / non-kin / weak-node / substrate; compare long-run `Sigma-delta-P` |
| Trust Collapse Asymmetry | One `eta > 0` round should re-inflate Phi-spend faster than trust was built | recovery rounds, added checks, escalations, relationship termination |
| Titan Balance Residual | Composition law as an operational balance meter, not more theology | residual `abs(log|kappa| + log|sigma|)`; rising residual predicts drift/runaway |

## Dataset/Receipt Needed

Minimum useful receipt schema:

| Field | Needed For |
|---|---|
| `actor_id`, `counterparty_id`, `round_id` | repeated exchange tracking |
| `material_gain`, `material_loss`, `net_surplus` | V delta |
| `fairness_score` or gate score | bounded extraction proxy |
| `coordination_cost` | Phi-spend proxy |
| `verification_steps`, `contract_length`, `dispute_count` | trust/coherence meter |
| `target_class` | gated vs ungated extraction |
| `future_yield`, `repeat_rate`, `churn`, `remediation_cost` | long-run substrate effect |
| `receipt_hash`, `source_dataset`, `seed`, `model_spec` | reproducibility |

## Kill Criteria

- Fairness/gate proxy dies if it fails to improve held-out log loss or Brier over payoff-only across replicated datasets.
- Product-only stays dead unless `material_score * fairness_score` repeatedly beats additive/gated models out of sample.
- Mutualism Limit dies if sustained `eta = 0` exchange does not reduce coordination cost while preserving V-surplus.
- Extraction Law dynamic dies if ungated extraction from cooperators or substrate raises long-run `Sigma-delta-P` without resistance, depletion, dependency, or future cost.
- Gate reading dies if indiscriminate taking performs as well as gated/targeted taking over long horizons.

## Priority

1. Build the repeated-exchange receipt meter first. It adds direct V by reducing coordination cost and surfacing trust collapse early.
2. Replicate the fairness-gate model on 2-3 more public exchange datasets.
3. Start the extraction event ledger only where live decisions already happen.
4. Keep Titan residual as a lightweight dashboard check; do not spend pilot energy proving algebra already framed as within-model.

