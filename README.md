# SIH26151 — PRAMANA

## 1. Project Information

- **Project Title:** PRAMANA — Evidence-Centric Attribution Platform for Dark Web Threat Actors
- **PS ID:** SIH26151
- **PS Title:** Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails
- **Category:** Software
- **Theme:** Blockchain & Cybersecurity (NTRO)
- **Team Name:** localhost:3000
- **Team ID:** *Not yet assigned — internal hackathon round, will be updated once issued*

## 2. Problem Statement

Dark-web operators rarely appear as a single clean identifier. The same underlying actor may surface
through multiple marketplace accounts, forum handles, PGP keys, payment addresses, images, and
infrastructure traces — while unrelated actors may share the same surface signals. Treating every
observed similarity as independent evidence produces false merges: a shared escrow address, a default
PGP block, or a copied listing template can all appear to corroborate the same person even when their
only common cause is the surrounding ecosystem. A missed link delays an investigation; a false link
contaminates every downstream hypothesis that reuses it. Attribution fails on the arithmetic of
evidence, not the shortage of it.

## 3. Proposed Solution

PRAMANA is an evidence-accounting platform, not a scraper or a similarity dashboard. Raw observations
are canonicalised, checked for independence, weighted by rarity, and only then combined into a
calibrated likelihood-ratio assessment — with an explicit counter-evidence pass, a hard-exclusion state
for contradicted hypotheses, and full provenance back to the source evidence. The system never emits a
bare match percentage: every assessment carries a verbal confidence band, the count of independent
evidence families behind it, the competing "different actor" hypothesis, and its known limitations.
A human analyst remains the sole author of any attribution conclusion.

## 4. Key Features

- Deterministic evidence extraction (PGP metadata, wallet indicators, onion/contact identifiers)
- Canonicalisation and clone detection to prevent duplicate evidence from being double-counted
- Independence-aware, capped log-likelihood-ratio evidence fusion across 9 evidence families (F1–F9)
- Explicit counter-evidence detection with a hard `EXCLUDED` state, not just a low score
- Calibrated confidence output (verbal bands, not raw percentages) with measured false-merge rate
- Evidence Balance Sheet: full traceability from raw observation to final assessment
- Offline, deterministic cybersecurity review slice — no live Tor access or credentialed scraping
- REST API layer (FastAPI) exposing extraction, fusion, and balance-sheet endpoints

## 5. Technology Stack

- **Frontend:** React, TypeScript (planned)
- **Backend:** Python, FastAPI, PostgreSQL 16
- **AI/ML:** scikit-learn, sentence-transformers, spaCy, Splink-style probabilistic linkage, SimHash/pHash, custom log-LR fusion engine
- **Cybersecurity/Evidence Review:** Deterministic Python pipeline (canonicalisation, indicator extraction, policy enforcement) — no external model dependency
- **Deployment:** Cloudflare Workers (free tier) for lightweight detectors, Hugging Face Spaces (free CPU tier) for model-backed services, Docker for local reproduction

## 6. Architecture

See [docs/architecture.md](docs/architecture.md).

```text
Raw Observation
      |
      v
Deterministic Derivation (cybersec: canonicalisation, indicator extraction, policy)
      |
      v
ML Feature Generation (ai-ml: List-A deterministic signals, List-B NLP/embedding/graph/LLM features)
      |
      v
Evidence Fusion Engine (ai-ml/pramana: independence grouping, rarity weighting, capped log-LR fusion,
                          counter-evidence, calibration)
      |
      v
Evidence Candidate -> Assessment (log-LR, verbal band, k, defence hypothesis, EXCLUDED state)
      |
      v
Backend API (FastAPI + PostgreSQL evidence ledger) [Planned]
      |
      v
Frontend Investigation Dashboard [Planned]
```

## 7. Repository Structure

```text
SIH26151/
├── README.md
├── SUBMISSION_GUIDE.md
├── FOLDER_STRUCTURE.md
├── submission/
│   ├── PRESENTATION.md
│   └── DEMO.md
├── ai-ml/
│   ├── group_a_deterministic/     # List-A: regex/hash extraction, rarity scoring
│   ├── group_b_nlp/                # List-A: stylometry, style-shift, language ID, template fingerprint
│   ├── group_c_wallet_infra/       # List-A: wallet clustering, temporal overlap, infra fingerprinting
│   ├── group_d_embeddings/         # List-B: sentence/image embedding similarity
│   ├── group_e_classification/     # List-B: category tagging, risk classification, evasion detection
│   ├── group_f_graph/              # List-B: co-occurrence and graph-derived persona-link features
│   ├── group_g_llm_assist/         # List-B: gated, citation-validated LLM-assisted hypotheses
│   ├── pramana/                    # Evidence Fusion Engine, RANGE-SIM harness, FastAPI service
│   ├── shared/                     # Frozen EvidenceCandidate contract + data loader
│   ├── cloudflare-workers/         # Free-tier REST routes for List-A detectors
│   ├── hf-space/                   # Hugging Face Space wrapper for model serving
│   ├── data/                       # Offline test fixtures
│   └── tests/
├── backend/                        # FastAPI server, PostgreSQL, auth, evidence ledger API [Planned]
├── frontend/                       # React/TypeScript investigation dashboard [Planned]
├── cybersec/                       # Offline cyber review slice (canonicalisation, indicators, policy)
├── docs/
│   └── architecture.md
├── assets/
│   └── screenshots/
│       └── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

### What goes where?

| Item | Location |
|---|---|
| Source code | `ai-ml/`, `backend/`, `frontend/`, `cybersec/` |
| Architecture / technical documentation | `docs/`, `cybersec/pramana/PRAMANA_Master_Blueprint.md` |
| Project screenshots / prototype photos | `assets/screenshots/` |
| Final PPT / presentation | `submission/PRESENTATION.md` |
| Demo video link | `submission/DEMO.md` |
| Project overview | `README.md` (this file) |

## 8. Final Presentation

See [submission/PRESENTATION.md](submission/PRESENTATION.md) for the required format. If the PPT is
too large for GitHub, use Google Drive/OneDrive and put the accessible viewer link there.

## 9. Demo Video

Add the YouTube/Google Drive link in [submission/DEMO.md](submission/DEMO.md).

## 10. Screenshots / Prototype Photos

Add important screenshots to `assets/screenshots/`. See
[assets/screenshots/README.md](assets/screenshots/README.md) for naming conventions.

## 11. Installation

```bash
git clone <YOUR_REPOSITORY_URL>
cd SIH26151

# Cybersec slice (offline, no dependencies beyond Python)
cd cybersec/pramana
python -m pytest -q

# AI/ML pipeline
cd ../../ai-ml
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
```

## 12. Run

```bash
# Cybersec offline demo
cd cybersec/pramana
python run_cyber_demo.py

# AI/ML List-A + List-B tests
cd ai-ml
python -m pytest group_a_deterministic/ group_b_nlp/ group_c_wallet_infra/
python -m pytest group_d_embeddings/ group_e_classification/ group_f_graph/ group_g_llm_assist/ tests/

# PRAMANA Fusion Engine
python -m pramana.range_sim
python -m pramana.demo
uvicorn pramana.api:app --port 8000

# Cloudflare Worker (free tier)
cd cloudflare-workers
npm install
npx wrangler dev
```

## 13. Future Scope

- Complete the backend evidence ledger (PostgreSQL, bitemporal history, retraction propagation) and the
  frontend investigation dashboard, both currently planned.
- Resolve the DC-01–DC-06 evidence-promotion contract so ML/cyber features can be promoted to
  authoritative evidence candidates under sign-off.
- Extend the RANGE-SIM synthetic evaluation corpus and add the RANGE-TOR controlled infrastructure
  testbed for adversarial/false-positive measurement.
- Add F6–F9 evidence-family generators (linguistic, behavioural, social/trust, external corroboration)
  not yet covered by List-A/List-B.
- Move from a single-instance PostgreSQL prototype to the specified migration path (graph/search
  clustering) only once measured scale thresholds are actually reached.

## Important

Before submission, make sure the repository is accessible to reviewers and is **public**. Do **not**
upload passwords, API keys, access tokens, `.env` files containing secrets, or other confidential
credentials.

## Team

**SIH 2026 — Team localhost:3000** (Team ID pending — internal hackathon round)
