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
| D0 | structural boundary role | singleton opaque ground role; Titan seats describe it from the metalanguage; any inscription is a D4 actual token | interpretive, not a physical dimension claim |
| D1 | structural predicate | distinction | an actual inscription or discrimination event is D4 |
| D2 | structural predicate | configuration | an actual configured carrier or observation is D4 |
| D3 | structural state content/model | quantum state `ρ`; distributions arise relative to measurement contexts | an actual preparation or assignment act is D4; the D3 state content and Born distribution are not an interaction/outcome record |
| **D4** | **actual** | causal actuality, embodied means, present model tokens, performed ranking/selection events, action, factual record, commitment and outcome receipts | what happened or is materially available now |
| **D5** | **merely possible** | counterfactual contents, alternative relations, modeled-future referents, candidates for selection, worldline foresight | what could be represented and pursued |
| D6 | structural boundary role | exit/nonclosure frame; any recognition or withdrawal act is a D4 actual token | revisited by `r₆`, not identity, recurrence, or state |

These are Emergentist modeling commitments `[I]`. They are not extra spacetime
dimensions and are not derived from the reciprocal chart.

`Structural` marks an abstract register predicate or boundary, not a third
kind of event. The token-modality tags distinguish an actual carrier from
merely-possible content; they are not exhaustive predicates of ordinary modal
logic. A present D4 model
token may represent D5 content. The token, ranking event, and selection event
are actual; the alternative they refer to remains merely possible:

```text
ModeledFutureToken:D4(actual) ── represents ──▶ AlternativeContent:D5(possible)
RankEvent:D4(actual)          ── ranks ───────▶ AlternativeContent:D5(possible)
SelectionEvent:D4(actual)     ── selects ─────▶ AlternativeContent:D5(possible)
```

Topology exports keep the short schema value `possible`; for D5 it means
`merely_possible`.

Representation does not automatically make every referent D5. A present
memory is an actual D4 token. It may represent a HistoricalClaim which, if
independently warranted as veridical, refers to a past D4 event; imagined
variants remain D5 merely possible content:

```text
m_t:MemoryToken(D4,actual) ── represents ──▶ h_τ:HistoricalClaim
h_τ ── refersTo, if warranted ──▶ e_τ:HistoricalEvent(D4,actual)
m_t ── represents ──▶ p'_τ:AlternativeContent(D5,merely_possible)
```

Vividness is a present D4 salience property. It does not change modality,
register role, dependency priority, or evidence tier. A remembered sunset may
be first in an agent's order of access while depending on D1 distinction, D2
configuration, and a D4 carrier. A quantum description may assign that carrier
a D3 state, but the memory example neither requires nor measures it.

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

### A D5 history bundle over the D4 light cone

For a flat `d+1`-dimensional spacetime and an event at the origin, the future
causal region has cross-section

```text
J⁺(0)={ (t,x) : t≥0 and ||x||≤ct }
Vol_d(t)=π^(d/2)/Γ(d/2+1) · (ct)^d.
```

That geometric widening is D4 physical reachability. It does not count worlds.
The D5 overlay is a separately typed **history bundle**:

```text
π: Hist₅(Q,T) → J⁺(0)
π(h)=endpoint(h)
π⁻¹(e)=represented alternative histories ending at event e.
```

The base cone says where an influence may reach; the fiber says which complete
histories an actual model co-represents. Under a declared discretization and a
set of exclusive/decohered history weights, effective branching can be measured
by `H_hist(t)=−Σ_h p_t(h)log p_t(h)` or `N_eff(t)=exp(H_hist(t))`. For interfering
quantum alternatives one must retain complex amplitudes until the probability
conditions are met.

Thus the cone mouth may be used as a visual analogy for an expanding option
horizon, but its width alone proves neither increasing branch count nor
physically parallel universes. Those require a separate model and evidence.

The authorized option set is a separate normative subset of the physically
reachable option cone. Physical capacity never entails permission.

Two agents can share the same physical causal cone and have different option
cones. Humans are notable for symbolic, social, institutional, and
intergenerational reach—not for exceeding `c` or possessing greater intrinsic
worth. “Agents widen/maximize the cone” is an Emergentist objective hypothesis
`[C]`; the Justice-constrained form seeks durable mutual option-cone widening,
not domination.

### Complete histories and the long tail

A D3 state is one probability-bearing frame. Even an exhaustive state set does
not contain temporal order. The Burri film-from-frames conjecture `[C]` says
that a saturated D3 description must additionally expose compatible complex
transition amplitudes/channels and an internal clock relation. These sew frames
into possible ordered histories. D4 time is the ordering borne by an actual
chain of interactions and records; if an external `t` supplied the ordering,
the construction has reconstructed rather than derived time.

The next lift is **block-to-ensemble**. Let `Hist₄(Q,T)` be the complete
D4-shaped histories admitted by declared laws, boundary conditions, context,
and horizon. Then

```text
Ω₅(Q,T) = {h∈Hist₄(Q,T) : weight_Q(h)>0}
h*∈Ω₅ and receipted                         D4 actual history
{h : h≠h*} represented together in Ω₅      D5 possible contents
OptionCone_t(A) ⊆ Ω₅(Q,T).
```

This is the formal core of the user's “parallel probable timelines” insight.
The histories are parallel in the sense that one actual D4 model token can
co-represent and compare them. The equation does not assert that they all
co-exist physically. “All” is always relative to `Q`, `T`, the declared
contexts, and the error tolerance; it never means every logically describable
universe.

A declared D3 initial state combined with D4 dynamics, clocks, interventions,
and compatible measurement contexts can induce a probability measure on a
support of complete histories `Γ_T⁺`. Known time-indexed states determine
momentum expectations and distributions; a declared record/unravelling can
condition them into quantum trajectories. They do not determine one
context-free classical momentum path. The types remain distinct:

```text
realized history γ*:                     D4 actual
model token representing a history:      D4 actual
represented alternative history γ:       D5 possible
OptionCone_t(A) ⊆ Γ_T⁺
```

Exact enumeration is warranted only for a suitable finite model. Otherwise
“exhausting the long tail” means a declared coverage claim such as
`𝔓_Q(Ĝ_T)≥1−ε`, with the horizon, discretization, contexts, and
tolerance exposed. It neither makes every model-admissible history reachable
by an agent nor proves that every history physically exists. Reading the
support as one block universe plus all possible block universes remains a
removable correspondence `[C]`.

This supplies the register-safe compression: `μ₃` concerns how a probability
assignment is joined to one actual run and record; `μ₄` concerns whether an
actual carrier can represent and rank alternatives to that history. The
composite `D3 → D4 → D5` is a transmission through actuality, never a jump over
it.

## 7. Constraint rule

D4 modeling of D5 content may reweight which D4-admissible paths an agent
selects. Merely possible content has no independent causal arrow, and no model
can authorize physically forbidden transitions:

```text
support(K_X^C) ⊆ support(K_X).
```

Constraint and selection provide a non-mystical account of downward causation:
the higher-level pattern changes probabilities or choices among lower-lawful
trajectories.

## 8. D3 quantum boundary and removable interpretations

D3 and D5 are now explicitly different types:

```text
D3: ρ plus measurement context M -> p(k|ρ,M)=Tr(ρE_k)
D4: actual preparation, interaction, outcome token, and record
D5: semantic counterfactual contents represented and ranked by an agent
```

A D3 quantum alternative is not thereby a D5 modeled future. `μ₃` may name the
selected state-to-record interface; it is not `χ`, an agent commitment, a
consciousness act, or an asserted fundamental collapse.

Interpretation claims remain optional: Everett has no fundamental collapse;
Copenhagen-family actualization is interpretation-specific; neither is an
extra spacetime dimension or a rung stacked above the other. Removing these
interpretive sentences leaves the density-operator, Born/POVM, D4 record, and
D5 agent-option contracts unchanged. The chart identity `φν=1` is never a Born
normalization.

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
- maps quantum branch alternatives to D5 agent counterfactuals by identity;
- stacks Everett and Copenhagen as dimensional layers;
- makes one quantum interpretation necessary for the operational calculus.

## Read with

- [Primitives and Type Signatures](29_PRIMITIVES_AND_TYPE_SIGNATURES.md)
- [μ-Limit Formula](10_EFR_MU_LIMIT_FORMULA.md)
- [Dimensional Closure](23_DIMENSIONAL_CLOSURE_PROOF.md)
- [Quantum Boundary](38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md)
- [Soul Loop](../01_THE_TRANSCENDENTAL_TRINITY/10_THE_SOUL_LOOP.md)

*D5 lets the possible become causally relevant. D4 is where the world answers.*
