---
title: "FAL-01 — Fiber-Asymmetry Lemma (projection, not ontology)"
id: "FAL-01"
type: formal-lemma
status: "ACTIVE [A] in declared reconstruction models; no D-level or physical promotion"
date: 2026-08-23
proposer: "Yves R. Burri"
evidence_tier: "[A] section/retraction and path-sensitive 0·∞ typing; [I] image for SLWP reconstruction debt; [C] ontological and physical emergence remain unearned"
owner: "Ontology lemma subordinate to SLWP-01; does not replace BIL-01 or adopt W19"
canonical_phrase: "Nontrivial fibers plus a declared selector yield reconstruction asymmetry; the earned report tag is PROJECTION_ASYMMETRY_PROVEN, never ONTOLOGICAL_STRONG_EMERGENCE_PROVEN"
parents:
  - "12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md"
  - "../05_COSMOLOGY/03_FORMAL_SYSTEM/59_BOUNDARY_INFORMATION_LOSS_LEMMA_BIL_01.md"
report_tag_earned: "PROJECTION_ASYMMETRY_PROVEN"
report_tag_forbidden: "ONTOLOGICAL_STRONG_EMERGENCE_PROVEN"
evidence_slots:
  projection_loss: "EARNED_IN_DECLARED_MODEL — BIL-01 endpoint map and any declared nontrivial fiber of U_n"
  computational_opacity: "UNEARNED"
  ontological_irreducibility: "UNEARNED"
  downward_intervention: "UNEARNED"
---

# FAL-01 — Fiber-Asymmetry Lemma

> **The result.** `[A]` If a declared projection `U_n` has a selected section
> `s_n` with `U_n ∘ s_n = id` and at least one nontrivial fiber, then
> reconstruction is asymmetric: the lower description is recovered uniquely,
> the higher description is not. The only honest report tag is
> `PROJECTION_ASYMMETRY_PROVEN`.
>
> **The fence.** That tag is **not** `ONTOLOGICAL_STRONG_EMERGENCE_PROVEN`.
> A many-to-one map can be ordinary, fully reducible coarse-graining. This
> lemma does not prove physical strong emergence, `μ_n`, or any D-crossing.

Ownership of the directional conjecture remains
[`SLWP-01`](12_STRONG_LIFT_WEAK_PROJECTION_CONJECTURE_SLWP_01.md). This note
supplies the fiber lemma SLWP already targets, plus fail-closed slots and
arithmetic typing. It does not thaw SLWP-01C and does not close
`PA-SLWP-01`.

## 1 · Data

For one declared reconstruction model, fix sets and maps

```text
U_n : H_(n+1) → L_n          forgetful / recovery projection
s_n : L_n → H_(n+1)          selected section (selector σ_n is part of s_n)
```

Write the fiber of a lower point `ℓ` as

```text
F_n(ℓ) := U_n^{-1}(ℓ) ⊆ H_(n+1).
```

The fiber is **nontrivial** when `|F_n(ℓ)| ≥ 2` for some `ℓ`.
**Selector dependence** means: given only `U_n(h)`, recovering a unique
`h` requires an extra choice `σ_n` (or an equivalent constraint, history,
or law not present in `L_n`).

## 2 · Lemma FAL-01 `[A]`

**Assumptions.** `U_n ∘ s_n = id_(L_n)`, and some fiber of `U_n` is
nontrivial.

**Conclusion.**

```text
U_n ∘ s_n = id_(L_n)
s_n ∘ U_n ≠ id_(H_(n+1))
```

The first equation is the section/retraction identity (recovery of the
declared lower description). The second is forced by a nontrivial fiber:
if `h` and `h'` are distinct and `U_n(h)=U_n(h')=ℓ`, then at most one of
them can equal `s_n(ℓ)`, so `s_n(U_n(·))` moves the other point.

**Asymmetric reconstruction.** Lower recovery is unique once `s_n` is
declared. Higher reconstruction from `U_n(h)` alone is not unique; it
depends on the selector. That is all the lemma proves.

**Report tag.** When the assumptions are exhibited in a declared model,
the earned tag is `PROJECTION_ASYMMETRY_PROVEN`.

**Forbidden tag.** `ONTOLOGICAL_STRONG_EMERGENCE_PROVEN` is never a
consequence of this lemma, of BIL-01, or of the SLWP target equations.

### What is not assumed

- `H_(n+1)` need not be a D-level.
- `s_n` need not be a physical lift or a `μ_n`.
- Nontrivial fibers need not be computationally opaque.
- The lower rival need not fail.

A partition of a finite set, a hash that forgets a bit, or a thermodynamic
coarse-grain can satisfy the same equations.

## 3 · Four evidence slots (fail-closed)

Each slot is independently empty until filled by its own evidence type.
Filling one does **not** fill the others.

| Slot | What would earn it | Status after FAL-01 |
|---|---|---|
| `projection_loss` | A declared `U_n` that forgets a recoverable distinction, with `U_n ∘ s_n = id` and a nontrivial fiber, **or** the BIL-01 endpoint map `E(trace)=(0,+∞)` | **EARNED_IN_DECLARED_MODEL** only. Not earned for unnamed physical crossings. |
| `computational_opacity` | A lower-bounded argument that no algorithm using only frozen `L_n` resources computes the higher distinction (Bedau-style intractability is still not ontology) | **UNEARNED** |
| `ontological_irreducibility` | A reduction-proof that no generator using only frozen `L_n` laws yields the higher variation (μ-contract: missing reduction ≠ irreducible) | **UNEARNED** |
| `downward_intervention` | A specified higher-to-lower intervention that changes lower behavior in a way no lower rival can match | **UNEARNED** |

SLWP-01 already owns the grammar and the failed BIL→ontology bridge. The
only slot it and BIL-01 already fill is `projection_loss` inside the
declared arithmetic / extended-real / discrete-fiber models. The other
three remain empty. `PA-SLWP-01` stays `PARTIAL / BRIDGE NOT ESTABLISHED`.

## 4 · Path-sensitive `0·∞` and division limits

These sentences are **not** interchangeable. Mixing them is a type error.

### 4.1 Ordinary arithmetic (field `ℝ`)

For finite real `M` and `N>0`:

```text
0 · M = 0
N / 0   is undefined
```

There is no field identity `0 · ∞ = N` and no field identity `N / 0 = ∞`.

### 4.2 Extended reals (`R̄₊ = [0,+∞]`)

The pair `(0,+∞)` is a legitimate **point** of the extended-positive line.
BIL-01 proves there is no function

```text
m̄ : R̄₊ × R̄₊ → R̄₊
```

that agrees with ordinary multiplication on finite pairs and is continuous
at `(0,+∞)`. That is endpoint underdetermination, not a new product.

### 4.3 Limits (path-sensitive)

`0·∞` is an indeterminate **limit form**. Distinct paths with the same
endpoint signature can yield `0`, any finite `N`, `+∞`, or no limit:

```text
(1/k²)·k → 0
(N/k)·k = N
(1/k)·k² → +∞
((2+(-1)^k)/(2k))·k  has no limit
```

Likewise the lawful limit sentence is `lim_(ε→0⁺) N/ε = +∞`. It is not the
field equation `N/0=∞`. The fiber of the endpoint map `E` is exactly this
path-dependence: the selector is the trace (rate and correlation), which
`E` forgets.

FAL-01 applied to `E` therefore earns `PROJECTION_ASYMMETRY_PROVEN` in the
BIL model and still earns none of the other three slots.

## 5 · Countermodels (fail-closed)

The lemma **does not apply**, or applies without ontology, in these cases.

| Countermodel | Why it closes the overclaim |
|---|---|
| **CM-id.** `H=L`, `U=s=id` | Fibers are singletons. `s ∘ U = id`. No projection asymmetry. |
| **CM-iso.** `U` bijective, `s=U⁻¹` | Unique reconstruction; selector is idle. |
| **CM-grain.** Bit-forgetful coarse-grain generated by lower laws | `U ∘ s = id`, fibers nontrivial, tag `PROJECTION_ASYMMETRY_PROVEN` is allowed; `ontological_irreducibility` stays empty. |
| **CM-arith.** Treating `0·∞=N` as ordinary arithmetic | Type error. Ordinary product is `0`; the finite `N` lives on a correlated path. |
| **CM-div.** Treating `N/0=∞` as a field identity | Type error. Division by zero is undefined; the `+∞` sentence is a limit. |
| **CM-promote.** Inferring `ONTOLOGICAL_STRONG_EMERGENCE_PROVEN` from FAL-01 or BIL-01 | Forbidden. Noninvertibility is not strong emergence. |

## 6 · What this note does not earn

1. No physical, biological, mental, or social transition is proved strongly
   emergent.
2. No `μ_n` is established.
3. Computational hardness is not recorded.
4. Downward causal intervention is not recorded.
5. SLWP-01C (serial reality at every D-crossing) remains `[C]` and open.
6. Founder force prior still earns no score.

The strongest honest sentence:

> `[A]` In any model where a section recovers `L_n` and a fiber of `U_n` is
> nontrivial, reconstruction is asymmetric (`PROJECTION_ASYMMETRY_PROVEN`).
> `[A]` The BIL-01 endpoint map is one such model, and `0·∞` stays a
> path-sensitive limit form. `[C]` Whether any licensed D-crossing is
> ontologically strongly emergent remains unearned.

## 7 · Tests

Fail-closed executable countermodels live at
[`tests/test_slwp_fiber_asymmetry.py`](tests/test_slwp_fiber_asymmetry.py).

```text
python3 06_ONTOLOGY/tests/test_slwp_fiber_asymmetry.py
```
