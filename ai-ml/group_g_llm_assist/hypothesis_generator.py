"""
Group G: Non-Authoritative Candidate Hypothesis Generator.
Emits hypothesis structures verified against citation grounds.
NEVER emits authoritative merge decisions or alters assessment/evidence state directly.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

try:
    from shared.contracts import EvidenceCandidate
except ModuleNotFoundError:
    from ..shared.contracts import EvidenceCandidate

from .citation_validator import validate_citations

DETECTOR_VERSION = "hypothesis_gen_v0.1"


@dataclass
class HypothesisResult:
    subject_a: str
    subject_b: str
    hypothesis_text: str
    is_valid: bool
    citations: List[str]
    invalid_citations: List[str]
    is_authoritative: bool = False  # Hard contract: never authoritative
    candidate: Optional[EvidenceCandidate] = None


def generate_candidate_hypothesis(
    subject_a: str,
    subject_b: str,
    raw_hypothesis_text: str,
    valid_observation_ids: List[str],
    doc_ref: str,
) -> HypothesisResult:
    """
    Validate LLM hypothesis text against valid observation IDs.
    If grounded, builds an assistive F9 EvidenceCandidate.
    """
    val_res = validate_citations(raw_hypothesis_text, valid_observation_ids)
    is_valid = val_res["is_grounded"]

    candidate = None
    if is_valid:
        # F9: Out-of-band / Corroborated intelligence (max cap 3.0, conservative candidate score 0.3)
        candidate = EvidenceCandidate(
            subject_a=subject_a,
            subject_b=subject_b,
            family="F9",
            raw_log_lr=0.3,
            rarity_factor=1.0,
            independence_key=f"llm_hyp::{subject_a}__{subject_b}",
            polarity="+",
            detector_version=DETECTOR_VERSION,
            doc_ref=doc_ref,
            extra={
                "hypothesis": raw_hypothesis_text,
                "citations": val_res["valid_citations"],
                "authoritative": False,
            },
        )

    return HypothesisResult(
        subject_a=subject_a,
        subject_b=subject_b,
        hypothesis_text=raw_hypothesis_text,
        is_valid=is_valid,
        citations=val_res["valid_citations"],
        invalid_citations=val_res["invalid_citations"],
        is_authoritative=False,
        candidate=candidate,
    )
