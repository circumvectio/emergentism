#!/usr/bin/env python3
"""
cortex_loop.py — wire watchman contradictions into the L1-L7 RosettaChain.

This is Phase A of the "wire everything together and make it run" sequence.
It connects two pieces that already exist but were not talking to each other:

  watchman_run.py  -- emits typed contradiction artifacts  (Cortex OS Doc 07)
  RosettaChain     -- L1-L7 reasoning over RawSignals      (pipeline/agent_chain.py)

The wire:
  1. Optionally refresh contradiction artifacts by running watchman_run.py
  2. Read recent contradiction artifacts from
     02_ORGANS/Skyzai/memory/contradictions/
  3. Filter to those still OPEN (status != "fixed")
  4. Convert each into a RawSignal (content = the contradiction prose, context
     = the full artifact dict, source = "cortex_watchman:<contradiction_id>")
  5. Construct a ChainConfig with rosetta_column="C-K" and z.ai mixed routing
     so the (L, D)-aware refinements from Doc 24 §2.3 take effect end-to-end
  6. Run each signal through RosettaChain.run(signal)
  7. Observe which new K2 envelope(s) the chain staged into the canonical
     execution inbox (Skyzai/execution_log/) so K2 has one place to look
  8. Emit a per-cycle trace artifact recording: contradictions consumed,
     decisions, total tokens, latency

Run:
  python3 EMERGENTISM_ORG/09_TOOLS/cortex_loop.py --dry-run            # plan, no LLM calls
  python3 EMERGENTISM_ORG/09_TOOLS/cortex_loop.py --once               # one full cycle live
  python3 EMERGENTISM_ORG/09_TOOLS/cortex_loop.py --once --limit 1     # one cycle, one artifact
  python3 EMERGENTISM_ORG/09_TOOLS/cortex_loop.py --once --include-fixed   # don't filter status

Doctrine:
  - cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md (agent address scheme)
  - cortex-os/08_RECONCILIATION.md (corrective coherence layer)
  - cortex-os/07_WATCHMEN.md (event-driven reactive coherence layer)
  - cortex-os/19_ROADMAP.md Phase 4 (review packet model)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

# --- Path setup so we can import the Skyzai pipeline ---
_SCRIPTS_DIR = Path(__file__).resolve().parent  # EMERGENTISM_ORG/09_TOOLS/01_SCRIPTS/
_TOOLS_DIR = _SCRIPTS_DIR.parent  # EMERGENTISM_ORG/09_TOOLS/
PROJECT_ROOT = _TOOLS_DIR.parent  # repo root
_AGENTS_DIR = PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "agents"
if str(_AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(_AGENTS_DIR))

from dotenv import load_dotenv  # noqa: E402
from pipeline.cell_metabolism import summarize as summarize_cell_metabolism  # noqa: E402
from pipeline.cell_metabolism import install_default_hook  # noqa: E402
from pipeline.cell_registry import DEFAULT_REGISTRY  # noqa: E402
from pipeline.cell_policies import CHAIN_POLICIES  # noqa: E402
from pipeline.cells import cortex_reconciliation as _reconciliation_cells  # noqa: E402
from pipeline.cells.cortex_reconciliation import (  # noqa: E402
    ROSETTA_COLUMN,
    address_for_contradiction,
    is_authority_sensitive_temporal_artifact,
    policy_name_for_contradiction,
    requires_founder_hold_artifact,
)

_reconciliation_cells.register_all(DEFAULT_REGISTRY)

ENV_PATH = PROJECT_ROOT / ".env"
CONTRADICTION_DIR = (
    PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "memory" / "contradictions"
)
TRACE_DIR = (
    PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "memory" / "cortex_loop_traces"
)
K2_STAGING = (
    PROJECT_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "execution_log"
)
LAST_PROCESSED_PATH = TRACE_DIR / "last_processed.json"
# =========================================================================
# CONTRADICTION INTAKE
# =========================================================================


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_zai_env() -> None:
    """Map z.ai env names onto the OpenAI-compatible names the pipeline uses."""
    if not os.environ.get("OPENAI_API_KEY") and os.environ.get("ZAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = os.environ["ZAI_API_KEY"]
    if not os.environ.get("OPENAI_BASE_URL") and os.environ.get("ZAI_BASE_URL"):
        os.environ["OPENAI_BASE_URL"] = os.environ["ZAI_BASE_URL"]


# =========================================================================
# CACHE — last_processed.json sidecar
# =========================================================================
# Skip re-processing a contradiction whose artifact mtime has not changed
# since the last cycle that processed it. Bypassed via --force.
#
# Schema (keyed on contradiction_id, the unique-per-emission id):
#   {
#     "<contradiction_id>": {
#       "audit_id":        str,   # the C1/C2/... row this came from
#       "artifact_path":   str,   # repo-relative path to the artifact
#       "artifact_mtime":  float, # epoch seconds when we processed it
#       "processed_at":    str,   # ISO timestamp of the processing cycle
#       "policy":          str,   # "bounded_fast" / "deep" / ...
#       "decision":        str,   # canonical_decision (HOLD / EXECUTE / ...)
#       "k2_envelopes":    list,  # filenames staged by that cycle
#     },
#     ...
#   }


def artifact_mtime(art: dict) -> float | None:
    """Return the artifact file's mtime in epoch seconds, or None if unavailable."""
    rel = art.get("__path")
    if not rel:
        return None
    abs_path = PROJECT_ROOT / rel
    try:
        return abs_path.stat().st_mtime
    except OSError:
        return None


def load_last_processed() -> dict[str, dict]:
    """Load the cache; return {} if missing or unparseable."""
    if not LAST_PROCESSED_PATH.exists():
        return {}
    try:
        return json.loads(LAST_PROCESSED_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_last_processed(cache: dict[str, dict]) -> None:
    """Atomically persist the cache."""
    LAST_PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = LAST_PROCESSED_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(LAST_PROCESSED_PATH)


def is_cached(art: dict, cache: dict[str, dict]) -> bool:
    """True iff this artifact was already processed and has not changed since."""
    cid = art.get("contradiction_id")
    if not cid:
        return False
    entry = cache.get(cid)
    if not entry:
        return False
    cached_mtime = entry.get("artifact_mtime")
    current_mtime = artifact_mtime(art)
    if cached_mtime is None or current_mtime is None:
        return False
    # Floating-point compare with a tiny epsilon — filesystems can store
    # mtime at nanosecond precision and JSON round-trips fine.
    return abs(cached_mtime - current_mtime) < 1e-3


def cache_entry_for(art: dict, *, policy: str, decision: str | None,
                    k2_envelopes: list[str]) -> dict:
    """Construct the per-contradiction cache record."""
    return {
        "audit_id": art.get("audit_id"),
        "artifact_path": art.get("__path"),
        "artifact_mtime": artifact_mtime(art),
        "processed_at": now_iso(),
        "policy": policy,
        "decision": decision,
        "k2_envelopes": list(k2_envelopes or []),
    }


def load_contradictions(*, include_fixed: bool, limit: int | None) -> list[dict]:
    """Load contradiction artifacts from disk. Returns a list of dicts.

    Sorted newest-first by contradiction_id (which embeds an ISO timestamp).
    Filters to OPEN (status != "fixed") unless include_fixed is True.
    """
    if not CONTRADICTION_DIR.exists():
        return []
    items: list[dict] = []
    for path in sorted(
        CONTRADICTION_DIR.glob("contradiction_*.json"),
        reverse=True,  # newest-first by sortable timestamped filename
    ):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        body["__path"] = str(path.relative_to(PROJECT_ROOT))
        items.append(body)

    # Deduplicate per audit_id — keep only the newest artifact per audit row,
    # regardless of status. This prevents an older OPEN artifact from surviving
    # after a newer FIXED artifact has already superseded it.
    seen: set[str] = set()
    deduped: list[dict] = []
    for it in items:
        audit_id = it.get("audit_id") or it.get("contradiction_id")
        if audit_id in seen:
            continue
        seen.add(audit_id)
        deduped.append(it)

    if not include_fixed:
        deduped = [it for it in deduped if it.get("status") != "fixed"]

    if limit is not None:
        deduped = deduped[:limit]
    return deduped


def dispatch_contradiction_cell(art: dict):
    """Dispatch the contradiction artifact through the canonical `C-K / Org` cell family."""
    address = address_for_contradiction(str(art.get("contradiction_type") or "structural"))
    result = DEFAULT_REGISTRY.dispatch(address, art)
    return address, result


def contradiction_to_raw_signal(art: dict):
    """Convert a contradiction artifact to a RawSignal for the chain.

    Imports RawSignal lazily so --dry-run works without the pipeline imports.
    """
    from pipeline.schemas import RawSignal

    addr_blocks = art.get("agent_address") or []
    addr_str = ", ".join(
        f"L{a.get('L', '?')}-{a.get('varna', '?')}-{a.get('D', '?')}-{a.get('F', '?')}"
        for a in addr_blocks
    ) or "unknown"
    policy_name = policy_name_for_contradiction(art)
    policy = CHAIN_POLICIES[policy_name]
    authority_sensitive = is_authority_sensitive_temporal_artifact(art)
    founder_hold = requires_founder_hold_artifact(art)

    parts = [
        "CORTEX_OS RECONCILIATION EVENT",
        (
            f"id={art.get('contradiction_id')} audit={art.get('audit_id')} "
            f"type={art.get('contradiction_type')} severity={art.get('severity_initial')} "
            f"auto_repairable={art.get('auto_repairable')}"
        ),
        f"policy={policy_name} mode={policy['mode']} rosetta_column={ROSETTA_COLUMN}",
        f"agent_address={addr_str}",
        f"subject={art.get('subject')}",
        f"claim={art.get('summary')}",
        f"audit_truth={art.get('audit_truth')}",
    ]
    if authority_sensitive:
        parts.append("authority_sensitive=true")
    if founder_hold:
        parts.append("founder_hold_required=true")

    det = art.get("deterministic_check") or {}
    parts.append(
        f"deterministic_found={det.get('found')} corrected_marker={det.get('has_correction_marker')}"
    )

    llm = art.get("llm_judgment") or {}
    if llm and "judgment" in llm:
        j = llm["judgment"]
        parts.append(
            f"prior_llm_severity={j.get('severity')} requires_human={j.get('requires_human')}"
        )
        if j.get("proposed_repair"):
            parts.append(f"proposed_repair={j['proposed_repair']}")

    parts.append(
        "task=Choose exactly one path: AUTO_REPAIR, K2_REVIEW, or HOLD. Apply source-first repair doctrine."
    )
    if founder_hold:
        parts.append(
            "constraint=Direct source rewrite is not yet earned. Treat this as governance-sensitive runtime-priority reinterpretation. HOLD unless explicit founder review authorizes rewrite."
        )

    return RawSignal(
        content="\n".join(parts),
        source=f"cortex_watchman:{art.get('contradiction_id')}",
        timestamp=now_iso(),
        context={
            "policy_name": policy_name,
            "authority_sensitive_temporal": authority_sensitive,
            "founder_hold_required": founder_hold,
            "rosetta_column": ROSETTA_COLUMN,
            "audit_id": art.get("audit_id"),
            "contradiction_id": art.get("contradiction_id"),
            "subject": art.get("subject"),
            "contradiction_type": art.get("contradiction_type"),
            "agent_address": addr_blocks,
            "artifact_path": art.get("__path"),
            "disable_cortex_recall": True,
        },
    )


# =========================================================================
# K2 ENVELOPE OBSERVATION
# =========================================================================


def snapshot_k2_envelopes() -> set[str]:
    """Return the currently staged K2 envelope filenames."""
    if not K2_STAGING.exists():
        return set()
    return {path.name for path in K2_STAGING.glob("k2_*.json")}


def detect_new_k2_envelopes(before: set[str], after: set[str]) -> list[str]:
    """Return newly created K2 envelopes in stable order."""
    return sorted(after - before)


def subject_path_exists(art: dict) -> bool:
    subject = art.get("subject")
    if not subject:
        return False
    return (PROJECT_ROOT / str(subject)).exists()


def maybe_force_bounded_decision(result, art: dict):
    """Reduce variance on low-risk bounded temporal repairs.

    The bounded lane exists because some contradiction classes are already
    highly structured. When the substrate is clear enough, we can make the
    final decision more deterministic instead of letting L4 wobble between
    EXECUTE and HOLD.

    Rules:
    - founder-hold-required cases still HOLD
    - missing source paths HOLD deterministically
    - low-risk stale temporal/lexical/metric contradictions with a real source,
      no correction marker, and no human-required flag EXECUTE deterministically
    """
    from pipeline.schemas import EscalationDecision, PathologyStatus

    contradiction_type = str(art.get("contradiction_type") or "")
    if contradiction_type not in {"temporal", "lexical", "metric"}:
        return result

    det = art.get("deterministic_check") or {}
    judgment = ((art.get("llm_judgment") or {}).get("judgment") or {})
    severity = str(art.get("severity_initial") or "").lower()
    proposed_repair = judgment.get("proposed_repair") or art.get("audit_truth")

    if requires_founder_hold_artifact(art):
        return result

    if not subject_path_exists(art):
        reason = (
            f"Cited source path missing: {art.get('subject')}. "
            "Repair the inventory/source mapping before auto-repair."
        )
        result.l4.action_taken = f"HOLD: {reason}"
        result.l4.chosen_path = "NONE"
        result.l4.execution_result = reason
        result.l4.hold_reason = reason
        result.l4.ruling = "HOLD"
        result.l4.escalation = EscalationDecision.HALT
        result.l4.pathology_status = PathologyStatus.HEALTHY
        result.l4.l4_rationale = reason
        return result

    low_risk_auto = (
        severity == "yellow"
        and bool(det.get("found"))
        and not bool(det.get("has_correction_marker"))
        and (
            judgment.get("requires_human") is False
            or art.get("auto_repairable") is True
        )
    )
    if not low_risk_auto:
        return result

    result.l4.action_taken = (
        f"EXECUTE: Apply source-first repair in {art.get('subject')}: {proposed_repair}"
    )
    result.l4.chosen_path = "auto_repair_source"
    result.l4.execution_result = proposed_repair
    result.l4.hold_reason = ""
    result.l4.ruling = "PROCEED"
    result.l4.escalation = EscalationDecision.PROCEED
    result.l4.pathology_status = PathologyStatus.HEALTHY
    result.l4.l4_rationale = (
        "Deterministic bounded policy: low-risk stale contradiction with direct "
        "source path and no human-required judgment."
    )
    if getattr(result.l4, "confidence_score", 0.0) < 0.85:
        result.l4.confidence_score = 0.85
    return result


def maybe_stage_review_envelope_for_hold(*, policy_name: str, art: dict, result) -> str | None:
    """Stage explicit K2 review packets for deep HOLDs.

    Founder-hold bounded cases already stage envelopes inside the fast path.
    The missing case is judgment-bearing deep HOLDs: authority/structural
    contradictions that currently stop quietly.
    """
    if policy_name != "deep":
        return None
    if getattr(result, "canonical_decision", None) != "HOLD":
        return None

    from pipeline.agent_chain import RosettaChain
    from pipeline.executor import stage_k2_envelope

    hold_reason = getattr(result, "hold_reason", None) or getattr(result, "final_action", "")
    chosen_path = getattr(result, "chosen_path", None)
    if not chosen_path or str(chosen_path).strip().upper() in {"", "NONE", "NULL"}:
        chosen_path = "k2_review"
    return stage_k2_envelope(
        action=(
            "HOLD: Deep review required before rewriting "
            f"{art.get('subject')} for contradiction {art.get('audit_id')}"
        ),
        chosen_path=chosen_path,
        execution_result=hold_reason,
        chain_trace=RosettaChain.trace_to_dict(result),
        action_type="internal_state",
    )


# =========================================================================
# CYCLE TRACE
# =========================================================================


def emit_cycle_trace(stats: dict) -> Path:
    """Write a per-cycle trace artifact."""
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cycle_id = f"cortex_loop_{ts}_{uuid.uuid4().hex[:8]}"
    body = {
        "cycle_id": cycle_id,
        "rosetta_column": ROSETTA_COLUMN,
        "started_at": stats.get("started_at"),
        "finished_at": now_iso(),
        "contradictions_loaded": stats.get("contradictions_loaded", 0),
        "contradictions_processed": stats.get("contradictions_processed", 0),
        "contradictions_skipped_cached": stats.get("contradictions_skipped_cached", 0),
        "k2_staged": stats.get("k2_staged", 0),
        "errors": stats.get("errors", 0),
        "total_latency_ms": stats.get("total_latency_ms", 0),
        "total_tokens": stats.get("total_tokens", {}),
        "per_contradiction": stats.get("per_contradiction", []),
        "doctrine_refs": [
            "02_ORGANS/Skyzai/memory/cortex-os/08_RECONCILIATION.md",
            "02_ORGANS/Skyzai/memory/cortex-os/19_ROADMAP.md",
            "02_ORGANS/Skyzai/memory/cortex-os/24_ROSETTA_MATRIX_AGENT_TEMPLATE.md",
        ],
    }
    out = TRACE_DIR / f"{cycle_id}.json"
    out.write_text(json.dumps(body, indent=2, default=str), encoding="utf-8")
    return out


def load_recent_traces(limit: int = 5) -> list[dict]:
    traces: list[dict] = []
    if not TRACE_DIR.exists():
        return traces
    for path in sorted(TRACE_DIR.glob("cortex_loop_*.json"), reverse=True)[:limit]:
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        body["__file"] = path.name
        traces.append(body)
    return traces


def load_k2_packets(limit: int = 50) -> list[dict]:
    packets: list[dict] = []
    if not K2_STAGING.exists():
        return packets
    for path in sorted(K2_STAGING.glob("k2_*.json"), reverse=True)[:limit]:
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        body["__file"] = path.name
        packets.append(body)
    return packets


def _event_readiness_snapshot(metabolism: dict) -> dict:
    """Return a founder Event Cell readiness snapshot from runtime evidence."""
    stops: list[str] = []
    if metabolism.get("errors", 0) > 0:
        stops.append(f"{metabolism['errors']} cell metabolism errors")
    if metabolism.get("exact_resolution_rate", 1.0) < 0.5:
        stops.append("low_exact_resolution_rate")
    if metabolism.get("pathologies", 0) > 0:
        stops.append(f"{metabolism['pathologies']} pathologies flagged")
    return {
        "ready": len(stops) == 0,
        "stops": stops,
        "blockers": ["venue_not_set", "receiving_account_not_set"],  # human-gated
    }


def build_operator_summary() -> dict:
    open_items = load_contradictions(include_fixed=False, limit=None)
    all_pending_packets = [
        pkt for pkt in load_k2_packets()
        if str(pkt.get("status") or "").upper() in {"PENDING_SIGNATURE", "PENDING_K2_SIGNATURE"}
    ]
    pending_packets = [
        pkt for pkt in all_pending_packets
        if pkt.get("audit_id") or str(pkt.get("dedupe_key") or "").startswith("cortex:")
    ]
    legacy_pending_count = len(all_pending_packets) - len(pending_packets)
    latest_outcomes: dict[str, dict] = {}
    anomalies: list[dict] = []
    for trace in load_recent_traces(limit=12):
        for row in trace.get("per_contradiction", []):
            audit_id = row.get("audit_id")
            if row.get("anomaly_flag") or row.get("pathology"):
                anomalies.append({
                    "audit_id": audit_id,
                    "pathology": row.get("pathology"),
                    "anomaly_flag": row.get("anomaly_flag"),
                })
            if not audit_id or audit_id in latest_outcomes:
                continue
            decision = row.get("canonical_decision") or row.get("cached_decision")
            if decision is None and row.get("would_process"):
                continue
            latest_outcomes[audit_id] = {
                "trace": trace.get("__file"),
                "decision": decision,
                "policy": row.get("policy"),
                "mode": row.get("mode"),
                "success": row.get("success"),
                "chosen_path": row.get("chosen_path"),
                "latency_ms": row.get("latency_ms"),
                "tokens": row.get("tokens"),
                "k2_envelopes": row.get("k2_envelopes", []),
            }
    metabolism = summarize_cell_metabolism()
    return {
        "generated_at": now_iso(),
        "rosetta_column": ROSETTA_COLUMN,
        "open_contradictions": [
            {
                "audit_id": it.get("audit_id"),
                "type": it.get("contradiction_type"),
                "severity": it.get("severity_initial"),
                "policy": policy_name_for_contradiction(it),
                "status": it.get("status", "open"),
                "contradiction_id": it.get("contradiction_id"),
            }
            for it in open_items
        ],
        "pending_k2": [
            {
                "file": pkt.get("__file"),
                "audit_id": pkt.get("audit_id"),
                "status": pkt.get("status"),
                "chosen_path": pkt.get("chosen_path"),
                "subject": pkt.get("subject"),
                "action": pkt.get("action"),
            }
            for pkt in pending_packets
        ],
        "legacy_pending_k2_count": legacy_pending_count,
        "latest_outcomes_by_audit": latest_outcomes,
        "cell_metabolism": metabolism,
        "anomalies_in_recent_traces": anomalies,
        "event_readiness": _event_readiness_snapshot(metabolism),
    }


def run_structured_l3_l4(chain, signal, art: dict):
    """Run a bounded fast path for already-structured contradiction artifacts.

    Temporal/lexical/metric contradictions already arrive with explicit claim,
    audit truth, deterministic check, and prior watchman judgment. Re-paying
    for full L1 direct perception and L2 possibility generation on those
    structured packets is wasteful. This fast lane deterministically seeds
    L1/L2, then spends tokens only on L3/L4 where the actual decision lives.
    """
    from pipeline.schemas import (
        CandidatePath,
        ChainResult,
        EscalationDecision,
        L1Output,
        L2Output,
        PathologyStatus,
    )

    llm = art.get("llm_judgment") or {}
    judgment = llm.get("judgment") or {}
    proposed_repair = judgment.get("proposed_repair") or art.get("audit_truth")
    requires_human = bool(judgment.get("requires_human"))
    founder_hold = requires_founder_hold_artifact(art)
    authority_sensitive = is_authority_sensitive_temporal_artifact(art)
    contradictions = [(art.get("summary") or "", art.get("audit_truth") or "")]

    l1 = L1Output(
        facts=[
            f"claim: {art.get('summary')}",
            f"audit_truth: {art.get('audit_truth')}",
            f"subject: {art.get('subject')}",
            f"deterministic_found: {(art.get('deterministic_check') or {}).get('found')}",
            f"prior_requires_human: {requires_human}",
        ],
        entities=[
            str(art.get("audit_id") or ""),
            str(art.get("subject") or ""),
            str(art.get("contradiction_type") or ""),
        ],
        categories={
            "contradiction_type": [str(art.get("contradiction_type") or "")],
            "subject": [str(art.get("subject") or "")],
            "policy": [str(policy_name_for_contradiction(art))],
        },
        contradictions=contradictions,
        anomalies=[],
        pathology_status=PathologyStatus.HEALTHY,
        pathology_note="Prestructured contradiction artifact; L1 seeded deterministically.",
        escalation=EscalationDecision.PROCEED,
    )

    auto_repair_risk = "medium" if requires_human else "low"
    could_paths = []
    if not authority_sensitive:
        could_paths.append(
            CandidatePath(
                name="auto_repair_source",
                description=(
                    f"Apply the source-first repair directly in {art.get('subject')}: "
                    f"{proposed_repair}"
                ),
                derivation="Direct rewrite path derived from contradiction artifact claim vs audit truth.",
                risk_level=auto_repair_risk,
            )
        )
    could_paths.extend(
        [
            CandidatePath(
                name="k2_founder_review",
                description=(
                    "Stage a founder-review envelope with the contradiction, audit truth, "
                    "and proposed repair for explicit sign-off."
                ),
                derivation=(
                    "Human review path derived from governance-sensitive contradiction handling."
                    if authority_sensitive
                    else "Human review path derived from judgment-bearing contradiction handling."
                ),
                risk_level="low",
            ),
            CandidatePath(
                name="hold_for_more_evidence",
                description=(
                    "Hold the contradiction open until founder review or new evidence changes the source-first truth."
                    if authority_sensitive
                    else "Hold the contradiction open until new evidence changes the source-first truth."
                ),
                derivation=(
                    "Conservative path because rewrite authority is insufficient for this runtime-priority interpretation."
                    if authority_sensitive
                    else "Conservative path when repair authority is insufficient."
                ),
                risk_level="low",
            ),
        ]
    )
    l2 = L2Output(
        could_paths=could_paths,
        analogies_used=[
            (
                "Governance-sensitive temporal drift behaves like a disputed runtime control setting: review or hold before rewrite."
                if authority_sensitive
                else "Temporal doc drift behaves like an outdated ledger entry: either correct it, escalate it, or hold it."
            )
        ],
        state_space_summary=(
            "Structured contradiction review bounded to founder review or hold because the contradiction redefines runtime priority/root cause."
            if authority_sensitive
            else "Structured contradiction review bounded to three actions: repair, K2 review, or hold."
        ),
        pathology_status=PathologyStatus.HEALTHY,
        pathology_note="L2 seeded deterministically from structured contradiction packet.",
        escalation=EscalationDecision.PROCEED,
    )

    result = ChainResult(
        raw_signal=signal,
        l1=l1,
        l2=l2,
        chain_path=["L1*", "L2*"],
        escalation_history=["L1/L2 seeded from structured contradiction artifact"],
    )

    try:
        result.l3 = chain.l3.run(l2)
        result.chain_path.append("L3")
        result.l3.l1_contradictions = list(l1.contradictions)
        result.l3.l1_anomalies = list(l1.anomalies)
        result.l4 = chain.l4.run(result.l3)
        result.chain_path.append("L4")
    except Exception as exc:
        result.terminated_at = result.chain_path[-1] if result.chain_path else "L3"
        result.final_action = f"FAILURE at {result.terminated_at}: {exc}"
        return result

    result.l4 = chain._enforce_hold_criteria(result.l3, result.l4)
    result = maybe_force_bounded_decision(result, art)
    result.terminated_at = "L4"
    if founder_hold and result.l4.escalation == EscalationDecision.PROCEED:
        hold_reason = (
            "Founder review required before rewriting governance-sensitive blocker/root-cause language."
        )
        result.l4.action_taken = f"HOLD: {hold_reason}"
        result.l4.chosen_path = "NONE"
        result.l4.execution_result = hold_reason
        result.l4.hold_reason = hold_reason
        result.l4.ruling = "HOLD"
        result.l4.escalation = EscalationDecision.HALT
        result.l4.pathology_status = PathologyStatus.HEALTHY
        if not result.l4.l4_rationale:
            result.l4.l4_rationale = hold_reason
    if result.l4.escalation == EscalationDecision.HALT:
        result.final_action = f"L4 HOLD: {result.l4.hold_reason}"
        result.success = False
        chain._promote_canonical_fields(result)
        chain._store_memory(result)
        chain._run_witnesses(result)
        if founder_hold:
            from pipeline.executor import stage_k2_envelope
            from pipeline.agent_chain import RosettaChain

            stage_k2_envelope(
                action=(
                    "HOLD: Founder review required before rewriting governance-sensitive "
                    f"runtime narrative in {art.get('subject')}"
                ),
                chosen_path="NONE",
                execution_result=result.l4.hold_reason,
                chain_trace=RosettaChain.trace_to_dict(result),
                action_type="internal_state",
            )
    else:
        result.final_action = result.l4.action_taken
        result.success = result.l4.escalation == EscalationDecision.PROCEED
        chain._promote_canonical_fields(result)
        if result.success:
            chain._on_chain_complete(result)
        else:
            chain._store_memory(result)
    return result


def refresh_watchman(*, audit_id: str | None, no_llm: bool) -> int:
    """Run watchman_run.py to refresh contradiction artifacts before intake."""
    cmd = [sys.executable, str(PROJECT_ROOT / "05_TOOLS" / "watchman_run.py")]
    if audit_id:
        cmd.extend(["--contradiction", audit_id])
    if no_llm:
        cmd.append("--no-llm")
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT)
    return proc.returncode


# =========================================================================
# MAIN
# =========================================================================


def build_chain(policy_name: str):
    """Lazy import + construct a chain for the requested policy."""
    from pipeline.config import ChainConfig, apply_cli_model_selection
    from pipeline.agent_chain import RosettaChain

    policy = CHAIN_POLICIES[policy_name]
    config = ChainConfig()
    apply_cli_model_selection(
        config,
        provider="openai",  # z.ai uses OpenAI-compatible protocol
        zai_mixed=True,
        rosetta_column=ROSETTA_COLUMN,
    )
    if policy["l4_model"]:
        config.l4_model.model = policy["l4_model"]
    if policy["l4_max_tokens"]:
        config.l4_model.max_tokens = policy["l4_max_tokens"]
    return RosettaChain(config), config


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cortex OS reconciliation loop: watchman -> chain -> K2."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single cycle and exit. (Default: dry-run.)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan only — list contradictions that would be processed, do not call the LLM.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N contradictions. (Default: all OPEN.)",
    )
    parser.add_argument(
        "--include-fixed",
        action="store_true",
        help="Include contradictions whose status is 'fixed'. (Default: skip them.)",
    )
    parser.add_argument(
        "--audit-id",
        default=None,
        help="Process only the contradiction with this audit_id (e.g. C2).",
    )
    parser.add_argument(
        "--refresh-watchman",
        action="store_true",
        help="Run watchman_run.py before loading contradiction artifacts.",
    )
    parser.add_argument(
        "--watchman-no-llm",
        action="store_true",
        help="When refreshing watchman, use deterministic-only mode.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Bypass the last_processed cache and re-fire the chain on every contradiction.",
    )
    parser.add_argument(
        "--cache-clear",
        action="store_true",
        help="Delete the last_processed.json cache file before running.",
    )
    parser.add_argument(
        "--cell-summary",
        action="store_true",
        help="Print the current cell metabolism summary after the run.",
    )
    parser.add_argument(
        "--operator-summary",
        action="store_true",
        help="Print the canonical operator summary. If passed alone, exits after summary.",
    )
    args = parser.parse_args()

    if not args.once and not args.dry_run:
        # Default to dry-run when nothing was specified, so a bare invocation
        # is safe and informative.
        args.dry_run = True

    summary_only = (
        args.operator_summary
        and not args.once
        and not args.refresh_watchman
        and args.dry_run
        and args.limit is None
        and not args.audit_id
        and not args.include_fixed
        and not args.force
        and not args.cache_clear
    )
    if summary_only:
        print("=== cortex_loop operator summary ===")
        print(json.dumps(build_operator_summary(), indent=2))
        return 0

    print(f"=== cortex_loop — Cortex OS reconciliation pass ===")
    print(f"started:        {now_iso()}")
    print(f"mode:           {'DRY-RUN (no LLM)' if args.dry_run else 'LIVE (--once)'}")
    print(f"rosetta_column: {ROSETTA_COLUMN}")
    print(f"cell_registry:  {len(DEFAULT_REGISTRY)} registered cells")
    print(f"contradictions: {CONTRADICTION_DIR.relative_to(PROJECT_ROOT)}")
    print(f"k2_staging:     {K2_STAGING.relative_to(PROJECT_ROOT)}")
    print(f"trace_dir:      {TRACE_DIR.relative_to(PROJECT_ROOT)}")
    print()

    if args.refresh_watchman:
        print("[watchman] refreshing contradiction artifacts...")
        rc = refresh_watchman(audit_id=args.audit_id, no_llm=args.watchman_no_llm)
        if rc != 0:
            print(f"FAIL: watchman refresh returned {rc}")
            return rc
        print("[watchman] refresh complete")
        print()

    items = load_contradictions(include_fixed=args.include_fixed, limit=args.limit)
    if args.audit_id:
        items = [it for it in items if it.get("audit_id") == args.audit_id]

    print(f"loaded {len(items)} contradictions to process:")
    for it in items:
        policy_name = policy_name_for_contradiction(it)
        print(
            f"  - {it.get('audit_id'):>4} {it.get('contradiction_type'):>10} "
            f"sev={it.get('severity_initial'):>6} "
            f"status={it.get('status', 'open'):>6} "
            f"policy={policy_name:<12} "
            f"{it.get('contradiction_id')}"
        )
    print()

    # --- Cache: maybe clear, then load ---
    if args.cache_clear and LAST_PROCESSED_PATH.exists():
        LAST_PROCESSED_PATH.unlink()
        print(f"[cache] cleared {LAST_PROCESSED_PATH.relative_to(PROJECT_ROOT)}")
    cache = load_last_processed()
    print(
        f"[cache] {len(cache)} entries in {LAST_PROCESSED_PATH.relative_to(PROJECT_ROOT)} "
        f"(force={args.force})"
    )
    print()

    started_at = now_iso()
    stats: dict = {
        "started_at": started_at,
        "contradictions_loaded": len(items),
        "contradictions_processed": 0,
        "contradictions_skipped_cached": 0,
        "k2_staged": 0,
        "errors": 0,
        "total_latency_ms": 0,
        "total_tokens": {"prompt": 0, "completion": 0, "total": 0},
        "per_contradiction": [],
    }

    if args.dry_run:
        print("[dry-run] not building chain, not calling LLM.")
        for it in items:
            address, cell_result = dispatch_contradiction_cell(it)
            policy_name = (
                cell_result.extra.get("policy_name")
                or policy_name_for_contradiction(it)
            )
            stats["per_contradiction"].append(
                {
                    "audit_id": it.get("audit_id"),
                    "contradiction_id": it.get("contradiction_id"),
                    "would_process": True,
                    "policy": policy_name,
                    "cell_decision": cell_result.decision,
                    "cell_role": cell_result.extra.get("cell_role"),
                    "cell_address": address.to_dict(),
                    "resolved_via": cell_result.extra.get("resolved_via"),
                    "founder_hold_required": cell_result.extra.get("founder_hold_required"),
                }
            )
        trace_path = emit_cycle_trace(stats)
        print(f"trace: {trace_path.relative_to(PROJECT_ROOT)}")
        if args.cell_summary:
            print()
            print("=== cell metabolism summary ===")
            print(json.dumps(summarize_cell_metabolism(), indent=2))
        if args.operator_summary:
            print()
            print("=== operator summary ===")
            print(json.dumps(build_operator_summary(), indent=2))
        return 0

    # --- LIVE PATH ------------------------------------------------------
    if not ENV_PATH.exists():
        print(f"FAIL: .env not found at {ENV_PATH}")
        return 2
    load_dotenv(ENV_PATH)
    normalize_zai_env()
    install_default_hook(DEFAULT_REGISTRY)

    chains: dict[str, tuple[object, object]] = {}

    for it in items:
        audit_id = it.get("audit_id")
        address, cell_result = dispatch_contradiction_cell(it)
        policy_name = (
            cell_result.extra.get("policy_name")
            or policy_name_for_contradiction(it)
        )

        # --- Cache check ---------------------------------------------------
        if not args.force and is_cached(it, cache):
            entry = cache.get(it.get("contradiction_id"), {})
            print(f"--- {audit_id} ({it.get('contradiction_type')}) [cached] ---")
            print(
                f"  cached: decision={entry.get('decision')} "
                f"policy={entry.get('policy')} "
                f"k2={entry.get('k2_envelopes')} "
                f"processed_at={entry.get('processed_at')}"
            )
            stats["contradictions_skipped_cached"] += 1
            stats["per_contradiction"].append({
                "audit_id": audit_id,
                "contradiction_id": it.get("contradiction_id"),
                "policy": policy_name,
                "cached": True,
                "cached_decision": entry.get("decision"),
                "cached_k2_envelopes": entry.get("k2_envelopes"),
                "cached_processed_at": entry.get("processed_at"),
                "cell_decision": cell_result.decision,
                "cell_role": cell_result.extra.get("cell_role"),
                "cell_address": address.to_dict(),
                "resolved_via": cell_result.extra.get("resolved_via"),
            })
            print()
            continue

        if policy_name not in chains:
            try:
                chains[policy_name] = build_chain(policy_name)
            except Exception as exc:
                print(f"FAIL: could not build chain for policy {policy_name}: {exc!r}")
                return 2
            _, config = chains[policy_name]
            print(
                f"chain built [{policy_name}]: rosetta_column={config.rosetta_column} "
                f"L4 model={config.l4_model.model} temp={config.l4_model.temperature}"
            )
        chain, _ = chains[policy_name]
        print(f"--- {audit_id} ({it.get('contradiction_type')}) ---")
        signal = contradiction_to_raw_signal(it)
        t0 = time.perf_counter()
        result = None
        err: str | None = None
        chain.config._usage_totals = {"prompt": 0, "completion": 0, "total": 0}
        before_k2 = snapshot_k2_envelopes()
        try:
            if CHAIN_POLICIES[policy_name]["mode"] == "structured_l3_l4":
                result = run_structured_l3_l4(chain, signal, it)
            elif CHAIN_POLICIES[policy_name]["mode"] == "trivium_only":
                result = chain.run_trivium_only(signal)
            else:
                result = chain.run(signal)
        except Exception as exc:
            err = repr(exc)[:300]
            stats["errors"] += 1
            print(f"  ERROR: {err}")
        if result is not None and err is None:
            maybe_stage_review_envelope_for_hold(
                policy_name=policy_name,
                art=it,
                result=result,
            )
        after_k2 = snapshot_k2_envelopes()
        new_k2 = detect_new_k2_envelopes(before_k2, after_k2)
        latency_ms = round((time.perf_counter() - t0) * 1000, 1)
        stats["total_latency_ms"] += latency_ms

        per: dict = {
            "audit_id": audit_id,
            "contradiction_id": it.get("contradiction_id"),
            "policy": policy_name,
            "cell_decision": cell_result.decision,
            "cell_role": cell_result.extra.get("cell_role"),
            "cell_address": address.to_dict(),
            "resolved_via": cell_result.extra.get("resolved_via"),
            "founder_hold_required": cell_result.extra.get("founder_hold_required"),
            "latency_ms": latency_ms,
            "error": err,
            "cached": False,
        }
        usage_totals = getattr(chain.config, "_usage_totals", None)
        if isinstance(usage_totals, dict):
            for key in ("prompt", "completion", "total"):
                stats["total_tokens"][key] += usage_totals.get(key, 0) or 0
            per["tokens"] = usage_totals

        if result is not None:
            success = getattr(result, "success", False)
            decision = getattr(result, "canonical_decision", None)
            chain_path = getattr(result, "chain_path", None)
            print(f"  chain: success={success} decision={decision} path={chain_path}")
            stats["contradictions_processed"] += 1
            per.update(
                {
                    "mode": CHAIN_POLICIES[policy_name]["mode"],
                    "success": success,
                    "canonical_decision": decision,
                    "chain_path": chain_path,
                    "confidence_score": getattr(result, "confidence_score", None),
                    "chosen_path": getattr(result, "chosen_path", None),
                }
            )

            if new_k2:
                stats["k2_staged"] += len(new_k2)
                per["k2_envelopes"] = new_k2
                print(f"  k2_envelopes: {new_k2}")
            else:
                per["k2_envelopes"] = []

            # --- Cache update on successful processing -------------------
            cid = it.get("contradiction_id")
            if cid and err is None:
                cache[cid] = cache_entry_for(
                    it,
                    policy=policy_name,
                    decision=decision,
                    k2_envelopes=new_k2,
                )

        stats["per_contradiction"].append(per)
        print()

    # Persist cache after the full pass — atomic write.
    try:
        save_last_processed(cache)
    except Exception as exc:
        print(f"[cache] WARN: could not persist cache: {exc!r}")

    print()
    print("=== cortex_loop summary ===")
    print(f"  loaded:      {stats['contradictions_loaded']}")
    print(f"  processed:   {stats['contradictions_processed']}")
    print(f"  cached:      {stats['contradictions_skipped_cached']}")
    print(f"  k2_staged:   {stats['k2_staged']}")
    print(f"  errors:      {stats['errors']}")
    print(f"  latency_ms:  {stats['total_latency_ms']:.1f}")
    print(f"  tokens:      {stats['total_tokens']}")
    trace_path = emit_cycle_trace(stats)
    print(f"  trace:       {trace_path.relative_to(PROJECT_ROOT)}")
    if args.cell_summary:
        print()
        print("=== cell metabolism summary ===")
        print(json.dumps(summarize_cell_metabolism(), indent=2))
    if args.operator_summary:
        print()
        print("=== operator summary ===")
        print(json.dumps(build_operator_summary(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
