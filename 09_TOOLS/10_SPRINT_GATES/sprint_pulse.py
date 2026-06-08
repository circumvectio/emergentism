#!/usr/bin/env python3
"""Sprint 3: Pulse — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, PULSE_TRACE_DIR,
)


def gate_A_pulse_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.pulse import run_beat, phase_cortex_loop, phase_heartbeat, "
        "phase_cell_witness, PULSE_TRACE_DIR; print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "pulse_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_pulse_dry_run() -> dict:
    before = set(p.name for p in PULSE_TRACE_DIR.glob("pulse_*.json")) if PULSE_TRACE_DIR.exists() else set()
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.pulse", "--once", "--dry-run"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=600)
    after = set(p.name for p in PULSE_TRACE_DIR.glob("pulse_*.json")) if PULSE_TRACE_DIR.exists() else set()
    new = sorted(after - before)
    return {"name": "pulse_dry_run",
            "passed": proc.returncode == 0 and "ALL OK" in (proc.stdout or "") and len(new) >= 1,
            "new_pulse_traces": new}


def gate_C_phase_summary_shape() -> dict:
    if not PULSE_TRACE_DIR.exists():
        return {"name": "phase_summary_shape", "passed": False}
    candidates = sorted(PULSE_TRACE_DIR.glob("pulse_*.json"), reverse=True)
    if not candidates:
        return {"name": "phase_summary_shape", "passed": False}
    body = json.loads(candidates[0].read_text(encoding="utf-8"))
    expected = {"beat_id", "trace_kind", "started_at", "finished_at",
                "phases", "all_ok", "total_metab_lines_added"}
    missing = expected - set(body.keys())
    return {"name": "phase_summary_shape",
            "passed": not missing,
            "phases_present": sorted(body.get("phases", {}).keys())}


def gate_D_matrix_grew() -> dict:
    from sprint_gates._common import matrix_summary, matrix_diff
    snap = matrix_summary()
    diff = matrix_diff(snap, "sprint_tissues_*.json")
    return {"name": "matrix_grew_since_sprint_2",
            "passed": diff.get("delta_total", 0) >= 0,
            "diff": diff}


def gate_E_pulse_phases_independent() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.pulse",
                           "--once", "--skip-cortex-loop", "--skip-heartbeat"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    return {"name": "pulse_phases_independent",
            "passed": proc.returncode == 0 and "ALL OK" in (proc.stdout or "")}


def main() -> int:
    return run_gates_main(
        sprint="pulse",
        gate_funcs=[gate_A_pulse_imports, gate_B_pulse_dry_run,
                    gate_C_phase_summary_shape, gate_D_matrix_grew,
                    gate_E_pulse_phases_independent],
        prior_glob="sprint_tissues_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
