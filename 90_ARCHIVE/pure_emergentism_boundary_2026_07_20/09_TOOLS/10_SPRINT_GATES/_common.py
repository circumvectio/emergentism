"""
Shared helpers for sprint gate runners.

Every `sprint_*_gates.py` follows the same pattern: run N gates, snapshot
the metabolism log, diff against the prior sprint's trace, emit a
trace artifact. This module owns the parts that don't vary.

Path layout (canonical after the 2026-05 root consolidation):

    PROJECT_ROOT / 02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/
        agents/                                — pipeline + cells
        memory/
            cell_metabolism.jsonl              — append-only dispatch log
            cortex_loop_traces/                — per-cycle cortex_loop traces
            sprint_traces/                     — sprint gate runs (THIS module's writes)
            pulse_traces/                      — per-beat pulse runs
            digests/                           — single-screen state snapshots
            lineage/                           — digest-over-digest diffs
            composer/                          — cell/tissue proposals
            contradictions/                    — typed contradiction artifacts
        execution_log/                         — K2 envelope inbox
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Walk up: _common.py -> 10_SPRINT_GATES/ -> 09_TOOLS/ -> 01_EMERGENTISM_ORG/ -> repo root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
AGENTS_DIR = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Skyzai" / "agents"
SKYZAI_DIR = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Skyzai"
MEMORY_DIR = SKYZAI_DIR / "memory"
SPRINT_TRACE_DIR = MEMORY_DIR / "sprint_traces"        # NEW canonical home
CORTEX_LOOP_TRACE_DIR = MEMORY_DIR / "cortex_loop_traces"  # cortex_loop traces only now
PULSE_TRACE_DIR = MEMORY_DIR / "pulse_traces"
DIGEST_DIR = MEMORY_DIR / "digests"
LINEAGE_DIR = MEMORY_DIR / "lineage"
COMPOSER_DIR = MEMORY_DIR / "composer"
METAB_LOG = MEMORY_DIR / "cell_metabolism.jsonl"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def env() -> dict:
    """Subprocess env: pipeline import path + z.ai credential aliases."""
    e = dict(os.environ)
    e["PYTHONPATH"] = f"{AGENTS_DIR}:{e.get('PYTHONPATH', '')}".rstrip(":")
    if not e.get("OPENAI_API_KEY") and e.get("ZAI_API_KEY"):
        e["OPENAI_API_KEY"] = e["ZAI_API_KEY"]
    if not e.get("OPENAI_BASE_URL") and e.get("ZAI_BASE_URL"):
        e["OPENAI_BASE_URL"] = e["ZAI_BASE_URL"]
    return e


def matrix_summary() -> dict:
    """Aggregate cell_metabolism.jsonl: total dispatches, by-cell, by-column."""
    if not METAB_LOG.exists():
        return {"total_dispatches": 0, "by_cell": {}, "by_address_L": {}, "by_column": {}}
    by_cell: dict[str, int] = defaultdict(int)
    by_L: dict[int, int] = defaultdict(int)
    by_col: dict[str, int] = defaultdict(int)
    n = 0
    for line in METAB_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        n += 1
        by_cell[r.get("cell", "<?>")] += 1
        addr = r.get("address") or {}
        if isinstance(addr.get("L"), int):
            by_L[addr["L"]] += 1
        if addr.get("D"):
            by_col[addr["D"]] += 1
    return {
        "total_dispatches": n,
        "by_cell": dict(sorted(by_cell.items(), key=lambda kv: -kv[1])),
        "by_address_L": dict(sorted(by_L.items())),
        "by_column": dict(sorted(by_col.items(), key=lambda kv: -kv[1])),
    }


def matrix_diff(current: dict, prior_glob: str) -> dict:
    """Compare current snapshot against the most-recent prior sprint trace
    matching `prior_glob` in SPRINT_TRACE_DIR.

    Returns a delta dict with new_cells / new_columns / total delta.
    """
    if not SPRINT_TRACE_DIR.exists():
        return {"prior_trace": None, "note": "no sprint_traces dir yet"}
    candidates = sorted(SPRINT_TRACE_DIR.glob(prior_glob), reverse=True)
    if not candidates:
        return {"prior_trace": None, "note": f"no prior trace matching {prior_glob}"}
    try:
        prior_trace = json.loads(candidates[0].read_text(encoding="utf-8"))
    except Exception as exc:
        return {"prior_trace": str(candidates[0]), "error": repr(exc)[:200]}
    prior = prior_trace.get("matrix_snapshot") or {}
    cells_now = current.get("by_cell", {})
    cells_prior = prior.get("by_cell", {})
    return {
        "prior_trace": str(candidates[0].relative_to(PROJECT_ROOT)),
        "prior_total": prior.get("total_dispatches", 0),
        "current_total": current.get("total_dispatches", 0),
        "delta_total": current.get("total_dispatches", 0) - prior.get("total_dispatches", 0),
        "new_cells_seen": sorted(set(cells_now) - set(cells_prior)),
        "new_columns_seen": sorted(set(current.get("by_column", {})) - set(prior.get("by_column", {}))),
    }


def run_python_script(code: str, timeout: int = 120) -> subprocess.CompletedProcess:
    """Run a Python script via tempfile (safe for multi-line code).

    Use this instead of `python -c "<long string>"` for any script with
    `for`/`if` blocks — semicolons-only doesn't work for those.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(textwrap.dedent(code))
        path = f.name
    try:
        return subprocess.run(
            [sys.executable, path],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            env=env(),
            timeout=timeout,
        )
    finally:
        Path(path).unlink(missing_ok=True)


def write_trace(*, sprint: str, gates: list[dict], snap: dict,
                diff: dict, doctrine_refs: list[str] | None = None) -> Path:
    """Build + write the standard sprint trace artifact. Returns the path.

    Same shape every sprint trace uses since Sprint 1 — keeps audits stable.
    """
    passed = sum(1 for g in gates if g.get("passed"))
    trace = {
        "trace_kind": "sprint_gate_run",
        "sprint": sprint,
        "trace_id": (
            f"sprint_{sprint}_"
            f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_"
            f"{uuid.uuid4().hex[:8]}"
        ),
        "started_at": now_iso(),
        "finished_at": now_iso(),
        "gates_total": len(gates),
        "gates_passed": passed,
        "gates_failed": len(gates) - passed,
        "all_passed": passed == len(gates),
        "gates": gates,
        "matrix_snapshot": snap,
        "matrix_diff": diff,
        "doctrine_refs": doctrine_refs or [
            "02_ORGANS/Skyzai/memory/cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md",
            "02_ORGANS/Skyzai/memory/cortex-os/19_ROADMAP.md",
        ],
    }
    SPRINT_TRACE_DIR.mkdir(parents=True, exist_ok=True)
    out = SPRINT_TRACE_DIR / f"{trace['trace_id']}.json"
    out.write_text(json.dumps(trace, indent=2, default=str), encoding="utf-8")
    return out


def print_summary(*, sprint: str, gates: list[dict], out_path: Path,
                   diff: dict | None = None) -> int:
    passed = sum(1 for g in gates if g.get("passed"))
    print(f"=== Sprint summary: {sprint} ===")
    for g in gates:
        marker = "✓" if g.get("passed") else "✗"
        print(f"  {marker} {g.get('name')}")
    print(f"\n{passed}/{len(gates)} gates passed")
    print(f"trace: {out_path.relative_to(PROJECT_ROOT)}")
    if diff and diff.get("prior_trace"):
        print(f"\n--- matrix diff ---")
        print(f"  prior: {diff['prior_trace']}")
        print(
            f"  total: {diff['prior_total']} -> {diff['current_total']} "
            f"(delta {diff['delta_total']:+d})"
        )
        if diff.get("new_cells_seen"):
            print(f"  new cells: {diff['new_cells_seen']}")
        if diff.get("new_columns_seen"):
            print(f"  new columns: {diff['new_columns_seen']}")
    return 0 if passed == len(gates) else 1


def run_gates_main(*, sprint: str, gate_funcs: list, prior_glob: str,
                    doctrine_refs: list[str] | None = None) -> int:
    """Run gate functions in order, write trace, print summary, return exit code.

    Each gate function takes no args and returns a dict with at least
    {"name": str, "passed": bool}.
    """
    print(f"=== Sprint: {sprint} — gate run ===")
    print(f"started: {now_iso()}\n")
    gates: list[dict] = []
    for fn in gate_funcs:
        print(f"running: {fn.__name__}")
        result = fn()
        marker = "[PASS]" if result.get("passed") else "[FAIL]"
        print(f"  {marker} {result.get('name')}\n")
        gates.append(result)
    snap = matrix_summary()
    diff = matrix_diff(snap, prior_glob)
    out = write_trace(sprint=sprint, gates=gates, snap=snap, diff=diff,
                      doctrine_refs=doctrine_refs)
    return print_summary(sprint=sprint, gates=gates, out_path=out, diff=diff)


__all__ = [
    "PROJECT_ROOT", "AGENTS_DIR", "SKYZAI_DIR", "MEMORY_DIR",
    "SPRINT_TRACE_DIR", "CORTEX_LOOP_TRACE_DIR", "PULSE_TRACE_DIR",
    "DIGEST_DIR", "LINEAGE_DIR", "COMPOSER_DIR", "METAB_LOG",
    "now_iso", "env", "matrix_summary", "matrix_diff",
    "run_python_script", "write_trace", "print_summary", "run_gates_main",
]
