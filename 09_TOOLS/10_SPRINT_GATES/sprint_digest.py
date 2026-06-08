#!/usr/bin/env python3
"""Sprint 5: Digest — gate run."""
from __future__ import annotations
import json, subprocess, sys
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, DIGEST_DIR,
)


def gate_A_digest_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.digest import collect, render_markdown, parse_window;"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "digest_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def gate_B_digest_quiet_json() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.digest", "--since", "30d", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "digest_quiet_json",
            "passed": (proc.returncode == 0 and body.get("kind") == "organism_digest"
                       and "matrix" in body and "k2_inbox" in body and "witness" in body),
            "matrix_dispatches": body.get("matrix", {}).get("total_dispatches"),
            "k2_pending": body.get("k2_inbox", {}).get("pending_count"),
            "witness_findings": body.get("witness", {}).get("findings_count")}


def gate_C_digest_markdown_renders() -> dict:
    proc = subprocess.run([sys.executable, "-m", "pipeline.digest", "--since", "30d"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    out = proc.stdout or ""
    return {"name": "digest_markdown_renders",
            "passed": (proc.returncode == 0 and "# Organism Digest" in out
                       and "## Matrix" in out and "## K2 inbox" in out
                       and "## Witness findings" in out)}


def gate_D_digest_writes_file() -> dict:
    before = set(p.name for p in DIGEST_DIR.glob("digest_*")) if DIGEST_DIR.exists() else set()
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.digest", "--since", "30d", "--write", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    after = set(p.name for p in DIGEST_DIR.glob("digest_*")) if DIGEST_DIR.exists() else set()
    new = sorted(after - before)
    return {"name": "digest_writes_file",
            "passed": (proc.returncode == 0
                       and any(n.endswith(".json") for n in new)
                       and any(n.endswith(".md") for n in new)),
            "new_files": new}


def gate_E_digest_collect_real_data() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.digest import collect; d = collect();"
        "assert d['kind'] == 'organism_digest';"
        "assert isinstance(d['matrix']['total_dispatches'], int);"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "digest_collect_real_data",
            "passed": proc.returncode == 0 and "ok" in proc.stdout}


def main() -> int:
    return run_gates_main(
        sprint="digest",
        gate_funcs=[gate_A_digest_imports, gate_B_digest_quiet_json,
                    gate_C_digest_markdown_renders, gate_D_digest_writes_file,
                    gate_E_digest_collect_real_data],
        prior_glob="sprint_receipts_*.json",
    )


if __name__ == "__main__":
    sys.exit(main())
