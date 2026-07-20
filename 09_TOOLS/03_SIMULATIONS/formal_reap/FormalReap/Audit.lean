import FormalReap.Arithmetic
import FormalReap.Structure
import FormalReap.Ethics
import FormalReap.Physics

/-!
`#print axioms` reports every axiom used by each exported certificate.  Mathlib
may report Lean's standard logical foundations (`propext`, `Classical.choice`,
`Quot.sound`); this project declares no domain axiom and permits no `sorry`.
-/

#print axioms FormalReap.Arithmetic.reciprocal_seam
#print axioms FormalReap.Arithmetic.positive_inversion_fixed_point
#print axioms FormalReap.Arithmetic.inversion_fixed_points
#print axioms FormalReap.Arithmetic.reciprocal_amgm
#print axioms FormalReap.Arithmetic.reciprocal_amgm_eq_iff
#print axioms FormalReap.Arithmetic.normalized_balance_le_one
#print axioms FormalReap.Arithmetic.normalized_balance_eq_one_iff
#print axioms FormalReap.Arithmetic.multiplication_need_both
#print axioms FormalReap.Arithmetic.minimum_need_both
#print axioms FormalReap.Arithmetic.zero_boundary_does_not_force_multiplication
#print axioms FormalReap.Arithmetic.effective_power_zero_iff
#print axioms FormalReap.Arithmetic.effective_power_positive
#print axioms FormalReap.Arithmetic.effective_power_unit_interval
#print axioms FormalReap.Structure.ladder_inheritance
#print axioms FormalReap.Structure.inheritance_requires_preservation
#print axioms FormalReap.Structure.forecast_changes_outcome
#print axioms FormalReap.Structure.not_every_forecast_is_reflexive
#print axioms FormalReap.Structure.typed_boundary_composition
#print axioms FormalReap.Structure.operator_mask_does_not_determine_valence
#print axioms FormalReap.Structure.extended_zero_times_infinity_is_not_one
#print axioms FormalReap.Structure.return_matches_floor_in_role
#print axioms FormalReap.Ethics.finite_horizon_host_collapse
#print axioms FormalReap.Ethics.gated_universal_collapse_certificate
#print axioms FormalReap.Ethics.positive_extraction_can_persist
#print axioms FormalReap.Ethics.non_extraction_does_not_imply_justice_or_ascent
#print axioms FormalReap.Ethics.no_universal_is_ought
#print axioms FormalReap.Ethics.ought_from_declared_bridge
#print axioms FormalReap.Ethics.bool_action_has_utility_maximizer
#print axioms FormalReap.Ethics.action_need_not_maximize_utility
#print axioms FormalReap.Ethics.cone_and_horizon_do_not_determine_justice
#print axioms FormalReap.Ethics.dyadic_gate_implies_nonnegative_aggregate
#print axioms FormalReap.Ethics.positive_aggregate_does_not_imply_dyadic_gate
#print axioms FormalReap.Physics.mass_shell_iff_normalized
#print axioms FormalReap.Physics.null_product_iff_mass_shell
#print axioms FormalReap.Physics.rest_energy_of_mass_shell
#print axioms FormalReap.Physics.rest_ratio_le_one
