#!/usr/bin/env python3
"""
assemble_gonogo_packet.py — Sprint VI Go/No-Go packet assembler.

Reads exact runtime evidence (cell metabolism, K2 state, business events,
operator notes) and produces one explicit Go/No-Go packet for the founder
Event Cell loop.

Usage:
    python3 assemble_gonogo_packet.py \
        --event-name "Skyzai Founder Briefing" \
        --event-date "2026-04-30" \
        --venue "TBD" \
        --price "CHF 29" \
        --capacity 12 \
        --receiving-account "TBD" \
        --mode dry_run

Output:
    A JSON file at proof_packets/gonogo_<timestamp>.json plus a human-readable
    markdown summary at proof_packets/gonogo_<timestamp>.md.

Constitutional rule: this script only assembles what exists. It does not
invent evidence. If a required field is missing, the packet is automatically
    NO-GO with the blocker named.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Allow running from repo root or from scripts/ dir
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent
_AGENTS_DIR = _REPO_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "agents"
sys.path.insert(0, str(_AGENTS_DIR))

from pipeline.cell_metabolism import summarize as summarize_cell_metabolism
from pipeline.schemas import ProofLoopTrace


PROOF_PACKET_DIR = _REPO_ROOT / "02_ORGANISM" / "02_ORGANS" / "Skyzai" / "memory" / "proof_packets"


def _load_k2_state() -> dict[str, Any]:
    """Best-effort K2 state snapshot."""
    try:
        from pipeline.cell_witness import load_k2_packets
        packets = load_k2_packets()
        pending = [p for p in packets if str(p.get("status") or "").upper() in {"PENDING_SIGNATURE", "PENDING_K2_SIGNATURE"}]
        return {
            "total_staged": len(packets),
            "pending_signature": len(pending),
            "superseded": len([p for p in packets if str(p.get("status") or "").upper() == "SUPERSEDED"]),
        }
    except Exception as exc:
        return {"error": str(exc)}


def _load_anomalies() -> list[dict]:
    """Best-effort anomaly snapshot from recent traces."""
    try:
        from pipeline.cell_witness import load_recent_traces
        anomalies: list[dict] = []
        for trace in load_recent_traces(limit=6):
            for row in trace.get("per_contradiction", []):
                if row.get("anomaly_flag") or row.get("pathology"):
                    anomalies.append({
                        "audit_id": row.get("audit_id"),
                        "pathology": row.get("pathology"),
                        "anomaly_flag": row.get("anomaly_flag"),
                    })
        return anomalies
    except Exception:
        return []


def assemble_packet(
    *,
    event_name: str,
    event_date: str,
    venue: str,
    price: str,
    capacity: int,
    receiving_account: str,
    mode: str = "dry_run",
    operator_notes: str = "",
) -> ProofLoopTrace:
    trace_id = f"gonogo-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    metabolism = summarize_cell_metabolism()
    k2_state = _load_k2_state()
    anomalies = _load_anomalies()

    total_dispatches = metabolism.get("total_dispatches", 0)
    hold_count = metabolism.get("by_decision", {}).get("HOLD", 0)
    hold_ratio = round(hold_count / total_dispatches, 4) if total_dispatches else 0.0

    # Auto-detect blockers from missing required fields
    blockers: list[str] = []
    if not venue or venue.upper() == "TBD":
        blockers.append("venue_not_set")
    if not receiving_account or receiving_account.upper() == "TBD":
        blockers.append("receiving_account_not_set")
    if not event_date:
        blockers.append("event_date_not_set")
    if mode == "live" and blockers:
        blockers.append("live_mode_with_missing_params")

    # Auto-detect stop conditions from runtime state
    stops: list[str] = []
    if k2_state.get("pending_signature", 0) > 5:
        stops.append("excessive_pending_k2_packets")
    if anomalies:
        stops.append(f"{len(anomalies)} unresolved anomalies in recent traces")
    if metabolism.get("errors", 0) > 0:
        stops.append(f"{metabolism['errors']} cell metabolism errors")
    if metabolism.get("exact_resolution_rate", 1.0) < 0.5:
        stops.append("low_exact_resolution_rate")

    # Determine outcome
    if blockers:
        outcome = "no_go"
    elif stops:
        outcome = "held"
    else:
        outcome = "green_light"

    return ProofLoopTrace(
        trace_id=trace_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        loop_type="founder_event",
        mode=mode,
        event_name=event_name,
        event_date=event_date,
        venue=venue,
        price=price,
        capacity=capacity,
        receiving_account=receiving_account,
        business_events_emitted=[],
        anomalies_detected=anomalies,
        manual_interventions=[],
        missing_emits=[],
        cell_metabolism_summary=metabolism,
        exact_resolution_rate=metabolism.get("exact_resolution_rate", 0.0),
        hold_ratio=hold_ratio,
        total_tokens=metabolism.get("total_tokens", 0),
        k2_packets_staged=k2_state.get("total_staged", 0),
        k2_packets_signed=k2_state.get("total_staged", 0) - k2_state.get("pending_signature", 0),
        k2_packets_superseded=k2_state.get("superseded", 0),
        operator_notes=operator_notes,
        stop_conditions_triggered=stops,
        green_light_blockers=blockers,
        outcome=outcome,
        evidence_refs=[],
    )


def _render_markdown(trace: ProofLoopTrace) -> str:
    lines = [
        f"# Go/No-Go Packet — {trace.trace_id}",
        "",
        f"**Generated:** {trace.generated_at}",
        f"**Mode:** {trace.mode}",
        f"**Outcome:** `{trace.outcome}`",
        "",
        "## Event Parameters",
        f"- **Name:** {trace.event_name}",
        f"- **Date:** {trace.event_date}",
        f"- **Venue:** {trace.venue}",
        f"- **Price:** {trace.price}",
        f"- **Capacity:** {trace.capacity}",
        f"- **Receiving Account:** {trace.receiving_account}",
        "",
        "## Runtime Evidence",
        f"- **Total Cell Dispatches:** {trace.cell_metabolism_summary.get('total_dispatches', 0)}",
        f"- **Exact Resolution Rate:** {trace.exact_resolution_rate}",
        f"- **Hold Ratio:** {trace.hold_ratio}",
        f"- **Total Tokens:** {trace.total_tokens}",
        f"- **K2 Staged:** {trace.k2_packets_staged} | **Signed:** {trace.k2_packets_signed} | **Superseded:** {trace.k2_packets_superseded}",
        "",
        "## Anomalies",
    ]
    if trace.anomalies_detected:
        for a in trace.anomalies_detected:
            lines.append(f"- `{a.get('audit_id', '?')}` — {a.get('pathology', a.get('anomaly_flag', 'unknown'))}")
    else:
        lines.append("- None detected")
    lines.extend(["", "## Stop Conditions"])
    if trace.stop_conditions_triggered:
        for s in trace.stop_conditions_triggered:
            lines.append(f"- ⚠️ {s}")
    else:
        lines.append("- None")
    lines.extend(["", "## Green-Light Blockers"])
    if trace.green_light_blockers:
        for b in trace.green_light_blockers:
            lines.append(f"- 🚫 {b}")
    else:
        lines.append("- None")
    lines.extend(["", "## Operator Notes", trace.operator_notes or "(none)", ""])
    lines.append("---")
    lines.append("*Assembled by assemble_gonogo_packet.py — Sprint VI Cell Membrane and Homeostasis*")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Assemble a Go/No-Go packet for the founder Event Cell loop.")
    parser.add_argument("--event-name", default="Skyzai Founder Briefing")
    parser.add_argument("--event-date", default="2026-04-30")
    parser.add_argument("--venue", default="TBD")
    parser.add_argument("--price", default="CHF 29")
    parser.add_argument("--capacity", type=int, default=12)
    parser.add_argument("--receiving-account", default="TBD")
    parser.add_argument("--mode", default="dry_run", choices=["dry_run", "rehearsal", "live"])
    parser.add_argument("--operator-notes", default="")
    parser.add_argument("--out-dir", default=str(PROOF_PACKET_DIR))
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    trace = assemble_packet(
        event_name=args.event_name,
        event_date=args.event_date,
        venue=args.venue,
        price=args.price,
        capacity=args.capacity,
        receiving_account=args.receiving_account,
        mode=args.mode,
        operator_notes=args.operator_notes,
    )

    base_name = trace.trace_id
    json_path = out_dir / f"{base_name}.json"
    md_path = out_dir / f"{base_name}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(asdict(trace), f, indent=2, default=str)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(_render_markdown(trace))

    print(f"✅ Go/No-Go packet assembled: {trace.outcome}")
    print(f"   JSON: {json_path}")
    print(f"   MD:   {md_path}")
    return 0 if trace.outcome == "green_light" else 1


if __name__ == "__main__":
    sys.exit(main())
