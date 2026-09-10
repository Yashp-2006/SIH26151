"""
AI/ML List-A (deterministic) + List-B (NLP) routes, wired into the gateway.

Runs the modules from ai-ml/group_a_deterministic and ai-ml/group_b_nlp in
process. If HF_SPACE_URL is set (the deployed Hugging Face Space at
ai-ml/hf-space), those calls are proxied there instead. The synthetic test
corpus lives in the HF dataset HF_DATASET_REPO
(yashai2006/pramana-synthetic-list-a) and is consumed by the ai-ml test suite.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "ai-ml"))

HF_SPACE_URL = os.environ.get("HF_SPACE_URL", "").rstrip("/")
HF_DATASET_REPO = os.environ.get("HF_DATASET_REPO", "yashai2006/pramana-synthetic-list-a")

router = APIRouter(prefix="/nlp", tags=["ai-ml"])

# ---- local module wiring -------------------------------------------------------

_local_err = None
try:
    from group_a_deterministic.canonicalise import canonicalise_text, are_near_duplicates, sha256_id
    from group_a_deterministic.extractors import extract_indicators
    from group_b_nlp.stylometry import extract_style_features
except Exception as e:  # pragma: no cover - env-dependent
    _local_err = repr(e)


class TextPair(BaseModel):
    text: str
    text_b: Optional[str] = None


class Text(BaseModel):
    text: str


def _space_up():
    if not HF_SPACE_URL:
        return False
    try:
        return httpx.get(f"{HF_SPACE_URL}/health", timeout=2).status_code == 200
    except Exception:
        return False


@router.get("/status")
def status():
    space = _space_up()
    return {
        "list_a": "space" if space else ("local" if not _local_err else "unavailable"),
        "list_b": "space" if space else ("local" if not _local_err else "unavailable"),
        "local_import_error": _local_err,
        "hf_space_url": HF_SPACE_URL or None,
        "hf_dataset_repo": HF_DATASET_REPO,
        "modules": [
            "group_a_deterministic.extractors",
            "group_a_deterministic.canonicalise",
            "group_b_nlp.stylometry",
        ],
    }


@router.post("/extract")
def extract(body: Text):
    """List-A · deterministic indicator extraction (BTC / PGP / onion / email)."""
    if _space_up():
        return httpx.post(f"{HF_SPACE_URL}/extract", json=body.model_dump(), timeout=10).json()
    return {"indicators": extract_indicators(body.text)}


@router.post("/canonicalise")
def canonicalise(body: TextPair):
    """List-A · SimHash canonicalisation + near-duplicate check."""
    if _space_up():
        return httpx.post(f"{HF_SPACE_URL}/canonicalise", json=body.model_dump(), timeout=10).json()
    canon = canonicalise_text(body.text)
    out = {"canonical_id": sha256_id(canon), "canonical_text": canon}
    if body.text_b is not None:
        out["near_duplicate"] = are_near_duplicates(body.text, body.text_b)
    return out


@router.post("/stylometry")
def stylometry(body: Text):
    """List-B · stylometric feature vector (function words, char n-grams)."""
    if _space_up():
        return httpx.post(f"{HF_SPACE_URL}/stylometry", json=body.model_dump(), timeout=10).json()
    feats = extract_style_features(body.text)
    return {k: (dict(list(v.items())[:12]) if isinstance(v, dict) else v) for k, v in feats.items()}
