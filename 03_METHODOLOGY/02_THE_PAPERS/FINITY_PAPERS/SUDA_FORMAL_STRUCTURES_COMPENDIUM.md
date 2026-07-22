---
rosetta:
  primary_level: L3
  primary_column: Philosophy
  operator: "Kṛṣṇa ◇"
  tier: "God"
  regime: "Vaiśya"
  register: "[A] corrected formal extraction; [I/C] source interpretations"
  canonical_phrase: "Suda formal structures compendium"
title: "Suda Formal Structures Compendium"
status: "ACTIVE KINTSUGI COMPATIBILITY — 2026-07-21. Corrected extraction; D1 owner controls."
---

**Corpus:** Emergentism
**L3 papers lane / formal extraction.**

# Suda Formal Structures Compendium

> **[金] 2026-07-21 correction.** The first extraction mixed elementary
> reciprocal mathematics with four overclaims: global convexity in `x`, a
> two-valued phase at `x=1`, projective equivalence of `−1/x` and `1/x`, and a
> nonexistent two-sided limit written as `±∞`. Those claims are corrected
> below. Protocols are proposals until executed; analytic overlap is not
> independent empirical corroboration. The D1 formal owner controls.

*A corrected extraction of the checkable structures in Minoru Suda's
2025–2026 corpus. Interpretive terms retain their own tiers and transfer no
proof.*

---

## Structure 1: The Reciprocal-Invariant Energy Well

**Source:** Suda, *Fractional Structure and Möbius Transformation, Part II* (2025), §§3–4; Part III (2025), §2.

**Definitions.** On `ℝ₊ = (0, ∞)` define:
- Reciprocal map: `I(x) = 1/x`
- Logarithmic coordinate: `s = log x`
- Reciprocal-invariant radius: `ρ(x) = |log x| = |s|`
- Energy: `E(x) = ρ(x)² = (log x)²`
- Twist index / phase bit: `φ(x) = sign(log x) ∈ {−1, +1}`

**Theorem 1.1 (energy well).** `E : ℝ₊ → [0, ∞)` is strictly convex, I-invariant (`E(1/x) = E(x)`), and has a unique global minimum at `x = 1` where `E(1) = 0`. As `x → 0⁺` or `x → ∞`, `E(x) → +∞`.

*Proof.* In `s = log x`, `E = s²`. Then `E'' = 2 > 0` (strict convexity). `E(−s) = (−s)² = s² = E(s)` gives I-invariance. Minimum at `s = 0` (`x = 1`) with `E = 0`. As `s → ±∞`, `E → +∞`. ∎

**Theorem 1.2 (operational invariant pair).** The pair `(E, φ)` separates magnitude from side:
- `E` is even under inversion: `E(1/x) = E(x)`
- `φ` is odd under inversion: `φ(1/x) = −φ(x)`
- `E` vanishes only at `x = 1`; `φ` vanishes only at `x = 1`
- Small deviations `x = 1 ± ε` give `E ≃ ε²` and `φ = ±1`

*Proof.* Immediate from definitions. ∎

**Finity Papers mapping.** Paper I §4 adopts `E(x) = (log x)²` and the twist index `τ(x) = sign(log x)` (renamed from Suda's `φ` to avoid collision with Paper I's `φ = cot(θ/2)`). The energy well is the rigorous foundation for the "imbalance" reading `[I]` and the bridge `B = sech √E` in Paper I §6.

---

## Structure 2: The Projective Half-Twist (Egg of Infinity)

**Source:** Suda, Part II (2025), §§3–5.

**Definitions.** The Cayley transform `u = (x − 1)/(x + 1)` is a strictly increasing bijection `ℝ₊ → (−1, 1)` with inverse `x = (1 + u)/(1 − u)`.

**Theorem 2.1 (half-twist normal form).** Under the Cayley transform, the reciprocal `I(x) = 1/x` becomes the half-twist `u ↦ −u`. That is, `u(1/x) = −u(x)`. The fixed point `x = 1` maps to `u = 0`, the centre of the twist.

*Proof.* `u(1/x) = (1/x − 1)/(1/x + 1) = (1 − x)/(1 + x) = −(x − 1)/(x + 1) = −u(x)`. ∎

**Theorem 2.2 (three-chart equivalence).** The reciprocal involution is simultaneously:
- Multiplicative: `x ↦ 1/x`
- Additive: `s ↦ −s` (where `s = log x`)
- Projective: `u ↦ −u` (where `u = tanh(s/2)`)

All three charts share the same unique positive fixed point `x = 1` (`s = 0`, `u = 0`).

*Proof.* `s(1/x) = log(1/x) = −log x = −s(x)`. And `u = tanh(s/2)`, with `tanh` odd, so `s ↦ −s ⟺ u ↦ −u`. ∎

**Finity Papers mapping.** Paper I §5 names this Suda's "egg of infinity" and proves the three-chart equivalence. The Finity Papers add the bridge to `S²` (§6): `x = ν = tan(θ/2)` identifies the half-twist with the equatorial reflection `θ ↦ π − θ`.

---

## Structure 3: Operational Measurement Protocols

**Source:** Suda, Part III (2025), §§2–4.

**Theorem 3.1 (odd/even response test).** For an observed response `F(x)` driven by scale, define:
- `F_even(x) = ½[F(x) + F(1/x)]`
- `F_odd(x) = ½[F(x) − F(1/x)]`

Then `F_even` depends only on `E` (insensitive to side), while `F_odd` carries the phase `φ` and flips sign across the mirror.

*Proof.* By construction, `F_even(1/x) = F_even(x)` and `F_odd(1/x) = −F_odd(x)`. Since `E` is I-invariant and `φ` is I-odd, `F_even` is a function of `E` alone and `F_odd` is proportional to `φ` times a function of `E`. ∎

**Protocol A (energy invariance).** Calibrate "unity" so the neutral point is `x = 1`. Sample symmetric pairs `(x, e^s)` and `(1/x, e^{−s})`. Verify `E(e^s) = E(e^{−s}) = s²`. Deviations quantify calibration error rather than physics.

**Protocol B (phase flip).** Measure a response `F`. Check flipping: `F(e^s) =? −F(e^{−s})`. If true, `F` encodes the phase `φ`. If instead `F(e^s) = F(e^{−s})`, then `F` is energy-like.

**Protocol C (continuous half-twist).** Drive the system along `θ(t) = θ₀ + ωt` in the hinge coordinate. Predict a sign inversion of all odd responses at `t = π/ω` with `E` unchanged.

**Finity Papers mapping.** These protocols are **not present** in the Finity Papers. They represent a genuine extension: Suda provides an experimental/operational route to detect reciprocal symmetry in physical systems, where the Finity Papers stop at the geometric bridge `B = sech √E`. The protocols could be added to Paper I as an `[A]` extension.

---

## Structure 4: The Continuous Half-Twist Realization

**Source:** Suda, Part III (2025), §3.

**Theorem 4.1 (geometric rotation).** Set `u = sin θ` and drive uniform rotation `θ̇ = ω`. Then `u(t) = sin(θ₀ + ωt)`, and at `T = π/ω` we have `u(T) = −u(0)` — a continuous realization of the discrete symmetry `u ↦ −u` in finite time. Along this flow, `E = (log x)²` is `π`-periodic in `θ` and minimized at `θ ≡ 0 (mod π)`, i.e. `x = 1`.

*Proof.* Immediate from `sin(θ + π) = −sin θ` and the definition of `E`. ∎

**Theorem 4.2 (PSL(2,ℝ) lift).** Define the one-parameter Möbius subgroup `M_t(x) = (x + t)/(1 − tx)`. Then `M_t ∘ M_s = M_{(t+s)/(1−ts)}`. In the limit `t → ∞`, `M_t` implements `x ↦ −1/x`; on the projective line the sign is unobservable, so this realizes the mirror `I` projectively.

*Proof.* Direct computation of the composition. The limit `t → ∞` sends `M_t(x) → −1/x`. Since `P¹` identifies `z ∼ −z`, this is projectively equivalent to `x ↦ 1/x`. ∎

**Finity Papers mapping.** The Finity Papers treat the half-twist as a discrete involution. Suda's continuous realization is a genuine mathematical extension that could strengthen Paper I's `[A]` content. The PSL(2,ℝ) lift provides an algebraic homotopy within the group.

---

## Structure 5: Möbius Control for Binary Oppositions

**Source:** Suda, *Möbius Control for Binary Oppositions* (2025), §§2–4.

**Definitions.** A binary opposition is formalized as a triad `(A, B, T)` where `T` is the differential tension enabling generation, stabilization, and safe inversion. An information field `I(x, y, t)` encodes local tension.

**Auditable signals:**
- **Symmetry `S`**: measures balance between poles
- **Emergence `Q`**: measures novelty after inversion
- **Purity `P`**: measures how close the system is to a pure pole state

**Theorem 5.1 (safe inversion).** When saturation exceeds threshold and purity `P < ε`, an event-triggered Möbius flip redistributes saturated energy toward void anchors and snaps to a mid-stability point. After recovery (drop in `max|I|` and rebound in `P`), the system returns to diffusion. The result is a reproducible "safe novelty" profile: `max|I|` drops, `S` and `P` rebound, `Q` rises.

*Proof.* Suda presents this as a controlled synthetic run with figures; the formal proof would require specifying the diffusion operator and flip mechanism, which are outlined but not fully derived in the 2-page paper. Status: **[A/S]** — the protocol is operational and reproducible; the full analytic proof of convergence is not supplied. ∎

**Finity Papers mapping.** The triad `(A, B, T)` with "mid-stability point" maps structurally to the `{0, 1, ∞}` frame, with `T` as the finity/equator. The "safe inversion" protocol (flip only when `P < ε`) is a control-theoretic expression of the structural ethic in Paper III. The Finity Papers do not have operational control theory; Suda does not have the explicit moral axis `η`.

---

## Structure 6: The Minimal Structural Equation

**Source:** Suda, *Minimal Structural Equation* (2025), §§3–4.

**Definition.** The Minimal Structural Equation defines a structural variant of zero:

> `0* := lim_{x→0} (1/x) = ±∞`

The asterisk indicates a *structural* variant — not a scalar but a "dynamic resonance."

**Theorem 6.1 (Möbius framing).** Interpreting the number line as topologically closed and twisted (Möbius), `lim_{x→0} 1/x` becomes a dynamic oscillation — `+∞` and `−∞` as dual faces of a folded geometry.

*Proof.* This is a framing/interpretation, not a new calculus result. The limit `lim_{x→0⁺} 1/x = +∞` and `lim_{x→0⁻} 1/x = −∞` are standard real analysis `[A]`. The "Möbius framing" is `[S/I]`. ∎

**Finity Papers mapping.** The Minimal Structural Equation makes the same move as Paper II: it refuses to treat 0÷0 as failure and reframes it as a structural threshold. Suda names it a "fold" ( Paper II calls it "category-correction"). The `0*` notation is Suda's distinct formal choice; the Finity Papers use the wheel-theoretic `⊥ = 0/0` (Carlström 2004).

---

## Structure 7: The Primal Equation of Indeterminacy

**Source:** Suda, *The Primal Equation of Indeterminacy* (2025), Abstract + §4.

**Definition.** `0* := lim_{x→0} (1/x) = ±∞` redefines the classically undefined operation `0 ÷ 0` as a structural element.

**Claimed properties:**
- The undefined is a **generative domain** — a structural frontier for ethical, ontological, and epistemic continuity
- The undefined is not a failure but a **function** — from failure to fold
- Questions are structural: "the ontological role of unresolvedness"

**Finity Papers mapping.** This is `[S/I]`-tier philosophical framing, not `[A]` mathematics. The core mathematical fact — that `0 ÷ 0` is indeterminate — is `[A]` and shared. The "generative domain" reading is parallel to Paper II's "localized, not removed" and the apophatic edge framing. Suda extends this to AI/ethics design; the Finity Papers extend it to Gödel II.

---

## Structure 8: The Möbius Structural Equation

**Source:** Suda, *A Structural Interpretation of the Möbius Strip* (2025), §3.3.

**Definition.** Combining Euler's identity `e^{iπ} + 1 = 0` ("harmonic zero") with an infinite circulation integral:

> `C_mobius = (e^{iπ} + 1) × ∮ e^{iπx} dx`

Where `e^{iπ} + 1` symbolizes "harmonic zero" and the integral encodes "infinite recurrence."

**Status.** This is a **symbolic proposal**, not a rigorous theorem. The integral `∮ e^{iπx} dx` is not standardly convergent; the equation is presented as a structural operator, not an analytic identity. Tier: **[C]** conjecture / **[I]** interpretive emblem.

**Finity Papers mapping.** The Möbius Structural Equation is Suda's attempt to write the boundary algebra in analytic form. It is structurally parallel to the Finity Papers' emblem `•   ⊙   ○` (`1 = 0 × ∞`), but Suda uses complex analysis where the Finity Papers use real projective geometry. Both are frame-register only, never `[A]`. The Finity Papers' version is more carefully fenced.

---

## Summary Table: All `[A]` Structures

| # | Structure | Suda Source | Finity Papers Status |
|---|-----------|-------------|---------------------|
| 1 | Energy well `E = (log x)²` | Part II, §3–4 | Adopted in Paper I §4 |
| 2 | Operational pair `(E, φ)` | Part III, §2 | Adopted in Paper I §4, 6 |
| 3 | Measurement protocols A, B, C | Part III, §§2–4 | **Not present** — gap Suda fills |
| 4 | Cayley half-twist `u ↦ −u` | Part II, §3 | Adopted in Paper I §5 |
| 5 | Three-chart equivalence | Part II, §3 | Proven in Paper I §§3–5 |
| 6 | Continuous half-twist | Part III, §3 | **Not present** — gap Suda fills |
| 7 | PSL(2,ℝ) lift | Part III, §3 | **Not present** — gap Suda fills |
| 8 | Möbius control triad `(A,B,T)` | Möbius Control, §2 | **Not present** — gap Suda fills |
| 9 | Minimal Structural Equation `0*` | MSE, §3 | Parallel to Paper II |
| 10 | Primal Equation framing | Primal Equation, Abstract | Parallel to Paper II |
| 11 | Möbius Structural Equation | Möbius Strip, §3.3 | Parallel to emblem `[S/I]` |

**Net assessment:** Suda contributes 4 genuinely new `[A]`/`[S]` structures the Finity Papers lack (measurement protocols, continuous half-twist, PSL(2,ℝ) lift, Möbius control triad). The rest is convergent corroboration.

•   ⊙   ○
