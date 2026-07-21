#!/usr/bin/env python3
"""Syntropic router scaffold for lane arbitration and Soma-event logging.

This is the first tracked implementation surface for the router described in
`01_EMERGENTISM/11_UPLINK/00_CORE/06c_AGENTS_RESOLUTIONS_v3.md`.
"""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[3]
NOOSPHERE_ROOT = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE"
ORGANS_ROOT = NOOSPHERE_ROOT / "02_ORGANS"
RUNTIME_ROOT = NOOSPHERE_ROOT / "00_BACKBONE" / "local_runtime" / "router"
SESSIONS_PATH = RUNTIME_ROOT / "sessions.json"
LOCKS_PATH = RUNTIME_ROOT / "locks.json"
SOMA_ROOT = NOOSPHERE_ROOT / "SOMA_LOG"

TRANSITIONS: dict[str, dict[str, Any]] = {
    "L1_to_L2": {"required_payload_keys": ["contradictions", "context_digest"], "lane_required": False},
    "L2_to_L3": {"required_payload_keys": ["candidates"], "lane_required": False},
    "L3_to_L4": {"required_payload_keys": ["recommendations"], "lane_required": True},
    "L4_to_L5": {"required_payload_keys": ["deadlock_description", "candidate_set_explored", "constraint_hit"], "lane_required": True},
    "L4_to_L6": {"required_payload_keys": ["archive_targets", "compression_goal"], "lane_required": True},
    "L5_to_L4star": {"required_payload_keys": ["redesign_doc_path", "expected_delta_p"], "lane_required": True},
    "L6_to_L4star": {"required_payload_keys": ["compression_report_path"], "lane_required": True},
    "L4star_to_L7": {"required_payload_keys": ["full_audit_trail", "axiom_in_question", "proposed_amendment_or_clarification", "human_signoff_required"], "lane_required": False},
    "L7_to_L4star": {"required_payload_keys": ["verdict_doc_path", "downstream_changes_required"], "lane_required": False},
}

LANE_REGISTRY_PATHS: dict[str, Path] = {
    "FOUNDATION": PROJECT_ROOT / "03_VENTURES/_PORTFOLIO" / "OPEN_FINANCE_NETWORK" / "GOVERNANCE" / "FOUNDATION" / "LANES.md",
    "MENEXUS": PROJECT_ROOT / "03_VENTURES" / "MENEXUS" / "LANES.md",
    "QNTM": PROJECT_ROOT / "03_VENTURES/_PORTFOLIO" / "QNTM" / "LANES.md",
    "TheCircle": ORGANS_ROOT / "TheCircle" / "LANES.md",
    "RealityFutures": ORGANS_ROOT / "RealityFutures" / "LANES.md",
    "APU": ORGANS_ROOT / "Agentz" / "LANES.md",
    "Skyzai": ORGANS_ROOT / "Skyzai" / "LANES.md",
    "CORTEX": ORGANS_ROOT / "Skyzai" / "memory" / "cortex-os" / "LANES.md",
}

ALLOWED_WRITE_OPS = {
    "L4": {"create", "write", "append", "update", "commit"},
    "L6": {"archive", "delete_duplicate", "compact", "move", "rename", "restructure"},
}

FORBIDDEN_WRITE_OPS = {
    "L4": {"delete", "mass_archive", "archive", "move", "rename", "restructure"},
    "L6": {"create", "append", "extend_live_canon", "new_canonical_claim", "commit"},
}


@dataclass(frozen=True)
class Lane:
    organ: str
    surface: str
    domain: str

    @property
    def key(self) -> str:
        return f"{self.organ}|{self.surface}|{self.domain}"

    @property
    def compact(self) -> str:
        return f"{self.organ}:{self.surface}:{self.domain}"


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def ensure_runtime_dirs() -> None:
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    SOMA_ROOT.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def soma_path() -> Path:
    stamp = datetime.now().astimezone()
    return SOMA_ROOT / stamp.strftime("%Y-%m") / "events.ndjson"


def parse_json_arg(raw: str | None) -> dict[str, Any] | list[dict[str, Any]]:
    if not raw:
        return {}
    return json.loads(raw)


def parse_lane(raw: str | None) -> Lane | None:
    if not raw:
        return None
    parts = raw.split(":", 2)
    if len(parts) != 3:
        raise ValueError("Lane must use ORGAN:SURFACE:DOMAIN form.")
    organ, surface, domain = (part.strip() for part in parts)
    if not organ or not surface or not domain:
        raise ValueError("Lane ORGAN:SURFACE:DOMAIN components may not be empty.")
    return Lane(organ=organ, surface=surface, domain=domain)


def lane_registry_path(organ: str) -> Path | None:
    if organ in LANE_REGISTRY_PATHS:
        return LANE_REGISTRY_PATHS[organ]

    organ_candidate = ORGANS_ROOT / organ / "LANES.md"
    if organ_candidate.exists():
        return organ_candidate

    entity_candidate = PROJECT_ROOT / "03_VENTURES" / organ / "LANES.md"
    if entity_candidate.exists():
        return entity_candidate

    portfolio_candidate = PROJECT_ROOT / "03_VENTURES/_PORTFOLIO" / organ / "LANES.md"
    if portfolio_candidate.exists():
        return portfolio_candidate

    return None


def validate_lane_registry(lane: Lane) -> tuple[bool, str]:
    registry = lane_registry_path(lane.organ)
    if registry is None or not registry.exists():
        return False, f"Lane registry missing for organ/entity '{lane.organ}'."
    content = registry.read_text(encoding="utf-8", errors="ignore")
    if lane.domain not in content or lane.surface not in content:
        return False, f"Lane '{lane.compact}' is not declared in {registry}."
    return True, str(registry)


def new_session_id() -> str:
    return f"router-{datetime.now().astimezone().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"


class SyntropicRouter:
    def __init__(self) -> None:
        ensure_runtime_dirs()

    def _sessions(self) -> dict[str, Any]:
        return load_json(SESSIONS_PATH, {})

    def _locks(self) -> dict[str, Any]:
        return load_json(LOCKS_PATH, {})

    def _save_sessions(self, sessions: dict[str, Any]) -> None:
        write_json(SESSIONS_PATH, sessions)

    def _save_locks(self, locks: dict[str, Any]) -> None:
        write_json(LOCKS_PATH, locks)

    def _log(self, session_id: str | None, kind: str, data: dict[str, Any]) -> dict[str, Any]:
        event = {
            "timestamp": now_iso(),
            "session_id": session_id,
            "kind": kind,
            "data": data,
        }
        append_ndjson(soma_path(), event)
        return event

    def invoke(self, transition: str, payload: dict[str, Any], lane: Lane | None = None) -> dict[str, Any]:
        if transition not in TRANSITIONS:
            raise ValueError(f"Unknown transition '{transition}'.")

        spec = TRANSITIONS[transition]
        missing = [key for key in spec["required_payload_keys"] if key not in payload]
        if missing:
            raise ValueError(f"Missing payload keys for {transition}: {', '.join(missing)}")
        if spec["lane_required"] and lane is None:
            raise ValueError(f"Transition {transition} requires a lane.")
        if lane is not None:
            ok, reason = validate_lane_registry(lane)
            if not ok:
                raise ValueError(reason)

        sessions = self._sessions()
        session_id = new_session_id()
        session = {
            "id": session_id,
            "transition": transition,
            "payload": payload,
            "lane": asdict(lane) if lane else None,
            "status": "invoked",
            "created_at": now_iso(),
        }
        sessions[session_id] = session
        self._save_sessions(sessions)
        self._log(session_id, "invoke", {"transition": transition, "lane": lane.compact if lane else None})
        return session

    def acquire_lane(self, session_id: str, lane: Lane) -> dict[str, Any]:
        sessions = self._sessions()
        if session_id not in sessions:
            raise ValueError(f"Unknown session '{session_id}'.")

        ok, reason = validate_lane_registry(lane)
        if not ok:
            raise ValueError(reason)

        locks = self._locks()
        record = locks.get(lane.key, {"owner": None, "queue": []})

        if record["owner"] in (None, session_id):
            record["owner"] = session_id
            acquired = True
            queue_pos = None
            sessions[session_id]["status"] = "holding_lane"
        else:
            if session_id not in record["queue"]:
                record["queue"].append(session_id)
            acquired = False
            queue_pos = record["queue"].index(session_id) + 1
            sessions[session_id]["status"] = "queued_for_lane"

        locks[lane.key] = record
        self._save_locks(locks)
        self._save_sessions(sessions)
        self._log(session_id, "lane_acquire", {"lane": lane.compact, "acquired": acquired, "queue_pos": queue_pos})
        return {"acquired": acquired, "queue_pos": queue_pos}

    def release_lane(self, session_id: str, lane: Lane) -> dict[str, Any]:
        locks = self._locks()
        sessions = self._sessions()
        record = locks.get(lane.key)
        if not record:
            return {"released": False, "reason": "lane not held"}
        if record["owner"] != session_id:
            return {"released": False, "reason": "session is not lane owner"}

        next_owner = None
        if record["queue"]:
            next_owner = record["queue"].pop(0)
            record["owner"] = next_owner
            locks[lane.key] = record
            if next_owner in sessions:
                sessions[next_owner]["status"] = "holding_lane"
        else:
            del locks[lane.key]

        if session_id in sessions:
            sessions[session_id]["status"] = "released_lane"

        self._save_locks(locks)
        self._save_sessions(sessions)
        self._log(session_id, "lane_release", {"lane": lane.compact, "next_owner": next_owner})
        return {"released": True, "next_owner": next_owner}

    def request_commit(self, session_id: str, writes: list[dict[str, Any]], authority: str) -> dict[str, Any]:
        if authority not in ALLOWED_WRITE_OPS:
            raise ValueError("Authority must be L4 or L6.")

        sessions = self._sessions()
        if session_id not in sessions:
            raise ValueError(f"Unknown session '{session_id}'.")

        session = sessions[session_id]
        lane_dict = session.get("lane")
        if not lane_dict:
            return {"granted": False, "reason": "session has no lane"}

        lane = Lane(**lane_dict)
        locks = self._locks()
        lock = locks.get(lane.key)
        if not lock or lock.get("owner") != session_id:
            return {"granted": False, "reason": f"session does not hold lane {lane.compact}"}

        for write in writes:
            op = write.get("op", "")
            if op in FORBIDDEN_WRITE_OPS[authority]:
                reason = f"{authority} may not perform '{op}'"
                self._log(session_id, "commit_denied", {"lane": lane.compact, "authority": authority, "reason": reason})
                return {"granted": False, "reason": reason}
            if op not in ALLOWED_WRITE_OPS[authority]:
                reason = f"{authority} does not recognize '{op}' as an allowed write operation"
                self._log(session_id, "commit_denied", {"lane": lane.compact, "authority": authority, "reason": reason})
                return {"granted": False, "reason": reason}

        sessions[session_id]["status"] = "commit_granted"
        self._save_sessions(sessions)
        self._log(session_id, "commit_granted", {"lane": lane.compact, "authority": authority, "writes": writes})
        return {"granted": True, "reason": None}

    def soma_event(self, session_id: str | None, kind: str, data: dict[str, Any]) -> dict[str, Any]:
        return self._log(session_id, kind, data)

    def tick(self) -> dict[str, Any]:
        return self._log(None, "tick", {"status": "ok"})

    def dream_cycle(self) -> dict[str, Any]:
        return self._log(None, "dream_cycle", {"status": "triggered"})

    def audit(self, month: str | None = None, limit: int | None = None) -> list[dict[str, Any]]:
        target = month or datetime.now().astimezone().strftime("%Y-%m")
        path = SOMA_ROOT / target / "events.ndjson"
        if not path.exists():
            return []
        events: list[dict[str, Any]] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                events.append(json.loads(line))
        if limit is not None:
            return events[-limit:]
        return events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    invoke = subparsers.add_parser("invoke", help="Create a router session for a transition request.")
    invoke.add_argument("--transition", required=True, choices=sorted(TRANSITIONS))
    invoke.add_argument("--payload-json", default="{}", help="JSON payload for the transition.")
    invoke.add_argument("--lane", help="Lane in ORGAN:SURFACE:DOMAIN form.")
    invoke.add_argument("--json", action="store_true")

    acquire = subparsers.add_parser("acquire-lane", help="Acquire or queue for a lane lock.")
    acquire.add_argument("--session-id", required=True)
    acquire.add_argument("--lane", required=True)
    acquire.add_argument("--json", action="store_true")

    release = subparsers.add_parser("release-lane", help="Release a lane lock.")
    release.add_argument("--session-id", required=True)
    release.add_argument("--lane", required=True)
    release.add_argument("--json", action="store_true")

    commit = subparsers.add_parser("request-commit", help="Request lane-scoped commit authority.")
    commit.add_argument("--session-id", required=True)
    commit.add_argument("--authority", required=True, choices=["L4", "L6"])
    commit.add_argument("--writes-json", default="[]", help="JSON array of write operations.")
    commit.add_argument("--json", action="store_true")

    event = subparsers.add_parser("soma-event", help="Append a Soma-event directly.")
    event.add_argument("--session-id")
    event.add_argument("--kind", required=True)
    event.add_argument("--data-json", default="{}", help="JSON object with event data.")
    event.add_argument("--json", action="store_true")

    tick = subparsers.add_parser("tick", help="Emit a scheduler tick.")
    tick.add_argument("--json", action="store_true")

    dream = subparsers.add_parser("dream-cycle", help="Emit a dream-cycle trigger event.")
    dream.add_argument("--json", action="store_true")

    audit = subparsers.add_parser("audit", help="Read Soma-events for a month.")
    audit.add_argument("--month", help="Month in YYYY-MM form. Defaults to current month.")
    audit.add_argument("--limit", type=int)
    audit.add_argument("--json", action="store_true")

    return parser.parse_args()


def emit(payload: Any, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if isinstance(payload, list):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def main() -> int:
    args = parse_args()
    router = SyntropicRouter()

    if args.command == "invoke":
        payload = parse_json_arg(args.payload_json)
        result = router.invoke(args.transition, payload, parse_lane(args.lane))
        return emit(result, args.json)
    if args.command == "acquire-lane":
        result = router.acquire_lane(args.session_id, parse_lane(args.lane))
        return emit(result, args.json)
    if args.command == "release-lane":
        result = router.release_lane(args.session_id, parse_lane(args.lane))
        return emit(result, args.json)
    if args.command == "request-commit":
        writes = parse_json_arg(args.writes_json)
        if not isinstance(writes, list):
            raise ValueError("--writes-json must decode to a JSON list.")
        result = router.request_commit(args.session_id, writes, args.authority)
        return emit(result, args.json)
    if args.command == "soma-event":
        data = parse_json_arg(args.data_json)
        if not isinstance(data, dict):
            raise ValueError("--data-json must decode to a JSON object.")
        result = router.soma_event(args.session_id, args.kind, data)
        return emit(result, args.json)
    if args.command == "tick":
        return emit(router.tick(), args.json)
    if args.command == "dream-cycle":
        return emit(router.dream_cycle(), args.json)
    if args.command == "audit":
        return emit(router.audit(args.month, args.limit), args.json)
    raise AssertionError(f"Unhandled command {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
