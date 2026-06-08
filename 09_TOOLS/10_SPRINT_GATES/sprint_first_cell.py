#!/usr/bin/env python3
"""Sprint 1: First Cell — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, run_python_script, METAB_LOG, SKYZAI_DIR,
)


SOURCE_FILES = [
    SKYZAI_DIR / "agents" / "pipeline" / "cell.py",
    SKYZAI_DIR / "agents" / "pipeline" / "cell_registry.py",
    SKYZAI_DIR / "agents" / "pipeline" / "cell_metabolism.py",
    SKYZAI_DIR / "agents" / "pipeline" / "cells" / "__init__.py",
    SKYZAI_DIR / "agents" / "pipeline" / "cells" / "cortex_watchmen.py",
    SKYZAI_DIR / "agents" / "pipeline" / "cells" / "aia.py",
]


def _count_metab_lines() -> int:
    if not METAB_LOG.exists(): return 0
    return sum(1 for line in METAB_LOG.read_text(encoding="utf-8").splitlines() if line.strip())


def gate_1_protocol() -> dict:
    files_status = []
    for f in SOURCE_FILES:
        p = subprocess.run([sys.executable, "-m", "py_compile", str(f)],
                           cwd=PROJECT_ROOT, capture_output=True, text=True)
        files_status.append({"file": str(f.relative_to(PROJECT_ROOT)), "ok": p.returncode == 0})
    proc = run_python_script('''
        import sys; sys.path.insert(0, '02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/agents')
        from pipeline.cell import CellAddress, CellResult, FunctionCell, cell
        a = CellAddress(L=4, D='C-K', S='Org', F='F-nu')
        r = CellResult(decision='HOLD')
        assert a.to_dict() == {'L':4,'D':'C-K','S':'Org','F':'F-nu'}
        assert r.success
        print('ok')
    ''')
    return {
        "name": "protocol",
        "passed": all(f["ok"] for f in files_status) and "ok" in proc.stdout,
        "files_compiled": files_status,
    }


def gate_2_registry() -> dict:
    proc = run_python_script('''
        import sys, json
        sys.path.insert(0, '02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/agents')
        from pipeline.cell import CellAddress
        from pipeline.cell_registry import CellRegistry, NoCellRegistered, PRECEDENCE_LADDER
        from pipeline.cells import cortex_watchmen as cw, aia
        reg = CellRegistry()
        cw.register_all(reg); aia.register_all(reg)
        cells = [(c.name, c.address.to_dict()) for c in reg.list_cells()]
        assert len(cells) == 7, len(cells)
        # Ladder rungs
        assert reg.resolve(CellAddress(L=4, D='C-K', S='Org', F='F-nu')).matched_at == 'exact'
        assert reg.resolve(CellAddress(L=4, D='C-K', S='Org', F='F-P')).matched_at == 'any-face'
        assert reg.resolve(CellAddress(L=4, D='C-K', S='Civ', F='F-nu')).matched_at == 'any-scale'
        assert reg.resolve(CellAddress(L=4, D='C-Pi', S='Org', F='F-nu')).matched_at == 'L-only'
        try:
            reg.resolve(CellAddress(L=2, D='C-K', S='Org', F='F-P'))
            assert False
        except NoCellRegistered:
            pass
        print(json.dumps({"cells": cells, "ladder": list(PRECEDENCE_LADDER)}))
    ''')
    payload = {}
    if proc.returncode == 0:
        try: payload = json.loads(proc.stdout)
        except Exception: pass
    return {
        "name": "registry",
        "passed": proc.returncode == 0 and len(payload.get("cells", [])) == 7,
        "cells_count": len(payload.get("cells", [])),
        "ladder_rungs_verified": ["exact", "any-face", "any-scale", "L-only", "raise"] if proc.returncode == 0 else [],
    }


def gate_3_retrofit() -> dict:
    before = _count_metab_lines()
    proc = subprocess.run([sys.executable, "01_EMERGENTISM/09_TOOLS/01_SCRIPTS/watchman_run.py", "--no-llm"],
                          cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    after = _count_metab_lines()
    out = proc.stdout or ""
    return {
        "name": "retrofit",
        "passed": (proc.returncode == 0 and "dispatch: cell-registry" in out
                   and (after - before) > 0),
        "metab_lines_added": after - before,
    }


def gate_4_metabolism() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.cell_metabolism", "--summary"],
                          cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    summary = {}
    if proc.returncode == 0:
        try: summary = json.loads(proc.stdout)
        except Exception: pass
    return {
        "name": "metabolism",
        "passed": proc.returncode == 0 and summary.get("total_dispatches", 0) > 0,
        "summary": summary,
    }


def gate_5_new_cell() -> dict:
    before = _count_metab_lines()
    proc = subprocess.run([sys.executable, "-m", "pipeline.cells.aia"],
                          cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    after = _count_metab_lines()
    return {
        "name": "new_cell",
        "passed": proc.returncode == 0 and (after - before) == 1,
        "metab_lines_added": after - before,
    }


def main() -> int:
    return run_gates_main(
        sprint="first_cell",
        gate_funcs=[gate_1_protocol, gate_2_registry, gate_3_retrofit,
                    gate_4_metabolism, gate_5_new_cell],
        prior_glob="sprint_first_cell_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
