#!/usr/bin/env python3
"""Offline-only CLI for PQA-54 v0.1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from pqa_core import (
    PROMPT_ARMS,
    build_freeze_manifest,
    build_public_projection,
    check_freeze_manifest,
    generate_dev_fixture,
    load_json,
    score_trial,
    sha256_value,
    validate_atlas,
    validate_document,
    validate_fixture,
    validate_trial,
    write_json,
)


HERE = Path(__file__).resolve().parent
ATLAS = HERE / "prompts" / "questions.json"
FIXTURE = HERE / "fixtures" / "dev" / "pqa54_dev.json"
TRIAL = HERE / "recorded_responses" / "pqa54_dev.json"
SCORE = HERE / "recorded_responses" / "pqa54_score.json"
PROJECTION = HERE / "public_projection.json"
FREEZE = HERE / "FREEZE_MANIFEST.json"


def fail(label: str, errors: list[str]) -> int:
    print(f"{label}: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    return 2


def command_validate(args: argparse.Namespace) -> int:
    atlas = load_json(ATLAS)
    value = load_json(args.input)
    schema_id, errors = validate_document(value, atlas)
    if errors:
        return fail(f"VALIDATE {schema_id}", errors)
    print(f"VALIDATE {schema_id}: PASS")
    return 0


def command_generate(args: argparse.Namespace) -> int:
    atlas = load_json(ATLAS)
    errors = validate_atlas(atlas)
    if errors:
        return fail("GENERATE", errors)
    expected = generate_dev_fixture(atlas)
    if args.check:
        if load_json(FIXTURE) != expected:
            return fail("GENERATE", ["development fixture drift"])
        print(f"GENERATE: PASS sha256={sha256_value(expected)}")
        return 0
    write_json(FIXTURE, expected)
    print(f"GENERATE: WROTE {FIXTURE}")
    return 0


def command_run(args: argparse.Namespace) -> int:
    if not args.dry_run:
        return fail("RUN", ["network/live execution is refused by the PQA-54 reference harness"])
    if args.arm not in PROMPT_ARMS:
        return fail("RUN", [f"unknown arm: {args.arm}"])
    atlas = load_json(ATLAS)
    fixture = load_json(FIXTURE)
    trial = load_json(TRIAL)
    errors = validate_atlas(atlas) + validate_fixture(fixture, atlas) + validate_trial(trial)
    if errors:
        return fail("RUN", errors)
    envelope = {
        "schema_id": "PQARunEnvelope.v1",
        "run_id": f"offline-recorded:{args.arm.lower()}",
        "run_class": "OFFLINE_DRY_RUN",
        "requested_model_id": None,
        "resolved_model_id": "recorded-response",
        "prompt_arm": args.arm,
        "tools": [],
        "memory": {"enabled": False},
        "budgets": {"cost_limit_usd": 0.0},
        "network": {"allowed": False},
        "authorization_ref": "",
        "fixture_hash": sha256_value(fixture),
    }
    print(json.dumps({"envelope": envelope, "trial_hash": sha256_value(trial), "result_state": "MACHINE_VALIDATED"}, sort_keys=True))
    return 0


def command_score(args: argparse.Namespace) -> int:
    trial = load_json(TRIAL)
    expected = score_trial(trial)
    if args.check:
        if load_json(SCORE) != expected:
            return fail("SCORE", ["recorded score drift"])
        print("SCORE: PASS vector-only; synthetic fixture; no native review quorum")
        return 0
    write_json(SCORE, expected)
    print(f"SCORE: WROTE {SCORE}")
    return 0


def command_project(args: argparse.Namespace) -> int:
    atlas = load_json(ATLAS)
    expected = build_public_projection(atlas)
    if args.check:
        if load_json(PROJECTION) != expected:
            return fail("PROJECT", ["public projection drift"])
        print("PROJECT: PASS 54 selected / 0 evaluated / 0 reviewed / 0 resolved")
        return 0
    write_json(PROJECTION, expected)
    print(f"PROJECT: WROTE {PROJECTION}")
    return 0


def command_freeze(args: argparse.Namespace) -> int:
    expected = build_freeze_manifest(HERE)
    if args.check:
        errors = check_freeze_manifest(HERE, load_json(FREEZE))
        if errors:
            return fail("FREEZE", errors)
        print(f"FREEZE: PASS files={len(expected['files'])}")
        return 0
    write_json(FREEZE, expected)
    print(f"FREEZE: WROTE {FREEZE}")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("input")
    validate.set_defaults(func=command_validate)
    generate = commands.add_parser("generate")
    generate.add_argument("--check", action="store_true")
    generate.set_defaults(func=command_generate)
    run = commands.add_parser("run")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--arm", default="NEUTRAL", choices=sorted(PROMPT_ARMS))
    run.set_defaults(func=command_run)
    score = commands.add_parser("score")
    score.add_argument("--check", action="store_true")
    score.set_defaults(func=command_score)
    project = commands.add_parser("project")
    project.add_argument("--check", action="store_true")
    project.set_defaults(func=command_project)
    freeze = commands.add_parser("freeze")
    freeze.add_argument("--check", action="store_true")
    freeze.set_defaults(func=command_freeze)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return fail(args.command.upper(), [str(exc)])


if __name__ == "__main__":
    raise SystemExit(main())
