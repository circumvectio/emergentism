#!/usr/bin/env python3
"""Run ONE Managed-Agents session against the L4 Kṣatriya (Arjuna) executor.

DATA PLANE (per task) — the runnable counterpart to provision.py's control plane.
provision.py creates the env + 7 agents and writes agent_ids.json; this script loads
those IDs, resolves the L4 executor + the shared environment, opens ONE session, and
streams it to completion. Arjuna is wired as the multiagent coordinator over the other
six (see provision.py / provision.sh), so a single session at L4 can delegate down the
caste ensemble — each delegation surfaces here as a `session.thread_created` event.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...        # or: ant auth login
    python run_session.py "Audit 06_ONTOLOGY and stage the smallest-defensible diff."

Platform discipline (mirrors README §Runtime + the claude-api Managed-Agents patterns):
    * STREAM-FIRST — open events.stream() BEFORE events.send() the kickoff, or the
      first events arrive buffered and you lose real-time reactivity.
    * Idle-break GATE — break on session.status_terminated, OR on session.status_idle
      whose stop_reason.type != 'requires_action'. Idle with requires_action is an
      ordinary tool-confirmation wait — do NOT break there.
    * Post-idle status race — the stream emits idle slightly before sessions.retrieve()
      reflects it, so poll a few times before reporting the final status.

Authorization note: Arjuna's write/edit/bash carry permission_policy always_ask. When
the agent prepares a mutation, the session goes idle with stop_reason.type ==
'requires_action' and an agent.tool_use event with evaluated_permission == 'ask'.
This script surfaces that ordinary tool-permission wait but never auto-confirms it.

Managed Agents is beta; the SDK sets `managed-agents-2026-04-01` automatically on
client.beta.{environments,agents,sessions}.* calls.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS_FILE = HERE / "agent_ids.json"

DEFAULT_TASK = (
    "Bring a decision to the equator: firewall the inputs (L1), explore candidates "
    "(L2), rank them (L3), then as L4 prepare the SMALLEST-defensible diff. Tier every "
    "claim (A7); archive, never delete (K3); escalate structural deadlocks to L5. Do "
    "NOT exceed the user's scope or granted permissions. For a consequential mutation, "
    "prepare the smallest reversible diff and wait for explicit tool confirmation when asked."
)

# Substrings that identify the L4 executor key written by provision.py. The canonical
# key is "Emergentism · L4 Kṣatriya (Arjuna) — Executor"; we match defensively on any of
# these tokens so a wording tweak in the yaml `name:` doesn't break resolution.
L4_TOKENS = ("Arjuna", "Executor", "L4", "Kṣatriya", "Ksatriya")

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency: pip install anthropic")


def load_ids() -> dict:
    if not IDS_FILE.exists():
        sys.exit(
            f"{IDS_FILE.name} not found — run provision.py (or provision.sh) first to "
            "create the environment + seven agents."
        )
    return json.loads(IDS_FILE.read_text())


def resolve_l4(ids: dict) -> tuple[str, str]:
    """Return (agent_name, agent_id) for the L4 executor, matched by name key."""
    for name, info in ids.items():
        if name == "_environment" or not isinstance(info, dict):
            continue
        if any(tok in name for tok in L4_TOKENS):
            return name, info["id"]
    sys.exit(
        "Could not find the L4 executor (Arjuna) in agent_ids.json. Looked for any of "
        f"{L4_TOKENS} in the agent-name keys; found: "
        f"{[k for k in ids if k != '_environment']}"
    )


def resolve_env(ids: dict) -> str:
    env = ids.get("_environment")
    if not env or "id" not in env:
        sys.exit('agent_ids.json is missing ["_environment"]["id"] — re-run provision.py.')
    return env["id"]


def text_blocks(event) -> str:
    """Concatenate the .text of any text content blocks on an agent.message event."""
    out = []
    for block in getattr(event, "content", None) or []:
        if getattr(block, "type", None) == "text":
            out.append(getattr(block, "text", "") or "")
    return "".join(out)


def main() -> None:
    task = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TASK

    ids = load_ids()
    env_id = resolve_env(ids)
    l4_name, l4_id = resolve_l4(ids)

    client = anthropic.Anthropic()  # resolves ANTHROPIC_API_KEY / auth profile

    print(f"→ executor : {l4_name}")
    print(f"→ agent_id : {l4_id}")
    print(f"→ env_id   : {env_id}")

    # Create ONE session against the L4 agent (string-id shorthand → latest version).
    session = client.beta.sessions.create(
        agent=l4_id,
        environment_id=env_id,
        title="Emergentism · L4 Arjuna session",
    )
    console_url = (
        f"https://platform.claude.com/workspaces/default/sessions/{session.id}"
    )
    print(f"→ session  : {session.id}  ({session.status})")
    print(f"→ console  : {console_url}\n")

    # STREAM-FIRST: open the stream, THEN send the kickoff user.message.
    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        client.beta.sessions.events.send(
            session_id=session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": task}],
                }
            ],
        )

        for event in stream:
            etype = getattr(event, "type", None)

            if etype == "agent.message":
                chunk = text_blocks(event)
                if chunk:
                    print(chunk, end="", flush=True)

            elif etype == "session.thread_created":
                # Arjuna (coordinator) spawned a sub-operator thread — a delegation
                # down the caste ensemble (e.g. L1 firewall, L2 explore, L3 rank).
                sub = getattr(event, "agent_name", None) or "<sub-operator>"
                print(f"\n  [delegation] coordinator spawned thread → {sub}", flush=True)

            elif etype == "session.status_terminated":
                print("\n--- session terminated ---", flush=True)
                break

            elif etype == "session.status_idle":
                stop = getattr(event, "stop_reason", None)
                stop_type = getattr(stop, "type", None)
                if stop_type == "requires_action":
                    # Transient: the agent is waiting on ordinary tool confirmation
                    # or a custom tool result. Do not break; surface the wait and keep
                    # the stream open for the next event.
                    print(
                        "\n--- idle: awaiting tool confirmation — "
                        "stage prepared; not breaking ---",
                        flush=True,
                    )
                    continue
                # end_turn / retries_exhausted — both terminal.
                print(f"\n--- session idle (stop_reason={stop_type}) ---", flush=True)
                break

    # Post-idle status-write race: the stream emits idle slightly before the queryable
    # status reflects it. Poll a few times before reporting the final status.
    final = None
    for _ in range(10):
        final = client.beta.sessions.retrieve(session_id=session.id)
        if final.status != "running":
            break
        time.sleep(0.2)

    print(f"\n→ final status: {final.status if final else 'unknown'}")
    print(f"→ watch / continue in Console: {console_url}")


if __name__ == "__main__":
    main()
