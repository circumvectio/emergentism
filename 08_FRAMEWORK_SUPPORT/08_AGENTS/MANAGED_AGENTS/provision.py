#!/usr/bin/env python3
"""Provision only the four operational Rosetta seats as Claude Managed Agents.

ONE-TIME SETUP — run once, then reuse the IDs in agent_ids.json on every session.
Idempotent by name: re-running skips agents that already exist.

Prerequisites:
    pip install anthropic pyyaml
    export ANTHROPIC_API_KEY=sk-ant-...        # or: ant auth login

What it does (control plane):
    1. Create (or reuse) the shared `emergentism-seven` cloud environment.
    2. Create (or reuse) L1-L3 from agents/*.agent.yaml.
    3. Create (or reuse) L4 Kṣatriya (Arjuna) as a MULTIAGENT COORDINATOR
       over L1-L3 plus self. L5-L7 remain non-deployable counsel phases and are
       never created as persistent hosted agents.
    4. Write agent_ids.json { name: {id, version} } + the environment id.

It does NOT start sessions — sessions are the data plane (per task), driven from
your application. See README §Runtime for the session pattern.

Managed Agents is beta; the SDK sets `managed-agents-2026-04-01` automatically on
client.beta.{environments,agents,sessions}.* calls.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENTS_DIR = HERE / "agents"
ENV_FILE = HERE / "emergentism.environment.yaml"
OUT_FILE = HERE / "agent_ids.json"

# L4 Kṣatriya (Arjuna) is the hosted coordinator over operational L1-L3 only.
# We identify its spec file (04_*) by these substrings in the yaml `name:` so a wording
# tweak doesn't break the wiring. Canonical name: "Emergentism · L4 Kṣatriya (Arjuna) — Executor".
L4_TOKENS = ("Arjuna", "Executor", "L4", "Kṣatriya", "Ksatriya")
OPERATIONAL_LEVELS = {"L1", "L2", "L3", "L4"}


def is_l4(name: str) -> bool:
    return any(tok in name for tok in L4_TOKENS)

try:
    import yaml  # pyyaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency: pip install anthropic")


def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def find_by_name(items, name: str):
    """Return the first resource whose .name matches, else None (auto-paginates)."""
    for it in items:
        if getattr(it, "name", None) == name:
            return it
    return None


def model_for(spec: dict) -> str:
    """Resolve an applied model assignment; caste YAMLs intentionally pin none."""
    level = (spec.get("metadata") or {}).get("level")
    if not isinstance(level, str):
        raise ValueError(f"agent {spec.get('name')!r} has no metadata.level")
    variable = f"ROSETTA_MODEL_{level}"
    model = os.environ.get(variable, "").strip()
    if not model:
        raise ValueError(f"{variable} is required; model routing is registry-bound")
    return model


def main() -> None:
    client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY / auth profile

    # 1. Environment (create or reuse by name) ------------------------------
    env_spec = load_yaml(ENV_FILE)
    existing_env = find_by_name(client.beta.environments.list(), env_spec["name"])
    if existing_env:
        env = existing_env
        print(f"= environment exists: {env.name} ({env.id})")
    else:
        env = client.beta.environments.create(
            name=env_spec["name"],
            description=env_spec.get("description", ""),
            config=env_spec["config"],
        )
        print(f"+ environment created: {env.name} ({env.id})")

    # 2. Operational agents (create or reuse by name) -----------------------
    # Create L1-L3 first, collect their ids, THEN create L4 as coordinator.
    # L5-L7 are source-owned counsel phases, never persistent hosted agents. multiagent must
    # be injected at create time on the L4 agent — the platform shape is
    #   multiagent={"type": "coordinator", "agents": [<L1-L3 ids>, {"type": "self"}]}.
    existing_agents = {a.name: a for a in client.beta.agents.list()}
    results: dict[str, dict] = {"_environment": {"name": env.name, "id": env.id}}

    all_specs = [(p, load_yaml(p)) for p in sorted(AGENTS_DIR.glob("*.agent.yaml"))]
    specs = [(p, s) for p, s in all_specs if (s.get("metadata") or {}).get("level") in OPERATIONAL_LEVELS]
    non_l4 = [(p, s) for (p, s) in specs if not is_l4(s["name"])]
    l4 = [(p, s) for (p, s) in specs if is_l4(s["name"])]
    if {(s.get("metadata") or {}).get("level") for _p, s in non_l4} != {"L1", "L2", "L3"} or len(l4) != 1:
        raise ValueError("hosted roster must be exactly L1-L3 workers plus one L4 coordinator")

    def create_or_reuse(spec: dict, **extra) -> object:
        """Create the agent by name, or reuse the existing one (idempotent by name)."""
        name = spec["name"]
        model = model_for(spec)
        if name in existing_agents:
            a = existing_agents[name]
            print(f"= agent exists:  {name}  ({a.id} v{a.version})")
            return a
        a = client.beta.agents.create(
            name=name,
            model=model,
            description=spec.get("description", ""),
            system=spec.get("system", ""),
            tools=spec.get("tools", []),
            metadata={k: str(v) for k, v in (spec.get("metadata") or {}).items()},
            **extra,
        )
        tag = " +coordinator" if "multiagent" in extra else ""
        print(f"+ agent created: {name}  ({a.id} v{a.version})  [{model}]{tag}")
        return a

    # 2a. L1-L3 first — collect their ids for the L4 roster.
    worker_ids: list[str] = []
    for _path, spec in non_l4:
        a = create_or_reuse(spec)
        results[spec["name"]] = {"id": a.id, "version": a.version, "model": model_for(spec)}
        worker_ids.append(a.id)

    # 2b. L4, wired over L1-L3 plus self. Boundary counsel is not provisioned.
    roster = [*worker_ids, {"type": "self"}]
    for _path, spec in l4:
        a = create_or_reuse(
            spec,
            multiagent={"type": "coordinator", "agents": roster},
        )
        results[spec["name"]] = {"id": a.id, "version": a.version, "model": model_for(spec)}
        if spec["name"] in existing_agents:
            # Existing agent reused by name — inject/refresh the coordinator roster via
            # update so Arjuna delegates to L1-L3 on a re-run (idempotent-friendly).
            try:
                updated = client.beta.agents.update(
                    a.id,
                    multiagent={"type": "coordinator", "agents": roster},
                )
                results[spec["name"]]["version"] = updated.version
                print(f"~ coordinator roster updated on {spec['name']} (v{updated.version})")
            except Exception as e:  # noqa: BLE001 — non-fatal; roster may already match
                print(f"! could not update coordinator roster on {spec['name']}: {e}")

    OUT_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nWrote {OUT_FILE.relative_to(HERE)} ({len(results) - 1} agents).")
    print(f"L4 (Arjuna) coordinates {len(worker_ids)} operational seats + self; L5-L7 remain non-deployable counsel.")
    print("Watch sessions in Console: https://platform.claude.com/workspaces/default/sessions")


if __name__ == "__main__":
    main()
