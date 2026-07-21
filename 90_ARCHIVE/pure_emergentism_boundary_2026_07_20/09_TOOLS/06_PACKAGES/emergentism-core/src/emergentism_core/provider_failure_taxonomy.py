"""
Provider Failure-Family Taxonomy — packet 96 post-Amendment capability.

Extends provider_availability.probe with semantic classification of known
failure modes. Turns generic "client_error" / "server_error" buckets into
actionable provider-specific intelligence:

  - xAI confabulations       → hallucinated function signatures
  - Groq truncations         → max_tokens mid-response clip
  - Anthropic RLHF theater   → over-refusal on constitutional prompts
  - OpenRouter routing fail  → upstream 502/503 from aggregation layer
  - z.ai latency spikes      → >30s on glm-5.1 thinking model
  - MiniMax rate limiting    → aggressive 429 on Chinese business hours
  - Kimi context overflow    → 128k window exceeded silently

The taxonomy is a regex + heuristic classifier over error_summary strings.
It does NOT require LLM parsing — deterministic, auditable, fast.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class FailurePattern:
    """A known failure mode for a specific provider."""
    pattern_id: str           # e.g. "xai_confabulation"
    provider: str             # e.g. "xai"
    display_name: str         # Human-readable name
    severity: str             # "transient" | "degrading" | "critical"
    recovery_action: str      # What the caller should do
    regex_patterns: Tuple[str, ...]  # Match any of these against error_summary


# Canonical failure-family registry.
# Order matters: more specific patterns should precede generic ones.
FAILURE_PATTERNS: List[FailurePattern] = [
    FailurePattern(
        pattern_id="xai_confabulation",
        provider="xai",
        display_name="xAI function-signature confabulation",
        severity="degrading",
        recovery_action="retry_with_simpler_prompt; validate JSON schema client-side",
        regex_patterns=(
            r"confabulation",
            r"hallucinated",
            r"invalid tool call",
            r"unknown function",
            r"signature mismatch",
        ),
    ),
    FailurePattern(
        pattern_id="groq_truncation",
        provider="groq",
        display_name="Groq response truncation",
        severity="transient",
        recovery_action="increase max_tokens; retry with higher token budget",
        regex_patterns=(
            r"truncat",
            r"max_tokens",
            r"token limit exceeded",
            r"response clipped",
            r"incomplete json",
        ),
    ),
    FailurePattern(
        pattern_id="anthropic_rlhf_theater",
        provider="anthropic",
        display_name="Anthropic RLHF over-refusal",
        severity="degrading",
        recovery_action="rephrase without safety trigger words; use constitutional framing",
        regex_patterns=(
            r"as an ai",
            r"i cannot comply",
            r"ethical concern",
            r"harmful content",
            r"refuse to",
            r"policy violation",
        ),
    ),
    FailurePattern(
        pattern_id="openrouter_routing_fail",
        provider="openrouter",
        display_name="OpenRouter upstream routing failure",
        severity="transient",
        recovery_action="retry with fallback provider; check OpenRouter status page",
        regex_patterns=(
            r"502 bad gateway",
            r"503 service unavailable",
            r"upstream error",
            r"provider unavailable",
            r"routing failed",
        ),
    ),
    FailurePattern(
        pattern_id="zai_latency_spike",
        provider="zai",
        display_name="z.ai latency spike (>30s)",
        severity="transient",
        recovery_action="reduce max_tokens; switch to glm-4-air for speed-critical path",
        regex_patterns=(
            r"timeout",
            r"deadline exceeded",
            r"latency",
            r"slow response",
        ),
    ),
    FailurePattern(
        pattern_id="minimax_rate_limit",
        provider="minimax",
        display_name="MiniMax aggressive rate limit",
        severity="transient",
        recovery_action="exponential backoff; batch requests outside CN business hours",
        regex_patterns=(
            r"429",
            r"rate limit",
            r"too many requests",
            r"quota exceeded",
        ),
    ),
    FailurePattern(
        pattern_id="kimi_context_overflow",
        provider="kimi",
        display_name="Kimi context window overflow",
        severity="degrading",
        recovery_action="truncate context to <100k tokens; use compression",
        regex_patterns=(
            r"context length exceeded",
            r"maximum context",
            r"token overflow",
            r"128k",
            r"window exceeded",
        ),
    ),
    FailurePattern(
        pattern_id="openai_moderation",
        provider="openai",
        display_name="OpenAI moderation flag",
        severity="degrading",
        recovery_action="rephrase prompt; avoid flagged topic keywords",
        regex_patterns=(
            r"moderation",
            r"content filter",
            r"flagged",
            r"safety system",
        ),
    ),
    FailurePattern(
        pattern_id="generic_network",
        provider="*",
        display_name="Generic network error",
        severity="transient",
        recovery_action="retry with exponential backoff",
        regex_patterns=(
            r"connection",
            r"network",
            r"dns",
            r"unreachable",
            r"reset by peer",
        ),
    ),
    FailurePattern(
        pattern_id="generic_auth",
        provider="*",
        display_name="Generic authentication error",
        severity="critical",
        recovery_action="rotate API key; check credential store",
        regex_patterns=(
            r"401",
            r"403",
            r"unauthorized",
            r"invalid key",
            r"api key",
        ),
    ),
]


# Pre-compile regexes for performance
_COMPILED: Dict[str, List[Tuple[FailurePattern, re.Pattern]]] = {}


def _compile() -> None:
    global _COMPILED
    if _COMPILED:
        return
    for fp in FAILURE_PATTERNS:
        compiled = []
        for pat in fp.regex_patterns:
            try:
                compiled.append((fp, re.compile(pat, re.IGNORECASE)))
            except re.error:
                continue
        _COMPILED[fp.pattern_id] = compiled


def classify_error_summary(
    error_summary: str,
    provider: str,
) -> Optional[FailurePattern]:
    """Classify an error summary into a known failure pattern.

    Returns the first matching FailurePattern, or None if no pattern matches.
    Provider-specific patterns are checked before generic (* provider) patterns.
    """
    if not error_summary:
        return None

    _compile()

    # Check provider-specific patterns first
    for fp in FAILURE_PATTERNS:
        if fp.provider != "*" and fp.provider != provider:
            continue
        if fp.provider == "*":
            continue  # Skip generic for now
        for _, regex in _COMPILED.get(fp.pattern_id, []):
            if regex.search(error_summary):
                return fp

    # Then check generic patterns
    for fp in FAILURE_PATTERNS:
        if fp.provider != "*":
            continue
        for _, regex in _COMPILED.get(fp.pattern_id, []):
            if regex.search(error_summary):
                return fp

    return None


def classify_outcome(
    outcome: str,
    error_summary: Optional[str],
    provider: str,
) -> Tuple[str, Optional[FailurePattern]]:
    """Classify a call outcome + error_summary into a failure family.

    Returns (outcome_label, pattern) where outcome_label is one of:
      - "success"
      - "rate_limit"
      - "server_error"
      - "client_error"
      - "network_error"
      - "timeout"
      - "auth_error"
    """
    if outcome == "success":
        return "success", None

    # Override generic outcome with auth-specific label when detected
    if error_summary:
        auth_pats = _COMPILED.get("generic_auth", [])
        for _, regex in auth_pats:
            if regex.search(error_summary):
                return "auth_error", FAILURE_PATTERNS[-1]  # generic_auth is last

    pattern = classify_error_summary(error_summary or "", provider)
    return outcome, pattern


def get_failure_family_report(
    store_path: Optional[str] = None,
) -> Dict[str, any]:
    """Generate a human-readable failure-family report from the health store.

    This is a convenience wrapper for operator dashboards and Cortex witness.
    """
    from .provider_availability import DEFAULT_HEALTH_STORE_PATH

    path = store_path or str(DEFAULT_HEALTH_STORE_PATH)

    # Query last 72h of call outcomes
    import sqlite3
    from datetime import datetime, timezone, timedelta

    cutoff = (datetime.now(timezone.utc) - timedelta(hours=72)).isoformat()
    try:
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT provider, model, outcome, error_summary FROM call_outcomes "
            "WHERE called_at >= ?",
            (cutoff,),
        ).fetchall()
        conn.close()
    except Exception:
        rows = []

    family_counts: Dict[str, Dict[str, int]] = {}
    provider_counts: Dict[str, int] = {}

    for row in rows:
        provider = row["provider"]
        provider_counts[provider] = provider_counts.get(provider, 0) + 1

        if row["outcome"] == "success":
            continue

        pattern = classify_error_summary(row["error_summary"] or "", provider)
        family = pattern.pattern_id if pattern else "unclassified"

        if family not in family_counts:
            family_counts[family] = {}
        family_counts[family][provider] = family_counts[family].get(provider, 0) + 1

    return {
        "window_hours": 72,
        "total_calls": len(rows),
        "calls_by_provider": provider_counts,
        "failure_families": family_counts,
        "known_patterns": len(FAILURE_PATTERNS),
    }


__all__ = [
    "FailurePattern",
    "FAILURE_PATTERNS",
    "classify_error_summary",
    "classify_outcome",
    "get_failure_family_report",
]
