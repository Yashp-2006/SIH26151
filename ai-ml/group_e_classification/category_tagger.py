"""
Group E: High-Level Dark-Web Category Tagger.
Taxonomy: drug, cyber, fraud, credential, counterfeit, other.
Emits EvidenceCandidate extensions; never outputs final confidence or merge decisions.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional

_AIML_DIR = Path(__file__).resolve().parent.parent
if str(_AIML_DIR) not in sys.path:
    sys.path.insert(0, str(_AIML_DIR))

from shared.contracts import EvidenceCandidate

DETECTOR_VERSION = "category_tagger_v0.1"

KEYWORDS: Dict[str, list[str]] = {
    "drug": ["chemical", "substance", "reagent", "compound", "capsule", "purity", "mg", "powder", "pill", "sample vial"],
    "cyber": ["exploit", "botnet", "malware", "ransomware", "payload", "cve", "ddos", "shell", "stealer", "rat"],
    "fraud": ["bank", "drop", "transfer", "western union", "carding", "fullz", "cashout", "chargeback", "escrow"],
    "credential": ["login", "combo", "database", "leak", "stealer log", "access", "corporate email", "dump", "passwords"],
    "counterfeit": ["passport", "replica", "fake id", "driver license", "ssn", "hologram", "novelty", "cloned card"],
}


def tag_category(text: str) -> Dict[str, Any]:
    """Tag text with primary category and scores across taxonomy."""
    lower = text.lower()
    scores = {}
    for cat, words in KEYWORDS.items():
        count = sum(1 for w in words if re.search(r"\b" + re.escape(w) + r"\b", lower))
        scores[cat] = count

    total = sum(scores.values())
    if total == 0:
        return {"primary_category": "other", "confidence": 0.0, "scores": scores}

    best_cat = max(scores, key=scores.get)
    confidence = round(scores[best_cat] / total, 3)
    return {"primary_category": best_cat, "confidence": confidence, "scores": scores}


def build_category_candidate(
    subject_a: str,
    subject_b: str,
    text_a: str,
    text_b: str,
    doc_ref: str,
    independence_key: Optional[str] = None,
) -> EvidenceCandidate:
    """Emits F7 (behavioural/category) EvidenceCandidate."""
    res_a = tag_category(text_a)
    res_b = tag_category(text_b)
    cat_match = res_a["primary_category"] == res_b["primary_category"] and res_a["primary_category"] != "other"
    key = independence_key or f"cat::{subject_a}__{subject_b}"

    raw_score = 0.5 if cat_match else 0.0

    return EvidenceCandidate(
        subject_a=subject_a,
        subject_b=subject_b,
        family="F7",
        raw_log_lr=raw_score,
        rarity_factor=1.0,
        independence_key=key,
        polarity="+" if cat_match else "-",
        detector_version=DETECTOR_VERSION,
        doc_ref=doc_ref,
        extra={
            "cat_a": res_a["primary_category"],
            "cat_b": res_b["primary_category"],
            "match": cat_match,
        },
    )
