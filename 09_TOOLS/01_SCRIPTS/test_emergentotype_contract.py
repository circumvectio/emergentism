#!/usr/bin/env python3
"""Contract tests for EgregoreotypeCandidateContract.v1."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "05_COSMOLOGY"
    / "00_EGREGOREOTYPE_CANDIDATE_CONTRACT.v1.schema.json"
)


def test_record(status: str = "PASS") -> dict[str, object]:
    return {
        "status": status,
        "measure": "predeclared measure",
        "evidenceRefs": ["evidence://fixture"],
    }


def passing_instance() -> dict[str, object]:
    marker_names = (
        "persistentTrace",
        "carrierTurnover",
        "selectionReweighting",
        "recurrentObjectiveLikeBias",
        "visibleSubstrateCost",
    )
    strategic_names = (
        "prospectivePrediction",
        "counterfactualPrediction",
        "interventionSensitiveUptake",
        "crossContextRecurrence",
        "incrementalValueBeyondRivals",
    )
    return {
        "schema": "emergentism/EgregoreotypeCandidateContract.v1",
        "recordId": "fixture-strategic-1",
        "profile": {
            "replicatorLayer": "EGREGOREOTYPE",
            "patternIdentity": "turnover-stable shared actor trace",
            "carrierClass": "people and records",
            "carrierInstanceIds": ["carrier-1", "carrier-2"],
            "admittedCarrierVariation": "individual carrier turnover",
            "persistenceCriterion": "trace and effect survive turnover",
            "intervention": "randomize actor framing",
            "rivalModels": ["direct command", "current incentives"],
            "evidenceRefs": ["evidence://profile"],
            "tier": "[B] bounded fixture",
            "killCriterion": "no persistence or intervention effect",
        },
        "baseCandidate": {
            "id": "candidate-1",
            "systemBoundary": "declared test population and trace",
            "individualCarrierIds": ["carrier-1", "carrier-2"],
            "whole": "candidate trace-mediated pattern",
            "sharedTraceRef": "trace://actor-model",
            "tracePersistenceWindow": "three preregistered episodes",
            "turnoverEvidence": "evidence://turnover",
            "selectionReweightingEstimate": "effect estimate with interval",
            "recurrentBiasMeasure": "directional recurrence score",
            "substrateCost": "time and attention ledger",
            "affectedBearerIds": ["carrier-1", "carrier-2"],
            "payerIds": ["carrier-1"],
            "beneficiaryIds": ["carrier-2"],
            "etaObserved": "declared separately",
            "custody": "evidence custodian",
            "consent": "recorded",
            "reversibility": "reversible trace perturbation",
            "exit": "participant withdrawal",
            "rivalModels": ["direct command", "current incentives"],
            "evidenceRefs": ["evidence://base"],
            "tier": "[B] bounded fixture",
            "killCriterion": "any parent marker fails",
            "markers": {name: test_record() for name in marker_names},
            "verdict": "PASS",
        },
        "agentRepresentation": {
            "targetCandidateId": "candidate-1",
            "attributorIds": ["carrier-1", "carrier-2"],
            "actorModelRef": "model://actor-1",
            "representationTraceRefs": ["trace://actor-model"],
            "attributedPolicy": "reward x and punish y",
            "scope": "declared decision domain",
            "horizon": "one preregistered episode",
            "uptakeMeasure": "change in action probability",
            "evidenceRefs": ["evidence://representation"],
            "tier": "[B] bounded fixture",
            "rivalModels": ["demand effect", "material incentive"],
            "killCriterion": "actor framing adds no effect",
        },
        "strategicAssessment": {
            "tests": {name: test_record() for name in strategic_names},
            "verdict": "PASS",
            "evidenceRefs": ["evidence://strategic"],
            "rivalModels": ["retrospective observer story"],
            "killCriterion": "no incremental prospective value",
        },
        "separateClaimRefs": {
            "consciousnessClaimRef": None,
            "personhoodClaimRef": None,
            "metaphysicalIndependenceClaimRef": None,
            "justiceAssessmentRef": "assessment://justice-1",
            "legitimacyAssessmentRef": None,
            "authorizationRef": None,
        },
        "resultState": "SURVIVES",
        "killCriterion": "strategic framing fails the incremental test",
        "survivorIfKilled": "ordinary trace, incentive, and institution models",
    }


class EgregoreotypeCandidateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def assert_valid(self, instance: dict[str, object]) -> None:
        self.assertEqual([], list(self.validator.iter_errors(instance)))

    def assert_invalid(self, instance: dict[str, object]) -> None:
        self.assertNotEqual([], list(self.validator.iter_errors(instance)))

    def test_complete_strategic_candidate_is_structurally_valid(self) -> None:
        self.assert_valid(passing_instance())

    def test_parent_pass_requires_all_five_marker_passes(self) -> None:
        instance = passing_instance()
        instance["baseCandidate"]["markers"]["carrierTurnover"]["status"] = "FAIL"
        self.assert_invalid(instance)

    def test_strategic_pass_requires_parent_pass(self) -> None:
        instance = passing_instance()
        instance["baseCandidate"]["verdict"] = "UNDERDETERMINED"
        self.assert_invalid(instance)

    def test_strategic_pass_requires_agent_representation(self) -> None:
        instance = passing_instance()
        instance["agentRepresentation"] = None
        self.assert_invalid(instance)

    def test_strategic_pass_requires_all_incremental_tests(self) -> None:
        instance = passing_instance()
        tests = instance["strategicAssessment"]["tests"]
        tests["incrementalValueBeyondRivals"]["status"] = "UNDERDETERMINED"
        self.assert_invalid(instance)

    def test_consciousness_shortcut_is_forbidden(self) -> None:
        instance = passing_instance()
        instance["conscious"] = True
        self.assert_invalid(instance)

    def test_legitimacy_shortcut_is_forbidden(self) -> None:
        instance = passing_instance()
        representation = instance["agentRepresentation"]
        representation["legitimate"] = True
        self.assert_invalid(instance)

    def test_untested_non_strategic_record_may_keep_representation_null(self) -> None:
        instance = passing_instance()
        instance["baseCandidate"]["verdict"] = "UNTESTED"
        instance["agentRepresentation"] = None
        instance["strategicAssessment"]["verdict"] = "UNTESTED"
        instance["resultState"] = "UNRUN"
        self.assert_valid(instance)


if __name__ == "__main__":
    unittest.main()
