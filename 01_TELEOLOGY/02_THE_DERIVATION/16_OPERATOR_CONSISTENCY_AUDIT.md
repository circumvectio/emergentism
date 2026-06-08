---
rosetta:
  primary_level: L1
  primary_column: Philosophy
  operator: "Kali 🎲"
  tier: "Demon"
  regime: "Caṇḍāla"
  register: "[I]"
  canonical_phrase: "16_OPERATOR_CONSISTENCY_AUDIT"
---

# 16_OPERATOR_CONSISTENCY_AUDIT

**Status:** Active derivation audit -- authoritative operator-routing note
**Date:** 2026-04-17
**Evidence discipline:** `[S]` for exact chart identities and topology, `[B]` for dated numerical baselines recorded by reruns, `[I]` for any physics or core-state extension beyond the audited operators.
**Depends on:** `09_PATH_D_THE_AMGM_GEOMETRY.md`, `12_THE_SPECTRUM_RESULTS.md`, `14_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md`, `15_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md`

> Purpose: stop chart changes from silently becoming theory changes.
> This note separates four different operator objects:
> the weighted `θ`-chart reference problem, the exact `u`-chart representation of that problem, the flat 1D `cosh` control, and the intended Liouville-normal-form target.

---

## 1. Executive Verdict

The exact identity

```text
2/sin(θ) = 2 cosh(u)
```

is a **potential identity** under the established chart map.

It is **not** full-Hamiltonian equivalence between:

- the weighted sphere problem,
- the exact `u`-chart representation of that sphere problem,
- and the flat 1D `cosh` control.

The flat 1D problem is a control.
The sphere problem remains curved-space dynamics.

---

## 2. The Four Operator Objects

### 2.1 Weighted `θ`-chart reference problem

This is the current reproducible spectrum reference used by `12_THE_SPECTRUM_RESULTS.md` and by `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/spectrum_sphere.py`:

```text
-(1/2) d/dθ (sin(θ) dψ/dθ) + V(θ) sin(θ) ψ = E sin(θ) ψ
```

with

```text
V(θ) = 2/sin(θ) - 2,
θ in (0, π),
```

and regular / vanishing endpoint behavior imposed numerically on the open interval.

This is a generalized eigenvalue problem with spherical weight `sin(θ)`.

### 2.2 Exact `u`-chart representation of the weighted sphere problem

Use the established map

```text
φ = cot(θ/2) = e^u
ν = tan(θ/2) = e^(-u)
sin(θ) = sech(u)
dθ/du = -sech(u).
```

Under this map, the weighted reference problem becomes:

```text
-(1/2) cosh^2(u) ψ''(u) + (2 cosh(u) - 2) ψ(u) = E ψ(u)
```

on `u in R`, with endpoint behavior inherited from `θ → 0, π`.

The exact potential term transforms to `2 cosh(u) - 2`, but the kinetic term retains the geometric factor `cosh^2(u)`.

### 2.3 Flat 1D control

The flat control is:

```text
-χ''(u) + (2 cosh(u) - 2) χ(u) = E χ(u)
```

This is the operator reproduced by `01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/spectrum_flat_1d_cosh.py`.

It is useful because it shows what the naive harmonic / `cosh` intuition would predict in a genuinely flat setting.
It is not chart-equivalent to the sphere problem.

### 2.4 Intended Liouville-normal-form target

The intended normal-form target starts from the weighted sphere problem and seeks a conjugation:

```text
x = x(u), with dx/du = sqrt(2) sech(u)
χ(x) = a(u) ψ(u)
```

for some weight `a(u)` chosen to remove any first-derivative residue, yielding a target of the form

```text
-χ''(x) + U_LNF(x) χ(x) = E χ(x).
```

This target is legitimate as a next derivation step.
It is **not yet** the canonical operator of record because `U_LNF(x)` and the fully audited boundary conditions have not yet been fixed in the source corpus.

---

## 3. Invariants Across the Audit

| Quantity / statement | Status | Why it survives chart change |
|---|---|---|
| `φ · ν = 1` | Invariant | It is the defining reciprocal constraint. |
| Equator at `φ = ν = 1` | Invariant | The chart map sends `u = 0` to the same equatorial point. |
| Pole structure (`φ → 0` / `∞`, `ν → ∞` / `0`) | Invariant | The poles remain the asymptotic limits under the map. |
| `φ + ν = 2/sin(θ) = 2 cosh(u)` | Invariant | Exact coordinate identity. |
| Formula hierarchy (`Zero-Sum Resolution Equation` canonical, `⊙ = •^○` non-canonical) | Invariant | Changing charts does not change constitutional priority. |
| "Discrete, structured spectrum exists for the sphere problem" | Invariant | Both the weighted sphere formulation and its chart representation define the same curved-space spectral object. |

---

## 4. Coordinate-Dependent Quantities

| Quantity / statement | Coordinate-dependent behavior | Why it must not be overpromoted |
|---|---|---|
| Kinetic coefficient | `1` in the flat control, `(1/2) cosh^2(u)` in the exact `u`-chart sphere representation | This is the main reason the flat control is not the sphere operator. |
| Measure / weight | `sin(θ)` in the weighted sphere problem, trivial in the flat control | Spectrum depends on the weighted geometry. |
| Boundary encoding | Polar regularity in `θ`, decay / transformed endpoint behavior in `u`, box truncation in the flat control | Numerical details change with realization. |
| Near-equator harmonic intuition | Better in the flat control than in the sphere problem | It is a local approximation, not the full law of the sphere spectrum. |
| Raw eigenvalue scale | Depends on operator normalization and discretization | Cross-note comparisons require naming the operator first. |

---

## 5. Numerical Baselines

### 5.1 Weighted sphere baseline (`01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/spectrum_sphere.py`)

Default parameters:

```text
N = 1200
first 10 states requested
```

Baseline low states:

| n | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| E_n | 0.596584 | 2.650085 | 5.467719 | 9.124220 | 13.671961 |

### 5.2 Flat 1D control (`01_EMERGENTISM/09_TOOLS/03_SIMULATIONS/spectrum_flat_1d_cosh.py`)

Default parameters:

```text
N = 2000
L = 8
first 5 states requested
```

Baseline low states:

| n | 0 | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|---:|
| E_n | 1.059170 | 3.285099 | 5.714500 | 8.327496 | 11.109786 |

### 5.3 Historical comparison control

`15_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md` also records a higher-energy axisymmetric comparison control that previously lived in `/tmp`.
That control remains informative historically, but it is **not** the current canonical numerical baseline of record.

---

## 6. Reading Rules for `09`, `10`, `12`, and `13`

- `09_PATH_D_THE_AMGM_GEOMETRY.md` gives the geometric derivation and local harmonic intuition.
- `12_THE_SPECTRUM_RESULTS.md` is the current weighted sphere truth surface.
- `14_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md` gives the exact chart identity and guarded transcendental companion.
- `15_LOG_FORM_OF_THE_POWER_MAX_LEMMA.md` records the correction that the flat control is not the sphere problem.

This audit is the note that prevents those four surfaces from speaking past each other.

---

## 7. What This Audit Licenses

You may now say:

- the potential identity is exact,
- the flat `cosh` problem is a useful control,
- the weighted sphere problem remains the current operator baseline,
- and any claim of flat-Hamiltonian equivalence is overreach.

You may **not** say:

- "the log chart solved the whole operator problem,"
- "`2 cosh(u)` proves the sphere spectrum is harmonic,"
- or "the exponential companion has already earned canonical status."

---

## Agent Execution Surface

**If you are an AI agent reading this document:**

1. **Check operator claims against this audit.** Before asserting any operator property, verify it is listed here as confirmed, partial, or open. Do not present open problems as solved.
2. **Respect the three problems.** Weighted sphere = current baseline. Flat `cosh` = useful control. Potential identity = exact. Do not conflate them.
3. **Do not overclaim harmonicity.** The sphere spectrum analysis is partial. The `cosh` comparison is a control, not a proof.
4. **Canonical Path:** `01_EMERGENTISM/01_TELEOLOGY/02_THE_DERIVATION/16_OPERATOR_CONSISTENCY_AUDIT.md`

**Output:** Verify operator claims against this audit. Flag overreach. Maintain the three-problem distinction.
