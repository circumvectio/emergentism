"""
Provider availability probe — packet 96 Amendment 1.

Binding precondition (alongside Amendment 2's lineage-decorrelation
invariant) for flipping `settings.council_l4_triangulation` to True.

Problem packet 96 names:

  Without an availability probe, the default triad collapses silently
  to 2-way (or 1-way) when any of `claude-sonnet-4-5`, `gpt-4o`, or
  `grok-2` deprecates. The aggregator would still produce output —
  but the output would carry the *appearance* of ensemble
  decorrelation while running on a single provider. This is a
  canonical Raktabīja failure mode: the guard against bias becomes
  the vehicle for it.

This module provides:

  - `ProviderHealth` — per-provider health record
  - `ProviderHealthStore` — SQLite-backed append-only health register
  - `record_call_result(...)` — post-dispatch hook to log success / rate-
    limit / error; callable from any provider-calling site
  - `assess_triad_availability(triad, store)` — aggregator pre-flight:
    returns (healthy_count, per_seat_assessment) so the L4 dispatcher
    can degrade to RECORDED-DISSENT mode rather than silent collapse
    when fewer than 2 of 3 providers are healthy

The store lives at `~/.apu_bot/provider_health.sqlite` by default
(sibling of `cortex.sqlite` — same local, no-network, η=0 principle).

Not a foundation invariant by itself — this is an operational
capability that enforces the foundation's "refuse false-Φ at any
caste" discipline by preventing silent-collapse ensemble-theater.
"""
from __future__ import annotations

import logging
import os
import sqlite3
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger("apu.bot.provider_availability")


DEFAULT_HEALTH_STORE_PATH = Path(os.path.expanduser("~/.apu_bot/provider_health.sqlite"))


@dataclass(frozen=True)
class ProviderHealth:
    """Snapshot of one provider's health over a trailing window."""
    provider: str
    model: str
    last_success_at: Optional[str]  # ISO8601, or None if never
    last_failure_at: Optional[str]
    total_calls_24h: int
    success_calls_24h: int
    rate_limit_calls_24h: int      # 429s
    server_error_calls_24h: int    # 5xx
    client_error_calls_24h: int    # 4xx other than 429
    status: str                     # "healthy" | "degraded" | "failing" | "unknown"
    reason: str


@dataclass(frozen=True)
class TriadAvailabilityAssessment:
    """Pre-dispatch assessment of a triad's availability."""
    triad: List[str]
    per_seat: List[ProviderHealth]
    healthy_count: int
    degraded_count: int
    failing_count: int
    unknown_count: int
    recommendation: str  # "proceed_triangulate" | "degrade_recorded_dissent" | "fallback_single" | "abort"
    reason: str


class ProviderHealthStore:
    """Append-only SQLite store for provider-call outcomes.

    Every call to an external provider writes one row. The trailing-
    24h query aggregates recent rows into a ProviderHealth snapshot.
    No updates in place — only inserts. Easy to audit, easy to prune,
    no write-amplification.
    """

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS call_outcomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        provider TEXT NOT NULL,
        model TEXT NOT NULL,
        called_at TEXT NOT NULL,       -- ISO8601
        outcome TEXT NOT NULL,         -- 'success' | 'rate_limit' | 'server_error' | 'client_error' | 'network_error' | 'timeout'
        http_status INTEGER,
        latency_ms REAL,
        error_summary TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_provider_called_at ON call_outcomes(provider, called_at);
    CREATE INDEX IF NOT EXISTS idx_called_at ON call_outcomes(called_at);
    """

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path is not None else DEFAULT_HEALTH_STORE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        with self._lock, self._connect() as conn:
            conn.executescript(self.SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.path), timeout=5.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def record_outcome(
        self,
        *,
        provider: str,
        model: str,
        outcome: str,
        http_status: Optional[int] = None,
        latency_ms: Optional[float] = None,
        error_summary: Optional[str] = None,
    ) -> None:
        """Record one provider-call outcome. Never raises."""
        valid_outcomes = {
            "success", "rate_limit", "server_error",
            "client_error", "network_error", "timeout",
        }
        if outcome not in valid_outcomes:
            logger.warning(f"Unknown outcome {outcome!r}; coercing to 'client_error'")
            outcome = "client_error"
        try:
            with self._lock, self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO call_outcomes
                      (provider, model, called_at, outcome, http_status, latency_ms, error_summary)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        provider, model,
                        datetime.now(timezone.utc).isoformat(),
                        outcome, http_status, latency_ms,
                        (error_summary or "")[:500],
                    ),
                )
        except sqlite3.Error as e:
            logger.warning(f"provider_health store write failed: {e}")

    def assess_provider(self, provider: str, model: str) -> ProviderHealth:
        """Build a ProviderHealth snapshot for one provider over the
        trailing 24-hour window.

        Status grading:
          healthy  — ≥ 3 successes in 24h AND most-recent outcome is success
          degraded — mixed record; recent rate-limits or server errors
          failing  — > 50% failures in last 10 calls, OR last success
                      was > 6h ago with recent failures
          unknown  — zero recorded calls in 24h (no signal)
        """
        cutoff = self._iso_utc_minus_hours(24)
        try:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT outcome, called_at FROM call_outcomes
                    WHERE provider = ? AND called_at >= ?
                    ORDER BY called_at DESC
                    """,
                    (provider, cutoff),
                ).fetchall()
        except sqlite3.Error as e:
            logger.warning(f"provider_health assess failed: {e}")
            rows = []

        total = len(rows)
        successes = sum(1 for r in rows if r["outcome"] == "success")
        rate_limits = sum(1 for r in rows if r["outcome"] == "rate_limit")
        server_errors = sum(1 for r in rows if r["outcome"] == "server_error")
        client_errors = sum(1 for r in rows if r["outcome"] == "client_error")

        last_success = next((r["called_at"] for r in rows if r["outcome"] == "success"), None)
        last_failure = next((r["called_at"] for r in rows if r["outcome"] != "success"), None)

        status, reason = self._grade(rows, successes, total)
        return ProviderHealth(
            provider=provider,
            model=model,
            last_success_at=last_success,
            last_failure_at=last_failure,
            total_calls_24h=total,
            success_calls_24h=successes,
            rate_limit_calls_24h=rate_limits,
            server_error_calls_24h=server_errors,
            client_error_calls_24h=client_errors,
            status=status,
            reason=reason,
        )

    @staticmethod
    def _grade(rows, successes: int, total: int) -> Tuple[str, str]:
        if total == 0:
            return "unknown", "No calls recorded in trailing 24h"

        if successes >= 3 and rows and rows[0]["outcome"] == "success":
            return "healthy", (
                f"{successes}/{total} successes in 24h; most-recent outcome is success"
            )

        # Last 10 calls for a near-term trend
        window = rows[:10]
        recent_successes = sum(1 for r in window if r["outcome"] == "success")
        recent_failure_rate = 1 - (recent_successes / len(window)) if window else 0

        if recent_failure_rate > 0.5:
            return "failing", (
                f"Recent failure rate {recent_failure_rate:.0%} over last "
                f"{len(window)} calls"
            )

        if successes == 0:
            return "failing", f"0/{total} successes in 24h"

        return "degraded", (
            f"{successes}/{total} successes in 24h; mixed record (recent "
            f"failure rate {recent_failure_rate:.0%})"
        )

    @staticmethod
    def _iso_utc_minus_hours(hours: int) -> str:
        return datetime.fromtimestamp(
            time.time() - hours * 3600, tz=timezone.utc
        ).isoformat()

    def prune_older_than(self, hours: int = 72) -> int:
        """Delete rows older than `hours`. Returns rows deleted."""
        cutoff = self._iso_utc_minus_hours(hours)
        try:
            with self._lock, self._connect() as conn:
                cur = conn.execute(
                    "DELETE FROM call_outcomes WHERE called_at < ?",
                    (cutoff,),
                )
                return cur.rowcount
        except sqlite3.Error as e:
            logger.warning(f"provider_health prune failed: {e}")
            return 0


# Module-level default store. Lazy-init so tests can monkey-patch.
_default_store: Optional[ProviderHealthStore] = None


def get_default_store() -> ProviderHealthStore:
    global _default_store
    if _default_store is None:
        _default_store = ProviderHealthStore()
    return _default_store


def record_call_result(
    provider: str,
    model: str,
    outcome: str,
    *,
    http_status: Optional[int] = None,
    latency_ms: Optional[float] = None,
    error_summary: Optional[str] = None,
    store: Optional[ProviderHealthStore] = None,
) -> None:
    """Public fire-and-log hook for provider-calling code sites."""
    s = store or get_default_store()
    s.record_outcome(
        provider=provider, model=model, outcome=outcome,
        http_status=http_status, latency_ms=latency_ms,
        error_summary=error_summary,
    )


# ------------------------------------------------------------
# Triad availability assessment (the L4 pre-flight gate)
# ------------------------------------------------------------


def _provider_from_model(model: str) -> str:
    """Local copy of provider-from-model — decoupled from ai_client."""
    m = (model or "").lower().strip()
    if not m:
        return "unknown"
    if m.startswith("openai/") or m.startswith("gpt-"):
        return "openai"
    if m.startswith("anthropic/") or m.startswith("claude-"):
        return "anthropic"
    if m.startswith("google/") or m.startswith("gemini-"):
        return "google"
    if m.startswith("meta/") or m.startswith("meta-llama/") or m.startswith("llama-"):
        return "meta"
    if m.startswith("mistralai/") or m.startswith("mistral/") or m.startswith("mistral-"):
        return "mistral"
    if m.startswith("x-ai/") or m.startswith("xai/") or m.startswith("grok-"):
        return "xai"
    if m.startswith("zhipuai/") or m.startswith("zai/") or m.startswith("glm-"):
        return "zai"
    if m.startswith("minimax/") or m.startswith("minimax-"):
        return "minimax"
    if (m.startswith("moonshotai/") or m.startswith("moonshot/")
            or m.startswith("kimi/") or m.startswith("kimi-")
            or m.startswith("moonshot-")):
        return "kimi"
    if m.startswith("groq/"):
        return "groq"
    if m.startswith("nvidia/"):
        return "nvidia"
    if m.startswith("deepseek/") or m.startswith("deepseek-"):
        return "deepseek"
    if m.startswith("qwen/") or m.startswith("qwen-"):
        return "qwen"
    return "unknown"


def assess_triad_availability(
    triad: List[str],
    store: Optional[ProviderHealthStore] = None,
) -> TriadAvailabilityAssessment:
    """Pre-dispatch assessment of a triad's availability.

    Returns a TriadAvailabilityAssessment whose .recommendation is one of:

      "proceed_triangulate" — ≥ 2 seats healthy; safe to fire triad
      "degrade_recorded_dissent" — exactly 1 seat healthy; fire single
           with the dissent recorded in Cortex (not silently collapsing)
      "fallback_single" — all seats unknown (no history); fire single-
           provider path with degraded confidence; triangulation unsafe
      "abort" — 0 healthy + ≥ 1 failing; all known seats are failing;
           escalate or HOLD

    Packet 96 Amendment 1 binding condition: if fewer than 2 of 3 seats
    are healthy, the aggregator must NOT silently collapse to a
    smaller ensemble. The recommendation is what the caller must
    observe to preserve that invariant.
    """
    s = store or get_default_store()
    per_seat: List[ProviderHealth] = []
    for model in triad:
        provider = _provider_from_model(model)
        per_seat.append(s.assess_provider(provider, model))

    healthy = sum(1 for p in per_seat if p.status == "healthy")
    degraded = sum(1 for p in per_seat if p.status == "degraded")
    failing = sum(1 for p in per_seat if p.status == "failing")
    unknown = sum(1 for p in per_seat if p.status == "unknown")

    # Recommendation grading
    if healthy >= 2:
        recommendation = "proceed_triangulate"
        reason = (
            f"{healthy}/{len(triad)} seats healthy; triangulation safe. "
            f"(degraded={degraded}, failing={failing}, unknown={unknown})"
        )
    elif healthy == 1 and failing + degraded >= 1:
        recommendation = "degrade_recorded_dissent"
        reason = (
            f"Only 1/{len(triad)} seats healthy with {failing} failing + "
            f"{degraded} degraded; fire single-provider path with DISSENT "
            f"recorded in Cortex to prevent silent-collapse false-Φ."
        )
    elif unknown == len(triad):
        recommendation = "fallback_single"
        reason = (
            f"All {len(triad)} seats have no health history (unknown); "
            f"triangulation unsafe without baseline. Fire single-provider "
            f"path and begin recording outcomes."
        )
    elif failing >= len(triad) - unknown:
        recommendation = "abort"
        reason = (
            f"{failing}/{len(triad)} seats failing, {unknown} unknown, "
            f"0 healthy — triad cannot produce a trustworthy decision. "
            f"Escalate to L5 or HOLD."
        )
    else:
        # Mixed case: 0 healthy, some unknown/degraded, no quorum possible
        recommendation = "degrade_recorded_dissent"
        reason = (
            f"No healthy seats (healthy={healthy}, degraded={degraded}, "
            f"failing={failing}, unknown={unknown}); degrade path."
        )

    return TriadAvailabilityAssessment(
        triad=list(triad),
        per_seat=per_seat,
        healthy_count=healthy,
        degraded_count=degraded,
        failing_count=failing,
        unknown_count=unknown,
        recommendation=recommendation,
        reason=reason,
    )


__all__ = [
    "ProviderHealth",
    "ProviderHealthStore",
    "TriadAvailabilityAssessment",
    "DEFAULT_HEALTH_STORE_PATH",
    "get_default_store",
    "record_call_result",
    "assess_triad_availability",
]
