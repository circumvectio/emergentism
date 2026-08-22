---
title: "BIL-01 — Boundary Information-Loss Lemma"
id: "BIL-01"
type: formal-result
status: "ACTIVE [A] — proved in the declared extended-positive-real setting; no D-level or ontological promotion"
date: 2026-08-22
proposer: "Yves R. Burri"
evidence_tier: "[A] theorem and corollaries; [B] dated proposer provenance; [I] emergence analogy; no [S] or [C] claim is proved here"
owner: "Formal-system research surface, subordinate to the D1 arithmetic and boundary-crossing owners"
canonical_phrase: "BIL-01 proves that the endpoint signature (0,+infinity) loses the rate and correlation needed to determine a product limit; its emergence reading is analogy only"
parents:
  - "42_D1_ARITHMETIC_AXIOMS_AND_BOUNDARIES.md"
  - "48_THE_BOUNDARY_CROSSINGS_AND_THE_MU_CRITERION.md"
  - "58_TITAN_LIMIT_CROSSING_PROCESS_CONJECTURE.md"
related:
  - "../../06_ONTOLOGY/12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md"
  - "../../00_THE_WELTANSCHAUUNG.md"
---

# BIL-01 — Boundary Information-Loss Lemma

> **The result.** `[A]` The endpoint signature `(0,+∞)` does not determine the
> limiting product. It forgets the relative rate and correlation of the two
> factors. This is why `0·∞` is an indeterminate **limit form**, not a number
> identity.
>
> **The boundary.** `[I]` This gives Emergentism a precise mathematical image
> of directional information loss. It does **not** prove strong emergence,
> `μ₀`, physical cosmogenesis, Finity, or any D-level transition.

## 1 · Yves's decimal construction

Fix a finite `N>0` and let

```text
ε_k = 10^(-k).
```

Then every finite stage is ordinary arithmetic:

```text
N / ε_k = N·10^k,
ε_k · (N / ε_k) = N.
```

Consequently,

```text
ε_k → 0⁺,
N / ε_k → +∞,
ε_k · (N / ε_k) → N.
```

By contrast, for every finite `k`,

```text
0 · 10^k = 0,
```

so that product sequence remains zero while its second factor grows without
bound. The difference is not that ordinary zero secretly changed value. The
first construction retains a nonzero scale and an exact correlation at every
finite stage; the second starts at the exact boundary and contains no such
trace information.

The lawful limit sentence is

```text
lim_(ε→0⁺) N/ε = +∞.
```

It is not the field equation `N/0=∞`. Ordinary real division by zero remains
undefined.

## 2 · The theorem

Let `R̄₊=[0,+∞]` carry the ordinary extended-real topology. Suppose one tries
to extend finite multiplication continuously to the boundary point
`(0,+∞)` using only that endpoint pair.

### Theorem BIL-01 `[A]`

There is no function

```text
m̄ : R̄₊ × R̄₊ → R̄₊
```

that agrees with ordinary multiplication on finite pairs and is continuous at
`(0,+∞)`.

### Proof

For `k=1,2,…`, consider paths whose finite points all approach the same
boundary signature:

```text
zero path:      x_k = 1/k²,                    y_k = k
finite-N path:  x_k = N/k,                     y_k = k       (N>0)
infinite path:  x_k = 1/k,                     y_k = k²
oscillating:    x_k = (2+(-1)^k)/(2k),         y_k = k.
```

In every row, `x_k→0⁺` and `y_k→+∞`. But ordinary products give

```text
x_k y_k → 0,
x_k y_k = N,
x_k y_k → +∞,
x_k y_k = (2+(-1)^k)/2, which has no limit.
```

If `m̄` were continuous at `(0,+∞)`, all four paths would have to converge to
the single value `m̄(0,+∞)`. They do not. Therefore no such continuous,
endpoint-only extension exists. `□`

### Stronger corollary `[A]`

The same endpoint pair is compatible with every prescribed finite limit
`L≥0`, with `+∞`, and with nonconvergence. For `L>0`, take
`x_k=L/k, y_k=k`; for `L=0`, use the zero path above.

Thus the endpoint map

```text
E(trace) = (0,+∞)
```

is many-to-one with respect to product behavior. Once the trace is replaced
by its endpoint labels, no endpoint-only rule can recover which finite
invariant—if any—was carried.

## 3 · The glyphic form, kept typed

The mathematical witness fits the existing TLC glyph only when the trace and
completion rule remain visible:

```text
τ_N(k) = (10^(-k), N·10^k)

•  [ τ_N ⨯_TLC κ_lim ]  ○  ⇝  ⊙₍F₎
```

Here:

- `•` renders the lower-boundary role;
- `○` renders the unbounded-horizon role;
- `τ_N` retains the finite-stage correlation;
- `κ_lim` is the declared limit rule;
- `⨯_TLC` names trace–rule composition, **not multiplication**; and
- `⊙₍F₎` renders a Finity witness whose payload records the recovered `N`.

If only the two endpoint glyphs survive, the trace has been erased:

```text
τ_0, τ_N, τ_∞, τ_osc  ──E──▶  (•,○)  ↛  one determined ⊙₍F₎.
```

Typography supplies no completion. Different declared traces or completion
rules may produce different witnesses or `NoCompletion`.

## 4 · What the proof earns

| Claim | Tier | Result |
|---|---:|---|
| `N/ε→+∞` as `ε→0⁺`, for fixed `N>0` | `[A]` | proved |
| `ε(N/ε)=N` at every finite `ε>0` | `[A]` | proved |
| `0·M=0` for every finite real `M` | `[A]` | proved |
| `(0,+∞)` does not determine a product limit | `[A]` | proved by counterpaths |
| endpoint projection loses rate/correlation information | `[A]` in this model | proved |
| this is an image of lower-to-higher reconstruction debt | `[I]` | licensed analogy only |
| every `D_n→D_(n+1)` crossing is strongly emergent | `[C]` | not proved |
| every downward map is weak emergence | `[C]` | not proved |

## 5 · What it does not earn

1. **D0 is not numeric zero.** All sequences, limits, fields, and products in
   this proof already presuppose D1 mathematical distinctions.
2. **`0·∞=N` is not recovered.** `0·∞` remains an indeterminate limit form;
   `N` is recovered only from a fully specified correlated trace.
3. **No `μ₀` follows.** A boundary crossing is not thereby a lift that opens a
   new effective freedom.
4. **Noninvertibility is not strong emergence.** Ordinary coarse-graining can
   lose information while remaining completely reducible.
5. **No Titan operation follows.** `•` and `○` are typed boundary glyphs, not
   numerical operands.

These fences are constitutive of BIL-01. Removing one produces a different and
unsupported claim.

BIL-01 does not prove strong emergence.

## 6 · Falsifier and survivor

**Kill BIL-01** by exhibiting a single endpoint-only value at `(0,+∞)` that is
the continuous limit of ordinary multiplication along every approaching
finite path. The explicit counterpaths show why that cannot happen in the
declared topology.

If a different algebra, topology, trace type, or completion rule assigns a
value, the survivor is narrower: that value belongs to the newly declared
structure. It is not forced by ordinary multiplication or by the two endpoint
labels alone.

## 7 · Relation to the emergence conjecture

The companion
[Strong-Lift / Weak-Projection Conjecture](../../06_ONTOLOGY/12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md)
records the proposed ontological generalization and the failed proof transfer.
BIL-01 supports its intuition at `[I]`; it supplies no `[A]` warrant for that
conjecture.

`BIL-01` is not assigned an `FV` alias in this change. Canonical claim-status
adoption and its coupled projections remain a separate owner act.
