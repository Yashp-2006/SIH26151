# FROZEN CONTRACT — do not modify without updating all three group modules and evidence_writer.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class EvidenceCandidate:
    subject_a: str
    subject_b: str
    family: str              # one of "F1".."F9"
    raw_log_lr: float
    rarity_factor: float
    independence_key: str
    polarity: str             # "+" or "-"
    detector_version: str
    doc_ref: str
    extra: Optional[dict] = None
