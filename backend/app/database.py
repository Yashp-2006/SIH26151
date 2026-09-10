import json
from typing import AsyncGenerator

from sqlalchemy import Column, String, Integer, Text, Boolean, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./pramana_ledger.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


class ListingEventModel(Base):
    __tablename__ = "listing_events"

    event_id = Column(String, primary_key=True, index=True)
    account_id = Column(String, index=True)
    source_ref = Column(String)
    snapshot_ref = Column(String)
    listing_ref = Column(String)
    content = Column(Text)


class BalanceSheetModel(Base):
    __tablename__ = "balance_sheets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_a = Column(String, index=True)
    account_b = Column(String, index=True)
    assessment = Column(String, nullable=True)
    score_data = Column(Text, nullable=True)  # Store JSON representation of the score
    status = Column(String)


async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
