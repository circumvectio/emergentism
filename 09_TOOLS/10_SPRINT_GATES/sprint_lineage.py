#!/usr/bin/env python3
"""Sprint 7: Lineage — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, DIGEST_DIR, LINEAGE_DIR,
)


def gate_A_lineage_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.lineage import diff_digests, render_markdown;"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "lineage_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_lineage_default() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.lineage"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    out = proc.stdout or ""
    return {"name": "lineage_default_two_digests",
            "passed": (proc.returncode == 0 and "# Organism Lineage" in out
                       and "## Matrix Δ" in out and "## K2 inbox Δ" in out)}


def gate_C_lineage_quiet_json() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.lineage", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "lineage_quiet_json",
            "passed": (proc.returncode == 0 and body.get("kind") == "lineage_diff"
                       and "matrix" in body and "k2_inbox" in body and "witness" in body)}


def gate_D_lineage_writes_files() -> dict:
    before = set(p.name for p in LINEAGE_DIR.glob("lineage_*")) if LINEAGE_DIR.exists() else set()
    proc = subprocess.run([sys.executable, "-m", "pipeline.lineage", "--write", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    after = set(p.name for p in LINEAGE_DIR.glob("lineage_*")) if LINEAGE_DIR.exists() else set()
    new = sorted(after - before)
    return {"name": "lineage_writes_files",
            "passed": (proc.returncode == 0
                       and any(n.endswith(".json") for n in new)
                       and any(n.endswith(".md") for n in new))}


def gate_E_lineage_explicit_diff() -> dict:
    if not DIGEST_DIR.exists():
        return {"name": "lineage_explicit_diff", "passed": False}
    cands = sorted(DIGEST_DIR.glob("digest_*.json"), reverse=True)
    if len(cands) < 2:
        return {"name": "lineage_explicit_diff", "passed": False}
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.lineage",
         "--before", cands[1].stem, "--after", cands[0].stem, "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=60)
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "lineage_explicit_diff",
            "passed": proc.returncode == 0 and body.get("kind") == "lineage_diff"}


def main() -> int:
    # Self-contained: write a fresh digest first so we always have ≥2 to diff
    subprocess.run([sys.executable, "-m", "pipeline.digest", "--write", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    return run_gates_main(
        sprint="lineage",
        gate_funcs=[gate_A_lineage_imports, gate_B_lineage_default,
                    gate_C_lineage_quiet_json, gate_D_lineage_writes_files,
                    gate_E_lineage_explicit_diff],
        prior_glob="sprint_politik_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
