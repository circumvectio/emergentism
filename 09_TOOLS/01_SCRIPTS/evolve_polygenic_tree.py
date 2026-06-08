#!/usr/bin/env python3
"""
evolve_polygenic_tree.py — v3.1 self-contained (no external deps)
Polygenic Economic Evolution Engine CLI.

Biological laws:
  Mutation   — point / CNV / factor substitution / regulatory shock / network amplification
  Selection  — stabilising: CCI > 0.50 → pull toward uniform baseline
  Red Queen  — absolute: raw_fitness < 0.25 → mutation pressure (top ~5% selected)
  Frequency  — rare phenotype bonus when avg CCI > 0.10
  Arms race  — directional push toward L4 when competitor gap > 0.20
  Mutualism  — cross-chapter compatibility boost
  HGT        — 3% chance per pair → capability borrowing (L2/L3/L4 only)
  Exaptation — accidental market alignment when dominant L > 0.65
  Speciation — chi-sq + variance + 3 signals met → offspring with founder drift
  Extinction — CCI > 0.60 OR inactive > 180d OR K2 refusal > 80%
  Regime     — COMPLIANCE/GROWTH/STABILITY/INNOVATION, persisted across runs
  Founder    — offspring = parent ± 0.08 gaussian drift + dominant boost
  r/K        — ACTIVE/K → 0.05/level; FORMING/r → 0.15/level
  Phylogeny  — lineage chain; distance to parent measured each generation

Usage:
    python3 evolve_polygenic_tree.py --init
    python3 evolve_polygenic_tree.py --scan
    python3 evolve_polygenic_tree.py --all
    python3 evolve_polygenic_tree.py --all --seed 42 --ngen 30
    python3 evolve_polygenic_tree.py --feed-k2 ch01_tokencen sign
    python3 evolve_polygenic_tree.py --report
    python3 evolve_polygenic_tree.py --phylo
    python3 evolve_polygenic_tree.py --mutate ch01_tokencen
"""

import argparse
import json
import math
import random
import re
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# ─── PATHS ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent
EMER_ROOT    = SCRIPT_DIR.parent.parent.parent
AGENTZ_SPEC  = EMER_ROOT / "02_SKYZAI/01_NOOSPHERE/02_INFRASTRUCTURE/Cascade/08_AGENTZ_CLOUD_PWA/01_POLYGENETIC_TREE"
ECOSYSTEM_PATH = AGENTZ_SPEC / "09_POLYGENETIC_ECOSYSTEM.json"
EVOLUTION_LOG = AGENTZ_SPEC / "09_EVOLUTION_LOG.jsonl"
EVOLUTION_REPORT = AGENTZ_SPEC / "09_EVOLUTION_REPORT.md"

# ─── BIOLOGICAL CONSTANTS ─────────────────────────────────────────────────────
R_Q_THRESHOLD          = 0.30    # Red Queen survival threshold (absolute fitness)
RED_QUEEN_PRESSURE     = 0.05    # mutation bonus when below threshold
PUNCTUATION_PERIOD     = 7       # generations of stasis before burst possible
PUNCTUATION_BURST      = 0.10    # probability of burst at stasis >= period
MUT_AMPLITUDE          = 0.15    # max shift per point mutation
MUT_RATE_K             = 0.05    # per-level probability — K-strategist (ACTIVE)
MUT_RATE_R             = 0.15    # per-level probability — r-strategist (PLANNED)
HGT_RATE               = 0.03    # probability per active pair → transfer
COEV_RATE              = 0.05    # probability per active pair → mutualism
FREQ_BONUS             = 0.04    # rare-phenotype bonus
FREQ_PENALTY           = 0.04    # common-phenotype penalty
FREQ_THRESHOLD         = 0.25    # avg CCI threshold for frequency effects
REGIME_SHIFT_PROB       = 0.10    # probability of regime shift each generation
REGIME_HYSTERESIS       = 0.50    # stay-in-current-regime probability on shift
EXAPTATION_PROB        = 0.05    # probability per chapter per generation
EXAPTATION_BOOST       = 0.06    # fitness bonus on exaptation
CCI_FORMING_MAX        = 0.200   # healthy CCI upper bound
CCI_SELECT_PRESSURE    = 0.50    # CCI > this → stabilising selection fires
CCI_EXTINCT            = 0.60    # CCI > this → extinction candidate
INACTIVITY_WARN        = 90      # days before warning
INACTIVITY_KILL        = 180     # days before extinction
K2_REFUSAL_KILL        = 0.80   # refusal rate > this → extinction
TRADE_SPECIAL_BOOST    = 0.06    # fitness bonus per trade specialisation
F_DRIFT_SIGMA          = 0.08    # founder effect gaussian drift std dev
CARRYING_CAPACITY      = 3       # max chapters per cluster
CHI_SQ_CRIT            = 12.592  # chi-sq critical value (df=6, p=0.05)

# Regime peak emphasis vectors (7 L-levels, normalised)
REGIME_PEAKS = {
    "COMPLIANCE": [0.30, 0.25, 0.15, 0.10, 0.10, 0.07, 0.03],
    "GROWTH":     [0.10, 0.15, 0.25, 0.30, 0.12, 0.05, 0.03],
    "STABILITY":  [0.08, 0.12, 0.20, 0.25, 0.20, 0.10, 0.05],
    "INNOVATION": [0.05, 0.10, 0.20, 0.30, 0.20, 0.10, 0.05],
}
REGIMES = list(REGIME_PEAKS.keys())


# ─── DATA MODELS ──────────────────────────────────────────────────────────────

class GenotypeEmphasis:
    __slots__ = ("L1","L2","L3","L4","L5","L6","L7")

    def __init__(self, L1=.15, L2=.15, L3=.15, L4=.15, L5=.15, L6=.15, L7=.10):
        self.L1=L1; self.L2=L2; self.L3=L3; self.L4=L4; self.L5=L5; self.L6=L6; self.L7=L7
        self._renormalise()

    @staticmethod
    def from_list(lst):
        if len(lst) == 7:
            return GenotypeEmphasis(*lst)
        raise ValueError(f"Expected 7 values, got {len(lst)}")

    def to_list(self):
        return [self.L1,self.L2,self.L3,self.L4,self.L5,self.L6,self.L7]

    def distance_to(self, other):
        return math.sqrt(sum((a-b)**2 for a,b in zip(self.to_list(), other.to_list())))

    def dominants(self):
        avg = 1.0 / 7.0
        return [f"L{i+1}" for i,v in enumerate(self.to_list()) if v > avg]

    def CCI(self):
        total = sum(self.to_list())
        if total == 0: return 0.0
        shares = [v/total for v in self.to_list()]
        return sum(s*s for s in shares)

    def shift(self, level, delta, rng=None):
        attr = level.upper()
        if not hasattr(self, attr): raise ValueError(f"Unknown level: {level}")
        old = getattr(self, attr)
        new = max(0.0, min(1.0, old + delta))
        setattr(self, attr, new)
        self._renormalise()

    def apply_founder_drift(self, sigma, rng):
        for attr in self.__slots__:
            v = max(0.0, getattr(self, attr) + rng.gauss(0, sigma))
            setattr(self, attr, v)
        self._renormalise()

    def _renormalise(self):
        total = sum(self.to_list())
        if total > 0:
            for attr in self.__slots__:
                setattr(self, attr, max(0.0, min(1.0, getattr(self, attr) / total)))
        else:
            for attr in self.__slots__:
                setattr(self, attr, 1.0/7.0)

    def copy(self):
        return GenotypeEmphasis(*self.to_list())

    def __repr__(self):
        return f"GenotypeEmphasis({','.join(f'{v:.3f}' for v in self.to_list())})"


class SpeciationSignals:
    __slots__ = ("novelty_events","design_requests","k2_signatures","k2_refusals",
                 "k2_conditional","trade_receipts","external_demand_events",
                 "last_novelty","novelty_descriptions")

    def __init__(self, novelty_events=0, design_requests=0, k2_signatures=0,
                 k2_refusals=0, k2_conditional=0, trade_receipts=0,
                 external_demand_events=0, last_novelty="", novelty_descriptions=None):
        self.novelty_events=novelty_events
        self.design_requests=design_requests
        self.k2_signatures=k2_signatures
        self.k2_refusals=k2_refusals
        self.k2_conditional=k2_conditional
        self.trade_receipts=trade_receipts
        self.external_demand_events=external_demand_events
        self.last_novelty=last_novelty
        self.novelty_descriptions=novelty_descriptions or []

    def novelty_met(self):      return self.novelty_events >= 3
    def design_met(self):        return self.design_requests >= 5
    def repeatability_met(self): return (self.k2_signatures + self.k2_refusals + self.k2_conditional) >= 3
    def readiness(self):
        n = sum([self.novelty_met(), self.design_met(), self.repeatability_met()])
        return {3:"ready", 2:"building", 1:"latent"}.get(n, "dormant")
    def chi_sq_test(self):
        obs = [self.novelty_events, self.design_requests, self.k2_signatures,
               self.k2_refusals, self.k2_conditional, self.trade_receipts]
        total = sum(obs) or 1; exp = total/6.0
        return sum((o-exp)**2/exp for o in obs)
    def f_test(self):
        obs = [self.novelty_events, self.design_requests, self.k2_signatures,
               self.k2_refusals, self.k2_conditional, self.trade_receipts]
        n=len(obs)
        if n<2: return 0.0
        m=sum(obs)/n; return sum((x-m)**2 for x in obs)/(n-1) if n>1 else 0.0
    def to_dict(self):
        return {k:getattr(self,k) for k in self.__slots__}
    @staticmethod
    def from_dict(d):
        kw = {k:d.get(k,0) for k in SpeciationSignals.__slots__[:-2]}
        kw["novelty_descriptions"] = d.get("novelty_descriptions", [])
        return SpeciationSignals(**kw)


class Chapter:
    __slots__ = ("id","name","description","status","genotype","signals","strategy_type",
                 "k2_signatures","k2_refusals","k2_conditional","created","last_activity",
                 "trade_receipts","trade_specialisations","lineage","speciation_generation",
                 "_stasis_generations","_cci","_cci_health","_raw_fit")

    def __init__(self, id="", name="", description="", status="PLANNED",
                 genotype=None, signals=None, strategy_type="r",
                 k2_signatures=0, k2_refusals=0, k2_conditional=0,
                 created="", last_activity="", trade_receipts=0,
                 trade_specialisations=None, lineage=None, speciation_generation=0):
        self.id=id; self.name=name; self.description=description; self.status=status
        self.genotype=genotype or GenotypeEmphasis()
        self.signals=signals or SpeciationSignals()
        self.strategy_type=strategy_type
        self.k2_signatures=k2_signatures; self.k2_refusals=k2_refusals
        self.k2_conditional=k2_conditional
        self.created=created; self.last_activity=last_activity
        self.trade_receipts=trade_receipts
        self.trade_specialisations=trade_specialisations or []
        self.lineage=lineage or []; self.speciation_generation=speciation_generation
        self._stasis_generations=0; self._cci=0.0; self._cci_health="FORMING"
        self._raw_fit=0.0

    @property
    def is_active(self):
        return self.status in ("ACTIVE","EMERGING","PROPOSED")

    @property
    def total_k2(self):
        return self.k2_signatures + self.k2_refusals + self.k2_conditional

    @property
    def k2_approval_rate(self):
        return self.k2_signatures / self.total_k2 if self.total_k2 > 0 else 0.4

    @property
    def k2_refusal_rate(self):
        return self.k2_refusals / self.total_k2 if self.total_k2 > 0 else 0.4

    @property
    def inactivity_days(self):
        if not self.last_activity: return 0
        try:
            last = datetime.fromisoformat(self.last_activity)
            delta = datetime.now(timezone.utc) - last
            return max(0, delta.days)
        except Exception:
            return 0

    def base_mutation_rate(self):
        return MUT_RATE_K if self.status in ("ACTIVE","EMERGING") else MUT_RATE_R

    def compute_fitness(self, active_chapters=None, regime_vec=None):
        # F_k2 — Bayesian prior 0.4 + empirical
        f_k2 = self.k2_approval_rate if self.total_k2 > 0 else 0.4

        # F_cci — HHI specialisation
        cci = self.genotype.CCI()
        if cci <= CCI_FORMING_MAX:
            f_cci = 1.0
        elif cci <= CCI_SELECT_PRESSURE:
            f_cci = max(0.3, 1.0 - (cci-CCI_FORMING_MAX)/(CCI_SELECT_PRESSURE-CCI_FORMING_MAX))
        else:
            f_cci = 0.1

        # F_act — inactivity decay
        inact = self.inactivity_days
        if inact <= 30:
            f_act = 1.0
        elif inact >= INACTIVITY_KILL:
            f_act = 0.0
        else:
            f_act = 1.0 - (inact-30)/(INACTIVITY_KILL-30)

        # F_excl — competitive exclusion
        f_excl = 1.0
        if active_chapters:
            competitors = [c for c in active_chapters
                          if c.id != self.id and c.status not in ("EXTINCT","DORMANT")]
            if competitors:
                min_dist = min(self.genotype.distance_to(c.genotype) for c in competitors)
                if   min_dist < 0.15: f_excl = 0.6
                elif min_dist < 0.25: f_excl = 0.8
                elif min_dist < 0.35: f_excl = 0.9

        # F_regime — alignment with regime peak
        f_regime = 1.0
        if regime_vec:
            rv_sum = sum(regime_vec)
            regime_norm = [v/rv_sum for v in regime_vec]
            fit_dist = sum((g-r)**2 for g,r in zip(self.genotype.to_list(), regime_norm))
            f_regime = max(0.5, 1.0 - math.sqrt(fit_dist)*1.5)

        # F_trade
        f_trade = 1.0 + min(len(self.trade_specialisations)*TRADE_SPECIAL_BOOST, 0.18)

        self._raw_fit = max(0.0, min(1.0, f_k2*f_cci*f_act*f_excl*f_regime*f_trade))
        return self._raw_fit

    def CCI(self):
        self._cci = self.genotype.CCI()
        if   self._cci <= CCI_FORMING_MAX:    self._cci_health = "HEALTHY"
        elif self._cci <= CCI_SELECT_PRESSURE: self._cci_health = "SELECTED"
        else:                                   self._cci_health = "PATHOLOGICAL"
        return self._cci

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "description": self.description,
            "status": self.status, "genotype": self.genotype.to_list(),
            "signals": self.signals.to_dict(), "strategy_type": self.strategy_type,
            "k2_signatures": self.k2_signatures, "k2_refusals": self.k2_refusals,
            "k2_conditional": self.k2_conditional, "created": self.created,
            "last_activity": self.last_activity, "trade_receipts": self.trade_receipts,
            "trade_specialisations": self.trade_specialisations[-20:],
            "lineage": self.lineage, "speciation_generation": self.speciation_generation,
        }

    @staticmethod
    def from_dict(d):
        gd = d.get("genotype", d.get("genotype_emphasis", None))
        genotype = GenotypeEmphasis.from_list(gd) if isinstance(gd, list) else GenotypeEmphasis()
        sd = d.get("signals", d.get("speciation_signals", {}))
        signals = SpeciationSignals.from_dict(sd)
        return Chapter(
            id=d.get("id","unknown"), name=d.get("name",""),
            description=d.get("description",""), status=d.get("status","PLANNED"),
            genotype=genotype, signals=signals,
            strategy_type=d.get("strategy_type","r"),
            k2_signatures=d.get("k2_signatures",0), k2_refusals=d.get("k2_refusals",0),
            k2_conditional=d.get("k2_conditional",0),
            created=d.get("created",""), last_activity=d.get("last_activity",""),
            trade_receipts=d.get("trade_receipts",0),
            trade_specialisations=d.get("trade_specialisations",[]),
            lineage=d.get("lineage",[]), speciation_generation=d.get("speciation_generation",0),
        )


# ─── DEFAULT ECOSYSTEM ────────────────────────────────────────────────────────
NOW = "2026-04-01T10:00:00Z"
CREATED = "2026-01-01T00:00:00Z"

DEFAULT_ECOSYSTEM = {
    "generation": 0, "regime": "COMPLIANCE", "last_evolution": None,
    "chapters": [
        {"id":"ch01_tokencen","name":"TOKENCEN","description":"RWA tokenisation",
         "status":"ACTIVE","genotype":[0.15,0.15,0.20,0.20,0.20,0.07,0.03],
         "signals":{"novelty_events":3,"design_requests":6,"k2_signatures":2,
                    "k2_refusals":0,"k2_conditional":1,"trade_receipts":4,
                    "external_demand_events":2,"last_novelty":"RWA deed bridge",
                    "novelty_descriptions":["RWA deed bridge","PE fractionation","Yield micro-token"]},
         "strategy_type":"K","k2_signatures":2,"k2_refusals":0,"k2_conditional":1,
         "created":CREATED,"last_activity":NOW,"trade_receipts":4,
         "trade_specialisations":["deed_bridge","yield_microtoken"],"lineage":[],"speciation_generation":0},

        {"id":"ch02_capital","name":"CAPITAL","description":"Proprietary trading",
         "status":"EMERGING","genotype":[0.08,0.12,0.30,0.30,0.10,0.07,0.03],
         "signals":{"novelty_events":1,"design_requests":2,"k2_signatures":0,
                    "k2_refusals":0,"k2_conditional":0,"trade_receipts":0,
                    "external_demand_events":1,"last_novelty":"","novelty_descriptions":[]},
         "strategy_type":"r","k2_signatures":0,"k2_refusals":0,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":0,
         "trade_specialisations":[],"lineage":[],"speciation_generation":0},

        {"id":"ch03_regaltec","name":"REGALTEC","description":"KYC/AML/CTF/FATF compliance",
         "status":"ACTIVE","genotype":[0.35,0.30,0.12,0.10,0.05,0.05,0.03],
         "signals":{"novelty_events":2,"design_requests":3,"k2_signatures":1,
                    "k2_refusals":1,"k2_conditional":0,"trade_receipts":2,
                    "external_demand_events":3,"last_novelty":"KYC biometric ledger",
                    "novelty_descriptions":["KYC ledger","Biometric oracle"]},
         "strategy_type":"K","k2_signatures":1,"k2_refusals":1,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":2,
         "trade_specialisations":["kyc_oracle"],"lineage":[],"speciation_generation":0},

        {"id":"ch04_advisory","name":"ADVISORY","description":"Institutional research",
         "status":"PROPOSED","genotype":[0.07,0.10,0.25,0.25,0.20,0.08,0.05],
         "signals":{"novelty_events":0,"design_requests":1,"k2_signatures":0,
                    "k2_refusals":0,"k2_conditional":0,"trade_receipts":0,
                    "external_demand_events":0,"last_novelty":"","novelty_descriptions":[]},
         "strategy_type":"r","k2_signatures":0,"k2_refusals":0,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":0,
         "trade_specialisations":[],"lineage":[],"speciation_generation":0},

        {"id":"ch05_infrastruct","name":"INFRASTRUCT","description":"Protocol design",
         "status":"PLANNED","genotype":[0.05,0.10,0.15,0.15,0.30,0.20,0.05],
         "signals":{"novelty_events":0,"design_requests":2,"k2_signatures":0,
                    "k2_refusals":0,"k2_conditional":0,"trade_receipts":0,
                    "external_demand_events":0,"last_novelty":"","novelty_descriptions":[]},
         "strategy_type":"r","k2_signatures":0,"k2_refusals":0,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":0,
         "trade_specialisations":[],"lineage":[],"speciation_generation":0},

        {"id":"ch06_academy","name":"ACADEMY","description":"Training, certification",
         "status":"ACTIVE","genotype":[0.10,0.25,0.15,0.15,0.10,0.22,0.03],
         "signals":{"novelty_events":4,"design_requests":5,"k2_signatures":3,
                    "k2_refusals":0,"k2_conditional":1,"trade_receipts":5,
                    "external_demand_events":4,"last_novelty":"Agent certification",
                    "novelty_descriptions":["Rosetta certification","Agent runbook","Academy PWA"]},
         "strategy_type":"K","k2_signatures":3,"k2_refusals":0,"k2_conditional":1,
         "created":CREATED,"last_activity":NOW,"trade_receipts":5,
         "trade_specialisations":["certification","curriculum"],"lineage":[],"speciation_generation":0},

        {"id":"ch07_legal","name":"LEGAL","description":"Contract mechanics",
         "status":"PLANNED","genotype":[0.07,0.08,0.25,0.20,0.28,0.07,0.05],
         "signals":{"novelty_events":0,"design_requests":1,"k2_signatures":0,
                    "k2_refusals":0,"k2_conditional":0,"trade_receipts":0,
                    "external_demand_events":0,"last_novelty":"","novelty_descriptions":[]},
         "strategy_type":"K","k2_signatures":0,"k2_refusals":0,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":0,
         "trade_specialisations":[],"lineage":[],"speciation_generation":0},

        {"id":"ch08_negotiation","name":"NEGOTIATION","description":"Deal negotiation",
         "status":"PLANNED","genotype":[0.08,0.10,0.28,0.28,0.12,0.08,0.06],
         "signals":{"novelty_events":1,"design_requests":1,"k2_signatures":0,
                    "k2_refusals":0,"k2_conditional":0,"trade_receipts":0,
                    "external_demand_events":1,"last_novelty":"","novelty_descriptions":[]},
         "strategy_type":"r","k2_signatures":0,"k2_refusals":0,"k2_conditional":0,
         "created":CREATED,"last_activity":NOW,"trade_receipts":0,
         "trade_specialisations":[],"lineage":[],"speciation_generation":0},

        {"id":"ch09_governance","name":"GOVERNANCE","description":"Constitutional design",
         "status":"PLANNED","genotype":[0.05,0.08,0.12,0.15,0.20,0.25,0.15],
         "signals":{"novelty_events":2,"design_requests":3,"k2_signatures":1,
                    "k2_refusals":0,"k2_conditional":1,"trade_receipts":1,
                    "external_demand_events":2,"last_novelty":"K2 governance charter",
                    "novelty_descriptions":["K2 charter","Grace Exit clause"]},
         "strategy_type":"r","k2_signatures":1,"k2_refusals":0,"k2_conditional":1,
         "created":CREATED,"last_activity":NOW,"trade_receipts":1,
         "trade_specialisations":["k2_charter"],"lineage":[],"speciation_generation":0},
    ],
}


# ─── PERSISTENCE ──────────────────────────────────────────────────────────────

def load_ecosystem():
    if ECOSYSTEM_PATH.exists():
        with open(ECOSYSTEM_PATH) as f:
            return json.load(f)
    return deepcopy(DEFAULT_ECOSYSTEM)

def save_ecosystem(eco):
    ECOSYSTEM_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(ECOSYSTEM_PATH, "w") as f:
        json.dump(eco, f, indent=2)

def chapters_from_ecosystem(eco):
    return [Chapter.from_dict(d) for d in eco.get("chapters", [])]

def ecosystem_from_chapters(chapters):
    eco = load_ecosystem()
    eco["chapters"] = [c.to_dict() for c in chapters]
    return eco


# ─── MUTATION OPERATORS ───────────────────────────────────────────────────────

def apply_point_mutation(ch, rng):
    events = []
    levels = ["L1","L2","L3","L4","L5","L6","L7"]
    idx = rng.randint(0, 6)
    level = levels[idx]
    shift = rng.uniform(-MUT_AMPLITUDE, MUT_AMPLITUDE)
    old_val = ch.genotype.to_list()[idx]
    ch.genotype.shift(level, shift, rng)
    new_val = ch.genotype.to_list()[idx]
    if abs(new_val - old_val) > 0.001:
        events.append({"type":"POINT_MUTATION","chapter":ch.id,"level":level,
                       "before":round(old_val,4),"after":round(new_val,4),
                       "shift":round(shift,4),
                       "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_CNV(ch, rng):
    events = []
    levels = ["L1","L2","L3","L4","L5","L6","L7"]
    src = rng.randint(0,5)
    tgt = rng.randint(src+1,6) if src<6 else rng.randint(0,5)
    donor = ch.genotype.to_list()[src] * 0.5
    old_tgt = ch.genotype.to_list()[tgt]
    ch.genotype.shift(levels[src], -donor, rng)
    ch.genotype.shift(levels[tgt], donor/2, rng)
    events.append({"type":"CNV","chapter":ch.id,"donor":levels[src],
                   "recipient":levels[tgt],"donated":round(donor,4),
                   "before":round(old_tgt,4),"after":round(ch.genotype.to_list()[tgt],4),
                   "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_factor_substitution(ch, rng):
    events = []
    levels = ["L1","L2","L3","L4","L5","L6","L7"]
    i = rng.randint(0,6); j = rng.randint(0,6)
    if i == j: return events
    vals = ch.genotype.to_list()
    vals[i],vals[j] = vals[j],vals[i]
    for k,lvl in enumerate(levels): setattr(ch.genotype, lvl, vals[k])
    ch.genotype._renormalise()
    events.append({"type":"FACTOR_SUBSTITUTION","chapter":ch.id,
                   "swapped":[levels[i],levels[j]],
                   "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_regulatory_shock(ch, rng):
    events = []
    levels = ["L1","L2","L3","L4","L5","L6","L7"]
    idx = rng.randint(0,6)
    old_val = ch.genotype.to_list()[idx]
    new_val = rng.uniform(0.0, 0.30)
    ch.genotype.shift(levels[idx], new_val - old_val, rng)
    events.append({"type":"REGULATORY_SHOCK","chapter":ch.id,"level":levels[idx],
                   "before":round(old_val,4),"after":round(new_val,4),
                   "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_network_amplification(ch, rng):
    events = []
    doms = ch.genotype.dominants()
    if not doms: return events
    boost = rng.uniform(0.05, 0.15)
    for lvl in doms[:3]:
        ch.genotype.shift(lvl, boost/len(doms[:3]), rng)
    events.append({"type":"NETWORK_AMPLIFICATION","chapter":ch.id,
                   "boosted":doms[:3],"boost":round(boost,4),
                   "CCI_after":round(ch.genotype.CCI(),4),
                   "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_mutation(ch, rng, punctuated=False):
    if not ch.is_active: return []
    if rng.random() > ch.base_mutation_rate(): return []
    ops = [apply_point_mutation, apply_CNV, apply_factor_substitution, apply_regulatory_shock]
    if rng.random() < 0.1: ops.append(apply_network_amplification)
    events = rng.choice(ops)(ch, rng)
    if not events: return []
    if punctuated:
        for _ in range(rng.randint(1,3)):
            extra = rng.choice(ops)(ch, rng)
            events.extend(extra)
        events.append({"type":"PUNCTUATION_BURST","chapter":ch.id,
                       "burst_count":1+rng.randint(1,3),
                       "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── SELECTION ────────────────────────────────────────────────────────────────

def apply_selection(chapters):
    events = []
    for ch in chapters:
        cci = ch.CCI()
        if cci > CCI_SELECT_PRESSURE:
            deficit = cci - CCI_SELECT_PRESSURE
            avg = 1.0/7.0
            for lvl in ["L1","L2","L3","L4","L5","L6","L7"]:
                val = getattr(ch.genotype, lvl)
                if val > avg:
                    adjustment = (val-avg)*0.5*(deficit/0.10)
                    ch.genotype.shift(lvl, -adjustment, random.Random())
            events.append({"type":"STABILISING_SELECTION","chapter":ch.id,
                           "CCI_before":round(cci,4),
                           "CCI_after":round(ch.genotype.CCI(),4),
                           "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── RED QUEEN ────────────────────────────────────────────────────────────────

def apply_red_queen(ch, raw_fitness, rng):
    events = []
    if raw_fitness < R_Q_THRESHOLD:
        pressure = RED_QUEEN_PRESSURE*(R_Q_THRESHOLD-raw_fitness)/R_Q_THRESHOLD
        if rng.random() < 0.7:
            mut_events = apply_mutation(ch, rng, punctuated=False)
            events.extend(mut_events)
        events.append({"type":"RED_QUEEN_PRESSURE","chapter":ch.id,
                       "raw_fitness":round(raw_fitness,4),"threshold":R_Q_THRESHOLD,
                       "pressure":round(pressure,4),
                       "note":f"raw {raw_fitness:.4f} < {R_Q_THRESHOLD}",
                       "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── FREQUENCY-DEPENDENT SELECTION ───────────────────────────────────────────

def apply_frequency_selection(chapters, raw_fitness):
    events = []
    active = [c for c in chapters if c.is_active]
    if not active: return events
    avg_cci = sum(c.genotype.CCI() for c in active)/len(active)
    if avg_cci < FREQ_THRESHOLD: return events
    for ch in active:
        cci = ch.genotype.CCI()
        if cci < avg_cci*0.5:
            bonus = FREQ_BONUS*(avg_cci-cci)/avg_cci
            events.append({"type":"FREQUENCY_DEPENDENCE","chapter":ch.id,
                           "direction":"BONUS","bonus":round(bonus,4),
                           "CCI":round(cci,4),
                           "timestamp":datetime.now(timezone.utc).isoformat()})
        elif cci > avg_cci*1.5:
            penalty = FREQ_PENALTY*(cci-avg_cci)/avg_cci
            events.append({"type":"FREQUENCY_DEPENDENCE","chapter":ch.id,
                           "direction":"PENALTY","penalty":round(penalty,4),
                           "CCI":round(cci,4),
                           "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── COEVOLUTION ──────────────────────────────────────────────────────────────

def apply_arms_race(ch, competitors, raw_fitness, rng):
    events = []
    for comp in competitors:
        if comp.id==ch.id or comp.status in ("EXTINCT","DORMANT"): continue
        gap = raw_fitness.get(comp.id,0) - raw_fitness.get(ch.id,0)
        if gap > 0.20:
            dist = ch.genotype.distance_to(comp.genotype)
            if dist < 0.30:
                push = gap*0.1*(1.0-dist)
                ch.genotype.shift("L4", push, rng)
                events.append({"type":"ARMS_RACE","chapter":ch.id,
                               "competitor":comp.id,"gap":round(gap,4),
                               "push_L4":round(push,4),
                               "timestamp":datetime.now(timezone.utc).isoformat()})
    return events

def apply_mutualism(ch, others, rng):
    events = []
    for other in others:
        if ch.id==other.id or other.status in ("EXTINCT","DORMANT"): continue
        dist = ch.genotype.distance_to(other.genotype)
        if 0.30<dist<0.60 and rng.random()<COEV_RATE:
            lvl = rng.choice(["L1","L2","L3","L4","L5","L6","L7"])
            donor = getattr(other.genotype, lvl)
            if donor > 0.15:
                boost = donor*0.15
                ch.genotype.shift(lvl, boost, rng)
                events.append({"type":"COEVOLUTION_MUTUALISM","chapter":ch.id,
                               "partner":other.id,"level":lvl,"boost":round(boost,4),
                               "distance":round(dist,4),
                               "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── HGT ─────────────────────────────────────────────────────────────────────

def apply_HGT(active, rng):
    events = []
    if len(active) < 2: return events
    pairs = [(a,b) for i,a in enumerate(active) for b in active[i+1:]]
    for ch_a, ch_b in pairs:
        if rng.random() >= HGT_RATE: continue   # FIRE on < 3% of pairs
        lvl = rng.choice(["L2","L3","L4"])
        donor = getattr(ch_b.genotype, lvl)
        if donor > 0.15:
            boost = donor*0.20
            ch_a.genotype.shift(lvl, boost, rng)
            events.append({"type":"HORIZONTAL_TRANSFER","chapter":ch_a.id,
                           "donor":ch_b.id,"level":lvl,"boost":round(boost,4),
                           "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── EXAPTATION ───────────────────────────────────────────────────────────────

def apply_exaptation(chapters, rng):
    events = []
    for ch in chapters:
        if not ch.is_active or rng.random() >= EXAPTATION_PROB: continue
        for lvl in ["L1","L2","L3","L4","L5","L6","L7"]:
            if getattr(ch.genotype, lvl) > 0.65:
                events.append({"type":"EXAPTATION","chapter":ch.id,"level":lvl,
                               "value":round(getattr(ch.genotype,lvl),4),
                               "bonus":EXAPTATION_BOOST,
                               "note":"Accidental alignment with external market demand",
                               "timestamp":datetime.now(timezone.utc).isoformat()})
                ch.signals.external_demand_events += 1
                ch.signals.novelty_events += 1
                ch.signals.novelty_descriptions.append(f"exaptation:{lvl}")
    return events


# ─── SPECIATION ────────────────────────────────────────────────────────────────

def execute_speciation(parent, rng, generation):
    if parent.signals.readiness() != "ready": return []
    chi = parent.signals.chi_sq_test()
    fv = parent.signals.f_test()
    if chi < CHI_SQ_CRIT or fv < 0.5: return []
    offspring_geno = parent.genotype.copy()
    offspring_geno.apply_founder_drift(F_DRIFT_SIGMA, rng)
    doms = parent.genotype.dominants()
    if doms:
        offspring_geno.shift(rng.choice(doms), 0.15, rng)
    lineage = parent.lineage + [parent.id]
    return [Chapter(
        id=f"{parent.id}_offspring_{generation}",
        name=f"{parent.name}_V2",
        description=f"Speciated from {parent.id} at generation {generation}.",
        status="EMERGING", genotype=offspring_geno, signals=SpeciationSignals(),
        strategy_type=rng.choice(["r","K"]), lineage=lineage,
        speciation_generation=generation,
        created=datetime.now(timezone.utc).isoformat(),
        last_activity=datetime.now(timezone.utc).isoformat(),
    )]


# ─── EXTINCTION ───────────────────────────────────────────────────────────────

def check_extinction(chapters, raw_fitness):
    events = []
    for ch in chapters:
        if ch.status in ("EXTINCT","DORMANT"): continue
        reasons = []
        if ch.genotype.CCI() > CCI_EXTINCT:
            reasons.append(f"CCI={ch.genotype.CCI():.3f}>{CCI_EXTINCT}")
        if ch.inactivity_days > INACTIVITY_KILL:
            reasons.append(f"inactive={ch.inactivity_days}d>{INACTIVITY_KILL}d")
        if ch.k2_refusal_rate > K2_REFUSAL_KILL:
            reasons.append(f"K2_refusal={ch.k2_refusal_rate:.1%}>{K2_REFUSAL_KILL:.1%}")
        if reasons:
            ch.status = "EXTINCT"
            events.append({"type":"EXTINCTION","chapter":ch.id,"reasons":reasons,
                           "fitness_at_extinction":round(raw_fitness.get(ch.id,0),4),
                           "timestamp":datetime.now(timezone.utc).isoformat()})
    extinct_ids = {e["chapter"] for e in events if e["type"]=="EXTINCTION"}
    for ch in chapters:
        if ch.id not in extinct_ids and ch.is_active:
            events.append({"type":"ECOLOGICAL_RELEASE","chapter":ch.id,
                           "released_by":list(extinct_ids),"bonus":0.04,
                           "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── CARRYING CAPACITY ─────────────────────────────────────────────────────────

def check_carrying_capacity(chapters):
    from collections import defaultdict
    events = []
    clusters = defaultdict(list)
    for ch in chapters:
        if ch.status not in ("EXTINCT","DORMANT"):
            clusters[ch.id.split("_")[0]].append(ch)
    for cluster, members in clusters.items():
        if len(members) > CARRYING_CAPACITY:
            members.sort(key=lambda c: c.speciation_generation)
            for ch in members[:-CARRYING_CAPACITY]:
                ch.status = "DORMANT"
                events.append({"type":"CARRYING_CAPACITY_TRIGGER","chapter":ch.id,
                               "cluster":cluster,"size":len(members),"limit":CARRYING_CAPACITY,
                               "timestamp":datetime.now(timezone.utc).isoformat()})
    return events


# ─── REGIME SHIFT ─────────────────────────────────────────────────────────────

def shift_regime(current, rng):
    if rng.random() >= REGIME_SHIFT_PROB: return current, False
    candidates = [r for r in REGIMES if r != current]
    new_regime = rng.choice(candidates)
    if rng.random() < REGIME_HYSTERESIS and candidates: return current, False
    return new_regime, True


# ─── PUNCTUATION ──────────────────────────────────────────────────────────────

def check_punctuation(chapters, rng):
    punctuating = set()
    for ch in chapters:
        if not ch.is_active: continue
        ch._stasis_generations += 1
        if ch._stasis_generations >= PUNCTUATION_PERIOD:
            if rng.random() < PUNCTUATION_BURST:
                punctuating.add(ch.id)
                ch._stasis_generations = 0
    return punctuating


# ─── LOGGING ──────────────────────────────────────────────────────────────────

def log_events(events):
    EVOLUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(EVOLUTION_LOG, "a") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")


# ─── ONE EVOLUTION CYCLE ──────────────────────────────────────────────────────

def run_evolution_cycle(seed=None, ngen=1, dry_run=False):
    rng = random.Random(seed)
    eco = load_ecosystem()
    generation = eco.get("generation", 0)
    current_regime = eco.get("regime", "COMPLIANCE")
    regime_vec = REGIME_PEAKS.get(current_regime, REGIME_PEAKS["COMPLIANCE"])

    all_events = []
    summary = {"generations":0,"speciation_count":0,"extinction_count":0,"regime_shifts":0}

    for _ in range(ngen):
        generation += 1
        chapters = chapters_from_ecosystem(eco)
        active = [c for c in chapters if c.is_active]

        # 1. Regime shift
        new_regime, did_shift = shift_regime(current_regime, rng)
        if did_shift:
            regime_vec = REGIME_PEAKS[new_regime]
            all_events.append({"type":"REGIME_SHIFT","from":current_regime,"to":new_regime,
                               "generation":generation,"regime_peak":regime_vec,
                               "note":"Market conditions shifted.",
                               "timestamp":datetime.now(timezone.utc).isoformat()})
            current_regime = new_regime
            summary["regime_shifts"] += 1

        # 2. Raw fitness
        raw_fitness = {c.id: c.compute_fitness(active_chapters=active, regime_vec=regime_vec)
                       for c in chapters}

        # 3. Punctuation
        punctuating = check_punctuation(chapters, rng)
        for ch_id in punctuating:
            all_events.append({"type":"PUNCTUATION_BURST","chapter":ch_id,
                               "stasis_generations":PUNCTUATION_PERIOD,
                               "note":f"Burst after {PUNCTUATION_PERIOD} gens stasis",
                               "timestamp":datetime.now(timezone.utc).isoformat()})

        # 4. Red Queen + Frequency
        for ch in active:
            all_events.extend(apply_red_queen(ch, raw_fitness.get(ch.id,0), rng))
        all_events.extend(apply_frequency_selection(chapters, raw_fitness))

        # 5. Coevolution
        for ch in active:
            competitors = [c for c in active if c.id != ch.id]
            all_events.extend(apply_arms_race(ch, competitors, raw_fitness, rng))
            all_events.extend(apply_mutualism(ch, active, rng))

        # 6. HGT
        all_events.extend(apply_HGT(active, rng))

        # 7. Vertical mutation
        for ch in active:
            all_events.extend(apply_mutation(ch, rng, punctuated=ch.id in punctuating))

        # 8. Exaptation
        all_events.extend(apply_exaptation(chapters, rng))

        # 9. Stabilising selection
        all_events.extend(apply_selection(chapters))

        # 10. Speciation
        offspring_all = []
        for ch in active:
            if ch.signals.readiness() == "ready":
                offspring = execute_speciation(ch, rng, generation)
                for o in offspring:
                    all_events.append({"type":"SPECIATION_EVENT","parent":ch.id,"offspring":o.id,
                                       "parent_genotype":ch.genotype.to_list(),
                                       "offspring_genotype":o.genotype.to_list(),
                                       "founder_drift_sigma":F_DRIFT_SIGMA,
                                       "generation":generation,
                                       "timestamp":datetime.now(timezone.utc).isoformat()})
                    offspring_all.append(o)
        chapters.extend(offspring_all)
        summary["speciation_count"] += len(offspring_all)

        # 11. Re-compute fitness
        active_now = [c for c in chapters if c.is_active]
        for ch in chapters:
            raw_fitness[ch.id] = ch.compute_fitness(active_chapters=active_now, regime_vec=regime_vec)

        # 12. Extinction
        all_events.extend(check_extinction(chapters, raw_fitness))

        # 13. Carrying capacity
        all_events.extend(check_carrying_capacity(chapters))

        log_events(all_events); all_events = []

        eco = ecosystem_from_chapters(chapters)
        eco["generation"] = generation
        eco["regime"] = current_regime
        eco["last_evolution"] = datetime.now(timezone.utc).isoformat()
        if not dry_run: save_ecosystem(eco)

        summary["generations"] = generation
        summary["extinction_count"] = sum(1 for c in chapters if c.status=="EXTINCT")

    return summary


# ─── REPORT ───────────────────────────────────────────────────────────────────

def generate_report():
    eco = load_ecosystem()
    generation = eco.get("generation",0)
    regime = eco.get("regime","COMPLIANCE")
    chapters = chapters_from_ecosystem(eco)
    active = [c for c in chapters if c.is_active]
    regime_vec = REGIME_PEAKS.get(regime, REGIME_PEAKS["COMPLIANCE"])
    raw_fitness = {c.id: c.compute_fitness(active_chapters=active, regime_vec=regime_vec)
                   for c in chapters}

    lines = [
        f"# Polygenetic Skill Tree — Evolution Report",
        f"",
        f"**Generation:** {generation}  **Regime:** {regime}  **Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f"",
        f"## Ecosystem State",
        f"",
        f"| Chapter | Status | Fitness | CCI | Health | Dominant | K2 Rate | Inact |",
        f"|---------|--------|---------|-----|--------|---------|---------|-------|",
    ]
    for ch in sorted(chapters, key=lambda c: raw_fitness.get(c.id,0), reverse=True):
        cci = ch.CCI()
        fit = raw_fitness.get(ch.id,0)
        doms = ", ".join(ch.genotype.dominants()) or "flat"
        k2r = f"{ch.k2_approval_rate:.0%}" if ch.total_k2 > 0 else "—"
        lines.append(f"| {ch.id} | {ch.status} | {fit:.4f} | {cci:.4f} | "
                     f"{ch._cci_health} | {doms} | {k2r} | {ch.inactivity_days}d |")

    af = [raw_fitness[c.id] for c in active] if active else [0]
    avg_fit = sum(af)/len(af)
    regime_intensity = max(af)-min(af) if af else 0
    sel_pressure = max(0.0, regime_intensity-0.3)*2.0

    lines.extend([
        f"",
        f"## Fitness Summary",
        f"",
        f"- **Active:** {len(active)}/{len(chapters)}  **Avg fitness:** {avg_fit:.4f}",
        f"- **Selection pressure:** {sel_pressure:.4f}",
        f"- **Regime peak:** "
        f"L1={regime_vec[0]:.2f} L2={regime_vec[1]:.2f} L3={regime_vec[2]:.2f} "
        f"L4={regime_vec[3]:.2f} L5={regime_vec[4]:.2f} L6={regime_vec[5]:.2f} L7={regime_vec[6]:.2f}",
        f"",
        f"## Phylogeny",
        f"",
        f"| Chapter | Parent | Distance | Spec Gen |",
        f"|---------|--------|----------|----------|",
    ])
    for ch in chapters:
        parent_dist = "—"
        if ch.lineage:
            parent_ch = next((c for c in chapters if c.id==ch.lineage[-1]), None)
            if parent_ch: parent_dist = f"{ch.genotype.distance_to(parent_ch.genotype):.3f}"
        lines.append(f"| {ch.id} | {ch.lineage[-1] if ch.lineage else '—'} | "
                     f"{parent_dist} | {ch.speciation_generation} |")
    lines.extend(["",f"## Speciation Watch",""])
    for ch in active:
        sig = ch.signals
        lines.append(f"- **{ch.id}** ({ch.status}): {sig.readiness()} | "
                      f"novelty={sig.novelty_events}/3 design={sig.design_requests}/5 "
                      f"chi2={sig.chi_sq_test():.1f} (crit={CHI_SQ_CRIT})")
    return "\n".join(lines)


# ─── PHYLOGENETIC TREE ─────────────────────────────────────────────────────────

def print_phylogeny(chapters):
    eco = load_ecosystem()
    regime = eco.get("regime","COMPLIANCE")
    print(f"\n  Polygenetic Skill Tree — Gen {eco.get('generation',0)} | Regime: {regime}")
    print("  " + "-"*58)
    roots = [c for c in chapters if not c.lineage]
    for ch in sorted(roots, key=lambda c: c.id):
        _print_node(ch, chapters, "", True)

def _print_node(ch, all_chapters, prefix, is_last):
    conn = "+-- " if is_last else "|-- "
    cci = ch.CCI(); f = ch.compute_fitness([c for c in all_chapters if c.is_active])
    doms = ",".join(ch.genotype.dominants()) or "flat"
    print(f"  {prefix}{conn}{ch.id} [{ch.status}] f={f:.3f} CCI={cci:.3f}({ch._cci_health}) dom={doms}")
    children = [c for c in all_chapters if c.lineage and c.lineage[-1]==ch.id]
    for i, child in enumerate(children):
        ext = "    " if is_last else "|   "
        _print_node(child, all_chapters, prefix+ext, i==len(children)-1)


# ─── CLI ───────────────────────────────────────────────────────────────────────

def cmd_init():
    eco = deepcopy(DEFAULT_ECOSYSTEM)
    save_ecosystem(eco)
    print(f"Registry initialised: {len(eco['chapters'])} chapters, gen 0")

def cmd_scan(eco):
    chapters = chapters_from_ecosystem(eco)
    regime = eco.get("regime","COMPLIANCE")
    regime_vec = REGIME_PEAKS.get(regime, REGIME_PEAKS["COMPLIANCE"])
    active = [c for c in chapters if c.is_active]
    raw_fitness = {c.id: c.compute_fitness(active_chapters=active, regime_vec=regime_vec)
                   for c in chapters}
    print(f"\n  Agentz Polygenetic Skill Tree — Scan")
    print(f"  Gen {eco.get('generation',0)} | Regime: {regime}")
    print(f"  {'='*58}")
    print(f"  {'Chapter':<24} {'Status':<10} {'Fit':>7} {'CCI':>7} {'Health':<12} Dominant")
    for ch in sorted(chapters, key=lambda c: raw_fitness.get(c.id,0), reverse=True):
        cci = ch.CCI(); fit = raw_fitness.get(ch.id,0)
        doms = ",".join(ch.genotype.dominants()) or "flat"
        print(f"  {ch.id:<24} {ch.status:<10} {fit:>7.4f} {cci:>7.4f} {ch._cci_health:<12} {doms}")
    if active:
        af = sum(raw_fitness[c.id] for c in active)/len(active)
        print(f"\n  Avg fitness: {af:.4f}  Active: {len(active)}/{len(chapters)}")

def main():
    parser = argparse.ArgumentParser(description="Agentz Polygenetic Evolution Engine")
    parser.add_argument("--init",  action="store_true", help="Initialise ecosystem")
    parser.add_argument("--scan",  action="store_true", help="Scan current state")
    parser.add_argument("--all",   action="store_true", help="Run full evolution cycle")
    parser.add_argument("--seed",  type=int, default=None, help="Random seed")
    parser.add_argument("--ngen",  type=int, default=1,    help="Number of generations")
    parser.add_argument("--mutate",type=str, help="Mutate single chapter")
    parser.add_argument("--feed-k2", nargs=2, metavar=("CH","TYPE"),
                        help="Feed K2 signal: sign | refuse | conditional")
    parser.add_argument("--feed-activity", type=str, help="Record activity for chapter")
    parser.add_argument("--report", action="store_true", help="Generate Markdown report")
    parser.add_argument("--phylo",  action="store_true", help="Print phylogenetic tree")
    args = parser.parse_args()

    if args.init:
        cmd_init(); return

    eco = load_ecosystem()

    if args.scan:
        cmd_scan(eco); return

    if args.feed_k2:
        ch_id, sig_type = args.feed_k2
        chapters = chapters_from_ecosystem(eco)
        ch = next((c for c in chapters if c.id==ch_id), None)
        if not ch: print(f"Chapter '{ch_id}' not found."); return
        if sig_type=="sign":         ch.k2_signatures+=1; ch.signals.k2_signatures+=1
        elif sig_type=="refuse":     ch.k2_refusals+=1;  ch.signals.k2_refusals+=1
        elif sig_type=="conditional":ch.k2_conditional+=1; ch.signals.k2_conditional+=1
        else: print(f"Unknown: {sig_type}"); return
        ch.last_activity = datetime.now(timezone.utc).isoformat()
        save_ecosystem(ecosystem_from_chapters(chapters))
        print(f"K2 '{sig_type}' for {ch_id}. Approval: {ch.k2_approval_rate:.0%}")
        return

    if args.feed_activity:
        chapters = chapters_from_ecosystem(eco)
        ch = next((c for c in chapters if c.id==args.feed_activity), None)
        if not ch: print(f"Chapter '{args.feed_activity}' not found."); return
        ch.last_activity = datetime.now(timezone.utc).isoformat()
        save_ecosystem(ecosystem_from_chapters(chapters))
        print(f"Activity recorded for {args.feed_activity}.")
        return

    if args.all:
        label = f" (seed={args.seed})" if args.seed else ""
        print(f"Running {args.ngen} generation(s){label}…")
        result = run_evolution_cycle(seed=args.seed, ngen=args.ngen, dry_run=False)
        eco = load_ecosystem()
        print(f"Gen {result['generations']} | Regime: {eco.get('regime')} | "
              f"Speciations: {result['speciation_count']} | "
              f"Extinctions: {result['extinction_count']} | "
              f"Regime shifts: {result['regime_shifts']}")
        cmd_scan(eco); return

    if args.mutate:
        chapters = chapters_from_ecosystem(eco)
        ch = next((c for c in chapters if c.id==args.mutate), None)
        if not ch: print(f"Chapter '{args.mutate}' not found."); return
        rng = random.Random()
        events = apply_mutation(ch, rng, punctuated=False)
        save_ecosystem(ecosystem_from_chapters(chapters))
        print(f"{args.mutate}: {len(events)} mutation(s)")
        for e in events: print(f"  {e['type']}: {e.get('level', e.get('swapped','—'))}")
        return

    if args.report:
        report = generate_report()
        EVOLUTION_REPORT.parent.mkdir(parents=True, exist_ok=True)
        with open(EVOLUTION_REPORT, "w") as f: f.write(report)
        print(f"Report: {EVOLUTION_REPORT}"); return

    if args.phylo:
        chapters = chapters_from_ecosystem(eco)
        print_phylogeny(chapters); return

    parser.print_help()

if __name__ == "__main__":
    main()
