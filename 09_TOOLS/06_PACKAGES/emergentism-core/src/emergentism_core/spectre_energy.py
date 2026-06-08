"""
SPECTRE EBM energy function — packet 605 §3.3 / packet 606 §8 P2 scaffold.

Per `605_SPECTRE_AS_D5_SELECTION_MESH.md` §3.3, every SPECTRE node's
EBM head scores candidate route actions with a four-component energy:

    E(z, a) = w_eff · C_efficiency
            + w_fx  · C_effectiveness
            + w_hon · C_honesty
            + w_stb · C_stability

Lower energy = better candidate. The L4 selection step commits to
the lowest-energy candidate (at sovereign edge via K2 signature; at
intermediate hop via node stake).

This module implements the energy function over *direct features*
extracted from gossip envelopes — i.e. without requiring a trained
per-node LeWM (P1 of packet 605's build plan). Once P1 is shipped,
the same energy interface accepts features derived from the LeWM
latent `z` rather than from raw gossip — the energy signature does
not change, only the feature source.

Scope: this is P2 scaffold. Query-only; stateless; no network I/O.
The module does not select candidates (that is L4's job); it only
scores and ranks.

Honest-scope clarifications (inherited from packet 605 §8):
  - The weights `w_*` are node-local hyperparameters, not global
    constants. A node declares its weights publicly so callers can
    route around nodes whose weighting diverges from requirements.
  - "Stability" here is the packet-605 register (variance of cost
    under feature perturbation). Packet 606's "confidence" axis is
    a related but distinct concern and is not modeled here.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

logger = logging.getLogger("apu.bot.spectre_energy")


# ------------------------------------------------------------
# Feature dataclasses — direct telemetry shape, no LeWM required
# ------------------------------------------------------------


@dataclass(frozen=True)
class EfficiencyFeatures:
    """Direct cost of traversing a candidate route."""
    expected_latency_ms: float           # ≥ 0
    expected_fee_usdc: float             # ≥ 0
    expected_compute_units: float        # ≥ 0
    expected_bandwidth_mb: float         # ≥ 0


@dataclass(frozen=True)
class EffectivenessFeatures:
    """Does the route actually complete the intent well?"""
    predicted_success_probability: float  # ∈ [0, 1]
    predicted_slippage_bps: float         # ≥ 0; basis points lost to execution drift
    predicted_settlement_delay_s: float   # ≥ 0; seconds beyond best-case


@dataclass(frozen=True)
class HonestyFeatures:
    """How plausible is the route's gossip?

    `implausibility_score` is the LeWM-derived out-of-distribution
    score per packet 605 §3.3: gossip that sits far from the learned
    neighborhood distribution scores high. Without a trained LeWM,
    the caller may pass a heuristic substitute (e.g. variance
    between direct and reciprocal telemetry).
    """
    implausibility_score: float           # ≥ 0; 0 = fully plausible
    reciprocal_mismatch: float            # ≥ 0; direct vs reciprocal observation delta
    witness_count: int                    # ≥ 1; corroborating peers


@dataclass(frozen=True)
class StabilityFeatures:
    """Variance of predicted outcome under gossip perturbation.

    `outcome_variance` is the spread of the predictor's output
    across small perturbations of the input state. High variance →
    the score cannot be trusted; commit somewhere else.
    """
    outcome_variance: float               # ≥ 0


@dataclass(frozen=True)
class RouteCandidate:
    """One candidate next-hop or short route plan scored by the EBM."""
    route_id: str
    hops: Tuple[str, ...]                 # sequence of validator endpoints
    efficiency: EfficiencyFeatures
    effectiveness: EffectivenessFeatures
    honesty: HonestyFeatures
    stability: StabilityFeatures


@dataclass(frozen=True)
class EnergyWeights:
    """Node-local weights. Must be publicly declared per 605 §3.3."""
    w_efficiency: float = 1.0
    w_effectiveness: float = 1.0
    w_honesty: float = 1.0
    w_stability: float = 1.0


@dataclass(frozen=True)
class RouteEnergy:
    """Result of scoring one candidate."""
    route_id: str
    total: float                          # lower = better
    cost_efficiency: float
    cost_effectiveness: float
    cost_honesty: float
    cost_stability: float
    explanation: str


# ------------------------------------------------------------
# Per-component cost functions — lower cost = better candidate
# ------------------------------------------------------------


def _cost_efficiency(f: EfficiencyFeatures) -> float:
    """Additive cost over the four direct-cost features.

    Equal unit weights internally; callers set relative weighting
    across the four top-level components via EnergyWeights. Values
    are treated as already in comparable units (ms / USDC / CU / MB);
    this is a local node's concern to normalize before calling.
    """
    return (
        f.expected_latency_ms
        + f.expected_fee_usdc
        + f.expected_compute_units
        + f.expected_bandwidth_mb
    )


def _cost_effectiveness(f: EffectivenessFeatures) -> float:
    """Cost rises as success probability falls; slippage + delay
    add on top. Reciprocal form keeps the cost ≥ 0 and growing
    sharply near p = 0 without diverging."""
    p = max(1e-6, min(1.0, f.predicted_success_probability))
    return (
        (1.0 - p)
        + f.predicted_slippage_bps / 100.0
        + f.predicted_settlement_delay_s
    )


def _cost_honesty(f: HonestyFeatures) -> float:
    """Implausibility + reciprocal-mismatch; witness count divides
    because more corroborating peers reduce the confidence cost of
    the honesty signal (noisier across few witnesses)."""
    w = max(1, f.witness_count)
    return (f.implausibility_score + f.reciprocal_mismatch) / w


def _cost_stability(f: StabilityFeatures) -> float:
    """Outcome variance is the direct cost; higher variance → lower
    trust in any single score from this node's predictor."""
    return f.outcome_variance


# ------------------------------------------------------------
# Top-level scoring
# ------------------------------------------------------------


def compute_route_energy(
    candidate: RouteCandidate,
    weights: Optional[EnergyWeights] = None,
) -> RouteEnergy:
    """Score one candidate. Lower energy = better."""
    w = weights or EnergyWeights()
    c_eff = _cost_efficiency(candidate.efficiency)
    c_fx = _cost_effectiveness(candidate.effectiveness)
    c_hon = _cost_honesty(candidate.honesty)
    c_stb = _cost_stability(candidate.stability)
    total = (
        w.w_efficiency * c_eff
        + w.w_effectiveness * c_fx
        + w.w_honesty * c_hon
        + w.w_stability * c_stb
    )
    return RouteEnergy(
        route_id=candidate.route_id,
        total=total,
        cost_efficiency=c_eff,
        cost_effectiveness=c_fx,
        cost_honesty=c_hon,
        cost_stability=c_stb,
        explanation=(
            f"E={total:.3f} = {w.w_efficiency:.2f}·{c_eff:.2f}(eff) "
            f"+ {w.w_effectiveness:.2f}·{c_fx:.2f}(fx) "
            f"+ {w.w_honesty:.2f}·{c_hon:.2f}(hon) "
            f"+ {w.w_stability:.2f}·{c_stb:.2f}(stb)"
        ),
    )


def rank_candidates(
    candidates: Sequence[RouteCandidate],
    weights: Optional[EnergyWeights] = None,
) -> List[Tuple[RouteCandidate, RouteEnergy]]:
    """Rank candidates by energy, lowest first.

    The L4 selection step commits to the lowest-energy candidate.
    This function does NOT select — it only ranks. Selection is
    the node's (or signer's) responsibility, because selection is
    where the D5 Force fires and must be borne by the committing
    agent per packet 605 §4 and the D5 Force coordination bridge.
    """
    scored = [(c, compute_route_energy(c, weights)) for c in candidates]
    scored.sort(key=lambda pair: pair[1].total)
    return scored


def energy_spread(energies: Sequence[RouteEnergy]) -> float:
    """Distance between best and worst candidate energy.

    If the spread is small, the L4 commit is genuinely indifferent
    and may reasonably refuse to collapse (HOLD). Callers can use
    this as a dissent-recording signal — commit with recorded
    uncertainty rather than pretend the best candidate is decisive.
    """
    if not energies:
        return 0.0
    totals = [e.total for e in energies]
    return max(totals) - min(totals)


__all__ = [
    "EfficiencyFeatures",
    "EffectivenessFeatures",
    "HonestyFeatures",
    "StabilityFeatures",
    "RouteCandidate",
    "EnergyWeights",
    "RouteEnergy",
    "compute_route_energy",
    "rank_candidates",
    "energy_spread",
]
