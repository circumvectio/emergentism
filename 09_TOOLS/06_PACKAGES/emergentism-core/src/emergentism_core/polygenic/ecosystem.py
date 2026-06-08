"""Ecosystem orchestration: Chapter, Ecosystem, and EvolutionCycle.

A Chapter is an economic organism with a 12-dimensional genotype.
An Ecosystem is a collection of Chapters with trade relationships.
An EvolutionCycle executes one biological generation:
  1. Environmental fluctuation
  2. Coevolution (competitive pressure + mutualism)
  3. Horizontal gene transfer
  4. Mutation (caste + economic + CNV + factor substitution)
  5. Selection (stabilising + directional)
  6. Competitive exclusion check
  7. Speciation (founder effect)
  8. Extinction
  9. Carrying capacity enforcement
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from .genotype import FullGenotype, CasteBlock, EconomicBlock
from .mutation import MutationEngine
from .fitness import FitnessLandscape, FitnessResult
from .trade import TradeReceipt, ComparativeAdvantageMap


# ─────────────────────────────────────────────────────────────────────────────
# CHAPTER — economic organism
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Chapter:
    id: str
    name: str
    description: str
    status: str = "ACTIVE"  # ACTIVE|EMERGING|PROPOSED|PLANNED|DORMANT|LATENT|EXTINCT
    primary_phenotype: str = ""
    genotype: FullGenotype = field(default_factory=FullGenotype)

    # Speciation signals
    novelty_events: list[str] = field(default_factory=list)
    design_requests: list[str] = field(default_factory=list)
    transaction_count: int = 0
    external_demand: list[str] = field(default_factory=list)

    # K2 performance
    k2_signatures: int = 0
    k2_refusals: int = 0
    k2_conditional: int = 0

    # Activity
    last_activity: str = ""
    activity_count: int = 0

    # Economic performance
    revenue: float = 0.0
    capital_cost: float = 0.0
    labour_cost: float = 0.0
    knowledge_cost: float = 0.0
    regulatory_cost: float = 0.0
    network_cost: float = 0.0
    eta_violation: bool = False

    # Lineage
    parent_chapter: Optional[str] = None
    generation_number: int = 0
    phylogenetic_depth: int = 0

    # Cluster & routing
    cluster: str = ""
    canonical_path: str = ""

    # Metadata
    created_at: str = ""
    notes: str = ""

    # Runtime
    _fitness: Optional[FitnessResult] = field(default=None, repr=False)

    @property
    def total_k2(self) -> int:
        return self.k2_signatures + self.k2_refusals + self.k2_conditional

    @property
    def k2_approval_rate(self) -> float:
        if self.total_k2 == 0:
            return 0.0
        return self.k2_signatures / self.total_k2

    @property
    def k2_refusal_rate(self) -> float:
        if self.total_k2 == 0:
            return 0.0
        return self.k2_refusals / self.total_k2

    @property
    def cci(self) -> float:
        return self.genotype.caste.compute_cci()

    @property
    def edi(self) -> float:
        return self.genotype.economic.compute_edi()

    @property
    def inactivity_days(self) -> int:
        if not self.last_activity:
            return 9999
        try:
            last = datetime.fromisoformat(self.last_activity.replace("Z", "+00:00"))
            return (datetime.now(timezone.utc) - last).days
        except ValueError:
            return 9999

    @property
    def is_active(self) -> bool:
        return self.status not in ("EXTINCT", "DORMANT")

    @property
    def speciation_readiness(self) -> str:
        n = self._novelty_met()
        d = self._design_met()
        r = self._repeatability_met()
        score = sum([n, d, r])
        if score >= 3:
            return "ready"
        if score >= 2:
            return "building"
        if score >= 1:
            return "latent"
        return "dormant"

    def _cutoff(self, days: int) -> str:
        return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    def _novelty_met(self) -> bool:
        cutoff = self._cutoff(60)
        return len([e for e in self.novelty_events if e >= cutoff]) >= 3

    def _design_met(self) -> bool:
        cutoff = self._cutoff(90)
        return len([e for e in self.design_requests if e >= cutoff]) >= 5

    def _repeatability_met(self) -> bool:
        return self.transaction_count >= 3

    def compute_fitness(
        self,
        landscape: FitnessLandscape,
        competitor_genotypes: Optional[list[FullGenotype]] = None,
        env_shock: float = 1.0,
    ) -> FitnessResult:
        self._fitness = landscape.compute(
            genotype=self.genotype,
            k2_signatures=self.k2_signatures,
            k2_refusals=self.k2_refusals,
            k2_conditional=self.k2_conditional,
            last_activity_iso=self.last_activity,
            activity_count=self.activity_count,
            competitor_genotypes=competitor_genotypes,
            env_shock=env_shock,
            revenue=self.revenue,
            capital_cost=self.capital_cost,
            labour_cost=self.labour_cost,
            knowledge_cost=self.knowledge_cost,
            regulatory_cost=self.regulatory_cost,
            network_cost=self.network_cost,
            eta_violation_detected=self.eta_violation,
        )
        return self._fitness

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "primary_phenotype": self.primary_phenotype,
            "genotype": self.genotype.to_dict(),
            "novelty_events": self.novelty_events,
            "design_requests": self.design_requests,
            "transaction_count": self.transaction_count,
            "external_demand": self.external_demand,
            "k2_signatures": self.k2_signatures,
            "k2_refusals": self.k2_refusals,
            "k2_conditional": self.k2_conditional,
            "last_activity": self.last_activity,
            "activity_count": self.activity_count,
            "revenue": self.revenue,
            "capital_cost": self.capital_cost,
            "labour_cost": self.labour_cost,
            "knowledge_cost": self.knowledge_cost,
            "regulatory_cost": self.regulatory_cost,
            "network_cost": self.network_cost,
            "eta_violation": self.eta_violation,
            "parent_chapter": self.parent_chapter,
            "generation_number": self.generation_number,
            "phylogenetic_depth": self.phylogenetic_depth,
            "cluster": self.cluster,
            "canonical_path": self.canonical_path,
            "created_at": self.created_at,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Chapter":
        return cls(
            id=d["id"],
            name=d["name"],
            description=d.get("description", ""),
            status=d.get("status", "ACTIVE"),
            primary_phenotype=d.get("primary_phenotype", ""),
            genotype=FullGenotype.from_dict(d.get("genotype", {})),
            novelty_events=d.get("novelty_events", []),
            design_requests=d.get("design_requests", []),
            transaction_count=d.get("transaction_count", 0),
            external_demand=d.get("external_demand", []),
            k2_signatures=d.get("k2_signatures", 0),
            k2_refusals=d.get("k2_refusals", 0),
            k2_conditional=d.get("k2_conditional", 0),
            last_activity=d.get("last_activity", ""),
            activity_count=d.get("activity_count", 0),
            revenue=d.get("revenue", 0.0),
            capital_cost=d.get("capital_cost", 0.0),
            labour_cost=d.get("labour_cost", 0.0),
            knowledge_cost=d.get("knowledge_cost", 0.0),
            regulatory_cost=d.get("regulatory_cost", 0.0),
            network_cost=d.get("network_cost", 0.0),
            eta_violation=d.get("eta_violation", False),
            parent_chapter=d.get("parent_chapter"),
            generation_number=d.get("generation_number", 0),
            phylogenetic_depth=d.get("phylogenetic_depth", 0),
            cluster=d.get("cluster", ""),
            canonical_path=d.get("canonical_path", ""),
            created_at=d.get("created_at", ""),
            notes=d.get("notes", ""),
        )


# ─────────────────────────────────────────────────────────────────────────────
# ECOSYSTEM
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Ecosystem:
    chapters: list[Chapter] = field(default_factory=list)
    generation: int = 0
    last_evolution: Optional[str] = None
    environment: dict = field(default_factory=dict)
    trade_map: ComparativeAdvantageMap = field(default_factory=ComparativeAdvantageMap)

    def get_active(self) -> list[Chapter]:
        return [c for c in self.chapters if c.is_active]

    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        for c in self.chapters:
            if c.id == chapter_id:
                return c
        return None

    def add_chapter(self, chapter: Chapter):
        self.chapters.append(chapter)

    def record_trade(self, receipt: TradeReceipt):
        self.trade_map.add_receipt(receipt)

    def to_dict(self) -> dict:
        return {
            "chapters": {c.id: c.to_dict() for c in self.chapters},
            "generation": self.generation,
            "last_evolution": self.last_evolution,
            "environment": self.environment,
            "trade_map": self.trade_map.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Ecosystem":
        chapters = [Chapter.from_dict(c) for c in d.get("chapters", {}).values()]
        eco = cls(
            chapters=chapters,
            generation=d.get("generation", 0),
            last_evolution=d.get("last_evolution"),
            environment=d.get("environment", {}),
        )
        # Restore trade receipts if present
        for receipt_dict in d.get("trade_map", {}).get("receipts", []):
            eco.trade_map.add_receipt(TradeReceipt.from_dict(receipt_dict))
        return eco

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)

    @classmethod
    def load(cls, path: Path) -> "Ecosystem":
        if not path.exists():
            return cls()
        with open(path) as f:
            return cls.from_dict(json.load(f))


# ─────────────────────────────────────────────────────────────────────────────
# EVOLUTION CYCLE
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class EvolutionResult:
    generation: int
    events: list[dict]
    speciation_count: int
    extinction_count: int
    mutation_count: int
    hgt_count: int
    coev_count: int
    excl_count: int
    fitness_results: dict[str, FitnessResult]


class EvolutionCycle:
    """Execute one full biological generation on an ecosystem."""

    # Speciation constants
    FOUNDER_EFFECT_NOISE = 0.10
    CARRYING_CAPACITY_PER_CLUSTER = 5
    INACTIVITY_CRITICAL_DAYS = 360
    CCI_PATHOLOGICAL = 0.500
    K2_REFUSAL_RATE_TRIGGER = 0.80
    COEVOLUTION_RATE = 0.05
    COEVOLUTION_STRENGTH = 0.10
    ENV_FLUCTUATION_AMP = 0.05
    ENV_DROUGHT_CHANCE = 0.02

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()
        self.landscape = FitnessLandscape()
        self.mutator = MutationEngine(self.rng)

    def run(self, ecosystem: Ecosystem, context: Optional[dict] = None) -> EvolutionResult:
        """Execute one evolution cycle. Returns result; mutates ecosystem in place."""
        context = context or {}
        ecosystem.generation += 1
        all_events: list[dict] = []
        active = ecosystem.get_active()

        # 1. Environmental fluctuation
        env_events, env_modifiers = self._environmental_fluctuation(active)
        all_events.extend(env_events)

        # Compute fitness for all chapters
        fitness_results: dict[str, FitnessResult] = {}
        for ch in ecosystem.chapters:
            competitors = [c.genotype for c in active if c.id != ch.id]
            fitness_results[ch.id] = ch.compute_fitness(
                landscape=self.landscape,
                competitor_genotypes=competitors,
                env_shock=env_modifiers.get(ch.id, 1.0),
            )

        # 2. Coevolution
        coev_events = self._coevolution(active, fitness_results)
        all_events.extend(coev_events)

        # 3. Horizontal gene transfer
        hgt_events = self._horizontal_transfer(active, fitness_results)
        all_events.extend(hgt_events)

        # 4. Mutation (caste + economic + CNV + factor sub)
        mut_events = []
        for ch in active:
            events = self.mutator.mutate(ch.genotype, ch.id, context=context)
            mut_events.extend([e.to_dict() for e in events])
        all_events.extend(mut_events)

        # 5. Selection (stabilising)
        sel_events = self._selection(active)
        all_events.extend(sel_events)

        # 6. Competitive exclusion check
        excl_events = self._competitive_exclusion(active, fitness_results)
        all_events.extend(excl_events)

        # 7. Speciation
        spec_events, offspring = self._speciation(active)
        all_events.extend(spec_events)
        ecosystem.chapters.extend(offspring)

        # 8. Extinction
        ext_events = self._extinction(ecosystem.chapters)
        all_events.extend(ext_events)

        # 9. Carrying capacity
        cap_events = self._carrying_capacity(ecosystem.chapters)
        all_events.extend(cap_events)

        ecosystem.last_evolution = datetime.now(timezone.utc).isoformat()
        ecosystem.environment = {
            "is_drought": any(e.get("type") == "ENVIRONMENTAL_DROUGHT" for e in all_events),
            "avg_fitness": round(
                sum(f.total for f in fitness_results.values()) / len(fitness_results), 4
            ) if fitness_results else 0,
        }

        return EvolutionResult(
            generation=ecosystem.generation,
            events=all_events,
            speciation_count=len(offspring),
            extinction_count=len([e for e in all_events if e.get("type") in ("EXTINCTION", "DORMANCY")]),
            mutation_count=len([e for e in all_events if "MUTATION" in e.get("type", "")]),
            hgt_count=len([e for e in all_events if "HORIZONTAL_TRANSFER" in e.get("type", "")]),
            coev_count=len([e for e in all_events if "COEVOLUTION" in e.get("type", "")]),
            excl_count=len([e for e in all_events if e.get("type") == "COMPETITIVE_EXCLUSION_WARNING"]),
            fitness_results=fitness_results,
        )

    def _environmental_fluctuation(self, chapters: list[Chapter]) -> tuple[list[dict], dict[str, float]]:
        events = []
        modifiers = {}
        is_drought = self.rng.random() < self.ENV_DROUGHT_CHANCE

        for ch in chapters:
            if is_drought:
                shock = self.rng.uniform(0.2, 0.4)
                modifiers[ch.id] = shock
                events.append({
                    "type": "ENVIRONMENTAL_DROUGHT",
                    "chapter": ch.id,
                    "modifier": round(shock, 4),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
            else:
                noise = self.rng.gauss(0, self.ENV_FLUCTUATION_AMP)
                modifiers[ch.id] = round(max(0.7, min(1.3, 1.0 + noise)), 4)

        return events, modifiers

    def _coevolution(self, active: list[Chapter], fitness_map: dict[str, FitnessResult]) -> list[dict]:
        events = []
        if len(active) < 2:
            return events

        for ch in active:
            if self.rng.random() > self.COEVOLUTION_RATE:
                continue
            fitness = fitness_map.get(ch.id)
            if not fitness:
                continue

            for competitor in active:
                if competitor.id == ch.id:
                    continue
                dist = ch.genotype.distance_to(competitor.genotype)
                comp_fitness = fitness_map.get(competitor.id)
                if not comp_fitness:
                    continue

                if dist < 0.25 and fitness.total < comp_fitness.total:
                    # Niche partition: loser shifts away
                    dom = competitor.genotype.caste.dominant_levels()
                    if dom:
                        lvl = self.rng.choice(dom)
                        ch.genotype.caste.apply_vertical_mutation(lvl, -self.COEVOLUTION_STRENGTH * 0.5)
                        events.append({
                            "type": "COEVOLUTION_NICHE_PARTITION",
                            "chapter": ch.id,
                            "competitor": competitor.id,
                            "level": lvl,
                            "distance": round(dist, 4),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
                elif dist > 0.55 and fitness.total > 0.4 and comp_fitness.total > 0.4:
                    # Mutualism: distant phenotypes reinforce
                    dom = ch.genotype.caste.dominant_levels()
                    if dom:
                        lvl = self.rng.choice(dom)
                        ch.genotype.caste.apply_vertical_mutation(lvl, self.COEVOLUTION_STRENGTH * 0.3)
                        events.append({
                            "type": "COEVOLUTION_MUTUALISM",
                            "chapter": ch.id,
                            "partner": competitor.id,
                            "level": lvl,
                            "distance": round(dist, 4),
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        })
        return events

    def _horizontal_transfer(self, active: list[Chapter], fitness_map: dict[str, FitnessResult]) -> list[dict]:
        events = []
        if len(active) < 2:
            return events

        for target in active:
            if self.rng.random() > 0.03:  # HGT rate
                continue

            competitors = [c for c in active if c.id != target.id]
            if not competitors:
                continue

            weights = [fitness_map.get(c.id, FitnessResult(0,0,0,0,0,0,0,0,0,[],[])).total + 0.01 for c in competitors]
            total_w = sum(weights)
            probs = [w / total_w for w in weights]
            donor = self.rng.choices(competitors, weights=probs, k=1)[0]

            mut_events = self.mutator.horizontal_transfer(
                donor.genotype, target.genotype, donor.id, target.id
            )
            events.extend([e.to_dict() for e in mut_events])

        return events

    def _selection(self, active: list[Chapter]) -> list[dict]:
        """Stabilising selection: pull over-specialised chapters toward baseline."""
        events = []
        for ch in active:
            cci = ch.cci
            if cci > 0.200:
                dom = ch.genotype.caste.dominant_levels()
                for lvl in dom:
                    current = getattr(ch.genotype.caste, lvl)
                    new_val = max(1.0, current * 0.90)
                    setattr(ch.genotype.caste, lvl, round(new_val, 4))
                    events.append({
                        "type": "STABILISING_SELECTION",
                        "chapter": ch.id,
                        "level": lvl,
                        "cci": cci,
                        "before": round(current, 4),
                        "after": round(new_val, 4),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
        return events

    def _competitive_exclusion(self, active: list[Chapter], fitness_map: dict[str, FitnessResult]) -> list[dict]:
        events = []
        checked = set()
        for i, a in enumerate(active):
            for b in active[i + 1:]:
                pair = tuple(sorted([a.id, b.id]))
                if pair in checked:
                    continue
                checked.add(pair)
                dist = a.genotype.distance_to(b.genotype)
                if dist < 0.15:
                    fa = fitness_map.get(a.id, FitnessResult(0,0,0,0,0,0,0,0,0,[],[])).total
                    fb = fitness_map.get(b.id, FitnessResult(0,0,0,0,0,0,0,0,0,[],[])).total
                    loser = b.id if fa > fb else a.id
                    events.append({
                        "type": "COMPETITIVE_EXCLUSION_WARNING",
                        "chapter_a": a.id,
                        "chapter_b": b.id,
                        "distance": round(dist, 4),
                        "weakest_chapter": loser,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
        return events

    def _speciation(self, active: list[Chapter]) -> tuple[list[dict], list[Chapter]]:
        events = []
        offspring = []
        for ch in active:
            if ch.speciation_readiness != "ready":
                continue

            parent_vec = ch.genotype.caste.to_list()
            offspring_caste = [
                max(0.3, min(2.0, v + self.rng.uniform(-self.FOUNDER_EFFECT_NOISE, self.FOUNDER_EFFECT_NOISE)))
                for v in parent_vec
            ]
            # Economic block: specialise further in dominant dimension
            parent_econ = ch.genotype.economic.to_list()
            max_idx = parent_econ.index(max(parent_econ))
            offspring_econ = parent_econ.copy()
            offspring_econ[max_idx] = min(0.60, offspring_econ[max_idx] + 0.10)
            # Renormalise
            total = sum(offspring_econ)
            offspring_econ = [v / total for v in offspring_econ]

            child = Chapter(
                id=f"{ch.id}_sp{ch.generation_number + 1}_{datetime.now(timezone.utc).strftime('%Y%m%d')}",
                name=f"{ch.name} (SP{ch.generation_number + 1})",
                description=f"Speciation from {ch.name}. {ch.description}",
                status="EMERGING",
                primary_phenotype=ch.primary_phenotype,
                genotype=FullGenotype(
                    caste=CasteBlock.from_list(offspring_caste),
                    economic=EconomicBlock.from_list(offspring_econ),
                ),
                parent_chapter=ch.id,
                generation_number=ch.generation_number + 1,
                phylogenetic_depth=ch.phylogenetic_depth + 1,
                cluster=ch.cluster,
                canonical_path=ch.canonical_path,
                created_at=datetime.now(timezone.utc).isoformat(),
                last_activity=datetime.now(timezone.utc).isoformat(),
            )
            offspring.append(child)
            ch.status = "PROPOSED"
            events.append({
                "type": "SPECIATION_EVENT",
                "parent": ch.id,
                "offspring": child.id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        return events, offspring

    def _extinction(self, chapters: list[Chapter]) -> list[dict]:
        events = []
        for ch in chapters:
            reasons = []
            if ch.cci > self.CCI_PATHOLOGICAL:
                reasons.append(f"CCI={ch.cci} > {self.CCI_PATHOLOGICAL}")
            if ch.inactivity_days > self.INACTIVITY_CRITICAL_DAYS:
                reasons.append(f"Inactive {ch.inactivity_days}d > {self.INACTIVITY_CRITICAL_DAYS}d")
            if ch.total_k2 > 0 and ch.k2_refusal_rate > self.K2_REFUSAL_RATE_TRIGGER:
                reasons.append(f"K2 refusal {ch.k2_refusal_rate:.1%} > {self.K2_REFUSAL_RATE_TRIGGER}")
            if ch.eta_violation:
                reasons.append("η violation detected")

            if reasons:
                if ch.inactivity_days > 180 and ch.status != "DORMANT":
                    ch.status = "DORMANT"
                    events.append({
                        "type": "DORMANCY",
                        "chapter": ch.id,
                        "reason": reasons[0],
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
                elif (ch.inactivity_days > self.INACTIVITY_CRITICAL_DAYS or
                      ch.cci > self.CCI_PATHOLOGICAL or
                      ch.eta_violation or
                      (ch.total_k2 > 0 and ch.k2_refusal_rate > self.K2_REFUSAL_RATE_TRIGGER)):
                    ch.status = "EXTINCT"
                    events.append({
                        "type": "EXTINCTION",
                        "chapter": ch.id,
                        "reasons": reasons,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
        return events

    def _carrying_capacity(self, chapters: list[Chapter]) -> list[dict]:
        events = []
        clusters = {}
        for ch in chapters:
            if ch.is_active and ch.cluster:
                clusters.setdefault(ch.cluster, []).append(ch.id)
        for cluster, members in clusters.items():
            if len(members) > self.CARRYING_CAPACITY_PER_CLUSTER:
                events.append({
                    "type": "CARRYING_CAPACITY_EXCEEDED",
                    "cluster": cluster,
                    "chapter_count": len(members),
                    "capacity": self.CARRYING_CAPACITY_PER_CLUSTER,
                    "members": members,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                })
        return events
