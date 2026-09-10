"""
Pramana List-A — HF Space FastAPI app
Routes: /health /canonicalise /pgp /lang /stylometry /style-shift
CPU-only. spaCy en_core_web_sm baked into Docker image.
"""
import sys
import os

# Add parent dir so 'shared', 'group_a_deterministic', 'group_b_nlp' resolve
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ── module imports ────────────────────────────────────────────────────────────

from group_a_deterministic.canonicalise import (
    canonicalise_text,
    are_near_duplicates,
    sha256_id,
)
from group_a_deterministic.pgp_meta import parse_pgp_key
from group_b_nlp.lang_ner import analyze_text
from group_b_nlp.stylometry import extract_style_features
from group_b_nlp.style_shift import detect_style_shift

# ── lifespan (startup log) ────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] pramana-hf-space ready", flush=True)
    yield
    print("[shutdown] pramana-hf-space stopping", flush=True)

app = FastAPI(
    title="Pramana List-A",
    description="NLP + deterministic analysis routes for Group A/B modules.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── /health ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    """Keep-alive ping — call before demo to warm the space."""
    return {"status": "ok"}

# ── /canonicalise ─────────────────────────────────────────────────────────────

class CanonicaliseRequest(BaseModel):
    text: str
    text_b: str | None = None  # optional second text for near-dup check
    threshold: int = 3

class CanonicaliseResponse(BaseModel):
    simhash: str
    sha256: str
    near_duplicate: bool | None = None  # only when text_b provided

@app.post("/canonicalise", response_model=CanonicaliseResponse, response_model_exclude_none=True)
def route_canonicalise(req: CanonicaliseRequest) -> Any:
    """
    Returns SimHash hex + SHA-256 for text.
    If text_b is provided, also returns near_duplicate boolean.
    """
    simhash = canonicalise_text(req.text)
    sha = sha256_id(req.text)
    near_dup = None
    if req.text_b is not None:
        near_dup = are_near_duplicates(req.text, req.text_b, req.threshold)
    return CanonicaliseResponse(simhash=simhash, sha256=sha, near_duplicate=near_dup)

# ── /pgp ──────────────────────────────────────────────────────────────────────

class PgpRequest(BaseModel):
    block: str  # ASCII-armored PGP public key block

class SubkeyInfo(BaseModel):
    key_id: str
    algorithm: str

class PgpResponse(BaseModel):
    algorithm: str
    key_size: str | int | None = None
    created: str | None = None
    subkeys: list[SubkeyInfo] = []
    uids: list[str] = []

@app.post("/pgp", response_model=PgpResponse)
def route_pgp(req: PgpRequest) -> Any:
    """
    Parse PGP public key block.
    Returns algorithm, key_size, created, subkeys, uids.
    Raises 422 on parse failure.
    """
    result = parse_pgp_key(req.block)
    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])
    return result

# ── /lang ─────────────────────────────────────────────────────────────────────

class LangRequest(BaseModel):
    text: str

class LangResponse(BaseModel):
    language: str
    entities: list[str]
    crypto_addresses: list[str]

@app.post("/lang", response_model=LangResponse)
def route_lang(req: LangRequest) -> Any:
    """Language detection + NER (spaCy en_core_web_sm) + BTC address extraction."""
    return analyze_text(req.text)

# ── /stylometry ───────────────────────────────────────────────────────────────

class StyleRequest(BaseModel):
    text: str

class StyleResponse(BaseModel):
    function_words: dict[str, int]
    char_ngrams: dict[str, int]

@app.post("/stylometry", response_model=StyleResponse)
def route_stylometry(req: StyleRequest) -> Any:
    """Extract function-word frequencies and top-50 char 3-grams."""
    return extract_style_features(req.text)

# ── /style-shift ──────────────────────────────────────────────────────────────

class StyleShiftRequest(BaseModel):
    documents: list[str]

class ShiftResult(BaseModel):
    doc_index: int
    shift_score: float

@app.post("/style-shift", response_model=list[ShiftResult])
def route_style_shift(req: StyleShiftRequest) -> Any:
    """
    Detect style drift across a sequence of documents.
    Returns shift_score per document (0.0 for the first doc).
    """
    if not req.documents:
        return []
    return detect_style_shift(req.documents)
