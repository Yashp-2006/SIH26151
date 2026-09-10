# backend/

Gateway between the `frontend/` dashboard and the evidence fusion engine in
`ai-ml/pramana/`. Read path only — it imports the engine directly (no HTTP hop,
no model), precomputes every candidate pair at startup, and serves the results.

Persistence (PostgreSQL ledger, JWT auth, retraction log, Z1–Z4 zones) stays
deferred per [docs/architecture.md](../docs/architecture.md).

## Run

```bash
# from repo root
python -m venv .venv && .venv/bin/pip install -r backend/requirements.txt
.venv/bin/python -m uvicorn backend.app.main:app --port 8000
# docs at http://localhost:8000/docs
```

If `frontend/dist` exists (`cd frontend && npm run build`) it is served at `/`,
so the whole prototype runs on one origin.

## Routes

| Method | Path | Returns |
|---|---|---|
| `GET` | `/health` | engine params — `lambda`, `tau`, family caps, `k_min`, ceiling |
| `GET` | `/accounts` | all RANGE-SIM personas (handle, market, identifiers, operator_id) |
| `GET` | `/pairs` | candidate pairs with ground truth and planted-case notes |
| `GET` | `/assess/{a}/{b}` | the assessment for a pair (cached) + naive baseline |
| `GET` | `/balance_sheet/{a}/{b}` | alias of `/assess` — the object the Balance Sheet renders |
| `GET` | `/metrics` | RANGE-SIM ablation: naive / no-grouping / PRAMANA |
| `GET` | `/demo` | the three curated demo cases with full assessments |
| `GET` | `/nlp/status` | which List-A/B path is live (local modules vs HF Space) |
| `POST` | `/nlp/extract` | List-A deterministic indicator extraction (BTC / PGP / onion / email) |
| `POST` | `/nlp/canonicalise` | List-A SimHash canonicalisation + near-duplicate check |
| `POST` | `/nlp/stylometry` | List-B stylometric feature vector |

Every fusion number comes from `ai-ml/pramana/score_pramana.py`. The `/nlp/*`
routes run `ai-ml/group_a_deterministic` + `ai-ml/group_b_nlp` in process, or
proxy the deployed Hugging Face Space when `HF_SPACE_URL` is set. The backend
re-derives nothing.
