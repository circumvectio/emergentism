import Mathlib

/-!
# Conditional inheritance, reflexivity, and typed frames

Theorems in this module expose the premises required by three Reap claims.
Countermodels make clear that the conclusions do not follow without those premises.
-/

set_option autoImplicit false

namespace FormalReap.Structure

/-- A property carried at the base and preserved at each transition is inherited. -/
theorem ladder_inheritance
    (P : ℕ → Prop)
    (base : P 0)
    (preserve : ∀ n : ℕ, P n → P (n + 1)) :
    ∀ n : ℕ, P n := by
  intro n
  induction n with
  | zero => exact base
  | succ n ih => simpa [Nat.succ_eq_add_one] using preserve n ih

/-- A base property need not survive even one rung without a preservation law. -/
theorem inheritance_requires_preservation :
    ∃ P : ℕ → Prop, P 0 ∧ ¬ P 1 := by
  refine ⟨(fun n : ℕ => n = 0), rfl, ?_⟩
  norm_num

/-- A minimal embodied-foresight model: forecasts select actions; actions affect worlds. -/
structure ForesightSystem (World Forecast Action : Type) where
  policy : Forecast → Action
  evolve : World → Action → World

/-- The world reached after acting on a forecast. -/
def outcome {World Forecast Action : Type}
    (system : ForesightSystem World Forecast Action)
    (world : World) (forecast : Forecast) : World :=
  system.evolve world (system.policy forecast)

/-- Forecast changes alter outcomes when they alter action and action effects are injective. -/
theorem forecast_changes_outcome
    {World Forecast Action : Type}
    (system : ForesightSystem World Forecast Action)
    (world : World) (f₁ f₂ : Forecast)
    (hpolicy : system.policy f₁ ≠ system.policy f₂)
    (heffect : Function.Injective (system.evolve world)) :
    outcome system world f₁ ≠ outcome system world f₂ := by
  intro hout
  apply hpolicy
  apply heffect
  exact hout

/-- A policy may ignore every forecast, so reflexivity is not automatic. -/
def constant_policy_system : ForesightSystem Unit Bool Bool where
  policy := fun _ => false
  evolve := fun _ action => action

/-- Distinct forecasts can yield the same action and outcome. -/
theorem not_every_forecast_is_reflexive :
    true ≠ false ∧
    constant_policy_system.policy true = constant_policy_system.policy false ∧
    outcome constant_policy_system () true = outcome constant_policy_system () false := by
  decide

/-- Boundary frames are a separate type from executable moves. -/
inductive Frame where
  | void
  | unit
  | infinity
  deriving DecidableEq, Repr

/-- An operator name or mask is not its moral valence. -/
inductive OperatorMask where
  | give
  | take
  | preserve
  | transform
  deriving DecidableEq, Repr

inductive Valence where
  | nonExtractive
  | extractive
  deriving DecidableEq, Repr

structure Move where
  mask : OperatorMask
  valence : Valence
  deriving DecidableEq, Repr

/-- A game carries a frame, but its executor accepts a `Move`, never a `Frame`. -/
structure Game where
  frame : Frame
  legal : Move → Prop

/-- The type signature is the machine-checked frame/move deployment fence. -/
def Game.execute (_game : Game) (move : Move) : Valence := move.valence

/-- One operator mask can carry opposite valences; the mask does not judge the move. -/
theorem operator_mask_does_not_determine_valence :
    ∃ first second : Move,
      first.mask = second.mask ∧ first.valence ≠ second.valence := by
  refine ⟨
    { mask := .take, valence := .nonExtractive },
    { mask := .take, valence := .extractive },
    rfl,
    ?_⟩
  decide

end FormalReap.Structure
