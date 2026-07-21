#!/usr/bin/env python3
"""
generate_g4_traces.py — Sprint 1 carryover G4: clean HOLD + EXECUTE backbone traces.

Generates two discriminated traces through the unified packetized backbone,
using the canonical adapter layer (same path as test_backbone_demo_flow.py).

Output:
  02_SKYZAI/01_NOOSPHERE/02_ORGANS/Skyzai/memory/backbone_traces/
    backbone_trace_EXECUTE_<ts>_<id>.json
    backbone_trace_HOLD_<ts>_<id>.json

Each file contains:
  - trace_id, decision, closure_reason
  - validation summary (has_signal, has_probability, has_action, has_receipt, valid_minimum)
  - vitals snapshot (packets_published, decisions, hold_ratio)
  - packets array (serialized Signal → Probability → Context → Action → Receipt/HOLD)
"""

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure backbone is on path when run from repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKBONE_DIR = PROJECT_ROOT / "03_VENTURES" / "SKYZAI" / "01_NOOSPHERE" / "00_BACKBONE"
sys.path.insert(0, str(BACKBONE_DIR))

from adapters.circle_adapter import CircleAdapter
from adapters.realityfutures_adapter import RealityFuturesAdapter
from adapters.apu_adapter import APUAdapter
from adapters.ofn_adapter import OFNAdapter
from adapters.nexus_adapter import NexusAdapter
from services.trace_graph import InMemoryTraceGraph
from services.subject_resolver import SubjectResolver
from services.witness_engine import WitnessEngine
from services.vitals import BackboneVitals


OUTPUT_DIR = (
    PROJECT_ROOT
    / "03_VENTURES"
    / "SKYZAI"
    / "01_NOOSPHERE"
    / "02_ORGANS"
    / "Skyzai"
    / "memory"
    / "backbone_traces"
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _serialize_trace(graph: InMemoryTraceGraph, trace_id: str, vitals: BackboneVitals) -> dict:
    """Build a JSON-serializable dict from an InMemoryTraceGraph trace."""
    summary = graph.validate_trace(trace_id)
    trace_record = graph.get_trace(trace_id)

    packets_serializable: list[dict] = []
    for pid in trace_record.packet_ids:
        pkt = graph._packets.get(pid)
        if pkt is not None:
            packets_serializable.append(json.loads(pkt.model_dump_json()))

    return {
        "meta": {
            "generated_at": _now_iso(),
            "generator": "generate_g4_traces.py",
            "sprint_carryover": "G4",
            "trace_id": trace_id,
            "closure_reason": trace_record.closure_reason,
            "closure_decision": trace_record.closure_decision,
        },
        "validation": summary,
        "vitals": {
            "packets_published": vitals.packets_published,
            "decisions": dict(vitals.decisions),
            "hold_ratio": vitals.hold_ratio,
        },
        "packets": packets_serializable,
    }


def generate_execute_trace() -> Path:
    """Clean EXECUTE trace: strong signal, strong pricing, trading allowed, receipt closed."""
    subject_id = "nexus:g4_execute"
    circle = CircleAdapter()
    rf = RealityFuturesAdapter()
    apu = APUAdapter()
    ofn = OFNAdapter()
    nexus = NexusAdapter()
    graph = InMemoryTraceGraph()
    resolver = SubjectResolver()
    vitals = BackboneVitals()

    # F0 — Context (trading allowed)
    ctx = nexus.to_context_packet(
        subject_id=subject_id,
        subject_type="person",
        can_trade=True,
        max_order_usdc=500.0,
        usdc_available=2000.0,
        risk_profile="moderate",
        domains_of_interest=["macro", "crypto"],
    )
    resolver.register_context(ctx)
    vitals.record_packet("ContextPacket")

    # F1 — Signal (strong, credible)
    signal = circle.to_signal_packet(
        subject_id=subject_id,
        subject_type="person",
        signal_id="sig_g4_exec_001",
        source_name="reuters",
        source_type="rss",
        source_credibility=0.9,
        domain="macro",
        signal_type="policy",
        urgency=0.8,
        novelty=0.4,
        facts=["Fed signals rate pause", "Markets rally on dovish tone"],
        claims=[{"text": "Rate cut likely in Q3", "confidence": 0.65}],
        tags=["fed", "rates", "macro"],
        cycle_id="cycle_g4_sprint1",
    )
    graph.append(signal)
    vitals.record_packet("SignalPacket")

    # F2 — Probability (tight spread, high confidence)
    prob = rf.to_probability_packet(
        signal_packet=signal,
        market_id="rf_g4_exec_001",
        question="Will the Fed cut rates by July?",
        base_probability=0.74,
        spread=0.09,
        volatility=0.18,
        confidence_in_price=0.78,
        branches=[
            {"label": "cut_25bp", "probability": 0.55},
            {"label": "cut_50bp", "probability": 0.19},
            {"label": "no_cut", "probability": 0.26},
        ],
    )
    graph.append(prob)
    vitals.record_packet("ProbabilityPacket")

    # F3 — Action (EXECUTE)
    action = apu.to_action_packet(
        subject_id=subject_id,
        subject_type="person",
        root_signal_id=signal.payload.signal_id,
        trace_id=signal.lineage.trace_id,
        cycle_id=signal.lineage.cycle_id,
        parent_packet_id=prob.packet_id,
        witness=prob.witness.model_dump(),
        raw_decision={
            "decision": "EXECUTE",
            "confidence_score": 0.83,
            "epistemic_warrant": "STRONG",
            "constitutional_warrant": "STRONG",
            "downside_boundedness": "MEDIUM",
            "rationale": "High-confidence rate-cut signal with strong pricing and bounded downside.",
            "chosen_path": "long_btc_fed_narrative",
            "recommended_action": {
                "action_type": "TRADE",
                "asset": "BTC",
                "direction": "LONG",
                "size_usdc": 250.0,
            },
        },
    )
    graph.append(action)
    vitals.record_packet("ActionPacket")
    vitals.record_decision("EXECUTE")
    assert resolver.validate_permissions(action, ctx) is True

    # F4 — Receipt (confirmed execution)
    receipt = ofn.to_receipt_packet(
        action_packet=action,
        receipt_id="rcpt_g4_exec_001",
        execution_status="EXECUTED",
        tx_hash="0xdeadbeef1234",
        filled_size_usdc=250.0,
        slippage=0.002,
        finality="CONFIRMED",
        signal_packet_id=signal.packet_id,
        probability_packet_id=prob.packet_id,
    )
    graph.append(receipt)
    vitals.record_packet("ReceiptPacket")

    # Close trace
    graph.close_trace(signal.lineage.trace_id, reason="receipt_confirmed")

    # Serialize & save
    payload = _serialize_trace(graph, signal.lineage.trace_id, vitals)
    ts = _now_iso()
    uid = uuid.uuid4().hex[:8]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"backbone_trace_EXECUTE_{ts}_{uid}.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


def generate_hold_trace() -> Path:
    """Clean HOLD trace: weak signal, wide spread, no trading permission, refusal closed."""
    subject_id = "nexus:g4_hold"
    circle = CircleAdapter()
    rf = RealityFuturesAdapter()
    apu = APUAdapter()
    nexus = NexusAdapter()
    graph = InMemoryTraceGraph()
    resolver = SubjectResolver()
    vitals = BackboneVitals()

    # F0 — Context (no trading allowed)
    ctx = nexus.to_context_packet(
        subject_id=subject_id,
        subject_type="person",
        can_trade=False,
        usdc_available=0.0,
        risk_profile="conservative",
    )
    resolver.register_context(ctx)
    vitals.record_packet("ContextPacket")

    # F1 — Signal (weak, unverified)
    signal = circle.to_signal_packet(
        subject_id=subject_id,
        subject_type="person",
        signal_id="sig_g4_hold_001",
        source_name="anon_telegram",
        source_type="social",
        source_credibility=0.25,
        domain="crypto",
        signal_type="rumor",
        urgency=0.3,
        novelty=0.2,
        facts=["Unverified whale wallet movement", "No onchain confirmation"],
        tags=["unverified", "whale", "rumor"],
        cycle_id="cycle_g4_sprint1",
    )
    graph.append(signal)
    vitals.record_packet("SignalPacket")

    # F2 — Probability (wide spread, low confidence)
    prob = rf.to_probability_packet(
        signal_packet=signal,
        market_id="rf_g4_hold_001",
        question="Will price move 5% within 24h?",
        base_probability=0.35,
        spread=0.25,
        volatility=0.40,
        confidence_in_price=0.30,
    )
    graph.append(prob)
    vitals.record_packet("ProbabilityPacket")
    assert "SPREAD_WIDE" in prob.witness.flags

    # F3 — Action (HOLD)
    action = apu.to_action_packet(
        subject_id=subject_id,
        subject_type="person",
        root_signal_id=signal.payload.signal_id,
        trace_id=signal.lineage.trace_id,
        cycle_id=signal.lineage.cycle_id,
        parent_packet_id=prob.packet_id,
        witness=prob.witness.model_dump(),
        raw_decision={
            "decision": "HOLD",
            "confidence_score": 0.25,
            "epistemic_warrant": "WEAK",
            "constitutional_warrant": "WEAK",
            "downside_boundedness": "LOW",
            "rationale": "Low-credibility social rumor, wide spread, no trading permission.",
            "hold_reason": "Weak epistemics + no trade permission + wide spread + unverified source",
        },
    )
    graph.append(action)
    vitals.record_packet("ActionPacket")
    vitals.record_decision("HOLD")
    assert action.payload.decision == "HOLD"
    assert action.payload.envelope_allowed is False

    # Close trace (no receipt on HOLD)
    graph.close_trace(signal.lineage.trace_id, reason="refusal_recorded")

    # Serialize & save
    payload = _serialize_trace(graph, signal.lineage.trace_id, vitals)
    ts = _now_iso()
    uid = uuid.uuid4().hex[:8]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"backbone_trace_HOLD_{ts}_{uid}.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out_path


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    exec_path = generate_execute_trace()
    hold_path = generate_hold_trace()

    print(f"✅ EXECUTE trace: {exec_path.relative_to(PROJECT_ROOT)}")
    print(f"✅ HOLD trace:    {hold_path.relative_to(PROJECT_ROOT)}")

    # Quick validation prints
    exec_data = json.loads(exec_path.read_text())
    hold_data = json.loads(hold_path.read_text())

    print(f"\nEXECUTE validation:")
    print(f"  has_signal={exec_data['validation']['has_signal']}")
    print(f"  has_probability={exec_data['validation']['has_probability']}")
    print(f"  has_action={exec_data['validation']['has_action']}")
    print(f"  has_receipt={exec_data['validation']['has_receipt']}")
    print(f"  valid_minimum={exec_data['validation']['valid_minimum']}")
    print(f"  closure_reason={exec_data['meta']['closure_reason']}")
    print(f"  packets={len(exec_data['packets'])}")

    print(f"\nHOLD validation:")
    print(f"  has_signal={hold_data['validation']['has_signal']}")
    print(f"  has_probability={hold_data['validation']['has_probability']}")
    print(f"  has_action={hold_data['validation']['has_action']}")
    print(f"  has_receipt={hold_data['validation']['has_receipt']}")
    print(f"  valid_minimum={hold_data['validation']['valid_minimum']}")
    print(f"  closure_reason={hold_data['meta']['closure_reason']}")
    print(f"  packets={len(hold_data['packets'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
