"""
Provider cluster-correlated failure detection — the fifth coordination-
memo gap (2026-04-23), closed at the polygenetic-safety layer.

Relation to sibling module `provider_failure_taxonomy.py`:

  - `provider_failure_taxonomy` classifies a single error_summary
    into a known failure PATTERN (e.g. xai_confabulation,
    groq_truncation, anthropic_rlhf_theater). Semantic, per-string.
  - `provider_cluster_correlation` (this module) aggregates raw
    outcome rows across providers and detects when multiple
    providers in the same RLHF lineage cluster fail with the same
    family simultaneously. Statistical, per-cluster.

These are complementary closures of the same gap. A per-string
classifier without a cluster-layer aggregator cannot tell you "all
three western_frontier seats hit 429 within a 15-minute window";
an aggregator without a classifier cannot tell you *which* 429.
Together they close the polygenetic-safety blind spot that the
coordination memo named.

Why this matters at the aggregator:

  Lineage decorrelation (packet 96 Amendment 2) guarantees that a
  default triad draws from ≥ 2 distinct RLHF lineage clusters.
  That guarantee protects against SAMPLING-time cluster monoculture.
  It does NOT protect against RUNTIME cluster failure correlation —
  the case where three seats from different clusters are sampled
  correctly but two of them happen to be in the same cluster which
  is simultaneously degrading. This module makes that runtime signal
  queryable so the aggregator can refuse false-Φ.

Query-only surface. Writes nothing. Operates on the existing
`call_outcomes` table in provider_health.sqlite.
"""
from __future__ import annotations

import logging
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple

from .lineage_decorrelation import RLHF_LINEAGE_CLUSTERS
from .provider_availability import ProviderHealthStore, get_default_store

logger = logging.getLogger("apu.bot.provider_cluster_correlation")


# Outcome families the ProviderHealthStore records. Duplicated here as a
# local whitelist so schema drift in provider_availability surfaces
# as an explicit failure rather than silent mis-classification.
OUTCOME_FAMILIES: Tuple[str, ...] = (
    "success",
    "rate_limit",
    "server_error",
    "client_error",
    "network_error",
    "timeout",
)
FAILURE_FAMILIES: Tuple[str, ...] = tuple(f for f in OUTCOME_FAMILIES if f != "success")


@dataclass(frozen=True)
class ProviderFamilyBreakdown:
    """Per-family outcome breakdown for a single (provider, model) pair."""
    provider: str
    model: str
    window_hours: int
    total_calls: int
    counts: Dict[str, int]            # family → raw count
    pct: Dict[str, float]             # family → percentage (0-100)
    dominant_family: Optional[str]    # family with highest count among failures
    signature: str                    # classification: see _classify_signature
    reason: str


@dataclass(frozen=True)
class ClusterBurst:
    """A detected cluster-correlated failure burst."""
    cluster_id: str
    family: str
    providers_affected: List[str]
    window_start: str                 # ISO8601
    window_end: str                   # ISO8601
    event_count: int
    reason: str


def _iso_utc_minus(hours: float = 0, minutes: float = 0) -> str:
    return (
        datetime.now(timezone.utc) - timedelta(hours=hours, minutes=minutes)
    ).isoformat()


def _classify_signature(total: int, counts: Dict[str, int]) -> Tuple[str, str]:
    """Map raw family counts to a human-readable signature + reason."""
    if total == 0:
        return "unknown_no_volume", "No calls recorded in window."
    successes = counts.get("success", 0)
    failures = total - successes
    if failures == 0:
        return "healthy", f"All {total} calls succeeded."
    if total < 5:
        return (
            "unknown_low_volume",
            f"Only {total} calls in window; signature not yet meaningful.",
        )
    failure_pct = (failures / total) * 100.0
    failing_only = {k: v for k, v in counts.items() if k in FAILURE_FAMILIES and v > 0}
    if not failing_only:
        return "healthy", f"All {total} calls succeeded."
    dominant = max(failing_only.items(), key=lambda kv: kv[1])[0]
    dominant_pct = (failing_only[dominant] / total) * 100.0
    if failure_pct < 10.0:
        return (
            f"healthy_intermittent_{dominant}",
            f"{failures}/{total} failures ({failure_pct:.1f}%); "
            f"dominant family {dominant} ({dominant_pct:.1f}%) below "
            f"10% floor — intermittent, not systemic.",
        )
    if failure_pct < 40.0:
        return (
            f"{dominant}_dominated",
            f"{failures}/{total} failures ({failure_pct:.1f}%); "
            f"dominant family {dominant} ({dominant_pct:.1f}%).",
        )
    return (
        f"{dominant}_systemic",
        f"{failures}/{total} failures ({failure_pct:.1f}%) — systemic; "
        f"dominant family {dominant} ({dominant_pct:.1f}%).",
    )


def compute_provider_family_breakdown(
    provider: str,
    model: str,
    *,
    window_hours: int = 24,
    store: Optional[ProviderHealthStore] = None,
) -> ProviderFamilyBreakdown:
    """Compute per-family outcome breakdown for (provider, model).

    Returns a ProviderFamilyBreakdown even when there is no history; in
    that case `total_calls == 0` and `signature == "unknown_no_volume"`.
    Never raises on empty or malformed rows.
    """
    s = store or get_default_store()
    cutoff = _iso_utc_minus(hours=window_hours)
    counts: Dict[str, int] = {f: 0 for f in OUTCOME_FAMILIES}

    try:
        with sqlite3.connect(str(s.path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT outcome FROM call_outcomes
                WHERE provider = ? AND model = ? AND called_at >= ?
                """,
                (provider, model, cutoff),
            ).fetchall()
    except sqlite3.Error as e:
        logger.warning(
            f"provider_cluster_correlation: breakdown query failed for "
            f"({provider}, {model}): {e}"
        )
        rows = []

    for r in rows:
        family = r["outcome"]
        if family in counts:
            counts[family] += 1
        else:
            counts["client_error"] += 1  # match record_outcome coercion rule

    total = sum(counts.values())
    pct = {
        k: (v / total * 100.0) if total > 0 else 0.0
        for k, v in counts.items()
    }
    failing_only = {k: v for k, v in counts.items() if k in FAILURE_FAMILIES and v > 0}
    dominant = (
        max(failing_only.items(), key=lambda kv: kv[1])[0]
        if failing_only else None
    )
    signature, reason = _classify_signature(total, counts)

    return ProviderFamilyBreakdown(
        provider=provider,
        model=model,
        window_hours=window_hours,
        total_calls=total,
        counts=counts,
        pct=pct,
        dominant_family=dominant,
        signature=signature,
        reason=reason,
    )


def detect_cluster_correlated_bursts(
    *,
    window_minutes: int = 60,
    min_seats: int = 2,
    store: Optional[ProviderHealthStore] = None,
) -> List[ClusterBurst]:
    """Detect cluster-correlated failure bursts in the last `window_minutes`.

    A burst is defined as: ≥ `min_seats` distinct providers within the
    same RLHF lineage cluster, each recording the SAME failure family
    within the window.

    Returns one ClusterBurst per (cluster, family) that satisfies the
    threshold. Empty list if no cluster-correlated bursts detected.
    Providers in `unknown` or `unknown_aggregator` clusters are
    excluded — they do not constitute a cluster-correlated signal.

    This is the cluster-layer Raktabīja detector — it names failures
    that lineage-decorrelation at SAMPLING time is structurally blind
    to at RUNTIME.
    """
    s = store or get_default_store()
    window_start_iso = _iso_utc_minus(minutes=window_minutes)
    now_iso = datetime.now(timezone.utc).isoformat()

    try:
        with sqlite3.connect(str(s.path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT provider, outcome, called_at FROM call_outcomes
                WHERE called_at >= ? AND outcome != 'success'
                """,
                (window_start_iso,),
            ).fetchall()
    except sqlite3.Error as e:
        logger.warning(f"provider_cluster_correlation: burst query failed: {e}")
        return []

    # Group by (cluster, family) → {provider: event_count}
    grouped: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in rows:
        provider = r["provider"]
        family = r["outcome"]
        cluster = RLHF_LINEAGE_CLUSTERS.get(provider, "unknown")
        if cluster in ("unknown", "unknown_aggregator"):
            continue
        grouped[(cluster, family)][provider] += 1

    bursts: List[ClusterBurst] = []
    for (cluster, family), per_provider in grouped.items():
        affected = sorted(per_provider.keys())
        if len(affected) >= min_seats:
            events = sum(per_provider.values())
            bursts.append(
                ClusterBurst(
                    cluster_id=cluster,
                    family=family,
                    providers_affected=affected,
                    window_start=window_start_iso,
                    window_end=now_iso,
                    event_count=events,
                    reason=(
                        f"{len(affected)} providers in cluster {cluster!r} "
                        f"hit {family!r} in last {window_minutes}m "
                        f"({events} events across {', '.join(affected)})"
                    ),
                )
            )

    bursts.sort(key=lambda b: (-len(b.providers_affected), -b.event_count))
    return bursts


__all__ = [
    "OUTCOME_FAMILIES",
    "FAILURE_FAMILIES",
    "ProviderFamilyBreakdown",
    "ClusterBurst",
    "compute_provider_family_breakdown",
    "detect_cluster_correlated_bursts",
]
