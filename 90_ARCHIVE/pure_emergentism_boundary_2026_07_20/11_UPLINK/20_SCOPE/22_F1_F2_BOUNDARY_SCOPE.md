---
rosetta:
  primary_column: "Liberal art"
  register: "[I]"
  canonical_phrase: "F1 / F2 Boundary Scope"
---

# F1 / F2 BOUNDARY SCOPE

**Evidence tier:** [I]  
*Organism document. Interpretive operational content. Bounded by current system state.*

## What belongs to TheCircle, what belongs to RealityFutures, and why the boundary matters

> This note defines the canonical boundary between F1 and F2 so that observation, prediction, and market pricing are not silently collapsed into one organ.

---

## Purpose

The organism depends on the integrity of the Three-Stage Process separation:
- F1 observes
- F2 prices uncertainty
- F3 deliberates
- F4 acts

If F1 begins to predict, or F2 silently becomes a perception engine, the organism loses one of its most important protections: the ability to distinguish observation from priced possibility.

This note exists to make that boundary explicit.

---

## Canonical Rule

> **F1 may structure reality, but it may not price possibility.**

> **F2 may price possibility, but it may not pretend to be the observing source.**

That is the core distinction.

---

## F1 — TheCircle

### Canonical function
F1 is the observation and signal-structuring organ.

### What F1 is allowed to do
- ingest raw signals
- normalize observations
- separate facts from claims
- attach provenance and source metadata
- score source credibility or trust history
- emit structured observation packets

### What F1 is NOT allowed to do
- issue market probabilities as if they were prices
- collapse uncertainty into a prediction claim without passing through F2
- act as if source credibility and probability are the same kind of quantity
- replace market formation with observer confidence

### Why
Observation and prediction are not the same operation.
A source can be highly credible and still be wrong about what will happen next.
F1 is allowed to say: “this signal is well-sourced.”
It is not allowed to say: “therefore the event has a 73% probability.”

---

## F2 — RealityFutures

### Canonical function
F2 is the uncertainty-pricing organ.

### What F2 is allowed to do
- take structured F1 signals as input
- construct or match markets/questions
- price possibility through market or model mechanisms
- expose probability, spread, volatility, and confidence-in-price
- emit ProbabilityPacket-style outputs

### What F2 is NOT allowed to do
- pretend to be the original observer
- fabricate raw signal provenance
- skip F1 and claim direct epistemic authority over the world
- convert priced uncertainty into final action or recommendation

### Why
F2 does not tell the organism what reality is. It tells the organism how uncertainty is currently priced.

---

## The Key Distinction

F1 answers:
- What was observed?
- How credible is the source?
- What facts and claims are present?

F2 answers:
- Given these observations, what possibility space is priced?
- What probability is currently implied?
- How wide is the spread?
- How stable is the uncertainty surface?

This distinction is load-bearing.

---

## Common Category Errors

### Error 1 — Confidence becomes probability
“This source is strong, therefore the event is likely.”

This is invalid. Source confidence is not market probability.

### Error 2 — Forecasting inside F1 is mistaken for pricing
A forecasting helper inside TheCircle may be useful operationally, but if it outputs probability claims as if F1 itself were the pricing organ, the Three-Stage Process boundary is violated.

### Error 3 — F2 treated as truth oracle
Probability pricing is not the same as observation. F2 prices possibility; it does not witness raw reality.

---

## Boundary Test

A simple test:

### If the question is
- “What happened?”
- “Who said it?”
- “How credible is this source?”

then the answer belongs to **F1**.

### If the question is
- “What is the implied probability?”
- “How uncertain is this?”
- “How is this possibility currently priced?”

then the answer belongs to **F2**.

---

## Current Reconciliation Implication

Any existing forecasting/probability logic inside TheCircle should be treated as one of the following until reconciled:
- migration target to F2,
- temporary helper requiring explicit downgrade in claim strength,
- or architectural violation requiring removal.

It must not remain silently canonical as if the F1/F2 distinction were intact while code says otherwise.

---

## Relationship to the Packet Spine

In packet terms:
- F1 emits SignalPacket
- F2 emits ProbabilityPacket

A SignalPacket may contain:
- facts,
- claims,
- provenance,
- credibility,
- warnings,

but it should not be treated as if it were already a ProbabilityPacket.

That is exactly the separation the packet spine is meant to protect.

---

## Safer Current Language

Prefer saying:

> TheCircle structures observations; RealityFutures prices uncertainty.

Avoid saying:
- TheCircle predicts markets
- F1 probabilities
- observer confidence equals market likelihood

unless the system is explicitly in a temporary helper mode and that helper status is named honestly.

---

## Final Formulation

# F1 / F2 rule

> **F1 structures the observed. F2 prices the possible. Neither may silently become the other.**

That is the canonical boundary.

---
Related documents:
- 05_ARCHITECTURE.md
- 09_STATE.md
- 11_CANON_RECONCILIATION.md
- 13_FINANCIAL_RECONCILIATION.md
- 20_K2_SOVEREIGNTY_SCOPE.md
