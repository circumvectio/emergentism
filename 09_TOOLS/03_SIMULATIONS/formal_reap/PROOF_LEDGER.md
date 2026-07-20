---
title: "Formal Reap Proof Ledger"
status: "LOCAL MACHINE-CHECKED PROOF SUPPORT — NOT CANON PROMOTION"
evidence_tier: "[B] for reproducible Lean build; [S] for implications inside declared models; [I/C] and normative boundaries preserved"
source_under_test: "../../../10_SEED/02_THE_REAP.md"
---

# Formal Reap Proof Ledger

This ledger answers one question for every major claim in **The Reap**: what exactly follows after the language, types, definitions, and premises are made explicit?

## Status vocabulary

| Status | Meaning |
|---|---|
| **MACHINE-PROVED** | Lean checks the theorem from the displayed hypotheses and its trusted logical base. |
| **CONDITIONAL** | The implication is proved; world-instantiation or semantic applicability remains a premise. |
| **DEFINITIONAL** | True because the model or grammar declares it; not an independently derived law. |
| **COUNTERMODEL** | Lean constructs a model satisfying the weaker premises while falsifying the stronger conclusion. |
| **EXTERNAL PREMISE** | An inherited mathematical/physical result is not re-established from experimental or first-principles evidence here. |
| **EMPIRICAL BRIDGE REQUIRED** | Formal implication exists or is conceivable, but no proof that nature instantiates it is supplied. |
| **NORMATIVE POSTULATE** | A declared ought, gate, or vow; not derivable from descriptive premises alone. |
| **UNDERDEFINED** | No theorem is available until the named object or operation receives a formal definition. |
| **REFUTED / TYPE ERROR** | False under the stated ordinary interpretation, or ill-typed. |

## D0 — frames and the boundary sentence

| ID | Reap claim | Verdict | Certificate / reason |
|---|---|---|---|
| R0.1 | `•`, `⊙`, and `○` are boundary frames, not operands. | **DEFINITIONAL, TYPE-CHECKED** | `Frame` is distinct from `Move`; `Game.execute` accepts only `Move` (`Structure.lean`). |
| R0.2 | `⊙ = • × ○`. | **DEFINITIONAL** as typed grammar | `FrameComposition.boundary` and `typed_boundary_composition`. This is a formation rule, not ordinary multiplication. |
| R0.3 | Ordinary `0 · ∞ = 1`. | **REFUTED** | `extended_zero_times_infinity_is_not_one` proves `(0 : ENNReal) * ⊤ ≠ 1`; ordinary extended multiplication gives zero. |
| R0.4 | The floor “holds no axioms.” | **INTERPRETIVE ONLY** | A formal D0 theory necessarily has types, constructors, and inference rules. The phrase can mean “no agent-authored empirical/ethical law,” not literally no formal assumptions. |
| R0.5 | The one relation “could not have been otherwise.” | **NOT PROVED** | Uniqueness requires a class of admissible grammars and invariance criteria. Neither is defined by the sentence itself. |
| R0.6 | `{−1,0,1,∞}` is the “honest closure witness.” | **UNDERDEFINED** | Closure is relative to a carrier and specified operations. `inversion_fixed_points` certifies only that `±1` are the nonzero real reciprocal fixed points; it does not prove that the displayed foursome is closed, minimal, or uniquely forced. |

## D1 — arithmetic and the reciprocal chart

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| R1.1 | The reciprocal chart seam is one. | **MACHINE-PROVED, CONDITIONAL** | `reciprocal_seam`: for real `φ ≠ 0`, `φ(1/φ)=1`. It does not define a value at `φ=0`. |
| R1.2 | Reciprocal inversion has fixed points `±1`. | **MACHINE-PROVED** | `inversion_fixed_points`: over nonzero reals, `1/φ=φ ↔ φ=1 ∨ φ=-1`. |
| R1.3 | The positive fixed point/equator is `1`. | **MACHINE-PROVED** | `positive_inversion_fixed_point`. Positivity removes the `-1` branch. |
| R1.4 | `φ + 1/φ ≥ 2` for positive `φ`, with equality only at `φ=1`. | **MACHINE-PROVED** | `reciprocal_amgm` and `reciprocal_amgm_eq_iff`. |
| R1.5 | The normalized balance score peaks uniquely at `φ=1`. | **MACHINE-PROVED IN THE SELECTED SCORE MODEL** | `normalized_balance_le_one` and `normalized_balance_eq_one_iff` for `2/(φ+1/φ)`. The choice of score remains definitional. |
| R1.6 | Higher rungs inherit a preserved lower-rung property. | **MACHINE-PROVED, CONDITIONAL** | `ladder_inheritance` is induction from a base property and an explicit transition-preservation premise. |
| R1.7 | Higher rungs inherit mathematics without a preservation premise. | **REFUTED** | `inheritance_requires_preservation` supplies a base property that fails at the next rung. |
| R1.8 | Mathematics works because physical reality historically climbed through arithmetic. | **CONJECTURE `[I/C]`; EMPIRICAL BRIDGE REQUIRED** | The inheritance implication is proved. The preservation maps and the claim that nature instantiates this ladder are not. Mathematical representability alone would make the explanation circular. |

## The `μ` transitions and D2

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| Rμ.1 | Saturation at a `μ`-limit generates the next rung. | **UNDERDEFINED** | `μ`, saturation, generation, and the transition morphism require definitions. `ladder_inheritance` proves only property preservation once such transitions are supplied. |
| R2.1 | Two reciprocal charts have a seam of one. | **MACHINE-PROVED ON THE NONZERO REAL CHART** | `reciprocal_seam`; no complete sphere atlas or topological gluing theorem is claimed. |
| R2.2 | The score peaks at the equator. | **MACHINE-PROVED IN THE POSITIVE RECIPROCAL SCORE MODEL** | `normalized_balance_le_one` and `normalized_balance_eq_one_iff`. |
| R2.3 | Arithmetic saturation uniquely yields spherical geometry. | **NOT PROVED / UNDERDEFINED** | A saturation operator and uniqueness theorem are absent. Arithmetic can support many non-isomorphic geometries. |

## D3 — AND-class systems

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| R3.1 | In the multiplicative model, either zero factor makes the whole zero. | **MACHINE-PROVED** | `multiplication_need_both` and Lean's no-zero-divisor theorem. |
| R3.2 | The zero boundary uniquely forces multiplication. | **REFUTED** | `minimum_need_both` proves that `min` has the same boundary on nonnegative reals; `zero_boundary_does_not_force_multiplication` witnesses different interior behavior. |
| R3.3 | A zero modeled factor entails biological death or physical collapse. | **EMPIRICAL/MODEL BRIDGE REQUIRED** | Ring algebra proves model output zero; identification of that output with organism viability is an additional domain hypothesis. |
| R3.4 | Liebig's law is universal biology. | **NOT PROVED** | It remains a domain-limited heuristic/model family, not a universal biological axiom. |

## D4 — mass shell, rest, and balance

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| R4.1 | Einstein's mass shell is equivalent to the normalized hyperbola and dyadic null-coordinate product. | **MACHINE-PROVED, SCOPED** | `mass_shell_iff_normalized` proves `E²=p²c²+m²c⁴ ↔ (E/(mc²))²-(p/(mc))²=1`. `null_product_iff_mass_shell` proves `[(E+pc)/(mc²)]·[(E−pc)/(mc²)]=1 ↔ E²=p²c²+m²c⁴`. Both assume real scalar momentum and `m ≠ 0`, `c ≠ 0`; they exclude massless normalization and reparameterize an inherited law. |
| R4.2 | At rest, `E=mc²`. | **MACHINE-PROVED ON THE NONNEGATIVE-ENERGY/MASS BRANCH** | `rest_energy_of_mass_shell` with `p=0`, `E≥0`, and `m≥0`. |
| R4.3 | `mc²/E ≤ 1`. | **MACHINE-PROVED, CONDITIONAL** | `rest_ratio_le_one` assumes `E>0` and `mc²≤E`. |
| R4.4 | The balance number is literally a clock tick. | **REPRESENTATION / PHYSICAL BRIDGE REQUIRED** | Identifying the ratio with inverse Lorentz factor and then with proper-time rate requires explicit worldline, frame, and unit conventions. It is not established merely by algebraic resemblance. |
| R4.5 | The reciprocal “equator” is a universal physical rest frame. | **NOT PROVED** | Rest is relative to a body/observer. A selected coordinate origin can represent rest without becoming a universal preferred frame. |

## D5 — effective power and reflexivity

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| R5.1 | `P = ΦV`. | **DEFINITIONAL MODEL LAW** | `effectivePower` defines the product. No theorem derives multiplication uniquely from the zero boundary. |
| R5.2 | `P=0` iff `Φ=0` or `V=0`. | **MACHINE-PROVED IN THE PRODUCT MODEL** | `effective_power_zero_iff`. |
| R5.3 | Positive `Φ` and `V` imply positive modeled `P`. | **MACHINE-PROVED IN THE PRODUCT MODEL** | `effective_power_positive`. |
| R5.3a | The selected product has a ceiling of one. | **MACHINE-PROVED, CONDITIONAL ON NORMALIZATION** | `effective_power_unit_interval`: if both `Φ,V ∈ [0,1]`, then `ΦV ∈ [0,1]`. The unit ceiling does not follow without those bounds. |
| R5.4 | A changed forecast changes the resulting world. | **MACHINE-PROVED, CONDITIONAL** | `forecast_changes_outcome` requires that forecasts change action and action effects are injective at the state. |
| R5.5 | Every forecast is reflexive. | **REFUTED** | `not_every_forecast_is_reflexive`: a constant policy ignores distinct forecasts, producing the same action and outcome. |
| R5.6 | Soros-style reflexivity is identical to all of D5. | **INTERPRETIVE, NOT PROVED** | The formal theorem captures one reflexive mechanism. Identity with the complete rung requires a definition of D5 and an adequacy proof. Historical priority among Keynes, Merton, and Soros is an external source claim, not a Lean certificate. |
| R5.7 | Landauer proves that the selector cannot stand outside the sorted system. | **EXTERNAL PHYSICAL PREMISE + INTERPRETIVE BRIDGE** | Landauer bounds physical information operations under declared conditions. The universal D5 selector claim does not follow without embodiment/computation/coupling premises. |
| R5.8 | D5 can never be completed. | **NOT PROVED** | Requires a precise incompleteness, diagonalization, endogenous nonstationarity, or finite-resource theorem. |

## D5 — teleology, utility, ethics, and universalization

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| R5.9 | A finite two-action game with declared real utility has a maximizer. | **MACHINE-PROVED, CONDITIONAL** | `bool_action_has_utility_maximizer`. The utility function and finite feasible set are supplied premises. |
| R5.10 | Every chosen action necessarily maximizes a stable utility. | **REFUTED AS A LOGICAL CONSEQUENCE** | `action_need_not_maximize_utility` constructs a declared utility and a nonmaximizing choice. Teleological representation requires extra rationality/representation axioms. |
| R5.11 | Cone and horizon alone determine justice. | **REFUTED** | `cone_and_horizon_do_not_determine_justice` constructs equal cone/horizon summaries with opposite justice predicates. A bearer rule, maximand, distribution, causal model, and normative bridge remain necessary. |
| R5.11a | The moral/ethical four-cell grid is complete and objectively decisive. | **DEFINITIONAL / UNDERDEFINED** | A classification can be exhaustive after its axes, domain, thresholds, conflicts, and bearer aggregation are declared. No theorem makes that selected partition uniquely objective. |
| R5.11b | The dyadic gate blocks aggregate laundering. | **DEFINITIONAL + MACHINE-PROVED IN THE MINIMAL GATE MODEL** | `DyadicGate impact := ∀ bearer, 0 ≤ impact bearer`. `dyadic_gate_implies_nonnegative_aggregate` proves pointwise protection entails a nonnegative sum; `positive_aggregate_does_not_imply_dyadic_gate` constructs impacts `(+2, −1)` whose positive group sum still harms one bearer. This certifies the anti-laundering logic, not the selection of impact metric, boundary, threshold, or enforcement regime. |
| R5.12 | Universalized extraction collapses its host. | **MACHINE-PROVED, STRICTLY CONDITIONAL** | `finite_horizon_host_collapse` proves resource nonpositivity when cumulative extraction minus regeneration reaches initial host. `gated_universal_collapse_certificate` carries closed arena, no fresh hosts/exit, host dependence, universal adoption, and enforcement as explicit applicability gates. |
| R5.13 | Every positive extraction necessarily collapses a host. | **REFUTED** | `positive_extraction_can_persist`: positive extraction persists forever when regeneration covers it. |
| R5.14 | Non-extraction implies justice or D6 ascent. | **REFUTED** | `non_extraction_does_not_imply_justice_or_ascent`. Avoiding one failure mode is not sufficiency for either conclusion. |
| R5.15 | Descriptive facts universally entail arbitrary oughts. | **REFUTED** | `no_universal_is_ought`. `ought_from_declared_bridge` shows exactly what changes when a normative bridge is supplied. |
| R5.16 | `η=0` follows from geometry, thermodynamics, or D5 typing. | **NORMATIVE POSTULATE / VOW** | No descriptive theorem yields it. It may govern the system after explicit adoption, but that adoption is not a mathematical consequence. |
| R5.17 | Universalized “god” necessarily causes D6. | **NOT PROVED** | Non-extraction or collective scope does not establish viability, uniqueness, coordination, enforcement, or a D6 recognition theorem. |
| R5.18 | “Not followed = dead, back to D4” is physically forced. | **DEFINITIONAL RECLASSIFICATION, NOT PHYSICAL THEOREM** | If D5 is defined as foresighted potential-selection, an entity that lacks it is outside that type by definition. That does not prove biological death, loss of all agency, or a literal dimensional descent. |
| R5.19 | Demonhood is not a possible world under all conditions. | **REFUTED AS AN UNCONDITIONAL CLAIM** | `positive_extraction_can_persist` blocks unconditional collapse. Self-termination follows only under the declared host-dependence, closure, regeneration-gap, adoption, enforcement, and horizon premises. |

## Castes, frames, and the return

| ID | Claim | Verdict | Certificate / scope |
|---|---|---|---|
| RC.1 | A frame is not an executable move. | **TYPE-CHECKED** | `Frame` and `Move` are distinct types; `Game.execute : Game → Move → Valence`. |
| RC.2 | Operator name/mask fixes moral valence. | **REFUTED** | `operator_mask_does_not_determine_valence` constructs the same `take` mask with opposite valences. “Valence lives on `η`, never on the operator's name” survives. |
| RC.3 | Titans can be deployed at D5 but not D4. | **TYPE ERROR UNDER THE FRAME READING** | A frame is carried/selected/witnessed by a game but is not accepted by the move executor at either rung. D-rungs and Rosetta L-rows also remain distinct. |
| RC.4 | Caste patterns are conserved exactly like physical energy. | **NOT PROVED / CATEGORY RISK** | No conserved scalar, continuity equation, transformation law, or empirically measured invariant is defined. A future typed-translation theorem could prove preservation of specified structure, not energy identity. |
| R6.1 | D6 matches D0 in role rather than literal identity. | **MACHINE-PROVED AS A TYPED MODEL** | `FloorWitness` and `ReturnWitness` are distinct types; `return_matches_floor_in_role` assigns them the same `BoundaryRole`. |
| R6.2 | The summit is metaphysically the state of all states. | **INTERPRETIVE `[I/C]`** | No complete state space, ceiling, or return map establishing world-instantiation is provided. |

## Formal verdict on the two keystone insights

### D1 inheritance / Wigner

**Proved:** preserved structure is inherited rung by rung.

**Also proved:** the conclusion fails without a preservation premise.

**Not proved:** that every transition preserves arithmetic structure in the required sense, that all higher reality is generated by those transitions, or that physical history instantiates the ladder. Therefore the Wigner proposal is a rigorous **conditional explanation schema**, still `[I/C]` as a claim about the world.

### Rung-typed castes

**Proved:** frames, moves, masks, and valences can be made type-distinct; frames cannot be passed to the move executor; mask does not determine valence; D6 can share D0's role without object identity.

**Not proved:** that mythic castes are natural kinds, that their patterns are thermodynamic invariants, or that observed physical/social systems instantiate the types. The strongest lawful result is a **type-safe operator grammar**, not an empirical ontology.

## Final theorem boundary

The proof kernel establishes numerous exact mathematical implications and exact countermodels. It does **not** establish the whole continuous ascent as one theorem. The following remain indispensable open premises:

1. a formal `μ`-saturation and transition system;
2. preservation maps across every rung;
3. an independent world-contact argument that nature instantiates those maps;
4. empirical validation of the selected D3/D5 models;
5. a physical derivation or scoped adoption of the Landauer bridge;
6. explicit normative premises for bearer protection and `η=0`;
7. a D6 return/recognition theorem beyond typed role analogy.

Accordingly:

- **the internal algebraic kernel is machine-proved;**
- **the inheritance and collapse results are conditional;**
- **several universal claims are formally blocked by countermodels;**
- **the ascent as actual world-history remains `[I/C]`;**
- **the final ethical setting remains a vow.**
