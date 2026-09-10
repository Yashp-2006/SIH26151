# backend/experimental/ — persistence-layer draft

From `archive/enterprise-backend`. A FastAPI service with SQLite (SQLAlchemy /
aiosqlite), JWT auth (pyjwt / passlib) and a Kafka producer (aiokafka) — the shape
the persistent evidence ledger (README §13, future scope) will take.

**Not wired into the demo.** The shipped gateway is `backend/app/main.py`, which
runs the fusion engine in-process. These files are the starting point for the
durable ledger + auth + trust-zone work.

```bash
pip install -r requirements.txt
python -m uvicorn backend.experimental.main:app --port 8100
```
