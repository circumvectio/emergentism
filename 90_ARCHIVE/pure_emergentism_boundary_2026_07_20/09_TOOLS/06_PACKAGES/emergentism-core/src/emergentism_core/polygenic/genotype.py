"""12-dimensional genotype: 7 caste emphasis weights + 5 economic intensity dimensions.

Biological invariants:
  - Caste block (L1-L7): range [0.3, 2.0], no sum constraint. These are emphasis
    weights — how much cognitive energy the organism devotes to each caste function.
  - Economic block (κ,λ,μ,ρ,ν): range [0.0, 1.0], sum to 1.0. These are intensity
    proportions — how the organism deploys resources across factor dimensions.
  - The two blocks evolve semi-independently. Caste mutation affects cognition;
    economic mutation affects resource deployment.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

# ─────────────────────────────────────────────────────────────────────────────
# CASTE BLOCK — L1..L7 emphasis weights
# ─────────────────────────────────────────────────────────────────────────────

CASTE_LEVELS = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
CASTE_MIN = 0.3
CASTE_MAX = 2.0
STRUCTURAL_LEVELS = {"L1", "L5", "L7"}  # lower mutation rate


@dataclass
class CasteBlock:
    L1: float = 1.0  # Caṇḍāla — sovereign intake / firewall
    L2: float = 1.0  # Śūdra — discovery / pattern recognition
    L3: float = 1.0  # Vaiśya — constitutional audit / compliance
    L4: float = 1.0  # Kṣatriya — execution / decision
    L5: float = 1.0  # Brāhmaṇa — architecture / redesign
    L6: float = 1.0  # Sādhu — compression / archive
    L7: float = 1.0  # Ṛṣi — constitutional / vision

    def to_list(self) -> list[float]:
        return [self.L1, self.L2, self.L3, self.L4, self.L5, self.L6, self.L7]

    @classmethod
    def from_list(cls, lst: list[float]) -> "CasteBlock":
        if len(lst) != 7:
            raise ValueError(f"CasteBlock requires 7 values, got {len(lst)}")
        return cls(*[max(CASTE_MIN, min(CASTE_MAX, v)) for v in lst])

    def clamp(self) -> "CasteBlock":
        """Return a new CasteBlock with all values clamped to [CASTE_MIN, CASTE_MAX]."""
        return CasteBlock.from_list(self.to_list())

    def compute_cci(self) -> float:
        """Capability Concentration Index. 0 = generalist (flat), 1 = specialist (spike)."""
        vals = self.to_list()
        total = sum(vals)
        if total == 0:
            return 0.0
        probs = [v / total for v in vals]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        cci = 1.0 - (entropy / math.log2(7))
        return round(cci, 4)

    def dominant_levels(self, threshold: float = 1.3) -> list[str]:
        """L-levels at or above threshold × baseline = phenotype characteristic."""
        return [name for name, val in zip(CASTE_LEVELS, self.to_list()) if val >= threshold]

    def distance_to(self, other: "CasteBlock") -> float:
        """Normalised Euclidean distance. 0 = identical, 1 = maximally different."""
        diff_sq = sum((a - b) ** 2 for a, b in zip(self.to_list(), other.to_list()))
        max_diff_sq = 7 * (CASTE_MAX - CASTE_MIN) ** 2
        return math.sqrt(diff_sq) / math.sqrt(max_diff_sq)

    def apply_vertical_mutation(self, level: str, delta: float) -> float:
        """Apply a delta to a level, clamped to [CASTE_MIN, CASTE_MAX]. Returns new value."""
        new_val = getattr(self, level) + delta
        new_val = max(CASTE_MIN, min(CASTE_MAX, new_val))
        setattr(self, level, round(new_val, 4))
        return getattr(self, level)

    def copy(self) -> "CasteBlock":
        return CasteBlock.from_list(self.to_list())


# ─────────────────────────────────────────────────────────────────────────────
# ECONOMIC BLOCK — κ,λ,μ,ρ,ν intensity proportions
# ─────────────────────────────────────────────────────────────────────────────

ECONOMIC_DIMS = ["kappa", "lambda", "mu", "rho", "nu"]
ECONOMIC_LABELS = {
    "kappa": "capital_intensity",
    "lambda": "labour_intensity",
    "mu": "knowledge_intensity",
    "rho": "regulatory_intensity",
    "nu": "network_intensity",
}


@dataclass
class EconomicBlock:
    kappa: float = 0.20   # κ — capital intensity
    lambda_: float = 0.20  # λ — labour intensity (rename to avoid keyword)
    mu: float = 0.20      # μ — knowledge intensity
    rho: float = 0.20     # ρ — regulatory intensity
    nu: float = 0.20      # ν — network intensity

    def __post_init__(self):
        # Enforce sum-to-1.0 invariant via renormalisation
        vals = [self.kappa, self.lambda_, self.mu, self.rho, self.nu]
        total = sum(vals)
        if total > 0 and abs(total - 1.0) > 0.001:
            self.kappa = round(self.kappa / total, 6)
            self.lambda_ = round(self.lambda_ / total, 6)
            self.mu = round(self.mu / total, 6)
            self.rho = round(self.rho / total, 6)
            self.nu = round(1.0 - self.kappa - self.lambda_ - self.mu - self.rho, 6)

    def to_list(self) -> list[float]:
        return [self.kappa, self.lambda_, self.mu, self.rho, self.nu]

    def to_dict(self) -> dict[str, float]:
        return {
            "kappa": self.kappa,
            "lambda": self.lambda_,
            "mu": self.mu,
            "rho": self.rho,
            "nu": self.nu,
        }

    @classmethod
    def from_list(cls, lst: list[float]) -> "EconomicBlock":
        if len(lst) != 5:
            raise ValueError(f"EconomicBlock requires 5 values, got {len(lst)}")
        return cls(kappa=lst[0], lambda_=lst[1], mu=lst[2], rho=lst[3], nu=lst[4])

    @classmethod
    def from_dict(cls, d: dict) -> "EconomicBlock":
        return cls(
            kappa=d.get("kappa", 0.20),
            lambda_=d.get("lambda", d.get("lambda_", 0.20)),
            mu=d.get("mu", 0.20),
            rho=d.get("rho", 0.20),
            nu=d.get("nu", 0.20),
        )

    def compute_edi(self) -> float:
        """Economic Diversity Index. 0 = monoculture, 1 = perfectly balanced."""
        vals = self.to_list()
        # Use Simpson's diversity index: 1 - sum(p²)
        return round(1.0 - sum(v ** 2 for v in vals), 4)

    def compute_sd(self) -> float:
        """Specialisation Depth = max / min. Higher = more specialised."""
        vals = [v for v in self.to_list() if v > 0.001]
        if not vals:
            return 1.0
        return round(max(vals) / min(vals), 4)

    def dominant_dimensions(self, threshold: float = 0.30) -> list[str]:
        """Economic dimensions at or above threshold = specialisation focus."""
        return [
            ECONOMIC_LABELS[name]
            for name, val in zip(ECONOMIC_DIMS, self.to_list())
            if val >= threshold
        ]

    def distance_to(self, other: "EconomicBlock") -> float:
        """Normalised Euclidean distance. 0 = identical economic profile."""
        diff_sq = sum((a - b) ** 2 for a, b in zip(self.to_list(), other.to_list()))
        # Max distance = sqrt(2) when one dim = 1.0 and another = 0.0 (but sum=1)
        # Actually max diff between two probability distributions is bounded
        return round(math.sqrt(diff_sq) / math.sqrt(2.0), 4)

    def copy(self) -> "EconomicBlock":
        return EconomicBlock.from_list(self.to_list())


# ─────────────────────────────────────────────────────────────────────────────
# FULL GENOTYPE — 12 dimensions
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class FullGenotype:
    caste: CasteBlock = field(default_factory=CasteBlock)
    economic: EconomicBlock = field(default_factory=EconomicBlock)

    def to_full_list(self) -> list[float]:
        return self.caste.to_list() + self.economic.to_list()

    def to_dict(self) -> dict:
        return {
            "caste": {k: v for k, v in zip(CASTE_LEVELS, self.caste.to_list())},
            "economic": self.economic.to_dict(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FullGenotype":
        caste_dict = d.get("caste", {})
        caste_list = [caste_dict.get(lvl, 1.0) for lvl in CASTE_LEVELS]
        economic_dict = d.get("economic", {})
        return cls(
            caste=CasteBlock.from_list(caste_list),
            economic=EconomicBlock.from_dict(economic_dict),
        )

    @classmethod
    def from_12_list(cls, lst: list[float]) -> "FullGenotype":
        if len(lst) != 12:
            raise ValueError(f"FullGenotype requires 12 values, got {len(lst)}")
        return cls(
            caste=CasteBlock.from_list(lst[:7]),
            economic=EconomicBlock.from_list(lst[7:]),
        )

    def phenotype_signature(self) -> str:
        """Human-readable phenotype: dominant caste + dominant economic dimensions."""
        caste_dom = self.caste.dominant_levels()
        econ_dom = self.economic.dominant_dimensions()
        caste_str = ",".join(caste_dom) if caste_dom else "flat"
        econ_str = ",".join(econ_dom) if econ_dom else "balanced"
        return f"[{caste_str}]×[{econ_str}]"

    def distance_to(self, other: "FullGenotype") -> float:
        """Combined distance: 50% caste + 50% economic."""
        caste_dist = self.caste.distance_to(other.caste)
        econ_dist = self.economic.distance_to(other.economic)
        return round(0.5 * caste_dist + 0.5 * econ_dist, 4)

    def copy(self) -> "FullGenotype":
        return FullGenotype(caste=self.caste.copy(), economic=self.economic.copy())
