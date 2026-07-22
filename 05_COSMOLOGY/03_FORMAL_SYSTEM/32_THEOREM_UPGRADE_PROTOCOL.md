---
rosetta:
  primary_level: L5
  primary_column: Methodology
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "Claim upgrade protocol — evidence types do not ladder silently"
title: "Claim Upgrade Protocol"
status: "ACTIVE KINTSUGI SUCCESSOR"
evidence_tier: "[S] procedural contract; claims retain their own evidence types"
date_repaired: 2026-07-21
original_git_blob: 144a4fe25921824593c037736993fe72ac91831f
---

# Claim Upgrade Protocol

This protocol changes a claim's standing only when new evidence of the right
type exists. `[A/B/S/I/D/C]` are evidence types, not rungs on a single prestige
ladder.

## 1. Claim packet

Every proposed change supplies:

```text
ClaimPacket = {
  id, exact proposition, variable types, domain, assumptions,
  current evidence type, proposed evidence type,
  derivation or result custody, serious rivals,
  prediction, kill criterion, affected owners
}
```

No summary, Rosetta row, receipt, visualization, or passing unit test may
upgrade the source owner by itself.

## 2. Evidence-type rules

| Type | Required warrant |
|---|---|
| `[A]` | checked analytic proof/counterproof inside explicit assumptions |
| `[B]` | dated observation/result with provenance, method, and custody |
| `[S]` | structural consequence of declared definitions or architecture |
| `[I]` | explicitly defeasible interpretation/crosswalk |
| `[D]` | proposal not yet adopted or tested |
| `[C]` | open conjecture with a real kill criterion |

A claim may carry more than one type on separable clauses. For example, a
formal product bound can be `[A]`, a measured dataset `[B]`, and the proposed
world interpretation `[I/C]`. These warrants do not merge automatically.

## 3. Lyapunov discipline

For a declared dynamical system

```text
ẋ=f(x),
```

a differentiable function `L` is a Lyapunov candidate until the domain,
equilibrium set, regularity, and sign condition are proved. A Lyapunov result
requires at least

```text
L(x)≥0,
L(x*)=0,
L̇(x)=∇L(x)·f(x)≤0
```

on the declared domain; asymptotic claims need the corresponding strictness or
invariance argument. Therefore `H(φ)=φ+1/φ` has a minimum at `φ=1` `[A]`, but it
is **not** “the Lyapunov function for F5” until an F5 flow is specified and
`Ḣ≤0` is proved. Before that it is a candidate objective/potential only.

## 4. Noncircular empirical workflow

1. Freeze independent operational definitions and notation.
2. Preregister population, intervention, horizon, exclusions, metric, rivals,
   and decision rule.
3. Separate training/calibration data from held-out evaluation.
4. Record commitment and world-issued outcome receipts separately.
5. Report nulls and negative controls.
6. Update only the proposition actually tested.

Defining `V̂:=1/Φ̂` and then observing `Φ̂V̂=1` is a chart construction, not an
empirical result.

## 5. Worked example: product fit

Suppose `Φ̂,V̂∈[0,1]` are measured independently under the
[Operational Definitions](30_OPERATIONAL_DEFINITIONS.md). The conjecture is not
that their product must equal one. It is:

> In a frozen domain, `Φ̂V̂` predicts a held-out outcome better than declared
> additive, minimum, harmonic, and asymmetric/CES or Cobb–Douglas rivals.

The result receives `[B]` custody. Product's zero-boundary and monotonicity
remain `[S]` model properties. A claim of universal product fit remains `[C]`
and is not upgraded by one domain.

## 6. Adoption and rollback

- Update the semantic owner first.
- Record contradictions and supersessions explicitly.
- Propagate only after owner tests pass.
- A failed discriminator restores the prior standing or kills the scoped claim;
  it cannot be reinterpreted as support without a new preregistered study.
- Historical text remains recoverable; it does not compete with the successor.

The predecessor remains recoverable at Git blob
`144a4fe25921824593c037736993fe72ac91831f`.
