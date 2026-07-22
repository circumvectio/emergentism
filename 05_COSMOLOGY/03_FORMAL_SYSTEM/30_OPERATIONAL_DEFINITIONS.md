---
rosetta:
  primary_level: L5
  primary_column: Methodology
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[D/C]"
  canonical_phrase: "Operational definitions — independent measurement candidates"
title: "Operational Definitions — Independent Measurement Candidates"
status: "ACTIVE WORKING SURFACE — no validated instrument"
evidence_tier: "[D] protocol design; [C] construct hypotheses; [B] only after external result custody"
date_repaired: 2026-07-21
original_git_blob: ebd11c6b6fcc168b268567306dce6ce648f1ff71
---

# Operational Definitions — Independent Measurement Candidates

This file proposes measurement contracts. It does not own notation, establish a
world law, or promote any claim. The
[Canonical Formula Block](../00_CANONICAL_FORMULA_BLOCK.md) owns the symbols.

## 1. Type firewall

| Type | Symbols | Meaning |
|---|---|---|
| reciprocal chart | `φ,ν,θ,B,P∞` | analytic coordinates and functions on a selected chart |
| finite node | `Φ,V,P_node` | D5 option-field quality/foresight, D4 usable means, and a selected conjunctive score |
| estimates | `Φ̂,V̂` | outputs of independently specified instruments |

`φν=1` is true by definition on the chart. It is not an empirical hypothesis
and cannot be “confirmed” by measuring `Φ̂,V̂`. Conversely, `Φ̂V̂≈1` is not a
chart identity. If proposed in a normalized domain, it is an ordinary empirical
hypothesis about two node variables and must compete with rivals.

The old surface mixed an uppercase foresight estimate with a lowercase chart
coordinate, then selected reciprocal pairs before testing reciprocity. That made
the result true by construction. The seam is closed here.

## 2. Candidate `Φ̂` instruments `[D/C]`

`Φ` means the quality of an actually carried D5 option field: how well a system
models, distinguishes, ranks, and updates action-relevant alternatives. It is
not generic intelligence, eloquence, coherence, or consciousness.

### A. Held-out future-model score

For a preregistered event partition `Ω`, forecast distribution `p`, realized D4
outcome `y`, and proper scoring rule `S`:

```text
raw_Φ = S(p,y)
Φ̂_A = normalize_holdout(raw_Φ) ∈ [0,1].
```

The normalization, baseline forecaster, horizon, event partition, and missing
outcome policy must be frozen before evaluation. A proper score measures
forecast quality; it does not by itself measure whether the alternatives were
useful for action.

### B. Counterfactual-discrimination score

Hold the D4 state and means fixed; intervene on represented alternatives or
their weights. Estimate whether the system changes present selections in the
direction predicted by its declared ranking:

```text
Φ̂_B = held_out_discrimination(intervention → selection) ∈ [0,1].
```

This candidate is closest to the D4/D5 type contract, but ordinary planning,
control, and learning are mandatory rivals.

### C. Perturbation/update score

After a bounded surprise, measure calibration recovery and model revision on
held-out observations. A declared monotone map normalizes the result to
`[0,1]`. Stability without accurate updating does not count as foresight.

No candidate is canonical. Every use of `Φ̂` must name its candidate, construct
validity evidence, uncertainty interval, population, horizon, and failure mode.

## 3. Candidate `V̂` instruments `[D/C]`

`V` means D4 usable means for a declared action set—not wealth, force, or raw
capacity in the abstract.

### A. Feasible-action fraction

For a preregistered action set `A` and actual means state `x`:

```text
V̂_A(x) = |{a∈A : Feasible(a,x)}| / |A|.
```

The action enumeration and feasibility predicate must be fixed independently of
the observed outcome.

### B. Costed enactment capacity

For standardized tasks, estimate the share successfully attempted within the
declared physical resource and time envelope. Report cost and failure
separately. Authorization `U` and safety admissibility are independent typed
gates: an unauthorized act may still be physically feasible and therefore may
count toward `V̂`, while remaining prohibited from commitment.

Every use of `V̂` must name the action set, physical resource boundary, bearer
costs, and uncertainty interval. Report authorization/consent and safety as
separate variables; never build them into the `V̂` instrument.

## 4. Derived node diagnostics

The declared Emergentist product is

```text
P̂_node = Φ̂V̂.
```

This is a model output, not proof that product is the correct aggregator. Test
it on held-out outcomes against at least additive, minimum, harmonic, and a
preregistered asymmetric/CES or Cobb–Douglas rival.

For `(Φ̂,V̂)≠(0,0)`, a scale-free ratio-balance diagnostic may be declared:

```text
B̂_ratio = 2Φ̂V̂ / (Φ̂²+V̂²).
```

`B̂_ratio≤1`, with equality at `Φ̂=V̂`, is an analytic fact about this selected
diagnostic. It is not the chart's `B=sinθ` unless an explicit, independently
validated map to the chart is supplied. At `(0,0)` the ratio is undefined; a
domain may separately assign a reporting convention, but not an analytic value.

## 5. Extraction and justice measurements

There is no context-free universal `η` meter. A study must identify:

1. affected bearer set;
2. resource or option being depleted;
3. counterfactual baseline;
4. payer and beneficiary;
5. custody, consent, reversibility, and exit; and
6. time horizon and uncertainty.

Only then may it define a nonnegative extraction statistic `η_domain`. The
normative constraint `η_domain=0` is a declared Justice condition, not an
empirical theorem and not sufficient for justice by itself.

## 6. Testing model-mediated future influence

The operational D5 test is not a regression of `Φ̂−V̂` toward zero. It is an
intervention:

```text
change represented future content/weights
hold current D4 state and usable means fixed as far as possible
measure the change in the present selection distribution
compare against reactive-policy, learning, demand, and experimenter-cue rivals.
```

A positive result supports a model-mediated effect in that domain. It does not
show physical retrocausality or a fifth interaction. The strong F5 claim needs a
preregistered residual discriminator that ordinary anticipation and control do
not explain.

## 7. Evidence and kill contract

- Protocol code and a passed internal test are `[D/S]` method facts, not worldly
  validation.
- A result with declared data custody is `[B]`; its interpretation remains
  separately `[I/C]`.
- Formal bounds are `[A/S]` only inside named assumptions.
- Construct invalidity kills the instrument.
- Product losing to a fair rival kills product fit in that domain.
- Selecting reciprocal pairs and then reporting reciprocal symmetry kills the
  study as circular.
- No evidence type silently upgrades another.

The [External Component
Calibration](../../03_METHODOLOGY/00_EXTERNAL_COMPONENT_CALIBRATION_2026_07_20.md)
records the current absence of external validation.
