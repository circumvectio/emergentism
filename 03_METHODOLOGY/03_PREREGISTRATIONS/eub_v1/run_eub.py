#!/usr/bin/env python3
"""Command-line interface for the offline-first EUB-1 v1.0 harness."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import uuid

from adapters import (
    AdapterError,
    AnthropicMessagesAdapter,
    AuthorizationRequired,
    BudgetRefused,
    conservative_prompt_token_bound,
    configured_credential_values,
    contains_credential_material,
    CredentialMaterialDetected,
    NetworkPolicy,
    NetworkRefused,
    OpenAICompatibleAdapter,
    RecordedResponseAdapter,
)
from eub_core import (
    PROMPT_ARMS,
    SITTING_ORDER,
    build_recorded_trial,
    build_freeze_manifest,
    check_freeze_manifest,
    generate_fixture,
    load_json,
    invalid_run_receipt,
    score_dasein_trial,
    score_serial_force_response,
    serial_force_fixture,
    sha256_value,
    validate_document,
    validate_dasein_account,
    validate_fixture_bundle,
    validate_receipt,
    validate_run_bundle,
    validate_run_envelope,
    validate_trial_prefix,
    write_json,
)


HERE = Path(__file__).resolve().parent
DEFAULT_FIXTURE = HERE / "fixtures" / "dev" / "dasein_chain_seed_1701.json"
DEFAULT_RECORDED = HERE / "recorded_responses" / "dasein_account_dev.json"
DEFAULT_CONDITIONS = HERE / "prompts" / "conditions.json"


def _print_errors(prefix: str, errors: list[str]) -> int:
    print(f"{prefix}: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 2


def _write_json_exclusive(path: str | Path, value: object) -> None:
    """Publish a complete result once; never replace an earlier receipt."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.pending-",
        dir=target.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = -1
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary_name, target)
        directory_descriptor = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def _output_path_available(path: str | Path) -> bool:
    return not Path(path).exists() and not Path(path).is_symlink()


def _write_result_or_refuse(path: str | Path, value: object, label: str) -> int | None:
    try:
        _write_json_exclusive(path, value)
    except FileExistsError:
        return _print_errors(label, [f"output path already exists and was preserved: {path}"])
    return None


def command_validate(args: argparse.Namespace) -> int:
    try:
        value = load_json(args.input)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return _print_errors("VALIDATE", [str(exc)])
    if args.kind == "fixture":
        kind, errors = "FixtureBundle.v1", validate_fixture_bundle(value)
    elif args.kind == "receipt":
        kind, errors = "EUBRunReceipt.v2", validate_receipt(value)
    elif args.kind == "run-envelope":
        kind, errors = "RunEnvelope.v1", validate_run_envelope(value)
    elif args.kind == "run-bundle":
        kind, errors = "EUBRunBundle.v1", validate_run_bundle(value)
    else:
        kind, errors = validate_document(value)
    if errors:
        return _print_errors(f"VALIDATE {kind}", errors)
    print(f"VALIDATE {kind}: PASS")
    return 0


def command_generate(args: argparse.Namespace) -> int:
    if not _output_path_available(args.out):
        return _print_errors("GENERATE", [f"output path already exists and was preserved: {args.out}"])
    if args.kind == "serial-force":
        fixture = serial_force_fixture()
        errors: list[str] = []
    else:
        fixture = generate_fixture(args.seed)
        errors = validate_fixture_bundle(fixture)
        if errors:
            return _print_errors("GENERATE", errors)
    refused = _write_result_or_refuse(args.out, fixture, "GENERATE")
    if refused is not None:
        return refused
    print(f"GENERATE: PASS kind={args.kind} seed={args.seed} sha256={sha256_value(fixture)} out={args.out}")
    return 0


def _conditions() -> tuple[str, dict[str, dict[str, str]]]:
    raw = load_json(DEFAULT_CONDITIONS)
    return raw["shared_instruction"], {item["condition_id"]: item for item in raw["conditions"]}


def _make_envelope(args: argparse.Namespace, resolved_model: str | None, run_id: str) -> dict[str, object]:
    offline = bool(args.dry_run)
    return {
        "schema_id": "RunEnvelope.v1",
        "run_id": run_id,
        "run_class": "OFFLINE_DRY_RUN" if args.dry_run else args.run_class,
        "requested_model_id": args.model,
        "resolved_model_id": resolved_model,
        "adapter": "recorded" if args.dry_run else args.adapter,
        "runtime": {"python": sys.version.split()[0], "harness": "EUB-1-v1.0"},
        "prompt_arm": args.condition,
        "tools": [],
        "memory": {"enabled": False, "description": "no external memory in reference run"},
        "budgets": {
            "max_input_tokens": args.max_input_tokens,
            "max_output_tokens": args.max_output_tokens,
            "cost_limit_usd": args.cost_limit_usd,
            "input_cost_per_million_usd": 0.0 if offline else args.input_cost_per_million_usd,
            "output_cost_per_million_usd": 0.0 if offline else args.output_cost_per_million_usd,
            "cost_basis_ref": "OFFLINE_NO_PROVIDER_COST" if offline else args.cost_basis_ref,
        },
        "network": {"allowed": bool(args.allow_network and not args.dry_run), "endpoint_class": "OFFLINE" if args.dry_run else args.adapter},
        "authorization_ref": "" if args.dry_run else args.authorization_ref,
    }


def _sitting_packet(fixture: dict[str, object], sitting: str) -> object:
    if sitting == "UNFOLD":
        return fixture["public_view"]["initial_packet"]
    truth = fixture.get("hidden_truth")
    if not isinstance(truth, dict):
        raise RuntimeError("custodied sitting packets are unavailable")
    return truth["packets"][sitting]


def _make_prompt(shared: str, arm: dict[str, str], fixture: dict[str, object], sitting: str, run_id: str, previous: dict[str, object] | None) -> str:
    payload = {
        "run_id": run_id,
        "sitting_id": sitting,
        "packet": _sitting_packet(fixture, sitting),
        "previous_public_snapshot": previous,
    }
    return (
        shared
        + "\n\nCondition insert:\n"
        + arm["instruction"]
        + "\n\nSitting packet:\n"
        + json.dumps(
            payload,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
        )
    )


def _safe_failure_state(error: Exception) -> str:
    if isinstance(error, NetworkRefused):
        return "NETWORK_REFUSED"
    if isinstance(error, AuthorizationRequired):
        return "AUTH_REQUIRED"
    if isinstance(error, BudgetRefused):
        return "BUDGET_REFUSED"
    return "ABORTED"


def _secret_free(value: object, credential_values: tuple[str, ...] = ()) -> bool:
    serialized = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    )
    return not contains_credential_material(serialized, credential_values)


def _redact_credential_strings(
    value: object,
    credential_values: tuple[str, ...],
) -> object:
    """Replace every credential-bearing string before any public hash."""

    if isinstance(value, str):
        return (
            "WITHHELD_CREDENTIAL_MATCH"
            if contains_credential_material(value, credential_values)
            else value
        )
    if isinstance(value, list):
        return [_redact_credential_strings(row, credential_values) for row in value]
    if isinstance(value, dict):
        return {
            str(_redact_credential_strings(key, credential_values)):
            _redact_credential_strings(row, credential_values)
            for key, row in value.items()
        }
    return value


def _empty_usage() -> dict[str, object]:
    return {
        "input_tokens": 0,
        "output_tokens": 0,
        "estimated_cost_usd": 0.0,
        "reserved_cost_usd": 0.0,
        "calls": [],
    }


def _append_usage_call(
    usage: dict[str, object],
    *,
    sitting: str,
    status: str,
    max_input_tokens: int,
    max_output_tokens: int,
    reserved_cost_usd: float,
    input_tokens: int | None,
    output_tokens: int | None,
    estimated_cost_usd: float | None,
) -> None:
    calls = usage.setdefault("calls", [])
    if not isinstance(calls, list):
        raise ValueError("usage.calls must be a list")
    calls.append({
        "call_index": len(calls) + 1,
        "sitting_id": sitting,
        "status": status,
        "reserved_input_tokens": max_input_tokens,
        "reserved_output_tokens": max_output_tokens,
        "reserved_cost_usd": round(float(reserved_cost_usd), 12),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_usd": (
            round(float(estimated_cost_usd), 12)
            if estimated_cost_usd is not None else None
        ),
    })
    usage["input_tokens"] = sum(
        int(row["input_tokens"] or 0) for row in calls if isinstance(row, dict)
    )
    usage["output_tokens"] = sum(
        int(row["output_tokens"] or 0) for row in calls if isinstance(row, dict)
    )
    usage["estimated_cost_usd"] = round(sum(
        float(row["estimated_cost_usd"] or 0.0)
        for row in calls if isinstance(row, dict)
    ), 12)
    usage["reserved_cost_usd"] = round(sum(
        float(row["reserved_cost_usd"] or 0.0)
        for row in calls if isinstance(row, dict)
    ), 12)


def _strict_json_loads(value: str) -> object:
    return json.loads(
        value,
        parse_constant=lambda constant: (_ for _ in ()).throw(
            ValueError(f"non-finite JSON constant is forbidden: {constant}")
        ),
    )


def _sha256_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _completed_sitting_rows(
    snapshots: list[dict[str, object]],
    prompt_hashes: dict[str, str],
    raw_hashes: dict[str, str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for sitting, account in zip(SITTING_ORDER, snapshots):
        if sitting not in prompt_hashes or sitting not in raw_hashes:
            break
        rows.append({
            "sitting_id": sitting,
            "prompt_hash": prompt_hashes[sitting],
            "raw_output_hash": raw_hashes[sitting],
            "public_account_hash": sha256_value(account),
            "public_account": account,
        })
    return rows


def _write_failed_run(
    args: argparse.Namespace,
    fixture: dict[str, object],
    run_id: str,
    envelope: dict[str, object],
    raw_hash: str,
    errors: list[str],
    state: str,
    raw_output: str | None = None,
    prompt_hashes: dict[str, str] | None = None,
    raw_hashes: dict[str, str] | None = None,
    snapshots: list[dict[str, object]] | None = None,
    usage: dict[str, object] | None = None,
    failed_sitting: str = "PRE_RUN",
    recorded_source_hash: str | None = None,
    credential_redacted: bool = False,
    prompt_redacted: bool = False,
) -> int:
    credential_values = tuple(getattr(args, "_credential_values", ()))
    safe_errors = list(errors)
    safe_raw_output = raw_output
    credential_redacted = credential_redacted or (
        raw_output is not None
        and not _secret_free(raw_output, credential_values)
    )
    provider_raw_sha256: str | None = None
    if credential_redacted:
        safe_raw_output = None
        safe_errors.append("credential-bearing output was withheld without hashing its bytes")
        descriptor = {
            "schema_id": "WithheldOutputCommitment.v1",
            "disposition": "WITHHELD_CREDENTIAL_MATCH",
            "run_id": run_id,
            "sitting_id": failed_sitting,
            "result_state": state,
        }
        public_output_hash = sha256_value(descriptor)
        disposition = "WITHHELD_CREDENTIAL_MATCH"
        commitment_kind = "REDACTION_DESCRIPTOR_SHA256"
    elif raw_output is not None:
        public_output_hash = hashlib.sha256(safe_raw_output.encode("utf-8")).hexdigest()
        if _sha256_digest(raw_hash):
            provider_raw_sha256 = raw_hash
        disposition = "PRESERVED"
        commitment_kind = "PRESERVED_TEXT_UTF8_SHA256"
    else:
        descriptor = {
            "schema_id": "WithheldOutputCommitment.v1",
            "disposition": "NO_PROVIDER_OUTPUT",
            "run_id": run_id,
            "sitting_id": failed_sitting,
            "result_state": state,
        }
        public_output_hash = sha256_value(descriptor)
        disposition = "NO_PROVIDER_OUTPUT"
        commitment_kind = "NO_OUTPUT_DESCRIPTOR_SHA256"

    public_prompt_hashes = dict(prompt_hashes or {})
    public_raw_hashes = dict(raw_hashes or {})
    completed = list(snapshots or [])
    if failed_sitting in SITTING_ORDER:
        public_raw_hashes[failed_sitting] = provider_raw_sha256 or public_output_hash
    if prompt_redacted:
        safe_errors.append("credential-bearing prompt was withheld without hashing its bytes")
        prompt_disposition = "WITHHELD_CREDENTIAL_MATCH"
        prompt_kind = "REDACTION_DESCRIPTOR_SHA256"
    elif failed_sitting in SITTING_ORDER and _sha256_digest(
        public_prompt_hashes.get(failed_sitting)
    ):
        prompt_disposition = "HASHED"
        prompt_kind = "PROMPT_UTF8_SHA256"
    else:
        prompt_disposition = "NO_PROMPT"
        prompt_kind = "NO_PROMPT_DESCRIPTOR_SHA256"
    if prompt_disposition == "HASHED":
        prompt_commitment = public_prompt_hashes[failed_sitting]
    else:
        prompt_descriptor = {
            "schema_id": "WithheldPromptCommitment.v1",
            "disposition": prompt_disposition,
            "run_id": run_id,
            "sitting_id": failed_sitting,
            "result_state": state,
        }
        prompt_commitment = sha256_value(prompt_descriptor)
        if failed_sitting in SITTING_ORDER:
            public_prompt_hashes[failed_sitting] = prompt_commitment
    snapshot_hashes = {
        sitting: sha256_value(account)
        for sitting, account in zip(SITTING_ORDER, completed)
    }
    aggregate_raw_hash = sha256_value({"raw_output_hashes": public_raw_hashes})
    failure_record = {
        "schema_id": "EUBRunFailure.v1",
        "sitting_id": failed_sitting,
        "result_state": state,
        "structured_errors": safe_errors,
        "prompt_disposition": prompt_disposition,
        "prompt_commitment_kind": prompt_kind,
        "prompt_commitment_sha256": prompt_commitment,
        "raw_output_disposition": disposition,
        "output_commitment_kind": commitment_kind,
        "output_commitment_sha256": public_output_hash,
        "provider_raw_sha256": provider_raw_sha256,
        "raw_output": safe_raw_output,
    }
    usage_record = usage if usage is not None else _empty_usage()
    receipt = invalid_run_receipt(
        run_id=run_id,
        fixture=fixture,
        run_envelope=envelope,
        raw_output_hash=aggregate_raw_hash,
        errors=safe_errors,
        result_state=state,
        account=completed[-1] if completed else None,
        sitting_output_hashes=public_raw_hashes,
        snapshot_hashes=snapshot_hashes,
        prompt_hashes=public_prompt_hashes,
        usage=usage_record,
        failure=failure_record,
    )
    bundle = {
        "run_envelope": envelope,
        "trial": {
            "sittings": _completed_sitting_rows(completed, public_prompt_hashes, public_raw_hashes),
            "recorded_source_hash": recorded_source_hash,
            "failure": failure_record,
        },
        "usage": usage_record,
        "receipt": receipt,
    }
    if not _secret_free(bundle, credential_values):
        return _print_errors("RUN", ["credential material reached the serializable failure path"])
    bundle_errors = validate_run_bundle(bundle)
    if bundle_errors:
        return _print_errors(
            "RUN",
            ["internal failure artifact did not validate", *bundle_errors],
        )
    refused = _write_result_or_refuse(args.out, bundle, "RUN")
    if refused is not None:
        return refused
    return _print_errors("RUN", [f"{state}; structured receipt written to {args.out}"])


def command_run(args: argparse.Namespace) -> int:
    if not _output_path_available(args.out):
        return _print_errors("RUN", [f"output path already exists and was preserved: {args.out}"])
    args._credential_values = configured_credential_values()
    requested_run_id = args.run_id or f"eub-{uuid.uuid4()}"
    preflight_material = {
        "run_id": requested_run_id,
        "requested_model_id": args.model,
        "adapter": args.adapter,
        "base_url": args.base_url,
        "run_class": args.run_class,
        "authorization_ref": args.authorization_ref,
        "cost_basis_ref": args.cost_basis_ref,
        "condition": args.condition,
    }
    if not _secret_free(preflight_material, args._credential_values):
        safe_run_id = "eub-contaminated-input"
        envelope = _redact_credential_strings(
            _make_envelope(args, "WITHHELD_CREDENTIAL_MATCH", safe_run_id),
            args._credential_values,
        )
        return _write_failed_run(
            args,
            {},
            safe_run_id,
            envelope if isinstance(envelope, dict) else {},
            sha256_value({"failure": "credential-bearing-request-metadata"}),
            ["request metadata contained credential material and was withheld"],
            "CONTAMINATED",
            usage=_empty_usage(),
            failed_sitting="PRE_RUN",
            prompt_redacted=True,
        )
    shared, conditions = _conditions()
    if args.condition not in conditions:
        return _print_errors("RUN", [f"unknown condition: {args.condition}"])
    try:
        fixture = load_json(args.fixture)
    except (OSError, ValueError, json.JSONDecodeError):
        return _print_errors("RUN", ["fixture is missing or malformed"])
    fixture_errors = validate_fixture_bundle(fixture)
    if fixture_errors:
        return _print_errors("RUN", fixture_errors)
    run_id = requested_run_id
    prompt_inputs = {
        "fixture": fixture,
        "shared_instruction": shared,
        "condition": conditions[args.condition],
    }
    if not _secret_free(prompt_inputs, args._credential_values):
        envelope = _make_envelope(args, "UNRESOLVED_REDACTED", run_id)
        return _write_failed_run(
            args,
            {},
            run_id,
            envelope,
            sha256_value({"failure": "credential-bearing-prompt-input"}),
            ["fixture or condition text contained credential material and was withheld"],
            "CONTAMINATED",
            usage=_empty_usage(),
            failed_sitting="PRE_RUN",
            prompt_redacted=True,
        )
    policy = NetworkPolicy(
        args.allow_network,
        args.run_class,
        args.authorization_ref,
        args.cost_limit_usd,
        args.input_cost_per_million_usd,
        args.output_cost_per_million_usd,
        args.cost_basis_ref,
    )
    prompts: dict[str, str] = {}
    prompt_hashes: dict[str, str] = {}
    raw_hashes: dict[str, str] = {}
    snapshots: list[dict[str, object]] = []
    usage = _empty_usage()

    if not args.dry_run and fixture.get("hidden_truth") is None:
        envelope = _make_envelope(args, "UNRESOLVED_NO_CALL", run_id)
        return _write_failed_run(
            args,
            fixture,
            run_id,
            envelope,
            sha256_value({"failure": "custody-unavailable-preflight"}),
            ["held-out custody interface is unavailable before the first call"],
            "CUSTODY_UNAVAILABLE",
            usage=usage,
            failed_sitting="PRE_RUN",
        )

    if args.dry_run:
        adapter = RecordedResponseAdapter(args.recorded_response)
    elif args.adapter == "anthropic":
        adapter = AnthropicMessagesAdapter()
    elif args.adapter == "openai-compatible":
        adapter = OpenAICompatibleAdapter(args.base_url, allow_keyless_local=args.allow_keyless_local)
    else:
        unresolved = _make_envelope(args, "UNRESOLVED_NO_CALL", run_id)
        return _write_failed_run(args, fixture, run_id, unresolved, sha256_value({"failure": "adapter"}), ["live runs require anthropic or openai-compatible adapter"], "NETWORK_REFUSED")

    if args.dry_run:
        first_prompt = _make_prompt(shared, conditions[args.condition], fixture, "UNFOLD", run_id, None)
        if contains_credential_material(first_prompt, args._credential_values):
            envelope = _make_envelope(args, args.model, run_id)
            return _write_failed_run(
                args,
                fixture,
                run_id,
                envelope,
                sha256_value({"failure": "credential-bearing-prompt"}),
                ["UNFOLD prompt contained credential material and was withheld"],
                "CONTAMINATED",
                usage=usage,
                failed_sitting="UNFOLD",
                prompt_redacted=True,
            )
        try:
            response = adapter.call(first_prompt, args.model, policy, args.max_output_tokens, args.max_input_tokens)
        except CredentialMaterialDetected:
            envelope = _make_envelope(args, args.model, run_id)
            return _write_failed_run(
                args, fixture, run_id, envelope, sha256_value({"failure": "credential-redaction"}),
                ["recorded response contained credential material"], "CONTAMINATED",
                prompt_hashes={"UNFOLD": sha256_value(first_prompt)}, usage=usage,
                failed_sitting="UNFOLD",
                credential_redacted=True,
            )
        except (OSError, AdapterError):
            envelope = _make_envelope(args, args.model, run_id)
            return _write_failed_run(
                args, fixture, run_id, envelope, sha256_value({"failure": "recorded-read"}),
                ["recorded response could not be read safely"], "ABORTED",
                prompt_hashes={"UNFOLD": sha256_value(first_prompt)}, usage=usage,
                failed_sitting="UNFOLD",
            )
        envelope = _make_envelope(args, response.resolved_model_id, run_id)
        try:
            base_account = _strict_json_loads(response.content)
        except (TypeError, ValueError, json.JSONDecodeError):
            return _write_failed_run(
                args, fixture, run_id, envelope, response.raw_response_hash,
                ["recorded/provider output is not valid JSON"], "INVALID_OUTPUT",
                raw_output=response.content,
                prompt_hashes={"UNFOLD": sha256_value(first_prompt)}, usage=usage,
                failed_sitting="UNFOLD", recorded_source_hash=response.raw_response_hash,
            )
        base_errors = validate_dasein_account(base_account)
        if base_errors:
            return _write_failed_run(
                args,
                fixture,
                run_id,
                envelope,
                response.raw_response_hash,
                ["recorded development account failed DaseinAccount.v1 validation", *base_errors],
                "INVALID_OUTPUT",
                raw_output=response.content,
                prompt_hashes={"UNFOLD": sha256_value(first_prompt)},
                usage=usage,
                failed_sitting="UNFOLD",
                recorded_source_hash=response.raw_response_hash,
            )
        try:
            staged_snapshots = build_recorded_trial(base_account, run_id)
        except (KeyError, TypeError, ValueError):
            return _write_failed_run(
                args,
                fixture,
                run_id,
                envelope,
                response.raw_response_hash,
                ["recorded development account does not satisfy the deterministic replay contract"],
                "INVALID_OUTPUT",
                raw_output=response.content,
                prompt_hashes={"UNFOLD": sha256_value(first_prompt)},
                usage=usage,
                failed_sitting="UNFOLD",
                recorded_source_hash=response.raw_response_hash,
            )
        snapshots = []
        previous = None
        for sitting, account in zip(SITTING_ORDER, staged_snapshots):
            prompt = _make_prompt(shared, conditions[args.condition], fixture, sitting, run_id, previous)
            if contains_credential_material(prompt, args._credential_values):
                return _write_failed_run(
                    args,
                    fixture,
                    run_id,
                    envelope,
                    sha256_value({"failure": "credential-bearing-prompt"}),
                    [f"{sitting} prompt contained credential material and was withheld"],
                    "CONTAMINATED",
                    prompt_hashes=prompt_hashes,
                    raw_hashes=raw_hashes,
                    snapshots=snapshots,
                    usage=usage,
                    failed_sitting=sitting,
                    recorded_source_hash=response.raw_response_hash,
                    prompt_redacted=True,
                )
            prompts[sitting] = prompt
            prompt_hashes[sitting] = sha256_value(prompt)
            if conservative_prompt_token_bound(prompt) > args.max_input_tokens:
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "input-budget"}),
                    [f"{sitting} prompt exceeds the declared input-token approximation"], "BUDGET_REFUSED",
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting, recorded_source_hash=response.raw_response_hash,
                )
            raw_hashes[sitting] = sha256_value(account)
            snapshots.append(account)
            previous = account
        recorded_source_hash = response.raw_response_hash
    else:
        resolved_model: str | None = None
        previous = None
        recorded_source_hash = None
        for sitting in SITTING_ORDER:
            try:
                prompt = _make_prompt(shared, conditions[args.condition], fixture, sitting, run_id, previous)
            except RuntimeError:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_NO_CALL", run_id)
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "custody"}),
                    ["custodied reveal packet unavailable"], "CUSTODY_UNAVAILABLE",
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting,
                )
            if contains_credential_material(prompt, args._credential_values):
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_REDACTED", run_id)
                return _write_failed_run(
                    args,
                    fixture,
                    run_id,
                    envelope,
                    sha256_value({"failure": "credential-bearing-prompt"}),
                    [f"{sitting} prompt contained credential material and was withheld"],
                    "CONTAMINATED",
                    prompt_hashes=prompt_hashes,
                    raw_hashes=raw_hashes,
                    snapshots=snapshots,
                    usage=usage,
                    failed_sitting=sitting,
                    prompt_redacted=True,
                )
            prompts[sitting] = prompt
            prompt_hashes[sitting] = sha256_value(prompt)
            if conservative_prompt_token_bound(prompt) > args.max_input_tokens:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_NO_CALL", run_id)
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "input-budget"}),
                    [f"{sitting} prompt exceeds the declared input-token approximation"], "BUDGET_REFUSED",
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting,
                )
            reserved_before = policy.reserved_cost_usd
            try:
                response = adapter.call(prompt, args.model, policy, args.max_output_tokens, args.max_input_tokens)
            except CredentialMaterialDetected:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_REDACTED", run_id)
                reservation_delta = policy.reserved_cost_usd - reserved_before
                if reservation_delta > 0:
                    _append_usage_call(
                        usage,
                        sitting=sitting,
                        status="FAILED_AFTER_RESERVATION",
                        max_input_tokens=args.max_input_tokens,
                        max_output_tokens=args.max_output_tokens,
                        reserved_cost_usd=reservation_delta,
                        input_tokens=None,
                        output_tokens=None,
                        estimated_cost_usd=None,
                    )
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "credential-redaction"}),
                    ["provider response contained credential material"], "CONTAMINATED",
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting, credential_redacted=True,
                )
            except AdapterError as error:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_NO_CALL", run_id)
                reservation_delta = policy.reserved_cost_usd - reserved_before
                if reservation_delta > 0:
                    _append_usage_call(
                        usage,
                        sitting=sitting,
                        status="FAILED_AFTER_RESERVATION",
                        max_input_tokens=args.max_input_tokens,
                        max_output_tokens=args.max_output_tokens,
                        reserved_cost_usd=reservation_delta,
                        input_tokens=None,
                        output_tokens=None,
                        estimated_cost_usd=None,
                    )
                raw_output = getattr(error, "safe_raw_output", None)
                raw_output_hash = getattr(error, "safe_raw_response_hash", None)
                result_state = getattr(error, "result_state", None) or _safe_failure_state(error)
                return _write_failed_run(
                    args, fixture, run_id, envelope,
                    raw_output_hash or sha256_value({"failure": type(error).__name__}),
                    ["adapter boundary refused or aborted the call"], result_state,
                    raw_output=raw_output,
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting,
                )
            except OSError:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_TRANSPORT", run_id)
                reservation_delta = policy.reserved_cost_usd - reserved_before
                if reservation_delta > 0:
                    _append_usage_call(
                        usage,
                        sitting=sitting,
                        status="FAILED_AFTER_RESERVATION",
                        max_input_tokens=args.max_input_tokens,
                        max_output_tokens=args.max_output_tokens,
                        reserved_cost_usd=reservation_delta,
                        input_tokens=None,
                        output_tokens=None,
                        estimated_cost_usd=None,
                    )
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "transport"}),
                    ["adapter transport failed"], "ABORTED", prompt_hashes=prompt_hashes,
                    raw_hashes=raw_hashes, snapshots=snapshots, usage=usage, failed_sitting=sitting,
                )
            if not _secret_free(response.content, args._credential_values):
                envelope = _make_envelope(args, response.resolved_model_id, run_id)
                reservation_delta = policy.reserved_cost_usd - reserved_before
                if reservation_delta > 0:
                    _append_usage_call(
                        usage,
                        sitting=sitting,
                        status="FAILED_AFTER_RESERVATION",
                        max_input_tokens=args.max_input_tokens,
                        max_output_tokens=args.max_output_tokens,
                        reserved_cost_usd=reservation_delta,
                        input_tokens=None,
                        output_tokens=None,
                        estimated_cost_usd=None,
                    )
                return _write_failed_run(
                    args, fixture, run_id, envelope, sha256_value({"failure": "credential-redaction"}),
                    ["provider response contained credential material"], "CONTAMINATED",
                    raw_output=response.content, prompt_hashes=prompt_hashes, raw_hashes=raw_hashes,
                    snapshots=snapshots, usage=usage, failed_sitting=sitting, credential_redacted=True,
                )
            raw_hashes[sitting] = response.raw_response_hash
            _append_usage_call(
                usage,
                sitting=sitting,
                status="COMPLETED",
                max_input_tokens=args.max_input_tokens,
                max_output_tokens=args.max_output_tokens,
                reserved_cost_usd=response.reserved_cost_usd,
                input_tokens=response.usage["input_tokens"],
                output_tokens=response.usage["output_tokens"],
                estimated_cost_usd=response.estimated_cost_usd,
            )
            if resolved_model is not None and response.resolved_model_id != resolved_model:
                envelope = _make_envelope(args, response.resolved_model_id, run_id)
                return _write_failed_run(
                    args, fixture, run_id, envelope, response.raw_response_hash,
                    ["resolved model ID changed across sittings"], "INVALID_RUN",
                    raw_output=response.raw_response_text if response.raw_response_text is not None else response.content,
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting,
                )
            resolved_model = response.resolved_model_id
            if response.usage["input_tokens"] > args.max_input_tokens or response.usage["output_tokens"] > args.max_output_tokens:
                envelope = _make_envelope(args, resolved_model, run_id)
                return _write_failed_run(
                    args,
                    fixture,
                    run_id,
                    envelope,
                    response.raw_response_hash,
                    [f"{sitting} provider usage exceeded the declared token budget"],
                    "BUDGET_REFUSED",
                    raw_output=response.raw_response_text if response.raw_response_text is not None else response.content,
                    prompt_hashes=prompt_hashes,
                    raw_hashes=raw_hashes,
                    snapshots=snapshots,
                    usage=usage,
                    failed_sitting=sitting,
                )
            try:
                account = _strict_json_loads(response.content)
            except (TypeError, ValueError, json.JSONDecodeError):
                envelope = _make_envelope(args, resolved_model, run_id)
                return _write_failed_run(
                    args, fixture, run_id, envelope, response.raw_response_hash,
                    [f"{sitting} output is not valid JSON"], "INVALID_OUTPUT",
                    raw_output=response.raw_response_text if response.raw_response_text is not None else response.content,
                    prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
                    usage=usage, failed_sitting=sitting,
                )
            prefix_errors = validate_trial_prefix([*snapshots, account])
            if prefix_errors:
                envelope = _make_envelope(args, resolved_model, run_id)
                return _write_failed_run(
                    args,
                    fixture,
                    run_id,
                    envelope,
                    response.raw_response_hash,
                    [f"{sitting} output failed the DaseinAccount.v1 trial-prefix contract", *prefix_errors],
                    "INVALID_OUTPUT",
                    raw_output=response.raw_response_text if response.raw_response_text is not None else response.content,
                    prompt_hashes=prompt_hashes,
                    raw_hashes=raw_hashes,
                    snapshots=snapshots,
                    usage=usage,
                    failed_sitting=sitting,
                )
            snapshots.append(account)
            previous = account
        envelope = _make_envelope(args, resolved_model, run_id)

    envelope_errors = validate_run_envelope(envelope)
    if envelope_errors:
        return _write_failed_run(
            args, fixture, run_id, envelope, sha256_value({"failure": "envelope"}), envelope_errors,
            "INVALID_RUN", prompt_hashes=prompt_hashes, raw_hashes=raw_hashes,
            snapshots=snapshots, usage=usage, failed_sitting="POST_RUN",
            recorded_source_hash=recorded_source_hash,
        )
    receipt = score_dasein_trial(snapshots, fixture, envelope, raw_output_hashes=raw_hashes, prompt_hashes=prompt_hashes)
    receipt["usage_hash"] = sha256_value(usage)
    receipt["failure_hash"] = sha256_value({})
    receipt["trial_transcript_hash"] = sha256_value({
        "snapshot_hashes": receipt["snapshot_hashes"],
        "raw_output_hashes": receipt["sitting_output_hashes"],
        "prompt_hashes": receipt["prompt_hashes"],
        "usage_hash": receipt["usage_hash"],
        "failure_hash": receipt["failure_hash"],
    })
    receipt_errors = validate_receipt(receipt)
    if receipt_errors:
        return _write_failed_run(
            args, fixture, run_id, envelope, receipt["raw_output_hash"],
            ["internal receipt validation failed", *receipt_errors], "INVALID_RUN",
            prompt_hashes=prompt_hashes, raw_hashes=raw_hashes, snapshots=snapshots,
            usage=usage, failed_sitting="POST_RUN", recorded_source_hash=recorded_source_hash,
        )
    bundle = {
        "run_envelope": envelope,
        "trial": {
            "sittings": [
                {
                    "sitting_id": sitting,
                    "prompt_hash": prompt_hashes[sitting],
                    "raw_output_hash": raw_hashes[sitting],
                    "public_account_hash": sha256_value(account),
                    "public_account": account,
                }
                for sitting, account in zip(SITTING_ORDER, snapshots)
            ],
            "recorded_source_hash": recorded_source_hash,
        },
        "usage": usage,
        "receipt": receipt,
    }
    if not _secret_free(bundle, args._credential_values):
        return _print_errors("RUN", ["credential material reached serializable output"])
    bundle_errors = validate_run_bundle(bundle)
    if bundle_errors:
        return _write_failed_run(
            args,
            fixture,
            run_id,
            envelope,
            receipt["raw_output_hash"],
            ["internal run bundle validation failed", *bundle_errors],
            "INVALID_RUN",
            prompt_hashes=prompt_hashes,
            raw_hashes=raw_hashes,
            snapshots=snapshots,
            usage=usage,
            failed_sitting="POST_RUN",
            recorded_source_hash=recorded_source_hash,
        )
    refused = _write_result_or_refuse(args.out, bundle, "RUN")
    if refused is not None:
        return refused
    print(f"RUN: PASS sittings=5 class={envelope['run_class']} resolved_model={envelope['resolved_model_id']} state={receipt['result_state']} out={args.out}")
    return 0


def command_score(args: argparse.Namespace) -> int:
    if not _output_path_available(args.out):
        return _print_errors("SCORE", [f"output path already exists and was preserved: {args.out}"])
    try:
        fixture = load_json(args.fixture)
        account = load_json(args.account)
    except (OSError, ValueError, json.JSONDecodeError):
        return _print_errors("SCORE", ["fixture or account is missing or malformed JSON"])
    if not isinstance(fixture, dict):
        return _print_errors("SCORE", ["fixture must be a JSON object"])
    if fixture.get("fixture_kind") == "SERIAL_FORCE_STRESS":
        if not isinstance(account, dict) or not isinstance(account.get("assignment_analyses"), list):
            return _print_errors("SCORE", ["serial-force response must contain assignment_analyses[]"])
        result = {"fixture_id": fixture["fixture_id"], "score_vector": score_serial_force_response(account, fixture)}
    else:
        fixture_errors = validate_fixture_bundle(fixture)
        if fixture_errors:
            return _print_errors("SCORE", fixture_errors)
        account_errors = validate_dasein_account(account)
        if account_errors:
            run_id = (
                account.get("causal_account", {}).get("run_id", "score-invalid")
                if isinstance(account, dict)
                else "score-invalid"
            )
            result = invalid_run_receipt(
                run_id=run_id,
                fixture=fixture,
                run_envelope=None,
                raw_output_hash=sha256_value(account),
                errors=account_errors,
                result_state="INVALID_OUTPUT",
                account=account if isinstance(account, dict) else None,
            )
        else:
            try:
                snapshots = build_recorded_trial(
                    account,
                    account.get("causal_account", {}).get("run_id", "score-replay"),
                )
            except (KeyError, TypeError, ValueError):
                result = invalid_run_receipt(
                    run_id=account.get("causal_account", {}).get("run_id", "score-invalid"),
                    fixture=fixture,
                    run_envelope=None,
                    raw_output_hash=sha256_value(account),
                    errors=["account does not satisfy the deterministic replay contract"],
                    result_state="INVALID_OUTPUT",
                    account=account,
                )
            else:
                prompt_hashes = {sitting: sha256_value({"score_replay": sitting}) for sitting in SITTING_ORDER}
                raw_hashes = {sitting: sha256_value(snapshot) for sitting, snapshot in zip(SITTING_ORDER, snapshots)}
                result = score_dasein_trial(snapshots, fixture, None, raw_output_hashes=raw_hashes, prompt_hashes=prompt_hashes)
    refused = _write_result_or_refuse(args.out, result, "SCORE")
    if refused is not None:
        return refused
    state = result.get("result_state")
    if state is not None and state != "SCORED_DEV":
        return _print_errors(
            "SCORE",
            [f"{state}; structured result written to {args.out}"],
        )
    print(f"SCORE: PASS state={state or 'STRESS_PROFILE'} out={args.out}")
    return 0


def command_freeze(args: argparse.Namespace) -> int:
    manifest_path = HERE / "FREEZE_MANIFEST.json"
    if not args.check:
        return _print_errors("FREEZE", ["freeze is check-only; choose --check"])
    errors = check_freeze_manifest(HERE, manifest_path)
    if errors:
        return _print_errors("FREEZE MANIFEST_DRIFT", errors)
    print("FREEZE: PASS (read-only; payload matches FREEZE_MANIFEST.json)")
    return 0


def _finite_nonnegative_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed) or parsed < 0:
        raise argparse.ArgumentTypeError("must be a finite non-negative number")
    return parsed


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="EUB-1 v1.0 offline-first harness")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate")
    validate.add_argument("--input", required=True)
    validate.add_argument("--kind", choices=("auto", "fixture", "receipt", "run-envelope", "run-bundle"), default="auto")
    validate.set_defaults(func=command_validate)

    generate = sub.add_parser("generate")
    generate.add_argument("--kind", choices=("dasein", "serial-force"), default="dasein")
    generate.add_argument("--seed", type=int, default=1701)
    generate.add_argument("--out", required=True)
    generate.set_defaults(func=command_generate)

    run = sub.add_parser("run")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--fixture", default=str(DEFAULT_FIXTURE))
    run.add_argument("--recorded-response", default=str(DEFAULT_RECORDED))
    run.add_argument("--condition", choices=sorted(PROMPT_ARMS), default="NEUTRAL")
    run.add_argument("--adapter", choices=("recorded", "anthropic", "openai-compatible"), default="recorded")
    run.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    run.add_argument("--allow-keyless-local", action="store_true")
    run.add_argument("--allow-network", action="store_true")
    run.add_argument("--run-class", default="UNAUTHORIZED")
    run.add_argument("--authorization-ref", default="")
    run.add_argument("--cost-limit-usd", type=_finite_nonnegative_float, default=0.0)
    run.add_argument("--input-cost-per-million-usd", type=_finite_nonnegative_float)
    run.add_argument("--output-cost-per-million-usd", type=_finite_nonnegative_float)
    run.add_argument("--cost-basis-ref", default="")
    run.add_argument("--max-input-tokens", type=_positive_integer, default=32768)
    run.add_argument("--max-output-tokens", type=_positive_integer, default=4096)
    run.add_argument("--model", default="recorded-dasein-v1")
    run.add_argument("--run-id")
    run.add_argument("--out", required=True)
    run.set_defaults(func=command_run)

    score = sub.add_parser("score")
    score.add_argument("--fixture", required=True)
    score.add_argument("--account", required=True)
    score.add_argument("--out", required=True)
    score.set_defaults(func=command_score)

    freeze = sub.add_parser("freeze")
    freeze.add_argument("--check", action="store_true")
    freeze.set_defaults(func=command_freeze)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
