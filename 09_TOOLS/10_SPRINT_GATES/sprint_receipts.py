#!/usr/bin/env python3
"""Sprint 4: Receipts — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, PULSE_TRACE_DIR,
)


def gate_A_k2_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.k2_inbox import summarize, iter_envelopes, show, parse_window;"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "k2_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_k2_pending() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.k2_inbox", "--pending", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    summary = {}
    if proc.returncode == 0:
        try: summary = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "k2_pending",
            "passed": proc.returncode == 0 and summary.get("pending_count") is not None,
            "pending_count": summary.get("pending_count")}


def gate_C_k2_by_type() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.k2_inbox", "--by-type"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    return {"name": "k2_by_type",
            "passed": proc.returncode == 0 and "by type" in (proc.stdout or "")}


def gate_D_k2_top_stale() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.k2_inbox", "--top-stale", "5"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    return {"name": "k2_top_stale",
            "passed": proc.returncode == 0 and "oldest-pending" in (proc.stdout or "")}


def gate_E_pulse_includes_k2() -> dict:
    before = set(p.name for p in PULSE_TRACE_DIR.glob("pulse_*.json")) if PULSE_TRACE_DIR.exists() else set()
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.pulse", "--once", "--dry-run",
         "--skip-cortex-loop", "--skip-heartbeat", "--skip-witness"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    after = set(p.name for p in PULSE_TRACE_DIR.glob("pulse_*.json")) if PULSE_TRACE_DIR.exists() else set()
    new = sorted(after - before)
    if not new:
        return {"name": "pulse_includes_k2", "passed": False, "reason": "no new pulse trace"}
    body = json.loads((PULSE_TRACE_DIR / new[-1]).read_text(encoding="utf-8"))
    phases = body.get("phases", {})
    return {"name": "pulse_includes_k2",
            "passed": ("k2_inbox" in phases
                       and phases["k2_inbox"].get("ok") is True
                       and isinstance(phases["k2_inbox"].get("pending_count"), int)),
            "k2_inbox_in_trace": "k2_inbox" in phases,
            "pending_count_in_trace": phases.get("k2_inbox", {}).get("pending_count")}


def main() -> int:
    return run_gates_main(
        sprint="receipts",
        gate_funcs=[gate_A_k2_imports, gate_B_k2_pending, gate_C_k2_by_type,
                    gate_D_k2_top_stale, gate_E_pulse_includes_k2],
        prior_glob="sprint_pulse_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
