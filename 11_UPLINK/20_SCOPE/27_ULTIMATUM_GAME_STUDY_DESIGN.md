---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Ultimatum Game Study Design"
---

# ULTIMATUM GAME STUDY DESIGN

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*

## First empirical bridge for Behavior Is Multiplicative, Not Additive

> This note defines the first bounded experimental design for testing whether coherence-conditioned utility explains behavior better than additive utility in the ultimatum game.

---

## 1. Purpose

The ultimatum game is the clearest first proving ground because additive utility models predict one thing very strongly:

> any positive offer should be accepted.

But observed human behavior repeatedly violates that prediction.

This study asks whether those so-called anomalies are better explained by a multiplicative relation between:
- V = material viability / payoff, and
- Phi = coherence variables such as fairness, legitimacy, and self-respect.

---

## 2. Core Claim

> In ultimatum-game choice, positive payoff is often insufficient for acceptance when coherence collapses. A multiplicative Phi x V model will therefore predict accept/reject behavior better than additive payoff-only models.

---

## 3. Formal Contrast

### Additive baseline
U_add = payoff

Prediction:
- accept every offer > 0

### Multiplicative candidate
U_eff = Phi x V

Where:
- V = normalized material gain from the offer
- Phi = normalized coherence term capturing fairness, legitimacy, and identity congruence

Prediction:
- some positive offers will still be rejected when Phi is low enough

---

## 4. Hypotheses

### H1
A multiplicative coherence-conditioned model predicts accept/reject choices better than a payoff-only additive model.

### H2
The multiplicative model explains why low but positive offers are often rejected without classifying that rejection as irrational noise.

### H3
The model will perform especially well in conditions where legitimacy, framing, or social meaning are experimentally manipulated.

---

## 5. Unit of Analysis

Preferred:
- individual decision episode

Fallback:
- condition-level or aggregated response rates if raw trial data are unavailable

---

## 6. Outcome Variable

Binary outcome:
- 1 = accept
- 0 = reject

Optional extension:
- response latency
- confidence / affect if available, but not required for first pass

---

## 7. V Variables

For the first ultimatum-game study, keep V minimal and transparent.

### V1. Offer fraction
- offer / total pot
- normalized to [0,1]

### V2. Absolute payoff magnitude
- optional if multiple pot sizes exist
- normalized within dataset

### V first-pass recommendation
If pot size is fixed, use:
- V = offer fraction only

This keeps the first test clean.

---

## 8. Phi Variables

Phi must be kept minimal for the first test.

### Phi1. Fairness ratio
- closeness of offer to equal split
- simplest form: 1 - abs(offer_fraction - 0.5) / 0.5
- yields 1 at 50/50, lower as offer becomes more unequal

### Phi2. Legitimacy condition
- optional binary or ordinal variable if dataset contains manipulated procedure legitimacy
- for example: random allocation vs human intentional split

### Phi3. Identity / dignity condition
- optional if dataset tracks insult, status, anonymity, or social framing

### Phi first-pass recommendation
Start with:
- Phi = fairness ratio

Then in a second pass add legitimacy and identity modifiers if the dataset supports them.

---

## 9. First-Pass Model Set

### Model A — payoff-only additive
Predict accept whenever payoff > 0, or fit a logistic model using offer fraction only.

### Model B — weighted additive
accept ~ a*offer_fraction + b*fairness_ratio

### Model C — multiplicative
accept ~ offer_fraction * fairness_ratio
or logistic equivalent using the interaction term as the central explanatory variable

### Model D — additive + interaction benchmark
accept ~ offer_fraction + fairness_ratio + offer_fraction*fairness_ratio

This prevents the multiplicative model from winning against a strawman.

---

## 10. Preferred Statistical Form

If raw trial-level data are available, use logistic regression or a comparable binary classifier.

Recommended sequence:
1. payoff-only logistic baseline
2. additive fairness + payoff logistic
3. multiplicative / interaction-centered model
4. compare predictive performance

Metrics:
- held-out accuracy
- log loss / cross-entropy
- AUC if appropriate
- calibration on low-offer region

The low-offer region is especially important because that is where additive logic fails most clearly.

---

## 11. Main Diagnostic Region

The key region is:
- positive but unfair offers

This is where additive payoff-only logic predicts acceptance most strongly, but observed behavior often diverges.

If the multiplicative model captures rejection there better, the bridge is meaningful.

---

## 12. Kill Criteria

### K1
If payoff-only or additive models perform as well or better than the multiplicative candidate, the strong claim fails in this domain.

### KC2
If the multiplicative advantage only appears after arbitrary preprocessing or parameter tuning, the result is not robust.

### K3
If a second ultimatum dataset or replication sample fails to show the same pattern, the broader claim remains provisional.

### K4
If fairness coding cannot be made simple and transparent enough for an external reader to reproduce, the study design is too interpretive and must be narrowed.

---

## 13. Replication Packet Requirements

A stranger should be able to rerun the test with no corpus immersion.

Minimum packet:
- dataset source and citation
- exact variable mapping
- formula for fairness ratio
- all preprocessing steps
- exact model specifications
- kill criteria
- code or notebook
- short interpretation note on what a positive result does and does not imply

---

## 14. Interpretation Boundaries

A positive result would justify saying:
- ultimatum behavior is better modeled by coherence-conditioned utility than by payoff alone
- fairness is not merely decorative; it structurally conditions economic choice

A positive result would NOT justify saying:
- the whole core state is proven
- all behavioral economics is solved
- every human choice follows the full framework

This is one bounded empirical bridge.

---

## 15. Why This Is the Right First Behavioral Test

The ultimatum game is ideal because:
- the additive baseline is simple and strong
- the anomaly is famous
- fairness is central and legible
- the result is easy to explain publicly
- the replication burden is manageable

This makes it a better first strike than a broader and noisier behavioral economics tour.

---

## 16. Next Sequence

If this first study works, extend in order:
1. trust game
2. framing / loss-aversion tasks
3. public-goods / cooperation environments

Do not start broad. Win the first clean case first.

---

## Final Formulation

# Ultimatum-game study rule

> The first behavioral test should ask one narrow question: does coherence-conditioned utility explain the rejection of unfair positive offers better than additive payoff alone?

That is enough for the first bridge.

---
Related documents:
- 25_FLAGSHIP_PAPER_BRIEF.md
- 25_EXPERIMENT_SCOPE.md
- PAPER_I_KNOWN_UNKNOWNS_PROGRAM.md
- ../../00_META/00_WHAT_IS_ACTUALLY_NOVEL_HERE.md
