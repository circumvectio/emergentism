---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[A/I/C]"
  canonical_phrase: "PRIMITIVES AND TYPE SIGNATURES"
title: "Primitives and Type Signatures"
status: "CANONICAL TYPE INDEX — Kintsugi repair 2026-07-17."
evidence_tier: "[A] analytic types; [I] selected model records; [C] empirical and strong-emergence hypotheses."
supersedes_blob: "178eac8942c2d3c6c01cada8d37b0007d43e0832"
---

# Primitives and Type Signatures

This file is the closed type index for the repaired Emergentist Compass. It
does not turn an interpretation into a theorem. A symbol or record used with a
different type is a defect unless this owner is deliberately revised first.

## 1. Mathematical chart types

| Primitive | Type | Meaning |
|---|---|---|
| `0` | number | additive identity and ordinary operand |
| `1` | number | multiplicative identity and ordinary operand |
| `∞` | projective point | point at infinity in `ℂP¹`; not a largest number |
| `•,⊙,○` | symbolic tokens | selected Titan names for `0,1,∞`; `[I]`, not arithmetic |
| `S²≅ℂP¹` | compact real 2-manifold / complex 1-manifold | selected projective chart surface |
| `θ` | `(0,π)` in the reciprocal chart | colatitude; endpoints are excluded limits |
| `φ` | `(0,π)→ℝ₊`, `cot(θ/2)` | reciprocal chart coordinate |
| `ν` | `(0,π)→ℝ₊`, `tan(θ/2)` | reciprocal chart coordinate |
| `B` | `(0,π)→(0,1]`, `sinθ` | chart balance coordinate; “balance” is `[I]` |
| `s` | `ℝ₊→ℝ`, `log x` | additive coordinate for positive multiplication |
| `u` | `ℝ₊→(-1,1)`, `(x-1)/(x+1)` | bounded Cayley coordinate |
| `P∞` | `(0,π)→{1}` | analytic identity `φν=1`; not a world law |
| `E_B` | `(0,1]→[0,∞)`, `-log B` | one declared balance-deficit transform |
| `E_s` | `ℝ₊→[0,∞)`, `(log x)²` | inversion-symmetric log distance; not identical to `E_B` |

The identities below are true by construction `[A]`:

```text
φν=1
B=2/(φ+ν)=sinθ=sech(s)
φ+ν≥2
B≤1
```

No real system is thereby proved to instantiate the chart.

## 2. D-register and modality types

```text
DRegister  := D0 | D1 | D2 | D3 | D4 | D5 | D6
ModalityTag := actual | merely_possible
```

| Register | Modality contract | Working content |
|---|---|---|
| `D0` | actual | ground-limit boundary token |
| `D1` | actual | distinction |
| `D2` | actual | configuration |
| `D3` | actual | transformation/persistence |
| `D4` | **actual** | causal actuality, embodied means, present model tokens, performed ranking/selection events, action, factual record, receipt |
| `D5` | **merely possible** | counterfactual contents, alternative relations, modeled-future referents, candidates for selection |
| `D6` | actual | apophatic closure boundary token; no positive new freedom |

There are exactly six adjacent crossing identifiers `μ₀…μ₅`. There is no
`μ₆`. The return `r₆:D6↝D0` is an interpretive, non-μ closure edge.

`actual` and `merely_possible` are role tags in this modeling grammar, not
exhaustive predicates of ordinary modal logic. A present actual record can
represent merely-possible content without contradiction:

```text
ActualRepresentation := {register:D4, modality:actual, recordId:String}
AlternativeContent   := {register:D5, modality:merely_possible, contentId:String}

represents : ActualRepresentation → AlternativeContent
```

The physical production of a model, ranking, or selection is a D4 event. Its
counterfactual referent or ordering is D5 content. Graph exports retain the
short label `possible` for schema compatibility, but it means
`merely_possible` wherever a D5 element is typed.

## 3. Finite-node model types

```text
Φ : Node×Time → [0,1]       # D5 option-field / foresight score
V : Node×Time → [0,1]       # D4 usable means / viability score
P_node : Node×Time → [0,1]
```

Lowercase `φ,ν` are chart coordinates. Uppercase `Φ,V` are separately
operationalized node factors and are never inferred from the lowercase pair.

### ConjunctiveAggregator

```text
ConjunctiveAggregator := {
  id: String,
  domain: "[0,1]^2",
  codomain: "[0,1]",
  monotone: true,
  zeroAnnihilator: true,
  unitNormalized: true,       # C(1,1)=1
  formula: String,
  selected: Boolean,
  tier: EvidenceTier,
  alternatives: [String],
  killCriterion: String
}
```

The selected normalized instance is
`C×(Φ,V)=ΦV`, so `P_node:=C×(Φ,V)`. Selection is `[I]`; universal fit is
`[C]`.

## 4. Emergence record

```text
ReductionStatus := reduced | currently_unreduced | candidate_strong

MuCrossing := {
  id: μ₀ | μ₁ | μ₂ | μ₃ | μ₄ | μ₅,
  source: DRegister,
  target: DRegister,
  saturatedRegister: String,
  saturationEvidence: [EvidenceRef],
  evidenceStatus: supplied | not_yet_supplied,
  newFreedomOrBoundaryResult: String,
  lowerRegisterRecovery: String,
  reductionStatus: ReductionStatus,
  prediction: String,
  tier: EvidenceTier,
  killCriterion: String
}
```

Invariants:

```text
evidenceStatus = supplied         iff saturationEvidence is nonempty
evidenceStatus = not_yet_supplied iff saturationEvidence = []
```

The current externally uncalibrated scaffold instantiates all six records with
`saturationEvidence=[]` and `evidenceStatus=not_yet_supplied`. Descriptions,
predictions, and kill criteria are not evidence for their own crossings.

`μ₅` may record the explicit **no-positive-freedom boundary result** at D6.
Absence of a reducing law maps to `currently_unreduced`, not
`candidate_strong`, unless independent evidence licenses the stronger status.

## 5. Agency, future, and receipt types

```text
ModeledFutureToken := {
  tokenId: String,
  modelId: String,
  carrierRegister: D4,
  carrierModality: actual,
  representedAlternative: AlternativeContent,
  horizon: Duration,
  assumptions: [String],
  probabilityOrRank: Number?,
  generatedAt: Time
}
```

A model token is a present physical record **about** a possible future. It is
not that future and does not travel backward in time.

```text
RankEvent      := {register:D4, modality:actual, tokenId:String, eventId:String}
SelectionEvent := {register:D4, modality:actual, optionId:String, eventId:String}

ranks   : RankEvent × [AlternativeContent] → Order
selects : SelectionEvent → AlternativeContent
```

```text
OptionCone := {
  agentId: String,
  physicalCausalBoundary: String,
  physicallyAdmissibleHistoryIds: [String],
  modeledHistories: [ModeledFutureToken],
  physicallyReachableHistoryIds: [String],
  authorizedHistoryIds: [String],
  horizon: Duration,
  costs: [Cost],
  coordinationDependencies: [String]
}
```

An option cone is not a physical light cone. Agents with the same spacetime
causal cone can have different option cones. Its defining inclusion is

```text
set(physicallyReachableHistoryIds) ⊆ set(physicallyAdmissibleHistoryIds)
set(authorizedHistoryIds) ⊆ set(physicallyReachableHistoryIds).
```

Physical reachability and authorization are deliberately separate. An agent
may be able to model and physically attempt an unauthorized option; that option
is not thereby just or permitted.

```text
AuthorizationEnvelope := {
  principal: String,
  mandate: String,
  scope: String,
  consent: ConsentRecord,
  custody: String,
  expiryOrRevocation: String,
  contestPath: String,
  actor: String,
  consequenceBearerIds: [BearerId]
}
```

All nine fields are required for a **valid accountable authorization**. Their
absence does not make an action physically impossible.

```text
AuthorizationStatus := valid | invalid | absent | not_required

AuthorizationAssessment :=
  | {status:valid,
     envelope:AuthorizationEnvelope,
     reasons:[]}
  | {status:invalid,
     envelope:Partial<AuthorizationEnvelope>,
     reasons:NonEmpty[String]}
  | {status:absent,
     envelope:null,
     reasons:NonEmpty[String]}
  | {status:not_required,
     envelope:null,
     reasons:[],
     scope:NonConsequentialScope}
```

The governed selector may fail closed on `invalid|absent`; the descriptive
causal loop must still represent unauthorized, coerced, accidental, or
criminal attempts and their consequences.

The union is validated before a receipt is emitted. `valid` is inhabited only
by a complete envelope. `invalid` requires a supplied but defective record and
at least one defect. `absent` requires no envelope and at least one reason.
`not_required` is confined to an explicitly nonconsequential scope and can
never satisfy Justice or authorize a consequential act.

```text
EvaluationContract := {
  id: String,
  horizon: Duration,
  baselineRef: String,
  measureIds: [String],
  bearerIds: [BearerId],
  modelId: String
}

BearerObservation := {
  bearerId: String,
  measureId: String,
  baselineValue: Number,
  observedValue: Number,
  sourceRef: EvidenceRef,
  observedAt: Time
}

CommitmentReceipt := {
  receiptType: "commitment",
  status: authorized_committed | unauthorized_attempt | nonconsequential_attempt | refused | unavailable,
  attemptedActionId: String?,
  executionStatus: attempted | partial | failed | refused | unavailable,
  physicalAvailability: available | unavailable,
  authorization: AuthorizationAssessment,
  selectedOptionId: String?,
  intention: String,
  meansUsed: [String],
  evaluation: EvaluationContract,
  expectedBearerDeltas: {BearerId:Number},
  expectedOutcome: String?,
  payerIds: [BearerId],
  beneficiaryIds: [BearerId],
  actor: String,
  committedAt: Time
}

OutcomeReceipt := {
  receiptType: "outcome",
  receiptCause: action_attempt | ambient_observation,
  attemptedActionId: String?,
  performedActionId: String?,
  evaluationRef: String,
  environmentStateBefore: String,
  environmentStateAfter: String,
  consequenceBearerIds: [BearerId],
  bearerObservations: [BearerObservation],
  observedOutcome: String,
  observedAt: Time
}
```

Bearer coverage is a cross-record invariant, not optional metadata. Write
`ids(xs)` for the set of nonempty, unique bearer identifiers in a list and
`keys(m)` for the keys of a bearer map. For every commitment receipt `q`:

```text
E_q := ids(q.evaluation.bearerIds)                    # nonempty and unique
D_q := keys(q.expectedBearerDeltas)
P_q := ids(q.payerIds)
B_q := ids(q.beneficiaryIds)
A_q := ids(q.authorization.envelope.consequenceBearerIds)
       when an envelope or partial envelope supplies that field

D_q = E_q
A_q ⊆ E_q
P_q ⊆ E_q
B_q ⊆ E_q

q.status in {refused, unavailable}
  -> q.attemptedActionId=null and q.expectedOutcome=null
```

No named authorized bearer, payer, beneficiary, or evaluated affected bearer
may disappear by omission from the expected-delta map. For an action-attributed
outcome `r` paired with `q`:

```text
r.evaluationRef = q.evaluation.id
ids(r.consequenceBearerIds) = E_q
set(observation.bearerId for observation in r.bearerObservations)
  = ids(r.consequenceBearerIds)
```

Multiple measures may produce multiple observations for one bearer, but every
named consequence bearer must have at least one observation and no observation
may introduce an unnamed bearer. Ambient observations obey the same internal
`consequenceBearerIds`/`bearerObservations` equality under their own evaluation
reference; they are not linked to a null action as its consequence.

Outcome invariants:

```text
receiptCause=action_attempt     → attemptedActionId is non-null
receiptCause=ambient_observation → attemptedActionId=null
                                   and performedActionId=null
```

An ambient observation is world-facing evidence but not the consequence of a
null action. The cause discriminator prevents the loop from attributing an
unrelated environmental change to `⊥`.

For an attempted action, commitment status is **derived**, never copied from an
unvalidated label:

```text
valid        → authorized_committed
invalid      → unauthorized_attempt
absent       → unauthorized_attempt
not_required → nonconsequential_attempt  # only in NonConsequentialScope
```

Selector and environment are separate interfaces:

```text
χ_t:(X_t,Ω_t,M_t,V_t,U_t,G_t) → (a_t,q_t),  a_t ∈ Action ∪ {⊥}
(X_{t+1},r_{t+1}) ~ K_t(·|X_t,a_t,E_t)  when a_t ∈ Action
(M_{t+1},G_{t+1}) = Loop(M_t,G_t,q_t,r_{t+1})
```

`q_t:CommitmentReceipt`; `r_{t+1}:OutcomeReceipt`. The selector never emits an
outcome receipt. `a_t=⊥` only when no action is attempted because it is
refused or physically unavailable. Invalid or absent authorization is recorded
as `unauthorized_attempt`; if an action is nevertheless attempted, the causal
kernel receives it. A governed channel `χ_t^J` may instead refuse it by policy.
When `a_t=⊥`, `r_{t+1}∈OutcomeReceipt∪{∅}` is either null or has
`receiptCause=ambient_observation`; it is never an action outcome. Including
`G_t` makes the updated selector state load-bearing in the next cycle.

### Model-mediated future influence

```text
M⋆A : ModelState × PhysicallyFeasibleActionField → ActionWeights
```

The public compression `F=M×A` means that a **modeled** future can reweight
present action through an agent. It does not mean the realized future is the
product of model and agency, and it does not assert physical retrocausality.

## 6. Justice and Power-Max types

```text
W_x(T) := ∫₀ᵀ P_x(t)dt

JusticeEnvelope := {
  individual: BearerId,
  whole: BearerId,
  affectedBearerIds: [BearerId],
  eta: 0,
  custody: String,
  consent: ConsentRecord,
  reversibility: String,
  exit: String,
  payerIds: [BearerId],
  beneficiaryIds: [BearerId],
  authorization: AuthorizationEnvelope
}
```

`affectedBearerIds` is a nonempty finite set that includes the focal individual,
the sustaining whole, every payer and beneficiary, and every materially exposed
third party. `payerIds` and `beneficiaryIds` are mandatory and separately
reported even when a party appears in both sets. Justice fails closed if the
coverage is incomplete.

```text
AuthorizedCost(a;p,b) :=
  validAuthorizationForCost(a,p)
  and competentInformedCostConsent(a,p)
  and refusalCarriesNoPenalty(a,p)
  and disclosed(payer=p, beneficiary=b, magnitude, horizon, irreversibility)
  and completeAffectedBearerCoverage(a)
  and noUnconsentedThirdPartyLoss(a,p)

AuthorizedCost^R(q,r;p,b) :=
  authorizationForCostActuallyValid(q,r,p)
  and consentActuallyCovered(q,r,p)
  and evaluationMatchesDisclosedCost(q,r)
  and completeAffectedBearerCoverage(q,r)
  and noUnconsentedThirdPartyLoss(q,r,p)
```

This predicate makes voluntary sacrifice and extraction disjoint when payer
loss and beneficiary gain have been receipted. It deliberately does **not**
imply the ordinary `J` predicate, whose nonnegative frontier would contradict a
voluntary payer loss. It is a narrow, revocable authorization for a declared
cost and never licenses hidden or imposed loss to another bearer.

## 7. Egregoreotype candidate

```text
EgregoreotypeCandidate := {
  id: String,
  persistentSharedTrace: EvidenceRef,
  carrierTurnover: EvidenceRef,
  selectionReweightingIntervention: EvidenceRef,
  recurrentObjectiveLikeBias: EvidenceRef,
  visibleSubstrateCosts: [Cost],
  individual: BearerId,
  whole: BearerId,
  affectedBearerIds: [BearerId],
  etaObserved: Number | unknown,
  custody: String,
  consent: ConsentRecord,
  reversibility: String,
  exit: String,
  payerIds: [BearerId],
  beneficiaryIds: [BearerId],
  authorization: AuthorizationAssessment,
  consciousnessPresumed: false,
  personhoodPresumed: false,
  tier: EvidenceTier,
  killCriterion: String
}
```

Substrate reducibility does not disqualify a candidate. Failure of any of the
five evidentiary conditions does. Candidacy is descriptive: `etaObserved` may
be zero, positive, or unknown, and authorization may be valid, invalid, or
absent. Only a separate Justice or syntropy classification requires `η=0`
and valid accountable authorization.

## 8. Evidence type

```text
EvidenceTier := A | B | S | I | D | C
EvidenceRef  := {sourceId:String, tier:EvidenceTier, locator:String}
BearerId     := String
```

Rosetta projections preserve topology while leaving `tier` unchanged. They
cannot transfer proof between domains.

## Coherence rule

New semantics enter this index before they enter generated topology or public
compression. JSON and SVG artifacts may reference these records; they may not
invent new doctrine.

Canonical sources:

- [Canonical Formula Block](../00_CANONICAL_FORMULA_BLOCK.md)
- [Seven Axioms](00_THE_SEVEN_AXIOMS.md)
- [D4/D5 Canonical Reference](34_D4_D5_CANONICAL_REFERENCE.md)
- [μ-Limit Formula](10_EFR_MU_LIMIT_FORMULA.md)
- [Objective Morals and Ethics](../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md)

*Types are the joints of the compass. If a joint is hidden, the map can move
while pretending it stayed still.*
