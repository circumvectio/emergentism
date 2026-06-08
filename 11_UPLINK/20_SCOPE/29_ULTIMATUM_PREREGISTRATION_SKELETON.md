---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Ultimatum Preregistration Skeleton"
---

# ULTIMATUM PREREGISTRATION SKELETON

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*

## Multiplicative vs additive models of ultimatum-game behavior

Purpose: define the minimum honest preregistration structure for the first behavioral-economics bridge test.

---

## 1. Study Title

Behavior Is Multiplicative, Not Additive: Testing coherence-conditioned utility in ultimatum-game behavior

---

## 2. Core Hypothesis

Primary hypothesis:
> A multiplicative model of coherence and payoff will explain ultimatum-game acceptance/rejection behavior better than additive payoff-only models.

Secondary hypothesis:
> The multiplicative model will outperform both a naive positive-payoff baseline and at least one stronger fairness-threshold baseline.

---

## 3. Dataset

Primary dataset family:
- Henrich-style cross-cultural ultimatum-game data, if accessible in analyzable raw or condition-level form

Backup / replication dataset family:
- one standard laboratory ultimatum-game dataset with raw offer and accept/reject structure

To preregister before running:
- exact dataset source
- access status
- licensing status
- whether data are raw trial-level or condition-level

---

## 4. Unit of Analysis

Preferred unit:
- individual decision episode

Fallback unit:
- condition-level aggregate if raw trial-level data are not accessible

This choice must be fixed before model fitting.

---

## 5. Outcome Variable

Primary outcome:
- accept = 1
- reject = 0

Optional secondary outcomes:
- offer size distribution
- proposer behavior by condition/group

---

## 6. Variable Mapping

### V (payoff viability)
Minimal first-pass variable set may include:
- direct payoff to responder if accepted
- normalized offer fraction
- stake size if relevant

### Phi (coherence)
Minimal first-pass variable set may include:
- fairness deviation from reference anchor
- local norm coherence (if cross-cultural dataset supports it)
- legitimacy / expectation proxy where available

The exact Phi construction must be specified before fitting.

---

## 7. Competing Models

At minimum compare:

### Model A — additive / payoff-only baseline
- accept any positive payoff or equivalent additive utility baseline

### Model B — stronger fairness-threshold baseline
- acceptance based on fixed or estimated fairness cutoff

### Model C — multiplicative coherence-payoff model
- U = Phi x V

### Optional Model D — nonlinear competitor
- power-law, logistic, or interaction-enhanced additive model

No paper should be built on a strawman baseline only.

---

## 8. Evaluation Criteria

Pre-register at least one primary and one secondary metric.

Possible metrics:
- predictive accuracy
- log loss / likelihood
- cross-validation performance
- calibration quality
- out-of-sample classification performance

The primary metric must be fixed before fitting.

---

## 9. Preprocessing Rules

Must be fixed in advance:
- how offer values are normalized
- how stake size is handled
- how fairness anchors are defined
- treatment of missing data
- exclusion criteria
- whether cultural/group variables enter the Phi term directly or only in robustness checks

Any post-hoc adjustment must be explicitly labeled exploratory.

---

## 10. Kill Criteria

### K1
If additive or fairness-threshold models explain the data as well or better than the multiplicative model on the preregistered primary metric, the strong multiplicative claim is not supported in this domain.

### K2
If the multiplicative advantage depends on arbitrary preprocessing or post-hoc tuning, the result is not robust.

### K3
If the Phi coding cannot be independently reproduced from the same data and rubric, the result is not trustworthy as a public bridge.

### K4
If a second dataset fails to replicate the qualitative result, the broader claim remains provisional.

---

## 11. Interpretation Boundaries

A positive result would justify saying:
- in this domain, behavior is better modeled as coherence-conditioned utility than as additive payoff alone

A positive result would not justify saying:
- the full core state is proven
- all of behavioral economics is superseded
- every fairness or trust phenomenon reduces to this one model

A failed result narrows the bridge. It does not automatically kill the whole framework.

---

## 12. Replication Packet

Before publication, prepare a packet containing:
- dataset source and access notes
- exact variable definitions
- preprocessing steps
- model formulas
- evaluation metrics
- kill criteria
- runnable code/notebook

Replication standard:
> a stranger should be able to rerun the test without reading the whole corpus

---

## 13. Reporting Rule

When results arrive, report them in this order:
1. dataset and preprocessing
2. baseline performance
3. multiplicative performance
4. robustness checks
5. kill criteria status
6. interpretation boundaries

Do not reverse the order by leading with philosophical conclusions.

---

## 14. Final Formulation

> This preregistration exists so that the first behavioral-economics bridge of the framework can succeed or fail honestly.

---
Related documents:
- 24_EXPERIMENT_SCOPE.md
- 25_FLAGSHIP_PAPER_BRIEF.md
- 26_BEHAVIOR_IS_MULTIPLICATIVE_NOT_ADDITIVE_BRIEF.md
- 27_ULTIMATUM_GAME_STUDY_DESIGN.md
- 28_ULTIMATUM_DATASET_SELECTION_AND_VARIABLE_MAP.md
