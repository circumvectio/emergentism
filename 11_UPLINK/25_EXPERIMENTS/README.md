---
rosetta:
  primary_level: L3
  primary_column: Uplink Experiment Lane
  secondary:
    - level: L5
      column: Empirical Bridge Architecture
      role: "organize flagship-paper, preregistration, dataset, and study-design surfaces"
    - level: L4
      column: Execution Gate
      role: "separate routing from executed analysis"
    - level: L6
      column: Evidence Boundary
      role: "keep empirical synthesis from becoming empirical proof"
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[D/B/I]"
  canonical_phrase: "UPLINK EXPERIMENT LANE"
title: "UPLINK EXPERIMENT LANE"
status: "ACTIVE — empirical-bridge front door"
evidence_tier: "[D] for designs/preregistration; [B] only for dated data, reproducible analysis, or execution receipts; [I] for synthesis."
---

# UPLINK EXPERIMENT LANE

> Compressed empirical-bridge and study-design packet cluster.

**Rosetta boundary:** [I] This front door routes empirical bridge work. It does not [B] prove datasets, preregistration execution, reproducible analysis, or flagship-paper readiness without dated receipts.

## Files In This Lane

- `25_FLAGSHIP_PAPER_BRIEF.md`
- [`2026-07-02_extraction_law_empirical_test/`](2026-07-02_extraction_law_empirical_test/)
  — **RUN COMPLETE**; [`VERDICT.md`](2026-07-02_extraction_law_empirical_test/VERDICT.md)
  records "Product-only multiplicative proxy: NOT SUPPORTED in this dataset"
- [`2026-07-02_production_function_form/`](2026-07-02_production_function_form/)
  — **RUN COMPLETE**; [`VERDICT.md`](2026-07-02_production_function_form/VERDICT.md)
  records the symmetric product decisively rejected (all four kill criteria
  failed), and [`VERDICT_BALANCE.md`](2026-07-02_production_function_form/VERDICT_BALANCE.md)
  records the balance hump rejected with curvature of the opposite sign
- `../20_SCOPE/26_BEHAVIOR_IS_MULTIPLICATIVE_NOT_ADDITIVE_BRIEF.md`
- `../20_SCOPE/27_ULTIMATUM_GAME_STUDY_DESIGN.md`
- `../20_SCOPE/28_ULTIMATUM_DATASET_SELECTION_AND_VARIABLE_MAP.md`
- `../20_SCOPE/29_ULTIMATUM_PREREGISTRATION_SKELETON.md`

## Reproduce the two recorded runs

Run from the repository root. These commands replay local analyses; matching
their outputs establishes reproducibility of the code/data packet, not
independent replication or validation of the worldview.

```bash
(
  cd 11_UPLINK/25_EXPERIMENTS/2026-07-02_extraction_law_empirical_test
  python3 run_analysis.py
)
(
  cd 11_UPLINK/25_EXPERIMENTS/2026-07-02_production_function_form
  python3 run_prodfn.py
  python3 run_balance.py
)
```

## Use This Lane For

- bounded empirical bridge work
- flagship-paper routing
- prereg and dataset/study design surfaces
