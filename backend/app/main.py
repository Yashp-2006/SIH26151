"""PRAMANA gateway contract prototype.

Represents "The Ledger" API boundary. Kafka consumption, durable persistence,
ML integration, evidence promotion, and qualified assessments remain deferred.
Simulation responses must never be interpreted as authoritative evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Annotated, Literal
from urllib.parse import urlsplit

from fastapi import FastAPI, HTTPException, Path as FastAPIPath, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    JsonValue,
    StringConstraints,
    model_validator,
)

Identifier = Annotated[
    str,
    StringConstraints(
        strict=True,
        min_length=1,
        max_length=256,
        pattern=r"^\S(?:[\s\S]*\S)?$",
    ),
]

Family = Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]


class StrictModel(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        allow_inf_nan=False,
    )


class EvidenceCandidate(StrictModel):
    subject_a: Identifier
    subject_b: Identifier
    family: Family
    raw_log_lr: FiniteFloat
    rarity_factor: FiniteFloat
    independence_key: Identifier
    polarity: Literal["+", "-"]
    detector_version: Identifier
    doc_ref: Identifier
    extra: dict[str, JsonValue] | None = None


class AttributionRequest(StrictModel):
    account_a: Identifier
    account_b: Identifier

    @model_validator(mode="after")
    def require_distinct_accounts(self) -> AttributionRequest:
        if self.account_a == self.account_b:
            raise ValueError("Two distinct observed account references are required")
        return self


class ListingEvent(StrictModel):
    event_id: Identifier
    account_id: Identifier
    source_ref: Identifier
    snapshot_ref: Identifier
    listing_ref: Identifier
    content: Annotated[str, StringConstraints(strict=True, min_length=1, max_length=100_000)]


class IngestRequest(StrictModel):
    topic: Literal["pramana.listings.simulated"] = "pramana.listings.simulated"
    listing: ListingEvent


class IngestAcknowledgement(StrictModel):
    mode: Literal["simulation"] = "simulation"
    received: Literal[True] = True
    receipt_sha256: str
    event_id: Identifier
    topic: Literal["pramana.listings.simulated"]
    persisted: Literal[False] = False
    broker_offset_committed: Literal[False] = False
    evidence_promoted: Literal[False] = False


class BalanceSheetResponse(StrictModel):
    mode: Literal["simulation"] = "simulation"
    account_a: Identifier
    account_b: Identifier
    status: Literal["not_run"] = "not_run"
    issued: Literal[False] = False
    assessment: None = None
    score: None = None
    evidence_balance_sheet: None = None
    counter_evidence_status: Literal["not_run"] = "not_run"
    hard_veto_status: Literal["not_run"] = "not_run"
    promotion_status: Literal["blocked_DC-06"] = "blocked_DC-06"
    review_state: Literal["awaiting_human_review"] = "awaiting_human_review"
    limitations: tuple[str, ...] = (
        "No ML engine was called.",
        "No account existence or provenance verification was performed.",
        "No evidence was promoted, scored, or used for a veto.",
        "No identity claim or persona acceptance is produced.",
    )


def configured_origins() -> list[str]:
    origins: list[str] = []
    for value in os.getenv("PRAMANA_CORS_ORIGINS", "").split(","):
        origin = value.strip()
        if not origin:
            continue
        parsed = urlsplit(origin)
        if origin not in origins:
            origins.append(origin)
    return origins


def create_app() -> FastAPI:
    gateway = FastAPI(
        title="PRAMANA — The Ledger Gateway",
        version="0.1.0",
        description="Contract prototype for The Ledger API boundary.",
    )

    gateway.add_middleware(
        CORSMiddleware,
        allow_origins=configured_origins() or ["*"], # Open for demo
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        max_age=600,
    )

    @gateway.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "alive", "mode": "simulation"}

    @gateway.post("/stream/ingest", tags=["ledger"], response_model=IngestAcknowledgement)
    async def ingest(request: IngestRequest) -> IngestAcknowledgement:
        payload = json.dumps(
            request.model_dump(mode="json"),
            sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return IngestAcknowledgement(
            receipt_sha256=hashlib.sha256(payload).hexdigest(),
            event_id=request.listing.event_id,
            topic=request.topic,
        )

    @gateway.get("/assess/{account_a}/{account_b}", tags=["ledger"], response_model=BalanceSheetResponse)
    async def assess(account_a: str, account_b: str) -> BalanceSheetResponse:
        return BalanceSheetResponse(account_a=account_a, account_b=account_b)

    # --- GEMINI INTEGRATION: EMPIRICAL CALIBRATION ---
    @gateway.get("/calibration/tippett", tags=["math"])
    async def get_tippett_calibration():
        """Returns the Empirical Calibration metrics (ECE & Tippett) natively hooking into the ML engine."""
        aiml_path = str(Path(__file__).resolve().parent.parent.parent.parent / "ai-ml")
        if aiml_path not in sys.path:
            sys.path.insert(0, aiml_path)
        
        try:
            from pramana.evaluate import load_key
            from pramana.stub_features_a import emit_all
            from pramana.rarity import RarityIndex
            from pramana.score_pramana import assess as pramana_assess
            from pramana.calibration import expected_calibration_error, generate_tippett_coordinates
            
            directory = Path(aiml_path) / "pramana"
            accounts, pairs, obs_by_pair = emit_all(directory / "accounts.json", directory / "pairs.csv")
            rarity = RarityIndex(directory / "accounts.json")
            key = load_key(directory / "answer_key.csv")
            
            predictions = []
            for r in pairs:
                a, b = r["account_a"], r["account_b"]
                pid = f"{a}__{b}"
                t = (key[a] == key[b])
                obs = obs_by_pair[pid]
                p = pramana_assess(pid, a, b, obs, rarity, accounts)
                if p.issued and not p.excluded:
                    predictions.append((p.log_lr, t))
            
            ece = expected_calibration_error(predictions)
            tippett = generate_tippett_coordinates(predictions)
            
            return {
                "ece_score": ece,
                "model": "pramana-core-v0.1",
                "tippett_data": tippett
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return gateway

app = create_app()
