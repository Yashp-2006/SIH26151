# SIH26151 — PRAMANA

> **Smart India Hackathon 2026 | Problem Statement SIH26151**
> Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails.
> "Attribution fails on the arithmetic of evidence, not the shortage of it."

---

## Repository Structure

```
SIH26151/
├── ai-ml/        ← Evidence extraction, NLP, wallet/infra fingerprinting (List-A done; List-B coming)
├── backend/      ← FastAPI server, PostgreSQL, auth, evidence ledger API  (planned)
├── frontend/     ← React/TypeScript investigation dashboard               (planned)
└── cybersec/     ← PRAMANA offline cyber review slice (IMPLEMENTED + TESTED)
```

---

## Module Overview

### `ai-ml/` — PRAMANA Intelligence Engine

Two delivery lists. **List-A is complete.** List-B is incoming.

#### List-A — Deterministic Pipeline (✅ Done)

| Sub-module | Key files | Purpose |
|---|---|---|
| `group_a_deterministic/` | `extractors.py`, `rarity.py`, `canonicalise.py`, `pgp_meta.py` | Regex extraction of BTC addresses, PGP markers, onion links, emails; IDF-based rarity scoring |
| `group_b_nlp/` | `stylometry.py`, `style_shift.py`, `lang_ner.py`, `template_fp.py` | Writing-style fingerprinting, language detection, NER tagging, listing-template hash |
| `group_c_wallet_infra/` | `wallet_cluster.py`, `temporal.py`, `infra_fp.py` | Co-spend wallet clustering, temporal overlap detection, TLS/favicon infra fingerprinting |
| `shared/` | `contracts.py`, `data_loader.py` | Frozen `EvidenceCandidate` dataclass, shared CSV/data loader |
| `cloudflare-workers/` | `src/index.ts`, `wrangler.jsonc` | All 6 detectors as REST routes on Cloudflare free tier (no paid bindings) |
| `hf-space/` | `app.py`, `Dockerfile`, `requirements.txt` | Hugging Face Space wrapper for model serving |
| `data/` | sample CSVs + stylometry/darknet archive samples | Offline test fixtures |

**Cloudflare Worker routes (free tier, deployed at `workers.dev`):**

| Route | Input | Output |
|---|---|---|
| `POST /extract` | `{text}` | BTC/PGP/onion/email indicators |
| `POST /rarity` | `{terms[], corpus_counts{}}` | IDF rarity scores |
| `POST /wallet` | `{addresses[], risk_labels{}}` | Wallet clusters + risk flags |
| `POST /temporal` | `{events[]}` | Overlap bands (ms arithmetic) |
| `POST /infra` | `{hosts[]}` | TLS/favicon fingerprint groups |
| `POST /template` | `{text}` | SHA-256 template fingerprint |

#### List-B — NLP/ML Models (🔜 Coming Soon)

| Planned sub-module | Purpose |
|---|---|
| `group_d_embeddings/` | Sentence-level embedding similarity across listings |
| `group_e_classification/` | Multi-label classifier for threat category tagging |
| `group_f_graph/` | Graph-based persona linking (co-address, co-vouching) |
| `group_g_llm_assist/` | Gated LLM feature extraction (output cannot directly write evidence) |

> **Boundary:** List-B outputs feed into `EvidenceCandidate` features only. Promotion to authoritative evidence requires DC-01–DC-06 resolution (see cybersec module).

---

### `cybersec/` — PRAMANA Offline Cyber Review Slice

Deterministic offline evidence review. **Fully implemented and tested.** No model, DB, Tor, or API key required.

**Verified:** Python 3.13.7, pytest 9.0.2 — **76 passed, 13 skipped, 0 failed.**

| Component | Path | Status | Description |
|---|---|---|---|
| Archive reader | `pramana/adapters/gwern_grams/archive_reader.py` | ✅ IMPL + TESTED | Reads pinned `grams.tar.xz`, verifies SHA-256 digest |
| CSV normalizer | `pramana/adapters/gwern_grams/normalizer.py` | ✅ IMPL + VALIDATED | Exact raw-field preservation, unknown-time handling, provenance IDs |
| Exact repetition | `pramana/canonicalization/runner.py` | ✅ IMPL + TESTED | Deterministic exact/near-match comparison operands |
| Text spans + PGP | `pramana/cyber/indicators.py` | ✅ IMPL + VALIDATED | 8,794 real spans + 1 PGP-like marker in bounded validation |
| Bitcoin format | `pramana/cyber/indicators.py` | ✅ IMPL + TESTED | Legacy Base58Check lexical validation (zero real matches in sample) |
| Hub restriction | `pramana/cyber/policy.py` | ✅ IMPL + TESTED | >12 account rule for declared BTC populations |
| Clone restriction | `pramana/cyber/policy.py` | ✅ IMPL + TESTED | Externally declared occurrence-scope suppression |
| Review packet/HTML | `pramana/cyber/review.py`, `render.py` | ✅ IMPL + TESTED | Offline JSON + escaped static HTML viewer |
| Evidence promotion | — | 🔴 DEFERRED (DC-06) | Requires field-level contract + ML/Cyber/EV sign-off |
| Persistent ledger/API | — | 📋 SPECIFIED | Planned FastAPI + PostgreSQL (backend module) |
| F6–F9 generators | — | 📋 SPECIFIED / DEFERRED | Linguistic style, social/trust, external corroboration |
| RANGE-SIM / RANGE-TOR | — | 📋 SPECIFIED | Separate evaluation manifests required |

**Demo output (reproducible, no archive needed):**
```json
{ "records": 18, "indicators": 53, "validated_evidence_candidates": 0,
  "assessment": null, "hub_accounts": 13, "promotion": "blocked_DC-06" }
```

**Authority documents:**

| Doc | Purpose |
|---|---|
| [`cybersec/TEAM_README.md`](cybersec/TEAM_README.md) | Quick start + folder map |
| [`cybersec/PRAMANA_FINAL_PROJECT_HANDOFF_v1.md`](cybersec/PRAMANA_FINAL_PROJECT_HANDOFF_v1.md) | Authoritative team consolidation, P0/P1/P2 work items |
| [`cybersec/PRAMANA_REPRODUCTION_GUIDE_v1.md`](cybersec/PRAMANA_REPRODUCTION_GUIDE_v1.md) | Step-by-step reproduction with exact expected outputs |
| `cybersec/pramana/PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md` | Frozen cyber policy (do not modify) |
| `cybersec/pramana/docs/cyber/PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md` | Frozen Grams adapter/data contract (do not modify) |

---

### `backend/` — API Server *(Planned)*

| Planned component | Purpose |
|---|---|
| FastAPI app | REST endpoints wrapping the PRAMANA evidence pipeline |
| PostgreSQL 16 | Evidence/history storage, graph views, retraction log |
| Auth layer | JWT / Cloudflare Access; Z1–Z4 trust zone enforcement |
| Review persistence | Analyst notes, reviewer decisions, retraction history |
| Graph projection | Evidence graph views over PostgreSQL (no separate graph DB) |

> Prerequisite: DC-06 field-level promotion contract must be resolved before evidence tables can be populated.

---

### `frontend/` — Investigation Dashboard *(Planned)*

| Planned component | Purpose |
|---|---|
| React + TypeScript | Investigation dashboard SPA |
| Evidence graph view | Persona nodes, indicator edges, provenance drill-down |
| Review input panel | Displays existing review packet; no invented scores or auto-accept |
| Wallet cluster explorer | Co-spend clustering visualisation |
| Temporal timeline | Overlap bands across activity windows |
| Report export | PDF / JSON export of reviewed evidence packets |

> Prerequisite: Backend read/review API must be built first. UI must not invent percentage-match scores or expose an "approve identity" control.

---

## Interface Contract (Pipeline Boundary)

```
RAW OBSERVATION  →  DETERMINISTIC DERIVATION  →  ML FEATURE  →  EVIDENCE CANDIDATE
   (cybersec)            (cybersec/canon)          (ai-ml)          ⚠ DEFERRED
                                                                   requires DC-01–DC-06
```

| Stage | Owner | Must not |
|---|---|---|
| Raw observation | Cyber / DE | Infer actor, persona, or identity from vendor_name |
| Deterministic derivation | Cyber / ML | Make origin/k decisions; emit pair scores |
| ML feature | ML | Write directly to `evidence`, `assessment`, `must_not_link` |
| Evidence candidate | ML + PL + Cyber + EV | Promote without DC-06 contract + validation fixtures |

---

## Quick Start

### Cybersec slice (works offline, no deps)
```powershell
cd cybersec/pramana
python --version          # 3.13.7
python -m pytest -q       # 76 passed, 13 skipped
python run_cyber_demo.py  # 18 records, 53 indicators, null assessment
# Open docs/cyber/demo/review.html locally
```

### AI/ML List-A pipeline
```powershell
cd ai-ml
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m pytest group_a_deterministic/test_group_a.py
python -m pytest group_b_nlp/test_group_b.py
python -m pytest group_c_wallet_infra/test_group_c.py
```

### Cloudflare Worker (free tier)
```powershell
cd ai-ml/cloudflare-workers
npm install
npx wrangler login    # browser OAuth
npx wrangler deploy   # deploys to *.workers.dev
```

---

## Delivery Status

| Module | Status | Notes |
|---|---|---|
| `ai-ml` List-A | ✅ Complete | 6 Python modules + TypeScript Worker + tests |
| `ai-ml` List-B | 🔜 Coming soon | NLP/ML model layer |
| `cybersec` | ✅ Implemented + tested | 76 passing tests, bounded real validation |
| `backend` | 📋 Planned | Needs DC-06 before evidence tables |
| `frontend` | 📋 Planned | Needs backend API first |

---

## Team
**SIH 2026 — Team SIH26151**