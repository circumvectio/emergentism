from __future__ import annotations

import copy
import unittest

from kintsugi_kernel import (
    COMPASS_MUTATION_CODES,
    Issue,
    build_compass_contract,
    validate_compass_contract,
)


def replace_path(value: dict[str, object], path: tuple[str, ...], replacement: object) -> dict[str, object]:
    mutated = copy.deepcopy(value)
    cursor: dict[str, object] = mutated
    for component in path[:-1]:
        child = cursor[component]
        if not isinstance(child, dict):
            raise AssertionError(f"{component} is not an object")
        cursor = child
    cursor[path[-1]] = copy.deepcopy(replacement)
    return mutated


class CompassMutationContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = build_compass_contract()

    def test_canonical_draft_is_valid_pure_and_externally_uncalibrated(self) -> None:
        before = copy.deepcopy(self.contract)
        self.assertEqual(validate_compass_contract(self.contract), [])
        self.assertEqual(self.contract, before)
        self.assertEqual(self.contract["status"], "DRAFT_EXTERNALLY_UNCALIBRATED")
        second = build_compass_contract()
        second["status"] = "MUTATED"
        self.assertEqual(build_compass_contract()["status"], "DRAFT_EXTERNALLY_UNCALIBRATED")

    def mutation_matrix(self):
        inverted = copy.deepcopy(self.contract["registers"])
        inverted["d4"], inverted["d5"] = inverted["d5"], inverted["d4"]
        return (
            (
                "empirical_chart_inflation",
                ("chart", "scope"),
                "EMPIRICAL_CONSERVATION_LAW",
            ),
            (
                "product_uniqueness",
                ("nodePower", "universality"),
                "UNIQUELY_DERIVED_UNIVERSAL_LAW",
            ),
            (
                "forced_sevenfold_necessity",
                ("registers", "necessity"),
                "FORCED_NATURAL_DECOMPOSITION",
            ),
            (
                "missing_law_irreducibility",
                ("mu", "missingReduction"),
                "PROVES_IRREDUCIBILITY",
            ),
            (
                "d4_d5_inversion",
                ("registers",),
                inverted,
            ),
            (
                "scalar_sampling",
                ("quantum", "bornRule"),
                "SAMPLE_NORMALIZATION_SCALAR",
            ),
            (
                "quantum_dimension_stacking",
                ("quantum", "extraSpacetimeDimension"),
                True,
            ),
            (
                "forced_titans",
                ("titans", "role"),
                "FORCED_ONTOLOGICAL_GENERATORS",
            ),
            (
                "legacy_spelling",
                ("terminology", "canonical"),
                "Egregorotype",
            ),
            (
                "worldview_k2",
                ("authorization", "primitive"),
                "K2",
            ),
            (
                "physical_cone_expansion",
                ("soulLoop", "physicalCone"),
                "AGENT_WIDENED",
            ),
            (
                "physical_retrocausal_inflation",
                ("soulLoop", "futureInfluence"),
                "PHYSICAL_RETROCAUSAL_PULL",
            ),
            (
                "aggregate_ethical_laundering",
                ("ethics", "aggregateCompensation"),
                True,
            ),
            (
                "unconditional_power_max",
                ("powerMax", "unconditional"),
                True,
            ),
        )

    def test_exact_fourteen_fallacies_fail_closed_with_stable_diagnostics(self) -> None:
        mutations = self.mutation_matrix()
        expected = {
            "empirical_chart_inflation": Issue(
                "chart", "KIN-E-COMPASS-CHART", "chart identities are analytic facts only"
            ),
            "product_uniqueness": Issue(
                "nodePower", "KIN-E-COMPASS-AGGREGATOR",
                "the product is selected inside a non-interchangeable conjunctive family",
            ),
            "forced_sevenfold_necessity": Issue(
                "registers.sequence", "KIN-E-COMPASS-REGISTERS",
                "D0-D6 is a selected interpretive scaffold, not a forced decomposition",
            ),
            "missing_law_irreducibility": Issue(
                "mu.reductionStatus", "KIN-E-COMPASS-REDUCTION",
                "missing reduction records current non-reduction, not irreducibility",
            ),
            "d4_d5_inversion": Issue(
                "registers.modality", "KIN-E-COMPASS-MODALITY",
                "D4 is actual and D5 is possible",
            ),
            "scalar_sampling": Issue(
                "quantum.bornRule", "KIN-E-COMPASS-MEASURE",
                "Born probabilities sample outcomes from an event measure, never a scalar",
            ),
            "quantum_dimension_stacking": Issue(
                "quantum", "KIN-E-COMPASS-QUANTUM",
                "quantum interpretations are removable correspondences, not dimensions",
            ),
            "forced_titans": Issue(
                "titans", "KIN-E-COMPASS-TITANS",
                "Titan tokens are selected roles, not forced generators or arithmetic identities",
            ),
            "legacy_spelling": Issue(
                "terminology", "KIN-E-COMPASS-TERM",
                "Egregoreotype is canonical and Egregorotype is compatibility-only",
            ),
            "worldview_k2": Issue(
                "authorization", "KIN-E-COMPASS-AUTHORIZATION",
                "worldview accountability uses a complete authorization envelope, not K2",
            ),
            "physical_cone_expansion": Issue(
                "soulLoop.cones", "KIN-E-COMPASS-CONE",
                "the physical cone remains c-bounded while only modeled reach varies",
            ),
            "physical_retrocausal_inflation": Issue(
                "soulLoop.causality", "KIN-E-COMPASS-CAUSALITY",
                "represented futures influence present selection through models only",
            ),
            "aggregate_ethical_laundering": Issue(
                "ethics", "KIN-E-COMPASS-ETHICS",
                "aggregate gain cannot compensate for destroying either durable potential",
            ),
            "unconditional_power_max": Issue(
                "powerMax", "KIN-E-COMPASS-POWER-MAX",
                "Power-Max optimizes only inside the justice-constrained admissible set",
            ),
        }
        self.assertEqual(len(mutations), 14)
        self.assertEqual(
            list(COMPASS_MUTATION_CODES),
            [name for name, _, _ in mutations],
        )

        for name, path, replacement in mutations:
            with self.subTest(name=name):
                candidate = replace_path(self.contract, path, replacement)
                self.assertEqual(validate_compass_contract(candidate), [expected[name]])

    def test_combined_mutations_have_stable_complete_issue_order(self) -> None:
        candidate = self.contract
        for name, path, replacement in self.mutation_matrix():
            if name == "d4_d5_inversion":
                candidate = copy.deepcopy(candidate)
                registers = candidate["registers"]
                registers["d4"], registers["d5"] = registers["d5"], registers["d4"]
            else:
                candidate = replace_path(candidate, path, replacement)
        first = validate_compass_contract(candidate)
        second = validate_compass_contract(candidate)
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first))
        self.assertEqual(len(first), 14)
        self.assertEqual({issue.code for issue in first}, set(COMPASS_MUTATION_CODES.values()))

    def test_operational_contract_survives_quantum_inset_removal(self) -> None:
        without_quantum = copy.deepcopy(self.contract)
        without_quantum.pop("quantum")
        self.assertEqual(validate_compass_contract(without_quantum), [])

        operational = copy.deepcopy(self.contract)
        operational.pop("quantum")
        expected = copy.deepcopy(build_compass_contract())
        expected.pop("quantum")
        self.assertEqual(operational, expected)

    def test_unknown_fields_cannot_smuggle_a_second_semantic_contract(self) -> None:
        smuggled = copy.deepcopy(self.contract)
        smuggled["authorization"]["founderFallback"] = "enabled"
        self.assertIn(
            "KIN-E-COMPASS-SHAPE",
            {issue.code for issue in validate_compass_contract(smuggled)},
        )

    def test_public_api_is_closed_to_the_three_compass_symbols(self) -> None:
        import kintsugi_kernel

        for name in (
            "COMPASS_MUTATION_CODES",
            "build_compass_contract",
            "validate_compass_contract",
        ):
            self.assertIn(name, kintsugi_kernel.__all__)
            self.assertTrue(hasattr(kintsugi_kernel, name))

        with self.assertRaises(TypeError):
            COMPASS_MUTATION_CODES["smuggled"] = "KIN-E-SMUGGLED"


if __name__ == "__main__":
    unittest.main()
