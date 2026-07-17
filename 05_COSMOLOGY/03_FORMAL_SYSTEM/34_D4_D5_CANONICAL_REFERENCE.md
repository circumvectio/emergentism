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
| **D4** | **actual** | causal actuality, embodied means, present model tokens, performed ranking/selection events, action, factual record, commitment and outcome receipts | what happened or is materially available now |
| **D5** | **merely possible** | counterfactual contents, alternative relations, modeled-future referents, candidates for selection, worldline foresight | what could be represented and pursued |
| D6 | actual | apophatic closure boundary token, no additional positive freedom | returns by `r₆`, not identity |

These are Emergentist modeling commitments `[I]`. They are not extra spacetime
dimensions and are not derived from the reciprocal chart.

The modality tags distinguish an actual carrier from merely-possible content;
they are not exhaustive predicates of ordinary modal logic. A present D4 model
token may represent D5 content. The token, ranking event, and selection event
are actual; the alternative they refer to remains merely possible:

```text
ModeledFutureToken:D4(actual) ── represents ──▶ AlternativeContent:D5(possible)
RankEvent:D4(actual)          ── ranks ───────▶ AlternativeContent:D5(possible)
SelectionEvent:D4(actual)     ── selects ─────▶ AlternativeContent:D5(possible)
```

Topology exports keep the short schema value `possible`; for D5 it means
`merely_possible`.

## 2. The two motions

### Emergence: `D4 → μ₄ → D5`

The candidate crossing `μ₄` asks whether a D4 organism with memory, sensing,
and embodied interaction exhibits a newly discriminable capacity to produce
actual tokens and operations that represent and compare D5 alternatives not
presently actual, then use them to prepare action.

```text
D4 actual state ── μ₄ candidate crossing ──▶ D5 option field
```

This is a testable `[C]` claim per system. Missing reduction means
`currently_unreduced`, not irreducible. A successful reduction reclassifies the
crossing without deleting the useful register distinction.

### Enactment: `D5 → commitment → D4`

A governed commitment can authorize an attempted action only when a finite
agent has:

1. an option field and fallible model;
2. D4 means sufficient to attempt the action;
3. a valid complete `AuthorizationEnvelope`;
4. a normatively admissible action under current constraints.

```text
D5 option ── selection + D4 means + authorization ──▶ D4 attempted action
```

The D4 selection event is not a μ-crossing and does not guarantee the selected
future.
The environment, other agents, chance, and lower-level constraints still
determine what occurs.

This is a normative gate, not a causal law. Unauthorized, coerced, accidental,
or criminal attempts remain physically representable and must be receipted.
The governed selector may refuse them; the descriptive world model may not
erase them.

## 3. The typed selector and two receipts

```text
χ_t:(X_t,Ω_t,M_t,V_t,U_t,G_t) → (a_t,q_t),  a_t ∈ Action ∪ {⊥}
```

- `X_t`: actual state available to the agent;
- `Ω_t`: D5 merely-possible alternative contents;
- `M_t`: fallible D4-actual model and present modeled-future tokens;
- `V_t`: D4 usable means;
- `U_t`: authorization assessment and normative constraints;
- `G_t`: D4-actual selector policy, habits, or weights;
- `a_t`: attempted action, or `⊥` when commitment is refused/unavailable;
- `q_t`: **CommitmentReceipt**, recording selection, actor, physical
  availability, authorization status, and attempted commitment, refusal, or
  unavailability.

`a_t=⊥` only when no action is attempted because it is refused or physically
unavailable. Invalid or absent authorization is recorded separately. If an
unauthorized action is nevertheless attempted, `a_t∈Action` and the causal
kernel receives it. A governed channel `χ_t^J` may fail closed and return `⊥`
for that same authorization defect.

`AuthorizationAssessment` is a validated tagged union: `valid` requires a
complete non-null envelope; `invalid` requires a defective supplied record and
reasons; `absent` requires a null envelope and reasons; `not_required` is
limited to explicitly nonconsequential scope. Receipt commitment status is
derived from that validated assessment.

The world returns the outcome separately:

```text
(X_{t+1},r_{t+1}) ~ K_t(·|X_t,a_t,E_t)  when a_t ∈ Action
```

- `K_t`: environment transition kernel or causal process;
- `E_t`: conditions outside the selector;
- `r_{t+1}`: **OutcomeReceipt** recording observed consequence. With no action
  transition it is either null or carries `receiptCause=ambient_observation`
  with null action identifiers; ambient change is not attributed to `⊥`.

The feedback update is:

```text
(M_{t+1},G_{t+1}) = Loop(M_t,G_t,q_t,r_{t+1})
```

The selector cannot manufacture its own consequence. Because `G_t` is an input
to `χ_t`, an updated `G_{t+1}` can affect the next selection rather than become
a dangling audit field. A null or non-informative receipt may legitimately
produce a null update.

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
M⋆A : ModelState × PhysicallyFeasibleActionField → ActionWeights
```

Changing the represented future can change the distribution of present
actions. That is genuine causal influence in the present Soul Loop. The causal
carrier is the current model state embodied in memory, speech, diagrams,
institutions, or code—not future content physically propagating backward in
time. The realized future remains a function of the environment, other agents,
constraints, and chance.

Emergentism calls this **model-mediated retrocausality** as project-specific
shorthand. In standard causal language it is anticipatory or future-guided
control: every physical arrow in the displayed chain still points forward in
time. It does not assert a temporal relation from a future event to the past.

## 6. Physical causal cone and option cone

A physical light cone is the spacetime set of events that can be causally
connected under relativistic constraints. It remains bounded by spacetime and
`c`.

An **option cone** is a different type: the histories an agent can model, rank,
coordinate, and plausibly reach within a horizon and cost budget.

```text
OptionCone_t(A) =
  ReachableHistories(models, means, coordination, cost, horizon)
⊆ PhysicallyAdmissibleHistories(X_t)
```

The authorized option set is a separate normative subset of the physically
reachable option cone. Physical capacity never entails permission.

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

### Unauthorized but causal attempt

An actor has D4 means but lacks a valid envelope. A governed selector refuses
the action. If the actor nevertheless attempts it, the descriptive receipt
records `authorization.status∈{invalid,absent}`, and `K_t` still returns the
consequence. Normative invalidity does not make the event causally invisible.

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
- types a present model, ranking, or selector event as merely possible;
- treats invalid authorization as physical impossibility or erases an
  unauthorized attempted action;
- updates `G` without feeding it into the next selector;
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
