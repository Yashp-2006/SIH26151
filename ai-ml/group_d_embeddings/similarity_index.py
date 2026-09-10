"""
Group D: In-Memory Similarity Index for Candidate Blocking & Search.
Provides fast nearest-neighbor retrieval across text/features using cosine similarity.
"""

from typing import List, Tuple
from .text_embeddings import compute_text_similarity


class SimilarityIndex:
    """Lightweight in-memory vector/text similarity index."""

    def __init__(self):
        self.entries: List[Tuple[str, str]] = []  # (item_id, text)

    def add(self, item_id: str, text: str) -> None:
        self.entries.append((item_id, text))

    def search(self, query_text: str, top_k: int = 5, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """Return top_k items with similarity >= threshold, sorted descending."""
        scored = []
        for item_id, text in self.entries:
            sim = compute_text_similarity(query_text, text)
            if sim >= threshold:
                scored.append((item_id, sim))
        scored.sort(key=lambda x: -x[1])
        return scored[:top_k]

    def size(self) -> int:
        return len(self.entries)
