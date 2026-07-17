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
DRegister := D0 | D1 | D2 | D3 | D4 | D5 | D6
Modality  := actual | possible
```

| Register | Modality contract | Working content |
|---|---|---|
| `D0` | actual | ground-limit boundary token |
| `D1` | actual | distinction |
| `D2` | actual | configuration |
| `D3` | actual | transformation/persistence |
| `D4` | **actual** | causal actuality, embodied means, performed action, factual record, receipt |
| `D5` | **possible** | counterfactual alternatives, modeled futures, ranking, selection |
| `D6` | actual | apophatic closure boundary token; no positive new freedom |

There are exactly six adjacent crossing identifiers `μ₀…μ₅`. There is no
`μ₆`. The return `r₆:D6↝D0` is an interpretive, non-μ closure edge.

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
  newFreedomOrBoundaryResult: String,
  lowerRegisterRecovery: String,
  reductionStatus: ReductionStatus,
  prediction: String,
  tier: EvidenceTier,
  killCriterion: String
}
```

`μ₅` may record the explicit **no-positive-freedom boundary result** at D6.
Absence of a reducing law maps to `currently_unreduced`, not
`candidate_strong`, unless independent evidence licenses the stronger status.

## 5. Agency, future, and receipt types

```text
ModeledFutureToken := {
  tokenId: String,
  modelId: String,
  representedFutureId: String,
  horizon: Duration,
  assumptions: [String],
  probabilityOrRank: Number?,
  generatedAt: Time
}
```

A model token is a present physical record **about** a possible future. It is
not that future and does not travel backward in time.

```text
OptionCone := {
  agentId: String,
  physicalCausalBoundary: String,
  physicallyAdmissibleHistoryIds: [String],
  modeledHistories: [ModeledFutureToken],
  reachableHistoryIds: [String],
  horizon: Duration,
  costs: [Cost],
  coordinationDependencies: [String],
  authorization: AuthorizationEnvelope
}
```

An option cone is not a physical light cone. Agents with the same spacetime
causal cone can have different option cones. Its defining inclusion is

```text
set(reachableHistoryIds) ⊆ set(physicallyAdmissibleHistoryIds).
```

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
  consequenceBearer: String
}
```

All nine fields are required for consequential commitment.

```text
EvaluationContract := {
  id: String,
  horizon: Duration,
  baselineRef: String,
  measureIds: [String],
  bearerIds: [String],
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
  status: committed | refused | unavailable,
  authorizedActionId: String?,
  performedActionId: String?,
  executionStatus: committed | partial | failed | refused | unavailable,
  authorization: AuthorizationEnvelope,
  selectedOptionId: String?,
  intention: String,
  meansUsed: [String],
  evaluation: EvaluationContract,
  expectedBearerDeltas: {String:Number},
  expectedOutcome: String,
  payer: String,
  beneficiary: String,
  actor: String,
  committedAt: Time
}

OutcomeReceipt := {
  receiptType: "outcome",
  performedActionId: String,
  evaluationRef: String,
  environmentStateBefore: String,
  environmentStateAfter: String,
  consequenceBearer: String,
  bearerObservations: [BearerObservation],
  observedOutcome: String,
  observedAt: Time
}
```

Selector and environment are separate interfaces:

```text
χ_t:(X_t,Ω_t,M_t,V_t,U_t) → (a_t,q_t),  a_t ∈ Action ∪ {⊥}
(X_{t+1},r_{t+1}) ~ K_t(·|X_t,a_t,E_t)  when a_t ∈ Action
(M_{t+1},G_{t+1}) = Loop(M_t,G_t,q_t,r_{t+1})
```

`q_t:CommitmentReceipt`; `r_{t+1}:OutcomeReceipt`. The selector never emits an
outcome receipt. If means, authorization, or admissibility fails, `a_t=⊥` and
`q_t.status∈{refused,unavailable}`; no action transition is submitted to `K_t`,
and `r_{t+1}∈OutcomeReceipt∪{∅}` may be null or separately ambient.

### Model-mediated future influence

```text
M⋆A : ModelState × AdmissibleActionField → ActionWeights
```

The public compression `F=M×A` means that a **modeled** future can reweight
present action through an agent. It does not mean the realized future is the
product of model and agency, and it does not assert physical retrocausality.

## 6. Justice and Power-Max types

```text
W_x(T) := ∫₀ᵀ P_x(t)dt

JusticeEnvelope := {
  individual: String,
  whole: String,
  eta: 0,
  custody: String,
  consent: ConsentRecord,
  reversibility: String,
  exit: String,
  payer: String,
  beneficiary: String,
  authorization: AuthorizationEnvelope
}
```

`payer` and `beneficiary` are mandatory and distinct fields even when the same
party fills both roles.

```text
AuthorizedCost(a;p,b) :=
  J(a;p,b)
  and explicitCostConsent(a,p)
  and disclosed(payer=p, beneficiary=b, magnitude, horizon, irreversibility)

AuthorizedCost^R(q,r;p,b) :=
  J^R(q,r;p,b)
  and consentActuallyCovered(q,r,p)
  and evaluationMatchesDisclosedCost(q,r)
```

This predicate makes voluntary sacrifice and extraction disjoint when payer
loss and beneficiary gain have been receipted.

## 7. Egregoreotype candidate

```text
EgregoreotypeCandidate := {
  id: String,
  persistentSharedTrace: EvidenceRef,
  carrierTurnover: EvidenceRef,
  selectionReweightingIntervention: EvidenceRef,
  recurrentObjectiveLikeBias: EvidenceRef,
  visibleSubstrateCosts: [Cost],
  individual: String,
  whole: String,
  eta: 0,
  custody: String,
  consent: ConsentRecord,
  reversibility: String,
  exit: String,
  payer: String,
  beneficiary: String,
  authorization: AuthorizationEnvelope,
  consciousnessPresumed: false,
  personhoodPresumed: false,
  tier: EvidenceTier,
  killCriterion: String
}
```

Substrate reducibility does not disqualify a candidate. Failure of any of the
five evidentiary conditions does.

## 8. Evidence type

```text
EvidenceTier := A | B | S | I | D | C
EvidenceRef  := {sourceId:String, tier:EvidenceTier, locator:String}
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
