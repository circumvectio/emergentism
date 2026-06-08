#!/usr/bin/env python3
"""Sprint 8: Composer — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, COMPOSER_DIR,
)


def gate_A_composer_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.composer import collect, render_markdown, propose_missing_cells, "
        "propose_pseudo_orphans, propose_tissue_candidates, propose_silos;"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "composer_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_composer_quiet_json() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.composer", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    expected_proposals = {"missing_cells", "pseudo_orphans", "tissue_candidates", "silos"}
    return {"name": "composer_quiet_json",
            "passed": (proc.returncode == 0 and body.get("kind") == "composer_report"
                       and expected_proposals <= set(body.get("proposals", {}).keys())),
            "totals": body.get("totals"),
            "proposal_counts": {k: len(v) for k, v in (body.get("proposals") or {}).items()}}


def gate_C_tissue_candidates_found() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.composer", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    if proc.returncode != 0:
        return {"name": "tissue_candidates_found", "passed": False}
    body = json.loads(proc.stdout)
    candidates = body.get("proposals", {}).get("tissue_candidates", [])
    return {"name": "tissue_candidates_found",
            "passed": len(candidates) > 0,
            "candidate_count": len(candidates)}


def gate_D_composer_writes_files() -> dict:
    before = set(p.name for p in COMPOSER_DIR.glob("composer_*")) if COMPOSER_DIR.exists() else set()
    proc = subprocess.run([sys.executable, "-m", "pipeline.composer", "--write", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    after = set(p.name for p in COMPOSER_DIR.glob("composer_*")) if COMPOSER_DIR.exists() else set()
    new = sorted(after - before)
    return {"name": "composer_writes_files",
            "passed": (proc.returncode == 0
                       and any(n.endswith(".json") for n in new)
                       and any(n.endswith(".md") for n in new))}


def gate_E_markdown_renders() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.composer"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    out = proc.stdout or ""
    return {"name": "composer_markdown_renders",
            "passed": (proc.returncode == 0 and "# Composer Report" in out
                       and "## Proposals: missing cells" in out
                       and "## Proposals: tissue candidates" in out)}


def main() -> int:
    return run_gates_main(
        sprint="composer",
        gate_funcs=[gate_A_composer_imports, gate_B_composer_quiet_json,
                    gate_C_tissue_candidates_found, gate_D_composer_writes_files,
                    gate_E_markdown_renders],
        prior_glob="sprint_lineage_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
