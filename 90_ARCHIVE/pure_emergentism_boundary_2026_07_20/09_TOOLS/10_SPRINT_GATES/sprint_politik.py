#!/usr/bin/env python3
"""Sprint 6: Politik — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, run_python_script, METAB_LOG,
)


def gate_A_politik_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.cells.k2_politik import POLITIK_CELLS, register_all;"
        "assert len(POLITIK_CELLS) == 4; print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "politik_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_four_addresses() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.cells.k2_politik import POLITIK_CELLS;"
        "addrs = sorted([(c.address.L, c.address.F) for c in POLITIK_CELLS]);"
        "expected = sorted([(4, 'F-nu'), (5, 'F-P'), (6, 'F-phi'), (7, 'F-P')]);"
        "assert addrs == expected;"
        "assert all(c.address.D == 'C-Pi' for c in POLITIK_CELLS);"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "four_canonical_addresses",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_C_dispatch_each() -> dict:
    proc = run_python_script('''
        import sys, json
        sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.cell_registry import CellRegistry
        from pipeline.cells import k2_politik as kp
        reg = CellRegistry(); kp.register_all(reg)
        decisions = {}
        for c in kp.POLITIK_CELLS:
            r = reg.dispatch_by_name(c.name, {})
            assert r.error is None, (c.name, r.error)
            decisions[c.name] = r.decision
        print(json.dumps(decisions))
    ''')
    decisions = {}
    if proc.returncode == 0:
        try: decisions = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "dispatch_each_cell",
            "passed": proc.returncode == 0 and len(decisions) == 4 and all(decisions.values()),
            "decisions": decisions}


def gate_D_third_column_in_metabolism() -> dict:
    before = sum(1 for line in METAB_LOG.read_text(encoding="utf-8").splitlines()
                 if line.strip() and '"D":"C-Pi"' in line) if METAB_LOG.exists() else 0
    proc = run_python_script('''
        import sys
        sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.cell_registry import DEFAULT_REGISTRY
        from pipeline.cell_metabolism import install_default_hook
        from pipeline.cells import k2_politik as kp
        kp.register_all(DEFAULT_REGISTRY)
        install_default_hook(DEFAULT_REGISTRY)
        for c in kp.POLITIK_CELLS:
            DEFAULT_REGISTRY.dispatch_by_name(c.name, {})
        print("ok")
    ''')
    after = sum(1 for line in METAB_LOG.read_text(encoding="utf-8").splitlines()
                if line.strip() and '"D":"C-Pi"' in line) if METAB_LOG.exists() else 0
    return {"name": "third_column_in_metabolism",
            "passed": proc.returncode == 0 and (after - before) >= 4,
            "delta": after - before}


def gate_E_digest_sees_third_column() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.digest", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    if proc.returncode != 0:
        return {"name": "digest_sees_third_column", "passed": False}
    body = json.loads(proc.stdout)
    cols = body.get("matrix", {}).get("by_column", {})
    return {"name": "digest_sees_third_column",
            "passed": "C-Pi" in cols, "by_column": cols}


def main() -> int:
    return run_gates_main(
        sprint="politik",
        gate_funcs=[gate_A_politik_imports, gate_B_four_addresses,
                    gate_C_dispatch_each, gate_D_third_column_in_metabolism,
                    gate_E_digest_sees_third_column],
        prior_glob="sprint_digest_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
