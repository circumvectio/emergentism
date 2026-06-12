---
rosetta:
  primary_column: "Game theory"
  register: "[I]"
  canonical_phrase: "Paper Brief"
---

# PAPER BRIEF

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*

## Behavior Is Multiplicative, Not Additive

### Working subtitle
Coherence, trust, legitimacy, and the structure of economic choice

---

## 1. Purpose

This paper tests a bounded but important claim:

> many behaviors treated as irrational by additive utility models are better explained by a multiplicative relation between payoff viability and coherence-sensitive variables such as fairness, trust, legitimacy, and frame integrity.

This is not a defense of the whole framework.
It is a targeted empirical bridge.

---

## 2. Core Thesis

Standard behavioral-economics anomalies may not be anomalies at all.

They may instead show that:
- material payoff is not sufficient,
- and that choice is often governed by a finite-node multiplicative structure:

P_node = Φ × V

Where:
- V = payoff viability / instrumental value
- Φ = coherence variables such as fairness, trust, legitimacy, and self-consistency

The proposal is:

> additive models often fail because they omit the coherence conditions that make a payoff livable, acceptable, or actionable.

---

## 3. Why This Matters

Behavioral economics is full of cases where simple rational-choice expectations fail:

- people reject unfair positive offers
- people trust when exploitation seems possible
- framing changes choice despite constant nominal payoff
- legitimacy and trust alter compliance beyond raw incentives

These behaviors are often described as:
- biases
- irrationality
- bounded departures from utility

This paper asks whether they are better understood as:
coherence-sensitive utility.

---

## 4. Formal Proposal

### Additive baseline
U_add = sum(v_i)

### Weighted additive baseline
U_wadd = sum(w_i v_i)

### Multiplicative candidate
U_mult = Φ × V

Where:
- V aggregates payoff-relevant variables
- Φ aggregates coherence-relevant variables

### Optional stronger model
Φ = product(phi_j)^(1/n)
V = product(nu_k)^(1/m)
U = Φ × V

This stronger form can be tested in appendix or later work.

---

## 5. Conceptual distinction

### Additive view
A positive payoff remains worth taking if it adds to the total.

### Multiplicative view
A positive payoff may still be rejected if coherence collapses:
- unfairness,
- illegitimacy,
- self-respect loss,
- trust collapse,
- or frame incoherence
can drive the effective utility toward zero.

This gives a simple interpretation of many classic findings:

> the payoff exists, but the agent cannot inhabit it coherently.

---

## 6. Candidate experimental domains

The first paper should stay narrow.

### Preferred initial domains
1. ultimatum game
2. trust game
3. framing / loss-aversion tasks

These are ideal because:
- they are canonical in behavioral economics
- they have clear outcome variables
- additive baselines are well understood
- coherence-sensitive behavior is already visible

---

## 7. Variables

### V — payoff viability
Possible dimensions:
- immediate material payoff
- expected future payoff
- option preservation
- risk-adjusted value
- time/effort efficiency
- strategic leverage

### Φ — coherence
Possible dimensions:
- fairness perception
- trust in counterpart
- institutional legitimacy
- frame coherence
- identity congruence / self-respect
- expectation stability

The exact dimensional set should be minimized for each experimental domain.

---

## 8. First test case: ultimatum game

This is the strongest opening case.

### Additive prediction
Any positive offer should be accepted.

### Multiplicative prediction
A positive offer may still be rejected if:
- fairness collapses,
- self-respect collapses,
- legitimacy collapses,
- or the interaction becomes incoherent.

This gives a simple structural explanation for why positive utility may still be behaviorally null.

---

## 9. Second test case: trust game

The trust game tests whether trust is noise or structure.

### Additive prediction
Withhold where exploitation risk is high.

### Multiplicative prediction
Trust can be rational where:
- payoff viability is moderate,
- but coherence is high:
  - trustworthy counterpart
  - stable expectations
  - legitimate setting
  - repeated interaction structure

This would show that trust is not outside economics. It is part of viable exchange.

---

## 10. Third test case: framing effects

Framing problems are ideal because nominal payoff may remain constant while behavior changes.

### Additive prediction
Choice should remain stable if payoff is unchanged.

### Multiplicative prediction
Choice can shift because frame changes Φ without changing V.

This lets the paper test whether coherence-sensitive interpretation explains frame effects better than bias language alone.

---

## 11. Model comparison

The paper should compare at least:

### Model A
Additive payoff-only

### Model B
Weighted additive payoff-only

### Model C
Φ × V multiplicative model

### Optional Model D
One nonlinear competitor, such as power-law interaction or additive-plus-interaction baseline.

This prevents the multiplicative model from winning against a strawman.

---

## 12. Main hypotheses

### H1
The multiplicative model predicts observed choices better than additive payoff-only models.

### H2
The multiplicative model better explains unfair-offer rejection, trust-sensitive cooperation, and frame-sensitive choice.

### H3
The multiplicative model identifies cases where additive utility is positive but effective behavioral utility collapses because coherence is too low.

---

## 13. Kill criteria

These must be pre-registered.

### K1
If additive models predict behavior as well or better than the multiplicative model, the strong claim fails in that domain.

### K2
If the Φ coding cannot be replicated independently, the result is not trustworthy.

### K3
If multiplicative advantage depends entirely on arbitrary preprocessing or post-hoc tuning, the result is not robust.

### K4
If the result fails to generalize across at least one second domain (for example, trust game after ultimatum game), the broader claim remains provisional.

---

## 14. What a positive result would mean

A positive result would support the claim that many behavioral-economic anomalies are better modeled as failures of additive utility rather than failures of human reason.

It would justify saying:
- coherence-sensitive utility is a better model in at least this tested domain,
- fairness, trust, and legitimacy are not merely psychological decorations,
- they are structurally relevant to economic behavior.

### What it would NOT mean
It would not prove:
- the full core state,
- the full geometry,
- or every framework-level claim.

It would establish a bounded empirical bridge.

---

## 15. What a negative result would mean

A negative result would not kill the framework.
It would mean:
- the multiplicative choice thesis narrows,
- additive models remain more appropriate in that domain,
- or the Φ construction is weaker than expected.

This is acceptable. The test is meant to discipline the framework, not flatter it.

---

## 16. Replication packet

Minimum contents:
- dataset source
- raw variable descriptions
- coding rubric for Φ and V
- preprocessing steps
- model definitions
- evaluation metrics
- kill criteria
- reproducible code or notebook

The standard should be:

> a stranger should be able to rerun the paper without reading the whole corpus.

---

## 17. Tone discipline

This paper should not sound like a worldview manifesto.
It should sound like one clean empirical proposal with one model contrast and one bounded claim.

Avoid:
- triumphant metaphysical conclusions
- unnecessary framework jargon
- scorecard rhetoric
- grand civilizational overclaim

Prefer:
- exactness
- bounded scope
- explicit limits
- replication friendliness

---

## 18. Strongest sentence

> Many behavioral anomalies are not irrational departures from utility, but signs that utility is multiplicatively conditioned by coherence variables omitted from additive models.

That is the claim.

---

## 19. Recommended write order

1. ultimatum game only
2. add trust game
3. add framing effects
4. expand only after one strong result exists

Do not start broad. Make one clean strike first.

---

## 20. Final Formulation

# Paper rule

> One domain, one contrast, one test, one replication path.

That is the strongest way to introduce the framework into behavioral economics.

---
Working title:
Behavior Is Multiplicative, Not Additive
Coherence, trust, legitimacy, and the structure of economic choice
