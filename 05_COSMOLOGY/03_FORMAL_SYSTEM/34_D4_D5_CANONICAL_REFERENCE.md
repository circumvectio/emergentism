---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[I/C]"
  canonical_phrase: "D4 actuality / D5 possibility"
title: "D4/D5 Canonical Reference"
status: "CANONICAL — single-modality Kintsugi repair 2026-07-17."
evidence_tier: "[I] selected register semantics and operational grammar; [C] empirical emergence and option-cone hypotheses."
supersedes_blob: "f835bacca6f6d3cdeffeeaa8f2b1154f6c9ca5af"
---

# D4/D5 Canonical Reference

This document fixes one mandatory type distinction:

```text
D4 = causal actuality
D5 = counterfactual possibility
```

The meanings do not reverse between “emergence” and “action” registers.
Emergence and enactment are opposite **motions between the same typed nodes**,
not two meanings of actuality.

## 1. Register table

| Register | Modality | Canonical content | Boundary |
|---|---|---|---|
| D0 | actual | ground-limit / unarticulated boundary token | interpretive, not a physical dimension claim |
| D1 | actual | distinction | a difference is instantiated |
| D2 | actual | configuration | relations coexist |
| D3 | actual | transformation and persistence | state changes through time |
| **D4** | **actual** | causal actuality, embodied means, performed action, factual record, commitment and outcome receipts | what happened or is materially available now |
| **D5** | **possible** | counterfactual alternatives, modeled futures, ranking, selection, worldline foresight | what could be represented and pursued |
| D6 | actual | apophatic closure boundary token, no additional positive freedom | returns by `r₆`, not identity |

These are Emergentist modeling commitments `[I]`. They are not extra spacetime
dimensions and are not derived from the reciprocal chart.

## 2. The two motions

### Emergence: `D4 → μ₄ → D5`

The candidate crossing `μ₄` asks whether a D4 organism with memory, sensing,
and embodied interaction exhibits a newly discriminable D5 capacity: modeling
alternatives that are not presently actual, ranking them, and using them to
prepare action.

```text
D4 actual state ── μ₄ candidate crossing ──▶ D5 option field
```

This is a testable `[C]` claim per system. Missing reduction means
`currently_unreduced`, not irreducible. A successful reduction reclassifies the
crossing without deleting the useful register distinction.

### Enactment: `D5 → commitment → D4`

A modeled option can produce an attempted action only when a finite agent has:

1. an option field and fallible model;
2. D4 means sufficient to attempt the action;
3. a complete AuthorizationEnvelope;
4. an admissible action under current constraints.

```text
D5 option ── selection + D4 means + authorization ──▶ D4 attempted action
```

Selection is not a μ-crossing and does not guarantee the selected future.
The environment, other agents, chance, and lower-level constraints still
determine what occurs.

## 3. The typed selector and two receipts

```text
χ_t:(X_t,Ω_t,M_t,V_t,U_t) → (a_t,q_t),  a_t ∈ Action ∪ {⊥}
```

- `X_t`: actual state available to the agent;
- `Ω_t`: D5 option field;
- `M_t`: fallible model and present modeled-future tokens;
- `V_t`: D4 usable means;
- `U_t`: accountable authorization and admissibility constraints;
- `a_t`: attempted action, or `⊥` when commitment is refused/unavailable;
- `q_t`: **CommitmentReceipt**, recording selection, actor, authorization, and
  performed commitment, refusal, or unavailability.

If means, authorization, or admissibility fails, `a_t=⊥` and `q_t` records
the non-commitment. No action transition is submitted to `K_t`.

The world returns the outcome separately:

```text
(X_{t+1},r_{t+1}) ~ K_t(·|X_t,a_t,E_t)  when a_t ∈ Action
```

- `K_t`: environment transition kernel or causal process;
- `E_t`: conditions outside the selector;
- `r_{t+1}`: **OutcomeReceipt** recording observed consequence, or a typed null
  when no action transition was submitted.

The feedback update is:

```text
(M_{t+1},G_{t+1}) = Loop(M_t,G_t,q_t,r_{t+1})
```

The selector cannot manufacture its own consequence. A null or
non-informative receipt may legitimately produce a null update.

## 4. Three inspectable gaps

| Gap | Difference | Receipt surface |
|---|---|---|
| cognitive | territory versus model | prediction/model audit |
| execution | intended action versus performed commitment | `q_t` |
| outcome | expected consequence versus observed consequence | `r_{t+1}` |

Negative feedback means a declared error measure decreases. Positive feedback
means divergence or self-confirmation increases. These signs are dynamical,
not moral.

## 5. Model-mediated future influence

The public compression is:

```text
F = M × A
```

Read `F` here as a **modeled future's present influence**, `M` as the current
model token/representation, and `A` as agency capable of acting on it. The
formal operation is typed coupling:

```text
M⋆A : ModelState × AdmissibleActionField → ActionWeights
```

Changing the represented future can change the distribution of present
actions. That is genuine causal influence in the present Soul Loop. The causal
carrier is the current model state embodied in memory, speech, diagrams,
institutions, or code—not future content physically propagating backward in
time. The realized future remains a function of the environment, other agents,
constraints, and chance.

This is the most defensible meaning of **model-mediated retrocausality**. It
does not assert physical retrocausality.

## 6. Physical causal cone and option cone

A physical light cone is the spacetime set of events that can be causally
connected under relativistic constraints. It remains bounded by spacetime and
`c`.

An **option cone** is a different type: the admissible histories an agent can
model, rank, coordinate, authorize, and plausibly reach within a horizon and
cost budget.

```text
OptionCone_t(A) =
  ReachableHistories(models, means, coordination, authorization, cost, horizon)
⊆ PhysicallyAdmissibleHistories(X_t)
```

Two agents can share the same physical causal cone and have different option
cones. Humans are notable for symbolic, social, institutional, and
intergenerational reach—not for exceeding `c` or possessing greater intrinsic
worth. “Agents widen/maximize the cone” is an Emergentist objective hypothesis
`[C]`; the Justice-constrained form seeks durable mutual option-cone widening,
not domination.

## 7. Constraint rule

Higher-level D5 modeling may reweight which D4-admissible paths an agent
selects. It cannot authorize physically forbidden transitions:

```text
support(K_X^C) ⊆ support(K_X).
```

Constraint and selection provide a non-mystical account of downward causation:
the higher-level pattern changes probabilities or choices among lower-lawful
trajectories.

## 8. Removable quantum correspondence `[C]`

This analogy is optional and non-load-bearing:

- D5 alternatives may be compared with structured alternatives or
  observer-relative branch relations.
- D4 records may be compared with enacted or observer-relative factual
  records.
- Everett's relative-state formulation has no fundamental collapse.
- Copenhagen-family actualization is interpretation-specific.
- Neither interpretation is literally an extra spacetime dimension.
- Neither `μ` nor `χ` is quantum measurement.

Removing this section changes none of §§1–7. For a probability illustration,
use a measure on events,

```text
𝔓_ψ(A)=∫_A |ψ(s)|² ds,     o ~ 𝔓_ψ,
```

never a “sample” from the normalization scalar.

## 9. Worked boundary cases

### Selection without means

An agent ranks option `a` highest but has `V_t=0`. The option remains D5
possible; no D4 commitment occurs.

### Attempt with environment veto

An authorized agent performs `a_t`; `q_t` records the commitment. The
environment blocks or alters it, so `r_{t+1}` differs from the expected result.
The model updates from the gap rather than rewriting intention as success.

### Same physical cone, different option cones

Two people occupy the same room. One has relevant language, institutional
access, and training; the other does not. Their physical causal cones are
effectively the same, but their modeled and reachable history sets differ.

### Future-model intervention

Present an agent with two different credible forecasts while holding current
physical conditions fixed. If action distributions change, this supports
model-mediated future influence. It does not demonstrate future-to-past
physical signaling.

## 10. Falsifiers and source-negative rules

The canonical reference fails if a live owner:

- assigns D4 to possibility or D5 to actuality;
- calls actuality register-indexed;
- labels commitment `μ` or measurement;
- lets `χ` emit an outcome receipt;
- treats selected action as guaranteed consequence;
- says an agent physically widens a light cone;
- stacks Everett and Copenhagen as dimensional layers;
- makes the quantum inset necessary for the operational calculus.

## Read with

- [Primitives and Type Signatures](29_PRIMITIVES_AND_TYPE_SIGNATURES.md)
- [μ-Limit Formula](10_EFR_MU_LIMIT_FORMULA.md)
- [Dimensional Closure](23_DIMENSIONAL_CLOSURE_PROOF.md)
- [Quantum Boundary](38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md)
- [Soul Loop](../01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md)

*D5 lets the possible become causally relevant. D4 is where the world answers.*
