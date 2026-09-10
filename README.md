# SIH26151 — PRAMANA

> **Smart India Hackathon 2026 | Problem Statement SIH26151**
> Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails.
> "Attribution fails on the arithmetic of evidence, not the shortage of it."

---

## Repository Structure

```
SIH26151/
├── ai-ml/        ← Evidence extraction, NLP, wallet/infra fingerprinting (List-A Complete; List-B Pending)
├── backend/      ← FastAPI server, PostgreSQL, auth, evidence ledger API (Planned)
├── frontend/     ← React/TypeScript investigation dashboard              (Planned)
└── cybersec/     ← PRAMANA offline cyber review slice                    (Implemented & Tested)
```

---

## Module Overview

### `ai-ml/` — PRAMANA Intelligence Engine

Two delivery lists. **List-A is complete.** List-B is pending.

#### List-A — Deterministic Pipeline (Complete)

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

#### List-B — NLP/ML Models (Pending)

Four sub-modules, mirroring List-A's group structure. Every module returns feature-level
`EvidenceCandidate` extensions only — none may write to `evidence`, `assessment`, or
`must_not_link` directly (see Interface Contract above; promotion requires DC-01–DC-06).

| Sub-module | Key files | Purpose |
|---|---|---|
| `group_d_embeddings/` | `text_embeddings.py`, `image_embeddings.py`, `similarity_index.py`, `test_group_d.py` | Sentence-level embedding similarity across listings/posts (paraphrase-robust, complements F5/F6 hash-based similarity); perceptual embedding similarity for images beyond exact pHash matches; ANN index (FAISS or brute-force cosine for prototype scale) for candidate retrieval |
| `group_e_classification/` | `threat_classifier.py`, `category_tagger.py`, `confidence_calibration.py`, `test_group_e.py` | Multi-label classifier for threat/category tagging on listings and posts (drugs, weapons, fraud, digital-goods, etc.); per-label confidence score, not an identity or attribution signal |
| `group_f_graph/` | `graph_builder.py`, `persona_linker.py`, `path_features.py`, `test_group_f.py` | Graph-based persona linking features: co-address, co-vouching, co-membership, shared-neighbor overlap; outputs graph-derived similarity/rarity features only — no automatic transitive closure or cluster merge decisions (that stays with cybersec/backend evidence-resolution stage) |
| `group_g_llm_assist/` | `llm_extractor.py`, `evidence_summarizer.py`, `citation_validator.py`, `test_group_g.py` | Gated LLM-assisted feature extraction (entity/relationship suggestions, natural-language evidence summaries); every output must carry a source citation and pass `citation_validator.py` before being staged — output cannot directly write evidence, per project AI/ML governance rule |

**Shared constraints across all four groups:**
- All feature outputs use the frozen `EvidenceCandidate` shape from `shared/contracts.py` — put anything not covered by existing fields into `extra`, never a new top-level field.
- No module may output a merge/match decision, a pair score used as final confidence, or a persona/identity claim — these remain deferred pending DC-06.
- Each module must include a `test_group_x.py` validating against the existing `data/` fixtures (and any new fixtures it adds), matching List-A's test convention.
- CPU-only where feasible; if `group_d_embeddings` needs a model over ~300MB (e.g. a larger sentence-transformer), call it via a hosted API/HF Inference route rather than bundling it into the Cloudflare Worker or local test run.

**Deployment target:** same split as List-A — lightweight feature math (e.g. `path_features.py`, `category_tagger.py` scoring) can go on Cloudflare Workers; embedding/classification/LLM modules needing real models go on the `hf-space/` FastAPI service.

**Before starting `group_f_graph`:** read `cybersec/pramana/PRAMANA_Master_Blueprint.md` Section 7 on
entity resolution — this module must stay feature-generation only and must not make origin/k decisions
or emit pair scores, per the Interface Contract table above.

**Before starting `group_g_llm_assist`:** read `cybersec/pramana/cyber/review.py` and `policy.py` for
the existing citation-gated, non-authoritative promotion pattern (see the `"blocked_DC-06"` demo output)
— `citation_validator.py` should follow the same pattern rather than inventing a new one.

---

### `cybersec/` — PRAMANA Offline Cyber Review Slice

Deterministic offline evidence review. **Fully implemented and tested.** No model, DB, Tor, or API key required.

**Verified:** Python 3.13.7, pytest 9.0.2 — **76 passed, 13 skipped, 0 failed.**

| Component | Path | Status | Description |
|---|---|---|---|
| Archive reader | `pramana/adapters/gwern_grams/archive_reader.py` | Implemented & Tested | Reads pinned `grams.tar.xz`, verifies SHA-256 digest |
| CSV normalizer | `pramana/adapters/gwern_grams/normalizer.py` | Implemented & Validated | Exact raw-field preservation, unknown-time handling, provenance IDs |
| Exact repetition | `pramana/canonicalization/runner.py` | Implemented & Tested | Deterministic exact/near-match comparison operands |
| Text spans + PGP | `pramana/cyber/indicators.py` | Implemented & Validated | 8,794 real spans + 1 PGP-like marker in bounded validation |
| Bitcoin format | `pramana/cyber/indicators.py` | Implemented & Tested | Legacy Base58Check lexical validation (zero real matches in sample) |
| Hub restriction | `pramana/cyber/policy.py` | Implemented & Tested | >12 account rule for declared BTC populations |
| Clone restriction | `pramana/cyber/policy.py` | Implemented & Tested | Externally declared occurrence-scope suppression |
| Review packet/HTML | `pramana/cyber/review.py`, `render.py` | Implemented & Tested | Offline JSON + escaped static HTML viewer |
| Evidence promotion | — | Deferred (DC-06) | Requires field-level contract + ML/Cyber/EV sign-off |
| Persistent ledger/API | — | Specified | Planned FastAPI + PostgreSQL (backend module) |
| F6–F9 generators | — | Specified / Deferred | Linguistic style, social/trust, external corroboration |
| RANGE-SIM / RANGE-TOR | — | Specified | Separate evaluation manifests required |

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
   (cybersec)            (cybersec/canon)          (ai-ml)          [DEFERRED]
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
| `ai-ml` List-A | Complete | 6 Python modules + TypeScript Worker + tests |
| `ai-ml` List-B | Pending | NLP/ML model layer |
| `cybersec` | Implemented & Tested | 76 passing tests, bounded real validation |
| `backend` | Planned | Needs DC-06 before evidence tables |
| `frontend` | Planned | Needs backend API first |

---

## Team
**SIH 2026 — Team SIH26151**