import sys
from pathlib import Path
from datetime import datetime

_AIML_DIR = Path(__file__).resolve().parent.parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "f8_behavioral_ttp_v0.1"

def extract_active_hours(timestamps: list[str]) -> set[int]:
    """
    Given a list of ISO-8601 timestamps, extract the set of active hour buckets (0-23).
    """
    hours = set()
    for ts in timestamps:
        try:
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            hours.add(dt.hour)
        except ValueError:
            pass
    return hours

def compute_temporal_overlap(hours_a: set[int], hours_b: set[int]) -> float:
    if not hours_a or not hours_b:
        return 0.0
    overlap = len(hours_a.intersection(hours_b))
    union = len(hours_a.union(hours_b))
    return overlap / union if union > 0 else 0.0

def build_f8_candidate(subject_a: str, subject_b: str, timestamps_a: list[str], timestamps_b: list[str], doc_ref: str) -> EvidenceCandidate:
    """
    Evidence Family F8: Behavioral TTPs.
    Compares active posting hours. 
    """
    hours_a = extract_active_hours(timestamps_a)
    hours_b = extract_active_hours(timestamps_b)
    
    sim = compute_temporal_overlap(hours_a, hours_b)
    
    # Cap for F8 Behavioral is 2.0 (from README)
    raw_score = round(sim * 2.0, 3)
    
    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F8",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=f"behavioral::{subject_a}__{subject_b}",
        polarity="+" if sim >= 0.5 else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={"temporal_overlap": sim}
    )
