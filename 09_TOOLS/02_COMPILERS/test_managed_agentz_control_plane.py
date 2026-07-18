from __future__ import annotations

import copy
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from coincurve import PrivateKey


ROOT = Path(__file__).resolve().parents[2]
MANAGED = ROOT / "08_FRAMEWORK_SUPPORT/08_AGENTS/MANAGED_AGENTS"
sys.path.insert(0, str(MANAGED))
import contract  # noqa: E402


AUTH_PRIVATE_KEY = PrivateKey(bytes.fromhex("11" * 32))
DEPLOYMENT_PRIVATE_KEY = PrivateKey(bytes.fromhex("22" * 32))
WRONG_PRIVATE_KEY = PrivateKey(bytes.fromhex("33" * 32))
COMMITMENT_PRIVATE_KEY = PrivateKey(bytes.fromhex("44" * 32))
OUTCOME_PRIVATE_KEY = PrivateKey(bytes.fromhex("55" * 32))
AUTH_KEY_ID = "fixture-authorization-key"
DEPLOYMENT_KEY_ID = "fixture-deployment-key"
COMMITMENT_KEY_ID = "fixture-commitment-key"
OUTCOME_KEY_ID = "fixture-outcome-key"


def future(days: int = 30) -> str:
    value = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=days)
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def past(days: int = 1) -> str:
    value = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def trust_policy() -> dict:
    return {
        "schemaVersion": "1.0",
        "policyId": "managed-agentz-test-policy",
        "authorizationSigners": [
            {
                "keyId": AUTH_KEY_ID,
                "publicKeyHex": AUTH_PRIVATE_KEY.public_key_xonly.format().hex(),
                "principalIds": ["test-principal"],
            }
        ],
        "deploymentVerifiers": [
            {
                "keyId": DEPLOYMENT_KEY_ID,
                "publicKeyHex": DEPLOYMENT_PRIVATE_KEY.public_key_xonly.format().hex(),
                "verifierIds": ["independent-adapter-fixture"],
            }
        ],
        "commitmentIssuers": [
            {
                "keyId": COMMITMENT_KEY_ID,
                "publicKeyHex": COMMITMENT_PRIVATE_KEY.public_key_xonly.format().hex(),
                "issuerIds": ["trusted-action-wrapper"],
            }
        ],
        "outcomeIssuers": [
            {
                "keyId": OUTCOME_KEY_ID,
                "publicKeyHex": OUTCOME_PRIVATE_KEY.public_key_xonly.format().hex(),
                "issuerIds": ["trusted-world-wrapper"],
            }
        ],
        "maxAuthorizationAgeSeconds": 172800,
        "maxDeploymentAgeSeconds": 172800,
        "maxReceiptAgeSeconds": 172800,
        "maxFutureSkewSeconds": 60,
    }


def action_plan(*, consequential: bool = True) -> dict:
    return {
        "schemaVersion": "1.0",
        "planId": "plan-test-1",
        "summary": "Apply one bounded fixture edit and stop.",
        "repository": "https://github.com/example/repo",
        "repositoryRef": "deadbeef",
        "operations": ["read", "write"] if consequential else ["read"],
        "requestedPaths": ["docs/test.md"] if consequential else ["docs/test.md"],
    }


def sign_authorization(value: dict, key: PrivateKey = AUTH_PRIVATE_KEY) -> dict:
    value["signature"] = ""
    value["signature"] = key.sign_schnorr(
        contract.authorization_signature_digest(value),
        aux_randomness=None,
    ).hex()
    return value


def envelope(plan_sha256: str) -> dict:
    value = {
        "schemaVersion": "1.0",
        "envelopeId": "env-test-1",
        "actionPlanSha256": plan_sha256,
        "principal": "test-principal",
        "mandate": "Apply a bounded fixture edit.",
        "scope": {
            "repository": "https://github.com/example/repo",
            "repositoryRef": "deadbeef",
            "allowedPaths": ["docs/test.md"],
            "allowedOperations": ["read", "write"],
        },
        "consent": {
            "status": "granted",
            "grantedBy": "test-principal",
            "grantedAt": past(),
        },
        "custody": "test-principal",
        "issuedAt": past(),
        "expiresAt": future(),
        "revoked": False,
        "contestPath": "https://github.com/example/repo/issues",
        "actor": "Emergentism L4",
        "consequenceBearerIds": ["principal", "corpus"],
        "payerIds": ["principal"],
        "beneficiaryIds": ["principal", "corpus"],
        "expectedBearerDeltas": {"principal": 0.0, "corpus": 1.0},
        "signerKeyId": AUTH_KEY_ID,
        "signature": "",
    }
    return sign_authorization(value)


def request(*, consequential: bool = True) -> dict:
    plan = action_plan(consequential=consequential)
    plan_sha256 = contract.sha256_value(plan)
    return {
        "schemaVersion": "1.0",
        "requestId": "request-test-1",
        "task": "Apply one bounded fixture edit and stop.",
        "consequential": consequential,
        "operations": ["read", "write"] if consequential else ["read"],
        "repository": "https://github.com/example/repo",
        "repositoryRef": "deadbeef",
        "actionPlan": plan,
        "actionPlanSha256": plan_sha256,
        "budget": {
            "maxCalls": 12,
            "maxTokens": 20000,
            "maxWallSeconds": 900,
            "maxDelegations": 3,
        },
        "evaluation": {
            "contract": "blinded_budget_matched_against_flat_and_shorter_rivals",
            "blind": True,
            "rivals": ["flat", "shorter"],
        },
        "authorization": envelope(plan_sha256) if consequential else None,
    }


def deployment(lock: dict) -> dict:
    value = {
        "schemaVersion": "1.0",
        "status": "remote_verified",
        "bundleSha256": lock["bundleSha256"],
        "environment": {
            "id": "env_remote_1",
            "configSha256": lock["environment"]["configSha256"],
        },
        "agents": [
            {
                "level": row["level"],
                "id": f"agent_{row['level'].lower()}",
                "version": 1,
                "configSha256": row["configSha256"],
            }
            for row in lock["agents"]
        ],
        "topology": lock["topology"],
        "verifiedAt": past(),
        "verifier": "independent-adapter-fixture",
        "attestation": {
            "keyId": DEPLOYMENT_KEY_ID,
            "signedAt": past(),
            "signature": "",
        },
    }
    return sign_deployment(value)


def sign_deployment(value: dict, key: PrivateKey = DEPLOYMENT_PRIVATE_KEY) -> dict:
    value["attestation"]["signature"] = ""
    value["attestation"]["signature"] = key.sign_schnorr(
        contract.deployment_signature_digest(value),
        aux_randomness=None,
    ).hex()
    return value


def commitment(run_request: dict, deployed: dict) -> dict:
    value = {
        "schemaVersion": "1.0",
        "receiptType": "commitment",
        "requestId": run_request["requestId"],
        "actionId": "action-test-1",
        "status": "attempt_started",
        "authorizationAssessment": {
            "status": "valid",
            "envelopeSha256": contract.sha256_value(run_request["authorization"]),
            "reasons": [],
        },
        "actionPlanSha256": run_request["actionPlanSha256"],
        "budgetSha256": contract.sha256_value(run_request["budget"]),
        "deploymentSha256": contract.sha256_value(deployed),
        "issuedBy": "trusted-action-wrapper",
        "attestation": {
            "keyId": COMMITMENT_KEY_ID,
            "signedAt": past(),
            "signature": "",
        },
    }
    return sign_commitment(value)


def sign_commitment(
    value: dict, key: PrivateKey = COMMITMENT_PRIVATE_KEY
) -> dict:
    value["attestation"]["signature"] = ""
    value["attestation"]["signature"] = key.sign_schnorr(
        contract.commitment_signature_digest(value),
        aux_randomness=None,
    ).hex()
    return value


def outcome(run_request: dict) -> dict:
    value = {
        "schemaVersion": "1.0",
        "receiptType": "outcome",
        "receiptCause": "action_attempt",
        "requestId": run_request["requestId"],
        "actionId": "action-test-1",
        "actionPlanSha256": run_request["actionPlanSha256"],
        "status": "observed",
        "consequenceBearerIds": ["principal", "corpus"],
        "observedBearerDeltas": {"principal": 0.0, "corpus": 1.0},
        "justiceAssessment": {
            "status": "complete",
            "justiceSatisfied": True,
            "bearerCoverageComplete": True,
            "focalIndividualId": "principal",
            "declaredWholeId": "corpus",
            "focalBeneficiaryIds": ["corpus"],
            "assessedBy": "trusted-world-wrapper",
            "reasons": [],
        },
        "classification": {
            "status": "classified",
            "demonBearing": False,
            "godBearing": True,
            "preservativeStasis": False,
            "strictSyntropy": False,
        },
        "issuedBy": "trusted-world-wrapper",
        "attestation": {
            "keyId": OUTCOME_KEY_ID,
            "signedAt": past(),
            "signature": "",
        },
    }
    return sign_outcome(value)


def sign_outcome(value: dict, key: PrivateKey = OUTCOME_PRIVATE_KEY) -> dict:
    value["attestation"]["signature"] = ""
    value["attestation"]["signature"] = key.sign_schnorr(
        contract.outcome_signature_digest(value),
        aux_randomness=None,
    ).hex()
    return value


def validate_outcome(
    value: dict,
    run_request: dict,
    deployed: dict | None,
    committed: dict | None,
    *,
    policy: dict | None = None,
) -> dict:
    policy = policy or trust_policy()
    return contract.validate_outcome_receipt(
        value,
        request=run_request,
        deployment=deployed,
        commitment=committed,
        trust_policy=policy,
        expected_trust_policy_sha256=contract.sha256_value(policy),
    )


class ManagedAgentzControlPlaneTests(unittest.TestCase):
    def test_live_lock_is_current_and_deterministic(self) -> None:
        first = contract.build_lock()
        second = contract.build_lock()
        self.assertEqual(first, second)
        self.assertEqual(first, contract.validate_lock())
        self.assertEqual(7, len(first["agents"]))
        self.assertEqual("unprovisioned_x0", first["calibrationStatus"])

    def test_semantic_hash_ignores_yaml_comments_and_key_order(self) -> None:
        left = "# comment\nname: A\nmodel: m\nsystem: s\ntools: []\nmetadata: {level: L1}\n"
        right = "metadata:\n  level: L1\ntools: []\nsystem: s\nmodel: m\nname: A # another\n"
        with tempfile.TemporaryDirectory() as td:
            one = Path(td) / "one.yaml"
            two = Path(td) / "two.yaml"
            one.write_text(left, encoding="utf-8")
            two.write_text(right, encoding="utf-8")
            a = contract._api_agent_payload(contract.load_yaml(one))
            b = contract._api_agent_payload(contract.load_yaml(two))
        self.assertEqual(contract.sha256_value(a), contract.sha256_value(b))

    def test_prompt_model_tool_permission_and_environment_mutations_change_hashes(
        self,
    ) -> None:
        path = sorted(contract.AGENTS_DIR.glob("*.agent.yaml"))[0]
        base = contract._api_agent_payload(contract.load_yaml(path))
        mutations = []
        prompt = copy.deepcopy(base)
        prompt["system"] += "\nchanged"
        mutations.append(prompt)
        model = copy.deepcopy(base)
        model["model"] = "different-model"
        mutations.append(model)
        tools = copy.deepcopy(base)
        tools["tools"] = []
        mutations.append(tools)
        permission = copy.deepcopy(base)
        permission["tools"][0]["configs"][0]["enabled"] = False
        mutations.append(permission)
        baseline = contract.sha256_value(base)
        for mutant in mutations:
            self.assertNotEqual(baseline, contract.sha256_value(mutant))

        environment = contract._api_environment_payload(
            contract.load_yaml(contract.ENV_PATH)
        )
        changed = copy.deepcopy(environment)
        changed["config"]["networking"]["type"] = "unrestricted"
        self.assertNotEqual(
            contract.sha256_value(environment), contract.sha256_value(changed)
        )

    def test_duplicate_yaml_keys_fail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "duplicate.yaml"
            path.write_text("name: first\nname: second\n", encoding="utf-8")
            with self.assertRaisesRegex(contract.ContractError, "duplicate YAML key"):
                contract.load_yaml(path)
            duplicate_json = Path(td) / "duplicate.json"
            duplicate_json.write_text(
                '{"schemaVersion":"1.0","schemaVersion":"2.0"}', encoding="utf-8"
            )
            with self.assertRaisesRegex(contract.ContractError, "duplicate JSON key"):
                contract.load_json(duplicate_json, "duplicate fixture")

    def test_unknown_agent_field_fails(self) -> None:
        path = sorted(contract.AGENTS_DIR.glob("*.agent.yaml"))[0]
        spec = contract.load_yaml(path)
        spec["surprise"] = True
        with self.assertRaisesRegex(contract.ContractError, "unknown keys"):
            contract._api_agent_payload(spec)

    def test_budget_rejects_missing_noninteger_zero_and_negative_limits(self) -> None:
        good = request()["budget"]
        for key in sorted(contract.BUDGET_KEYS):
            mutant = copy.deepcopy(good)
            mutant.pop(key)
            with self.assertRaises(contract.ContractError):
                contract.validate_budget(mutant)
        for key, value in (
            ("maxCalls", 0),
            ("maxTokens", -1),
            ("maxWallSeconds", 0),
            ("maxDelegations", -1),
        ):
            mutant = copy.deepcopy(good)
            mutant[key] = value
            with self.assertRaises(contract.ContractError):
                contract.validate_budget(mutant)
        mutant = copy.deepcopy(good)
        mutant["maxCalls"] = 1.5
        with self.assertRaises(contract.ContractError):
            contract.validate_budget(mutant)

    def test_authorization_rejects_expired_revoked_scope_and_bearer_gaps(self) -> None:
        base_request = request()
        tests = []
        expired = copy.deepcopy(base_request["authorization"])
        expired["expiresAt"] = past()
        tests.append(expired)
        revoked = copy.deepcopy(base_request["authorization"])
        revoked["revoked"] = True
        tests.append(revoked)
        scope = copy.deepcopy(base_request["authorization"])
        scope["scope"]["allowedOperations"] = ["read"]
        tests.append(scope)
        payer = copy.deepcopy(base_request["authorization"])
        payer["payerIds"] = ["hidden-payer"]
        tests.append(payer)
        delta = copy.deepcopy(base_request["authorization"])
        delta["expectedBearerDeltas"].pop("corpus")
        tests.append(delta)
        for mutant in tests:
            with self.assertRaises(contract.ContractError):
                contract.validate_authorization(
                    mutant,
                    repository="https://github.com/example/repo",
                    operations=["read", "write"],
                    requested_paths=["docs/test.md"],
                    action_plan_sha256=base_request["actionPlanSha256"],
                    trust_policy=trust_policy(),
                )

    def test_action_plan_scope_hash_and_bip340_authority_fail_closed(self) -> None:
        policy = trust_policy()
        good = request()
        self.assertEqual(good, contract.validate_run_request(good, trust_policy=policy))

        outside = copy.deepcopy(good)
        outside["actionPlan"]["requestedPaths"] = ["secrets/private.txt"]
        outside["actionPlanSha256"] = contract.sha256_value(outside["actionPlan"])
        outside["authorization"]["actionPlanSha256"] = outside["actionPlanSha256"]
        sign_authorization(outside["authorization"])
        with self.assertRaisesRegex(
            contract.ContractError, "paths exceed authorization scope"
        ):
            contract.validate_run_request(outside, trust_policy=policy)

        traversal = copy.deepcopy(good)
        traversal["actionPlan"]["requestedPaths"] = ["docs/../secrets.txt"]
        traversal["actionPlanSha256"] = contract.sha256_value(traversal["actionPlan"])
        traversal["authorization"]["actionPlanSha256"] = traversal["actionPlanSha256"]
        sign_authorization(traversal["authorization"])
        with self.assertRaisesRegex(contract.ContractError, "parent traversal"):
            contract.validate_run_request(traversal, trust_policy=policy)

        stale_hash = copy.deepcopy(good)
        stale_hash["actionPlan"]["summary"] = "mutated after authorization"
        with self.assertRaisesRegex(contract.ContractError, "actionPlan hash mismatch"):
            contract.validate_run_request(stale_hash, trust_policy=policy)

        forged = copy.deepcopy(good)
        sign_authorization(forged["authorization"], WRONG_PRIVATE_KEY)
        with self.assertRaisesRegex(contract.ContractError, "signature is invalid"):
            contract.validate_run_request(forged, trust_policy=policy)

        with mock.patch.object(
            contract,
            "_verify_bip340",
            side_effect=contract.ContractError("coincurve unavailable"),
        ):
            with self.assertRaisesRegex(
                contract.ContractError, "coincurve unavailable"
            ):
                contract.validate_run_request(good, trust_policy=policy)

    def test_nonconsequential_request_cannot_smuggle_mutation_or_authority(
        self,
    ) -> None:
        clean = request(consequential=False)
        self.assertEqual(clean, contract.validate_run_request(clean))
        mutation = copy.deepcopy(clean)
        mutation["operations"] = ["write"]
        with self.assertRaises(contract.ContractError):
            contract.validate_run_request(mutation)
        authority = copy.deepcopy(clean)
        authority["authorization"] = envelope(clean["actionPlanSha256"])
        with self.assertRaises(contract.ContractError):
            contract.validate_run_request(authority)

    def test_deployment_receipt_binds_exact_bundle_versions_hashes_and_topology(
        self,
    ) -> None:
        lock = contract.validate_lock()
        good = deployment(lock)
        self.assertEqual(
            good,
            contract.validate_deployment_receipt(
                good, lock, trust_policy=trust_policy()
            ),
        )
        mutations = []
        stale = copy.deepcopy(good)
        stale["bundleSha256"] = "0" * 64
        mutations.append(stale)
        version = copy.deepcopy(good)
        version["agents"][0]["version"] = 0
        mutations.append(version)
        agent_hash = copy.deepcopy(good)
        agent_hash["agents"][0]["configSha256"] = "0" * 64
        mutations.append(agent_hash)
        topology = copy.deepcopy(good)
        topology["topology"]["coordinator"] = "L7"
        mutations.append(topology)
        for mutant in mutations:
            with self.assertRaises(contract.ContractError):
                contract.validate_deployment_receipt(
                    mutant,
                    lock,
                    trust_policy=trust_policy(),
                )

    def test_deployment_requires_trusted_fresh_bip340_attestation(self) -> None:
        lock = contract.validate_lock()
        policy = trust_policy()
        good = deployment(lock)
        contract.validate_deployment_receipt(good, lock, trust_policy=policy)

        forged = copy.deepcopy(good)
        sign_deployment(forged, WRONG_PRIVATE_KEY)
        with self.assertRaisesRegex(contract.ContractError, "signature is invalid"):
            contract.validate_deployment_receipt(forged, lock, trust_policy=policy)

        unknown = copy.deepcopy(good)
        unknown["attestation"]["keyId"] = "unknown-key"
        sign_deployment(unknown)
        with self.assertRaisesRegex(contract.ContractError, "not trusted"):
            contract.validate_deployment_receipt(unknown, lock, trust_policy=policy)

        stale = copy.deepcopy(good)
        stale["verifiedAt"] = past(days=30)
        stale["attestation"]["signedAt"] = past(days=30)
        sign_deployment(stale)
        with self.assertRaisesRegex(contract.ContractError, "stale"):
            contract.validate_deployment_receipt(stale, lock, trust_policy=policy)

    def test_schema_keeps_commitment_and_outcome_types_distinct(self) -> None:
        schema = json.loads(contract.SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(
            "commitment",
            schema["$defs"]["CommitmentReceipt"]["properties"]["receiptType"]["const"],
        )
        self.assertEqual(
            "outcome",
            schema["$defs"]["OutcomeReceipt"]["properties"]["receiptType"]["const"],
        )
        self.assertEqual(
            ["action_attempt", "ambient_observation"],
            schema["$defs"]["OutcomeReceipt"]["properties"]["receiptCause"]["enum"],
        )

    def test_trusted_receipt_validators_reject_type_confusion_model_issuers_and_bad_linkage(
        self,
    ) -> None:
        lock = contract.validate_lock()
        run_request = request()
        deployed = deployment(lock)
        committed = commitment(run_request, deployed)
        observed = outcome(run_request)
        policy = trust_policy()
        self.assertEqual(
            committed,
            contract.validate_commitment_receipt(
                committed,
                request=run_request,
                deployment=deployed,
                trust_policy=policy,
                expected_trust_policy_sha256=contract.sha256_value(policy),
            ),
        )
        self.assertEqual(
            observed,
            validate_outcome(observed, run_request, deployed, committed),
        )

        forged_commitment = copy.deepcopy(committed)
        sign_commitment(forged_commitment, WRONG_PRIVATE_KEY)
        with self.assertRaisesRegex(contract.ContractError, "signature is invalid"):
            validate_outcome(observed, run_request, deployed, forged_commitment)

        forged_outcome = copy.deepcopy(observed)
        sign_outcome(forged_outcome, WRONG_PRIVATE_KEY)
        with self.assertRaisesRegex(contract.ContractError, "signature is invalid"):
            validate_outcome(forged_outcome, run_request, deployed, committed)

        stale_outcome = copy.deepcopy(observed)
        stale_outcome["attestation"]["signedAt"] = past(days=30)
        sign_outcome(stale_outcome)
        with self.assertRaisesRegex(contract.ContractError, "stale"):
            validate_outcome(stale_outcome, run_request, deployed, committed)

        later_commitment = copy.deepcopy(committed)
        later_commitment["attestation"]["signedAt"] = future(days=0)
        sign_commitment(later_commitment)
        with self.assertRaisesRegex(contract.ContractError, "predates the attempted"):
            validate_outcome(observed, run_request, deployed, later_commitment)

        with self.assertRaisesRegex(contract.ContractError, "trust-policy SHA-256"):
            contract.validate_outcome_receipt(
                observed,
                request=run_request,
                deployment=deployed,
                commitment=committed,
                trust_policy=policy,
                expected_trust_policy_sha256="0" * 64,
            )
        type_confusion = copy.deepcopy(observed)
        type_confusion["receiptType"] = "commitment"
        with self.assertRaisesRegex(contract.ContractError, "type confusion"):
            validate_outcome(type_confusion, run_request, deployed, committed)

        with self.assertRaisesRegex(contract.ContractError, "requires a commitment"):
            validate_outcome(observed, run_request, deployed, None)

        shallow_fake = {
            "status": "attempt_started",
            "actionId": committed["actionId"],
            "actionPlanSha256": committed["actionPlanSha256"],
        }
        with self.assertRaisesRegex(contract.ContractError, "commitmentReceipt missing keys"):
            validate_outcome(observed, run_request, deployed, shallow_fake)

        same_role_policy = trust_policy()
        same_role_policy["outcomeIssuers"][0]["keyId"] = COMMITMENT_KEY_ID
        same_role_policy["outcomeIssuers"][0]["publicKeyHex"] = (
            COMMITMENT_PRIVATE_KEY.public_key_xonly.format().hex()
        )
        same_role_policy["outcomeIssuers"][0]["issuerIds"] = [
            "trusted-action-wrapper"
        ]
        with self.assertRaisesRegex(
            contract.ContractError, "duplicate keyId|public keys|identities"
        ):
            validate_outcome(
                observed,
                run_request,
                deployed,
                committed,
                policy=same_role_policy,
            )

        classified_ambient = copy.deepcopy(observed)
        classified_ambient["receiptCause"] = "ambient_observation"
        classified_ambient["actionId"] = None
        sign_outcome(classified_ambient)
        with self.assertRaisesRegex(contract.ContractError, "must remain unclassified"):
            validate_outcome(classified_ambient, run_request, None, None)

    def test_outcome_justice_classes_are_exact_and_incomplete_receipts_stay_unclassified(
        self,
    ) -> None:
        lock = contract.validate_lock()
        run_request = request()
        deployed = deployment(lock)
        committed = commitment(run_request, deployed)

        cases = [
            (
                {"principal": 1.0, "corpus": -1.0},
                False,
                {
                    "demonBearing": True,
                    "godBearing": False,
                    "preservativeStasis": False,
                    "strictSyntropy": False,
                },
            ),
            (
                {"principal": 0.0, "corpus": 1.0},
                True,
                {
                    "demonBearing": False,
                    "godBearing": True,
                    "preservativeStasis": False,
                    "strictSyntropy": False,
                },
            ),
            (
                {"principal": 0.0, "corpus": 0.0},
                True,
                {
                    "demonBearing": False,
                    "godBearing": False,
                    "preservativeStasis": True,
                    "strictSyntropy": False,
                },
            ),
            (
                {"principal": 1.0, "corpus": 1.0},
                True,
                {
                    "demonBearing": False,
                    "godBearing": True,
                    "preservativeStasis": False,
                    "strictSyntropy": True,
                },
            ),
        ]
        for deltas, justice_satisfied, expected in cases:
            receipt = outcome(run_request)
            receipt["observedBearerDeltas"] = deltas
            receipt["justiceAssessment"]["justiceSatisfied"] = justice_satisfied
            if expected["demonBearing"]:
                receipt["justiceAssessment"]["focalBeneficiaryIds"] = ["principal"]
            receipt["classification"].update(expected)
            sign_outcome(receipt)
            self.assertEqual(
                receipt,
                validate_outcome(receipt, run_request, deployed, committed),
            )

        wrong = outcome(run_request)
        wrong["classification"]["strictSyntropy"] = True
        sign_outcome(wrong)
        with self.assertRaisesRegex(contract.ContractError, "strictSyntropy"):
            validate_outcome(wrong, run_request, deployed, committed)

        pending = outcome(run_request)
        pending["status"] = "pending"
        pending["observedBearerDeltas"] = {"principal": None, "corpus": None}
        pending["justiceAssessment"].update(
            {
                "status": "incomplete",
                "justiceSatisfied": None,
                "bearerCoverageComplete": False,
                "focalIndividualId": None,
                "declaredWholeId": None,
                "focalBeneficiaryIds": [],
                "assessedBy": None,
                "reasons": ["pending world observation"],
            }
        )
        pending["classification"] = {
            "status": "unclassified",
            "demonBearing": None,
            "godBearing": None,
            "preservativeStasis": None,
            "strictSyntropy": None,
        }
        sign_outcome(pending)
        validate_outcome(pending, run_request, deployed, committed)
        inflated = copy.deepcopy(pending)
        inflated["classification"]["godBearing"] = True
        sign_outcome(inflated)
        with self.assertRaisesRegex(contract.ContractError, "cannot assert"):
            validate_outcome(inflated, run_request, deployed, committed)
        observed = outcome(run_request)
        model_issued = copy.deepcopy(observed)
        model_issued["issuedBy"] = "model-prose"
        sign_outcome(model_issued)
        with self.assertRaisesRegex(contract.ContractError, "issuer identity"):
            validate_outcome(model_issued, run_request, deployed, committed)
        bad_link = copy.deepcopy(observed)
        bad_link["actionId"] = "different-action"
        sign_outcome(bad_link)
        with self.assertRaisesRegex(contract.ContractError, "action linkage mismatch"):
            validate_outcome(bad_link, run_request, deployed, committed)

    def test_ambient_outcome_requires_null_action_and_pending_cannot_invent_delta(
        self,
    ) -> None:
        run_request = request(consequential=False)
        ambient = {
            "schemaVersion": "1.0",
            "receiptType": "outcome",
            "receiptCause": "ambient_observation",
            "requestId": run_request["requestId"],
            "actionId": None,
            "actionPlanSha256": run_request["actionPlanSha256"],
            "status": "pending",
            "consequenceBearerIds": ["corpus"],
            "observedBearerDeltas": {"corpus": None},
            "justiceAssessment": {
                "status": "incomplete",
                "justiceSatisfied": None,
                "bearerCoverageComplete": False,
                "focalIndividualId": None,
                "declaredWholeId": None,
                "focalBeneficiaryIds": [],
                "assessedBy": None,
                "reasons": ["outcome pending"],
            },
            "classification": {
                "status": "unclassified",
                "demonBearing": None,
                "godBearing": None,
                "preservativeStasis": None,
                "strictSyntropy": None,
            },
            "issuedBy": "trusted-world-wrapper",
            "attestation": {
                "keyId": OUTCOME_KEY_ID,
                "signedAt": past(),
                "signature": "",
            },
        }
        sign_outcome(ambient)
        validate_outcome(ambient, run_request, None, None)
        mutant = copy.deepcopy(ambient)
        mutant["observedBearerDeltas"]["corpus"] = 1.0
        sign_outcome(mutant)
        with self.assertRaisesRegex(contract.ContractError, "cannot invent deltas"):
            validate_outcome(mutant, run_request, None, None)

    def test_offline_provision_modes_make_no_sdk_or_network_call(self) -> None:
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        check = subprocess.run(
            [sys.executable, "provision.py", "--check-local"],
            cwd=MANAGED,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(0, check.returncode, check.stderr)
        self.assertIn("remote_calls=0", check.stdout)
        apply = subprocess.run(
            [sys.executable, "provision.py", "--apply"],
            cwd=MANAGED,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(2, apply.returncode)
        self.assertIn("REMOTE_ADAPTER_UNSUPPORTED", apply.stderr)

    def test_run_preflight_and_execute_refusal_emit_no_receipts(self) -> None:
        lock = contract.validate_lock()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request_path = root / "request.json"
            deployment_path = root / "deployment.json"
            trust_path = root / "trust-policy.json"
            request_path.write_text(json.dumps(request()), encoding="utf-8")
            deployment_path.write_text(json.dumps(deployment(lock)), encoding="utf-8")
            trust_path.write_text(json.dumps(trust_policy()), encoding="utf-8")
            trust_sha256 = contract.sha256_value(trust_policy())
            env = dict(os.environ)
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            base = [
                sys.executable,
                "run_session.py",
                "--request",
                str(request_path),
                "--deployment-receipt",
                str(deployment_path),
                "--trust-policy",
                str(trust_path),
                "--expect-trust-policy-sha256",
                trust_sha256,
            ]
            preflight = subprocess.run(
                base,
                cwd=MANAGED,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(0, preflight.returncode, preflight.stderr)
            value = json.loads(preflight.stdout)
            self.assertEqual(0, value["remoteCalls"])
            self.assertEqual(request()["actionPlanSha256"], value["actionPlanSha256"])
            self.assertIsNone(value["commitmentReceipt"])
            self.assertIsNone(value["outcomeReceipt"])
            execute = subprocess.run(
                [*base, "--execute"],
                cwd=MANAGED,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(2, execute.returncode)
            self.assertIn("REMOTE_ADAPTER_UNSUPPORTED", execute.stderr)
            wrong_policy_hash = subprocess.run(
                [*base[:-1], "0" * 64],
                cwd=MANAGED,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(1, wrong_policy_hash.returncode)
            self.assertIn("trust-policy SHA-256 mismatch", wrong_policy_hash.stderr)
            self.assertEqual([], list(root.glob("*receipt*")))


if __name__ == "__main__":
    unittest.main()
