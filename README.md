# SIH26151 — PRAMANA

> **Smart India Hackathon 2026 | Problem Statement SIH26151**  
> Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails.

---

## Repository Structure

```
SIH26151/
├── ai-ml/          ← Evidence extraction, rarity scoring, wallet clustering, NLP fingerprinting
├── backend/        ← API server, auth, database layer  (WIP)
├── frontend/       ← React/Next.js dashboard UI         (WIP)
└── cybersec/       ← OSINT tooling, threat feeds, scanning pipelines (WIP)
```

---

## Modules

### `ai-ml/` — PRAMANA List-A Intelligence Engine
Python-based pipeline split across three groups:

| Group | Files | Purpose |
|-------|-------|---------|
| `group_a_deterministic/` | `extractors.py`, `rarity.py`, `canonicalise.py`, `pgp_meta.py` | Regex extraction of BTC/PGP/onion/email + IDF-based rarity scoring |
| `group_b_nlp/` | `stylometry.py`, `style_shift.py`, `lang_ner.py`, `template_fp.py` | Stylometry, language/NER tagging, listing-template fingerprinting |
| `group_c_wallet_infra/` | `wallet_cluster.py`, `temporal.py`, `infra_fp.py` | Co-spend wallet clustering, temporal overlap, TLS/favicon infra fingerprinting |
| `shared/` | `contracts.py`, `data_loader.py` | Frozen `EvidenceCandidate` dataclass, shared data loading |
| `cloudflare-workers/` | TypeScript Worker | All 6 detectors exposed as REST routes (`/extract`, `/rarity`, `/wallet`, `/temporal`, `/infra`, `/template`) on Cloudflare free tier |

### `backend/` — API Server *(coming soon)*
REST API layer connecting the AI/ML pipeline to the frontend dashboard.

### `frontend/` — Dashboard *(coming soon)*
Investigation dashboard for visualising evidence graphs and wallet clusters.

### `cybersec/` — OSINT & Threat Intelligence *(coming soon)*
Automated darknet crawling, threat feed ingestion, and scanning infrastructure.

---

## Quick Start (AI/ML)

```bash
cd ai-ml
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt

# Run tests
python -m pytest group_a_deterministic/test_group_a.py
python -m pytest group_b_nlp/test_group_b.py
python -m pytest group_c_wallet_infra/test_group_c.py
```

## Cloudflare Workers (Free Tier)

```bash
cd ai-ml/cloudflare-workers
npm install
npx wrangler login    # opens browser OAuth
npx wrangler deploy   # deploys to workers.dev
```

---

## Team
**SIH 2026 — Team SIH26151**