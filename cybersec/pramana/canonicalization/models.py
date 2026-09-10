"""Models for the Canonicalization and Repetition layer."""

from dataclasses import dataclass, field
from typing import Optional, List, Set

@dataclass
class RepetitionReference:
    """A deterministic relation for exact source repetition (CY-POL-016/017 compatible)."""
    type: str  # e.g., "repeated_market_hash", "repeated_market_item_link", "exact_row_match", "exact_content_match"
    from_record_id: list
    to_record_id: list
    shared_value: str
    cross_snapshot: bool

@dataclass
class CanonicalTextContent:
    """Deterministic representation of prose for content comparisons."""
    source_record_id: list
    snapshot_id: list
    title_raw: Optional[str]
    description_raw: Optional[str]
    content_sha256: str
    simhash_64: int
    shingles: Set[str] = field(default_factory=set)
    content_hash_version: str = "text-pair-json-v2"

@dataclass
class NearDuplicateCandidate:
    """A deterministic comparison operand, not an attribution assertion."""
    source_record_id_1: list
    source_record_id_2: list
    hamming_distance: int
    jaccard_similarity: float
    containment_1_in_2: float
    containment_2_in_1: float
