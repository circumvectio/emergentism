#!/usr/bin/env python3
"""Sprint 12: Destination + Drive — gate run."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from sprint_gates._common import (
    PROJECT_ROOT, env, run_gates_main, run_python_script, METAB_LOG, SKYZAI_DIR,
)


EXECUTION_LOG_DIR = SKYZAI_DIR / "execution_log"
DRIVE_RECEIPTS_DIR = EXECUTION_LOG_DIR / "drive_receipts"


def _count_k2_route_envelopes() -> int:
    if not EXECUTION_LOG_DIR.exists(): return 0
    return len(list(EXECUTION_LOG_DIR.glob("k2_route_*.json")))


def gate_A_vmosk_imports() -> dict:
    proc = subprocess.run([sys.executable, "-c",
        "import sys; sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents');"
        "from pipeline.vmosk import OrganismVMOSK, VMOSK, collect, match_action;"
        "v = OrganismVMOSK(); assert v.to_dict() == {'organs': {}};"
        "print('ok')"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env())
    return {"name": "vmosk_imports",
            "passed": proc.returncode == 0 and "ok" in proc.stdout,
            "stderr_head": proc.stderr[:200] if proc.returncode != 0 else None}


def gate_B_vmosk_extracts_real_files() -> dict:
    proc = run_python_script('''
        import sys, json
        sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.vmosk import collect
        organism = collect()
        results = {}
        for name, v in organism.organs.items():
            results[name] = {
                "objectives": len(v.objectives),
                "strategies": len(v.strategies),
                "kpis": len(v.kpis),
                "warnings": len(v.parse_warnings),
            }
        # Need >=3 organs with non-empty objectives
        valid = sum(1 for r in results.values() if r["objectives"] > 0)
        print(json.dumps({"valid_organs": valid, "results": results}))
    ''')
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "vmosk_extracts_real_files",
            "passed": proc.returncode == 0 and body.get("valid_organs", 0) >= 3,
            "valid_organs": body.get("valid_organs", 0),
            "results": body.get("results", {}),
            "stderr_head": proc.stderr[:300] if proc.returncode != 0 else None}


def gate_C_router_cell_dispatches() -> dict:
    proc = run_python_script('''
        import sys, json
        sys.path.insert(0, 'SKYZAI_ORG/02_ORGANS/Skyzai/agents')
        from pipeline.cell_registry import CellRegistry
        from pipeline.cell import CellAddress
        from pipeline.cells import router as rt

        reg = CellRegistry()
        rt.register_all(reg)
        # Right address
        assert rt.route_proposer.address == CellAddress(L=7, D="C-Pi", S="Org", F="F-nu")
        # Dispatches without error
        r = reg.dispatch_by_name("route-proposer", {"max_proposals": 5})
        assert r.error is None, r.error
        out = r.output or {}
        proposals = out.get("proposals", [])
        # At minimum produces a no_action proposal even when nothing else fits
        assert len(proposals) >= 1
        # Each proposal has alignment + envelope template
        for p in proposals:
            assert "action_class" in p
            if p["action_class"] != "no_action":
                assert isinstance(p.get("k2_envelope_template"), dict)
        print(json.dumps({"proposal_count": len(proposals),
                          "decision": r.decision,
                          "action_classes": [p["action_class"] for p in proposals]}))
    ''')
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    return {"name": "router_cell_dispatches",
            "passed": proc.returncode == 0 and body.get("proposal_count", 0) >= 1,
            "proposal_count": body.get("proposal_count"),
            "action_classes": body.get("action_classes", []),
            "stderr_head": proc.stderr[:300] if proc.returncode != 0 else None}


def gate_D_drive_allowlist_holds() -> dict:
    """Stage three synthetic envelopes:
       - allowed doc_update with real in-repo target (Pass B will actuate)
       - denied money_move (not in allowlist)
       - escape-attempt doc_update with `..` path (Pass B path-safety must refuse)
    """
    proc = run_python_script('''
        import json, sys
        from pathlib import Path
        sys.path.insert(0, "SKYZAI_ORG/02_ORGANS/Skyzai/agents")
        from pipeline.drive import (
            EXECUTION_LOG_DIR, DRIVE_RECEIPTS_DIR, drive_pass, PROJECT_ROOT,
        )
        EXECUTION_LOG_DIR.mkdir(parents=True, exist_ok=True)

        # Real in-repo target file for the allowed envelope
        target_rel = "02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/memory/test_artifacts/gate_D_target.md"
        target_abs = PROJECT_ROOT / target_rel
        target_abs.parent.mkdir(parents=True, exist_ok=True)
        target_abs.write_text("# Gate D test target\\n\\nInitial content (pre-drive).\\n")
        size_before = target_abs.stat().st_size

        ts = "20260419_gate_D"
        envelopes = {}

        # 1) Allowed: in-repo doc_update
        envelopes["allowed"] = {
            "name": f"k2_route_{ts}_allowed.json",
            "body": {
                "type": "route_proposal",
                "action_class": "doc_update",
                "status": "SIGNED",
                "signed": True,
                "signed_at": "2026-04-19T05:00:00+00:00",
                "timestamp": "2026-04-19T04:50:00+00:00",
                "description": "Gate D test append. This line proves Pass B actuates.",
                "doc_update_target": target_rel,
                "doc_update_strategy": "append-section",
            },
        }
        # 2) Denied: action_class not in allowlist
        envelopes["denied"] = {
            "name": f"k2_route_{ts}_denied.json",
            "body": {
                "type": "route_proposal",
                "action_class": "money_move",
                "status": "SIGNED",
                "signed": True,
                "signed_at": "2026-04-19T05:00:00+00:00",
                "amount_usd": 1000000,
            },
        }
        # 3) Path-escape attempt — Pass B path-safety must refuse
        envelopes["escape"] = {
            "name": f"k2_route_{ts}_escape.json",
            "body": {
                "type": "route_proposal",
                "action_class": "doc_update",
                "status": "SIGNED",
                "signed": True,
                "signed_at": "2026-04-19T05:00:00+00:00",
                "timestamp": "2026-04-19T04:50:00+00:00",
                "description": "Gate D escape attempt — should be refused.",
                "doc_update_target": "../../../../../etc/passwd",
                "doc_update_strategy": "append-section",
            },
        }

        for env in envelopes.values():
            (EXECUTION_LOG_DIR / env["name"]).write_text(json.dumps(env["body"], indent=2))

        try:
            summary = drive_pass(dry_run=False)
            outcomes_by_class = {}
            for r in summary["receipts"]:
                key = (r["envelope_action_class"],
                       "escape" if "escape" in r["envelope_filename"] else
                       "allowed" if "allowed" in r["envelope_filename"] else
                       "denied")
                exec_result = r.get("executor_result") or {}
                outcomes_by_class[key] = (r["outcome"], exec_result.get("error"))
            size_after = target_abs.stat().st_size

            # Verify
            doc_allowed = outcomes_by_class.get(("doc_update", "allowed"))
            money = outcomes_by_class.get(("money_move", "denied"))
            doc_escape = outcomes_by_class.get(("doc_update", "escape"))

            assert doc_allowed and doc_allowed[0] == "executed", doc_allowed
            assert money and money[0] == "out_of_allowlist", money
            assert doc_escape and doc_escape[0] == "executed", doc_escape  # passed allowlist
            # ...but the executor result inside should record the escape refusal
            assert doc_escape[1] and "escape" in doc_escape[1].lower(), doc_escape

            assert size_after > size_before, f"target file did not grow: {size_before} -> {size_after}"

            print(json.dumps({
                "outcomes": {f"{k[0]}/{k[1]}": v[0] for k, v in outcomes_by_class.items()},
                "doc_update_appended_bytes": size_after - size_before,
                "escape_refused_with_error": bool(doc_escape and doc_escape[1]),
            }))
        finally:
            # Cleanup synthetic envelopes + receipts + the test target
            for env in envelopes.values():
                p = EXECUTION_LOG_DIR / env["name"]
                if p.exists(): p.unlink()
                rp = DRIVE_RECEIPTS_DIR / f"drive_receipt_{Path(env['name']).stem}.json"
                if rp.exists(): rp.unlink()
            if target_abs.exists(): target_abs.unlink()
            if target_abs.parent.exists():
                try: target_abs.parent.rmdir()
                except OSError: pass  # not empty, leave it
    ''')
    body = {}
    if proc.returncode == 0:
        try: body = json.loads(proc.stdout)
        except Exception: pass
    outcomes = body.get("outcomes", {})
    return {"name": "drive_allowlist_holds_pass_b",
            "passed": (proc.returncode == 0
                       and outcomes.get("doc_update/allowed") == "executed"
                       and outcomes.get("money_move/denied") == "out_of_allowlist"
                       and body.get("doc_update_appended_bytes", 0) > 0
                       and body.get("escape_refused_with_error") is True),
            "outcomes": outcomes,
            "doc_update_appended_bytes": body.get("doc_update_appended_bytes"),
            "escape_refused": body.get("escape_refused_with_error"),
            "stderr_head": proc.stderr[:400] if proc.returncode != 0 else None}


def gate_E_symbiosis_beat_ends_with_proposal() -> dict:
    """One symbiosis dry-run beat → at least one new k2_route_* envelope appears."""
    before = _count_k2_route_envelopes()
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.symbiosis", "--once", "--dry-run", "--quiet"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, env=env(), timeout=120)
    after = _count_k2_route_envelopes()
    delta = after - before
    return {"name": "symbiosis_beat_ends_with_proposal",
            "passed": proc.returncode == 0 and delta >= 1,
            "exit_code": proc.returncode,
            "k2_route_envelopes_before": before,
            "k2_route_envelopes_after": after,
            "delta": delta}


def main() -> int:
    return run_gates_main(
        sprint="destination_drive",
        gate_funcs=[
            gate_A_vmosk_imports,
            gate_B_vmosk_extracts_real_files,
            gate_C_router_cell_dispatches,
            gate_D_drive_allowlist_holds,
            gate_E_symbiosis_beat_ends_with_proposal,
        ],
        prior_glob="sprint_composer_*.json",
        doctrine_refs=[
            "02_ORGANS/Skyzai/memory/cortex-os/27_WAZE_LENS.md",
            "02_ORGANS/Skyzai/memory/cortex-os/29_BEATING_GOOGLE.md",
            "02_ORGANS/Skyzai/memory/cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md",
        ],
    )


if __name__ == "__main__":
    sys.exit(main())
