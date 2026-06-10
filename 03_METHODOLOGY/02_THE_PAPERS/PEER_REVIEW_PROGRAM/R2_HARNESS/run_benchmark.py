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

Design notes:
- No sampling parameters are sent (temperature/top_p are removed on Opus 4.7+;
  omitting them keeps one code path across all subject models). Determinism is
  approached through scenario count, not sampling control — note this in the paper.
- The scripted user never adapts to the model's replies; all conditions face
  byte-identical pressure.
"""

import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODELS = ["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"]
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
        messages.append({"role": "assistant", "content": text})
        transcript.append({"user": user_turn, "assistant": text})
    return transcript


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default=",".join(DEFAULT_MODELS))
    ap.add_argument("--conditions", default="C0,C1,C2,C3,C4,C5")
    ap.add_argument("--scenarios", default=os.path.join(HERE, "scenarios.json"))
    ap.add_argument("--conditions-file", default=os.path.join(HERE, "conditions.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "transcripts.jsonl"))
    ap.add_argument("--limit", type=int, default=0, help="cap adversarial scenarios (0 = all)")
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.scenarios) as f:
        battery = json.load(f)
    with open(args.conditions_file) as f:
        all_conditions = json.load(f)

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    cond_ids = [c.strip() for c in args.conditions.split(",") if c.strip()]
    adversarial = battery["adversarial"][: args.limit or None]
    controls = [] if args.no_controls else battery["controls"]

    n_runs = len(models) * len(cond_ids) * (len(adversarial) + len(controls))
    n_calls = len(models) * len(cond_ids) * (
        sum(len(s["turns"]) for s in adversarial) + len(controls))
    print(f"models={models}")
    print(f"conditions={cond_ids}")
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
                    out.write(json.dumps({
                        "run_started": stamp, "model": model,
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
                    out.write(json.dumps({
                        "run_started": stamp, "model": model,
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
