import Mathlib

/-!
# Scoped D5 collapse and is/ought boundaries

The host equation proves only a conditional finite-horizon result.  Separate
countermodels certify that extraction is not unconditionally self-defeating,
non-extraction does not entail justice or ascent, and descriptive truth does not
entail an arbitrary ought without a bridge premise.
-/

set_option autoImplicit false

namespace FormalReap.Ethics

open scoped BigOperators

/-- Linear closed-arena host accounting at a declared finite horizon. -/
def hostAfter
    (initialHost regeneration extraction : ℝ) (horizon : ℕ) : ℝ :=
  initialHost + (horizon : ℝ) * regeneration - (horizon : ℝ) * extraction

/-- Explicit semantic gates governing when the host equation may represent a game. -/
structure ArenaGates where
  closedArena : Prop
  noFreshHostsOrExit : Prop
  hostDependent : Prop
  universalAdoption : Prop
  enforcement : Prop

/-- All non-algebraic applicability gates hold. -/
def ArenaGates.Hold (gates : ArenaGates) : Prop :=
  gates.closedArena ∧
  gates.noFreshHostsOrExit ∧
  gates.hostDependent ∧
  gates.universalAdoption ∧
  gates.enforcement

/-- If cumulative net extraction exhausts the initial host, the modeled host is nonpositive. -/
theorem finite_horizon_host_collapse
    (initialHost regeneration extraction : ℝ) (horizon : ℕ)
    (hbudget : initialHost ≤ (horizon : ℝ) * (extraction - regeneration)) :
    hostAfter initialHost regeneration extraction horizon ≤ 0 := by
  unfold hostAfter
  nlinarith

/-- A certificate combines semantic applicability with the quantitative collapse proof. -/
theorem gated_universal_collapse_certificate
    (gates : ArenaGates)
    (initialHost regeneration extraction : ℝ) (horizon : ℕ)
    (hgates : gates.Hold)
    (hbudget : initialHost ≤ (horizon : ℝ) * (extraction - regeneration)) :
    gates.Hold ∧ hostAfter initialHost regeneration extraction horizon ≤ 0 := by
  exact ⟨hgates, finite_horizon_host_collapse
    initialHost regeneration extraction horizon hbudget⟩

/-- Positive extraction need not collapse a host when regeneration covers it. -/
theorem positive_extraction_can_persist :
    ∃ initialHost regeneration extraction : ℝ,
      0 < extraction ∧ extraction ≤ regeneration ∧
      ∀ horizon : ℕ, 0 < hostAfter initialHost regeneration extraction horizon := by
  refine ⟨1, 1, 1, by norm_num, le_rfl, ?_⟩
  intro horizon
  simp [hostAfter]

structure PolicyOutcome where
  extraction : ℝ
  just : Prop
  ascent : Prop

/-- The chosen model-level definition of non-extraction. -/
def NonExtractive (outcome : PolicyOutcome) : Prop := outcome.extraction = 0

/-- Avoiding extraction alone proves neither justice nor a higher-rung ascent. -/
theorem non_extraction_does_not_imply_justice_or_ascent :
    ∃ outcome : PolicyOutcome,
      NonExtractive outcome ∧ ¬ outcome.just ∧ ¬ outcome.ascent := by
  refine ⟨{ extraction := 0, just := False, ascent := False }, ?_⟩
  simp [NonExtractive]

/-- No arbitrary normative proposition follows from an arbitrary descriptive one. -/
theorem no_universal_is_ought :
    ¬ (∀ Is Ought : Prop, Is → Ought) := by
  intro bridge
  exact bridge True False True.intro

/-- Once a normative bridge is declared, its conclusion follows transparently. -/
theorem ought_from_declared_bridge
    (Is Ought : Prop) (fact : Is) (bridge : Is → Ought) : Ought :=
  bridge fact

/-- A finite action type with an explicitly supplied utility has a maximizer. -/
theorem bool_action_has_utility_maximizer (utility : Bool → ℝ) :
    ∃ action : Bool, ∀ alternative : Bool, utility alternative ≤ utility action := by
  by_cases h : utility false ≤ utility true
  · refine ⟨true, ?_⟩
    intro alternative
    cases alternative with
    | false => exact h
    | true => exact le_rfl
  · refine ⟨false, ?_⟩
    intro alternative
    cases alternative with
    | false => exact le_rfl
    | true => exact le_of_lt (lt_of_not_ge h)

/-- A chosen action need not maximize even a declared utility function. -/
theorem action_need_not_maximize_utility :
    ∃ utility : Bool → ℝ, ∃ chosen alternative : Bool,
      utility chosen < utility alternative := by
  refine ⟨(fun action => if action then 1 else 0), false, true, ?_⟩
  norm_num

structure EthicalSummary where
  cone : ℕ
  horizon : ℕ
  just : Prop

/-- Cone and horizon cannot determine justice unless a normative bridge is added. -/
theorem cone_and_horizon_do_not_determine_justice :
    ∃ first second : EthicalSummary,
      first.cone = second.cone ∧
      first.horizon = second.horizon ∧
      first.just ∧ ¬ second.just := by
  refine ⟨
    { cone := 1, horizon := 10, just := True },
    { cone := 1, horizon := 10, just := False },
    rfl,
    rfl,
    True.intro,
    ?_⟩
  simp

/-- The minimal dyadic gate: no declared impact-bearer has negative impact. -/
def DyadicGate {ι : Type*} (impact : ι → ℝ) : Prop :=
  ∀ bearer, 0 ≤ impact bearer

/-- Pointwise bearer protection entails a nonnegative aggregate. -/
theorem dyadic_gate_implies_nonnegative_aggregate
    {ι : Type*} [Fintype ι]
    (impact : ι → ℝ)
    (hgate : DyadicGate impact) :
    0 ≤ ∑ bearer, impact bearer := by
  exact Finset.sum_nonneg (fun bearer _ => hgate bearer)

def launderingCounterexample : Bool → ℝ
  | false => 2
  | true => -1

/-- A positive group sum does not imply the dyadic gate: one bearer may lose. -/
theorem positive_aggregate_does_not_imply_dyadic_gate :
    0 < ∑ bearer, launderingCounterexample bearer ∧
      ¬ DyadicGate launderingCounterexample := by
  constructor
  · norm_num [launderingCounterexample, Fintype.sum_bool]
  · intro hgate
    have hprotected := hgate true
    norm_num [launderingCounterexample] at hprotected

end FormalReap.Ethics
