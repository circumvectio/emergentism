#!/usr/bin/env python3
"""Pure, fail-closed contracts for the local Managed Agentz bundle.

This module deliberately contains no provider SDK import.  It validates the
version-controlled seven-row configuration, produces semantic hashes, and
checks the records that a future provider adapter must supply before a hosted
run can begin.  It never provisions a remote resource or infers an outcome
from model prose or session status.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import hmac
import importlib.util
import json
import math
import os
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AGENTS_DIR = HERE / "agents"
ENV_PATH = HERE / "emergentism.environment.yaml"
SCHEMA_PATH = HERE / "managed_agentz.schema.json"
LOCK_PATH = HERE / "agentz.lock.json"
TRUST_POLICY_PATH = HERE / "local_state/trust_policy.json"
VALIDATOR_PATH = ROOT / "09_TOOLS/02_COMPILERS/validate_agentz_rosetta.py"

MUTATING_OPERATIONS = {"write", "edit", "bash"}
KNOWN_OPERATIONS = {
    "read",
    "grep",
    "glob",
    "web_search",
    "web_fetch",
    *MUTATING_OPERATIONS,
}
BUDGET_KEYS = {
    "maxCalls",
    "maxTokens",
    "maxWallSeconds",
    "maxDelegations",
}
AUTHORIZATION_KEYS = {
    "schemaVersion",
    "envelopeId",
    "actionPlanSha256",
    "principal",
    "mandate",
    "scope",
    "consent",
    "custody",
    "issuedAt",
    "expiresAt",
    "revoked",
    "contestPath",
    "actor",
    "consequenceBearerIds",
    "payerIds",
    "beneficiaryIds",
    "expectedBearerDeltas",
    "signerKeyId",
    "signature",
}
ACTION_PLAN_KEYS = {
    "schemaVersion",
    "planId",
    "summary",
    "repository",
    "repositoryRef",
    "operations",
    "requestedPaths",
}
RUN_REQUEST_KEYS = {
    "schemaVersion",
    "requestId",
    "task",
    "consequential",
    "operations",
    "repository",
    "repositoryRef",
    "actionPlan",
    "actionPlanSha256",
    "budget",
    "evaluation",
    "authorization",
}
TRUST_POLICY_KEYS = {
    "schemaVersion",
    "policyId",
    "authorizationSigners",
    "deploymentVerifiers",
    "commitmentIssuers",
    "outcomeIssuers",
    "maxAuthorizationAgeSeconds",
    "maxDeploymentAgeSeconds",
    "maxReceiptAgeSeconds",
    "maxFutureSkewSeconds",
}
AUTHORIZATION_SIGNER_KEYS = {"keyId", "publicKeyHex", "principalIds"}
DEPLOYMENT_VERIFIER_KEYS = {"keyId", "publicKeyHex", "verifierIds"}
RECEIPT_ISSUER_KEYS = {"keyId", "publicKeyHex", "issuerIds"}
ATTESTATION_KEYS = {"keyId", "signedAt", "signature"}
JUSTICE_ASSESSMENT_KEYS = {
    "status",
    "justiceSatisfied",
    "bearerCoverageComplete",
    "focalIndividualId",
    "declaredWholeId",
    "focalBeneficiaryIds",
    "assessedBy",
    "reasons",
}
OUTCOME_CLASSIFICATION_KEYS = {
    "status",
    "demonBearing",
    "godBearing",
    "preservativeStasis",
    "strictSyntropy",
}

AUTHORIZATION_SIGNATURE_DOMAIN = "emergentism-managed-agentz/authorization/v1"
DEPLOYMENT_SIGNATURE_DOMAIN = "emergentism-managed-agentz/deployment/v1"
COMMITMENT_SIGNATURE_DOMAIN = "emergentism-managed-agentz/commitment/v1"
OUTCOME_SIGNATURE_DOMAIN = "emergentism-managed-agentz/outcome/v1"


class ContractError(ValueError):
    """Stable local contract failure."""


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: yaml.Loader, node: yaml.Node, deep: bool = False
) -> dict:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ContractError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _closed(record: Any, keys: set[str], label: str) -> dict[str, Any]:
    _require(isinstance(record, dict), f"{label} must be an object")
    missing = sorted(keys - set(record))
    unknown = sorted(set(record) - keys)
    _require(not missing, f"{label} missing keys: {missing}")
    _require(not unknown, f"{label} unknown keys: {unknown}")
    return record


def _text(value: Any, label: str) -> str:
    _require(
        isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text"
    )
    return value


def _unique_text_list(
    value: Any, label: str, *, allow_empty: bool = False
) -> list[str]:
    _require(isinstance(value, list), f"{label} must be a list")
    if not allow_empty:
        _require(bool(value), f"{label} must be nonempty")
    _require(
        all(isinstance(item, str) and item.strip() == item and item for item in value),
        f"{label} must contain nonempty text",
    )
    _require(len(value) == len(set(value)), f"{label} must be unique")
    return value


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _signature_digest(domain: str, payload: Any) -> bytes:
    return hashlib.sha256(
        domain.encode("ascii") + b"\0" + _canonical_bytes(payload)
    ).digest()


def authorization_signature_digest(envelope: dict[str, Any]) -> bytes:
    """Return the domain-separated digest signed by an authorization principal."""
    payload = {key: value for key, value in envelope.items() if key != "signature"}
    return _signature_digest(AUTHORIZATION_SIGNATURE_DOMAIN, payload)


def deployment_signature_digest(receipt: dict[str, Any]) -> bytes:
    """Return the domain-separated digest signed by a deployment verifier."""
    payload = copy.deepcopy(receipt)
    attestation = payload.get("attestation")
    if isinstance(attestation, dict):
        attestation.pop("signature", None)
    return _signature_digest(DEPLOYMENT_SIGNATURE_DOMAIN, payload)


def commitment_signature_digest(receipt: dict[str, Any]) -> bytes:
    """Return the domain-separated digest signed by an action wrapper."""
    payload = copy.deepcopy(receipt)
    attestation = payload.get("attestation")
    if isinstance(attestation, dict):
        attestation.pop("signature", None)
    return _signature_digest(COMMITMENT_SIGNATURE_DOMAIN, payload)


def outcome_signature_digest(receipt: dict[str, Any]) -> bytes:
    """Return the domain-separated digest signed by a world-outcome issuer."""
    payload = copy.deepcopy(receipt)
    attestation = payload.get("attestation")
    if isinstance(attestation, dict):
        attestation.pop("signature", None)
    return _signature_digest(OUTCOME_SIGNATURE_DOMAIN, payload)


def _hex_bytes(value: Any, length: int, label: str) -> bytes:
    _require(
        isinstance(value, str) and len(value) == length * 2,
        f"{label} must be {length * 2} lowercase hex characters",
    )
    _require(value == value.lower(), f"{label} must use lowercase hex")
    try:
        decoded = bytes.fromhex(value)
    except ValueError as exc:
        raise ContractError(f"{label} must be hexadecimal") from exc
    _require(len(decoded) == length, f"{label} must decode to {length} bytes")
    return decoded


def _verify_bip340(
    public_key_hex: Any, digest: bytes, signature_hex: Any, label: str
) -> None:
    public_key = _hex_bytes(public_key_hex, 32, f"{label}.publicKeyHex")
    signature = _hex_bytes(signature_hex, 64, f"{label}.signature")
    try:
        from coincurve import PublicKeyXOnly
    except (ImportError, OSError) as exc:
        raise ContractError(
            "coincurve BIP-340 verification is unavailable; refusing authenticated control-plane record"
        ) from exc
    try:
        verified = PublicKeyXOnly(public_key).verify(signature, digest)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{label} BIP-340 verification failed") from exc
    _require(verified, f"{label} BIP-340 signature is invalid")


def _canonical_repo_paths(
    value: Any, label: str, *, allow_empty: bool = False
) -> list[str]:
    paths = _unique_text_list(value, label, allow_empty=allow_empty)
    for raw in paths:
        _require(
            "\\" not in raw and "\0" not in raw,
            f"{label} must use canonical POSIX repository paths",
        )
        path = PurePosixPath(raw)
        _require(not path.is_absolute(), f"{label} cannot contain absolute paths")
        _require(
            raw not in {"", "."}
            and all(part not in {"", ".", ".."} for part in path.parts),
            f"{label} cannot contain dot or parent traversal segments",
        )
        _require(path.as_posix() == raw, f"{label} must be normalized canonical paths")
    return paths


def validate_trust_policy(value: Any) -> dict[str, Any]:
    policy = _closed(value, TRUST_POLICY_KEYS, "trustPolicy")
    _require(policy["schemaVersion"] == "1.0", "trustPolicy schemaVersion must be 1.0")
    _text(policy["policyId"], "trustPolicy.policyId")
    for key in (
        "maxAuthorizationAgeSeconds",
        "maxDeploymentAgeSeconds",
        "maxReceiptAgeSeconds",
        "maxFutureSkewSeconds",
    ):
        item = policy[key]
        _require(
            isinstance(item, int) and not isinstance(item, bool) and item >= 0,
            f"trustPolicy.{key} must be a nonnegative integer",
        )
    _require(
        policy["maxAuthorizationAgeSeconds"] > 0,
        "trustPolicy.maxAuthorizationAgeSeconds must be positive",
    )
    _require(
        policy["maxDeploymentAgeSeconds"] > 0,
        "trustPolicy.maxDeploymentAgeSeconds must be positive",
    )
    _require(
        policy["maxReceiptAgeSeconds"] > 0,
        "trustPolicy.maxReceiptAgeSeconds must be positive",
    )

    seen_key_ids: set[str] = set()
    seen_public_keys: set[bytes] = set()

    def register_key(record: dict[str, Any], label: str) -> None:
        key_id = _text(record["keyId"], f"{label}.keyId")
        public_key = _hex_bytes(record["publicKeyHex"], 32, f"{label}.publicKeyHex")
        _require(
            key_id not in seen_key_ids,
            f"trustPolicy duplicate keyId: {key_id}",
        )
        _require(
            public_key not in seen_public_keys,
            "trustPolicy public keys must be unique across authority roles",
        )
        seen_key_ids.add(key_id)
        seen_public_keys.add(public_key)

    signers = policy["authorizationSigners"]
    _require(
        isinstance(signers, list) and bool(signers),
        "trustPolicy.authorizationSigners must be a nonempty list",
    )
    for index, value in enumerate(signers):
        signer = _closed(
            value,
            AUTHORIZATION_SIGNER_KEYS,
            f"trustPolicy.authorizationSigners[{index}]",
        )
        register_key(signer, f"trustPolicy.authorizationSigners[{index}]")
        _unique_text_list(
            signer["principalIds"],
            f"trustPolicy.authorizationSigners[{index}].principalIds",
        )

    verifiers = policy["deploymentVerifiers"]
    _require(
        isinstance(verifiers, list) and bool(verifiers),
        "trustPolicy.deploymentVerifiers must be a nonempty list",
    )
    for index, value in enumerate(verifiers):
        verifier = _closed(
            value, DEPLOYMENT_VERIFIER_KEYS, f"trustPolicy.deploymentVerifiers[{index}]"
        )
        register_key(verifier, f"trustPolicy.deploymentVerifiers[{index}]")
        _unique_text_list(
            verifier["verifierIds"],
            f"trustPolicy.deploymentVerifiers[{index}].verifierIds",
        )

    issuer_roles: dict[str, set[str]] = {}
    for collection in ("commitmentIssuers", "outcomeIssuers"):
        records = policy[collection]
        _require(
            isinstance(records, list) and bool(records),
            f"trustPolicy.{collection} must be a nonempty list",
        )
        issuer_ids: set[str] = set()
        for index, value in enumerate(records):
            issuer = _closed(
                value,
                RECEIPT_ISSUER_KEYS,
                f"trustPolicy.{collection}[{index}]",
            )
            register_key(issuer, f"trustPolicy.{collection}[{index}]")
            identifiers = _unique_text_list(
                issuer["issuerIds"],
                f"trustPolicy.{collection}[{index}].issuerIds",
            )
            _require(
                issuer_ids.isdisjoint(identifiers),
                f"trustPolicy.{collection} issuerIds must be unique",
            )
            issuer_ids.update(identifiers)
        issuer_roles[collection] = issuer_ids
    _require(
        issuer_roles["commitmentIssuers"].isdisjoint(issuer_roles["outcomeIssuers"]),
        "commitment and world-outcome issuer identities must be disjoint",
    )
    return policy


def load_trust_policy(path: Path = TRUST_POLICY_PATH) -> dict[str, Any]:
    return validate_trust_policy(load_json(path, "trust policy"))


def validate_pinned_trust_policy(
    value: Any, expected_sha256: str
) -> dict[str, Any]:
    policy = validate_trust_policy(value)
    _hex_bytes(expected_sha256, 32, "expected trust-policy SHA-256")
    _require(
        hmac.compare_digest(expected_sha256, sha256_value(policy)),
        "trust-policy SHA-256 mismatch",
    )
    return policy


def _trusted_record(
    policy: dict[str, Any], collection: str, key_id: str, label: str
) -> dict[str, Any]:
    matches = [record for record in policy[collection] if record["keyId"] == key_id]
    _require(len(matches) == 1, f"{label} keyId is not trusted by the local policy")
    return matches[0]


def _utc_now(now: dt.datetime | None) -> dt.datetime:
    current = now or dt.datetime.now(dt.timezone.utc)
    _require(current.tzinfo is not None, "validation time must include a timezone")
    return current.astimezone(dt.timezone.utc)


def _require_fresh(
    instant: dt.datetime,
    *,
    now: dt.datetime,
    max_age_seconds: int,
    max_future_skew_seconds: int,
    label: str,
) -> None:
    _require(
        instant <= now + dt.timedelta(seconds=max_future_skew_seconds),
        f"{label} is too far in the future",
    )
    _require(
        instant >= now - dt.timedelta(seconds=max_age_seconds), f"{label} is stale"
    )


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise ContractError(f"cannot load {path}: {exc}") from exc
    _require(isinstance(value, dict), f"{path} YAML root must be an object")
    return value


def _load_rosetta_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_agentz_rosetta_runtime", VALIDATOR_PATH
    )
    _require(
        spec is not None and spec.loader is not None,
        "cannot load Agentz Rosetta validator",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _api_agent_payload(spec: dict[str, Any]) -> dict[str, Any]:
    allowed = {"name", "model", "description", "system", "tools", "metadata"}
    unknown = sorted(set(spec) - allowed)
    missing = sorted({"name", "model", "system", "tools", "metadata"} - set(spec))
    _require(not missing, f"agent spec missing keys: {missing}")
    _require(not unknown, f"agent spec unknown keys: {unknown}")
    metadata = spec.get("metadata")
    _require(isinstance(metadata, dict), "agent metadata must be an object")
    return {
        "name": _text(spec["name"], "agent.name"),
        "model": _text(spec["model"], "agent.model"),
        "description": str(spec.get("description", "")),
        "system": _text(spec["system"], "agent.system"),
        "tools": spec["tools"],
        "metadata": {str(key): str(value) for key, value in sorted(metadata.items())},
    }


def _api_environment_payload(spec: dict[str, Any]) -> dict[str, Any]:
    allowed = {"name", "description", "config", "metadata"}
    missing = sorted({"name", "config", "metadata"} - set(spec))
    unknown = sorted(set(spec) - allowed)
    _require(not missing, f"environment spec missing keys: {missing}")
    _require(not unknown, f"environment spec unknown keys: {unknown}")
    _require(isinstance(spec["config"], dict), "environment.config must be an object")
    _require(
        isinstance(spec["metadata"], dict), "environment.metadata must be an object"
    )
    return {
        "name": _text(spec["name"], "environment.name"),
        "description": str(spec.get("description", "")),
        "config": spec["config"],
        "metadata": {
            str(key): str(value) for key, value in sorted(spec["metadata"].items())
        },
    }


def build_lock() -> dict[str, Any]:
    """Build the deterministic semantic lock from the checked local bundle."""
    validator = _load_rosetta_validator()
    errors = validator.validate_paths(AGENTS_DIR, ENV_PATH)
    _require(not errors, "Rosetta validation failed: " + "; ".join(errors))

    paths = sorted(AGENTS_DIR.glob("*.agent.yaml"))
    _require(len(paths) == 7, f"expected exactly seven agent YAMLs, found {len(paths)}")
    unexpected = sorted(
        path.name
        for path in AGENTS_DIR.iterdir()
        if path.is_file() and not path.name.endswith(".agent.yaml")
    )
    _require(not unexpected, f"unexpected files in agents directory: {unexpected}")

    records: list[dict[str, Any]] = []
    names: set[str] = set()
    levels: set[str] = set()
    for path in paths:
        payload = _api_agent_payload(load_yaml(path))
        level = payload["metadata"].get("level", "")
        _require(level not in levels, f"duplicate level: {level}")
        _require(
            payload["name"] not in names, f"duplicate agent name: {payload['name']}"
        )
        levels.add(level)
        names.add(payload["name"])
        records.append(
            {
                "level": level,
                "path": str(path.relative_to(HERE)),
                "name": payload["name"],
                "configSha256": sha256_value(payload),
            }
        )
    _require(
        levels == {f"L{index}" for index in range(1, 8)},
        f"levels are incomplete: {sorted(levels)}",
    )
    records.sort(key=lambda item: item["level"])

    environment_payload = _api_environment_payload(load_yaml(ENV_PATH))
    base = {
        "schemaVersion": "1.0",
        "calibrationStatus": "unprovisioned_x0",
        "schema": {
            "path": str(SCHEMA_PATH.relative_to(HERE)),
            "sha256": sha256_file(SCHEMA_PATH),
        },
        "environment": {
            "path": str(ENV_PATH.relative_to(HERE)),
            "name": environment_payload["name"],
            "configSha256": sha256_value(environment_payload),
        },
        "agents": records,
        "topology": {
            "coordinator": "L4",
            "delegates": ["L1", "L2", "L3", "L5", "L6", "L7"],
            "selfDelegation": True,
        },
    }
    return {**base, "bundleSha256": sha256_value(base)}


def load_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    try:
        value = _load_unique_json(path)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        raise ContractError(f"cannot load lock {path}: {exc}") from exc
    _require(isinstance(value, dict), "agentz lock must be an object")
    return value


def validate_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    current = build_lock()
    stored = load_lock(path)
    _require(
        stored == current,
        "agentz.lock.json is stale; regenerate it from the validated bundle",
    )
    return current


def write_lock(path: Path = LOCK_PATH) -> None:
    value = build_lock()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _parse_utc(value: Any, label: str) -> dt.datetime:
    text = _text(value, label)
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ContractError(f"{label} must be ISO-8601") from exc
    _require(parsed.tzinfo is not None, f"{label} must include a timezone")
    return parsed.astimezone(dt.timezone.utc)


def validate_budget(value: Any) -> dict[str, int]:
    budget = _closed(value, BUDGET_KEYS, "budget")
    for key in sorted(BUDGET_KEYS):
        item = budget[key]
        _require(
            isinstance(item, int) and not isinstance(item, bool),
            f"budget.{key} must be an integer",
        )
        if key == "maxDelegations":
            _require(item >= 0, "budget.maxDelegations must be nonnegative")
        else:
            _require(item > 0, f"budget.{key} must be positive")
    return budget


def validate_authorization(
    value: Any,
    *,
    repository: str,
    operations: list[str],
    requested_paths: list[str],
    action_plan_sha256: str,
    trust_policy: dict[str, Any],
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    envelope = _closed(value, AUTHORIZATION_KEYS, "authorization")
    _require(
        envelope["schemaVersion"] == "1.0", "authorization schemaVersion must be 1.0"
    )
    for field in (
        "envelopeId",
        "principal",
        "mandate",
        "custody",
        "contestPath",
        "actor",
    ):
        _text(envelope[field], f"authorization.{field}")
    _require(
        envelope["actionPlanSha256"] == action_plan_sha256,
        "authorization actionPlan hash mismatch",
    )
    _require(envelope["revoked"] is False, "authorization is revoked")
    policy = validate_trust_policy(trust_policy)
    current = _utc_now(now)
    issued_at = _parse_utc(envelope["issuedAt"], "authorization.issuedAt")
    expires_at = _parse_utc(envelope["expiresAt"], "authorization.expiresAt")
    _require(expires_at > current, "authorization is expired")
    _require(issued_at < expires_at, "authorization must be issued before it expires")
    _require_fresh(
        issued_at,
        now=current,
        max_age_seconds=policy["maxAuthorizationAgeSeconds"],
        max_future_skew_seconds=policy["maxFutureSkewSeconds"],
        label="authorization.issuedAt",
    )

    scope = _closed(
        envelope["scope"],
        {"repository", "repositoryRef", "allowedPaths", "allowedOperations"},
        "authorization.scope",
    )
    _require(scope["repository"] == repository, "authorization repository mismatch")
    _text(scope["repositoryRef"], "authorization.scope.repositoryRef")
    allowed_paths = _canonical_repo_paths(
        scope["allowedPaths"], "authorization.scope.allowedPaths"
    )
    requested_paths = _canonical_repo_paths(
        requested_paths,
        "runRequest.actionPlan.requestedPaths",
        allow_empty=True,
    )
    _require(
        set(requested_paths) <= set(allowed_paths),
        "requested action paths exceed authorization scope",
    )
    allowed = set(
        _unique_text_list(
            scope["allowedOperations"], "authorization.scope.allowedOperations"
        )
    )
    _require(allowed <= KNOWN_OPERATIONS, "authorization contains unknown operations")
    _require(
        set(operations) <= allowed, "requested operations exceed authorization scope"
    )

    consent = _closed(
        envelope["consent"],
        {"status", "grantedBy", "grantedAt"},
        "authorization.consent",
    )
    _require(consent["status"] == "granted", "authorization consent is not granted")
    _text(consent["grantedBy"], "authorization.consent.grantedBy")
    granted_at = _parse_utc(consent["grantedAt"], "authorization.consent.grantedAt")
    _require(
        granted_at <= current + dt.timedelta(seconds=policy["maxFutureSkewSeconds"]),
        "authorization consent is too far in the future",
    )
    _require(
        granted_at <= issued_at + dt.timedelta(seconds=policy["maxFutureSkewSeconds"]),
        "authorization consent postdates the signed envelope",
    )

    bearers = _unique_text_list(
        envelope["consequenceBearerIds"], "authorization.consequenceBearerIds"
    )
    payers = _unique_text_list(
        envelope["payerIds"], "authorization.payerIds", allow_empty=True
    )
    beneficiaries = _unique_text_list(
        envelope["beneficiaryIds"], "authorization.beneficiaryIds", allow_empty=True
    )
    _require(
        set(payers) <= set(bearers),
        "authorization payerIds must be covered by consequenceBearerIds",
    )
    _require(
        set(beneficiaries) <= set(bearers),
        "authorization beneficiaryIds must be covered by consequenceBearerIds",
    )
    deltas = envelope["expectedBearerDeltas"]
    _require(
        isinstance(deltas, dict), "authorization.expectedBearerDeltas must be an object"
    )
    _require(
        set(deltas) == set(bearers),
        "authorization expected deltas must cover every bearer exactly",
    )
    _require(
        all(
            isinstance(delta, (int, float))
            and not isinstance(delta, bool)
            and math.isfinite(float(delta))
            for delta in deltas.values()
        ),
        "authorization expected bearer deltas must be finite numbers",
    )

    signer_key_id = _text(envelope["signerKeyId"], "authorization.signerKeyId")
    signer = _trusted_record(
        policy,
        "authorizationSigners",
        signer_key_id,
        "authorization signer",
    )
    _require(
        envelope["principal"] in signer["principalIds"],
        "authorization signer is not trusted for the declared principal",
    )
    _verify_bip340(
        signer["publicKeyHex"],
        authorization_signature_digest(envelope),
        envelope["signature"],
        "authorization",
    )
    return envelope


def validate_run_request(
    value: Any,
    *,
    trust_policy: dict[str, Any] | None = None,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    request = _closed(value, RUN_REQUEST_KEYS, "runRequest")
    _require(request["schemaVersion"] == "1.0", "runRequest schemaVersion must be 1.0")
    for field in ("requestId", "task", "repository", "repositoryRef"):
        _text(request[field], f"runRequest.{field}")
    _require(
        isinstance(request["consequential"], bool),
        "runRequest.consequential must be boolean",
    )
    operations = _unique_text_list(request["operations"], "runRequest.operations")
    _require(
        set(operations) <= KNOWN_OPERATIONS, "runRequest contains unknown operations"
    )
    action_plan = _closed(
        request["actionPlan"], ACTION_PLAN_KEYS, "runRequest.actionPlan"
    )
    _require(
        action_plan["schemaVersion"] == "1.0", "actionPlan schemaVersion must be 1.0"
    )
    _text(action_plan["planId"], "runRequest.actionPlan.planId")
    _text(action_plan["summary"], "runRequest.actionPlan.summary")
    _require(
        action_plan["repository"] == request["repository"],
        "actionPlan repository mismatch",
    )
    _require(
        action_plan["repositoryRef"] == request["repositoryRef"],
        "actionPlan repositoryRef mismatch",
    )
    plan_operations = _unique_text_list(
        action_plan["operations"], "runRequest.actionPlan.operations"
    )
    _require(
        plan_operations == operations,
        "actionPlan operations must exactly match runRequest operations",
    )
    requested_paths = _canonical_repo_paths(
        action_plan["requestedPaths"],
        "runRequest.actionPlan.requestedPaths",
        allow_empty=True,
    )
    action_plan_sha256 = _text(
        request["actionPlanSha256"], "runRequest.actionPlanSha256"
    )
    _hex_bytes(action_plan_sha256, 32, "runRequest.actionPlanSha256")
    _require(
        action_plan_sha256 == sha256_value(action_plan),
        "runRequest actionPlan hash mismatch",
    )
    validate_budget(request["budget"])
    evaluation = _closed(
        request["evaluation"], {"contract", "blind", "rivals"}, "runRequest.evaluation"
    )
    _require(
        evaluation["contract"]
        == "blinded_budget_matched_against_flat_and_shorter_rivals",
        "runRequest evaluation contract mismatch",
    )
    _require(evaluation["blind"] is True, "runRequest evaluation must be blind")
    _unique_text_list(evaluation["rivals"], "runRequest.evaluation.rivals")

    mutating = bool(set(operations) & MUTATING_OPERATIONS)
    if mutating:
        _require(
            bool(requested_paths),
            "mutating runRequest requires explicit requestedPaths",
        )
    if request["consequential"] or mutating:
        _require(
            request["consequential"] is True,
            "mutating operations require a consequential runRequest",
        )
        _require(
            request["authorization"] is not None,
            "consequential runRequest requires authorization",
        )
        _require(
            trust_policy is not None,
            "consequential runRequest requires a local trust policy",
        )
        validate_authorization(
            request["authorization"],
            repository=request["repository"],
            operations=operations,
            requested_paths=requested_paths,
            action_plan_sha256=action_plan_sha256,
            trust_policy=trust_policy,
            now=now,
        )
        _require(
            request["authorization"]["scope"]["repositoryRef"]
            == request["repositoryRef"],
            "authorization repositoryRef mismatch",
        )
    else:
        _require(
            request["authorization"] is None,
            "nonconsequential runRequest must not carry mutation authority",
        )
    return request


def validate_deployment_receipt(
    value: Any,
    lock: dict[str, Any],
    *,
    trust_policy: dict[str, Any],
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "status",
        "bundleSha256",
        "environment",
        "agents",
        "topology",
        "verifiedAt",
        "verifier",
        "attestation",
    }
    receipt = _closed(value, keys, "deploymentReceipt")
    _require(
        receipt["schemaVersion"] == "1.0", "deploymentReceipt schemaVersion must be 1.0"
    )
    _require(
        receipt["status"] == "remote_verified",
        "deploymentReceipt is not remote_verified",
    )
    _require(
        receipt["bundleSha256"] == lock["bundleSha256"],
        "deploymentReceipt bundle hash mismatch",
    )
    policy = validate_trust_policy(trust_policy)
    current = _utc_now(now)
    verified_at = _parse_utc(receipt["verifiedAt"], "deploymentReceipt.verifiedAt")
    verifier_id = _text(receipt["verifier"], "deploymentReceipt.verifier")

    environment = _closed(
        receipt["environment"], {"id", "configSha256"}, "deploymentReceipt.environment"
    )
    _text(environment["id"], "deploymentReceipt.environment.id")
    _require(
        environment["configSha256"] == lock["environment"]["configSha256"],
        "deployment environment hash mismatch",
    )

    agents = receipt["agents"]
    _require(
        isinstance(agents, list) and len(agents) == 7,
        "deploymentReceipt needs exactly seven agents",
    )
    expected = {item["level"]: item for item in lock["agents"]}
    seen: set[str] = set()
    for index, agent in enumerate(agents):
        agent = _closed(
            agent,
            {"level", "id", "version", "configSha256"},
            f"deploymentReceipt.agents[{index}]",
        )
        level = agent["level"]
        _require(
            level in expected and level not in seen,
            f"invalid or duplicate deployed level: {level}",
        )
        seen.add(level)
        _text(agent["id"], f"deploymentReceipt.{level}.id")
        _require(
            isinstance(agent["version"], int) and agent["version"] > 0,
            f"deploymentReceipt.{level}.version must be positive",
        )
        _require(
            agent["configSha256"] == expected[level]["configSha256"],
            f"deploymentReceipt.{level} hash mismatch",
        )
    _require(seen == set(expected), "deploymentReceipt levels are incomplete")
    _require(
        receipt["topology"] == lock["topology"], "deploymentReceipt topology mismatch"
    )

    attestation = _closed(
        receipt["attestation"], ATTESTATION_KEYS, "deploymentReceipt.attestation"
    )
    key_id = _text(attestation["keyId"], "deploymentReceipt.attestation.keyId")
    signer = _trusted_record(
        policy,
        "deploymentVerifiers",
        key_id,
        "deployment verifier",
    )
    _require(
        verifier_id in signer["verifierIds"],
        "deployment verifier identity is not trusted for this key",
    )
    signed_at = _parse_utc(
        attestation["signedAt"], "deploymentReceipt.attestation.signedAt"
    )
    _require(
        verified_at <= signed_at + dt.timedelta(seconds=policy["maxFutureSkewSeconds"]),
        "deployment attestation predates the observed verification",
    )
    _require_fresh(
        verified_at,
        now=current,
        max_age_seconds=policy["maxDeploymentAgeSeconds"],
        max_future_skew_seconds=policy["maxFutureSkewSeconds"],
        label="deploymentReceipt.verifiedAt",
    )
    _require_fresh(
        signed_at,
        now=current,
        max_age_seconds=policy["maxDeploymentAgeSeconds"],
        max_future_skew_seconds=policy["maxFutureSkewSeconds"],
        label="deploymentReceipt.attestation.signedAt",
    )
    _verify_bip340(
        signer["publicKeyHex"],
        deployment_signature_digest(receipt),
        attestation["signature"],
        "deployment attestation",
    )
    return receipt


def validate_commitment_receipt(
    value: Any,
    *,
    request: dict[str, Any],
    deployment: dict[str, Any],
    trust_policy: dict[str, Any],
    expected_trust_policy_sha256: str,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "receiptType",
        "requestId",
        "actionId",
        "status",
        "authorizationAssessment",
        "actionPlanSha256",
        "budgetSha256",
        "deploymentSha256",
        "issuedBy",
        "attestation",
    }
    receipt = _closed(value, keys, "commitmentReceipt")
    _require(
        receipt["schemaVersion"] == "1.0", "commitmentReceipt schemaVersion must be 1.0"
    )
    _require(receipt["receiptType"] == "commitment", "commitmentReceipt type confusion")
    _require(
        receipt["requestId"] == request["requestId"],
        "commitmentReceipt request mismatch",
    )
    _require(
        receipt["status"]
        in {"refused", "authorization_pending", "attempt_started", "attempt_failed"},
        "commitmentReceipt status is invalid",
    )
    policy = validate_pinned_trust_policy(
        trust_policy, expected_trust_policy_sha256
    )
    current = _utc_now(now)
    issuer = _text(receipt["issuedBy"], "commitmentReceipt.issuedBy")
    attestation = _closed(
        receipt["attestation"], ATTESTATION_KEYS, "commitmentReceipt.attestation"
    )
    key_id = _text(attestation["keyId"], "commitmentReceipt.attestation.keyId")
    signer = _trusted_record(
        policy, "commitmentIssuers", key_id, "commitment receipt issuer"
    )
    _require(
        issuer in signer["issuerIds"],
        "commitmentReceipt issuer identity is not trusted for this key",
    )
    signed_at = _parse_utc(
        attestation["signedAt"], "commitmentReceipt.attestation.signedAt"
    )
    deployment_verified_at = _parse_utc(
        deployment["verifiedAt"], "deploymentReceipt.verifiedAt"
    )
    _require(
        deployment_verified_at
        <= signed_at + dt.timedelta(seconds=policy["maxFutureSkewSeconds"]),
        "commitment attestation predates the verified deployment",
    )
    _require_fresh(
        signed_at,
        now=current,
        max_age_seconds=policy["maxReceiptAgeSeconds"],
        max_future_skew_seconds=policy["maxFutureSkewSeconds"],
        label="commitmentReceipt.attestation.signedAt",
    )
    _verify_bip340(
        signer["publicKeyHex"],
        commitment_signature_digest(receipt),
        attestation["signature"],
        "commitmentReceipt attestation",
    )
    _require(
        receipt["actionPlanSha256"] == request["actionPlanSha256"],
        "commitmentReceipt actionPlan hash mismatch",
    )
    _require(
        receipt["budgetSha256"] == sha256_value(request["budget"]),
        "commitmentReceipt budget hash mismatch",
    )
    _require(
        receipt["deploymentSha256"] == sha256_value(deployment),
        "commitmentReceipt deployment hash mismatch",
    )
    assessment = _closed(
        receipt["authorizationAssessment"],
        {"status", "envelopeSha256", "reasons"},
        "commitmentReceipt.authorizationAssessment",
    )
    _require(
        assessment["status"]
        in {"valid", "invalid", "expired", "revoked", "out_of_scope"},
        "authorizationAssessment status is invalid",
    )
    _unique_text_list(
        assessment["reasons"], "authorizationAssessment.reasons", allow_empty=True
    )
    if request["authorization"] is None:
        _require(
            assessment["envelopeSha256"] is None,
            "authorizationAssessment cannot invent an envelope",
        )
    else:
        _require(
            assessment["envelopeSha256"] == sha256_value(request["authorization"]),
            "authorizationAssessment envelope hash mismatch",
        )
    if receipt["status"] == "attempt_started":
        _require(
            isinstance(receipt["actionId"], str) and bool(receipt["actionId"].strip()),
            "attempt_started needs an actionId",
        )
        _require(
            assessment["status"] == "valid",
            "attempt_started requires valid authorization assessment",
        )
    else:
        _require(
            receipt["actionId"] is None or isinstance(receipt["actionId"], str),
            "commitmentReceipt actionId has invalid type",
        )
    return receipt


def validate_outcome_receipt(
    value: Any,
    *,
    request: dict[str, Any],
    deployment: dict[str, Any] | None,
    commitment: dict[str, Any] | None,
    trust_policy: dict[str, Any],
    expected_trust_policy_sha256: str,
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "receiptType",
        "receiptCause",
        "requestId",
        "actionId",
        "actionPlanSha256",
        "status",
        "consequenceBearerIds",
        "observedBearerDeltas",
        "justiceAssessment",
        "classification",
        "issuedBy",
        "attestation",
    }
    receipt = _closed(value, keys, "outcomeReceipt")
    _require(
        receipt["schemaVersion"] == "1.0", "outcomeReceipt schemaVersion must be 1.0"
    )
    _require(receipt["receiptType"] == "outcome", "outcomeReceipt type confusion")
    _require(
        receipt["requestId"] == request["requestId"], "outcomeReceipt request mismatch"
    )
    _require(
        receipt["receiptCause"] in {"action_attempt", "ambient_observation"},
        "outcomeReceipt cause is invalid",
    )
    _require(
        receipt["status"] in {"observed", "partial", "unobservable", "pending"},
        "outcomeReceipt status is invalid",
    )
    _require(
        receipt["actionPlanSha256"] == request["actionPlanSha256"],
        "outcomeReceipt actionPlan hash mismatch",
    )
    policy = validate_pinned_trust_policy(
        trust_policy, expected_trust_policy_sha256
    )
    current = _utc_now(now)
    issuer = _text(receipt["issuedBy"], "outcomeReceipt.issuedBy")
    attestation = _closed(
        receipt["attestation"], ATTESTATION_KEYS, "outcomeReceipt.attestation"
    )
    key_id = _text(attestation["keyId"], "outcomeReceipt.attestation.keyId")
    signer = _trusted_record(
        policy, "outcomeIssuers", key_id, "world-outcome receipt issuer"
    )
    _require(
        issuer in signer["issuerIds"],
        "outcomeReceipt issuer identity is not trusted for this key",
    )
    signed_at = _parse_utc(
        attestation["signedAt"], "outcomeReceipt.attestation.signedAt"
    )
    _require_fresh(
        signed_at,
        now=current,
        max_age_seconds=policy["maxReceiptAgeSeconds"],
        max_future_skew_seconds=policy["maxFutureSkewSeconds"],
        label="outcomeReceipt.attestation.signedAt",
    )
    _verify_bip340(
        signer["publicKeyHex"],
        outcome_signature_digest(receipt),
        attestation["signature"],
        "outcomeReceipt attestation",
    )

    if receipt["receiptCause"] == "action_attempt":
        _require(
            deployment is not None,
            "action outcome requires the validated deployment used by the commitment",
        )
        _require(
            commitment is not None,
            "action outcome requires a commitmentReceipt",
        )
        validated_commitment = validate_commitment_receipt(
            commitment,
            request=request,
            deployment=deployment,
            trust_policy=policy,
            expected_trust_policy_sha256=expected_trust_policy_sha256,
            now=current,
        )
        commitment_signed_at = _parse_utc(
            validated_commitment["attestation"]["signedAt"],
            "commitmentReceipt.attestation.signedAt",
        )
        _require(
            commitment_signed_at
            <= signed_at + dt.timedelta(seconds=policy["maxFutureSkewSeconds"]),
            "outcome attestation predates the attempted commitment",
        )
        _require(
            validated_commitment["status"] == "attempt_started",
            "action outcome requires an attempted action",
        )
        _require(
            receipt["actionId"] == validated_commitment["actionId"],
            "outcomeReceipt action linkage mismatch",
        )
        _require(
            receipt["actionPlanSha256"] == validated_commitment["actionPlanSha256"],
            "outcomeReceipt actionPlan linkage mismatch",
        )
    else:
        _require(commitment is None, "ambient outcome cannot carry a commitmentReceipt")
        _require(deployment is None, "ambient outcome cannot claim an action deployment")
        _require(receipt["actionId"] is None, "ambient outcome must have null actionId")

    bearers = _unique_text_list(
        receipt["consequenceBearerIds"],
        "outcomeReceipt.consequenceBearerIds",
        allow_empty=True,
    )
    if request["authorization"] is not None:
        expected = set(request["authorization"]["consequenceBearerIds"])
        _require(set(bearers) == expected, "outcomeReceipt bearer coverage mismatch")
    deltas = receipt["observedBearerDeltas"]
    _require(
        isinstance(deltas, dict),
        "outcomeReceipt observedBearerDeltas must be an object",
    )
    _require(
        set(deltas) <= set(bearers), "outcomeReceipt observes an undeclared bearer"
    )
    _require(
        all(
            delta is None
            or (
                isinstance(delta, (int, float))
                and not isinstance(delta, bool)
                and math.isfinite(float(delta))
            )
            for delta in deltas.values()
        ),
        "outcomeReceipt deltas must be finite numbers or null",
    )
    if receipt["status"] == "observed":
        _require(
            set(deltas) == set(bearers), "observed outcome must cover every bearer"
        )
        _require(
            all(delta is not None for delta in deltas.values()),
            "observed outcome cannot contain null deltas",
        )
    if receipt["status"] in {"unobservable", "pending"}:
        _require(
            all(delta is None for delta in deltas.values()),
            "unobservable or pending outcome cannot invent deltas",
        )

    assessment = _closed(
        receipt["justiceAssessment"],
        JUSTICE_ASSESSMENT_KEYS,
        "outcomeReceipt.justiceAssessment",
    )
    _require(
        assessment["status"] in {"complete", "incomplete"},
        "justiceAssessment status is invalid",
    )
    _require(
        isinstance(assessment["bearerCoverageComplete"], bool),
        "justiceAssessment bearerCoverageComplete must be boolean",
    )
    focal_beneficiaries = _unique_text_list(
        assessment["focalBeneficiaryIds"],
        "justiceAssessment.focalBeneficiaryIds",
        allow_empty=True,
    )
    reasons = _unique_text_list(
        assessment["reasons"], "justiceAssessment.reasons", allow_empty=True
    )
    classification = _closed(
        receipt["classification"],
        OUTCOME_CLASSIFICATION_KEYS,
        "outcomeReceipt.classification",
    )
    _require(
        classification["status"] in {"classified", "unclassified"},
        "outcome classification status is invalid",
    )

    observation_complete = (
        receipt["status"] == "observed"
        and set(deltas) == set(bearers)
        and all(delta is not None for delta in deltas.values())
    )
    assessment_complete = assessment["status"] == "complete"
    may_classify = (
        receipt["receiptCause"] == "action_attempt"
        and observation_complete
        and assessment_complete
        and assessment["bearerCoverageComplete"] is True
    )
    classification_fields = (
        "demonBearing",
        "godBearing",
        "preservativeStasis",
        "strictSyntropy",
    )
    if not may_classify:
        _require(
            classification["status"] == "unclassified",
            "incomplete outcome must remain unclassified",
        )
        _require(
            all(classification[field] is None for field in classification_fields),
            "unclassified outcome cannot assert Justice consequence classes",
        )
        _require(
            assessment["status"] == "incomplete",
            "non-classifiable outcome cannot claim complete Justice assessment",
        )
        _require(
            assessment["justiceSatisfied"] is None,
            "incomplete Justice assessment cannot assert satisfaction",
        )
        _require(bool(reasons), "incomplete Justice assessment requires reasons")
    else:
        _require(
            classification["status"] == "classified",
            "complete outcome requires typed classification",
        )
        _require(
            isinstance(assessment["justiceSatisfied"], bool),
            "complete Justice assessment needs a boolean verdict",
        )
        focal_individual = _text(
            assessment["focalIndividualId"], "justiceAssessment.focalIndividualId"
        )
        declared_whole = _text(
            assessment["declaredWholeId"], "justiceAssessment.declaredWholeId"
        )
        _require(
            focal_individual != declared_whole,
            "Justice focal individual and declared whole must be distinct",
        )
        _require(
            {focal_individual, declared_whole} <= set(bearers),
            "Justice focal dyad is absent from bearer set",
        )
        _require(
            bool(focal_beneficiaries),
            "complete Justice assessment requires focal beneficiaries",
        )
        _require(
            set(focal_beneficiaries) <= set(bearers),
            "Justice focal beneficiary is absent from bearer set",
        )
        if request["authorization"] is not None:
            _require(
                set(focal_beneficiaries)
                <= set(request["authorization"]["beneficiaryIds"]),
                "Justice focal beneficiaries exceed the authorized beneficiary set",
            )
        assessor = _text(assessment["assessedBy"], "justiceAssessment.assessedBy")
        _require(
            assessor in signer["issuerIds"],
            "Justice assessor is not a trusted world-outcome issuer",
        )
        numeric_deltas = {bearer: float(deltas[bearer]) for bearer in bearers}
        if assessment["justiceSatisfied"]:
            _require(
                all(delta >= 0 for delta in numeric_deltas.values()),
                "Justice cannot be satisfied while an affected bearer is negative",
            )
        expected = {
            "demonBearing": (
                any(numeric_deltas[bearer] > 0 for bearer in focal_beneficiaries)
                and any(delta < 0 for delta in numeric_deltas.values())
            ),
            "godBearing": (
                assessment["justiceSatisfied"]
                and all(delta >= 0 for delta in numeric_deltas.values())
                and any(delta > 0 for delta in numeric_deltas.values())
            ),
            "preservativeStasis": (
                assessment["justiceSatisfied"]
                and all(delta == 0 for delta in numeric_deltas.values())
            ),
            "strictSyntropy": (
                assessment["justiceSatisfied"]
                and numeric_deltas[focal_individual] > 0
                and numeric_deltas[declared_whole] > 0
                and all(delta >= 0 for delta in numeric_deltas.values())
            ),
        }
        for field, expected_value in expected.items():
            _require(
                classification[field] is expected_value,
                f"outcome classification {field} does not match the receipted predicate",
            )

    return receipt


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = _load_unique_json(path)
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        raise ContractError(f"cannot load {label}: {exc}") from exc
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _load_unique_json(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ContractError(f"duplicate JSON key: {key!r}")
            value[key] = item
        return value

    return json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )


def preflight(
    request_path: Path,
    deployment_path: Path,
    trust_policy_path: Path = TRUST_POLICY_PATH,
    expected_trust_policy_sha256: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    lock = validate_lock()
    trust_policy = load_trust_policy(trust_policy_path)
    _require(
        expected_trust_policy_sha256 is not None,
        "preflight requires an expected trust-policy SHA-256",
    )
    trust_policy = validate_pinned_trust_policy(
        trust_policy, expected_trust_policy_sha256
    )
    request = validate_run_request(
        load_json(request_path, "run request"),
        trust_policy=trust_policy,
    )
    deployment = validate_deployment_receipt(
        load_json(deployment_path, "deployment receipt"),
        lock,
        trust_policy=trust_policy,
    )
    return lock, request, deployment, trust_policy


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write-lock",
        action="store_true",
        help="atomically regenerate agentz.lock.json",
    )
    args = parser.parse_args()
    try:
        if args.write_lock:
            write_lock()
            print(f"LOCK-WRITTEN {LOCK_PATH.name} bundle={load_lock()['bundleSha256']}")
        else:
            lock = validate_lock()
            print(
                f"CONTRACT-OK agents=7 bundle={lock['bundleSha256']} status=unprovisioned_x0"
            )
    except ContractError as exc:
        print(f"CONTRACT-ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
