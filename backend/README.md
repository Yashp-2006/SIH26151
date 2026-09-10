# backend/

API server connecting the PRAMANA evidence pipeline to the frontend investigation dashboard.

> **Status:** Architecture specified. AI/ML resolution and evidence fusion algorithms reside in `ai-ml/pramana/` and edge workers in `ai-ml/cloudflare-workers/`.

## Planned Stack
- **FastAPI / Python:** REST endpoints wrapping the PRAMANA evidence ledger and query views
- **PostgreSQL 16:** Provenance-sealed evidence store, graph projections, and audit log
- **Auth Layer:** Cloudflare Access / JWT; trust zones Z1–Z4
- **Persistence:** Analyst notes, manual review decisions, and retraction propagation
