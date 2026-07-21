---
title: "Power-Max — Justice-Constrained Objective"
status: "ACTIVE FORMAL OWNER — dimension-first Kintsugi repair 2026-07-21"
date: 2026-07-21
evidence_tier: "[A/S] optimization facts under declared assumptions; [I] selected objective and Justice envelope; [C] empirical adequacy"
supersedes_blob: "4154ebeb1637a11b3bca40f0cca0425b226f849c:05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md"
---

# Power-Max — Justice-Constrained Objective

Power-Max is Emergentism's transparent action objective. It is not a theorem
that every agent in nature maximizes power, and it does not derive morality
from arithmetic. The optimization becomes meaningful only after the bearer,
horizon, measure, feasible actions, uncertainty model, and Justice constraints
have been declared.

## 1. Durable potential

For bearer `x` over horizon `T`, define a declared nonnegative potential score
`P_x(t)` and its durable integral:

```text
W_x(T) = ∫₀ᵀ P_x(t) dt.
```

When the finite-node product is selected,

```text
P_x(t) := P_node,x(t) = Φ_x(t)V_x(t),
```

where `Φ` is a present D4 assessment concerning D5 option-field quality or
foresight and `V` is D4 usable means. The product is one declared normalized
conjunctive model, not a uniquely forced world law. A different validated
potential model may be substituted if its type and evidence are explicit.

## 2. Justice-admissible actions

Let `i` be the acting individual, `H` the sustaining whole, and `B(a)` the
complete materially affected bearer set for action `a`. Define:

```text
A_J = {a :
  J(a;i,H,B(a))
  and Δ_T W_i(a) ≥ 0
  and Δ_T W_H(a) ≥ 0
  and no bearer in B(a) is hidden or destroyed by aggregation
}.
```

`J` requires at least:

- a complete and valid `AuthorizationEnvelope` for consequential exposure;
- named actors, payers, beneficiaries, and consequence bearers;
- consent, custody, contest, revocation, reversibility, and exit where
  applicable;
- no hidden extraction or compensating aggregate that erases a harmed side;
- physically admissible means and honest uncertainty.

Justice defines the feasible field. Maximization does not create or justify
that field.

## 3. The selected objective

```text
a* ∈ argmax_(a∈A_J) E_(M_t)[W_i(T) | a].
```

This is a conditional design rule. If `A_J` is empty, it licenses no action.
If the maximum is not attained, use a declared `ε`-optimal action only when a
finite supremum exists and the Justice constraints still hold. Model
uncertainty and distributional harms must remain visible.

The mathematical statement “`a*` maximizes the declared objective over
`A_J`” is analytic once the model is fixed. The choices of `W`, `J`, boundary,
horizon, and admissible actions are normative/modeling commitments `[I]` and
their usefulness in the world is conjectural `[C]`.

## 4. What coupling proves—and does not prove

For a toy coupled network,

```text
V_eff(i)=(1-λ)V_i+λ<V>,  0<λ≤1
P_eff(i)=Φ_i V_eff(i),
∂P_eff(i)/∂V_j=λΦ_i/N > 0.
```

The positive cross-partial proves monotone interdependence **inside that
model**. It does not prove cooperation is optimal. In a one-shot zero-sum
transfer `ΔV` from `j` to `i`, the mean `<V>` is unchanged and, for `λ<1`,

```text
ΔP_eff(i)=Φ_i(1-λ)ΔV > 0.
```

Extraction can therefore benefit the extractor locally. This counterexample
is load-bearing: non-extraction cannot be inferred from coupling, the product,
evolution, or rational self-interest. It is enforced by the Justice-admissible
field and then tested for long-run consequences.

## 5. Syntropic Dyadism

With all bearer and Justice conditions still explicit:

```text
Moral(a)
  iff Δ_T W_H(a)>0 and Δ_T W_i(a)≥0 and J(a;i,H,B(a))

Ethical(a)
  iff Δ_T W_i(a)>0 and Δ_T W_H(a)≥0 and J(a;i,H,B(a))

Syntropic(a)
  iff Δ_T W_i(a)>0 and Δ_T W_H(a)>0 and J(a;i,H,B(a)).
```

The arrows are mnemonic:

```text
morals: i → H
ethics: H → i
strict syntropy: i ↔ H, both durable potentials rise
```

Aggregate gains never compensate for destroying one side. The whole is not
licensed to consume the individual, and the individual is not licensed to
consume the whole.

## 6. Sacrifice

Voluntary sacrifice is a distinct costly class. It requires informed consent,
visible payer and beneficiary, revocability until the irreversible threshold,
and a valid authorization envelope. Because the payer's measured potential may
fall, it is not strict syntropy and may never be demanded as proof of morality,
loyalty, or collective worth.

## 7. Relation to the option cone

Power-Max operates only inside physically admissible and authorized option
cones. “Maximize the cone” is therefore shorthand for:

> prefer durable mutual option widening among declared bearers, under physical
> cost, accountable authorization, non-extraction, custody, contest, and exit.

It is not a universal law of agency, a warrant for domination, or a claim that
cognition enlarges the relativistic light cone.

## 8. Acceptance and kill criteria

The model must distinguish at least:

1. lawful preservation with no strict gain;
2. strict syntropy;
3. a hidden aggregate gain that harms one bearer;
4. voluntary sacrifice;
5. a one-shot extraction that benefits the extractor;
6. an empty Justice-admissible action set.

Reject or revise Power-Max for a domain if its declared potential measure is
not identifiable, if a simpler rival predicts receipts better, if boundary or
horizon choices manufacture the result, or if the Justice screen repeatedly
hides real payers or harms. A failed empirical fit does not invalidate the
analytic optimization statement; it invalidates the model's use for that
domain.

## Read with

- [Canonical Formula Block](../00_CANONICAL_FORMULA_BLOCK.md)
- [Objective Morals and Ethics](../../04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md)
- [D4/D5 Canonical Reference](34_D4_D5_CANONICAL_REFERENCE.md)
- [Primitives and Type Signatures](29_PRIMITIVES_AND_TYPE_SIGNATURES.md)

*First define what no optimization may consume. Then optimize honestly inside
what remains.*
