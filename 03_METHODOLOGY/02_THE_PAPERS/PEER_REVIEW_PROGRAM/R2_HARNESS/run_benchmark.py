#!/usr/bin/env python3
"""
R2 harness — transcript collection.

Plays scripted-user escalation scenarios (and non-adversarial controls)
against subject models under each system-prompt condition, and writes one
JSONL record per (model, condition, scenario) transcript.

Usage:
  python3 run_benchmark.py --dry-run --limit 2          # smoke test, no API
  python3 run_benchmark.py                              # full run (needs ANTHROPIC_API_KEY)
  python3 run_benchmark.py --models claude-haiku-4-5 --conditions C0,C2 --limit 1   # pilot
  python3 run_benchmark.py --scenarios ALT.json --non-registered ...  # alternate input

Design notes:
- No sampling parameters are sent (temperature/top_p are removed on Opus 4.7+;
  omitting them keeps one code path across all subject models). Determinism is
  approached through scenario count, not sampling control — note this in the paper.
- The scripted user never adapts to the model's replies; all conditions face
  byte-identical pressure.
- The default scenario and condition files are frozen inputs. Their fixed
  SHA-256 values are verified before client construction or model calls, and
  both hashes are embedded in every transcript row.
"""

import argparse
import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODELS = ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"]
DEFAULT_CONDITION_IDS = ["C0", "C1", "C2", "C3", "C4", "C5"]
DEFAULT_SCENARIOS_FILE = os.path.join(HERE, "scenarios_40_candidate.json")
DEFAULT_CONDITIONS_FILE = os.path.join(HERE, "conditions.json")
FROZEN_SCENARIOS_SHA256 = "51fbdeb707e971ef4f360288617034e31d777da74ba2a71dc33716df23fced99"
FROZEN_CONDITIONS_SHA256 = "3396a5d7aa6d656e40ee6fb11c73bc29be3a601d610a3930f4ae2c42573193a7"
MAX_TOKENS_PER_TURN = 1024


class MockClient:
    """Offline stand-in for smoke tests: echoes a canned reply."""

    class _Msgs:
        def create(self, **kwargs):
            class Block:
                type = "text"
                text = ("[dry-run mock reply] (model=%s, system_len=%d, turns_seen=%d)"
                        % (kwargs.get("model"), len(kwargs.get("system") or ""),
                           len(kwargs.get("messages", []))))

            class Msg:
                content = [Block()]
                model = kwargs.get("model")
                class usage:
                    input_tokens = 0
                    output_tokens = 0
            return Msg()

    def __init__(self):
        self.messages = self._Msgs()


def make_client(dry_run):
    if dry_run:
        return MockClient()
    import anthropic
    return anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env


def reply_text(message):
    return "".join(b.text for b in message.content if getattr(b, "type", "") == "text")


def same_input_path(candidate, default):
    return os.path.realpath(os.path.abspath(candidate)) == os.path.realpath(default)


def verify_input_custody(scenarios_path, conditions_path):
    """Read each input once, hash those bytes, and reject canonical drift."""
    with open(scenarios_path, "rb") as fh:
        scenarios_raw = fh.read()
    with open(conditions_path, "rb") as fh:
        conditions_raw = fh.read()
    scenarios_hash = hashlib.sha256(scenarios_raw).hexdigest()
    conditions_hash = hashlib.sha256(conditions_raw).hexdigest()
    default_scenarios = same_input_path(scenarios_path, DEFAULT_SCENARIOS_FILE)
    default_conditions = same_input_path(conditions_path, DEFAULT_CONDITIONS_FILE)
    errors = []
    if default_scenarios and scenarios_hash != FROZEN_SCENARIOS_SHA256:
        errors.append(
            f"default scenarios hash drift: expected {FROZEN_SCENARIOS_SHA256}, "
            f"got {scenarios_hash}"
        )
    if default_conditions and conditions_hash != FROZEN_CONDITIONS_SHA256:
        errors.append(
            f"default conditions hash drift: expected {FROZEN_CONDITIONS_SHA256}, "
            f"got {conditions_hash}"
        )
    if errors:
        raise ValueError("R2 INPUT CUSTODY: FAIL\n- " + "\n- ".join(errors))
    provenance = {
        "input_mode": (
            "FROZEN_DEFAULTS" if default_scenarios and default_conditions
            else "NON_REGISTERED_ALTERNATE_INPUTS"
        ),
        "registered_inputs": default_scenarios and default_conditions,
        "scenarios_file": os.path.basename(scenarios_path),
        "scenarios_sha256": scenarios_hash,
        "conditions_file": os.path.basename(conditions_path),
        "conditions_sha256": conditions_hash,
    }
    return provenance, scenarios_raw, conditions_raw


def classify_run(args, models, cond_ids, input_provenance):
    if args.dry_run:
        return "NON_REGISTERED_DRY_RUN"
    if args.non_registered:
        return "NON_REGISTERED_EXPLICIT"
    if not input_provenance["registered_inputs"]:
        return "NON_REGISTERED_ALTERNATE_INPUTS"
    full_selection = (
        models == DEFAULT_MODELS
        and cond_ids == DEFAULT_CONDITION_IDS
        and args.limit == 0
        and not args.no_controls
    )
    return "REGISTERED_INPUTS_FULL_BATTERY" if full_selection else "NON_REGISTERED_PILOT"


def selected_workload(battery, all_conditions, models, cond_ids, limit, no_controls):
    """Validate the complete selected workload before client construction."""
    errors = []
    if limit < 0:
        errors.append("--limit must be zero or a positive integer")
    if not models:
        errors.append("at least one model must be selected")
    if len(models) != len(set(models)):
        errors.append("model selections must not contain duplicates")
    if not cond_ids:
        errors.append("at least one condition must be selected")
    if len(cond_ids) != len(set(cond_ids)):
        errors.append("condition selections must not contain duplicates")
    if type(all_conditions) is not dict:
        errors.append("conditions input must be a JSON object")
        all_conditions = {}
    for cid in cond_ids:
        condition = all_conditions.get(cid)
        if type(condition) is not dict:
            errors.append(f"condition {cid!r} is missing or not an object")
            continue
        if type(condition.get("label")) is not str or not condition["label"]:
            errors.append(f"condition {cid!r} requires a non-empty string label")
        if type(condition.get("system")) is not str:
            errors.append(f"condition {cid!r} requires a string system prompt")

    if type(battery) is not dict:
        errors.append("scenario battery must be a JSON object")
        battery = {}
    adversarial_all = battery.get("adversarial")
    controls_all = battery.get("controls")
    if type(adversarial_all) is not list:
        errors.append("scenario battery adversarial field must be a list")
        adversarial_all = []
    if type(controls_all) is not list:
        errors.append("scenario battery controls field must be a list")
        controls_all = []
    adversarial = adversarial_all[: limit or None] if limit >= 0 else []
    controls = [] if no_controls else controls_all

    seen_ids = set()
    for index, scenario in enumerate(adversarial):
        prefix = f"adversarial[{index}]"
        if type(scenario) is not dict:
            errors.append(f"{prefix} must be an object")
            continue
        scenario_id = scenario.get("id")
        if type(scenario_id) is not str or not scenario_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif scenario_id in seen_ids:
            errors.append(f"duplicate selected scenario id {scenario_id!r}")
        else:
            seen_ids.add(scenario_id)
        turns = scenario.get("turns")
        if type(turns) is not list or not turns or any(type(turn) is not str for turn in turns):
            errors.append(f"{prefix}.turns must be a non-empty list of strings")
        for field in ("domain", "target_claim", "plausible_core"):
            if type(scenario.get(field)) is not str:
                errors.append(f"{prefix}.{field} must be a string")
    for index, control in enumerate(controls):
        prefix = f"controls[{index}]"
        if type(control) is not dict:
            errors.append(f"{prefix} must be an object")
            continue
        control_id = control.get("id")
        if type(control_id) is not str or not control_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif control_id in seen_ids:
            errors.append(f"duplicate selected scenario id {control_id!r}")
        else:
            seen_ids.add(control_id)
        if type(control.get("prompt")) is not str:
            errors.append(f"{prefix}.prompt must be a string")
    if errors:
        raise ValueError("R2 WORKLOAD VALIDATION: FAIL\n- " + "\n- ".join(errors))
    return adversarial, controls


def play_scenario(client, model, system, user_turns):
    """Scripted-user multi-turn conversation; returns list of (user, assistant)."""
    messages = []
    transcript = []
    for user_turn in user_turns:
        messages.append({"role": "user", "content": user_turn})
        kwargs = dict(model=model, max_tokens=MAX_TOKENS_PER_TURN, messages=messages)
        if system:
            kwargs["system"] = system
        response = client.messages.create(**kwargs)
        text = reply_text(response)
        response_model = getattr(response, "model", None)
        if type(response_model) is not str or not response_model:
            raise RuntimeError("model response omitted the exact response.model identifier")
        messages.append({"role": "assistant", "content": text})
        transcript.append({
            "user": user_turn,
            "assistant": text,
            "response_model": response_model,
        })
    return transcript


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(DEFAULT_MODELS))
    ap.add_argument("--conditions", default="C0,C1,C2,C3,C4,C5")
    ap.add_argument(
        "--scenarios",
        default=DEFAULT_SCENARIOS_FILE,
        help="frozen scenario battery (the legacy scenarios.json is truncated)",
    )
    ap.add_argument("--conditions-file", default=DEFAULT_CONDITIONS_FILE)
    ap.add_argument("--out", default=os.path.join(HERE, "transcripts.jsonl"))
    ap.add_argument("--limit", type=int, default=0, help="cap adversarial scenarios (0 = all)")
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--non-registered",
        action="store_true",
        help="required for real model calls with alternate input files; marks every output row non-registered",
    )
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    cond_ids = [c.strip() for c in args.conditions.split(",") if c.strip()]
    try:
        input_provenance, scenarios_raw, conditions_raw = verify_input_custody(
            args.scenarios, args.conditions_file
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if (
        not input_provenance["registered_inputs"]
        and not args.dry_run
        and not args.non_registered
    ):
        print(
            "R2 INPUT CUSTODY: FAIL\n- alternate inputs require --non-registered "
            "before any real model calls",
            file=sys.stderr,
        )
        return 2
    run_class = classify_run(args, models, cond_ids, input_provenance)

    try:
        battery = json.loads(scenarios_raw)
        all_conditions = json.loads(conditions_raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"R2 INPUT CUSTODY: FAIL\n- could not load verified input JSON: {exc}", file=sys.stderr)
        return 2
    try:
        adversarial, controls = selected_workload(
            battery, all_conditions, models, cond_ids, args.limit, args.no_controls
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    run_provenance = {
        "run_class": run_class,
        "models_requested": models,
        "conditions_selected": cond_ids,
        "adversarial_limit": args.limit,
        "controls_included": not args.no_controls,
        "dry_run": args.dry_run,
        "non_registered_acknowledged": args.non_registered,
    }

    n_runs = len(models) * len(cond_ids) * (len(adversarial) + len(controls))
    n_calls = len(models) * len(cond_ids) * (
        sum(len(s["turns"]) for s in adversarial) + len(controls))
    print(f"models={models}")
    print(f"conditions={cond_ids}")
    print(f"run_class={run_class}")
    print(
        "input_hashes="
        f"scenarios:{input_provenance['scenarios_sha256']} "
        f"conditions:{input_provenance['conditions_sha256']}"
    )
    print(f"adversarial={len(adversarial)} controls={len(controls)} "
          f"-> {n_runs} transcripts, {n_calls} API calls"
          f"{' (DRY RUN)' if args.dry_run else ''}")

    client = make_client(args.dry_run)
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    written = 0
    with open(args.out, "a") as out:
        for model in models:
            for cid in cond_ids:
                cond = all_conditions[cid]
                for scen in adversarial:
                    transcript = play_scenario(client, model, cond["system"], scen["turns"])
                    response_models = sorted({turn["response_model"] for turn in transcript})
                    out.write(json.dumps({
                        "run_started": stamp, "model": model,
                        "requested_model": model,
                        "response_models": response_models,
                        "run_class": run_class,
                        "run_provenance": run_provenance,
                        "input_provenance": input_provenance,
                        "condition": cid, "condition_label": cond["label"],
                        "scenario_id": scen["id"], "scenario_type": "adversarial",
                        "domain": scen["domain"],
                        "target_claim": scen["target_claim"],
                        "plausible_core": scen["plausible_core"],
                        "turns": transcript,
                    }) + "\n")
                    out.flush()
                    written += 1
                    print(f"  [{written}/{n_runs}] {model} {cid} {scen['id']}")
                for ctrl in controls:
                    transcript = play_scenario(client, model, cond["system"], [ctrl["prompt"]])
                    response_models = sorted({turn["response_model"] for turn in transcript})
                    out.write(json.dumps({
                        "run_started": stamp, "model": model,
                        "requested_model": model,
                        "response_models": response_models,
                        "run_class": run_class,
                        "run_provenance": run_provenance,
                        "input_provenance": input_provenance,
                        "condition": cid, "condition_label": cond["label"],
                        "scenario_id": ctrl["id"], "scenario_type": "control",
                        "turns": transcript,
                    }) + "\n")
                    out.flush()
                    written += 1
                    print(f"  [{written}/{n_runs}] {model} {cid} {ctrl['id']}")
    print(f"wrote {written} transcripts -> {args.out}")


if __name__ == "__main__":
    sys.exit(main())
