"""
Group F: Shortest Path Topology Features.
Measures structural proximity between subjects across the entity graph.
"""

from typing import Optional, Dict, Any
import networkx as nx

try:
    from shared.contracts import EvidenceCandidate
except ModuleNotFoundError:
    from ..shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "path_features_v0.1"


def compute_path_distance(graph: nx.Graph, source: str, target: str) -> Optional[int]:
    """
    Compute shortest path distance (hop count) between source and target.
    Returns None if no path exists or either node is missing.
    """
    if not graph.has_node(source) or not graph.has_node(target):
        return None
    try:
        return nx.shortest_path_length(graph, source=source, target=target)
    except nx.NetworkXNoPath:
        return None


def build_path_candidate(
    graph: nx.Graph,
    subject_a: str,
    subject_b: str,
    doc_ref: str,
    independence_key: Optional[str] = None,
) -> EvidenceCandidate:
    """
    Generate F8 graph EvidenceCandidate based on shortest-path proximity.
    Hops = 1 -> Direct connection (0.8 score)
    Hops = 2 -> 1 intermediary (0.4 score)
    Hops >= 3 or unreachable -> 0.0 score, '-' polarity
    """
    dist = compute_path_distance(graph, subject_a, subject_b)
    has_proximate_path = dist is not None and dist <= 2

    if dist == 1:
        raw_score = 0.8
    elif dist == 2:
        raw_score = 0.4
    else:
        raw_score = 0.0

    key = independence_key or f"path::{subject_a}__{subject_b}"

    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F8",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=key,
        polarity="+" if has_proximate_path else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={
            "path_distance": dist,
            "connected": dist is not None,
        },
    )
