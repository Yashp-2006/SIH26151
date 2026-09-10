"""
Group D: Image Feature & Perceptual Embedding Similarity.
Computes image visual similarity [0.0, 1.0] and constructs F5 content artefact candidates.
"""

import os
import sys
from pathlib import Path
from typing import Optional

_AIML_DIR = Path(__file__).resolve().parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "image_embeddings_v0.1"


def compute_image_similarity(path_a: str, path_b: str) -> float:
    """
    Compute visual similarity between two image files.
    Uses imagehash/PIL if available, returning normalized similarity [0.0, 1.0].
    """
    if not os.path.exists(path_a) or not os.path.exists(path_b):
        return 0.0

    try:
        import importlib
        pil_image = importlib.import_module("PIL.Image")
        imagehash = importlib.import_module("imagehash")
        hash_a = imagehash.phash(pil_image.open(path_a))
        hash_b = imagehash.phash(pil_image.open(path_b))
        diff = hash_a - hash_b
        # 64-bit phash: distance 0 -> 1.0, distance >= 32 -> 0.0
        sim = max(0.0, 1.0 - (diff / 32.0))
        return round(sim, 4)
    except Exception:
        # Fallback comparison by file size ratio
        sa = os.path.getsize(path_a)
        sb = os.path.getsize(path_b)
        if max(sa, sb) == 0:
            return 1.0
        return round(min(sa, sb) / max(sa, sb), 4)


def build_image_embedding_candidate(
    subject_a: str,
    subject_b: str,
    path_a: str,
    path_b: str,
    doc_ref: str,
    independence_key: Optional[str] = None,
) -> EvidenceCandidate:
    """Build F5 EvidenceCandidate based on visual embedding similarity."""
    sim = compute_image_similarity(path_a, path_b)
    raw_score = round(sim * 2.5, 3)
    key = independence_key or f"img_emb::{subject_a}__{subject_b}"

    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F5",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=key,
        polarity="+" if sim >= 0.75 else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={"visual_similarity": sim, "path_a": path_a, "path_b": path_b},
    )
