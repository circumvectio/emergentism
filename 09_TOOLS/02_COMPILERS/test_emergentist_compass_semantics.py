#!/usr/bin/env python3
"""Independent semantic acceptance tests for the Emergentist Compass.

This vessel deliberately does not import the Burri renderer.  It checks the
small formal models named by the repaired source owners and binds every
fallacy mutation to an owner-side repair marker.  All examples are finite,
deterministic, and use only the Python standard library.
"""

from __future__ import annotations

import json
import math
import re
import unittest
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable, Mapping, Optional, Sequence


ROOT = Path(__file__).resolve().parents[2]


def owner_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Analytic chart and conjunctive-family reference models


def reciprocal_chart(theta: float) -> tuple[float, float, float]:
    if not 0.0 < theta < math.pi:
        raise ValueError("the reciprocal chart requires theta in (0, pi)")
    phi = 1.0 / math.tan(theta / 2.0)
    nu = math.tan(theta / 2.0)
    balance = 2.0 / (phi + nu)
    return phi, nu, balance


def product(phi: float, viability: float) -> float:
    return phi * viability


def minimum(phi: float, viability: float) -> float:
    return min(phi, viability)


def harmonic(phi: float, viability: float) -> float:
    if phi == 0.0 or viability == 0.0:
        return 0.0
    return 2.0 * phi * viability / (phi + viability)


def cobb_douglas(phi: float, viability: float, alpha: float = 0.5) -> float:
    if not 0.0 < alpha < 1.0:
        raise ValueError("a conjunctive Cobb-Douglas exponent must lie in (0, 1)")
    return phi**alpha * viability ** (1.0 - alpha)


AGGREGATORS: tuple[Callable[[float, float], float], ...] = (
    product,
    minimum,
    harmonic,
    cobb_douglas,
)


class AnalyticAndAggregatorTests(unittest.TestCase):
    def test_reciprocal_identity_am_gm_and_balance_on_open_domain(self) -> None:
        for theta in (0.01, 0.2, 0.7, math.pi / 2.0, 2.4, math.pi - 0.01):
            with self.subTest(theta=theta):
                phi, nu, balance = reciprocal_chart(theta)
                self.assertAlmostEqual(phi * nu, 1.0, places=12)
                self.assertGreaterEqual(phi + nu + 1e-12, 2.0)
                self.assertAlmostEqual(balance, math.sin(theta), places=12)
                self.assertGreater(balance, 0.0)
                self.assertLessEqual(balance, 1.0 + 1e-12)

    def test_reciprocal_chart_excludes_both_poles(self) -> None:
        for theta in (-1.0, 0.0, math.pi, math.pi + 1.0):
            with self.subTest(theta=theta):
                with self.assertRaises(ValueError):
                    reciprocal_chart(theta)

    def test_am_gm_equality_is_only_at_the_equator_in_samples(self) -> None:
        equator = reciprocal_chart(math.pi / 2.0)
        self.assertAlmostEqual(equator[0], 1.0)
        self.assertAlmostEqual(equator[1], 1.0)
        self.assertAlmostEqual(equator[0] + equator[1], 2.0)
        for theta in (0.2, 0.8, 2.0, 2.9):
            phi, nu, _ = reciprocal_chart(theta)
            self.assertGreater(phi + nu, 2.0)

    def test_declared_conjunctive_family_boundaries_and_monotonicity(self) -> None:
        grid = (0.0, 0.1, 0.4, 0.8, 1.0)
        for aggregator in AGGREGATORS:
            with self.subTest(aggregator=aggregator.__name__):
                self.assertEqual(aggregator(0.0, 0.8), 0.0)
                self.assertEqual(aggregator(0.8, 0.0), 0.0)
                self.assertAlmostEqual(aggregator(1.0, 1.0), 1.0)
                for fixed in grid:
                    along_phi = [aggregator(x, fixed) for x in grid]
                    along_viability = [aggregator(fixed, y) for y in grid]
                    self.assertEqual(along_phi, sorted(along_phi))
                    self.assertEqual(along_viability, sorted(along_viability))

    def test_admissible_aggregators_are_not_ranking_equivalent(self) -> None:
        candidate_a = (0.2, 1.0)
        candidate_b = (0.4, 0.4)
        self.assertGreater(product(*candidate_a), product(*candidate_b))
        self.assertLess(minimum(*candidate_a), minimum(*candidate_b))
        self.assertLess(harmonic(*candidate_a), harmonic(*candidate_b))
        self.assertGreater(cobb_douglas(*candidate_a), cobb_douglas(*candidate_b))
        self.assertLess(
            cobb_douglas(*candidate_a, alpha=0.8),
            cobb_douglas(*candidate_b, alpha=0.8),
        )


# ---------------------------------------------------------------------------
# Soul Loop, represented futures, and option cones


@dataclass(frozen=True)
class AuthorizationEnvelope:
    principal: str
    mandate: str
    scope: str
    consent: bool
    custody: str
    expiry_or_revocation: str
    contest_path: str
    actor: str
    consequence_bearers: tuple[str, ...]

    def complete(self) -> bool:
        textual = (
            self.principal,
            self.mandate,
            self.scope,
            self.custody,
            self.expiry_or_revocation,
            self.contest_path,
            self.actor,
        )
        return self.consent and all(textual) and bool(self.consequence_bearers)


@dataclass(frozen=True)
class AuthorizationAssessment:
    status: str
    envelope: Optional[AuthorizationEnvelope]
    reasons: tuple[str, ...] = ()
    nonconsequential_scope: bool = False

    def validated_status(self) -> str:
        if self.status == "valid":
            if (
                self.envelope is None
                or not self.envelope.complete()
                or self.reasons
                or self.nonconsequential_scope
            ):
                raise ValueError("valid requires a complete envelope and no defects")
        elif self.status == "invalid":
            if self.envelope is None or not self.reasons or self.nonconsequential_scope:
                raise ValueError("invalid requires a supplied record and defects")
        elif self.status == "absent":
            if self.envelope is not None or not self.reasons or self.nonconsequential_scope:
                raise ValueError("absent requires a null envelope and reasons")
        elif self.status == "not_required":
            if self.envelope is not None or self.reasons or not self.nonconsequential_scope:
                raise ValueError("not_required is confined to nonconsequential scope")
        else:
            raise ValueError("unknown authorization status")
        return self.status

    def valid(self) -> bool:
        return self.validated_status() == "valid"


@dataclass(frozen=True)
class CommitmentReceipt:
    receipt_type: str
    status: str
    selected_option_id: Optional[str]
    attempted_action_id: Optional[str]
    expected_outcome: Optional[str]
    actor: str
    physical_availability: str
    authorization_status: str


@dataclass(frozen=True)
class OutcomeReceipt:
    receipt_type: str
    receipt_cause: str
    attempted_action_id: Optional[str]
    performed_action_id: Optional[str]
    observed_outcome: str
    environment_state_before: int
    environment_state_after: int


def select_action(
    action_weights: Mapping[str, float],
    means: Mapping[str, float],
    admissible_actions: set[str],
    authorization: AuthorizationAssessment,
    *,
    governed: bool = False,
) -> tuple[Optional[str], CommitmentReceipt]:
    authorization_status = authorization.validated_status()
    executable = sorted(
        action
        for action in admissible_actions
        if means.get(action, 0.0) > 0.0 and action in action_weights
    )
    if not executable:
        actor = authorization.envelope.actor if authorization.envelope else "unknown"
        return None, CommitmentReceipt(
            "commitment",
            "unavailable",
            None,
            None,
            None,
            actor,
            "unavailable",
            authorization_status,
        )
    selected = max(executable, key=lambda action: action_weights[action])
    actor = authorization.envelope.actor if authorization.envelope else "unknown"
    if governed and authorization_status in {"invalid", "absent"}:
        return None, CommitmentReceipt(
            "commitment",
            "refused",
            selected,
            None,
            None,
            actor,
            "available",
            authorization_status,
        )
    expected = "advanced" if selected == "advance" else f"completed:{selected}"
    return selected, CommitmentReceipt(
        "commitment",
        {
            "valid": "authorized_committed",
            "invalid": "unauthorized_attempt",
            "absent": "unauthorized_attempt",
            "not_required": "nonconsequential_attempt",
        }[authorization_status],
        selected,
        selected,
        expected,
        actor,
        "available",
        authorization_status,
    )


def environment_transition(
    state: int, action: str, *, veto: bool = False
) -> tuple[int, OutcomeReceipt]:
    if veto:
        return state, OutcomeReceipt(
            "outcome", "action_attempt", action, None, "vetoed", state, state
        )
    next_state = state + 1
    observed = "advanced" if action == "advance" else f"completed:{action}"
    return next_state, OutcomeReceipt(
        "outcome", "action_attempt", action, action, observed, state, next_state
    )


def ambient_observation(state_before: int, state_after: int) -> OutcomeReceipt:
    return OutcomeReceipt(
        "outcome",
        "ambient_observation",
        None,
        None,
        "ambient-change",
        state_before,
        state_after,
    )


def loop_update(
    model: dict[str, object],
    selector: dict[str, object],
    commitment: CommitmentReceipt,
    outcome: Optional[OutcomeReceipt],
) -> tuple[dict[str, object], dict[str, object]]:
    if outcome is None:
        return model, selector
    next_model = dict(model)
    next_selector = dict(selector)
    next_model["receipt_count"] = int(next_model.get("receipt_count", 0)) + 1
    next_model["last_observed"] = outcome.observed_outcome
    if commitment.expected_outcome != outcome.observed_outcome:
        next_selector["revision_count"] = int(
            next_selector.get("revision_count", 0)
        ) + 1
    return next_model, next_selector


def represented_future_distribution(flood_probability: float) -> dict[str, float]:
    if not 0.0 <= flood_probability <= 1.0:
        raise ValueError("probability must be normalized")
    return {"evacuate": flood_probability, "stay": 1.0 - flood_probability}


def selector_distribution(selector_state: Mapping[str, object]) -> dict[str, float]:
    revisions = int(selector_state.get("revision_count", 0))
    advance_weight = max(0.05, 0.9 - 0.4 * revisions)
    return {"advance": advance_weight, "wait": 1.0 - advance_weight}


def option_cone(
    physical_histories: set[str],
    modeled_histories: set[str],
    reachable_with_means: set[str],
) -> set[str]:
    return physical_histories & modeled_histories & reachable_with_means


def authorized_options(
    physically_reachable_options: set[str], authorized_histories: set[str]
) -> set[str]:
    return physically_reachable_options & authorized_histories


class SoulLoopAndConeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.envelope = AuthorizationEnvelope(
            principal="principal",
            mandate="advance one state",
            scope="test-boundary",
            consent=True,
            custody="operator",
            expiry_or_revocation="revocable before execution",
            contest_path="appeal",
            actor="agent",
            consequence_bearers=("system",),
        )
        self.authorization = AuthorizationAssessment("valid", self.envelope)

    def test_commitment_and_outcome_are_separate_receipt_types(self) -> None:
        action, commitment = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, self.authorization
        )
        self.assertEqual(action, "advance")
        self.assertEqual(commitment.receipt_type, "commitment")
        self.assertEqual(commitment.attempted_action_id, "advance")
        self.assertEqual(commitment.authorization_status, "valid")
        next_state, outcome = environment_transition(3, action)
        self.assertEqual(next_state, 4)
        self.assertEqual(outcome.receipt_type, "outcome")
        self.assertEqual(outcome.performed_action_id, "advance")
        self.assertIsNot(type(commitment), type(outcome))

    def test_selected_option_without_means_yields_null_action(self) -> None:
        action, receipt = select_action(
            {"advance": 1.0}, {"advance": 0.0}, {"advance"}, self.authorization
        )
        self.assertIsNone(action)
        self.assertEqual(receipt.status, "unavailable")
        self.assertEqual(receipt.receipt_type, "commitment")

    def test_governed_channel_fails_closed_on_invalid_authorization(self) -> None:
        incomplete_envelope = replace(self.envelope, consent=False)
        invalid = AuthorizationAssessment(
            "invalid", incomplete_envelope, ("consent missing",)
        )
        action, receipt = select_action(
            {"advance": 1.0},
            {"advance": 1.0},
            {"advance"},
            invalid,
            governed=True,
        )
        self.assertIsNone(action)
        self.assertEqual(receipt.status, "refused")
        self.assertEqual(receipt.physical_availability, "available")
        self.assertEqual(receipt.authorization_status, "invalid")

    def test_unauthorized_attempt_remains_causally_representable(self) -> None:
        invalid = AuthorizationAssessment(
            "invalid", replace(self.envelope, consent=False), ("coerced",)
        )
        action, receipt = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, invalid
        )
        self.assertEqual(action, "advance")
        self.assertEqual(receipt.status, "unauthorized_attempt")
        next_state, outcome = environment_transition(2, action or "")
        self.assertEqual(next_state, 3)
        self.assertEqual(outcome.performed_action_id, "advance")

    def test_absent_envelope_can_be_receipted(self) -> None:
        absent = AuthorizationAssessment("absent", None, ("no envelope",))
        action, receipt = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, absent
        )
        self.assertEqual(action, "advance")
        self.assertEqual(receipt.authorization_status, "absent")
        self.assertEqual(receipt.actor, "unknown")

    def test_nonconsequential_not_required_state_is_narrowly_inhabited(self) -> None:
        assessment = AuthorizationAssessment(
            "not_required", None, (), nonconsequential_scope=True
        )
        action, receipt = select_action(
            {"observe": 1.0}, {"observe": 1.0}, {"observe"}, assessment
        )
        self.assertEqual(action, "observe")
        self.assertEqual(receipt.status, "nonconsequential_attempt")
        self.assertEqual(receipt.authorization_status, "not_required")

    def test_malformed_authorization_union_combinations_are_rejected(self) -> None:
        malformed = (
            AuthorizationAssessment("valid", None),
            AuthorizationAssessment(
                "valid", replace(self.envelope, consent=False)
            ),
            AuthorizationAssessment("invalid", None, ("defect",)),
            AuthorizationAssessment("invalid", self.envelope, ()),
            AuthorizationAssessment("absent", self.envelope, ("unexpected",)),
            AuthorizationAssessment("absent", None, ()),
            AuthorizationAssessment("not_required", None),
            AuthorizationAssessment(
                "not_required", None, ("reason forbidden",), True
            ),
        )
        for assessment in malformed:
            with self.subTest(assessment=assessment):
                with self.assertRaises(ValueError):
                    select_action(
                        {"advance": 1.0},
                        {"advance": 1.0},
                        {"advance"},
                        assessment,
                    )

    def test_receipt_status_is_derived_from_validated_authorization(self) -> None:
        invalid = AuthorizationAssessment(
            "invalid", replace(self.envelope, consent=False), ("no consent",)
        )
        _, invalid_receipt = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, invalid
        )
        self.assertEqual(invalid_receipt.status, "unauthorized_attempt")
        self.assertEqual(invalid_receipt.authorization_status, "invalid")
        _, valid_receipt = select_action(
            {"advance": 1.0},
            {"advance": 1.0},
            {"advance"},
            self.authorization,
        )
        self.assertEqual(valid_receipt.status, "authorized_committed")
        self.assertEqual(valid_receipt.authorization_status, "valid")

    def test_imposed_cost_is_not_voluntary_sacrifice(self) -> None:
        invalid = AuthorizationAssessment(
            "invalid", replace(self.envelope, consent=False), ("imposed",)
        )
        action, receipt = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, invalid
        )
        self.assertEqual(action, "advance")
        self.assertEqual(receipt.status, "unauthorized_attempt")
        self.assertFalse(
            voluntary_sacrifice(
                -2.0,
                5.0,
                receipt.authorization_status == "valid",
            )
        )

    def test_environment_can_veto_a_committed_action(self) -> None:
        action, commitment = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, self.authorization
        )
        next_state, outcome = environment_transition(7, action or "", veto=True)
        self.assertEqual(commitment.status, "authorized_committed")
        self.assertEqual(next_state, 7)
        self.assertEqual(outcome.observed_outcome, "vetoed")
        self.assertNotEqual(commitment.expected_outcome, outcome.observed_outcome)

    def test_null_receipt_produces_null_update(self) -> None:
        model: dict[str, object] = {"receipt_count": 0}
        selector: dict[str, object] = {"revision_count": 0}
        _, commitment = select_action(
            {"advance": 1.0}, {"advance": 0.0}, {"advance"}, self.authorization
        )
        next_model, next_selector = loop_update(model, selector, commitment, None)
        self.assertIs(next_model, model)
        self.assertIs(next_selector, selector)

    def test_ambient_observation_is_not_attributed_to_null_action(self) -> None:
        action, commitment = select_action(
            {"advance": 1.0}, {"advance": 0.0}, {"advance"}, self.authorization
        )
        self.assertIsNone(action)
        ambient = ambient_observation(4, 5)
        self.assertEqual(ambient.receipt_cause, "ambient_observation")
        self.assertIsNone(ambient.attempted_action_id)
        self.assertIsNone(ambient.performed_action_id)
        model, _ = loop_update(
            {"receipt_count": 0}, {"revision_count": 0}, commitment, ambient
        )
        self.assertEqual(model["last_observed"], "ambient-change")

    def test_adverse_outcome_updates_map_and_selector(self) -> None:
        action, commitment = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, self.authorization
        )
        _, outcome = environment_transition(1, action or "", veto=True)
        model, selector = loop_update(
            {"receipt_count": 0}, {"revision_count": 0}, commitment, outcome
        )
        self.assertEqual(model["receipt_count"], 1)
        self.assertEqual(model["last_observed"], "vetoed")
        self.assertEqual(selector["revision_count"], 1)

    def test_updated_selector_changes_the_next_action_distribution(self) -> None:
        action, commitment = select_action(
            {"advance": 1.0}, {"advance": 1.0}, {"advance"}, self.authorization
        )
        _, outcome = environment_transition(1, action or "", veto=True)
        before = {"revision_count": 0}
        before_distribution = selector_distribution(before)
        _, after = loop_update(
            {"receipt_count": 0}, before, commitment, outcome
        )
        after_distribution = selector_distribution(after)
        self.assertNotEqual(before_distribution, after_distribution)
        self.assertGreater(
            before_distribution["advance"], after_distribution["advance"]
        )

    def test_model_future_intervention_changes_present_action_distribution(self) -> None:
        high_risk = represented_future_distribution(0.9)
        low_risk = represented_future_distribution(0.1)
        self.assertNotEqual(high_risk, low_risk)
        self.assertEqual(max(high_risk, key=high_risk.get), "evacuate")
        self.assertEqual(max(low_risk, key=low_risk.get), "stay")
        self.assertAlmostEqual(sum(high_risk.values()), 1.0)
        self.assertAlmostEqual(sum(low_risk.values()), 1.0)

    def test_same_physical_cone_can_contain_different_option_cones(self) -> None:
        physical = {"stay", "walk", "train", "moon"}
        agent_a = option_cone(
            physical,
            {"stay", "walk", "train"},
            {"stay", "walk"},
        )
        agent_b = option_cone(
            physical,
            {"stay", "walk", "train"},
            {"stay", "walk", "train"},
        )
        self.assertEqual(agent_a, {"stay", "walk"})
        self.assertEqual(agent_b, {"stay", "walk", "train"})
        self.assertLess(agent_a, agent_b)
        self.assertTrue(agent_a <= physical)
        self.assertTrue(agent_b <= physical)

    def test_authorization_is_a_normative_subset_not_the_option_cone(self) -> None:
        physical_option_cone = {"stay", "walk", "take_without_permission"}
        authorized = authorized_options(physical_option_cone, {"stay", "walk"})
        self.assertIn("take_without_permission", physical_option_cone)
        self.assertNotIn("take_without_permission", authorized)
        self.assertLess(authorized, physical_option_cone)


# ---------------------------------------------------------------------------
# Collective trace, Power-Max, and value-theory reference models


@dataclass(frozen=True)
class EgregoreotypeCandidate:
    persistent_shared_trace: bool
    carrier_turnover: bool
    selection_reweighting_intervention: bool
    recurrent_objective_like_bias: bool
    visible_substrate_costs: tuple[float, ...]
    payer: str
    beneficiary: str
    eta_observed: Optional[float] = None
    authorization_status: str = "absent"
    consciousness_presumed: bool = False
    personhood_presumed: bool = False
    substrate_reduced: bool = False

    def qualifies(self) -> bool:
        return all(
            (
                self.persistent_shared_trace,
                self.carrier_turnover,
                self.selection_reweighting_intervention,
                self.recurrent_objective_like_bias,
                bool(self.visible_substrate_costs),
                bool(self.payer),
                bool(self.beneficiary),
                not self.consciousness_presumed,
                not self.personhood_presumed,
            )
        )


@dataclass(frozen=True)
class ActionEvaluation:
    name: str
    expected_individual: float
    expected_whole: float
    justice: bool
    affected_bearer_deltas: tuple[float, ...] = ()


def unconstrained_power_max(actions: Sequence[ActionEvaluation]) -> ActionEvaluation:
    return max(actions, key=lambda action: action.expected_individual)


def justice_constrained_power_max(
    actions: Sequence[ActionEvaluation],
) -> Optional[ActionEvaluation]:
    admissible = [
        action
        for action in actions
        if action.justice
        and action.expected_individual >= 0.0
        and action.expected_whole >= 0.0
        and all(delta >= 0.0 for delta in action.affected_bearer_deltas)
    ]
    if not admissible:
        return None
    return max(admissible, key=lambda action: action.expected_individual)


def epsilon_optimal_open_unit(epsilon: float) -> float:
    if not 0.0 < epsilon < 1.0:
        raise ValueError("epsilon must lie in (0, 1)")
    return 1.0 - epsilon / 2.0


def extractor_gain(phi_i: float, coupling: float, delta_viability: float) -> float:
    if not (phi_i > 0.0 and 0.0 <= coupling <= 1.0 and delta_viability > 0.0):
        raise ValueError("counterexample parameters are outside their domain")
    return phi_i * (1.0 - coupling) * delta_viability


def dyadic_labels(
    delta_individual: float,
    delta_whole: float,
    justice: bool,
    affected_bearer_deltas: Sequence[float] = (),
) -> set[str]:
    labels: set[str] = set()
    if not justice or any(delta < 0.0 for delta in affected_bearer_deltas):
        return labels
    if delta_whole > 0.0 and delta_individual >= 0.0:
        labels.add("moral")
    if delta_individual > 0.0 and delta_whole >= 0.0:
        labels.add("ethical")
    if delta_individual > 0.0 and delta_whole > 0.0:
        labels.add("syntropic")
    if delta_individual == 0.0 and delta_whole == 0.0:
        labels.add("lawful-preservation")
    return labels


def voluntary_sacrifice(
    payer_delta: float, beneficiary_delta: float, authorized_cost: bool
) -> bool:
    return payer_delta < 0.0 and beneficiary_delta > 0.0 and authorized_cost


class CollectivePowerAndValueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidate = EgregoreotypeCandidate(
            persistent_shared_trace=True,
            carrier_turnover=True,
            selection_reweighting_intervention=True,
            recurrent_objective_like_bias=True,
            visible_substrate_costs=(1.0,),
            payer="carriers",
            beneficiary="institution",
        )

    def test_egregoreotype_requires_all_five_evidentiary_conditions(self) -> None:
        self.assertTrue(self.candidate.qualifies())
        failures = (
            {"persistent_shared_trace": False},
            {"carrier_turnover": False},
            {"selection_reweighting_intervention": False},
            {"recurrent_objective_like_bias": False},
            {"visible_substrate_costs": ()},
        )
        for mutation in failures:
            with self.subTest(mutation=mutation):
                self.assertFalse(replace(self.candidate, **mutation).qualifies())

    def test_candidate_does_not_presume_consciousness_or_personhood(self) -> None:
        self.assertFalse(self.candidate.consciousness_presumed)
        self.assertFalse(self.candidate.personhood_presumed)
        self.assertFalse(
            replace(self.candidate, consciousness_presumed=True).qualifies()
        )
        self.assertFalse(replace(self.candidate, personhood_presumed=True).qualifies())

    def test_successful_substrate_reduction_does_not_erase_macro_candidate(self) -> None:
        reduced = replace(self.candidate, substrate_reduced=True)
        self.assertTrue(reduced.qualifies())

    def test_candidacy_is_descriptive_not_eta_zero(self) -> None:
        nonextractive = replace(
            self.candidate, eta_observed=0.0, authorization_status="valid"
        )
        extractive = replace(
            self.candidate, eta_observed=0.4, authorization_status="invalid"
        )
        self.assertTrue(nonextractive.qualifies())
        self.assertTrue(extractive.qualifies())
        self.assertTrue(
            nonextractive.eta_observed == 0.0
            and nonextractive.authorization_status == "valid"
        )
        self.assertFalse(
            extractive.eta_observed == 0.0
            and extractive.authorization_status == "valid"
        )

    def test_one_shot_extraction_can_benefit_the_extractor(self) -> None:
        self.assertGreater(extractor_gain(0.8, 0.25, 0.1), 0.0)
        self.assertEqual(extractor_gain(0.8, 1.0, 0.1), 0.0)

    def test_justice_filters_the_unconstrained_power_max_counterexample(self) -> None:
        extraction = ActionEvaluation("extract", 10.0, -8.0, False)
        mutual = ActionEvaluation("mutual", 4.0, 4.0, True)
        preserve = ActionEvaluation("preserve", 1.0, 0.0, True)
        actions = (extraction, mutual, preserve)
        self.assertEqual(unconstrained_power_max(actions).name, "extract")
        self.assertEqual(justice_constrained_power_max(actions).name, "mutual")

    def test_empty_justice_field_has_no_admissible_maximizer(self) -> None:
        actions = (
            ActionEvaluation("extract", 10.0, -8.0, False),
            ActionEvaluation("harm", 3.0, -1.0, True),
        )
        self.assertIsNone(justice_constrained_power_max(actions))

    def test_noncompact_field_uses_epsilon_optimum_not_false_argmax(self) -> None:
        for candidate in (0.1, 0.5, 0.9, 0.999):
            improved = (candidate + 1.0) / 2.0
            self.assertGreater(improved, candidate)
            self.assertLess(improved, 1.0)
        epsilon = 0.02
        approximate = epsilon_optimal_open_unit(epsilon)
        self.assertGreaterEqual(approximate, 1.0 - epsilon)
        self.assertLess(approximate, 1.0)
        owner = owner_text(
            "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md"
        )
        self.assertIn("upper\nsemicontinuous", owner)
        self.assertIn("a_\\varepsilon", owner)

    def test_moral_ethical_and_strict_syntropic_directions(self) -> None:
        self.assertEqual(dyadic_labels(0.0, 2.0, True), {"moral"})
        self.assertEqual(dyadic_labels(2.0, 0.0, True), {"ethical"})
        self.assertEqual(
            dyadic_labels(2.0, 3.0, True), {"moral", "ethical", "syntropic"}
        )
        self.assertEqual(
            dyadic_labels(0.0, 0.0, True), {"lawful-preservation"}
        )

    def test_aggregate_gain_cannot_launder_hidden_bearer_harm(self) -> None:
        delta_individual, delta_whole = 100.0, -1.0
        self.assertGreater(delta_individual + delta_whole, 0.0)
        self.assertEqual(dyadic_labels(delta_individual, delta_whole, True), set())

    def test_focal_dyad_cannot_launder_a_harmed_third_bearer(self) -> None:
        superficially_mutual = ActionEvaluation(
            "dyad-wins-third-loses", 5.0, 4.0, True, (-3.0,)
        )
        safe = ActionEvaluation("bearer-complete", 2.0, 2.0, True, (0.0,))
        self.assertEqual(
            justice_constrained_power_max((superficially_mutual, safe)).name,
            "bearer-complete",
        )
        self.assertEqual(dyadic_labels(5.0, 4.0, True, (-3.0,)), set())

    def test_voluntary_sacrifice_is_costly_and_not_strict_syntropy(self) -> None:
        self.assertTrue(voluntary_sacrifice(-2.0, 5.0, True))
        self.assertFalse(voluntary_sacrifice(-2.0, 5.0, False))
        self.assertNotIn("syntropic", dyadic_labels(-2.0, 5.0, True))
        primitives = owner_text(
            "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md"
        )
        self.assertNotIn("AuthorizedCost(a;p,b) :=\n  J(", primitives)
        self.assertIn("does **not**\nimply the ordinary `J` predicate", primitives)


# ---------------------------------------------------------------------------
# Quantum-removal and source-bound fallacy mutation matrix


OPERATIONAL_KEYS = (
    "dRegisters",
    "soulLoop",
    "authorization",
    "justice",
    "egregoreotype",
    "closure",
)


def operational_projection(document: Mapping[str, object]) -> bytes:
    core = {key: document[key] for key in OPERATIONAL_KEYS}
    return json.dumps(
        core, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


@dataclass(frozen=True)
class MutationSpec:
    mutation_id: str
    owner: str
    repair_marker: str
    good_claim: str
    bad_claim: str
    forbidden_pattern: str


MUTATIONS: tuple[MutationSpec, ...] = (
    MutationSpec(
        "empirical-chart-inflation",
        "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
        "These are **chart facts only**.",
        "The reciprocal identity is analytic inside the declared open chart.",
        "phi * nu = 1 proves a universal empirical conservation law.",
        r"phi\s*\*\s*nu\s*=\s*1.{0,40}\bproves\b.{0,50}\bempirical\b",
    ),
    MutationSpec(
        "product-uniqueness",
        "05_COSMOLOGY/00_CANONICAL_FORMULA_BLOCK.md",
        "**AND-class**",
        "The product is one selected normalized conjunctive instance.",
        "P_node = Phi * V is uniquely derived as the only possible aggregator.",
        r"P_node.{0,40}(?<!not )uniquely derived.{0,50}only possible aggregator",
    ),
    MutationSpec(
        "forced-sevenfold-necessity",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/00_THE_SEVEN_AXIOMS.md",
        "not a necessary decomposition of nature",
        "D0-D6 is a selected structural and interpretive scaffold.",
        "Nature necessarily decomposes into exactly D0-D6 because S2 forces seven layers.",
        r"Nature necessarily decomposes.{0,60}D0-D6.{0,60}forces seven layers",
    ),
    MutationSpec(
        "missing-law-irreducibility",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
        "`currently_unreduced` means no accepted reduction is presently supplied.",
        "A missing reduction is currently_unreduced, not a proof of irreducibility.",
        "No reduction is known, therefore the crossing is strongly emergent and irreducible.",
        r"No reduction is known.{0,30}therefore.{0,50}irreducible",
    ),
    MutationSpec(
        "d4-d5-inversion",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "| **D4** | **actual** |",
        "D4 is actual and D5 is possible.",
        "D4 is possibility and D5 is actuality.",
        r"D4 is possibility and D5 is actuality",
    ),
    MutationSpec(
        "scalar-sampling",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md",
        "is not a distribution to sample from",
        "Sample an outcome from the Born probability measure.",
        "a_t = Sample[integral |psi|^2 ds].",
        r"Sample\s*\[\s*integral\s*\|psi\|\^2\s*ds\s*\]",
    ),
    MutationSpec(
        "quantum-dimension-stacking",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/38_QUANTUM_FOUNDATIONS_CONFIRMATION_BOUNDARY.md",
        "Neither interpretation is an added spacetime dimension.",
        "The quantum comparison is optional and interpretation-specific.",
        "Everett is a five-dimensional probability layer stacked above Copenhagen four-dimensional collapse.",
        r"Everett is a five-dimensional.{0,60}stacked above Copenhagen four-dimensional",
    ),
    MutationSpec(
        "forced-titans",
        "05_COSMOLOGY/01_THE_TRANSCENDENTAL_TRINITY/00_THE_TRANSCENDENTAL_TRINITY_CANON.md",
        "why the triad is selected, not forced",
        "The Titan tokens are selected symbolic roles; ordinary numbers stay operands.",
        "Inversion closure forces {0,1,infinity} as the unique generators of reality.",
        r"Inversion closure forces.{0,30}0,1,infinity.{0,60}unique generators of reality",
    ),
    MutationSpec(
        "legacy-spelling",
        "05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md",
        "**Egregoreotype** is canonical",
        "Egregoreotype is the canonical active spelling.",
        "The canonical active term is Egregorotype.",
        r"canonical active term is Egregorotype",
    ),
    MutationSpec(
        "worldview-k2",
        "00_META/00_SETTLED_CANON_REGISTRY.md",
        "it is not a primitive of reality, the Soul Loop, ethics, or the Compass.",
        "Consequential action requires complete accountable authorization.",
        "K2 is a universal primitive required for agency and ethics.",
        r"K2 is a universal primitive required for agency and ethics",
    ),
    MutationSpec(
        "physical-cone-expansion",
        "00_THE_COMPASS.md",
        "More foresight does not widen the physical light cone or exceed `c`.",
        "Models can widen option cones only inside physical admissibility.",
        "Human intelligence widens the physical light cone beyond c.",
        r"Human intelligence widens the physical light cone beyond c",
    ),
    MutationSpec(
        "physical-retrocausal-inflation",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/34_D4_D5_CANONICAL_REFERENCE.md",
        "does not assert a temporal relation from a future event to the past.",
        "Present model tokens about futures can reweight present selection.",
        "A future physical event sends information backward in time to cause present choice.",
        r"future physical event sends information backward in time.{0,30}present choice",
    ),
    MutationSpec(
        "aggregate-ethical-laundering",
        "04_AXIOLOGY/02_VALUE_THEORY/00_OBJECTIVE_MORALS_AND_ETHICS.md",
        "extraction, even if aggregate rises",
        "Each bearer remains separately visible under Justice.",
        "The action is ethical because total gain is positive even though the individual is destroyed.",
        r"ethical because total gain is positive.{0,50}individual is destroyed",
    ),
    MutationSpec(
        "unconditional-power-max",
        "05_COSMOLOGY/03_FORMAL_SYSTEM/08_EFR_POWER_MAX_LEMMA.md",
        "Justice defines the admissible field; Power-Max chooses within it.",
        "Power-Max selects only inside the Justice-admissible field.",
        "Power-Max is moral whenever it maximizes W_i, without any Justice constraint.",
        r"Power-Max is moral whenever it maximizes W_i.{0,50}without any Justice constraint",
    ),
)


class ClaimBoundaryValidator:
    def __init__(self, specs: Sequence[MutationSpec]) -> None:
        self._patterns = {
            spec.mutation_id: re.compile(
                spec.forbidden_pattern, re.IGNORECASE | re.DOTALL
            )
            for spec in specs
        }

    def violations(self, text: str) -> set[str]:
        return {
            mutation_id
            for mutation_id, pattern in self._patterns.items()
            if pattern.search(text)
        }


class QuantumRemovalAndMutationTests(unittest.TestCase):
    def test_quantum_inset_removal_leaves_operational_calculus_unchanged(self) -> None:
        document: dict[str, object] = {
            "dRegisters": {"D4": "actual", "D5": "possible"},
            "soulLoop": ["model", "commit", "world", "receipt", "revise"],
            "authorization": [
                "principal",
                "mandate",
                "scope",
                "consent",
                "custody",
                "expiryOrRevocation",
                "contestPath",
                "actor",
                "consequenceBearer",
            ],
            "justice": {"individual": "visible", "whole": "visible"},
            "egregoreotype": {"criteria": 5},
            "closure": "r6:D6->D0; non-mu",
            "quantumCorrespondence": {
                "tier": "C",
                "Everett": "relative-state/no fundamental collapse",
                "actualization": "interpretation-specific",
            },
        }
        with_quantum = operational_projection(document)
        without_quantum_document = dict(document)
        del without_quantum_document["quantumCorrespondence"]
        without_quantum = operational_projection(without_quantum_document)
        alternate_quantum_document = dict(document)
        alternate_quantum_document["quantumCorrespondence"] = {
            "tier": "C",
            "status": "removed",
        }
        self.assertEqual(with_quantum, without_quantum)
        self.assertEqual(
            with_quantum, operational_projection(alternate_quantum_document)
        )

    def test_all_fourteen_named_mutations_are_bound_to_repaired_owners(self) -> None:
        self.assertEqual(len(MUTATIONS), 14)
        self.assertEqual(len({spec.mutation_id for spec in MUTATIONS}), 14)
        validator = ClaimBoundaryValidator(MUTATIONS)
        for spec in MUTATIONS:
            with self.subTest(mutation=spec.mutation_id):
                source = owner_text(spec.owner)
                self.assertIn(spec.repair_marker, source)
                self.assertNotIn(spec.mutation_id, validator.violations(source))
                self.assertNotIn(spec.mutation_id, validator.violations(spec.good_claim))
                mutated_source = source + "\n\n" + spec.bad_claim + "\n"
                self.assertIn(spec.mutation_id, validator.violations(mutated_source))

    def test_legacy_spelling_is_only_an_explicit_owner_alias(self) -> None:
        source = owner_text("05_COSMOLOGY/00_STIGMERGY_AND_THE_EGREGOROTYPE.md")
        legacy_occurrences = re.findall(r"\bEgregorotype\b", source)
        self.assertEqual(legacy_occurrences, ["Egregorotype"])
        self.assertIn("**Compatibility note:**", source)
        self.assertIn("**Egregoreotype** is canonical", source)

    def test_invalid_scalar_sampling_expression_is_absent_from_mu_owner(self) -> None:
        source = owner_text("05_COSMOLOGY/03_FORMAL_SYSTEM/10_EFR_MU_LIMIT_FORMULA.md")
        self.assertNotIn("Sample[∫", source)
        self.assertIn("o ~ 𝔓_ψ", source)

    def test_mu_records_do_not_treat_hypothesis_prose_as_evidence(self) -> None:
        primitives = owner_text(
            "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md"
        )
        self.assertIn("evidenceStatus: supplied | not_yet_supplied", primitives)
        topology = json.loads(
            owner_text("05_COSMOLOGY/00_BURRI_RULES_TOPOLOGY.json")
        )
        crossings = [
            node for node in topology["nodes"] if node["kind"] == "crossing"
        ]
        self.assertEqual({node["id"] for node in crossings}, {f"mu-{i}" for i in range(6)})
        for crossing in crossings:
            with self.subTest(crossing=crossing["id"]):
                self.assertEqual(crossing["saturationEvidence"], [])
                self.assertEqual(
                    crossing["evidenceStatus"], "not_yet_supplied"
                )

    def test_fixed_modality_and_closure_contract_is_present_in_type_owner(self) -> None:
        source = owner_text(
            "05_COSMOLOGY/03_FORMAL_SYSTEM/29_PRIMITIVES_AND_TYPE_SIGNATURES.md"
        )
        self.assertIn("| `D4` | **actual** |", source)
        self.assertIn("| `D5` | **merely possible** |", source)
        self.assertIn("ModeledFutureToken := {", source)
        self.assertIn("carrierRegister: D4", source)
        self.assertIn("carrierModality: actual", source)
        self.assertIn("AlternativeContent   :=", source)
        self.assertNotRegex(source, r"ModeledFutureToken[^}]+modality:merely_possible")
        self.assertIn("There are exactly six adjacent crossing identifiers `μ₀…μ₅`.", source)
        self.assertIn("There is no\n`μ₆`.", source)
        self.assertIn("`r₆:D6↝D0` is an interpretive, non-μ closure edge.", source)


class RosettaAndReflexivityTests(unittest.TestCase):
    def test_rosetta_round_trip_preserves_type_modality_and_tier(self) -> None:
        source = (
            ("actual-model-token", "state", "D4", "actual", "I"),
            ("possible-content", "state", "D5", "possible", "I"),
            ("outcome-receipt", "receipt", "D4", "actual", "S"),
        )

        def project(
            records: tuple[tuple[str, str, str, str, str], ...], domain: str
        ) -> tuple[tuple[str, str, str, str, str], ...]:
            return tuple(
                (f"{domain}:{name}", kind, register, modality, tier)
                for name, kind, register, modality, tier in records
            )

        def unproject(
            records: tuple[tuple[str, str, str, str, str], ...]
        ) -> tuple[tuple[str, str, str, str, str], ...]:
            return tuple(
                (name.split(":", 1)[1], kind, register, modality, tier)
                for name, kind, register, modality, tier in records
            )

        translated = project(source, "institution")
        self.assertEqual(unproject(translated), source)
        self.assertEqual(
            [(row[1], row[2], row[3], row[4]) for row in translated],
            [(row[1], row[2], row[3], row[4]) for row in source],
        )

    def test_reflexive_bridge_keeps_all_three_gaps_inspectable(self) -> None:
        rulebook = owner_text("05_COSMOLOGY/00_THE_BURRI_RULES.md")
        for marker in (
            "observed territory versus model prediction",
            "intended versus performed commitment",
            "expected versus observed consequence",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, rulebook)

    def test_soros_crosswalk_forbids_three_physics_slippages(self) -> None:
        ledger = owner_text(
            "03_METHODOLOGY/01_THE_DERIVATION/01_BURRI_RULES_DERIVATION_LEDGER.md"
        )
        for forbidden_slippage in (
            "not quantum observation",
            "not physical retrocausality",
            "no physics prestige transfer",
        ):
            with self.subTest(slippage=forbidden_slippage):
                self.assertIn(forbidden_slippage, ledger)
        self.assertIn("negative is not evil; positive is not good", ledger)
        self.assertIn(
            "Soros does not evidence collapse, Everett/Copenhagen, `μ` physics",
            ledger,
        )


class ActiveCorpusPropagationTests(unittest.TestCase):
    """Keep repaired owner truth from drifting back through active mirrors."""

    _FROZEN_PARTS = {
        "12_PUBLIC_SITE",
        "90_ARCHIVE",
        "91_COMPATIBILITY",
    }

    def _active_route_cards(self) -> list[Path]:
        cards: list[Path] = []
        for name in ("AGENTS.md", "CLAUDE.md"):
            for path in ROOT.rglob(name):
                relative = path.relative_to(ROOT)
                if any(part in self._FROZEN_PARTS for part in relative.parts):
                    continue
                if relative.parts[:2] == ("11_UPLINK", "60_SESSION_PACKETS"):
                    continue
                cards.append(path)
        return cards

    def test_active_route_cards_reject_the_old_universal_k2_rule(self) -> None:
        forbidden = "every irreversible act requires natural-person signature"
        violations = [
            str(path.relative_to(ROOT))
            for path in self._active_route_cards()
            if forbidden in path.read_text(encoding="utf-8").lower()
        ]
        self.assertEqual(violations, [])

    def test_route_card_generator_cannot_restore_worldview_k2(self) -> None:
        generator = owner_text("09_TOOLS/07_AGENT_OPS/generate_agents_md.py")
        self.assertNotIn(
            "every irreversible act requires natural-person signature",
            generator.lower(),
        )
        self.assertIn("K2 is private-DAV-only", generator)
        self.assertIn("complete, scoped, contestable authorization", generator)

    def test_formula_and_option_cone_front_doors_preserve_the_type_split(self) -> None:
        root_route = owner_text("AGENTS.md")
        concepts = owner_text(
            "08_FRAMEWORK_SUPPORT/01_GOVERNANCE/00_CORE_CONCEPTS.md"
        )
        option_cone = owner_text(
            "05_COSMOLOGY/00_INTELLIGENCE_AND_THE_POTENTIAL_CONE.md"
        )
        ontology = owner_text("06_ONTOLOGY/README.md")
        self.assertIn("open reciprocal chart `θ∈(0,π)`", root_route)
        self.assertIn("licenses no ontology or ethic", root_route)
        self.assertIn("It is not derived from S².", concepts)
        self.assertNotIn("Authorized_x(h)", option_cone)
        self.assertIn("AuthorizedOptionCone_x(t)", option_cone)
        self.assertNotIn("D5 opens enacted agency", ontology)
        self.assertIn("D4 is causal actuality", ontology)
        self.assertIn("D5 is merely possible counterfactual content", ontology)

    def test_rosetta_front_door_does_not_reinstall_causal_or_identity_claims(self) -> None:
        rosetta = owner_text(
            "08_FRAMEWORK_SUPPORT/03_EVIDENCE/ROSETTA_STONE/00_THE_MASTER_ROSETTA.md"
        )
        self.assertNotIn("L0 and L∞ are the same", rosetta)
        self.assertNotRegex(
            rosetta,
            r"(?i)caste(?:s)?\s*(?:cause|determine|produce)\s*reasoning",
        )
        self.assertIn("translation lens", rosetta)

    def test_preserved_legacy_bodies_have_visible_non_authority_seams(self) -> None:
        legacy_paths = (
            "05_COSMOLOGY/00_THE_BURRI_RULES_MAP.svg",
            "05_COSMOLOGY/00_THE_COMPLETE_ONTOLOGY_OF_REALITY.md",
            "05_COSMOLOGY/00_THE_GEOMETRIC_ONTOLOGY_OF_REALITY.md",
            "05_COSMOLOGY/03_FORMAL_SYSTEM/25_STEEL_THREAD.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_283_The_Orthogonality_Theorem_v2.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_285_Dreams_Are_Unanchored_D5.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_287_Wigners_Puzzle_Dissolved.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_290_The_Ektropic_Radius_v2.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_291_The_Landauer_Horn.md",
            "08_FRAMEWORK_SUPPORT/02_OPERATORS/MF_ADVANCED/MF_294_Egregores_Are_Horn_Networks.md",
            "03_METHODOLOGY/02_THE_PAPERS/PAPER_W_DESCENT_ASYMMETRY.md",
            "03_METHODOLOGY/02_THE_PAPERS/PEER_REVIEW_PROGRAM/AXIOM_PAPERS/AX2_THE_ETHIC.md",
        )
        for path in legacy_paths:
            with self.subTest(path=path):
                source = re.sub(r"\s+", " ", owner_text(path).lower())
                self.assertRegex(source, r"not live(?: >)?(?: value)? authority")

    def test_worldview_statuses_no_longer_wait_for_k2(self) -> None:
        paths = (
            "00_META/00_THE_KINTSUGI_PROTOCOL.md",
            "01_TELEOLOGY/02_THE_DERIVATION/07A_F5_UNBUNDLED_COUPLING_PER_DIMENSION_PENDING_K2.md",
            "01_TELEOLOGY/02_THE_DERIVATION/07B_THE_FORCE_LADDER_FORMALIZED_PENDING_K2.md",
            "05_COSMOLOGY/00_THE_BALANCE_OPTIMUM_IS_CONDITIONAL.md",
        )
        for path in paths:
            with self.subTest(path=path):
                frontmatter = owner_text(path).split("---", 2)[1].lower()
                self.assertNotIn("pending k2", frontmatter)
                self.assertNotIn("staged for k2", frontmatter)


if __name__ == "__main__":
    unittest.main()
