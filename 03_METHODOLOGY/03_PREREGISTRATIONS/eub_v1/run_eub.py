#!/usr/bin/env python3
"""Command-line interface for the offline-first EUB-1 v1.0 harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import uuid

from adapters import (
    AdapterError,
    AnthropicMessagesAdapter,
    AuthorizationRequired,
    BudgetRefused,
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
    validate_fixture_bundle,
    validate_receipt,
    validate_run_bundle,
    validate_run_envelope,
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


def command_validate(args: argparse.Namespace) -> int:
    try:
        value = load_json(args.input)
    except (OSError, json.JSONDecodeError) as exc:
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
    if args.kind == "serial-force":
        fixture = serial_force_fixture()
        errors: list[str] = []
    else:
        fixture = generate_fixture(args.seed)
        errors = validate_fixture_bundle(fixture)
        if errors:
            return _print_errors("GENERATE", errors)
    write_json(args.out, fixture)
    print(f"GENERATE: PASS kind={args.kind} seed={args.seed} sha256={sha256_value(fixture)} out={args.out}")
    return 0


def _conditions() -> tuple[str, dict[str, dict[str, str]]]:
    raw = load_json(DEFAULT_CONDITIONS)
    return raw["shared_instruction"], {item["condition_id"]: item for item in raw["conditions"]}


def _make_envelope(args: argparse.Namespace, resolved_model: str | None, run_id: str) -> dict[str, object]:
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
        "budgets": {"max_input_tokens": args.max_input_tokens, "max_output_tokens": args.max_output_tokens, "cost_limit_usd": args.cost_limit_usd},
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
    return shared + "\n\nCondition insert:\n" + arm["instruction"] + "\n\nSitting packet:\n" + json.dumps(payload, sort_keys=True, ensure_ascii=False)


def _safe_failure_state(error: Exception) -> str:
    if isinstance(error, NetworkRefused):
        return "NETWORK_REFUSED"
    if isinstance(error, AuthorizationRequired):
        return "AUTH_REQUIRED"
    if isinstance(error, BudgetRefused):
        return "BUDGET_REFUSED"
    return "ABORTED"


def _secret_free(value: object) -> bool:
    serialized = json.dumps(value, sort_keys=True, ensure_ascii=False)
    environment = __import__("os").environ
    return all(not environment.get(name) or environment[name] not in serialized for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY"))


def _write_failed_run(args: argparse.Namespace, fixture: dict[str, object], run_id: str, envelope: dict[str, object], raw_hash: str, errors: list[str], state: str, raw_output: str | None = None, prompt_hashes: dict[str, str] | None = None) -> int:
    safe_errors = list(errors)
    safe_raw_output = raw_output
    if raw_output is not None and not _secret_free(raw_output):
        safe_raw_output = None
        safe_errors.append("raw output bytes are hash-bound but withheld because they matched credential material")
    receipt = invalid_run_receipt(
        run_id=run_id,
        fixture=fixture,
        run_envelope=envelope,
        raw_output_hash=raw_hash,
        errors=safe_errors,
        result_state=state,
        prompt_hashes=prompt_hashes,
    )
    bundle = {
        "run_envelope": envelope,
        "trial": {"sittings": [], "failure_state": state, "structured_errors": safe_errors},
        "raw_output": safe_raw_output,
        "receipt": receipt,
    }
    if not _secret_free(bundle):
        return _print_errors("RUN", ["credential material reached the serializable failure path"])
    write_json(args.out, bundle)
    return _print_errors("RUN", [f"{state}; structured receipt written to {args.out}"])


def command_run(args: argparse.Namespace) -> int:
    shared, conditions = _conditions()
    if args.condition not in conditions:
        return _print_errors("RUN", [f"unknown condition: {args.condition}"])
    try:
        fixture = load_json(args.fixture)
    except (OSError, json.JSONDecodeError):
        return _print_errors("RUN", ["fixture is missing or malformed"])
    fixture_errors = validate_fixture_bundle(fixture)
    if fixture_errors:
        return _print_errors("RUN", fixture_errors)
    run_id = args.run_id or f"eub-{uuid.uuid4()}"
    policy = NetworkPolicy(args.allow_network, args.run_class, args.authorization_ref, args.cost_limit_usd)
    prompts: dict[str, str] = {}
    prompt_hashes: dict[str, str] = {}
    raw_hashes: dict[str, str] = {}
    snapshots: list[dict[str, object]] = []
    usage = {"input_tokens": 0, "output_tokens": 0}

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
        try:
            response = adapter.call(first_prompt, args.model, policy, args.max_output_tokens)
        except (OSError, AdapterError):
            envelope = _make_envelope(args, args.model, run_id)
            return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": "recorded-read"}), ["recorded response could not be read safely"], "ABORTED")
        envelope = _make_envelope(args, response.resolved_model_id, run_id)
        try:
            base_account = json.loads(response.content)
        except json.JSONDecodeError:
            return _write_failed_run(args, fixture, run_id, envelope, response.raw_response_hash, ["recorded/provider output is not valid JSON"], "INVALID_OUTPUT", raw_output=response.content, prompt_hashes={"UNFOLD": sha256_value(first_prompt)})
        snapshots = build_recorded_trial(base_account, run_id)
        previous = None
        for sitting, account in zip(SITTING_ORDER, snapshots):
            prompt = _make_prompt(shared, conditions[args.condition], fixture, sitting, run_id, previous)
            if len(prompt.encode("utf-8")) > args.max_input_tokens * 4:
                return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": "input-budget"}), [f"{sitting} prompt exceeds the declared input-token approximation"], "BUDGET_REFUSED", prompt_hashes=prompt_hashes)
            prompts[sitting] = prompt
            prompt_hashes[sitting] = sha256_value(prompt)
            raw_hashes[sitting] = sha256_value(account)
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
                return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": "custody"}), ["custodied reveal packet unavailable"], "CUSTODY_UNAVAILABLE", prompt_hashes=prompt_hashes)
            if len(prompt.encode("utf-8")) > args.max_input_tokens * 4:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_NO_CALL", run_id)
                return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": "input-budget"}), [f"{sitting} prompt exceeds the declared input-token approximation"], "BUDGET_REFUSED", prompt_hashes=prompt_hashes)
            prompts[sitting] = prompt
            prompt_hashes[sitting] = sha256_value(prompt)
            try:
                response = adapter.call(prompt, args.model, policy, args.max_output_tokens)
            except AdapterError as error:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_NO_CALL", run_id)
                return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": type(error).__name__}), ["adapter boundary refused or aborted the call"], _safe_failure_state(error), prompt_hashes=prompt_hashes)
            except OSError:
                envelope = _make_envelope(args, resolved_model or "UNRESOLVED_TRANSPORT", run_id)
                return _write_failed_run(args, fixture, run_id, envelope, response.raw_response_hash if "response" in locals() else sha256_value({"failure": "transport"}), ["adapter transport failed"], "ABORTED", prompt_hashes=prompt_hashes)
            if resolved_model is not None and response.resolved_model_id != resolved_model:
                envelope = _make_envelope(args, response.resolved_model_id, run_id)
                return _write_failed_run(args, fixture, run_id, envelope, response.raw_response_hash, ["resolved model ID changed across sittings"], "INVALID_RUN", raw_output=response.content, prompt_hashes=prompt_hashes)
            resolved_model = response.resolved_model_id
            raw_hashes[sitting] = response.raw_response_hash
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
                    raw_output=response.content,
                    prompt_hashes=prompt_hashes,
                )
            usage["input_tokens"] += response.usage["input_tokens"]
            usage["output_tokens"] += response.usage["output_tokens"]
            try:
                account = json.loads(response.content)
            except json.JSONDecodeError:
                envelope = _make_envelope(args, resolved_model, run_id)
                return _write_failed_run(args, fixture, run_id, envelope, response.raw_response_hash, [f"{sitting} output is not valid JSON"], "INVALID_OUTPUT", raw_output=response.content, prompt_hashes=prompt_hashes)
            snapshots.append(account)
            previous = account
        envelope = _make_envelope(args, resolved_model, run_id)

    envelope_errors = validate_run_envelope(envelope)
    if envelope_errors:
        return _write_failed_run(args, fixture, run_id, envelope, sha256_value({"failure": "envelope"}), envelope_errors, "INVALID_RUN", prompt_hashes=prompt_hashes)
    receipt = score_dasein_trial(snapshots, fixture, envelope, raw_output_hashes=raw_hashes, prompt_hashes=prompt_hashes)
    receipt_errors = validate_receipt(receipt)
    if receipt_errors:
        return _write_failed_run(args, fixture, run_id, envelope, receipt["raw_output_hash"], ["internal receipt validation failed", *receipt_errors], "INVALID_RUN", prompt_hashes=prompt_hashes)
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
        "usage": response.usage,
        "receipt": receipt,
    }
    if not args.dry_run:
        bundle["usage"] = usage
    if not _secret_free(bundle):
        return _print_errors("RUN", ["credential material reached serializable output"])
    write_json(args.out, bundle)
    print(f"RUN: PASS sittings=5 class={envelope['run_class']} resolved_model={envelope['resolved_model_id']} state={receipt['result_state']} out={args.out}")
    return 0


def command_score(args: argparse.Namespace) -> int:
    fixture = load_json(args.fixture)
    account = load_json(args.account)
    if fixture.get("fixture_kind") == "SERIAL_FORCE_STRESS":
        result = {"fixture_id": fixture["fixture_id"], "score_vector": score_serial_force_response(account, fixture), "primary_scalar": None}
    else:
        snapshots = build_recorded_trial(account, account.get("causal_account", {}).get("run_id", "score-replay"))
        prompt_hashes = {sitting: sha256_value({"score_replay": sitting}) for sitting in SITTING_ORDER}
        raw_hashes = {sitting: sha256_value(snapshot) for sitting, snapshot in zip(SITTING_ORDER, snapshots)}
        result = score_dasein_trial(snapshots, fixture, None, raw_output_hashes=raw_hashes, prompt_hashes=prompt_hashes)
    write_json(args.out, result)
    print(f"SCORE: PASS state={result.get('result_state', 'STRESS_PROFILE')} out={args.out}")
    return 0


def command_freeze(args: argparse.Namespace) -> int:
    manifest_path = HERE / "FREEZE_MANIFEST.json"
    if args.write:
        if not args.acknowledge_review:
            return _print_errors("FREEZE", ["--write requires --acknowledge-review; automatic repinning is forbidden"])
        write_json(manifest_path, build_freeze_manifest(HERE))
        print(f"FREEZE: WROTE REVIEW CANDIDATE {manifest_path}")
        return 0
    if not args.check:
        return _print_errors("FREEZE", ["choose --check or the reviewed --write --acknowledge-review path"])
    errors = check_freeze_manifest(HERE, manifest_path)
    if errors:
        return _print_errors("FREEZE MANIFEST_DRIFT", errors)
    print("FREEZE: PASS (read-only; payload matches FREEZE_MANIFEST.json)")
    return 0


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
    run.add_argument("--cost-limit-usd", type=float, default=0.0)
    run.add_argument("--max-input-tokens", type=int, default=16384)
    run.add_argument("--max-output-tokens", type=int, default=4096)
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
    freeze.add_argument("--write", action="store_true")
    freeze.add_argument("--acknowledge-review", action="store_true")
    freeze.set_defaults(func=command_freeze)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
