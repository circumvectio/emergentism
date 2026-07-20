import Mathlib

/-!
# D4 mass-shell normalization

This module proves the exact algebraic equivalence between Einstein's one-axis
mass-shell relation and the dimensionless hyperbola used by the Reap.  It does
not prove that the Reap discovered the physical law or that a geometric equator
is a universal rest frame.
-/

set_option autoImplicit false

namespace FormalReap.Physics

/-- Einstein's one-axis mass-shell relation. -/
def MassShell (energy momentum mass lightSpeed : ℝ) : Prop :=
  energy ^ 2 = momentum ^ 2 * lightSpeed ^ 2 + mass ^ 2 * lightSpeed ^ 4

/-- The dimensionless hyperbola after `e = E/(mc²)` and `q = p/(mc)`. -/
def NormalizedMassShell (energy momentum mass lightSpeed : ℝ) : Prop :=
  (energy / (mass * lightSpeed ^ 2)) ^ 2 -
    (momentum / (mass * lightSpeed)) ^ 2 = 1

/-- Future/past null coordinates of one-axis four-momentum in rest-mass units. -/
noncomputable def forwardNull (energy momentum mass lightSpeed : ℝ) : ℝ :=
  (energy + momentum * lightSpeed) / (mass * lightSpeed ^ 2)

noncomputable def backwardNull (energy momentum mass lightSpeed : ℝ) : ℝ :=
  (energy - momentum * lightSpeed) / (mass * lightSpeed ^ 2)

/-- For nonzero mass and light speed, the two equations are algebraically equivalent. -/
theorem mass_shell_iff_normalized
    (energy momentum mass lightSpeed : ℝ)
    (hmass : mass ≠ 0) (hc : lightSpeed ≠ 0) :
    MassShell energy momentum mass lightSpeed ↔
      NormalizedMassShell energy momentum mass lightSpeed := by
  unfold MassShell NormalizedMassShell
  constructor
  · intro h
    field_simp [hmass, hc]
    nlinarith [h]
  · intro h
    field_simp [hmass, hc] at h
    nlinarith [h]

/-- The dyadic null-coordinate product is exactly the mass-shell equation. -/
theorem null_product_iff_mass_shell
    (energy momentum mass lightSpeed : ℝ)
    (hmass : mass ≠ 0) (hc : lightSpeed ≠ 0) :
    forwardNull energy momentum mass lightSpeed *
        backwardNull energy momentum mass lightSpeed = 1 ↔
      MassShell energy momentum mass lightSpeed := by
  constructor
  · intro hproduct
    unfold forwardNull backwardNull MassShell at *
    field_simp [hmass, hc] at hproduct
    nlinarith
  · intro hshell
    unfold forwardNull backwardNull MassShell at *
    field_simp [hmass, hc]
    nlinarith

/-- At zero momentum, the nonnegative-energy/nonnegative-mass branch has `E = mc²`. -/
theorem rest_energy_of_mass_shell
    (energy mass lightSpeed : ℝ)
    (henergy : 0 ≤ energy) (hmass : 0 ≤ mass)
    (h : MassShell energy 0 mass lightSpeed) :
    energy = mass * lightSpeed ^ 2 := by
  unfold MassShell at h
  norm_num at h
  have hrest : 0 ≤ mass * lightSpeed ^ 2 :=
    mul_nonneg hmass (sq_nonneg lightSpeed)
  nlinarith [h]

/-- The selected rest-energy ratio is bounded under positive energy and `mc² ≤ E`. -/
noncomputable def restRatio (energy mass lightSpeed : ℝ) : ℝ :=
  mass * lightSpeed ^ 2 / energy

/-- `mc²/E ≤ 1` follows from positive energy and `mc² ≤ E`. -/
theorem rest_ratio_le_one
    (energy mass lightSpeed : ℝ)
    (henergy : 0 < energy)
    (hrest : mass * lightSpeed ^ 2 ≤ energy) :
    restRatio energy mass lightSpeed ≤ 1 := by
  exact (div_le_one henergy).2 hrest

end FormalReap.Physics
