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
status: "CANONICAL SCHEMA INDEX — subordinate to per-register semantic owners; Kintsugi repair 2026-07-21."
evidence_tier: "[A] analytic types; [I] selected model records; [C] empirical and strong-emergence hypotheses."
supersedes_blob: "178eac8942c2d3c6c01cada8d37b0007d43e0832"
---

# Primitives and Type Signatures

This file is the closed **schema index** for the repaired Emergentist Compass.
It does not own the meaning of D0, D1, or D2: the Titan canon and the dedicated
D1/D2 owners do. It does not turn an interpretation into a theorem. A symbol or
record used with a different type is a defect unless the semantic owner and
this schema are deliberately revised together.

## 1. Mathematical chart types

| Primitive | Type | Meaning |
|---|---|---|
| `TitanFrame` | opaque sum type `0_T \| 1_T \| ∞_T` | sovereign metaframe terms used to describe D0/D1/horizon roles; no arithmetic, implicit numeric coercion, or claim of three internal D0 states |
| `render_T` | `TitanFrame→Glyph` | renders the three terms as `0`,`1`,`∞` without changing their type |
| `UnitSeed` | singleton set `U={★}` | chosen nonempty representative with cardinality `1_N`; not Titan `1_T` |
| `SignedUnit_N` | `{+1_N,-1_N}` | selected oriented unit-magnitude pair opening the D1 signed spine |
| `ℕ⁺` | positive finite cardinals `{1_N,2_N,…}` | finite multiplicities of `UnitSeed`; excludes numeric zero |
| `SignedMagnitude` | `{+,-}×ℕ⁺` | tagged construction of oriented positive magnitudes; does not presuppose `ℤ` |
| `ℤ_•` | `image(embed)=ℕ⁺ ⊎ (-ℕ⁺)=ℤ\{0_N}` | image of `SignedMagnitude` in standard `ℤ`; multiplicatively closed but not addition-closed |
| `ℤ` | `ℤ_•∪{0_N}` | standard additive completion of the signed spine |
| `ℚ^×,ℝ^×` | `ℚ\{0_N},ℝ\{0_N}` | nonzero multiplicative sectors; distinct from the ambient fields `ℚ,ℝ` |
| `0` | number | additive identity and ordinary operand |
| `1` | number | multiplicative identity and ordinary operand |
| `∞_P` (usually printed `∞`) | projective point | point at infinity in `ℂP¹`; not a largest number |
| `•,⊙,○` | Titan emblems | alternate renderings of `0_T,1_T,∞_T`; `[I]`, not arithmetic |
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

### Sovereign-frame type law

```text
TitanFrame := 0_T | 1_T | ∞_T
TitanFrame ↛ Number
ArithmeticSignature(TitanFrame)=∅
add_T, sub_T, mul_T, div_T, pow_T, log_T : undefined
```

`TitanFrame` is a metaframe vocabulary, not a three-state carrier inside D0.
The object-level D0 role remains opaque and has no positive freedom. The
distinctions among the three written constructors are distinctions in the
describing language; `μ₀` names the first positive object-level aperture.

`0_T/1_T`, `1_T/1_T`, `∞_T/1_T`, and `0_T×∞_T` are therefore inadmissible
terms, not exceptional arithmetic values. The ordinary number type retains
its lawful identity operations, including `x+0=x`, `x·1=x`, and `x/1=x`;
projective `∞_P` occurs only in an explicitly named extension. A shared printed
glyph never supplies an implicit coercion.

The D1 signed, positive-first presentation is likewise explicit:

```text
1_N:=|{★}|
n_N:=|⊔_{k=1}^n {★}_k|, n≥1
ℕ⁺:={n_N|n≥1}
SignedUnit_N:={+1_N,-1_N}
SignedMagnitude:={+,-}×ℕ⁺
embed(+,n)=n; embed(-,n)=-n
ℤ_•:=image(embed)=ℕ⁺⊎(-ℕ⁺)=ℤ\{0_N}
(+1_N)+(-1_N)=0_N∉ℤ_•
0_N:=|∅|; ℤ:=ℤ_•∪{0_N}
ℚ^×:=ℚ\{0_N}; ℝ^×:=ℝ\{0_N}
```

Thus `1_T≠1_N`, `0_N∉ℕ⁺`, `0_N∉ℤ_•`, and `μ₀` supplies no coercion
between the frame and number registers. `ℤ_•` is a useful nonzero set, not an
additive group; standard `ℤ`, `ℚ`, and `ℝ` retain zero wherever their additive
structure requires it. “Multiple of one” means repeated addition/disjoint union;
products of the unit alone do not generate the other naturals.

## 2. D-register roles and token modality

Registers are cumulative predicates/semantic roles, not seven disjoint
substances. Token modality is typed separately:

```text
DRegister := D0 | D1 | D2 | D3 | D4 | D5 | D6
RegisterRole :=
  ground_boundary | positive_structure | probability_bearing_state | actual_event
  | possible_content | exit_boundary
TokenModality := actual | merely_possible
```

| Register | Register role | Working content |
|---|---|---|
| `D0` | ground boundary | no positive freedom; an inscription of the role is a D4 actual token |
| `D1` | positive structure | distinguishability predicate |
| `D2` | positive structure | configurational/relational predicate |
| `D3` | probability-bearing state | quantum state assignment `ρ`; outcome distributions arise only relative to a measurement context |
| `D4` | **actual event** | causal actuality, embodied means, present models, performed ranking/selection, action, factual record, receipt |
| `D5` | **possible content** | merely possible counterfactuals, alternative relations, modeled-future referents, selection candidates |
| `D6` | exit boundary | no positive freedom; an act of recognition/exit is a D4 actual event |

An actual D4 carrier may realize D1 and D2 and, where the quantum description
applies, instantiate or be modeled by a D3 state assignment:

```text
realizes : ActualCarrier × RegisterPredicate → Boolean
D4_actual(x) -> may(realizes(x,D1) and realizes(x,D2) and realizes(x,D3))
```

This cumulative relation expresses dependency without claiming that lower
predicates completely explain the higher event.

### QuantumState and measurement context

```text
QuantumState := {
  systemRef:String,                # declared individuation boundary
  hilbertSpaceId:String,
  densityOperator:ρ,
  positiveSemidefinite:true,
  trace:1,
  rank:PositiveInteger | InfiniteRank,
  register:D3,
  role:probability_bearing_state
}

POVM := {
  effects:[E_k],
  eachPositive:true,
  sumIdentity:true,
  register:D2
}
Born(ρ,POVM)(k) := Tr(ρE_k)

Observable := {
  systemRef:String,
  operatorRef:String,
  selfAdjoint:true,
  domainRef:String,
  register:D2
}

CanonicalPair := {
  left:Observable,
  right:Observable,
  commonDomainRef:String,
  commutatorRef:String
}

StateConditionedDistribution := {
  stateRef:QuantumState,
  measurementRef:POVM | Observable,
  probabilities:ProbabilityDistribution,
  register:D3
}

QuantumInstrument := {
  outcomes:[k],
  operations:[I_k],
  eachCompletelyPositive:true,
  eachTraceNonIncreasing:true,
  sumTracePreserving:true,
  register:D2
}

D4StateAssignmentRecord := {
  recordId:String,
  runId:String,
  preparationRef:String,
  stateContentRef:QuantumState,
  method:String,
  preparationEvidenceRefs:[String],
  actorOrApparatus:String,
  timestamp:Time,
  custody:String,
  register:D4,
  modality:actual
}

D4MeasurementRecord := {
  recordId:String,
  runId:String,
  preparationRef:String,
  stateContentRef:QuantumState,
  instrumentRef:QuantumInstrument,
  outcomeId:String,
  assignedProbability:Probability,
  apparatus:String,
  timestamp:Time,
  custody:String,
  provenance:[String],
  register:D4,
  modality:actual
}

D3StateEntropy := {
  stateRef:QuantumState,
  value:-Tr(ρ log ρ),
  register:D3
}

D4MomentumTransferReceipt := {
  recordId:String,
  runId:String,
  deltaMomentum:Quantity,
  clockRef:String,
  interactingSystems:[String],
  provenance:[String],
  custody:String,
  register:D4,
  modality:actual
}

D4EntropyProductionReceipt := {
  recordId:String,
  processRef:String,
  clockInterval:Interval,
  coarseGrainingRef:String,
  deltaEntropy:Quantity,
  provenance:[String],
  custody:String,
  register:D4,
  modality:actual
}
```

The D3 state content `ρ` is not one freestanding classical distribution. It
generates a distribution only jointly with a declared measurement. Its actual
written or laboratory assignment is a `D4StateAssignmentRecord`; a performed
preparation, interaction, outcome, or provenance-bearing record is likewise
D4. D5 remains agent-represented counterfactual content and is not quantum
branch space. The full contract is owned by
[D3 Quantum State](44_D3_QUANTUM_STATE_REGISTER.md).

There are exactly five positive-freedom crossing identifiers `μ₀…μ₄`. There
is no `μ₅` or `μ₆`. The exit-marker edge `b₆:D5↝D6` and return
`r₆:D6↝D0` are interpretive and non-μ.

`actual` and `merely_possible` are token-modality tags in this modeling grammar,
not exhaustive predicates of ordinary modal logic. Representation may refer to
either a merely possible alternative or an alleged actual historical event:

```text
ActualRepresentation := {register:D4, modality:actual, recordId:String}
AlternativeContent   := {register:D5, modality:merely_possible, contentId:String}
HistoricalClaim      := {claimId:String, allegedTime:Time}
HistoricalEvent      := {register:D4, modality:actual, eventId:String}
RepresentedReferent  := AlternativeContent | HistoricalClaim

represents : ActualRepresentation → RepresentedReferent
refersTo   : HistoricalClaim → HistoricalEvent       # only if independently warranted
```

The physical production of a model, memory, ranking, or selection is a D4
event. Counterfactual referents and orderings are D5 content; a veridical memory
may instead refer to a past D4 event through a HistoricalClaim. Representation
alone proves neither veridicality nor actuality. Graph exports retain the short
label `possible` for schema compatibility, but it means `merely_possible`
wherever a D5 element is typed.

```text
MemoryToken := {
  register:D4,
  modality:actual,
  representationId:String,
  salienceByAgent:Map[AgentId,NonNegativeReal]
}

Salience(x,agent) > Salience(y,agent)
  does not entail x is dependency-prior, more actual, or better evidenced
```

## 3. Finite-node model types

```text
Φ : Node×Time → [0,1]       # D4-evaluated score of capacity concerning D5 option content
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
  id: μ₀ | μ₁ | μ₂ | μ₃ | μ₄,
  source: DRegister,
  target: DRegister,
  triggerType: origin_aperture | saturation_candidate,
  saturatedRegister: DRegister | null,
  saturationEvidence: [EvidenceRef],
  evidenceStatus: not_applicable | supplied | not_yet_supplied,
  newFreedom: String,
  lowerRegisterRecovery: String,
  reductionStatus: ReductionStatus,
  prediction: String,
  tier: EvidenceTier,
  killCriterion: String
}
```

Invariants:

```text
μ₀.triggerType = origin_aperture
μ₀.saturatedRegister = null
μ₀.evidenceStatus = not_applicable
μ₁…μ₄.triggerType = saturation_candidate
μ₁…μ₄.saturatedRegister = source
for μ₁…μ₄: evidenceStatus = supplied iff saturationEvidence is nonempty
for μ₁…μ₄: evidenceStatus = not_yet_supplied iff saturationEvidence = []
```

The current internally coherent but externally uncalibrated scaffold
instantiates `μ₀` with `saturationEvidence=[]` and
`evidenceStatus=not_applicable`; `μ₁…μ₄` have `saturationEvidence=[]` and
`evidenceStatus=not_yet_supplied`. Descriptions, predictions, and kill criteria
are not evidence for their own crossings.

`b₆` records the selected **no-positive-freedom boundary result** at D6 and is
not a `MuCrossing`. Absence of a reducing law maps to `currently_unreduced`, not
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
set(token.representedAlternative.contentId for token in modeledHistories)
  ⊆ set(physicallyAdmissibleHistoryIds)
set(authorizedHistoryIds) ⊆ set(physicallyReachableHistoryIds).
```

Physical reachability and authorization are deliberately separate. An agent
may be able to model and physically attempt an unauthorized option; that option
is not thereby just or permitted.
Impossible, incoherent, or physically forbidden fantasies may still be stored
as model tokens, but they remain outside `OptionCone.modeledHistories` and
cannot enter its reachable or authorized subsets.

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

All nine fields are required for a **valid accountable authorization**, but
completeness is necessary rather than sufficient. Their absence or invalidity
does not make an action physically impossible.

```text
AuthorizationStatus := valid | invalid | absent | not_required

AuthorizationAssessment :=
  | {status:valid,
     envelope:AuthorizationEnvelope,
     reasons:[]}
  | {status:invalid,
     envelope:AuthorizationEnvelope | Partial<AuthorizationEnvelope>,
     reasons:NonEmpty[String]}
  | {status:absent,
     envelope:null,
     reasons:NonEmpty[String]}
  | {status:not_required,
     envelope:null,
     reasons:[],
     scope:NonConsequentialScope}
```

Authorization is assessed against an attempted action, evaluation time, and
complete consequence-bearer set:

```text
AuthorizationValid(e,a,t,B) :=
  Complete(e)
  and PrincipalHasAuthority(e.principal,e.mandate,t)
  and ActionWithinMandateAndScope(a,e.mandate,e.scope)
  and ActorMatches(a,e.actor)
  and ConsentValidAndCurrent(e.consent,a,t)
  and CustodyValid(e.custody,a,t)
  and NotExpiredOrRevoked(e.expiryOrRevocation,t)
  and ContestPathAvailable(e.contestPath,t)
  and set(e.consequenceBearerIds)=B

assessAuthorization(e?,a,t,B) -> AuthorizationAssessment
```

The governed selector may fail closed on `invalid|absent`; the descriptive
causal loop must still represent unauthorized, coerced, accidental, or
criminal attempts and their consequences.

The union is validated before a receipt is emitted. `valid` is inhabited only
when `AuthorizationValid` holds. A complete but expired, revoked, out-of-scope,
actor-mismatched, nonconsensual, uncustodied, uncontestable, or bearer-incomplete
envelope is `invalid`. `invalid` requires a supplied record and at least one
defect. `absent` requires no envelope and at least one reason.
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
  attemptStatus: submitted | refused | unavailable,
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
  coverageDriftBearerIds: [BearerId],
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
q.authorization.status = valid -> A_q = E_q
q.authorization.status = invalid -> A_q ⊆ E_q when a partial field exists
P_q ⊆ E_q
B_q ⊆ E_q

q.status in {refused, unavailable}
  -> q.attemptedActionId=null and q.expectedOutcome=null
```

No named authorized bearer, payer, beneficiary, or evaluated affected bearer
may disappear by omission from the expected-delta map. A valid consequential
authorization must cover the complete evaluated bearer set; a partial subset
can only be recorded as invalid. For an action-attributed outcome `r` paired
with `q`:

```text
r.evaluationRef = q.evaluation.id
R_r := ids(r.consequenceBearerIds)
E_q ⊆ R_r
ids(r.coverageDriftBearerIds) = R_r \ E_q
set(observation.bearerId for observation in r.bearerObservations) = R_r
unique((observation.bearerId,observation.measureId)
       for observation in r.bearerObservations)

R_r \ E_q != empty
  -> RetrospectiveAuthorizationCoverage(q,r)=invalid
     and J^R(q,r)=false
```

Multiple measures may produce multiple observations for one bearer; uniqueness
is by `(bearerId,measureId)`, not by bearer alone. Every named consequence
bearer must have at least one observation and no observation may introduce an
unnamed bearer. An unforeseen bearer is added to `R_r` and `coverageDriftBearerIds`
rather than hidden or used to reject the evidence receipt. The original
prospective authorization status remains part of history, but it no longer
satisfies retrospective authorization coverage or Justice. Ambient observations obey the same internal
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
physicalAvailability=unavailable and no attempt → unavailable
governed refusal and no attempt                  → refused
valid + submitted Action                         → authorized_committed
invalid or absent + submitted Action             → unauthorized_attempt
not_required + submitted Action                  → nonconsequential_attempt
                                                   # only in NonConsequentialScope
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

AsymmetricCostTransfer^R(q,r;p,b) :=
  Delta^R_T W_b(q,r) > 0 and Delta^R_T W_p(q,r) < 0

Extraction^R(q,r;p,b) :=
  AsymmetricCostTransfer^R(q,r;p,b)
  and not AuthorizedCost^R(q,r;p,b)

VoluntarySacrifice^R(q,r;p,b) :=
  AsymmetricCostTransfer^R(q,r;p,b)
  and AuthorizedCost^R(q,r;p,b)
```

These predicates make voluntary sacrifice and extraction disjoint when payer
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

```text
invariant:
  visibleSubstrateCosts is NonEmpty[Cost]
  affectedBearerIds is NonEmpty Unique[BearerId]
  payerIds and beneficiaryIds are Unique[BearerId]
  every payerId and beneficiaryId belongs to affectedBearerIds
  every visible cost names at least one payer and one affected bearer
```

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
- [Emergent Axioms E1–E10](../../06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md)
- [Emergent Axioms — current owner](../../06_ONTOLOGY/03_THE_EMERGENT_AXIOMS.md); A1–A7 survive only as superseded genealogy
- [D4/D5 Canonical Reference](34_D4_D5_CANONICAL_REFERENCE.md)
- [μ-Limit Formula](10_EFR_MU_LIMIT_FORMULA.md)
- [Objective Morals and Ethics](../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md)

*Types are the joints of the compass. If a joint is hidden, the map can move
while pretending it stayed still.*
