# System Architecture — PRAMANA (SIH26151)

PRAMANA is an evidence-backed darknet intelligence platform designed to attribute pseudonymous personas across dark web markets, forums, and cryptocurrency trails without falling victim to naive co-occurrence traps, shared infrastructure hubs, or adversary decoys.

---

## High-Level Architecture Flow

```text
+-----------------------------------------------------------------------------------+
|                            RAW ADVERSARIAL SOURCES                               |
|        Darknet Market Listings, Forum Posts, PGP Keys, On-Chain BTC Clusters      |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                 CYBER INTELLIGENCE & CANONICALIZATION SLICE                       |
|  - Archive Reader & Normalizer (pramana/adapters/gwern_grams)                     |
|  - Text Hashing & Exact Repetition (pramana/canonicalization)                     |
|  - Hub & Clone Restrictions: >12 accounts rule (pramana/cyber/policy.py)          |
|  - Offline Human Review Packet & Viewer (pramana/cyber/render.py)                 |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        AI/ML FEATURE EXTRACTION PIPELINE                          |
|                                                                                   |
|  [List-A: Deterministic Pipeline]                                                 |
|    - Group A: BTC / PGP / Onion / Email Regex & IDF Rarity Scoring               |
|    - Group B: Stylometry, Writing-Style Shift, Lang Detection, NER, Template FP   |
|    - Group C: Co-spend Wallet Clustering, Temporal Overlap, Infra Fingerprinting  |
|                                                                                   |
|  [List-B: Machine Learning & Semantic Embeddings]                                 |
|    - Group D: Text & Perceptual Image Embeddings, Approximate Nearest Neighbor    |
|    - Group E: Multi-label Threat Classification & Leetspeak Evasion Detection     |
|    - Group F: Entity Co-occurrence, Subgraph Ego-network, Path Proximity          |
|    - Group G: Citation-Validated LLM Hypothesis Generator                        |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                  PRAMANA EVIDENCE FUSION ENGINE (ai-ml/pramana)                   |
|                                                                                   |
|  - Log-Likelihood Ratio Formulation: L(e) = log10( P(e|Same) / P(e|Diff) )        |
|  - Independence-Aware Family Discounting:                                         |
|      F1 (PGP/Crypto) | F2 (NLP/Style) | F3 (Infra/Network) | F4 (Temporal/Graph) |
|  - Decoy Immunity & Hard Gate: k >= 2 independent corroborating families required |
|  - Evidence Balance Sheet Generation (Full discount and audit traces)            |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           REST APIS & PERSISTENCE LAYER                           |
|                                                                                   |
|  - FastAPI Engine: /assess, /precompute, /balance_sheet, /health                  |
|  - Cloudflare Workers: Edge REST routes (/extract, /rarity, /wallet, /infra)      |
|  - Backend Service: PostgreSQL 16 Evidence Ledger & Retraction Log (Planned)      |
|  - Frontend: React/TypeScript Interactive Investigation Dashboard (Planned)       |
+-----------------------------------------------------------------------------------+
```

---

## System Subsystems

### 1. Cybersec Offline Review Slice (`cybersec/pramana/`)
- **Adapters (`adapters/gwern_grams/`):** Reads immutable archive snapshots (e.g. `grams.tar.xz`), enforces cryptographic SHA-256 digest validation, and standardizes disparate schema entries into unified provenance-linked records.
- **Canonicalization (`canonicalization/`):** Performs text normalization and hashing to establish identical repetition versus independent occurrence.
- **Deterministic Indicators & Policy (`cyber/`):** Evaluates PGP fingerprints, legacy Base58Check Bitcoin formats, and applies hard policy restrictions (e.g. suppression of shared custodial deposit addresses with >12 accounts).
- **Offline Review Viewer:** Exports static JSON review packets and standalone HTML inspectors (`docs/cyber/demo/review.html`) requiring no active server, database, or external network connectivity.

### 2. AI/ML Feature Extraction Engine (`ai-ml/`)
- **Group A (Deterministic Extractors):** Extracts structured forensic indicators from unstructured text and scores rarity using Inverse Document Frequency (IDF).
- **Group B (NLP Stylometry):** Quantifies stylistic traits (sentence length distributions, punctuation profiles, function words) and flags stylistic drift indicative of team-operated accounts.
- **Group C (Crypto & Infrastructure):** Performs heuristic co-spend clustering on Bitcoin transaction inputs and analyzes timestamp overlap distributions.
- **Group D (Dense Embeddings):** Generates high-dimensional vector representations of listings and images to catch paraphrase and visual re-use across platforms.
- **Group E (Risk & Evasion Classification):** Categorizes listings into illicit verticals (narcotics, fraud, counterfeit) and detects leetspeak obfuscation.
- **Group F (Graph Analysis):** Computes graph-derived proximity features and ego-network co-occurrence frequencies without prematurely asserting identity merges.
- **Group G (Grounded LLM Assist):** Synthesizes non-authoritative investigation hypotheses strictly gated by source observation ID citations.

### 3. PRAMANA Evidence Fusion Engine (`ai-ml/pramana/`)
- **Mathematical Principle:** Rather than naively summing similarity scores (which inflates confidence on correlated features like 10 listings using the same vendor template), PRAMANA partitions evidence into orthogonal families:
  - `F1_CRYPTO`: Cryptographic keys, exact wallet clusters.
  - `F2_STYLE`: Writing style, stylometry, vocabulary markers.
  - `F3_INFRA`: Hosting provider, TLS certificates, favicon hashes.
  - `F4_BEHAVIOR`: Temporal active hours, graph co-occurrence, trade volume.
- **Diminishing Marginal Weight:** Successive signals within the same family are discounted geometrically:
  $$\text{Weight}_n = \alpha^{n-1}$$
- **Minimum Independent Corroboration ($k \ge 2$):** Any candidate pair supported by only a single feature family is automatically flagged as insufficient for attribution, eliminating 100% of single-vector decoys and shared deposit false positives.
- **Auditability:** Every decision outputs an Evidence Balance Sheet itemizing positive signals, contradictory evidence, applied family discounts, and residual risk.

### 4. Application & Delivery Surface (`backend/`, `frontend/`, `cloudflare-workers/`)
- **Cloudflare Edge Workers:** Ultra-low latency deterministic extraction deployed globally on serverless workers (`POST /extract`, `POST /rarity`, `POST /wallet`, `POST /temporal`, `POST /infra`, `POST /template`).
- **PRAMANA REST API:** FastAPI server providing real-time evaluation (`/assess`), startup precomputation (`/precompute`), and balance sheet drilldown (`/balance_sheet/{a}/{b}`).
- **Planned Enterprise Layer:** PostgreSQL persistent ledger supporting Z1–Z4 security zone segmentation and an analyst workbench UI.

---

## Overall Technology Stack Matrix

| Architecture Tier | Technology / Library | Version / Runtime | Core Architectural Responsibility |
|---|---|---|---|
| **Analyst UI (Planned)** | React 18, TypeScript, Vite, TailwindCSS | React 18, TS 5.x | Interactive investigation dashboard, persona ego-network viewer, timeline explorer. |
| **Network Visualization** | Cytoscape.js, D3.js, Chart.js | Modern ESM | Graph ego-network visualization, co-spend transaction clustering, temporal activity overlap. |
| **API Gateway** | FastAPI, Pydantic v2, Starlette, Uvicorn | FastAPI >= 0.110.0 | High-performance asynchronous REST endpoints for evaluation and balance sheet export. |
| **Edge Serverless** | Cloudflare Workers, TypeScript, Wrangler CLI | Node.js 20+, Wrangler 3.x | Sub-10ms global edge execution across 7 REST routes for deterministic regex extraction. |
| **Forensic Cyber Slice** | Python Standard Library (`tarfile`, `hashlib`, `re`) | Python 3.13.7 / 3.11.9 | Air-gapped offline ingestion (`gwern_grams`), SHA-256 validation, Base58Check decoding, HTML review. |
| **NLP & Stylometry** | spaCy (`en_core_web_sm`), Langdetect | spaCy >= 3.7.0 | Author stylometric profiling, Named Entity Recognition, and language detection. |
| **Visual Fingerprinting** | Pillow, ImageHash | Pillow >= 10.0.0, ImageHash >= 4.3 | Perceptual pHash computation and listing image deduplication. |
| **Dense ML & Embeddings** | Hugging Face Transformers, Sentence-Transformers | PyTorch / ONNX | High-dimensional semantic sentence embeddings and multi-label threat vertical tagging. |
| **Crypto Forensics** | PGPy, Cryptography | PGPy >= 0.6.0 | PGP public key packet parsing, key ID extraction, and cryptographic verification. |
| **Evidence Fusion Engine** | PRAMANA Bayesian Likelihood Engine | Custom Python 3.11+ | Independence-aware log-likelihood ratio fusion, geometric discounting (`F1`–`F4`), decoy immunity. |
| **Persistence (Planned)** | PostgreSQL 16, SQLAlchemy 2.0, Alembic | PostgreSQL 16 | Relational evidence ledger, JSONB audit traces, hash-chained retraction logs, Z1–Z4 security zones. |
| **Containerization** | Docker, Hugging Face Spaces | Debian Bookworm / Docker | Containerized hosting of heavy ML models on Hugging Face Spaces. |
| **Verification & QA** | PyTest, Coverage | PyTest >= 8.0.0 | Dual offline test suites: Cybersec (76 tests) and AI/ML (27 tests). |

