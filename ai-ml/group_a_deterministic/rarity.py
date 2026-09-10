"""
IDF-style rarity scoring over a corpus of indicators.
"""
import math


HUB_THRESHOLD = 12


def compute_rarity(indicator: str, corpus_counts: dict) -> tuple:
    """
    Returns (rarity_score: float, is_hub: bool).

    rarity_score = log(N / count) where N = sum of all counts.
    is_hub = True if count > HUB_THRESHOLD (indicator appears in >12 docs).

    corpus_counts: {indicator_str: int} — occurrence counts across corpus.
    """
    count = corpus_counts.get(indicator, 0)
    is_hub = count > HUB_THRESHOLD

    if count == 0:
        # Unseen: maximum rarity
        return (float("inf"), False)

    n = sum(corpus_counts.values()) or 1
    rarity_score = math.log(n / count)
    return (rarity_score, is_hub)
