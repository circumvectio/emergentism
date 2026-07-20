import FormalReap.Arithmetic
import FormalReap.Structure
import FormalReap.Ethics

/-!
`#print axioms` reports every axiom used by each exported certificate.  Mathlib
may report Lean's standard logical foundations (`propext`, `Classical.choice`,
`Quot.sound`); this project declares no domain axiom and permits no `sorry`.
-/

#print axioms FormalReap.Arithmetic.reciprocal_seam
#print axioms FormalReap.Arithmetic.positive_inversion_fixed_point
#print axioms FormalReap.Arithmetic.reciprocal_amgm
#print axioms FormalReap.Arithmetic.zero_boundary_does_not_force_multiplication
#print axioms FormalReap.Structure.ladder_inheritance
#print axioms FormalReap.Structure.inheritance_requires_preservation
#print axioms FormalReap.Structure.forecast_changes_outcome
#print axioms FormalReap.Structure.not_every_forecast_is_reflexive
#print axioms FormalReap.Structure.operator_mask_does_not_determine_valence
#print axioms FormalReap.Ethics.finite_horizon_host_collapse
#print axioms FormalReap.Ethics.positive_extraction_can_persist
#print axioms FormalReap.Ethics.non_extraction_does_not_imply_justice_or_ascent
#print axioms FormalReap.Ethics.no_universal_is_ought
