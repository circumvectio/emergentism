#!/usr/bin/env python3
"""Provision the seven Emergentism caste agents as Claude Managed Agents.

ONE-TIME SETUP — run once, then reuse the IDs in agent_ids.json on every session.
Idempotent by name: re-running skips agents that already exist.

Prerequisites:
    pip install anthropic pyyaml
    export ANTHROPIC_API_KEY=sk-ant-...        # or: ant auth login

What it does (control plane):
    1. Create (or reuse) the shared `emergentism-seven` cloud environment.
    2. Create (or reuse) the SIX non-L4 caste agents from agents/*.agent.yaml.
    3. Create (or reuse) the L4 Kṣatriya (Arjuna) executor as a MULTIAGENT COORDINATOR
       over those six (multiagent={type: coordinator, agents:[<six ids>, {type: self}]}),
       so a single L4 session can delegate down the caste ensemble.
    4. Write agent_ids.json { name: {id, version} } + the environment id.

It does NOT start sessions — sessions are the data plane (per task), driven from
your application. See README §Runtime for the session pattern.

Managed Agents is beta; the SDK sets `managed-agents-2026-04-01` automatically on
client.beta.{environments,agents,sessions}.* calls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENTS_DIR = HERE / "agents"
ENV_FILE = HERE / "emergentism.environment.yaml"
OUT_FILE = HERE / "agent_ids.json"

# The L4 Kṣatriya (Arjuna) executor is the multiagent COORDINATOR over the other six.
# We identify its spec file (04_*) by these substrings in the yaml `name:` so a wording
# tweak doesn't break the wiring. Canonical name: "Emergentism · L4 Kṣatriya (Arjuna) — Executor".
L4_TOKENS = ("Arjuna", "Executor", "L4", "Kṣatriya", "Ksatriya")


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

    # 2. Agents (create or reuse by name) -----------------------------------
    # Split the roster: create the SIX non-L4 castes first, collect their ids, THEN
    # create the L4 (Arjuna) executor as a coordinator over those six. multiagent must
    # be injected at create time on the L4 agent — the platform shape is
    #   multiagent={"type": "coordinator", "agents": [<six ids>, {"type": "self"}]}.
    existing_agents = {a.name: a for a in client.beta.agents.list()}
    results: dict[str, dict] = {"_environment": {"name": env.name, "id": env.id}}

    specs = [(p, load_yaml(p)) for p in sorted(AGENTS_DIR.glob("*.agent.yaml"))]
    non_l4 = [(p, s) for (p, s) in specs if not is_l4(s["name"])]
    l4 = [(p, s) for (p, s) in specs if is_l4(s["name"])]

    def create_or_reuse(spec: dict, **extra) -> object:
        """Create the agent by name, or reuse the existing one (idempotent by name)."""
        name = spec["name"]
        if name in existing_agents:
            a = existing_agents[name]
            print(f"= agent exists:  {name}  ({a.id} v{a.version})")
            return a
        a = client.beta.agents.create(
            name=name,
            model=spec["model"],
            description=spec.get("description", ""),
            system=spec.get("system", ""),
            tools=spec.get("tools", []),
            metadata={k: str(v) for k, v in (spec.get("metadata") or {}).items()},
            **extra,
        )
        tag = " +coordinator" if "multiagent" in extra else ""
        print(f"+ agent created: {name}  ({a.id} v{a.version})  [{spec['model']}]{tag}")
        return a

    # 2a. The six non-L4 castes first — collect their ids for the L4 roster.
    six_ids: list[str] = []
    for _path, spec in non_l4:
        a = create_or_reuse(spec)
        results[spec["name"]] = {"id": a.id, "version": a.version, "model": spec["model"]}
        six_ids.append(a.id)

    # 2b. The L4 Kṣatriya (Arjuna) executor, wired as coordinator over the six.
    roster = [*six_ids, {"type": "self"}]  # the six + self-delegation
    for _path, spec in l4:
        a = create_or_reuse(
            spec,
            multiagent={"type": "coordinator", "agents": roster},
        )
        results[spec["name"]] = {"id": a.id, "version": a.version, "model": spec["model"]}
        if spec["name"] in existing_agents:
            # Existing agent reused by name — inject/refresh the coordinator roster via
            # update so Arjuna delegates to the six even on a re-run (idempotent-friendly).
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
    print(f"L4 (Arjuna) coordinates {len(six_ids)} castes + self.")
    print("Watch sessions in Console: https://platform.claude.com/workspaces/default/sessions")


if __name__ == "__main__":
    main()
