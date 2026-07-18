---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S/C]"
  canonical_phrase: "η=0 — degenerate Model-A theorem; enforcement hypothesis elsewhere"
status: "ACTIVE KINTSUGI REPAIR — Model A/B retained; Three-Gates theorem retired"
date: 2026-07-19
superseded_blob: "130413a08dd63bdca57f6e47b813887bff88bdb4"
---

# `η=0` in Two Explicit Games

> **[金] Crack:** the former working paper correctly separated a no-private-gain
> Model A from a private-side-payment Model B, but then claimed that an
> under-specified “Three Gates” mechanism restored a unique Nash equilibrium and
> was DSIC iff a local derivative bound held. The exit payoff and simultaneous
> transition were undefined; a condition at zero cannot prove a unique global
> optimum; and the stated derivative inequality was not the claimed iff.
>
> **Repair:** preserve the two bounded results and retire the mechanism theorem.
> The complete prior paper remains at Git blob
> `130413a08dd63bdca57f6e47b813887bff88bdb4`.

## 1. Common setup

Let `N≥2`, each scalar action satisfy `η_i≥0`, and

```text
E(η) = sum_i η_i
B(E) = cos(f(E))
```

where `f:[0,∞)→[0,π/2)` is strictly increasing, differentiable where a
derivative is used, and `f(0)=0`. This is a declared payoff fixture. Writing
`B=sin(θ)` with `θ=π/2−f(E)` is only a reparameterization; sphere geometry does
not independently create an incentive or enforcement mechanism.

## 2. Model A: no private benefit `[S]`

Define every player's payoff by

```text
u_i^A(η) = B(E(η)).
```

For any fixed `η_{−i}`, increasing `η_i` strictly increases `E`; strict
monotonicity of `f` and strict decrease of `cos` on `[0,π/2)` strictly lower
`u_i^A`. Therefore `η_i=0` strictly dominates every `η_i>0`, and
`η=(0,…,0)` is the unique Nash equilibrium.

This theorem is intentionally degenerate: the action called “extraction” has
no private benefit at all. It proves neither cooperation in a real commons nor
that `η=0` enforces itself.

## 3. Model B: a private side-payment breaks the result `[S]`

Let `0<δ<1`, let `g` be differentiable near zero with `g'(0)>0`, and define

```text
u_i^B(η) = (1−δ)B(E(η)) + δ g(η_i).
```

At the all-zero profile,

```text
∂u_i^B/∂η_i = −(1−δ) sin(f(0)) f'(0) + δ g'(0)
             = δ g'(0) > 0.
```

Thus `η_i=0` is not even a local best response at that profile; all-zero is not
a Nash equilibrium. This is the corpus's bounded Power-Max extraction
counterexample: once a private capture channel is admitted, unconstrained local
maximization can reward extraction.

## 4. Enforcement remains a design hypothesis `[C]`

Receipts can improve observability, penalties can change payoffs, and Grace
Exit can limit custody. None automatically yields global dominance, budget
balance, DSIC, or a unique equilibrium. A future mechanism claim must specify:

1. action spaces and timing;
2. simultaneous transition and conflict resolution;
3. what is observed, by whom, and with what error;
4. the complete penalty function and payer/beneficiary flows;
5. exit timing, post-exit assets, and residual payoffs;
6. authorization, consent, custody, contest, and reversibility;
7. equilibrium concept and complete proof; and
8. comparisons with simpler enforcement and repeated-game rivals.

A derivative bound at `η=0` is at most local. It is not an iff for global
dominance. “Truth-telling” is also not synonymous with choosing `η=0` unless a
separate type/reporting mechanism is defined.

## 5. Justice boundary

Even a valid equilibrium theorem would describe incentives, not morality.
`η=0` is a necessary non-extraction fence in the Emergentist Justice envelope,
not a sufficient moral verdict. Commitment and outcome receipts must expose
every bearer, payer, beneficiary, authorization, and consequence.

## Kill criteria

- Model A fails if a positive `η_i` weakly improves `u_i^A` under the stated
  assumptions.
- Model B's counterexample fails if the displayed derivative is nonpositive
  while `0<δ<1`, `g'(0)>0`, and the differentiability assumptions hold.
- Any future enforcement theorem is rejected if its action/outcome map is
  incomplete, it infers a global result from a local condition, or an
  admissible profitable deviation survives.

**Execution boundary:** structural toy-game results and a conjectural design
program only. No product, governance, deployment, or moral authority follows.
