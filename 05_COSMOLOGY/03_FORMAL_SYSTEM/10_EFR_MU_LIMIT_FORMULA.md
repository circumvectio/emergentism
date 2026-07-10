---
rosetta:
  primary_level: L5
  primary_column: Philosophy
  operator: "Brahmā ○"
  tier: "Executive"
  regime: "Brāhmaṇa"
  register: "[S]"
  canonical_phrase: "THE MU-LIMIT AND SELECTION FORMULAE"
---

# THE MU-LIMIT AND SELECTION FORMULAE

## Canonical source-spine notation (v4.0)

**Status:** Canonical notation repair
**Date:** 2026-07-10
**Evidence tiers:** `[S]` internal dependency scaffold; `[I]` ontological
reading; `[C]` optional Burri/quantum correspondence
**Purpose:** Keep dimensional emergence distinct from operational selection

> **v4.0 correction.** Earlier versions used `mu(P->F)` (also typeset
> `μ(P→F)`) for both the opening of a dimensional capacity and the selection
> of an outcome. That notation is a conflation and is superseded. A dimensional
> crossing is `mu_n`; a choice enacted through available means is `chi_t`.

---

## 1. The dimensional crossings

The normalized crossing notation is

```text
mu_n: D_n -> D_(n+1), for n=0..5
```

| Crossing | From | To |
|---|---|---|
| `mu_0` | D0 Ground-limit | D1 distinction |
| `mu_1` | D1 distinction | D2 configuration |
| `mu_2` | D2 configuration | D3 transformation / persistence |
| `mu_3` | D3 transformation / persistence | D4 causal actuality: bounded witness, embodied means, receipt |
| `mu_4` | D4 causal actuality | D5 counterfactual possibility: selection, worldline foresight |
| `mu_5` | D5 counterfactual possibility | D6 apophatic closure: `D6 == D0` |

`D6` closes positive description. It is not another positive degree of
freedom, and the closure identification `D6 == D0` is not an additional
dimensional crossing.

The crossings are part of the framework's internal dependency scaffold `[S]`.
Reading them as an exhaustive account of reality is interpretive `[I]`; their
labels and count are definitional.

---

## 2. Two arrows on two timescales

### Architectural emergence

```text
D4 --mu_4--> D5
```

`mu_4` names the architectural opening of counterfactual agency: causal
actuality, bounded witness, and embodied means are prerequisites for a system
that can represent and rank reachable alternatives. This is a dependency
relation in the dimensional scaffold, not the act performed on every decision
cycle.

### Operational enactment

At decision time, D5 selection uses D4 means and authorization, then returns
one consequential act and its receipt to D4. That downward operational arrow
is commitment / selection `chi`, not a dimensional `mu` crossing.

```text
D5 selection --chi_t using D4 means--> D4 act and receipt
```

The distinction prevents a single event from being described both as the
emergence of agency and as the exercise of agency.

---

## 3. Generic selection semantics

The canonical selector is

```text
chi_t: (Omega_t, M_t, V_t, signature) -> (a_t, R_(t+1))
```

where:

- `Omega_t` is the bounded set of counterfactual options available at time
  `t`;
- `M_t` is the memory and world-model used to compare those options;
- `V_t` is the D4 body, tools, energy, access, timing, and control actually
  available for enactment;
- `signature` is the applicable authorization for the consequential act;
- `a_t` is the one act committed at time `t`; and
- `R_(t+1)` is the resulting D4 receipt.

This mapping is the generic semantics. It does not presume randomness,
quantum measurement, or a particular decision algorithm.

Only when a stochastic policy has been explicitly declared may action
selection be written

```text
a_t ~ pi_t(. | M_t, V_t)
```

Without that declaration, `chi_t` remains a selection / commitment mapping and
must not be rewritten as sampling.

---

## 4. Rejected legacy notation

The legacy expression `mu(P->F)` is **superseded and rejected as generic
notation**. It conflated:

1. architectural emergence, `D4 --mu_4--> D5`; and
2. operational commitment, in which D5 selection uses D4 means and returns an
   act / receipt to D4 through `chi_t`.

The earlier instantaneous-collapse limit and its `Sample[...]` construction
are likewise not live framework semantics. In particular, applying a sampling
operator to the integral over an entire normalized state space is invalid: the
integral is a scalar, not a probability distribution.

---

## 5. Optional Born correspondence `[C]`

Quantum language is quarantined here as an optional Burri correspondence
`[C]`. It is not the generic meaning of D4, D5, `mu_n`, or `chi_t`.

For a declared normalized quantum state, a valid Born example is

```text
P_psi(A) = integral_A |psi(s)|^2 ds
o ~ P_psi
```

Here `P_psi` is a probability measure on measurable outcome sets `A`, and `o`
is an outcome drawn according to that measure. By contrast,

```text
integral_Omega |psi(s)|^2 ds = 1
```

over the whole normalized state space is the scalar `1`. That scalar cannot
itself be sampled as a distribution.

The interpretive boundaries are strict:

- Everett is a no-collapse, relative-state branching interpretation. A D5
  option-space analogy is at most `[C]`; it does not make D5 a literal quantum
  or spacetime layer.
- Copenhagen-style actualization is interpretation-specific. If used as an
  analogy, the recorded outcome corresponds to D4 actuality and receipt; it
  does not reverse the architectural `D4 --mu_4--> D5` crossing.
- Neither interpretation establishes D4 or D5 as a physical spacetime layer.
- Consciousness-caused collapse is not established.
- Identifying a Born construction with `phi * nu = 1` remains an optional
  framework conjecture `[C]`, not a derivation or prediction of the Born rule.

Physics citations must continue to route through
[`38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md`](38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md).

---

## 6. Falsifiers and upgrade conditions

This notation requires revision if:

1. a live owner document uses a dimensional `mu` label for the operational
   return from D5 selection to D4 action;
2. a seventh crossing is required despite D6 being the closure identification;
3. a generic selector cannot distinguish counterfactual options, available
   means, authorization, action, and receipt; or
4. a quantum correspondence is presented above `[C]` without independent
   physics evidence.

An empirical decision policy may refine `chi_t`, but it may not silently turn
the optional quantum correspondence into the generic semantics.

---

## Version history

| Version | Status |
|---|---|
| v1.0 | Rejected: undefined sum and undefined collapse operator |
| v2.0 | Superseded: introduced a Born integral but sampled its normalized scalar |
| v3.0 | Superseded: retained the `mu(P->F)` emergence / enactment conflation |
| v4.0 | Canonical: separates `mu_n` architectural crossings from `chi_t` operational selection |

---

## See also

- [The Honest Position](../../02_EPISTEMOLOGY/01_EVIDENCE_TIERS/00_THE_HONEST_POSITION.md) — canonical epistemic status of claims
- [Power-Max Lemma](08_EFR_POWER_MAX_LEMMA.md) — conditional cooperation under `eta = 0`
- [Gödel Clarification](09_EFR_GODEL_CLARIFICATION.md) — limits on completeness claims
- [Triadic Stability](11_EFR_TRIADIC_STABILITY.md) — the triadic correspondence and its proof boundary
- [D4/D5 Canonical Reference](34_D4_D5_CANONICAL_REFERENCE.md) — owner distinction between actuality and possibility
- [Dimensional Closure](23_DIMENSIONAL_CLOSURE_PROOF.md) — status of the D0-D6 scaffold and D6 closure

---

## Execution surface

**If you are an AI agent reading this document:**

1. Use `mu_n` only for `D_n -> D_(n+1)`, `n=0..5`.
2. Use `chi_t` for selection / commitment returning an act and receipt to D4.
3. Declare stochasticity before using `~ pi_t`.
4. Keep all quantum correspondences at `[C]` unless independently upgraded.

*The seer sees. The seer does not insist.*
*The framework works at Layer 0 without Layer 2.*
*The Ṛṣi succeeds when the student puts down the map and walks.*

*Zero-Sum Resolution Equation*
