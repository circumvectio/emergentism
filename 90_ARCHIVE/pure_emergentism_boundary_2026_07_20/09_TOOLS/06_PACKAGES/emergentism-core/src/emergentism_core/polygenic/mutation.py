"""Biological mutation operators for the 12-dimensional polygenic genotype.

Mutation laws (grounded in population genetics):
  1. Point mutation: most common (~70%), single-dimension perturbation.
  2. Copy number variation (~15%): duplication or deletion of caste emphasis.
  3. Horizontal gene transfer (~10%): inter-chapter capability borrowing.
  4. Factor substitution (~4%): swap mass between economic dimensions.
  5. Regulatory shock (~0.9%): ρ spike on jurisdiction change.
  6. Network amplification (~0.1%): ν increase on Metcalfe threshold crossing.

All mutations respect constitutional invariants:
  - η ≥ 0 (no extraction)
  - K2 signature required for lethal mutations
  - Economic block sum-to-1.0 maintained
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from .genotype import (
    EconomicBlock,
    FullGenotype,
    CASTE_LEVELS,
    CASTE_MIN,
    CASTE_MAX,
    STRUCTURAL_LEVELS,
    ECONOMIC_DIMS,
)


# ─────────────────────────────────────────────────────────────────────────────
# BIOLOGICAL CONSTANTS — governed by K2 (human-adjustable)
# ─────────────────────────────────────────────────────────────────────────────

MUTATION_RATE_VERTICAL = 0.08      # per caste level per generation
MUTATION_AMPLITUDE = 0.15          # ±15% max shift per caste dimension
MUTATION_RATE_ECONOMIC = 0.12      # per generation (higher than caste — markets move faster)
MUTATION_ECONOMIC_AMP = 0.10       # ±10% Dirichlet concentration perturbation

CNV_RATE = 0.03                    # copy number variation rate
CNV_DUPLICATION_BOOST = 1.4        # multiply duplicated level by this
CNV_DELETION_PENALTY = 0.6         # multiply deleted level by this

HGT_RATE = 0.03                    # horizontal gene transfer per active pair
HGT_CONVERGENCE = 0.30             # 30% gap closure per HGT event
HGT_TRANSFERABLE_CASTE = ["L2", "L3", "L4", "L6"]  # not L1/L5/L7 (structural)
HGT_TRANSFERABLE_ECON = ["kappa", "lambda", "mu", "nu"]  # not rho (jurisdiction-bound)

FACTOR_SUB_RATE = 0.02             # factor substitution rate
FACTOR_SUB_MAG = 0.15              # mass swapped between dimensions

REGULATORY_SHOCK_RATE = 0.005      # rare: new jurisdiction entered
REGULATORY_SHOCK_AMP = 0.25        # ρ spike amplitude

NETWORK_AMPLIFICATION_RATE = 0.001  # very rare: network crosses threshold
NETWORK_AMPLIFICATION_AMP = 0.20   # ν increase


@dataclass
class MutationEvent:
    type: str
    chapter_id: str
    timestamp: str
    details: dict

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "chapter": self.chapter_id,
            "timestamp": self.timestamp,
            **self.details,
        }


class MutationEngine:
    """Executes all mutation operators with biological fidelity."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    # ── Caste point mutation ────────────────────────────────────────────────

    def point_mutation_caste(self, genotype: FullGenotype, chapter_id: str) -> list[MutationEvent]:
        """Vertical mutation: random drift in caste emphasis weights.

        Biological law: each L-level has MUTATION_RATE_VERTICAL chance of drift.
        Structural levels (L1, L5, L7) have 50% lower mutation rate.
        """
        events = []
        for lvl in CASTE_LEVELS:
            rate = MUTATION_RATE_VERTICAL * (0.5 if lvl in STRUCTURAL_LEVELS else 1.0)
            if self.rng.random() >= rate:
                continue

            current = getattr(genotype.caste, lvl)
            shift = self.rng.gauss(0, MUTATION_AMPLITUDE / 2)
            new_val = max(CASTE_MIN, min(CASTE_MAX, current + shift))

            if abs(new_val - current) > 0.01:
                setattr(genotype.caste, lvl, round(new_val, 4))
                events.append(MutationEvent(
                    type="POINT_MUTATION_CASTE",
                    chapter_id=chapter_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={
                        "level": lvl,
                        "before": round(current, 4),
                        "after": round(new_val, 4),
                        "shift": round(shift, 4),
                    },
                ))
        return events

    # ── Economic drift mutation ─────────────────────────────────────────────

    def point_mutation_economic(self, genotype: FullGenotype, chapter_id: str) -> list[MutationEvent]:
        """Economic drift: Dirichlet perturbation of intensity proportions.

        Biological law: markets move faster than cognition. Economic block mutates
        at 1.5× the caste rate. Uses Dirichlet distribution to maintain sum=1.0.
        """
        if self.rng.random() >= MUTATION_RATE_ECONOMIC:
            return []

        events = []
        vals = genotype.economic.to_list()
        before = vals.copy()

        # Dirichlet perturbation: add small random mass to each dimension
        # then renormalise. This is biologically realistic for proportions.
        perturbations = [self.rng.gauss(0, MUTATION_ECONOMIC_AMP) for _ in range(5)]
        new_vals = [max(0.001, v + p) for v, p in zip(vals, perturbations)]
        total = sum(new_vals)
        new_vals = [v / total for v in new_vals]

        # Apply back
        genotype.economic.kappa = round(new_vals[0], 6)
        genotype.economic.lambda_ = round(new_vals[1], 6)
        genotype.economic.mu = round(new_vals[2], 6)
        genotype.economic.rho = round(new_vals[3], 6)
        genotype.economic.nu = round(1.0 - sum(new_vals[:4]), 6)

        # Record which dimensions changed most
        changes = {
            name: round(new - old, 4)
            for name, old, new in zip(ECONOMIC_DIMS, before, new_vals)
            if abs(new - old) > 0.005
        }

        if changes:
            events.append(MutationEvent(
                type="POINT_MUTATION_ECONOMIC",
                chapter_id=chapter_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={
                    "before": {n: round(v, 4) for n, v in zip(ECONOMIC_DIMS, before)},
                    "after": {n: round(v, 4) for n, v in zip(ECONOMIC_DIMS, new_vals)},
                    "changes": changes,
                },
            ))
        return events

    # ── Copy number variation ───────────────────────────────────────────────

    def copy_number_variation(self, genotype: FullGenotype, chapter_id: str) -> list[MutationEvent]:
        """CNV: duplication or deletion of a caste emphasis weight.

        Biological law: gene duplication creates redundancy; deletion creates
        dependency. In economic terms: duplication = double-down on specialisation;
        deletion = pivot away from a function.
        """
        if self.rng.random() >= CNV_RATE:
            return []

        events = []
        lvl = self.rng.choice(CASTE_LEVELS)
        current = getattr(genotype.caste, lvl)

        if self.rng.random() < 0.5:
            # Duplication: boost this level, reduce others proportionally
            new_val = min(CASTE_MAX, current * CNV_DUPLICATION_BOOST)
            factor = (sum(genotype.caste.to_list()) - current + new_val) / sum(genotype.caste.to_list())
            for level in CASTE_LEVELS:
                if level == lvl:
                    setattr(genotype.caste, lvl, round(new_val, 4))
                else:
                    v = getattr(genotype.caste, level)
                    setattr(genotype.caste, level, round(v / factor, 4))
            event_type = "CNV_DUPLICATION"
        else:
            # Deletion: reduce this level, boost others proportionally
            new_val = max(CASTE_MIN, current * CNV_DELETION_PENALTY)
            factor = (sum(genotype.caste.to_list()) - current + new_val) / sum(genotype.caste.to_list())
            for level in CASTE_LEVELS:
                if level == lvl:
                    setattr(genotype.caste, lvl, round(new_val, 4))
                else:
                    v = getattr(genotype.caste, level)
                    setattr(genotype.caste, level, round(v / factor, 4))
            event_type = "CNV_DELETION"

        genotype.caste = genotype.caste.clamp()

        events.append(MutationEvent(
            type=event_type,
            chapter_id=chapter_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details={
                "level": lvl,
                "before": round(current, 4),
                "after": round(getattr(genotype.caste, lvl), 4),
            },
        ))
        return events

    # ── Horizontal gene transfer ────────────────────────────────────────────

    def horizontal_transfer(
        self,
        donor: FullGenotype,
        receiver: FullGenotype,
        donor_id: str,
        receiver_id: str,
    ) -> list[MutationEvent]:
        """HGT: capability adoption across phenotypes.

        Biological law: non-lethal capability borrowing. Fitness-weighted donors.
        Only transferable levels (L2/L3/L4/L6, κ/λ/μ/ν) — not structural/jurisdiction.
        """
        if self.rng.random() >= HGT_RATE:
            return []

        events = []
        # 50% chance caste, 50% chance economic
        if self.rng.random() < 0.5:
            # Caste HGT
            lvl = self.rng.choice(HGT_TRANSFERABLE_CASTE)
            donor_val = getattr(donor.caste, lvl)
            target_val = getattr(receiver.caste, lvl)
            gap = donor_val - target_val
            transfer = gap * HGT_CONVERGENCE
            if abs(transfer) > 0.02:
                new_val = max(CASTE_MIN, min(CASTE_MAX, target_val + transfer))
                setattr(receiver.caste, lvl, round(new_val, 4))
                events.append(MutationEvent(
                    type="HORIZONTAL_TRANSFER_CASTE",
                    chapter_id=receiver_id,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    details={
                        "donor": donor_id,
                        "level": lvl,
                        "donor_value": round(donor_val, 4),
                        "target_before": round(target_val, 4),
                        "target_after": round(new_val, 4),
                        "transfer_amount": round(transfer, 4),
                    },
                ))
        else:
            # Economic HGT
            dim = self.rng.choice(HGT_TRANSFERABLE_ECON)
            donor_val = getattr(donor.economic, dim)
            target_val = getattr(receiver.economic, dim)
            gap = donor_val - target_val
            transfer = gap * HGT_CONVERGENCE
            if abs(transfer) > 0.01:
                # Apply transfer while maintaining sum=1.0
                old_vals = receiver.economic.to_list()
                dim_idx = ECONOMIC_DIMS.index(dim)
                new_vals = old_vals.copy()
                new_vals[dim_idx] = max(0.0, min(1.0, target_val + transfer))
                # Renormalise
                total = sum(new_vals)
                if total > 0:
                    new_vals = [v / total for v in new_vals]
                    receiver.economic = EconomicBlock.from_list(new_vals)
                    events.append(MutationEvent(
                        type="HORIZONTAL_TRANSFER_ECONOMIC",
                        chapter_id=receiver_id,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                        details={
                            "donor": donor_id,
                            "dimension": dim,
                            "donor_value": round(donor_val, 4),
                            "target_before": round(target_val, 4),
                            "target_after": round(getattr(receiver.economic, dim), 4),
                            "transfer_amount": round(transfer, 4),
                        },
                    ))
        return events

    # ── Factor substitution ─────────────────────────────────────────────────

    def factor_substitution(self, genotype: FullGenotype, chapter_id: str) -> list[MutationEvent]:
        """Factor substitution: swap mass between economic dimensions.

        Biological law: when technology permits, organisms substitute factors.
        Example: AI reduces λ (labour), increases μ (knowledge).
        Triggered by L5 redesign + L6 compression in the phenotype.
        """
        if self.rng.random() >= FACTOR_SUB_RATE:
            return []

        events = []
        # Pick two distinct dimensions
        dims = self.rng.sample(ECONOMIC_DIMS, 2)
        source, target = dims[0], dims[1]
        source_val = getattr(genotype.economic, source)
        target_val = getattr(genotype.economic, target)

        # Transfer mass from source to target
        transfer = min(source_val * FACTOR_SUB_MAG, source_val - 0.05)
        if transfer > 0.01:
            new_source = source_val - transfer
            new_target = target_val + transfer
            setattr(genotype.economic, source, round(new_source, 6))
            setattr(genotype.economic, target, round(new_target, 6))
            # Renormalise to maintain sum=1.0
            genotype.economic = EconomicBlock.from_list(genotype.economic.to_list())

            events.append(MutationEvent(
                type="FACTOR_SUBSTITUTION",
                chapter_id=chapter_id,
                timestamp=datetime.now(timezone.utc).isoformat(),
                details={
                    "source": source,
                    "target": target,
                    "transfer_amount": round(transfer, 4),
                    "before": {source: round(source_val, 4), target: round(target_val, 4)},
                    "after": {
                        source: round(getattr(genotype.economic, source), 4),
                        target: round(getattr(genotype.economic, target), 4),
                    },
                },
            ))
        return events

    # ── Regulatory shock ────────────────────────────────────────────────────

    def regulatory_shock(
        self,
        genotype: FullGenotype,
        chapter_id: str,
        jurisdiction_change: bool = False,
    ) -> list[MutationEvent]:
        """Regulatory shock: ρ spike when entering new jurisdiction.

        Biological law: environmental stress induces phenotypic plasticity.
        Entering UK FCA or SAMA sandbox dramatically increases regulatory burden.
        """
        if not jurisdiction_change and self.rng.random() >= REGULATORY_SHOCK_RATE:
            return []

        events = []
        current_rho = genotype.economic.rho
        spike = REGULATORY_SHOCK_AMP * (1.0 if jurisdiction_change else self.rng.uniform(0.5, 1.0))
        new_rho = min(0.60, current_rho + spike)  # cap at 60% (still must leave room)

        # Reduce other dimensions proportionally to maintain sum=1.0
        old_vals = genotype.economic.to_list()
        rho_idx = ECONOMIC_DIMS.index("rho")
        other_total = sum(old_vals[:rho_idx] + old_vals[rho_idx + 1:])
        scale = (1.0 - new_rho) / other_total if other_total > 0 else 0.0

        new_vals = []
        for i, v in enumerate(old_vals):
            if i == rho_idx:
                new_vals.append(new_rho)
            else:
                new_vals.append(v * scale)

        genotype.economic = EconomicBlock.from_list(new_vals)

        events.append(MutationEvent(
            type="REGULATORY_SHOCK",
            chapter_id=chapter_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details={
                "rho_before": round(current_rho, 4),
                "rho_after": round(new_rho, 4),
                "spike_magnitude": round(spike, 4),
                "jurisdiction_change": jurisdiction_change,
            },
        ))
        return events

    # ── Network amplification ───────────────────────────────────────────────

    def network_amplification(
        self,
        genotype: FullGenotype,
        chapter_id: str,
        node_count: int = 0,
        metcalfe_threshold: int = 100,
    ) -> list[MutationEvent]:
        """Network amplification: ν increase when node count crosses threshold.

        Biological law: network effects are threshold-dependent (Metcalfe's law).
        Below threshold: minimal ν. Above threshold: rapid amplification.
        """
        if node_count < metcalfe_threshold:
            return []
        if self.rng.random() >= NETWORK_AMPLIFICATION_RATE:
            return []

        events = []
        current_nu = genotype.economic.nu
        # Amplification proportional to log of node count above threshold
        amplification = NETWORK_AMPLIFICATION_AMP * math.log10(node_count / metcalfe_threshold + 1)
        new_nu = min(0.50, current_nu + amplification)

        old_vals = genotype.economic.to_list()
        nu_idx = ECONOMIC_DIMS.index("nu")
        other_total = sum(old_vals[:nu_idx] + old_vals[nu_idx + 1:])
        scale = (1.0 - new_nu) / other_total if other_total > 0 else 0.0

        new_vals = []
        for i, v in enumerate(old_vals):
            if i == nu_idx:
                new_vals.append(new_nu)
            else:
                new_vals.append(v * scale)

        genotype.economic = EconomicBlock.from_list(new_vals)

        events.append(MutationEvent(
            type="NETWORK_AMPLIFICATION",
            chapter_id=chapter_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details={
                "nu_before": round(current_nu, 4),
                "nu_after": round(new_nu, 4),
                "node_count": node_count,
                "threshold": metcalfe_threshold,
                "amplification": round(amplification, 4),
            },
        ))
        return events

    # ── Master mutation method ──────────────────────────────────────────────

    def mutate(
        self,
        genotype: FullGenotype,
        chapter_id: str,
        context: Optional[dict] = None,
    ) -> list[MutationEvent]:
        """Execute all mutation operators in biological priority order.

        Returns list of all mutation events that occurred.
        """
        context = context or {}
        all_events: list[MutationEvent] = []

        # 1. Point mutations (most common)
        all_events.extend(self.point_mutation_caste(genotype, chapter_id))
        all_events.extend(self.point_mutation_economic(genotype, chapter_id))

        # 2. Copy number variation
        all_events.extend(self.copy_number_variation(genotype, chapter_id))

        # 3. Factor substitution
        all_events.extend(self.factor_substitution(genotype, chapter_id))

        # 4. Regulatory shock (if jurisdiction change detected)
        if context.get("jurisdiction_change"):
            all_events.extend(self.regulatory_shock(
                genotype, chapter_id, jurisdiction_change=True
            ))

        # 5. Network amplification (if node count provided)
        node_count = context.get("node_count", 0)
        if node_count > 0:
            all_events.extend(self.network_amplification(
                genotype, chapter_id, node_count=node_count,
                metcalfe_threshold=context.get("metcalfe_threshold", 100)
            ))

        return all_events
