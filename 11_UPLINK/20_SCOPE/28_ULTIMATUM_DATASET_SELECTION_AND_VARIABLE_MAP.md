---
rosetta:
  primary_column: "Philosophy"
  register: "[I]"
  canonical_phrase: "Ultimatum Dataset Selection And Variable Map"
---

# ULTIMATUM DATASET SELECTION AND VARIABLE MAP

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*

## First empirical bridge for the behavioral-economics flagship path

> This note selects the first dataset family for the ultimatum-game study and maps the available variables into the framework's coherence (Phi) and viability (V) structure.

---

## Decision

### Primary dataset family
**Henrich-style cross-cultural ultimatum game data**

### Replication dataset family
**one standard laboratory ultimatum-game dataset with raw offer/acceptance fields**

This is the current canonical choice.

---

## Why this dataset family

This dataset family is preferred because it offers:
- public recognizability,
- a direct challenge to additive rational-choice expectations,
- variation in fairness norms and legitimacy conditions,
- and a cleaner path to a bounded first empirical bridge.

A purely self-report flourishing dataset is not the right first proving ground here.
The ultimatum game is better because it gives:
- hard behavioral outcomes,
- clear payoff structure,
- and direct visibility of when additive utility fails.

---

## Paper-level hypothesis

> Additive utility models under-explain ultimatum-game behavior because they omit coherence-sensitive variables such as fairness, legitimacy, and expectation structure.

> A multiplicative or coherence-conditioned model should outperform purely additive payoff models in explaining observed accept/reject behavior.

---

## Required raw fields

The first paper should use a dataset that contains, at minimum:
- proposer offer amount or offer fraction,
- responder accept/reject outcome,
- stake size or total pot,
- condition / group / society identifier.

Strongly preferred additional fields:
- anonymity/publicness condition,
- one-shot vs repeated condition,
- market integration / social complexity indicators,
- demographic fields,
- local norm or fairness expectation data where available.

---

## Variable mapping

### V — Viability / payoff
For the ultimatum game, the first clean approximation of V is material payoff viability.

For the responder:
- amount received if accepted
- normalized payoff share
- optional future/repeated-game leverage if the design includes repeated rounds

Minimal starting form:

```text
V = offered payoff (normalized to stake size)
```

### Phi — Coherence / fairness / legitimacy
For the ultimatum game, Phi should initially be modeled as the coherence of the offer with the operative fairness norm or legitimacy expectation.

Possible first proxies:
- distance from a 50/50 split,
- distance from local median accepted fair split,
- distance from culture-specific fairness anchor,
- condition-level legitimacy/framing variable if available.

Minimal starting form:

```text
Phi = 1 - |offer_fraction - fairness_anchor|
```

where `fairness_anchor` is either:
- 0.50, or
- an empirically estimated local fairness norm.

This is only the first operationalization, not the final one.

---

## Model comparison set

The first paper should compare at least:

### Model A — Additive rational-choice baseline
Predict acceptance from positive material payoff alone.

### Model B — Fixed fairness threshold baseline
Predict rejection below a threshold fairness cutoff.

### Model C — Phi x V model
Predict choice from coherence-conditioned payoff.

Possible simple form:

```text
U = Phi x V
```

### Optional Model D — nonlinear competitor
For example:
- logistic fairness-payoff interaction,
- power-law model,
- weighted additive-plus-interaction model.

The framework must not win against a strawman only.

---

## Outcome variable

For the first study, keep the outcome simple:

```text
accept = 1
reject = 0
```

That gives a clean binary prediction target.

---

## Why cross-cultural data matters

A single lab dataset may show that additive utility fails, but a cross-cultural dataset is stronger because it varies the coherence regime itself.

That means the same formal game can be tested across changing:
- fairness norms,
- legitimacy structures,
- market integration,
- and social expectations.

This is exactly where a Phi-sensitive model should show its value.

---

## Replication strategy

### Stage 1
Primary result on the cross-cultural ultimatum dataset family.

### Stage 2
Replication on one standard lab ultimatum dataset.

This protects the result from being dismissed as either:
- culture-specific anomaly, or
- purely anthropological storytelling.

---

## Current open questions

Before the paper can move from brief to preregistration, the following must be locked:

1. exact dataset source and access path
2. final fairness-anchor definition
3. whether Phi is hand-coded or directly inferred from the data structure
4. final competitor model set
5. exact kill criteria

---

## Canonical next move

The next artifact after this note should be:

# ULTIMATUM PREREGISTRATION SKELETON

That document should include:
- exact hypothesis
- exact datasets
- preprocessing rules
- exact models
- exact kill criteria
- replication packet requirements

---

## Final Formulation

> The first behavioral-economics bridge should begin with the ultimatum game, using a cross-cultural dataset to test whether coherence-conditioned payoff models outperform additive payoff models.

That is the current canonical starting point.

---
Related documents:
- 24_EXPERIMENT_SCOPE.md
- 25_FLAGSHIP_PAPER_BRIEF.md
- 26_BEHAVIOR_IS_MULTIPLICATIVE_NOT_ADDITIVE_BRIEF.md
- 27_ULTIMATUM_GAME_STUDY_DESIGN.md
