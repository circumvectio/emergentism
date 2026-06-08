#!/usr/bin/env python3
"""Sprint 2: Tissues — gate run."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, run_python_script, METAB_LOG,
)


def _count_metab_lines() -> int:
    if not METAB_LOG.exists(): return 0
    return sum(1 for line in METAB_LOG.read_text(encoding="utf-8").splitlines() if line.strip())


def gate_A_heartbeat_cells_declared() -> dict:
    proc = run_python_script('''
        import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.cells import heartbeat as hb
        addrs = [hb.heartbeat_cell_address(L) for L in range(1, 8)]
        assert len(addrs) == 7
        assert all(a.D == 'C-Γ' and a.S == 'Org' for a in addrs)
        print('ok')
    ''')
    return {"name": "heartbeat_cells_declared",
            "passed": proc.returncode == 0 and "ok" in proc.stdout,
            "stderr_head": proc.stderr[:200] if proc.returncode != 0 else None}


def gate_B_pathology_witness() -> dict:
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.cell_witness", "--since", "30d", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "pathology_witness",
            "passed": proc.returncode == 0 and body.get("report_kind") == "cell_witness_report",
            "totals": body.get("totals")}


def gate_C_heartbeat_live() -> dict:
    before = _count_metab_lines()
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.organism_heartbeat", "--demo", "--once", "--zai-mixed"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=600)
    after = _count_metab_lines()
    delta = after - before
    out = proc.stdout or ""
    hb_lines = 0
    if delta > 0 and METAB_LOG.exists():
        for line in METAB_LOG.read_text(encoding="utf-8").splitlines()[-delta:]:
            try:
                r = json.loads(line)
                if (r.get("cell") or "").startswith("heartbeat-"): hb_lines += 1
            except Exception: pass
    return {"name": "heartbeat_live",
            "passed": proc.returncode == 0 and "[matrix]" in out and hb_lines > 0,
            "metab_lines_added": delta, "heartbeat_cell_dispatches": hb_lines}


def gate_D_multi_column_matrix() -> dict:
    from sprint_gates._common import matrix_summary
    snap = matrix_summary()
    cols = snap.get("by_column", {})
    return {"name": "multi_column_matrix",
            "passed": cols.get("C-K", 0) > 0 and cols.get("C-Γ", 0) > 0,
            "by_column": cols}


def gate_E_tissue_end_to_end() -> dict:
    proc = run_python_script('''
        import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.cell import cell, CellAddress, CellResult
        from pipeline.cell_registry import CellRegistry
        from pipeline.tissue import Tissue, TissueStep

        @cell(L=1, D='C-K', S='Org', F='F-phi', name='gate_e_ta')
        def ta(s): return CellResult(decision='ta', output=s + '-A')
        @cell(L=2, D='C-K', S='Org', F='F-phi', name='gate_e_tb')
        def tb(s): return CellResult(decision='tb', output=s + '-B')

        reg = CellRegistry()
        reg.register(ta); reg.register(tb)
        t = Tissue(name='gate_e_ab',
                   address=CellAddress(L=2, D='C-K', S='Org', F='F-P'),
                   steps=[TissueStep(cell='gate_e_ta', signal_builder=lambda ctx: ctx.input),
                          TissueStep(cell='gate_e_tb', signal_builder=lambda ctx: ctx.last.output)])
        r = t.run('seed', registry=reg)
        assert r.success and r.output == 'seed-A-B' and len(r.cell_results) == 2
        print('ok')
    ''')
    return {"name": "tissue_end_to_end",
            "passed": proc.returncode == 0 and "ok" in proc.stdout,
            "stderr_head": proc.stderr[:300] if proc.returncode != 0 else None}


def main() -> int:
    return run_gates_main(
        sprint="tissues",
        gate_funcs=[gate_A_heartbeat_cells_declared, gate_B_pathology_witness,
                    gate_C_heartbeat_live, gate_D_multi_column_matrix,
                    gate_E_tissue_end_to_end],
        prior_glob="sprint_first_cell_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
