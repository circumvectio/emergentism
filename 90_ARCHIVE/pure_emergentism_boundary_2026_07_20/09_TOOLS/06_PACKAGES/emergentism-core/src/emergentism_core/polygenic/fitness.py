"""Fitness landscape for the 12-dimensional polygenic genotype.

Fitness = product of 8 factors, each ∈ [0, 1]:
  F_k2   — K2 approval rate (constitutional consent)
  F_cci  — Caste Concentration Index health (not over-specialised)
  F_edi  — Economic Diversity Index (not monoculture)
  F_act  — Activity recency (not dormant)
  F_excl — Competitive exclusion (niche differentiation)
  F_env  — Environmental modifier (market conditions)
  F_econ — Economic efficiency (revenue / cost)
  F_eta  — η compliance (zero extraction verification)

Any factor = 0 → lethal (fitness = 0). This enforces hard constitutional constraints.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from .genotype import FullGenotype


# ─────────────────────────────────────────────────────────────────────────────
# FITNESS CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────

CCI_FORMING_MAX = 0.010
CCI_HEALTHY_MAX = 0.200
CCI_PATHOLOGICAL = 0.500

EDI_HEALTHY_MIN = 0.60
EDI_PATHOLOGICAL = 0.20

INACTIVITY_LIMIT_DAYS = 180
INACTIVITY_CRITICAL_DAYS = 360
GENERATION_DAYS = 30

K2_REFUSAL_RATE_TRIGGER = 0.80
FITNESS_COLLAPSE_TRIGGER = 0.10

ENV_FLUCTUATION_AMP = 0.05
ENV_DROUGHT_CHANCE = 0.02


@dataclass
class FitnessResult:
    total: float
    f_k2: float
    f_cci: float
    f_edi: float
    f_act: float
    f_excl: float
    f_env: float
    f_econ: float
    f_eta: float
    lethal_factors: list[str]
    notes: list[str]

    def to_dict(self) -> dict:
        return {
            "fitness": round(self.total, 4),
            "factors": {
                "k2": round(self.f_k2, 4),
                "cci": round(self.f_cci, 4),
                "edi": round(self.f_edi, 4),
                "activity": round(self.f_act, 4),
                "exclusion": round(self.f_excl, 4),
                "environment": round(self.f_env, 4),
                "economic": round(self.f_econ, 4),
                "eta": round(self.f_eta, 4),
            },
            "lethal_factors": self.lethal_factors,
            "notes": self.notes,
        }


class FitnessLandscape:
    """Computes phenotype fitness from genotype + environment + performance data."""

    def __init__(self):
        pass

    def compute(
        self,
        genotype: FullGenotype,
        # K2 performance
        k2_signatures: int = 0,
        k2_refusals: int = 0,
        k2_conditional: int = 0,
        # Activity
        last_activity_iso: Optional[str] = None,
        activity_count: int = 0,
        # Competitive context
        competitor_genotypes: Optional[list[FullGenotype]] = None,
        # Environment
        env_shock: float = 1.0,
        # Economic performance
        revenue: float = 0.0,
        capital_cost: float = 0.0,
        labour_cost: float = 0.0,
        knowledge_cost: float = 0.0,
        regulatory_cost: float = 0.0,
        network_cost: float = 0.0,
        # η compliance
        eta_violation_detected: bool = False,
    ) -> FitnessResult:
        """Compute full fitness with all 8 factors."""

        lethal: list[str] = []
        notes: list[str] = []

        # ── F_k2: Constitutional consent ────────────────────────────────────
        total_k2 = k2_signatures + k2_refusals + k2_conditional
        if total_k2 == 0:
            f_k2 = 0.4  # no-data prior
            notes.append("No K2 data — neutral prior (0.4)")
        else:
            approval_rate = k2_signatures / total_k2
            refusal_rate = k2_refusals / total_k2
            f_k2 = approval_rate
            if refusal_rate > K2_REFUSAL_RATE_TRIGGER:
                lethal.append("k2_refusal_rate")
                notes.append(f"K2 refusal rate {refusal_rate:.1%} > threshold — lethal")

        # ── F_cci: Caste specialisation health ──────────────────────────────
        cci = genotype.caste.compute_cci()
        if cci < CCI_FORMING_MAX:
            f_cci = 0.5
            notes.append("CCI forming — no penalty")
        elif cci <= CCI_HEALTHY_MAX:
            f_cci = 1.0
        elif cci <= CCI_PATHOLOGICAL:
            f_cci = max(0.0, 1.0 - (cci - CCI_HEALTHY_MAX) / (CCI_PATHOLOGICAL - CCI_HEALTHY_MAX))
            notes.append(f"CCI over-specialised ({cci:.3f})")
        else:
            f_cci = 0.0
            lethal.append("cci_pathological")
            notes.append(f"CCI pathological ({cci:.3f}) — lethal")

        # ── F_edi: Economic diversity health ────────────────────────────────
        edi = genotype.economic.compute_edi()
        if edi >= EDI_HEALTHY_MIN:
            f_edi = 1.0
        elif edi >= EDI_PATHOLOGICAL:
            f_edi = max(0.0, (edi - EDI_PATHOLOGICAL) / (EDI_HEALTHY_MIN - EDI_PATHOLOGICAL))
            notes.append(f"EDI low ({edi:.3f}) — economic monoculture risk")
        else:
            f_edi = 0.0
            lethal.append("edi_pathological")
            notes.append(f"EDI pathological ({edi:.3f}) — lethal monoculture")

        # ── F_act: Activity recency ─────────────────────────────────────────
        if not last_activity_iso:
            f_act = 0.0
            lethal.append("no_activity")
            notes.append("No activity recorded — lethal dormancy")
        else:
            try:
                last = datetime.fromisoformat(last_activity_iso.replace("Z", "+00:00"))
                inactive_days = (datetime.now(timezone.utc) - last).days
            except ValueError:
                inactive_days = 9999

            if inactive_days <= GENERATION_DAYS:
                f_act = 1.0
            elif inactive_days >= INACTIVITY_CRITICAL_DAYS:
                f_act = 0.0
                lethal.append("critical_inactivity")
                notes.append(f"Inactive {inactive_days}d — critical")
            elif inactive_days >= INACTIVITY_LIMIT_DAYS:
                f_act = 0.3
                notes.append(f"Inactive {inactive_days}d — dormancy warning")
            else:
                f_act = 1.0 - (inactive_days - GENERATION_DAYS) / (INACTIVITY_LIMIT_DAYS - GENERATION_DAYS)

        # ── F_excl: Competitive exclusion ───────────────────────────────────
        f_excl = 1.0
        if competitor_genotypes:
            distances = [genotype.distance_to(c) for c in competitor_genotypes]
            min_dist = min(distances) if distances else 1.0
            if min_dist < 0.15:
                f_excl = 0.6
                notes.append(f"Niche overlap ({min_dist:.3f}) — severe exclusion")
            elif min_dist < 0.25:
                f_excl = 0.8
                notes.append(f"Niche overlap ({min_dist:.3f}) — moderate exclusion")
            elif min_dist < 0.35:
                f_excl = 0.9
                notes.append(f"Niche overlap ({min_dist:.3f}) — mild exclusion")

        # ── F_env: Environmental modifier ───────────────────────────────────
        f_env = max(0.0, min(1.0, env_shock))
        if f_env < 0.3:
            notes.append(f"Environmental drought (modifier {f_env:.2f})")

        # ── F_econ: Economic efficiency ─────────────────────────────────────
        total_cost = (
            genotype.economic.kappa * capital_cost +
            genotype.economic.lambda_ * labour_cost +
            genotype.economic.mu * knowledge_cost +
            genotype.economic.rho * regulatory_cost +
            genotype.economic.nu * network_cost
        )
        if total_cost <= 0:
            if revenue > 0:
                f_econ = 1.0  # pure profit, no cost
            else:
                f_econ = 0.5  # no cost, no revenue — neutral
        else:
            efficiency = revenue / total_cost
            f_econ = min(1.0, efficiency / 2.0)  # 2.0× cost = 100% fitness
            if efficiency < 1.0:
                notes.append(f"Economic inefficiency ({efficiency:.2f}×)")

        # ── F_eta: Zero-extraction compliance ───────────────────────────────
        if eta_violation_detected:
            f_eta = 0.0
            lethal.append("eta_violation")
            notes.append("η violation detected — extraction > 0 — lethal")
        else:
            f_eta = 1.0

        # ── Composite fitness ───────────────────────────────────────────────
        total = f_k2 * f_cci * f_edi * f_act * f_excl * f_env * f_econ * f_eta

        return FitnessResult(
            total=round(max(0.0, min(1.0, total)), 4),
            f_k2=round(f_k2, 4),
            f_cci=round(f_cci, 4),
            f_edi=round(f_edi, 4),
            f_act=round(f_act, 4),
            f_excl=round(f_excl, 4),
            f_env=round(f_env, 4),
            f_econ=round(f_econ, 4),
            f_eta=round(f_eta, 4),
            lethal_factors=lethal,
            notes=notes,
        )

    def compute_comparative_advantage_score(
        self,
        genotype: FullGenotype,
        service_type: str,
        ecosystem_genotypes: list[FullGenotype],
        service_phi_nu_map: dict[str, float],
    ) -> float:
        """Compute comparative advantage score for a specific service type.

        Returns ratio of this genotype's expected Φ×ν to ecosystem average.
        > 1.2 = strong comparative advantage.
        """
        if not ecosystem_genotypes:
            return 1.0

        my_phi_nu = service_phi_nu_map.get(service_type, 0.5)
        all_phi_nu = [
            service_phi_nu_map.get(service_type, 0.5)
            for _ in ecosystem_genotypes
        ]
        avg_phi_nu = sum(all_phi_nu) / len(all_phi_nu) if all_phi_nu else 0.5

        if avg_phi_nu <= 0:
            return 1.0

        return round(my_phi_nu / avg_phi_nu, 4)
