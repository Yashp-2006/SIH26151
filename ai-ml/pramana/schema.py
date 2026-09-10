"""
PRAMANA | FROZEN INTERFACE  v0.1
The only contract between Person A (evidence generation) and Person B (fusion).
Change this and the split silently breaks.

RULE:  A emits WHAT MATCHED and WHERE IT CAME FROM.
       A never emits a weight, a score, or a likelihood ratio.
       B assigns rarity, hub status, log-LR, damping, caps and the verdict.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


# ----------------------------------------------------------------- A -> B

@dataclass
class Observation:
    """One indicator that matched across a candidate pair. Emitted by Person A."""
    pair_id: str
    family: str                  # F1..F9
    indicator_type: str          # "pgp_fp", "contact_id", "asn", "template_id", "image_id"
    indicator_value: str         # the actual shared value  -> B counts its corpus frequency
    match_type: str              # "exact" | "phash" | "simhash" | "cosine"
    independence_key: str        # WHICH CAPTURE this observation came from.
                                 # Same key on two rows = ONE observation, not two.
    similarity: float = 1.0      # raw, uncalibrated. 1.0 for exact match.
    n_raw_hits: int = 1          # how many raw retrievals collapsed into this row

    # deliberately absent: raw_log_lr, rarity_factor, weight, is_hub


# ----------------------------------------------------------------- B -> world

@dataclass
class FamilyResult:
    family: str
    raw_log_lr: float            # sum of group contributions before cap
    damped_log_lr: float         # after lambda damping
    capped_log_lr: float         # after family cap
    n_groups: int
    discount_reason: str         # <- THIS is the Evidence Balance Sheet


@dataclass
class CounterEvidence:
    contradiction_class: str
    severity: str                # "soft" | "hard"
    delta: float                 # log10 LR subtracted (0.0 for hard vetoes)
    explanation: str


@dataclass
class Assessment:
    pair_id: str
    account_a: str
    account_b: str
    issued: bool                 # False = system refused to score
    excluded: bool               # True = hard must-not-link fired
    log_lr: Optional[float]
    verbal_band: Optional[str]
    family_count_k: int
    distinct_independence_keys: int
    families: list = field(default_factory=list)
    counter_evidence: list = field(default_factory=list)
    defence_hypothesis: str = ""
    limitations: list = field(default_factory=list)
    refusal_reason: str = ""
    params_version: str = "v0.1"

    def to_dict(self):
        d = asdict(self)
        return d


BANDS = [(0.0, 1.0, "LIMITED"), (1.0, 2.0, "MODERATE"),
         (2.0, 3.0, "MODERATELY STRONG"), (3.0, 4.01, "STRONG")]


def verbal_band(x: float) -> str:
    for lo, hi, name in BANDS:
        if lo <= x < hi:
            return name
    return "LIMITED" if x < 0 else "STRONG"
