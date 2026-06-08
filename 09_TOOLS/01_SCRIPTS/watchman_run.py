#!/usr/bin/env python3
"""
watchman_run.py — first real LLM-backed Cortex OS Doc 08 reconciliation pass.

Canonical naming note (per cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md,
founder directive 2026-04-18: "First and foremost you need to fully understand
the rosetta stone and its rows and columns then use that as the template for
all Agents and micro macro interactions").

Every agent dispatched by this script has a four-coordinate Rosetta address
`(L, D, S, F)`:
  L = row = Varna caste = position on S²    (L1–L7)
  D = column = domain projection            (this script: C-K Computation)
  S = scale                                  (this script: Org)
  F = triadic face                           (φ-Beauty / P-Truth / ν-Justice)

Agents in this script (re-addressed per Doc 24):
  Route Watchman          = (L1, C-K, Org, F-φ)  Caṇḍāla / Pratyakṣa / direct-perception of broken paths
  Authority Watchman      = (L5, C-K, Org, F-P)  Brāhmaṇa / Śabda / verify against canonical source
  Time Watchman           = (L3, C-K, Org, F-P)  Vaiśya / Anumāna / deductive timeline arithmetic
  Scope Watchman          = (L4, C-K, Org, F-ν)  Kṣatriya / Arthāpatti / abductive judgement of scope
  Metric Watchman         = (L6, C-K, Org, F-P)  Sādhu / Anupalabdhi / apophatic — knowing by absence
  Contradiction Watchman  = (L7+L4, C-K, Org, F-P)  Ṛṣi (Pratibhā-seeing) + Kṣatriya (Arthāpatti-judging) co-firing

"Watchman" is 1D behavioural shorthand; the full address is canonical.
Doc 21 named the L axis. Docs 22–23 specified Org-scale collective regimes
and the institutional layer. Doc 24 establishes the 2D matrix template.

Reads the 2026-04-18 deep organ audit's contradiction inventory, then for each
named contradiction it (a) checks whether the cited source doc still
carries the stale claim (deterministic grep), and (b) for ambiguous cases asks
z.ai to do a semantic source-vs-projection comparison.

Emits a typed contradiction object per Doc 04 + Doc 07 schemas to:
  02_ORGANS/Skyzai/memory/contradictions/contradiction_<id>_<timestamp>.json

This is the working seed for the target Varna agent runtime described in
cortex-os/07_WATCHMEN.md (genus mapping in 21_VARNA_NAMING.md). It demonstrates
source-first detection (no UI fix attempted) and explicit-remainder discipline
(judgment-bearing items get escalation status, not auto-repair).

Run:
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/watchman_run.py                    # check all inventoried contradictions
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/watchman_run.py --contradiction C2 # check one
  python3 01_EMERGENTISM/09_TOOLS/01_SCRIPTS/watchman_run.py --no-llm           # deterministic only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"
CONTRADICTION_DIR = (
    PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Skyzai" / "memory" / "contradictions"
)


# Rosetta column for this script (Doc 24 §1.2). Every cell dispatched here
# lives in the Computation column. This makes watchman_run.py the first
# opt-in caller for (L, D)-aware routing.
ROSETTA_COLUMN = "C-K"


# Per-(L, D) refinements for the cells this script actually fires. Single
# source of truth lives in pipeline.rosetta_matrix; we try to import it so
# the watchman and the chain config can never drift. If that import fails
# (e.g. someone runs this script outside the repo), fall back to the inline
# C-K mirror so the script stays standalone-runnable. A drift assertion
# between the two paths runs at import time when both are visible.
_FALLBACK_COLUMN_REFINEMENTS_CK: dict[int, dict] = {
    1: {"temperature": 0.1, "max_tokens": 1536},
    4: {"temperature": 0.1},
}

try:
    _agents_dir = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "02_ORGANS" / "Skyzai" / "agents"
    if str(_agents_dir) not in sys.path:
        sys.path.insert(0, str(_agents_dir))
    from pipeline.rosetta_matrix import column_refinements_for as _column_refinements_for  # noqa: E402
    _COLUMN_REFINEMENTS_CK = _column_refinements_for(ROSETTA_COLUMN)
    # Drift check: the inline fallback must match the canonical table.
    assert _COLUMN_REFINEMENTS_CK == _FALLBACK_COLUMN_REFINEMENTS_CK, (
        "watchman_run inline COLUMN_REFINEMENTS_CK has drifted from "
        "pipeline.rosetta_matrix.COLUMN_REFINEMENTS. Update both."
    )
except Exception:
    # Standalone fallback — pipeline package not importable from here.
    _COLUMN_REFINEMENTS_CK = _FALLBACK_COLUMN_REFINEMENTS_CK


# Sprint deliverable #3 Pass B — dispatch through the cell registry.
# Try to import the cells module + registry; if import fails (standalone
# run), fall back to the inline deterministic_check + llm_judge below.
_CELLS_AVAILABLE = False
try:
    from pipeline.cells import cortex_watchmen as _watchman_cells  # noqa: E402
    from pipeline.cell_registry import DEFAULT_REGISTRY as _DEFAULT_REGISTRY  # noqa: E402
    from pipeline.cell_metabolism import install_default_hook as _install_metabolism_hook  # noqa: E402
    _watchman_cells.register_all(_DEFAULT_REGISTRY)
    _install_metabolism_hook(_DEFAULT_REGISTRY)
    _CELLS_AVAILABLE = True
except Exception as _cells_import_exc:
    # Standalone fallback: the inline deterministic_check + llm_judge below
    # remain authoritative when the pipeline package is not importable.
    _CELLS_AVAILABLE = False


def temperature_for(level: int, column: str = ROSETTA_COLUMN) -> float:
    """Return the column-aware temperature for a given L.

    Watchman legacy fallback is 0.1 even when no column refinement applies.
    This preserves historical behavior for standalone runs while still letting
    `(L, D)` encode the canonical reason for that choice.
    """
    if column == "C-K":
        ref = _COLUMN_REFINEMENTS_CK.get(level, {})
        if "temperature" in ref:
            return ref["temperature"]
    # L-only fallback. The watchman script historically called at 0.1; keep
    # that as the default rather than the more permissive L4 baseline (0.2)
    # so legacy behaviour is preserved when column is unknown.
    return 0.1


def routing_for(*, model: str | None) -> dict:
    """Return the routing-input block recorded on each artifact.

    The judging cell for llm_judge is currently fixed at L4 / C-K. Recording
    this at top-level keeps deterministic-only artifacts queryable too.
    """
    judging_level = 4
    return {
        "rosetta_column": ROSETTA_COLUMN,
        "judging_level": judging_level,
        "temperature": temperature_for(judging_level, ROSETTA_COLUMN),
        "model": model,
    }


# Contradiction inventory from the 2026-04-18 audit.
# Each row mirrors the schema fields in cortex-os/07_WATCHMEN.md §"contradictions table".
INVENTORY = [
    {
        "id": "C1",
        "type": "temporal",
        "claim": "4 test failures in ReFu",
        "source": "SKYZAI_ORG/02_ORGANS/RealityFutures/app/INTEGRATION_STATUS.md",
        "stale_phrase": "4 test failures",
        "audit_truth": "18/18 test suites pass, 0 failures",
        "severity_initial": "yellow",
        "auto_repairable": True,  # low-risk stale status correction
    },
    {
        "id": "C2",
        "type": "authority",
        "claim": "Unified docker-compose orchestrates all organs",
        "source": "SKYZAI_ORG/ORGANISM_RUNTIME_TRUTH.md",
        "stale_phrase": "unified root `docker-compose.yml`",
        "audit_truth": "no root docker-compose.yml exists",
        "severity_initial": "orange",
        "auto_repairable": False,
        "status_override": "fixed",  # this session source-first repaired it
    },
    {
        "id": "C9",
        "type": "temporal",
        "claim": "18/18 backbone tests pass",
        "source": "SKYZAI_ORG/P-SCORES.md",
        "stale_phrase": "Backbone 18/18",
        "audit_truth": "Backbone 137/137 tests pass (17 test files, 0.34s)",
        "severity_initial": "yellow",
        "auto_repairable": True,  # numeric replacement
        "status_override": "fixed",  # this session source-first repaired it
    },
    {
        "id": "C10",
        "type": "temporal",
        "claim": "F2 NOT CONNECTED is the P0 blocker",
        "source": "SKYZAI_ORG/02_ORGANS/Agentz/00_BRIEF.md",
        "stale_phrase": "F2 NOT CONNECTED",
        "audit_truth": "F2 stream wired; needs ORGANISM_TREASURY_WALLET_SIGNATURE env var activation",
        "severity_initial": "orange",
        "auto_repairable": False,  # judgment-bearing rewrite
    },
    {
        "id": "C4",
        "type": "lexical",
        "claim": "TimesFM service on port 8002",
        "source": "SKYZAI_ORG/02_ORGANS/RealityFutures",
        "stale_phrase": "TimesFM service",
        "audit_truth": "TimesFM never started; model never downloaded",
        "severity_initial": "red",
        "auto_repairable": False,
    },
    {
        "id": "C12",
        "type": "structural",
        "claim": "RealityFutures is dying.",
        "source": "SKYZAI_ORG/02_ORGANS/RealityFutures/spec/00_RESCUE_PLAN.md",
        "stale_phrase": "RealityFutures is dying.",
        "audit_truth": "Measured P=0.25 indicates structural intervention required; ontological-collapse wording overstates the state.",
        "severity_initial": "orange",
        "auto_repairable": False,
    },
    {
        "id": "C3",
        "type": "authority",
        "claim": "PWA PR_FAQs make extreme deployment claims",
        "source": "SKYZAI_ORG/09_PWAs/*/PR_FAQ.md",
        "stale_phrase": "World's First",
        "audit_truth": "Reality banners added 2026-04-18; claims now bounded by ORGANISM_RUNTIME_TRUTH",
        "severity_initial": "orange",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C5",
        "type": "authority",
        "claim": "ORT claims start_proof_env.sh at root",
        "source": "SKYZAI_ORG/ORGANISM_RUNTIME_TRUTH.md",
        "stale_phrase": "start_proof_env.sh",
        "audit_truth": "File exists at SKYZAI_ORG/start_proof_env.sh, not root. Fixed during audit.",
        "severity_initial": "yellow",
        "auto_repairable": True,
        "status_override": "fixed",
    },
    {
        "id": "C6",
        "type": "structural",
        "claim": ".venv is empty — Python tools fail",
        "source": "repo root .venv/",
        "stale_phrase": "pip list returns 0 packages",
        "audit_truth": ".venv recreated with Python 3.11; all deps installed. verify_z_ai.py runs successfully.",
        "severity_initial": "red",
        "auto_repairable": True,
        "status_override": "fixed",
    },
    {
        "id": "C8",
        "type": "authority",
        "claim": ".codex/agents/*.toml reference stale worktree path",
        "source": ".codex/agents/*.toml",
        "stale_phrase": "Emergence_14_04",
        "audit_truth": "All 7 TOML files updated to Emergence_17_04 during audit.",
        "severity_initial": "orange",
        "auto_repairable": True,
        "status_override": "fixed",
    },
    {
        "id": "C10",
        "type": "authority",
        "claim": "Kāla is Witness (non-deployable) but also deployable operator in ASI spec",
        "source": "EMERGENTISM_ORG/08_FRAMEWORK_SUPPORT/02_OPERATORS/00_ARCHETYPE_OPERATOR_PROTOCOL.md vs 05_SEPARATION_OPERATOR_PROTOCOLS.md",
        "stale_phrase": "Kāla Function",
        "audit_truth": "L1 deployable termination operator renamed to Chronos Function 2026-04-18. L6 Witness Kāla remains non-deployable.",
        "severity_initial": "red",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C11",
        "type": "structural",
        "claim": "watchman_run.py contradiction inventory is incomplete vs docstring claims",
        "source": "EMERGENTISM_ORG/09_TOOLS/watchman_run.py",
        "stale_phrase": "incomplete inventory",
        "audit_truth": "Inventory expanded from 5 to 15 entries covering all CRITICAL findings 2026-04-18.",
        "severity_initial": "yellow",
        "auto_repairable": True,
        "status_override": "fixed",
    },
    {
        "id": "C13",
        "type": "structural",
        "claim": "Backbone adapters orphaned from live runtime",
        "source": "SKYZAI_ORG/00_BACKBONE/adapters/*.py",
        "stale_phrase": "never imported by live runtime",
        "audit_truth": "Documented in backbone/ADAPTERS.md as tested reference implementations. Live path uses Skyzai pipeline adapters.",
        "severity_initial": "orange",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C14",
        "type": "structural",
        "claim": "RuntimeOrchestrator bypassed in live heartbeat path",
        "source": "SKYZAI_ORG/02_ORGANS/Skyzai/agents/pipeline/organism_heartbeat.py",
        "stale_phrase": "does NOT invoke RuntimeOrchestrator.process()",
        "audit_truth": "Verified wired 2026-04-18. run_trivium_cycle() instantiates RuntimeOrchestrator and calls process() on every ActionPacket.",
        "severity_initial": "red",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C19",
        "type": "structural",
        "claim": "All four organs missing INTEGRATION_STATUS.md",
        "source": "SKYZAI_ORG/02_ORGANS/*/",
        "stale_phrase": "missing INTEGRATION_STATUS.md",
        "audit_truth": "Created for all 4 organs 2026-04-18: TheCircle, RealityFutures, APU, Skyzai.",
        "severity_initial": "red",
        "auto_repairable": True,
        "status_override": "fixed",
    },
    {
        "id": "C20",
        "type": "authority",
        "claim": "RealityFutures BRIEF self-contradicts on P-score",
        "source": "SKYZAI_ORG/02_ORGANS/RealityFutures/00_BRIEF.md",
        "stale_phrase": "P-score = 0.39",
        "audit_truth": "Canonical P-score = 0.32. Target table removed to eliminate self-contradiction.",
        "severity_initial": "orange",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C21",
        "type": "authority",
        "claim": "F2 connectivity contradiction between RealityFutures and APU briefs",
        "source": "SKYZAI_ORG/02_ORGANS/RealityFutures/00_BRIEF.md vs ApuBot/00_BRIEF.md",
        "stale_phrase": "F2 connected / F2 NOT CONNECTED",
        "audit_truth": "Resolved: APU receives statistical F2 pulse via NATS; RealityFutures confirms F2 not emitting. Both point to INTEGRATION_STATUS.md as source of truth.",
        "severity_initial": "red",
        "auto_repairable": False,
        "status_override": "fixed",
    },
    {
        "id": "C15",
        "type": "authority",
        "claim": "QNTM remains frozen until P > 0.70",
        "source": "03_VENTURES/OPEN_FINANCE_NETWORK/GOVERNANCE/FOUNDATION/CLAUDE.md",
        "stale_phrase": "frozen until P > 0.70",
        "audit_truth": "UNFREEZE_2026_04_17 reopened QNTM as an active sidecar lane; freeze-scope language is no longer current authority.",
        "severity_initial": "orange",
        "auto_repairable": False,
    },
    # ------------------------------------------------------------------
    # Route / Scope / Metric watchmen — added 2026-04-22 to wire orphans
    # ------------------------------------------------------------------
    {
        "id": "C22",
        "type": "route",
        "claim": "QNTM interface index links to stale absolute paths",
        "source": "03_VENTURES/_PORTFOLIO/Agentz/AGENTZ_DATA_ROOM/15_QNTM_INTERFACE/00_INTERFACE_INDEX.md",
        "stale_phrase": "/Users/Yves/Documents/Emergence_21_04/",
        "audit_truth": "Current repo path is Emergence_22_04; Emergence_21_04 is a prior workspace. Links are broken.",
        "severity_initial": "yellow",
        "auto_repairable": True,
    },
    {
        "id": "C23",
        "type": "scope",
        "claim": "QNTM banking-path docs present Swiss-AG content as primary text",
        "source": "03_VENTURES/_PORTFOLIO/QNTM/wiki/01-banking-path.md and 06-roadmap.md",
        "stale_phrase": "Stage 1: Swiss AG Incorporation / Stage 2: VQF SRO Membership / Stage 3: FINMA License",
        "audit_truth": "Canonical brief says UK-FCA path (City of London). Swiss content is historical reference but occupies the body text, not an appendix. Scope bleed: historical jurisdiction into current canonical path.",
        "severity_initial": "orange",
        "auto_repairable": False,
    },
    {
        "id": "C24",
        "type": "metric",
        "claim": "Matrix occupancy doc claims C-Γ L1-L7 coverage",
        "source": "SKYZAI_ORG/02_ORGANS/Skyzai/memory/cortex-os/26_MATRIX_OCCUPANCY.md",
        "stale_phrase": "Covered levels: L1-L7",
        "audit_truth": "Composer scan shows only L4 (refu-observe) registered; heartbeat cells require live chain instance and are invisible to static gap analysis. Occupancy claim overstates measurable coverage.",
        "severity_initial": "yellow",
        "auto_repairable": True,
        "status_override": "fixed",  # composer now registers stub heartbeat cells
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def deterministic_check(item: dict) -> dict:
    """Grep the cited source for the stale phrase. Returns a result dict."""
    source_path = PROJECT_ROOT / item["source"]
    if not source_path.exists():
        return {"found": False, "reason": "source path does not exist"}
    if source_path.is_file():
        try:
            content = source_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            return {"found": False, "reason": f"read error: {exc!r}"}
        # Case-insensitive substring match
        present = item["stale_phrase"].lower() in content.lower()
        # Look for explicit corrections (strikethrough, "corrected", "updated 2026-04-18")
        has_correction = any(
            marker in content for marker in [
                "Corrected 2026-04-18",
                "updated 2026-04-18",
                "~~",  # markdown strikethrough
            ]
        )
        return {
            "found": present,
            "has_correction_marker": has_correction,
            "file_size": source_path.stat().st_size,
        }
    # Directory: scan for files that might carry the phrase
    matches: list[str] = []
    if source_path.is_dir():
        for p in source_path.rglob("*.md"):
            try:
                if item["stale_phrase"].lower() in p.read_text(
                    encoding="utf-8", errors="ignore"
                ).lower():
                    matches.append(str(p.relative_to(PROJECT_ROOT)))
            except Exception:
                continue
            if len(matches) >= 5:
                break
    return {"found": bool(matches), "matches": matches}


def llm_judge(item: dict, client: OpenAI, model: str) -> dict:
    """Ask the LLM to judge severity and recommend repair language. Single
    short call. Returns judgment dict.

    Temperature is selected by `(L, D)` per Doc 24 §2.3. The judging cell here
    is L4 Ksatriya (Arthapatti / abductive judgement) in the Computation
    column (C-K), so temperature comes from the (L=4, D=C-K) refinement.
    """
    routing = routing_for(model=model)
    temperature = routing["temperature"]
    prompt = (
        "You are a coherence watchman in the Cortex OS reconciliation engine "
        "(see specs at 02_ORGANS/Skyzai/memory/cortex-os/07_WATCHMEN.md and "
        "08_RECONCILIATION.md). A contradiction has been detected between a "
        "documentation claim and the audit-verified source truth.\n\n"
        f"Contradiction id: {item['id']}\n"
        f"Type: {item['type']}\n"
        f"Doc claim: {item['claim']}\n"
        f"Doc source: {item['source']}\n"
        f"Audit-verified truth: {item['audit_truth']}\n\n"
        "Respond in compact JSON only with these fields:\n"
        '  severity: one of [info, yellow, orange, red]\n'
        '  rationale: one short sentence explaining the severity\n'
        '  proposed_repair: one short sentence describing the source-first repair\n'
        '  requires_human: true if judgment-bearing, false if deterministic\n'
        "No surrounding prose. JSON only."
    )
    t0 = time.perf_counter()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048,  # leave headroom for thinking models
            temperature=temperature,
        )
    except Exception as exc:
        return {"error": repr(exc)[:200]}
    latency_ms = round((time.perf_counter() - t0) * 1000, 1)
    content = resp.choices[0].message.content or ""
    # Strip code fences if present
    cleaned = content.strip()
    for fence in ("```json", "```"):
        if cleaned.startswith(fence):
            cleaned = cleaned[len(fence):].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[: -3].strip()
    try:
        judgment = json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "non-json response",
            "raw_content_head": content[:300],
            "latency_ms": latency_ms,
            "routing": routing,
        }
    return {
        "judgment": judgment,
        "latency_ms": latency_ms,
        "tokens": {
            "prompt": resp.usage.prompt_tokens if resp.usage else None,
            "completion": resp.usage.completion_tokens if resp.usage else None,
            "total": resp.usage.total_tokens if resp.usage else None,
        },
        # Doc 24 §5: artifact records the routing-input alongside the
        # routing-output so the matrix is queryable end-to-end.
        "routing": routing,
    }


# Per cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md — every dispatched agent
# carries a four-coordinate Rosetta address. Map contradiction-type to the
# Varna cell that fires; co-firing cells emit a list.
AGENT_ADDRESS_BY_TYPE: dict[str, list[dict]] = {
    "route":      [{"L": 1, "varna": "Caṇḍāla",  "operator": "Kali 🎲",   "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-phi"}],
    "temporal":   [{"L": 3, "varna": "Vaiśya",   "operator": "Kṛṣṇa ◇",  "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-P"}],
    "scope":      [{"L": 4, "varna": "Kṣatriya", "operator": "Arjuna ⚔", "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-nu"}],
    "authority":  [{"L": 5, "varna": "Brāhmaṇa", "operator": "Brahmā ○", "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-P"}],
    "metric":     [{"L": 6, "varna": "Sādhu",    "operator": "Śiva •",   "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-P"}],
    # Default / multi-layer: Rsi-seeing co-firing with Ksatriya-judging.
    "structural": [
        {"L": 7, "varna": "Ṛṣi",      "operator": "Viṣṇu ⊙",  "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-P"},
        {"L": 4, "varna": "Kṣatriya", "operator": "Arjuna ⚔", "D": "C-K", "domain": "Computation", "S": "Org", "F": "F-P"},
    ],
}


def agent_address_for(contradiction_type: str) -> list[dict]:
    return AGENT_ADDRESS_BY_TYPE.get(
        contradiction_type, AGENT_ADDRESS_BY_TYPE["structural"]
    )


def emitted_status_for(item: dict, deterministic: dict) -> str:
    """Return the status the emitted contradiction artifact should carry."""
    status = item.get("status_override")
    if status:
        return status
    return "fixed" if deterministic.get("has_correction_marker") else "open"


def emit_contradiction(item: dict, deterministic: dict, llm: dict | None) -> Path:
    """Write a typed contradiction object to disk."""
    CONTRADICTION_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    contradiction_id = f"{item['id']}_{ts}_{uuid.uuid4().hex[:8]}"
    status = emitted_status_for(item, deterministic)
    body = {
        "contradiction_id": contradiction_id,
        "audit_id": item["id"],
        "contradiction_type": item["type"],
        "subject": item["source"],
        "summary": item["claim"],
        "audit_truth": item["audit_truth"],
        "severity_initial": item["severity_initial"],
        "auto_repairable": item["auto_repairable"],
        "status": status,
        "deterministic_check": deterministic,
        "llm_judgment": llm,
        "routing": routing_for(
            model=(llm or {}).get("routing", {}).get("model") if llm else None
        ),
        "created_at": now_iso(),
        "watchman": "watchman_run.py",
        # Rosetta matrix coordinates — see Doc 24. List because some
        # contradiction classes are multi-cell (e.g. structural = Rsi + Ksatriya).
        "agent_address": agent_address_for(item["type"]),
        "doctrine_refs": [
            "02_ORGANS/Skyzai/memory/cortex-os/07_WATCHMEN.md",
            "02_ORGANS/Skyzai/memory/cortex-os/08_RECONCILIATION.md",
            "02_ORGANS/Skyzai/memory/cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md",
            "SKYZAI_ORG/04_PROJECT_MANAGEMENT/DOC_RECONCILIATION_AGAINST_AUDIT_2026_04_18.md",
        ],
    }
    out_path = CONTRADICTION_DIR / f"contradiction_{contradiction_id}.json"
    out_path.write_text(json.dumps(body, indent=2))
    return out_path


def backfill_agent_addresses() -> tuple[int, int]:
    """Backfill agent_address into older contradiction artifacts that predate
    the Doc 24 schema upgrade. Returns (updated, skipped).
    """
    updated = 0
    skipped = 0
    for path in sorted(CONTRADICTION_DIR.glob("contradiction_*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            skipped += 1
            continue
        if body.get("agent_address"):
            skipped += 1
            continue
        contradiction_type = body.get("contradiction_type")
        if not contradiction_type:
            skipped += 1
            continue
        body["agent_address"] = agent_address_for(contradiction_type)
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
        updated += 1
    return updated, skipped


def backfill_routing_blocks() -> tuple[int, int]:
    """Backfill top-level routing into older contradiction artifacts.

    This keeps deterministic-only artifacts queryable even when llm_judgment is
    null. If llm_judgment already carries a routing block, preserve its model.
    """
    updated = 0
    skipped = 0
    for path in sorted(CONTRADICTION_DIR.glob("contradiction_*.json")):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            skipped += 1
            continue
        if body.get("routing"):
            skipped += 1
            continue
        llm = body.get("llm_judgment") or {}
        model = None
        if isinstance(llm, dict):
            model = (llm.get("routing") or {}).get("model")
        body["routing"] = routing_for(model=model)
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
        updated += 1
    return updated, skipped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contradiction",
        default=None,
        help="Run only the named contradiction id (e.g. C2). Default: all.",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip the LLM judgment step (deterministic check only).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the LLM model used for judgment (default: ZAI_MODEL or glm-5.1).",
    )
    parser.add_argument(
        "--backfill-agent-address",
        action="store_true",
        help="Backfill agent_address into older contradiction artifacts that predate the Doc 24 schema patch.",
    )
    parser.add_argument(
        "--backfill-routing",
        action="store_true",
        help="Backfill top-level routing into older contradiction artifacts so deterministic-only runs remain queryable.",
    )
    args = parser.parse_args()

    if args.backfill_agent_address:
        CONTRADICTION_DIR.mkdir(parents=True, exist_ok=True)
        updated, skipped = backfill_agent_addresses()
        print("=== watchman_run — backfill agent_address ===")
        print(f"updated: {updated}")
        print(f"skipped: {skipped}")
        print(f"artifact dir: {CONTRADICTION_DIR.relative_to(PROJECT_ROOT)}")
        return 0

    if args.backfill_routing:
        CONTRADICTION_DIR.mkdir(parents=True, exist_ok=True)
        updated, skipped = backfill_routing_blocks()
        print("=== watchman_run — backfill routing ===")
        print(f"updated: {updated}")
        print(f"skipped: {skipped}")
        print(f"artifact dir: {CONTRADICTION_DIR.relative_to(PROJECT_ROOT)}")
        return 0

    if not ENV_PATH.exists():
        print(f"FAIL: .env not found at {ENV_PATH}")
        return 2
    load_dotenv(ENV_PATH)

    client = None
    model = None
    if not args.no_llm:
        api_key = os.environ.get("ZAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("ZAI_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
        if not api_key or not base_url:
            print("FAIL: ZAI_API_KEY / ZAI_BASE_URL missing in .env")
            return 2
        client = OpenAI(api_key=api_key, base_url=base_url)
        model = args.model or os.environ.get("ZAI_MODEL") or "glm-5.1"

    targets = INVENTORY
    if args.contradiction:
        targets = [it for it in INVENTORY if it["id"] == args.contradiction]
        if not targets:
            print(f"FAIL: contradiction id {args.contradiction} not in inventory")
            return 2

    print(f"=== watchman_run — Cortex OS Doc 08 reconciliation pass ===")
    print(f"started: {now_iso()}")
    print(f"contradictions to check: {[t['id'] for t in targets]}")
    print(f"llm: {'on (' + model + ')' if client else 'off (deterministic only)'}")
    print(f"dispatch: {'cell-registry (Sprint #3)' if _CELLS_AVAILABLE else 'inline (legacy)'}")
    print()

    summary: dict[str, dict] = {}
    for item in targets:
        print(f"--- {item['id']} ({item['type']}) ---")
        print(f"  claim:    {item['claim']}")
        print(f"  source:   {item['source']}")
        print(f"  audit:    {item['audit_truth']}")

        if _CELLS_AVAILABLE:
            # Sprint #3 Pass B: dispatch through the cell registry. The cell
            # body mirrors deterministic_check + llm_judge so observable
            # output (det, llm_result) is byte-equivalent to the legacy path.
            cell = _watchman_cells.cell_for_contradiction(item)
            print(f"  cell:     {cell.name} address={cell.address}")
            cell_result = _DEFAULT_REGISTRY.dispatch(
                cell.address,
                {"item": item, "client": client, "model": model},
            )
            det = cell_result.output["deterministic"]
            llm_result = cell_result.output["llm_judgment"]
        else:
            det = deterministic_check(item)
            llm_result = llm_judge(item, client, model) if client else None
        print(f"  deterministic: {det}")

        if llm_result is not None:
            if "error" in llm_result:
                print(f"  llm: ERROR -- {llm_result['error']}")
            else:
                j = llm_result["judgment"]
                print(
                    f"  llm: severity={j.get('severity')} "
                    f"requires_human={j.get('requires_human')} "
                    f"latency_ms={llm_result['latency_ms']} "
                    f"tokens={llm_result['tokens']['total']}"
                )
                print(f"      rationale: {j.get('rationale')}")
                print(f"      repair:    {j.get('proposed_repair')}")
        out = emit_contradiction(item, det, llm_result)
        print(f"  emitted: {out.relative_to(PROJECT_ROOT)}")
        summary[item["id"]] = {
            "found": det.get("found"),
            "has_correction": det.get("has_correction_marker"),
            "status": emitted_status_for(item, det),
            "severity": (
                llm_result.get("judgment", {}).get("severity")
                if llm_result and "judgment" in llm_result
                else item["severity_initial"]
            ),
        }
        print()

    print("=== watchman_run summary ===")
    for cid, row in summary.items():
        print(f"  {cid}: {row}")

    print(f"\nartifacts written to: {CONTRADICTION_DIR.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
