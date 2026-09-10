"""
Group F: Entity Co-Occurrence Graph Analysis.
Emits F8 graph evidence candidates based on shared document appearances.
"""

from collections import defaultdict
from itertools import combinations
from pathlib import Path
import sys
from typing import List, Dict, Tuple, Optional
import networkx as nx

_AIML_DIR = Path(__file__).resolve().parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "co_occurrence_v0.1"


class CoOccurrenceGraph:
    """Manages entity co-occurrence counts and builds NetworkX graphs."""

    def __init__(self):
        self.graph = nx.Graph()
        self.doc_entity_map: Dict[str, List[str]] = {}

    def add_document(self, doc_id: str, entities: List[str]) -> None:
        """Add unique entities present within a single document context."""
        unique_entities = sorted(list(set(entities)))
        self.doc_entity_map[doc_id] = unique_entities

        for ent in unique_entities:
            if not self.graph.has_node(ent):
                self.graph.add_node(ent, doc_count=0)
            self.graph.nodes[ent]["doc_count"] += 1

        for ent_a, ent_b in combinations(unique_entities, 2):
            if self.graph.has_edge(ent_a, ent_b):
                self.graph[ent_a][ent_b]["weight"] += 1
            else:
                self.graph.add_edge(ent_a, ent_b, weight=1)

    def get_co_occurrence(self, entity_a: str, entity_b: str) -> int:
        """Return the co-occurrence weight between two entities."""
        if self.graph.has_edge(entity_a, entity_b):
            return int(self.graph[entity_a][entity_b].get("weight", 0))
        return 0


def build_cooccurrence_candidate(
    graph: CoOccurrenceGraph,
    subject_a: str,
    subject_b: str,
    doc_ref: str,
    min_count: int = 1,
    independence_key: Optional[str] = None,
) -> EvidenceCandidate:
    """
    Produce an F8 EvidenceCandidate from entity co-occurrence frequency.
    Caps raw_log_lr at 1.0 (family F8 limit).
    """
    count = graph.get_co_occurrence(subject_a, subject_b)
    has_cooc = count >= min_count

    # Max F8 cap is 1.0; 1 occurrence = 0.3, 2 = 0.6, 3+ = 0.9
    raw_score = min(1.0, round(count * 0.3, 2)) if has_cooc else 0.0
    key = independence_key or f"cooc::{subject_a}__{subject_b}"

    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F8",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=key,
        polarity="+" if has_cooc else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={
            "co_occurrence_count": count,
            "min_count": min_count,
        },
    )
