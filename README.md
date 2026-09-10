# SIH26151 — PRAMANA

> **Smart India Hackathon 2026 | Problem Statement SIH26151**
> **Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails.**
> *"Attribution fails on the arithmetic of evidence, not the shortage of it."*

---

## 1. Project Information

- **Project Title:** PRAMANA — Darknet Intelligence & Evidence Fusion Platform
- **PS ID:** SIH26151
- **PS Title:** Darknet Intelligence Platform for detecting cross-persona evidence and crypto-money trails
- **Category:** Software
- **Theme:** Smart Automation / Cybersecurity / Law Enforcement
- **Team ID:** Not yet assigned *(Official ID pending allocation; placeholder per competition guidelines)*

---

## 2. Problem Statement

Law enforcement and intelligence analysts face acute attribution challenges across decentralized darknet markets, illicit forums, and cryptocurrency trails:

1. **Adversarial Persona Multiplication:** Illicit operators deliberately partition operations across dozens of pseudonymous vendor identities, PGP keys, and vanity onion domains across multiple hidden services.
2. **The "Arithmetic of Evidence" Trap:** Conventional correlation systems perform naive additive scoring (e.g. summing weights of matching indicators). When an actor posts 50 product listings using the same layout template, naive systems inflate confidence 50-fold, creating catastrophic false-merge rates (~30%).
3. **Shared Infrastructure & Deposit Hubs:** Centralized market deposit addresses and tumblers are shared by thousands of independent vendors. Additive algorithms falsely cluster these into single impossible "super-identities".
4. **Adversarial Decoys:** Sophisticated threat actors plant decoy Bitcoin addresses, PGP keys, or stylistic markers in competitor listings to poison automated clustering pipelines.

---

## 3. Proposed Solution

PRAMANA resolves darknet attribution through a principled, multi-tier intelligence pipeline combining **deterministic forensic extraction**, **dense semantic/graph analysis**, and **independence-aware Bayesian evidence fusion**:

1. **Deterministic Cyber Slice (`cybersec/`):** Standardizes raw darknet archives (Gwern Grams), validates Bitcoin Base58Check/PGP lexical structures, and strictly suppresses shared infrastructure (>12 accounts hub rule) prior to scoring.
2. **Multi-Vector Feature Extraction (`ai-ml/`):**
   - *List-A:* Regex entity extractors, IDF rarity weighting, stylometry, language/NER tagging, co-spend transaction clustering, and temporal overlap detection.
   - *List-B:* Dense text/image embeddings, vertical multi-label threat classification, leetspeak evasion detection, ego-network graph features, and citation-gated LLM hypothesis generation.
3. **PRAMANA Evidence Fusion Engine (`ai-ml/pramana/`):**
   - Replaces naive addition with **Log-Likelihood Ratios**: $L(e) = \log_{10} \frac{P(e \mid \text{Same})}{P(e \mid \text{Diff})}$.
   - Partitions evidence into orthogonal families: `F1_CRYPTO`, `F2_STYLE`, `F3_INFRA`, and `F4_BEHAVIOR`.
   - Applies **geometric discounting** ($\alpha^{n-1}$) to intra-family evidence, penalizing correlated redundant signals.
   - Enforces a hard attribution gate requiring $k \ge 2$ independent corroborating families, neutralizing 100% of single-vector decoys.
4. **Evidence Balance Sheets:** Emits fully auditable, human-contestable ledgers detailing supporting signals, contradictions, discount penalties, and residual risk.

---

## 4. Key Features

| Subsystem | Feature | Capability & Implementation | Operational Benefit |
|---|---|---|---|
| **Cyber Intelligence** | Immutable Ingestion | Pinned archive reader with SHA-256 validation (`adapters/gwern_grams`) | Tamper-proof forensic provenance across darknet datasets |
| **Cyber Intelligence** | Hub Suppression Policy | Deterministic detection of shared deposit addresses (>12 accounts) | Eliminates massive false-merge clusters from market infrastructure |
| **Cyber Intelligence** | Offline Review Packet | Zero-dependency JSON packet + standalone HTML viewer (`review.html`) | Enables secure, air-gapped forensic inspection in high-security environments |
| **AI/ML (List-A)** | Deterministic Extraction | Regex extraction for BTC addresses, PGP fingerprints, onion links, emails | Instant, sub-millisecond indicator extraction with IDF rarity scoring |
| **AI/ML (List-A)** | Stylometric Profiling | Sentence length distributions, punctuation profiles, function words | Detects writing-style matches and multi-operator team shifts |
| **AI/ML (List-A)** | Crypto & Infra Clustering | Co-spend transaction heuristics and temporal activity overlap bands | Maps shared financial control and overlapping active operating hours |
| **AI/ML (List-B)** | Semantic Embeddings | Dense text embeddings + perceptual image similarity (`group_d_embeddings`) | Detects paraphrased listings and cross-market reused product imagery |
| **AI/ML (List-B)** | Threat Vertical Tagger | Multi-label classification (narcotics, fraud, cyber, weapons, credentials) | Automatic classification and risk tiering of illicit vendor operations |
| **AI/ML (List-B)** | Evasion Detection | Leetspeak normalizer and obfuscated keyword detector (`group_e_classification`) | Neutralizes adversarial spelling substitutions designed to bypass filters |
| **AI/ML (List-B)** | Graph Ego-Networks | Shortest path proximity and entity co-occurrence frequency (`group_f_graph`) | Discovers topological clustering without premature identity assertions |
| **AI/ML (List-B)** | Grounded LLM Assist | Strict observation-ID citation validation (`group_g_llm_assist`) | Generates non-authoritative investigation leads with zero hallucination |
| **Fusion Engine** | Independence Fusion | Bayesian log-likelihood ratio engine with intra-family geometric discounting | Reduces false-merge rate from 29.8% down to 1.5% |
| **Fusion Engine** | Decoy Immunity | Hard gate requiring $k \ge 2$ independent feature families for match approval | Refuses 100% of planted adversary decoys (20/20 on RANGE-SIM) |
| **Fusion Engine** | Evidence Balance Sheet | Complete audit trace showing positive weights, counter-evidence, discounts | Full legal contestability and explainable AI for court proceedings |
| **Deployment** | Edge Micro-Services | Cloudflare Workers REST API (7 routes, serverless global edge) | Low-latency, scalable indicator processing with zero cold-start overhead |

---

## 5. Technology Stack

PRAMANA employs a robust, hybrid architecture engineered for both ultra-low latency edge feature extraction and mathematically rigorous, air-gapped forensic evidence fusion.

### Overall Technology Matrix

| Layer / Subsystem | Technology & Frameworks | Version / Spec | Architecture Role & Operational Purpose |
|---|---|---|---|
| **Frontend & UI (Planned)** | React 18, TypeScript, Vite, TailwindCSS | React 18, TS 5.x | Interactive analyst workbench: persona ego-network exploration, temporal overlap alignment, and evidence balance sheet inspection. |
| **Graph & Visual Analytics** | Cytoscape.js, D3.js, Chart.js | Modern ESM | Interactive topological graph rendering, co-spend transaction cluster visualization, and diurnal activity density charts. |
| **API & Service Gateway** | FastAPI, Pydantic v2, Starlette, Uvicorn | FastAPI >= 0.110.0, Python 3.11/3.13 | Asynchronous, high-throughput REST API serving `/assess`, `/precompute`, and `/balance_sheet` endpoints with OpenAPI auto-docs. |
| **Edge Serverless Compute** | Cloudflare Workers, TypeScript, Wrangler CLI | Node.js 20+, Wrangler 3.x | Sub-10ms global edge execution across 7 REST routes for deterministic regex extraction, IDF rarity scoring, and template hashing. |
| **Cyber Intelligence Slice** | Python Standard Library (`tarfile`, `hashlib`, `re`) | Python 3.13.7 / 3.11.9 | 100% standard library offline forensic ingestion (`gwern_grams`), SHA-256 digest validation, Base58Check decoding, and air-gapped HTML review generation. |
| **NLP & Stylometry** | spaCy (`en_core_web_sm`), Langdetect | spaCy >= 3.7.0 | Natural language identification, Named Entity Recognition, stylometric sentence/punctuation profiling, and author style-shift tracking. |
| **Perceptual Image Analytics** | Pillow, ImageHash | Pillow >= 10.0.0, ImageHash >= 4.3 | Image normalization, perceptual pHash computation, and visual re-use fingerprinting across darknet market listings. |
| **Dense Embeddings & ML** | Hugging Face Transformers, Sentence-Transformers | PyTorch / ONNX | High-dimensional semantic sentence embeddings (paraphrase-robust) and multi-label illicit vertical classification (drugs, cyber, fraud). |
| **Cryptographic Forensics** | PGPy, Cryptography | PGPy >= 0.6.0 | PGP public key packet parsing, key ID extraction, lexical validation, and cryptographic signature verification. |
| **Evidence Fusion Engine** | PRAMANA Bayesian Likelihood Engine | Custom Python 3.11+ | Independence-aware log-likelihood ratio fusion, geometric intra-family discounting (`F1`–`F4`), and decoy immunity enforcement. |
| **Data & Persistence (Planned)** | PostgreSQL 16, SQLAlchemy 2.0, Alembic | PostgreSQL 16 | Relational evidence ledger, JSONB audit traces, hash-chained retraction logs, and Z1–Z4 security zone access boundaries. |
| **Container & Hosting** | Docker, Hugging Face Spaces | Debian Bookworm / Docker | Containerized serving of GPU/CPU-intensive ML embedding models and classification spaces. |
| **Testing & Verification** | PyTest, Coverage | PyTest >= 8.0.0 | Dual offline test suites: Cybersec (76 passing tests, 13 skipped) and AI/ML (27 unit/integration tests). |

---

## 6. Architecture

Detailed system architecture specifications, subsystem interface contracts, and formal mathematical bounds are documented in [docs/architecture.md](docs/architecture.md).

### Overall System Interaction & Component Architecture

```text
+---------------------------------------------------------------------------------------------------+
|                                      ANALYST / CLIENT TIER                                        |
|   - React 18 / TypeScript Investigation Dashboard (Interactive Ego-Networks, Timelines, Ledgers)   |
|   - Air-gapped Offline Static HTML Review Viewer (docs/cyber/demo/review.html)                    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                         +------------------------+------------------------+
                         | (REST API / HTTPS)                              | (Local / Offline)
                         v                                                 v
+--------------------------------------------------+    +-------------------------------------------+
|            API & EDGE ROUTING TIER               |    |      AIR-GAPPED FORENSIC SLICE            |
|  - Cloudflare Edge Workers (*.workers.dev)       |    |      (cybersec/pramana/)                  |
|    [/extract, /rarity, /wallet, /temporal,       |    |  - Gwern Grams Archive Reader (SHA-256)   |
|     /infra, /template, /assess]                  |    |  - Deterministic Normalizer & Hasher      |
|  - FastAPI Microservice (uvicorn on port 8000)   |    |  - Hub Policy Suppression (>12 accounts)  |
|    [/assess, /precompute, /balance_sheet, /health|    |  - Standalone JSON & HTML Review Packet   |
+--------------------------------------------------+    +-------------------------------------------+
                         |                                                 |
                         +------------------------+------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  AI/ML FEATURE EXTRACTION PIPELINE                                |
|                                                                                                   |
|   [List-A: Deterministic Forensic Extractors]                                                      |
|   ├── Group A: Regex Indicator Extraction (BTC, PGP, Onion, Email) + Corpus IDF Rarity            |
|   ├── Group B: Stylometric Feature Extraction + NER + Language Tagging + SHA-256 Template Hashing |
|   └── Group C: Bitcoin Co-spend Clustering + Millisecond Temporal Activity Overlap Windows        |
|                                                                                                   |
|   [List-B: Dense Machine Learning & Graph Analytics]                                              |
|   ├── Group D: Dense Sentence Embeddings + Perceptual Image Fingerprints + ANN Vector Index       |
|   ├── Group E: Multi-label Illicit Threat Classification + Leetspeak Evasion Normalization        |
|   ├── Group F: Ego-network Subgraph Extraction + Entity Co-occurrence Proximity (F8 Features)     |
|   └── Group G: Citation-Gated Investigation Hypothesis Generator (Non-authoritative Leads)        |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                            PRAMANA EVIDENCE FUSION ENGINE (ai-ml/pramana)                         |
|                                                                                                   |
|   Mathematical Formulation: Log-Likelihood Ratio: L(e) = log10( P(e|Same) / P(e|Diff) )           |
|                                                                                                   |
|   Orthogonal Feature Families:                                                                    |
|   ├── Family 1 (F1_CRYPTO):   Cryptographic Keys, On-Chain Co-spend Transaction Clusters          |
|   ├── Family 2 (F2_STYLE):    Writing Stylometry, Vocabulary Complexity, Author Shift Markers     |
|   ├── Family 3 (F3_INFRA):    Hosting Infrastructure, TLS Certificates, Favicon Hashes            |
|   └── Family 4 (F4_BEHAVIOR): Temporal Operating Hours, Trade Volumes, Graph Ego Proximity        |
|                                                                                                   |
|   Intra-Family Geometric Discounting:  Weight_n = alpha^(n - 1)  (Penalizes correlated redundancy)|
|   Hard Decoy Immunity Gate:            Requires k >= 2 independent families (Refuses 100% decoys) |
|   Explainable Output:                  Human-Contestable Evidence Balance Sheets with Full Traces |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                  ENTERPRISE PERSISTENCE LAYER                                     |
|   - PostgreSQL 16 Relational & JSONB Evidence Ledger                                              |
|   - Immutable Hash-Chained Audit Trail & Retraction History Logs                                  |
|   - Z1–Z4 Security Boundary Access Controls (Law Enforcement Multi-Agency Compartmentalization)   |
+---------------------------------------------------------------------------------------------------+
```

---

## 7. Repository Structure

```text
SIH26151/
├── README.md                  # Comprehensive documentation across sections 1-13
├── SUBMISSION_GUIDE.md        # Pre-submission verification checklist
├── FOLDER_STRUCTURE.md        # Fully-expanded repository directory tree
├── requirements.txt           # Unified top-level Python dependencies
├── .gitignore                 # Secrets, cache, and artifact exclusions
├── LICENSE                    # MIT open-source license
├── submission/
│   ├── PRESENTATION.md        # Final SIH presentation deck (PPT/PPTX link)
│   └── DEMO.md                # Demonstration video link
├── docs/
│   └── architecture.md        # Detailed system architecture and data contracts
├── assets/
│   └── screenshots/
│       └── README.md          # Screenshot inventory, examples, and conventions
├── ai-ml/                     # Feature extraction engines, ML models, and Fusion Engine
├── cybersec/                  # PRAMANA offline cyber review slice, adapters, and policies
├── backend/                   # Planned FastAPI REST service and PostgreSQL ledger
└── frontend/                  # Planned React/TypeScript investigation dashboard
```

### What Goes Where?

| Item / Deliverable | Location | Description |
|---|---|---|
| **AI/ML Feature Extraction** | `ai-ml/group_a_*` to `group_g_*` | Deterministic extractors, stylometry, embeddings, classifiers, and graph features |
| **Evidence Fusion Engine** | `ai-ml/pramana/` | Bayesian log-likelihood ratio fusion, RANGE-SIM simulation, and FastAPI service |
| **Cloudflare Edge Workers** | `ai-ml/cloudflare-workers/` | Serverless TypeScript edge workers for low-latency indicator extraction |
| **Offline Cyber Review Slice** | `cybersec/pramana/` | Air-gapped archive ingestion, canonicalization, indicators, and static HTML review |
| **System Architecture** | `docs/architecture.md` | In-depth architectural design, data flows, and subsystem boundary definitions |
| **Screenshots & Visuals** | `assets/screenshots/` | Prototype captures, balance sheet screenshots, and workflow diagrams |
| **Presentation Deck** | `submission/PRESENTATION.md` | Final competition presentation deck / accessible viewer link |
| **Demo Video Link** | `submission/DEMO.md` | Video demonstration walkthrough link |
| **Directory Structure Map** | `FOLDER_STRUCTURE.md` | Fully-expanded tree and cybersec module grouping breakdown |
| **Submission Checklist** | `SUBMISSION_GUIDE.md` | Compliance checklist before sharing the repository |

---

### Comprehensive Tabular Breakdown of Modules & Sub-modules

#### Table 7.1: `ai-ml/` List-A Sub-modules (Deterministic Extraction Engine)

| Sub-module | Directory | Key Files | Operational Purpose |
|---|---|---|---|
| **Group A: Deterministic** | `ai-ml/group_a_deterministic/` | `extractors.py`, `canonicalise.py`, `pgp_meta.py`, `rarity.py`, `test_group_a.py` | Regex extraction of Bitcoin addresses, PGP blocks, onion URLs, email addresses; IDF term rarity calculation. |
| **Group B: NLP & Style** | `ai-ml/group_b_nlp/` | `stylometry.py`, `style_shift.py`, `lang_ner.py`, `template_fp.py`, `test_group_b.py` | Writing-style fingerprinting, stylometric shift detection for team-operated accounts, multi-language detection, NER, listing template hashing. |
| **Group C: Wallet & Infra** | `ai-ml/group_c_wallet_infra/` | `wallet_cluster.py`, `temporal.py`, `infra_fp.py`, `test_group_c.py` | Co-spend Bitcoin transaction clustering, millisecond temporal activity overlap detection, TLS/favicon infrastructure fingerprinting. |
| **Shared Contracts** | `ai-ml/shared/` | `contracts.py`, `data_loader.py` | Frozen `EvidenceCandidate` dataclass contract and unified sample data loaders. |
| **Cloudflare Workers** | `ai-ml/cloudflare-workers/` | `src/index.ts`, `wrangler.jsonc`, `package.json`, `deploy.ps1` | Global serverless edge microservices exposing 7 REST routes on Cloudflare's free tier with zero paid bindings. |
| **Model Space Runtime** | `ai-ml/hf-space/` | `app.py`, `Dockerfile`, `requirements.txt` | Containerized FastAPI runtime for hosting heavier NLP and transformer models. |
| **Offline Test Data** | `ai-ml/data/` | `bitcoinheist_sample.csv`, `darknet_archives_sample/`, `stylometry_sample/` | Bounded local test fixtures for deterministic extractor verification. |

#### Table 7.2: `ai-ml/` List-B Sub-modules (NLP/ML Models & PRAMANA Fusion Engine)

| Sub-module | Directory | Key Files | Operational Purpose |
|---|---|---|---|
| **Group D: Dense Embeddings** | `ai-ml/group_d_embeddings/` | `text_embeddings.py`, `image_embeddings.py`, `similarity_index.py`, `test_group_d.py` | Paraphrase-robust sentence embeddings across forum listings, perceptual image embeddings, and ANN candidate retrieval index. |
| **Group E: Threat Classification** | `ai-ml/group_e_classification/` | `category_tagger.py`, `risk_classifier.py`, `evasion_detector.py`, `test_group_e.py` | Multi-label classification across illicit verticals (drugs, fraud, cyber, weapons, credentials), threat tiering, and leetspeak evasion detection. |
| **Group F: Graph Analysis** | `ai-ml/group_f_graph/` | `co_occurrence.py`, `subgraph_extractor.py`, `path_features.py`, `test_group_f.py` | Graph topological features: entity co-occurrence frequency, ego-network extraction, and shortest path proximity (features only, no premature merges). |
| **Group G: LLM Investigation** | `ai-ml/group_g_llm_assist/` | `prompt_builder.py`, `citation_validator.py`, `hypothesis_generator.py`, `test_group_g.py` | Grounded investigation prompts, strict observation-ID citation validation, non-authoritative linking hypotheses with zero hallucinations. |
| **Evidence Fusion Engine** | `ai-ml/pramana/` | `score_pramana.py`, `score_naive.py`, `range_sim.py`, `sensitivity.py`, `schema.py`, `api.py`, `demo.py`, `evaluate.py` | Core Bayesian likelihood fusion engine with geometric discounting across feature families, decoy immunity verification, and FastAPI service. |
| **Integration Test Suite** | `ai-ml/tests/` | `test_fusion.py` | Integration tests verifying cross-persona candidate evaluation and balance sheet generation. |

#### Table 7.3: `cybersec/` Sub-modules (Grouped by Functional Subsystem)

| Functional Group | Directory | Key Files | Operational Scope |
|---|---|---|---|
| **CS-01: Ingestion & Adapters** | `cybersec/pramana/adapters/gwern_grams/` | `archive_reader.py`, `csv_parser.py`, `normalizer.py`, `identifiers.py`, `models.py`, `runner.py`, `errors.py` | Pinned tarball reader (`grams.tar.xz`), SHA-256 digest validation, exact raw-field preservation, unknown-timestamp handling, and provenance tracking. |
| **CS-02: Canonicalization** | `cybersec/pramana/canonicalization/` | `runner.py`, `models.py`, `text_hashing.py`, `tests/test_canonicalization.py` | Deterministic text normalization and cryptographic hashing to distinguish exact copy-paste marketplace mirrors from independent content. |
| **CS-03: Cyber Indicators & Policy** | `cybersec/pramana/cyber/` | `indicators.py`, `policy.py`, `review.py`, `render.py`, `demo.py` | Base58Check legacy Bitcoin validation, PGP marker extraction, `hub_restriction` (>12 accounts suppression), `clone_restriction`, and review generation. |
| **CS-04: Test Suite & Drivers** | `cybersec/pramana/tests/` + Runners | `test_cyber_slice.py`, `test_adapter_regressions.py`, `test_fixtures.py`, `run_cyber_demo.py`, `run_cyber_validation.py`, `run_canonicalization.py` | Zero-dependency offline test suite (76 passed, 13 skipped); executes without active database, network, Tor, or GPU. |
| **CS-05: Documentation & Evidence** | `cybersec/pramana/docs/` + Dossiers | `docs/cyber/` (`demo/review.html`, `validation/pytest.xml`), `PRAMANA_Master_Blueprint.md`, `PRAMANA_Technical_Project_Dossier.pdf` | Frozen policy contracts (`PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md`), technical blueprints, reproduction manuals, and validation logs. |
| **CS-06: Verification & QA Assets** | `cybersec/pramana/hatch-runs/` | `starjotaro-v2/` (`decoded/`, `final/`, `qa/`, `source/`) | Prototype verification assets, assembly manifests, contact sheets, and anchor alignments for UI and report rendering. |

#### Table 7.4: `backend/` and `frontend/` Sub-modules (Planned Platform Services)

| Module | Directory | Planned Components | Architecture Role |
|---|---|---|---|
| **Backend Service** | `backend/` | `README.md`, `requirements.txt`, FastAPI Server, PostgreSQL 16 Ledger, Auth Layer | Persistent evidence store, Z1–Z4 trust zone enforcement, analyst note persistence, and retraction logging (pending DC-06 contract). |
| **Investigation Frontend** | `frontend/` | `README.md`, `.gitkeep`, React 18, TypeScript, Vite Dashboard | Analyst workbench: visual persona graph exploration, co-spend wallet visualizer, temporal timeline alignment, and PDF export. |

#### Table 7.5: Reference Submission & Governance Scaffolding

| Deliverable | File / Directory | Mandatory Section / Content | Compliance Status |
|---|---|---|---|
| **Submission Guide** | `SUBMISSION_GUIDE.md` | Verification checklist and requirements audit | Implemented & Verified |
| **Presentation Deck** | `submission/PRESENTATION.md` | PPT/PPTX file link or accessible cloud viewer URL | Scaffolded |
| **Demonstration Video** | `submission/DEMO.md` | YouTube / Google Drive public video link | Scaffolded |
| **System Architecture** | `docs/architecture.md` | Detailed architectural specifications and diagrams | Implemented & Verified |
| **Prototype Screenshots** | `assets/screenshots/README.md` | Screenshot catalog and naming conventions | Implemented & Verified |
| **Open Source License** | `LICENSE` | MIT License | Implemented |
| **Root Dependencies** | `requirements.txt` | Pinned core dependencies across components | Implemented |

---

### Cloudflare Worker Routes (Deployed at `workers.dev`)

| HTTP Method | Route | Input Payload | Output Response |
|---|---|---|---|
| `POST` | `/extract` | `{"text": string}` | Extracted Bitcoin addresses, PGP markers, onion links, emails |
| `POST` | `/rarity` | `{"terms": string[], "corpus_counts": object}` | IDF-weighted rarity scores per indicator |
| `POST` | `/wallet` | `{"addresses": string[], "risk_labels": object}` | Co-spend wallet clusters and associated threat flags |
| `POST` | `/temporal` | `{"events": object[]}` | Temporal overlap bands computed with millisecond arithmetic |
| `POST` | `/infra` | `{"hosts": string[]}` | TLS certificate and favicon hash fingerprint groups |
| `POST` | `/template` | `{"text": string}` | Cryptographic SHA-256 listing template fingerprint |
| `POST` | `/assess` | `{"account_a": object, "account_b": object}` | Lightweight edge independence assessment and score |

---

### PRAMANA Evidence Fusion API Endpoints (`pramana.api`)

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Service status, pinned parameter version (`v0.1`), asserted Bayesian priors |
| `POST` | `/assess` | Score persona pair given `{account_a, account_b, include_naive?}` |
| `POST` | `/precompute` | Evaluates all candidate pairs at startup into an in-memory cache |
| `GET` | `/balance_sheet/{a}/{b}` | Outputs complete Evidence Balance Sheet with family breakdowns and discount traces |

---

### Measured Benchmark Performance on RANGE-SIM v0.1

| Evaluation Metric | Naive Additive System | No Grouping Baseline | PRAMANA Fusion Engine (Shipped) |
|---|---|---|---|
| **False-Merge Rate** | 29.8% | 3.5% | **1.5%** |
| **False Merges (Count)** | 239 | 28 | **12** *(10 are planted account handovers)* |
| **Precision** | 28.2% | 75.2% | **87.6%** |
| **Recall** | 94.9% | 85.9% | **85.9%** |
| **F1 Score** | 0.435 | 0.802 | **0.867** |
| **Adversarial Decoys Refused** | 0 / 20 (0%) | 20 / 20 (100%) | **20 / 20 (100% Refused)** |
| **Low-Corroboration Refused ($k < 2$)** | 0 | — | **803 candidate pairs** |

*Corpus: 900 candidate pairs across 60 synthetic operators (99 positive, 801 negative, 20 planted decoys, 10 planted handovers).*

---

### Pipeline Interface Contract (Data Boundaries)

```text
RAW OBSERVATION  ──>  DETERMINISTIC DERIVATION  ──>  ML FEATURE  ──>  EVIDENCE CANDIDATE
   (cybersec)             (cybersec/canon)            (ai-ml)              [DEFERRED]
                                                                      requires DC-01–DC-06
```

| Pipeline Stage | Module Owner | Strict Constraint |
|---|---|---|
| **Raw Observation** | `cybersec` | Must not infer actor, persona, or identity from raw strings. |
| **Deterministic Derivation** | `cybersec/canon` | Must not make origin/k decisions or emit final pair scores. |
| **ML Feature** | `ai-ml` | Must not write directly to `evidence`, `assessment`, or `must_not_link`. |
| **Evidence Candidate** | Cross-Team Signoff | Promotion strictly deferred until field-level contract validation (DC-06). |

---

## 8. Final Presentation

The official SIH 2026 final presentation deck is maintained in the `submission/` directory.

- **Presentation Link:** See [submission/PRESENTATION.md](submission/PRESENTATION.md) for the presentation file and cloud viewer link.

---

## 9. Demo Video

The demonstration video showcases PRAMANA's end-to-end evidence ingestion, offline cyber suppression, independence-aware fusion scoring, and balance sheet generation.

- **Demo Video Link:** See [submission/DEMO.md](submission/DEMO.md) for the accessible video link.

---

## 10. Screenshots / Prototype Photos

Visual artifacts, dashboard wireframes, and balance sheet inspect windows are cataloged in `assets/screenshots/`.

- **Screenshot Directory:** [assets/screenshots/](assets/screenshots/)
- **Catalog:** See [assets/screenshots/README.md](assets/screenshots/README.md) for details on naming conventions and screenshots inventory.

| Preview Item | Location | Description |
|---|---|---|
| Architecture Diagram | `assets/screenshots/01-architecture-overview.png` | End-to-end multi-tier pipeline schematic |
| Evidence Balance Sheet | `assets/screenshots/02-evidence-balance-sheet.png` | Itemized audit trace showing family discounts |
| Offline Cyber Review Viewer | `assets/screenshots/03-offline-cyber-review.png` | Standalone static HTML viewer (`docs/cyber/demo/review.html`) |

---

## 11. Installation

### Environment Requirements
- **Python:** 3.11 or 3.13
- **Node.js (Optional, for Workers):** Node.js 20+ and npm

### 1. Cybersec Slice (Zero-Dependency Offline Setup)
```powershell
cd cybersec/pramana
python --version    # Requires Python 3.11 or 3.13
python -m pytest -q # Standard library only — runs immediately
```

### 2. AI/ML Pipeline & Fusion Engine Setup
```powershell
cd ai-ml
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Cloudflare Workers Edge Setup (Optional)
```powershell
cd ai-ml/cloudflare-workers
npm install
```

---

## 12. Run

### Execute Test Suites
```powershell
# 1. Run offline cybersec tests (76 passing, 13 skipped)
cd cybersec/pramana
python -m pytest -q

# 2. Run deterministic cyber demo (outputs 18 records, 53 indicators, hub suppression)
python run_cyber_demo.py
# Open docs/cyber/demo/review.html in any browser

# 3. Run AI/ML List-A tests (Deterministic, NLP, Wallet/Infra)
cd ../../ai-ml
python -m pytest group_a_deterministic/test_group_a.py
python -m pytest group_b_nlp/test_group_b.py
python -m pytest group_c_wallet_infra/test_group_c.py

# 4. Run AI/ML List-B tests (Embeddings, Classification, Graph, LLM, Fusion)
python -m pytest group_d_embeddings/ group_e_classification/ group_f_graph/ group_g_llm_assist/ tests/
```

### Run PRAMANA Fusion Engine & API
```powershell
cd ai-ml

# Generate synthetic RANGE-SIM corpus
python -m pramana.range_sim

# Run full ablation and balance sheet demo
python -m pramana.demo

# Launch local FastAPI service (Swagger UI at http://localhost:8000/docs)
uvicorn pramana.api:app --reload --port 8000
```

### Run Cloudflare Worker Locally
```powershell
cd ai-ml/cloudflare-workers
npx wrangler dev
```

---

## 13. Future Scope

1. **Persistent Evidence Ledger:** Implement PostgreSQL 16 storage with immutable hash-chained audit trails and explicit retraction logs for analyst contestability.
2. **Interactive Analyst Workbench:** Deploy a React 18 / TypeScript frontend featuring interactive graph ego-network visualization and co-spend transaction clustering.
3. **Live Tor Hidden Service Crawling:** Add an asynchronous, rate-limited Onionscan / Tor crawler daemon feeding directly into the deterministic canonicalization pipeline.
4. **RANGE-TOR Evaluation:** Scale the benchmark evaluation from the synthetic RANGE-SIM corpus to historical, unsealed darknet market law enforcement takedown datasets.

---

## Important

> [!CAUTION]
> **Credential & Secrets Protection:**
> Never commit `.env` files, API keys, private PGP keys, database passwords, or auth tokens to this repository. All environment variables must use `.env.example` placeholders. The repository must remain public and accessible to reviewers at all times without authentication barriers.

---

## Team

**SIH 2026 — Team localhost:3000**

- **Team ID:** Not yet assigned *(Official ID pending allocation; placeholder per competition guidelines)*
- **Project Lead & Architecture:** Team SIH26151
- **Cyber Intelligence & Forensic Slice:** Team SIH26151 Cybersec Unit
- **AI/ML Feature Extraction & Fusion Engine:** Team SIH26151 AI/ML Unit