"""
Group D: Text Embedding Similarity & Feature Generation.
Uses sentence-level embedding or lightweight cosine similarity over character/word n-grams.
Emits EvidenceCandidate extensions; never outputs final confidence or merge decisions.
"""

import math
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

_AIML_DIR = Path(__file__).resolve().parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate
from shared.redaction import redact_identifiers

DETECTOR_VERSION = "text_embeddings_v0.1"


def _char_ngram_vector(text: str, n: int = 3) -> Counter:
    cleaned = re.sub(r"\s+", " ", text.lower().strip())
    if len(cleaned) < n:
        return Counter([cleaned])
    return Counter(cleaned[i:i + n] for i in range(len(cleaned) - n + 1))


def _cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
    dot = sum(vec_a[k] * vec_b[k] for k in vec_a if k in vec_b)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def compute_text_similarity(text_a: str, text_b: str, *, model=None) -> float:
    """
    Compute sentence/document similarity score [0.0, 1.0].
    Deterministic character n-gram cosine by default; an explicit model is optional.
    """
    if not text_a.strip() or not text_b.strip():
        return 0.0
    text_a = redact_identifiers(text_a)
    text_b = redact_identifiers(text_b)
    if model is not None:
        # Caller selects and loads a pinned model explicitly; failures propagate.
        emb_a, emb_b = model.encode(text_a), model.encode(text_b)
        sim = float(model.similarity(emb_a, emb_b)[0][0])
        if not math.isfinite(sim):
            raise ValueError("Embedding model returned nonfinite similarity")
        return max(0.0, min(1.0, sim))
    sim = _cosine_similarity(_char_ngram_vector(text_a), _char_ngram_vector(text_b))
    return max(0.0, min(1.0, round(sim, 4)))


def build_text_embedding_candidate(
    subject_a: str,
    subject_b: str,
    text_a: str,
    text_b: str,
    doc_ref: str,
    independence_key: Optional[str] = None,
) -> EvidenceCandidate:
    """Construct EvidenceCandidate extension without authoritative merge claim."""
    sim = compute_text_similarity(text_a, text_b)
    # Scaled feature score capped at 1.0 for F6 linguistic family
    raw_score = round(sim * 1.0, 3)
    key = independence_key or f"text_emb::{subject_a}__{subject_b}"

    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F6",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=key,
        polarity="+" if sim >= 0.5 else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={"similarity_score": sim, "method": "character_trigram_cosine"},
    )
