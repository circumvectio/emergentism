"""Polygenic economic evolution engine — 12-dimensional genotype with biological operators.

Genotype = 7 caste emphasis weights + 5 economic intensity dimensions.
Mutation = point, CNV, HGT, factor substitution, regulatory shock, network amplification.
Selection = natural (fitness-weighted), sexual (partner preference), group (ecosystem).
Speciation = founder effect + comparative advantage structural dominance.
Extinction = fitness collapse, inactivity, pathological CCI, η violation.

This module is the living kernel. The .md documents its state; this code executes it.
"""

from .genotype import CasteBlock, EconomicBlock, FullGenotype
from .mutation import MutationEngine, MutationEvent
from .fitness import FitnessLandscape, FitnessResult
from .ecosystem import Chapter, Ecosystem, EvolutionCycle
from .trade import TradeReceipt, ComparativeAdvantageMap

__all__ = [
    "CasteBlock",
    "EconomicBlock",
    "FullGenotype",
    "MutationEngine",
    "MutationEvent",
    "FitnessLandscape",
    "FitnessResult",
    "Chapter",
    "Ecosystem",
    "EvolutionCycle",
    "TradeReceipt",
    "ComparativeAdvantageMap",
]
