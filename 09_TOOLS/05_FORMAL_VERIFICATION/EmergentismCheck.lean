/-
  Machine-check of the Emergentism `[A]` claim set — docs 45–51.
  Receipt 173 found the corpus had never submitted a claim to an oracle outside
  itself. This file is that submission. Lean 4 + mathlib.

  There is no `sorry` in this file. Anything not proved is listed in §7 as
  unchecked, rather than stubbed and counted as checked.
-/
import Mathlib

set_option linter.style.header false
set_option linter.unusedVariables false

namespace Emergentism

/-! ## 1 · The field boundary — doc 48 §2 (T-A) -/

/-- **T-A.** For `a ≠ 0` there is no `y` with `0 * y = a`.
The corpus insists `a/0` is *no such element*, not merely *undefined*.
Note mathlib **defines** `a / 0 = 0` as a junk value — which is exactly why the
corpus's distinction matters: the junk value is a convention, not a solution. -/
theorem no_quotient_by_zero {K : Type*} [Field K] (a : K) (ha : a ≠ 0) :
    ¬ ∃ y : K, 0 * y = a := by
  rintro ⟨y, hy⟩
  rw [zero_mul] at hy
  exact ha hy.symm

/-- mathlib's junk value, recorded so the distinction above is not lost. -/
theorem mathlib_assigns_junk (a : ℝ) : a / 0 = 0 := div_zero a

/-! ## 2 · Inversion and its fixed points — FV-06, FV-07 -/

/-- **FV-07.** Inversion `ι(x) = 1/x` fixes exactly `±1`. -/
theorem inversion_fixed_iff (x : ℝ) (hx : x ≠ 0) : x⁻¹ = x ↔ x = 1 ∨ x = -1 := by
  constructor
  · intro h
    have hxx : x * x = 1 := by
      field_simp at h
      linarith [h]
    have : (x - 1) * (x + 1) = 0 := by nlinarith [hxx]
    rcases mul_eq_zero.mp this with h1 | h2
    · exact Or.inl (by linarith)
    · exact Or.inr (by linarith)
  · rintro (rfl | rfl) <;> norm_num

/-- **FV-06.** On the positive ray only `+1` survives — the unique positive
fixed point of inversion. This is why Suda's chart, living on `ℝ₊`, cannot
see `−1`. -/
theorem unique_positive_fixed_point (x : ℝ) (hx : 0 < x) : x⁻¹ = x ↔ x = 1 := by
  rw [inversion_fixed_iff x (ne_of_gt hx)]
  constructor
  · rintro (h | h)
    · exact h
    · exfalso; rw [h] at hx; linarith
  · exact Or.inl

/-- **The orbit identity — doc 45 §5.** `x` and `ι(x)` multiply to `1` for every
nonzero `x`. The factors are *bound*, not free, so no indeterminate form arises
anywhere along the orbit. -/
theorem orbit_product (x : ℝ) (hx : x ≠ 0) : x * x⁻¹ = 1 := mul_inv_cancel₀ hx

/-! ## 3 · The keel is the complementary-angle rule — the Thales construction -/

/-- **The keel identity.** `φ · ν = 1` *is* the statement that the two acute
angles of a right triangle are complementary: with `ν = tan A` and
`φ = tan(π/2 − A)`, the product is `1`.

This is the elementary form of the corpus's keel — checkable with a protractor,
and requiring none of the framework to state. -/
theorem keel_is_complementary_angles (A : ℝ) (h : Real.tan A ≠ 0) :
    Real.tan A * Real.tan (Real.pi / 2 - A) = 1 := by
  rw [Real.tan_pi_div_two_sub]
  exact mul_inv_cancel₀ h

/-- **T2, the projection at 45°.** The construction sends `A = π/4` to exactly
`1` — the ι-fixed point, and the centre of the whole structure. -/
theorem projection_at_45 : Real.tan (Real.pi / 4) = 1 := Real.tan_pi_div_four

/-! ## 4 · `E(x) = (log x)²` is minimal exactly at `x = 1` — Suda's metric -/

/-- **S-3.** The inversion-invariant energy vanishes only at unity, and is
strictly positive elsewhere on the positive ray. -/
theorem energy_min_at_one (x : ℝ) (hx : 0 < x) :
    0 ≤ (Real.log x) ^ 2 ∧ ((Real.log x) ^ 2 = 0 ↔ x = 1) := by
  refine ⟨sq_nonneg _, ?_⟩
  constructor
  · intro h
    have hlog : Real.log x = 0 := by nlinarith [sq_nonneg (Real.log x)]
    have := Real.exp_log hx
    rw [hlog, Real.exp_zero] at this
    exact this.symm
  · rintro rfl; simp

/-- **S-3, invariance.** `E` is unchanged by inversion — the metric is symmetric
about the fixed point. -/
theorem energy_inversion_invariant (x : ℝ) (hx : 0 < x) :
    (Real.log x⁻¹) ^ 2 = (Real.log x) ^ 2 := by
  rw [Real.log_inv]; ring

/-! ## 5 · The `F2` correction — "exactly one identity" was published, and false -/

/-- **The corrected `I1`.** A structure has *at most* one two-sided identity.
Uniqueness is the theorem. -/
theorem at_most_one_identity {M : Type*} [Mul M] (e e' : M)
    (he : ∀ x : M, e * x = x ∧ x * e = x)
    (he' : ∀ x : M, e' * x = x ∧ x * e' = x) : e = e' := by
  have h1 : e * e' = e' := (he e').1
  have h2 : e * e' = e := (he' e).2
  rw [← h1, h2]

/-- **Existence is NOT forced — the counterexample that killed the published `F2`.**
The constant operation on `Bool` has no two-sided identity, so
"a multiplicative structure has exactly one identity" is false. Existence is a
gift of the selected object, not a theorem about structures. -/
theorem existence_not_forced :
    ¬ ∃ e : Bool, ∀ x : Bool, (false && e) = x ∧ (false && x) = x := by
  rintro ⟨e, he⟩
  have h := (he true).1
  simp at h

/-! ## 6 · The two involutions are dual — doc 42 §6A -/

/-- Negation fixes `0`. -/
theorem negation_fixes_zero : -(0:ℝ) = 0 := neg_zero

/-- Negation swaps the ι-fixed points `±1`. -/
theorem negation_swaps_units : -(1:ℝ) = -1 ∧ -(-1:ℝ) = 1 := ⟨rfl, neg_neg 1⟩

/-- Inversion fixes `±1` — so each involution fixes exactly what the other moves.
`fix(ι) = {+1,−1}` while `fix(neg) = {0}` on the affine line. -/
theorem inversion_fixes_units : (1:ℝ)⁻¹ = 1 ∧ (-1:ℝ)⁻¹ = -1 := by
  constructor <;> norm_num

/-- The two involutions **commute** — which is what makes `{id, neg, ι, neg∘ι}`
a Klein four-group. -/
theorem involutions_commute (x : ℝ) : (-x)⁻¹ = -(x⁻¹) := by
  rw [inv_neg]

/-! ## 7 · NOT CHECKED HERE — stated so this file cannot be over-read

* **No ontological, ethical, teleological or cosmological claim.** None is
  formalisable and none is asserted. The keel above is analytic and empty of
  world; that fence is inherited verbatim.
* **The dimension counts underwriting the μ-criterion** (`ℝ→ℝP¹` 1→1,
  `ℂ→ℂP¹` 2→2, `ℝP¹→Ĉ` 1→2) are NOT formalised. They are what the whole ladder
  census rests on, and doc 48 is currently *inconsistent* about which notion of
  dimension it means. That owner ruling (HR-1) is owed before formalising them.
* **"`Ĉ` is not a ring" — NOW CHECKED, in §8, with its scope stated.** What is
  proved is the *structural reason*: no nontrivial ring admits an additively
  absorbing element, and the point at infinity must absorb. What is NOT proved is
  a statement about mathlib's `Projectivization` as an object — `ℂP¹` is never
  constructed here. The corpus's claim is the reason; the reason is machine-checked.
* **Suda's hinge `= tanh(log x / 2)`** verified numerically to 1e-12 but not
  proved here.
* **The Lorentz–Möbius correspondence** (doc 49) is inherited standard physics
  and is not re-derived.
-/

/-! ## 8 · The associativity falsifier and the projective type boundary

`KSC-04` retired the attempted Titan equations. The argument below shows that
the proposed pole product collapses any nontrivial ring. Observing that `Ĉ` is
not a ring does not restore that product: global multiplication is unavailable
there, and TitanFrame is a separate opaque type. The lawful survivors are only
the separately typed numeric reciprocal and projective inversion facts. -/

/-- **The canon's falsifier, formalised — and it is VALID.**
Given a total associative multiplication, an element `w` with `0 * w = 1`, and
the ring facts `2 * 0 = 0` and `2 * 1 = 2`, one derives `1 = 2`.

So the corpus was right to retire the attempted equation as ring arithmetic;
the type firewall also forbids recasting it as Titan arithmetic. -/
theorem associativity_falsifier {R : Type*} [Mul R] [Zero R] [One R]
    (assoc : ∀ a b c : R, a * b * c = a * (b * c))
    (two : R) (h20 : two * 0 = 0) (h21 : two * 1 = two)
    (w : R) (h0w : 0 * w = 1) :
    (1 : R) = two := by
  have h := assoc two 0 w
  rw [h20, h0w, h21] at h
  exact h

/-- **And the falsifier's own hypothesis is already impossible in any ring.**
`0 * w = 0` holds for every `w`, so `0 * w = 1` forces `1 = 0`. The falsifier
never needed associativity: its premise collapses a nontrivial ring on contact. -/
theorem falsifier_premise_impossible {R : Type*} [Ring R] [Nontrivial R] (w : R) :
    0 * w ≠ 1 := by
  rw [zero_mul]
  exact zero_ne_one

/-- **The reason no ring can carry a point at infinity.**
`∞` must absorb addition — `∞ + 1 = ∞`. In a ring that forces `1 = 0`. -/
theorem no_additive_absorber {R : Type*} [Ring R] (w : R) (h : w + 1 = w) :
    (1 : R) = 0 := by
  have h' : w + 1 = w + 0 := by rw [add_zero]; exact h
  exact add_left_cancel h'

/-- **`Ĉ` IS NOT A RING — the statement, machine-checked.**
No nontrivial ring contains an additively absorbing element. Since the point at
infinity of `Ĉ` absorbs addition, no nontrivial ring structure carries it, and
the falsifier's premise (ii) is unavailable. **The derivation never starts.** -/
theorem no_absorber_in_nontrivial_ring {R : Type*} [Ring R] [Nontrivial R] :
    ¬ ∃ w : R, w + 1 = w := by
  rintro ⟨w, hw⟩
  exact one_ne_zero (no_additive_absorber w hw)

/-- Cancellation is what does the work, and `ℂ` has it — so `ℂ` itself admits
no absorber. Recorded so the claim is anchored to the corpus's actual chart. -/
theorem complex_has_no_absorber : ¬ ∃ w : ℂ, w + 1 = w :=
  no_absorber_in_nontrivial_ring

end Emergentism
