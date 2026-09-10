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
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import (
    BaseModel,
    ConfigDict,
    FiniteFloat,
    JsonValue,
    StringConstraints,
    model_validator,
)
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka import AIOKafkaProducer

from backend.app.database import init_db, get_db, ListingEventModel
from backend.app.auth import Token, create_access_token, get_current_user, TokenData

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = None

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


class ListingEvent(StrictModel):
    event_id: Identifier
    account_id: Identifier
    source_ref: Identifier
    snapshot_ref: Identifier
    listing_ref: Identifier
    content: Annotated[str, StringConstraints(strict=True, min_length=1, max_length=100_000)]


class IngestRequest(StrictModel):
    topic: Literal["pramana.listings"] = "pramana.listings"
    listing: ListingEvent


class IngestAcknowledgement(StrictModel):
    mode: Literal["production"] = "production"
    received: Literal[True] = True
    receipt_sha256: str
    event_id: Identifier
    topic: str
    persisted: bool = True
    broker_offset_committed: bool = True
    evidence_promoted: Literal[False] = False


class BalanceSheetResponse(StrictModel):
    mode: Literal["production"] = "production"
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global producer
    await init_db()
    
    # Try connecting to Kafka, fail gracefully if Kafka isn't running (for local dev)
    try:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        print("Kafka Producer started")
    except Exception as e:
        print(f"Warning: Could not connect to Kafka broker at {KAFKA_BOOTSTRAP_SERVERS}. Running without Kafka.")
        producer = None
        
    yield
    # Shutdown
    if producer:
        await producer.stop()


def create_app() -> FastAPI:
    gateway = FastAPI(
        title="PRAMANA — The Ledger Gateway",
        version="0.2.0",
        description="Production API boundary with Auth, DB, and Kafka integration.",
        lifespan=lifespan
    )

    gateway.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        max_age=600,
    )

    @gateway.post("/token", response_model=Token, tags=["auth"])
    async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        # In a real app, verify against the DB. Here we use a dummy check.
        if form_data.username != "admin" or form_data.password != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}

    @gateway.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "alive", "mode": "production", "kafka": "connected" if producer else "disconnected"}

    @gateway.post("/stream/ingest", tags=["ledger"], response_model=IngestAcknowledgement)
    async def ingest(
        request: IngestRequest, 
        current_user: Annotated[TokenData, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)
    ) -> IngestAcknowledgement:
        
        payload_dict = request.model_dump(mode="json")
        payload = json.dumps(payload_dict, sort_keys=True, separators=(",", ":")).encode("utf-8")
        
        # 1. Persist to Database
        db_event = ListingEventModel(
            event_id=request.listing.event_id,
            account_id=request.listing.account_id,
            source_ref=request.listing.source_ref,
            snapshot_ref=request.listing.snapshot_ref,
            listing_ref=request.listing.listing_ref,
            content=request.listing.content
        )
        db.add(db_event)
        await db.commit()
        
        # 2. Produce to Kafka
        kafka_success = False
        if producer:
            try:
                await producer.send_and_wait(request.topic, payload)
                kafka_success = True
            except Exception as e:
                print(f"Failed to produce to Kafka: {e}")

        return IngestAcknowledgement(
            receipt_sha256=hashlib.sha256(payload).hexdigest(),
            event_id=request.listing.event_id,
            topic=request.topic,
            persisted=True,
            broker_offset_committed=kafka_success,
        )

    @gateway.get("/assess/{account_a}/{account_b}", tags=["ledger"], response_model=BalanceSheetResponse)
    async def assess(
        account_a: str, 
        account_b: str,
        current_user: Annotated[TokenData, Depends(get_current_user)],
    ) -> BalanceSheetResponse:
        return BalanceSheetResponse(account_a=account_a, account_b=account_b)

    return gateway

app = create_app()
