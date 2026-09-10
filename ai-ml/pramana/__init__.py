"""
PRAMANA Evidence Fusion Package (List B).
Resolution, independence grouping, hub suppression, and likelihood-ratio fusion.
"""

try:
    from pramana.schema import Observation, Assessment, FamilyResult, CounterEvidence, verbal_band
    from pramana.score_pramana import assess, merged, LAMBDA, K_MIN, CEILING, CAPS
    from pramana.rarity import RarityIndex, TAU
except ModuleNotFoundError:
    from .schema import Observation, Assessment, FamilyResult, CounterEvidence, verbal_band
    from .score_pramana import assess, merged, LAMBDA, K_MIN, CEILING, CAPS
    from .rarity import RarityIndex, TAU

__all__ = [
    "Observation",
    "Assessment",
    "FamilyResult",
    "CounterEvidence",
    "verbal_band",
    "assess",
    "merged",
    "LAMBDA",
    "K_MIN",
    "CEILING",
    "CAPS",
    "RarityIndex",
    "TAU",
]
