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
import datetime as dt
import hashlib
import importlib.util
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any

import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AGENTS_DIR = HERE / "agents"
ENV_PATH = HERE / "emergentism.environment.yaml"
SCHEMA_PATH = HERE / "managed_agentz.schema.json"
LOCK_PATH = HERE / "agentz.lock.json"
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
    "principal",
    "mandate",
    "scope",
    "consent",
    "custody",
    "expiresAt",
    "revoked",
    "contestPath",
    "actor",
    "consequenceBearerIds",
    "payerIds",
    "beneficiaryIds",
    "expectedBearerDeltas",
}
RUN_REQUEST_KEYS = {
    "schemaVersion",
    "requestId",
    "task",
    "consequential",
    "operations",
    "repository",
    "repositoryRef",
    "budget",
    "evaluation",
    "authorization",
}


class ContractError(ValueError):
    """Stable local contract failure."""


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: yaml.Loader, node: yaml.Node, deep: bool = False) -> dict:
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
    _require(isinstance(value, str) and bool(value.strip()), f"{label} must be nonempty text")
    return value


def _unique_text_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    _require(isinstance(value, list), f"{label} must be a list")
    if not allow_empty:
        _require(bool(value), f"{label} must be nonempty")
    _require(all(isinstance(item, str) and item.strip() == item and item for item in value), f"{label} must contain nonempty text")
    _require(len(value) == len(set(value)), f"{label} must be unique")
    return value


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise ContractError(f"cannot load {path}: {exc}") from exc
    _require(isinstance(value, dict), f"{path} YAML root must be an object")
    return value


def _load_rosetta_validator():
    spec = importlib.util.spec_from_file_location("validate_agentz_rosetta_runtime", VALIDATOR_PATH)
    _require(spec is not None and spec.loader is not None, "cannot load Agentz Rosetta validator")
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
    _require(isinstance(spec["metadata"], dict), "environment.metadata must be an object")
    return {
        "name": _text(spec["name"], "environment.name"),
        "description": str(spec.get("description", "")),
        "config": spec["config"],
        "metadata": {str(key): str(value) for key, value in sorted(spec["metadata"].items())},
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
        _require(payload["name"] not in names, f"duplicate agent name: {payload['name']}")
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
    _require(levels == {f"L{index}" for index in range(1, 8)}, f"levels are incomplete: {sorted(levels)}")
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
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load lock {path}: {exc}") from exc
    _require(isinstance(value, dict), "agentz lock must be an object")
    return value


def validate_lock(path: Path = LOCK_PATH) -> dict[str, Any]:
    current = build_lock()
    stored = load_lock(path)
    _require(stored == current, "agentz.lock.json is stale; regenerate it from the validated bundle")
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
        _require(isinstance(item, int) and not isinstance(item, bool), f"budget.{key} must be an integer")
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
    now: dt.datetime | None = None,
) -> dict[str, Any]:
    envelope = _closed(value, AUTHORIZATION_KEYS, "authorization")
    _require(envelope["schemaVersion"] == "1.0", "authorization schemaVersion must be 1.0")
    for field in ("envelopeId", "principal", "mandate", "custody", "contestPath", "actor"):
        _text(envelope[field], f"authorization.{field}")
    _require(envelope["revoked"] is False, "authorization is revoked")
    current = now or dt.datetime.now(dt.timezone.utc)
    _require(_parse_utc(envelope["expiresAt"], "authorization.expiresAt") > current, "authorization is expired")

    scope = _closed(
        envelope["scope"],
        {"repository", "repositoryRef", "allowedPaths", "allowedOperations"},
        "authorization.scope",
    )
    _require(scope["repository"] == repository, "authorization repository mismatch")
    _text(scope["repositoryRef"], "authorization.scope.repositoryRef")
    _unique_text_list(scope["allowedPaths"], "authorization.scope.allowedPaths")
    allowed = set(_unique_text_list(scope["allowedOperations"], "authorization.scope.allowedOperations"))
    _require(allowed <= KNOWN_OPERATIONS, "authorization contains unknown operations")
    _require(set(operations) <= allowed, "requested operations exceed authorization scope")

    consent = _closed(envelope["consent"], {"status", "grantedBy", "grantedAt"}, "authorization.consent")
    _require(consent["status"] == "granted", "authorization consent is not granted")
    _text(consent["grantedBy"], "authorization.consent.grantedBy")
    _parse_utc(consent["grantedAt"], "authorization.consent.grantedAt")

    bearers = _unique_text_list(envelope["consequenceBearerIds"], "authorization.consequenceBearerIds")
    payers = _unique_text_list(envelope["payerIds"], "authorization.payerIds", allow_empty=True)
    beneficiaries = _unique_text_list(envelope["beneficiaryIds"], "authorization.beneficiaryIds", allow_empty=True)
    _require(set(payers) <= set(bearers), "authorization payerIds must be covered by consequenceBearerIds")
    _require(set(beneficiaries) <= set(bearers), "authorization beneficiaryIds must be covered by consequenceBearerIds")
    deltas = envelope["expectedBearerDeltas"]
    _require(isinstance(deltas, dict), "authorization.expectedBearerDeltas must be an object")
    _require(set(deltas) == set(bearers), "authorization expected deltas must cover every bearer exactly")
    _require(
        all(isinstance(delta, (int, float)) and not isinstance(delta, bool) and math.isfinite(float(delta)) for delta in deltas.values()),
        "authorization expected bearer deltas must be finite numbers",
    )
    return envelope


def validate_run_request(value: Any, *, now: dt.datetime | None = None) -> dict[str, Any]:
    request = _closed(value, RUN_REQUEST_KEYS, "runRequest")
    _require(request["schemaVersion"] == "1.0", "runRequest schemaVersion must be 1.0")
    for field in ("requestId", "task", "repository", "repositoryRef"):
        _text(request[field], f"runRequest.{field}")
    _require(isinstance(request["consequential"], bool), "runRequest.consequential must be boolean")
    operations = _unique_text_list(request["operations"], "runRequest.operations")
    _require(set(operations) <= KNOWN_OPERATIONS, "runRequest contains unknown operations")
    validate_budget(request["budget"])
    evaluation = _closed(request["evaluation"], {"contract", "blind", "rivals"}, "runRequest.evaluation")
    _require(
        evaluation["contract"] == "blinded_budget_matched_against_flat_and_shorter_rivals",
        "runRequest evaluation contract mismatch",
    )
    _require(evaluation["blind"] is True, "runRequest evaluation must be blind")
    _unique_text_list(evaluation["rivals"], "runRequest.evaluation.rivals")

    mutating = bool(set(operations) & MUTATING_OPERATIONS)
    if request["consequential"] or mutating:
        _require(request["consequential"] is True, "mutating operations require a consequential runRequest")
        _require(request["authorization"] is not None, "consequential runRequest requires authorization")
        validate_authorization(
            request["authorization"],
            repository=request["repository"],
            operations=operations,
            now=now,
        )
        _require(
            request["authorization"]["scope"]["repositoryRef"] == request["repositoryRef"],
            "authorization repositoryRef mismatch",
        )
    else:
        _require(request["authorization"] is None, "nonconsequential runRequest must not carry mutation authority")
    return request


def validate_deployment_receipt(value: Any, lock: dict[str, Any]) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "status",
        "bundleSha256",
        "environment",
        "agents",
        "topology",
        "verifiedAt",
        "verifier",
    }
    receipt = _closed(value, keys, "deploymentReceipt")
    _require(receipt["schemaVersion"] == "1.0", "deploymentReceipt schemaVersion must be 1.0")
    _require(receipt["status"] == "remote_verified", "deploymentReceipt is not remote_verified")
    _require(receipt["bundleSha256"] == lock["bundleSha256"], "deploymentReceipt bundle hash mismatch")
    _parse_utc(receipt["verifiedAt"], "deploymentReceipt.verifiedAt")
    _text(receipt["verifier"], "deploymentReceipt.verifier")

    environment = _closed(receipt["environment"], {"id", "configSha256"}, "deploymentReceipt.environment")
    _text(environment["id"], "deploymentReceipt.environment.id")
    _require(environment["configSha256"] == lock["environment"]["configSha256"], "deployment environment hash mismatch")

    agents = receipt["agents"]
    _require(isinstance(agents, list) and len(agents) == 7, "deploymentReceipt needs exactly seven agents")
    expected = {item["level"]: item for item in lock["agents"]}
    seen: set[str] = set()
    for index, agent in enumerate(agents):
        agent = _closed(agent, {"level", "id", "version", "configSha256"}, f"deploymentReceipt.agents[{index}]")
        level = agent["level"]
        _require(level in expected and level not in seen, f"invalid or duplicate deployed level: {level}")
        seen.add(level)
        _text(agent["id"], f"deploymentReceipt.{level}.id")
        _require(isinstance(agent["version"], int) and agent["version"] > 0, f"deploymentReceipt.{level}.version must be positive")
        _require(agent["configSha256"] == expected[level]["configSha256"], f"deploymentReceipt.{level} hash mismatch")
    _require(seen == set(expected), "deploymentReceipt levels are incomplete")
    _require(receipt["topology"] == lock["topology"], "deploymentReceipt topology mismatch")
    return receipt


def validate_commitment_receipt(
    value: Any,
    *,
    request: dict[str, Any],
    deployment: dict[str, Any],
    trusted_issuers: set[str],
) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "receiptType",
        "requestId",
        "actionId",
        "status",
        "authorizationAssessment",
        "budgetSha256",
        "deploymentSha256",
        "issuedBy",
    }
    receipt = _closed(value, keys, "commitmentReceipt")
    _require(receipt["schemaVersion"] == "1.0", "commitmentReceipt schemaVersion must be 1.0")
    _require(receipt["receiptType"] == "commitment", "commitmentReceipt type confusion")
    _require(receipt["requestId"] == request["requestId"], "commitmentReceipt request mismatch")
    _require(
        receipt["status"] in {"refused", "authorization_pending", "attempt_started", "attempt_failed"},
        "commitmentReceipt status is invalid",
    )
    issuer = _text(receipt["issuedBy"], "commitmentReceipt.issuedBy")
    _require(issuer in trusted_issuers, "commitmentReceipt issuer is not trusted")
    _require(receipt["budgetSha256"] == sha256_value(request["budget"]), "commitmentReceipt budget hash mismatch")
    _require(receipt["deploymentSha256"] == sha256_value(deployment), "commitmentReceipt deployment hash mismatch")
    assessment = _closed(
        receipt["authorizationAssessment"],
        {"status", "envelopeSha256", "reasons"},
        "commitmentReceipt.authorizationAssessment",
    )
    _require(
        assessment["status"] in {"valid", "invalid", "expired", "revoked", "out_of_scope"},
        "authorizationAssessment status is invalid",
    )
    _unique_text_list(assessment["reasons"], "authorizationAssessment.reasons", allow_empty=True)
    if request["authorization"] is None:
        _require(assessment["envelopeSha256"] is None, "authorizationAssessment cannot invent an envelope")
    else:
        _require(
            assessment["envelopeSha256"] == sha256_value(request["authorization"]),
            "authorizationAssessment envelope hash mismatch",
        )
    if receipt["status"] == "attempt_started":
        _require(isinstance(receipt["actionId"], str) and bool(receipt["actionId"].strip()), "attempt_started needs an actionId")
        _require(assessment["status"] == "valid", "attempt_started requires valid authorization assessment")
    else:
        _require(receipt["actionId"] is None or isinstance(receipt["actionId"], str), "commitmentReceipt actionId has invalid type")
    return receipt


def validate_outcome_receipt(
    value: Any,
    *,
    request: dict[str, Any],
    commitment: dict[str, Any] | None,
    trusted_issuers: set[str],
) -> dict[str, Any]:
    keys = {
        "schemaVersion",
        "receiptType",
        "receiptCause",
        "requestId",
        "actionId",
        "status",
        "consequenceBearerIds",
        "observedBearerDeltas",
        "issuedBy",
    }
    receipt = _closed(value, keys, "outcomeReceipt")
    _require(receipt["schemaVersion"] == "1.0", "outcomeReceipt schemaVersion must be 1.0")
    _require(receipt["receiptType"] == "outcome", "outcomeReceipt type confusion")
    _require(receipt["requestId"] == request["requestId"], "outcomeReceipt request mismatch")
    _require(receipt["receiptCause"] in {"action_attempt", "ambient_observation"}, "outcomeReceipt cause is invalid")
    _require(receipt["status"] in {"observed", "partial", "unobservable", "pending"}, "outcomeReceipt status is invalid")
    issuer = _text(receipt["issuedBy"], "outcomeReceipt.issuedBy")
    _require(issuer in trusted_issuers, "outcomeReceipt issuer is not trusted")

    bearers = _unique_text_list(receipt["consequenceBearerIds"], "outcomeReceipt.consequenceBearerIds", allow_empty=True)
    if request["authorization"] is not None:
        expected = set(request["authorization"]["consequenceBearerIds"])
        _require(set(bearers) == expected, "outcomeReceipt bearer coverage mismatch")
    deltas = receipt["observedBearerDeltas"]
    _require(isinstance(deltas, dict), "outcomeReceipt observedBearerDeltas must be an object")
    _require(set(deltas) <= set(bearers), "outcomeReceipt observes an undeclared bearer")
    _require(
        all(delta is None or (isinstance(delta, (int, float)) and not isinstance(delta, bool) and math.isfinite(float(delta))) for delta in deltas.values()),
        "outcomeReceipt deltas must be finite numbers or null",
    )
    if receipt["status"] == "observed":
        _require(set(deltas) == set(bearers), "observed outcome must cover every bearer")
        _require(all(delta is not None for delta in deltas.values()), "observed outcome cannot contain null deltas")
    if receipt["status"] in {"unobservable", "pending"}:
        _require(all(delta is None for delta in deltas.values()), "unobservable or pending outcome cannot invent deltas")

    if receipt["receiptCause"] == "action_attempt":
        _require(commitment is not None, "action outcome requires a commitmentReceipt")
        _require(commitment["status"] == "attempt_started", "action outcome requires an attempted action")
        _require(receipt["actionId"] == commitment["actionId"], "outcomeReceipt action linkage mismatch")
    else:
        _require(receipt["actionId"] is None, "ambient outcome must have null actionId")
    return receipt


def load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot load {label}: {exc}") from exc
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def preflight(request_path: Path, deployment_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    lock = validate_lock()
    request = validate_run_request(load_json(request_path, "run request"))
    deployment = validate_deployment_receipt(load_json(deployment_path, "deployment receipt"), lock)
    return lock, request, deployment


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-lock", action="store_true", help="atomically regenerate agentz.lock.json")
    args = parser.parse_args()
    try:
        if args.write_lock:
            write_lock()
            print(f"LOCK-WRITTEN {LOCK_PATH.name} bundle={load_lock()['bundleSha256']}")
        else:
            lock = validate_lock()
            print(f"CONTRACT-OK agents=7 bundle={lock['bundleSha256']} status=unprovisioned_x0")
    except ContractError as exc:
        print(f"CONTRACT-ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
