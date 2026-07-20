import Mathlib

/-!
# Arithmetic and AND-class kernel

These theorems certify mathematics inside explicitly declared real-number models.
They do not establish that a physical or moral system instantiates those models.
-/

set_option autoImplicit false

namespace FormalReap.Arithmetic

/-- The reciprocal seam is a field theorem for a nonzero real coordinate. -/
theorem reciprocal_seam (φ : ℝ) (hφ : φ ≠ 0) : φ * (1 / φ) = 1 := by
  field_simp

/-- The only positive real fixed by reciprocal inversion is `1`. -/
theorem positive_inversion_fixed_point
    (φ : ℝ) (hφ : 0 < φ) (hfix : 1 / φ = φ) : φ = 1 := by
  have hφ0 : φ ≠ 0 := ne_of_gt hφ
  have hsquare : φ * φ = 1 := by
    calc
      φ * φ = (1 / φ) * φ := by rw [hfix]
      _ = 1 := by field_simp
  nlinarith

/-- AM-GM on the positive reciprocal chart. -/
theorem reciprocal_amgm (φ : ℝ) (hφ : 0 < φ) : 2 ≤ φ + 1 / φ := by
  have hφ0 : φ ≠ 0 := ne_of_gt hφ
  have hnonneg : 0 ≤ (φ - 1) ^ 2 / φ :=
    div_nonneg (sq_nonneg (φ - 1)) (le_of_lt hφ)
  have hid : (φ - 1) ^ 2 / φ = φ + 1 / φ - 2 := by
    field_simp [hφ0]
    <;> ring
  rw [hid] at hnonneg
  linarith

/-- The normalized reciprocal balance score is at most one. -/
theorem normalized_balance_le_one (φ : ℝ) (hφ : 0 < φ) :
    2 / (φ + 1 / φ) ≤ 1 := by
  have hden : 0 < φ + 1 / φ := add_pos hφ (one_div_pos.mpr hφ)
  exact (div_le_one hden).2 (reciprocal_amgm φ hφ)

/-- A binary operation has the AND-class zero boundary on nonnegative reals. -/
def NeedBoth (op : ℝ → ℝ → ℝ) : Prop :=
  ∀ a b : ℝ, 0 ≤ a → 0 ≤ b → (op a b = 0 ↔ a = 0 ∨ b = 0)

/-- Multiplication has the AND-class zero boundary. -/
theorem multiplication_need_both : NeedBoth (fun a b : ℝ => a * b) := by
  intro a b _ _
  exact mul_eq_zero

/-- Minimum has the same AND-class zero boundary on nonnegative reals. -/
theorem minimum_need_both : NeedBoth (fun a b : ℝ => min a b) := by
  intro a b ha hb
  constructor
  · intro h
    by_cases hab : a ≤ b
    · left
      simpa [min_eq_left hab] using h
    · right
      have hba : b ≤ a := le_of_not_ge hab
      simpa [min_eq_right hba] using h
  · intro h
    rcases h with rfl | rfl
    · simpa using (min_eq_left hb)
    · simpa using (min_eq_right ha)

/-- Zero-boundary behavior alone does not uniquely force multiplication. -/
theorem zero_boundary_does_not_force_multiplication :
    ∃ op : ℝ → ℝ → ℝ,
      NeedBoth op ∧ op 2 3 ≠ (2 : ℝ) * 3 := by
  refine ⟨(fun a b : ℝ => min a b), minimum_need_both, ?_⟩
  norm_num

end FormalReap.Arithmetic
