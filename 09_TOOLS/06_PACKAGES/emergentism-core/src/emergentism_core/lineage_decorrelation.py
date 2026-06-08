"""
RLHF-lineage decorrelation invariant for L4 triangulated triad — packet 96 Amendment 2.

The invariant (geometric, not geographic):

  No default L4 triad may draw more than two seats from a single
  RLHF-lineage cluster, where "lineage" is defined by shared
  researcher-movement, shared reward-model convention, and shared
  safety-corpora heritage — not by geography, regulation, or
  political frame.

A triad of three logos can still be one covariance basin. Counting
providers says 3; counting failure-mode covariance says ~1.5 if the
three providers are RLHF-adjacent. Packet 96 names this as a
Raktabīja-at-aggregator failure mode: the guard against bias becomes
the vehicle for it.

Lineage cluster definitions are best-effort and conservative — when
in doubt, group two providers together (which makes the invariant
stricter, not looser). Mappings should be revised when:
  - A new provider's training methodology becomes public
  - Researcher movements between labs make a previous boundary stale
  - Empirical evidence of correlated failure modes emerges from
    Cortex v2 lineage queries

Source authority: EMERGENTISM_ORG/11_UPLINK/96_SPRINT_B_POST_95_DRIFT_AND_L4_VERDICT_2026_04_23.md
                  §"Amendment 2 — RLHF-lineage decorrelation invariant"
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List

logger = logging.getLogger("apu.bot.lineage_decorrelation")


# RLHF-lineage clusters. Each cluster name is descriptive; the
# load-bearing identity is the SET of providers in it. Two providers
# in the same cluster have correlated failure modes under adversarial
# load (shared red-team playbook, shared reward-model convention,
# shared safety-corpora). Two providers in different clusters have
# decorrelated failure modes (different training pipeline, different
# RLHF methodology, different safety-corpora heritage).
#
# This is NOT a moral or political grouping. It is a structural
# claim about the covariance of failure modes at the aggregator.

RLHF_LINEAGE_CLUSTERS: Dict[str, str] = {
    # Western frontier RLHF cluster — Constitutional AI / RLHF-from-HF
    # paradigm; ex-OpenAI researcher movement to Anthropic and xAI;
    # adjacent red-team playbooks; overlapping reward-model conventions
    "openai":     "western_frontier_rlhf",
    "anthropic":  "western_frontier_rlhf",
    "xai":        "western_frontier_rlhf",

    # Google / DeepMind cluster — distinct researcher tradition but
    # similar Western big-tech RLHF discipline; conservatively grouped
    # separately because of different training pipeline + safety-corpora
    "google":     "google_deepmind",

    # Meta / Llama cluster — open-weights tradition; different RLHF
    # methodology than the frontier-lab cluster; Groq serves Llama so
    # Groq inherits Meta's lineage when running llama-* models
    "meta":       "meta_open_weights",
    "groq":       "meta_open_weights",  # Groq serves Llama models

    # Chinese frontier cluster — distinct research lineages
    # (Zhipu/Tsinghua, MiniMax, Moonshot, DeepSeek, Alibaba/Qwen);
    # different safety-corpora; different reward-model conventions
    "zai":        "chinese_frontier",
    "minimax":    "chinese_frontier",
    "kimi":       "chinese_frontier",
    "deepseek":   "chinese_frontier",
    "qwen":       "chinese_frontier",

    # Mistral cluster — French open-weights / EU heritage; distinct
    # tradition though convergent on some Western RLHF practices
    "mistral":    "mistral_eu",

    # NVIDIA cluster — model-serving + occasional fine-tunes;
    # provider-of-models stance, not a unified RLHF lineage
    "nvidia":     "nvidia_serving",

    # OpenRouter is an aggregator — its lineage is the underlying
    # provider's lineage. Treat as "unknown" so it does not falsely
    # decorrelate by being counted as a separate cluster. Callers
    # should map openrouter slugs to their underlying provider before
    # checking the invariant; if they don't, openrouter contributes
    # zero to the cluster count.
    "openrouter": "unknown_aggregator",
}


# Maximum number of seats a single cluster may hold in a default triad.
# Per packet 96: "no default triad may draw MORE THAN two seats from a
# single RLHF-lineage cluster" — so the cap is 2 of 3.
MAX_SEATS_PER_CLUSTER = 2


@dataclass(frozen=True)
class LineageCheckResult:
    """Result of a triad-composition lineage decorrelation check."""
    passes: bool
    reason: str
    cluster_breakdown: Dict[str, List[str]]  # cluster_id → [model slugs]


def _provider_from_model(model: str) -> str:
    """Extract canonical provider id from a model slug.

    Mirrors the routing logic in ai_client._provider_from_model and
    pipeline/l2_expansion._resolve_route. Kept local here so the
    decorrelation check has zero coupling to the rest of the stack.
    """
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
    if m.startswith("deepseek/") or m.startswith("deepseek-"):
        return "deepseek"
    if m.startswith("qwen/") or m.startswith("qwen-"):
        return "qwen"
    if m.startswith("nvidia/"):
        return "nvidia"
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
    return "unknown"


def cluster_for_model(model: str) -> str:
    """Map a model slug to its RLHF lineage cluster id.

    Returns "unknown_aggregator" or "unknown" for slugs we cannot
    confidently classify (caller decides how strict to be).
    """
    provider = _provider_from_model(model)
    return RLHF_LINEAGE_CLUSTERS.get(provider, "unknown")


def check_triad_lineage_decorrelation(
    triad: List[str],
    *,
    max_per_cluster: int = MAX_SEATS_PER_CLUSTER,
    treat_unknown_as_distinct: bool = False,
) -> LineageCheckResult:
    """Verify a triad satisfies the lineage-decorrelation invariant.

    Args:
        triad: list of model slugs (e.g.
               ["anthropic/claude-sonnet-4-5", "openai/gpt-4o", "xai/grok-2"])
        max_per_cluster: maximum seats permitted in any single cluster
                         (default 2; packet 96 invariant)
        treat_unknown_as_distinct: if True, each "unknown" model counts
                                    as its own cluster (loose check; useful
                                    when probing experimental providers).
                                    If False (default), all "unknown"
                                    models collapse into one bucket
                                    (strict check; matches the invariant
                                    intent — uncertainty is not decorrelation).

    Returns:
        LineageCheckResult with .passes (bool), .reason (string), and
        .cluster_breakdown (cluster_id → list of model slugs).
    """
    if not triad:
        return LineageCheckResult(
            passes=False,
            reason="Empty triad — no seats to check",
            cluster_breakdown={},
        )

    breakdown: Dict[str, List[str]] = {}
    for i, model in enumerate(triad):
        cluster = cluster_for_model(model)
        if cluster == "unknown" and treat_unknown_as_distinct:
            cluster = f"unknown_{i}"
        breakdown.setdefault(cluster, []).append(model)

    # Find any cluster exceeding the limit
    violators = {
        cluster: models
        for cluster, models in breakdown.items()
        if len(models) > max_per_cluster
    }

    if not violators:
        clusters_seen = sorted(breakdown.keys())
        return LineageCheckResult(
            passes=True,
            reason=(
                f"Lineage-decorrelation invariant satisfied: "
                f"{len(breakdown)} cluster(s) across {len(triad)} seats, "
                f"max-per-cluster={max(len(m) for m in breakdown.values())} "
                f"<= cap={max_per_cluster}. Clusters: {clusters_seen}."
            ),
            cluster_breakdown=breakdown,
        )

    violator_summary = "; ".join(
        f"{cluster}={len(models)} seats ({', '.join(models)})"
        for cluster, models in violators.items()
    )
    return LineageCheckResult(
        passes=False,
        reason=(
            f"Lineage-decorrelation invariant VIOLATED: cluster(s) "
            f"exceed cap={max_per_cluster}. {violator_summary}. "
            f"Effective decorrelation is well below the apparent "
            f"{len(triad)}-way ensemble — this is false-Φ at the Kṣatriya "
            f"seat. Replace one seat with a provider from a different "
            f"lineage cluster (e.g., zai/glm-*, minimax/MiniMax-*, "
            f"kimi/moonshot-*, google/gemini-*, mistral/*, meta/llama-*)."
        ),
        cluster_breakdown=breakdown,
    )


def assert_triad_lineage_decorrelated(triad: List[str]) -> None:
    """Hard-assert the lineage invariant. Raises ValueError on violation.

    Use at config-load time for default triads; the explicit error
    message names which cluster overflows so the operator can pick
    a replacement.
    """
    result = check_triad_lineage_decorrelation(triad)
    if not result.passes:
        raise ValueError(
            f"L4 triad violates lineage-decorrelation invariant "
            f"(packet 96 Amendment 2): {result.reason}"
        )


__all__ = [
    "RLHF_LINEAGE_CLUSTERS",
    "MAX_SEATS_PER_CLUSTER",
    "LineageCheckResult",
    "cluster_for_model",
    "check_triad_lineage_decorrelation",
    "assert_triad_lineage_decorrelated",
]
