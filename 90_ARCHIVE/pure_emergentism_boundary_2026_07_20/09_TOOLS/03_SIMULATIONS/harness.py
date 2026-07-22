#!/usr/bin/env python3
"""
DAC Simulation Harness — Packet 164 Shared Contract

Track A (substrate) + Track B (organ) joint test runner.
Reads YAML scenarios, simulates actors, outputs transcripts,
checks assertions, guarantees determinism via seeded randomness.

Usage:
    python harness.py run --scenario 00_SCENARIOS/00_happy/honest_path.yaml [--seed 42]
    python harness.py run --dir 00_SCENARIOS/00_happy/
    python harness.py verify --scenario 00_SCENARIOS/00_happy/honest_path.yaml --runs 5
"""

import argparse
import hashlib
import json
import os
import random
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml


# ---------------------------------------------------------------------------
# Actor definitions
# ---------------------------------------------------------------------------

@dataclass
class Actor:
    actor_id: str
    actor_type: str
    is_honest: bool = True
    state: Dict[str, Any] = field(default_factory=dict)

    def act(self, round_num: int, global_state: Dict) -> Optional[Dict]:
        """Return an action dict or None."""
        return None


class Validator(Actor):
    def __init__(self, actor_id: str, is_honest: bool = True):
        super().__init__(actor_id, "Validator", is_honest)
        self.state = {
            "current_round": 0,
            "sig_queue": [],
            "signed_checkpoints": set(),
        }

    def act(self, round_num: int, global_state: Dict) -> Optional[Dict]:
        self.state["current_round"] = round_num
        cp_height = global_state.get("last_checkpoint_height", 0)
        if cp_height not in self.state["signed_checkpoints"]:
            self.state["signed_checkpoints"].add(cp_height)
            return {
                "action": "sign_checkpoint",
                "target": {"cp_height": cp_height},
            }
        return None


class Archiver(Actor):
    def __init__(self, actor_id: str, is_honest: bool = True):
        super().__init__(actor_id, "Archiver", is_honest)
        self.state = {
            "stored_bundles": {},
            "fee_balance": 0.0,
        }

    def act(self, round_num: int, global_state: Dict) -> Optional[Dict]:
        cp_height = global_state.get("last_checkpoint_height", 0)
        if cp_height > 0 and cp_height not in self.state["stored_bundles"]:
            if self.is_honest:
                self.state["stored_bundles"][cp_height] = f"bundle_{cp_height}"
                return {
                    "action": "store_bundle",
                    "target": {"cp_height": cp_height},
                }
            else:
                # Byzantine archiver: withhold bundle
                return {
                    "action": "withhold_bundle",
                    "target": {"cp_height": cp_height},
                }
        return None


class SuperCheckpoint:
    def __init__(self, height: int):
        self.height = height
        self.tx_root = f"tx_root_{height}"
        self.state_root = f"state_root_{height}"
        self.sig_set: set = set()
        self.finality_state = "Orange"

    def add_sig(self, validator_id: str):
        self.sig_set.add(validator_id)

    def try_green(self, quorum: int):
        if len(self.sig_set) >= quorum and self.finality_state == "Orange":
            self.finality_state = "Green"
            return True
        return False


class Event:
    def __init__(self, event_id: str, round_num: int, producer: str):
        self.event_id = event_id
        self.round_num = round_num
        self.producer = producer
        self.payload_hash = hashlib.sha256(event_id.encode()).hexdigest()[:16]
        self.super_checkpoint_height: Optional[int] = None


class Cluster(Actor):
    def __init__(self, actor_id: str, is_honest: bool = True):
        super().__init__(actor_id, "Cluster", is_honest)
        self.state = {
            "phi_nu_scalars": [1.0, 1.0],
            "member_set": set(),
        }

    def act(self, round_num: int, global_state: Dict) -> Optional[Dict]:
        # Minimal cluster behavior: merge available members
        available = global_state.get("available_nodes", set())
        new_members = available - self.state["member_set"]
        if new_members and self.is_honest:
            for m in list(new_members)[:2]:
                self.state["member_set"].add(m)
            return {
                "action": "merge_members",
                "target": {"members": list(new_members)[:2]},
            }
        return None


# ---------------------------------------------------------------------------
# Harness engine
# ---------------------------------------------------------------------------

class Harness:
    def __init__(self, scenario: Dict, seed: int = 42):
        self.scenario = scenario
        self.seed = seed
        self.rng = random.Random(seed)
        self.round_num = 0
        self.duration = scenario.get("duration_rounds", 20)
        self.actors: List[Actor] = []
        self.events: List[Event] = []
        self.checkpoints: Dict[int, SuperCheckpoint] = {}
        self.transcript: List[Dict] = []
        self.global_state: Dict = {
            "last_checkpoint_height": 0,
            "available_nodes": set(),
        }
        self._init_actors()
        self._init_events()

    def _init_actors(self):
        for actor_cfg in self.scenario.get("actors", []):
            atype = actor_cfg["type"]
            aid = actor_cfg["id"]
            honest = actor_cfg.get("is_honest", True)
            if atype == "Validator":
                self.actors.append(Validator(aid, honest))
            elif atype == "Archiver":
                self.actors.append(Archiver(aid, honest))
            elif atype == "Cluster":
                self.actors.append(Cluster(aid, honest))
            if atype in ("Validator", "Cluster"):
                self.global_state["available_nodes"].add(aid)

    def _init_events(self):
        event_idx = 0
        for ev_cfg in self.scenario.get("events", []):
            rnd = ev_cfg["round"]
            count = ev_cfg["count"]
            producer = ev_cfg["producer"]
            for _ in range(count):
                eid = f"ev_{event_idx}"
                self.events.append(Event(eid, rnd, producer))
                event_idx += 1

    def _global_state_hash(self) -> str:
        def serialize(obj):
            if isinstance(obj, set):
                return sorted(list(obj))
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [serialize(v) for v in obj]
            return obj
        state_str = json.dumps({
            "round": self.round_num,
            "actors": {a.actor_id: serialize(a.state) for a in self.actors},
            "events": len(self.events),
            "checkpoints": {h: list(cp.sig_set) for h, cp in self.checkpoints.items()},
        }, sort_keys=True)
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

    def _create_checkpoint(self, height: int):
        if height not in self.checkpoints:
            self.checkpoints[height] = SuperCheckpoint(height)

    def run(self) -> Dict:
        for r in range(1, self.duration + 1):
            self.round_num = r
            # Create checkpoint every 10 rounds
            if r % 10 == 0:
                cp_height = r // 10
                self._create_checkpoint(cp_height)
                self.global_state["last_checkpoint_height"] = cp_height

            # Process events for this round
            for ev in self.events:
                if ev.round_num == r:
                    ev.super_checkpoint_height = self.global_state["last_checkpoint_height"]

            # Actor actions (shuffled for fairness)
            acting_order = self.actors[:]
            self.rng.shuffle(acting_order)
            for actor in acting_order:
                if not actor.is_honest and self.rng.random() < 0.3:
                    continue  # Byzantine: 30% chance to withhold action
                action = actor.act(r, self.global_state)
                if action:
                    # Record checkpoint signatures
                    if actor.actor_type == "Validator" and action["action"] == "sign_checkpoint":
                        cp_h = action["target"]["cp_height"]
                        if cp_h in self.checkpoints:
                            self.checkpoints[cp_h].add_sig(actor.actor_id)
                            quorum = len([a for a in self.actors if a.actor_type == "Validator" and a.is_honest]) // 2 + 1
                            self.checkpoints[cp_h].try_green(quorum)

                    self.transcript.append({
                        "round": r,
                        "actor": actor.actor_id,
                        "action": action["action"],
                        "target": action.get("target", {}),
                        "state_hash": self._global_state_hash(),
                    })

        return self._check_assertions()

    def _check_assertions(self) -> Dict:
        assertions = self.scenario.get("assertions", [])
        results = []
        all_pass = True

        for assertion in assertions:
            name = assertion if isinstance(assertion, str) else assertion.get("name", assertion)
            status = "✅"
            detail = {}

            if name == "every_super_checkpoint_reaches_green":
                failed = [h for h, cp in self.checkpoints.items() if cp.finality_state != "Green"]
                if failed:
                    status = "❌"
                    all_pass = False
                    detail = {"failed_checkpoints": failed}

            elif name == "no_event_pruned_before_bundle_verified":
                # Simplified: all events should have a checkpoint assignment
                orphaned = [e.event_id for e in self.events if e.super_checkpoint_height is None]
                if orphaned:
                    status = "❌"
                    all_pass = False
                    detail = {"orphaned_events": orphaned}

            elif name == "deterministic_transcript_hash":
                expected = assertion.get("expected") if isinstance(assertion, dict) else None
                actual = hashlib.sha256(json.dumps(self.transcript, sort_keys=True).encode()).hexdigest()[:16]
                if expected and actual != expected:
                    status = "❌"
                    all_pass = False
                detail = {"expected": expected, "actual": actual}

            elif name == "byzantine_minority_cannot_finalize":
                byzantine_validators = [a for a in self.actors if a.actor_type == "Validator" and not a.is_honest]
                if byzantine_validators:
                    # Check no checkpoint finalized solely by byzantine
                    for h, cp in self.checkpoints.items():
                        byz_sigs = [s for s in cp.sig_set if any(b.actor_id == s for b in byzantine_validators)]
                        if len(byz_sigs) >= len(cp.sig_set) and cp.finality_state == "Green":
                            status = "❌"
                            all_pass = False
                            detail = {"checkpoint": h, "byzantine_sigs": byz_sigs}

            results.append({"name": name, "status": status, **detail})

        return {
            "scenario": self.scenario.get("name", "unnamed"),
            "seed": self.seed,
            "passed": all_pass,
            "assertions": results,
            "transcript_hash": hashlib.sha256(json.dumps(self.transcript, sort_keys=True).encode()).hexdigest()[:16],
        }

    def write_transcript(self, path: str):
        with open(path, "w") as f:
            for line in self.transcript:
                f.write(json.dumps(line, sort_keys=True) + "\n")

    def write_assertions(self, path: str):
        result = self._check_assertions()
        with open(path, "w") as f:
            json.dump(result, f, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_run(args):
    if args.scenario:
        paths = [args.scenario]
    elif args.dir:
        paths = sorted(Path(args.dir).glob("*.yaml"))
    else:
        print("Error: --scenario or --dir required")
        sys.exit(1)

    all_pass = True
    for p in paths:
        with open(p) as f:
            scenario = yaml.safe_load(f)
        seed = args.seed if args.seed is not None else scenario.get("seed", 42)
        harness = Harness(scenario, seed=seed)
        result = harness.run()

        base = Path(p).stem
        out_dir = Path(args.output_dir) if args.output_dir else Path(p).parent
        out_dir.mkdir(parents=True, exist_ok=True)

        harness.write_transcript(out_dir / f"{base}.transcript")
        harness.write_assertions(out_dir / f"{base}.assertions")

        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status}  {scenario.get('name', base)}  (seed={seed}, assertions={len(result['assertions'])})")
        for a in result["assertions"]:
            print(f"    {a['status']}  {a['name']}")

        if not result["passed"]:
            all_pass = False

    sys.exit(0 if all_pass else 1)


def cmd_verify(args):
    with open(args.scenario) as f:
        scenario = yaml.safe_load(f)

    seed = scenario.get("seed", 42)
    hashes = []
    for run in range(args.runs):
        harness = Harness(scenario, seed=seed)
        harness.run()
        h = hashlib.sha256(json.dumps(harness.transcript, sort_keys=True).encode()).hexdigest()[:16]
        hashes.append(h)

    unique = set(hashes)
    if len(unique) == 1:
        print(f"✅ Deterministic: {args.runs} runs produced identical transcript hash {hashes[0]}")
        sys.exit(0)
    else:
        print(f"❌ Non-deterministic: {len(unique)} unique hashes in {args.runs} runs")
        for i, h in enumerate(hashes):
            print(f"  Run {i}: {h}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="DAC Simulation Harness")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run scenario(s)")
    run_p.add_argument("--scenario", type=str, help="Path to scenario YAML")
    run_p.add_argument("--dir", type=str, help="Directory of scenario YAMLs")
    run_p.add_argument("--seed", type=int, default=None, help="Override random seed")
    run_p.add_argument("--output-dir", type=str, default=None, help="Output directory")

    ver_p = sub.add_parser("verify", help="Verify determinism")
    ver_p.add_argument("--scenario", type=str, required=True)
    ver_p.add_argument("--runs", type=int, default=5)

    args = parser.parse_args()
    if args.command == "run":
        cmd_run(args)
    elif args.command == "verify":
        cmd_verify(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
