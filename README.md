# PRAMANA

An evidence-centric identity attribution engine that mathematically bounds probabilistic features using deterministic cryptographic ledgers and strict statistical independence limits.

## 1. What problem PRAMANA solves
In cybersecurity and intelligence, attribution is often handled by black-box AI models that ingest vast amounts of fragmented data and output an opaque "confidence score." In legal, forensic, or high-stakes intelligence environments, this is a liability. An LLM hallucinating a connection, or an embedding model double-counting the same underlying cryptographic key as a "linguistic match," can lead to false attribution. PRAMANA solves the problem of "AI-driven false merges" by separating evidence extraction from mathematical fusion, forcing all features to prove statistical independence before contributing to a hypothesis.

## 2. Core thesis
**"Attribution fails on the arithmetic of evidence, not on the shortage of it."**

PRAMANA operates on the principle that:
*   **Weight of evidence:** Evidence must be quantified via Log-Likelihood Ratios ($log_{10} LR$), not opaque neural network activations.
*   **Independence:** If the same actor posts the same PGP key 50 times, it is ONE piece of evidence, not 50. 
*   **Rarity:** A shared common word is weak; a shared unique Bitcoin wallet is strong. Scores must be mathematically scaled by the population prevalence ($\tau$).
*   **Exclusion:** If independent origins ($k$) are less than 2, attribution must be actively refused.
*   **Human Review:** The system generates a Balance Sheet; a human makes the final decision.

## 3. What PRAMANA IS and IS NOT

**IS:**
*   A pseudonymous evidence analysis engine.
*   An evidence fusion system enforcing independence.
*   A producer of calibrated/contestable attribution leads (where fully implemented).

**IS NOT:**
*   NOT guaranteed real-world identity attribution (it links personas, not physical humans).
*   NOT an autonomous deanonymization agent.
*   NOT an exploitation or offensive cyber tool.
*   NOT an unauthorized Tor/network collection system (operates on provided datasets).
*   NOT a cryptocurrency tracing engine beyond supported extraction scopes.

## 4. The system in one picture

```text
[DARK WEB / NETWORK DATA]
           ↓
[INGESTION / VALIDATION] ----> (cybersec/pramana/run_cyber_validation.py)
           ↓
[NORMALIZATION]
           ↓
[DETERMINISTIC INDICATORS] --> [LIST-A: PGP, Wallets]
           ↓
[REDACTION BOUNDARY] --------> (Strips List-A from text to prevent leakage)
           ↓
[ML / FEATURE LAYER] --------> [LIST-B: Stylometry, Embeddings]
           ↓
[EVIDENCE CONSTRUCTION]
           ↓
[INDEPENDENCE + RARITY] -----> (Enforces k >= 2, scales by tau)
           ↓
[COUNTER-EVIDENCE]
           ↓
[FUSION / SCORING] ----------> (Log-LR Arithmetic, Caps, Damping)
           ↓
[CALIBRATION / EVALUATION] --> (Tippett Plots, ECE Validation)
           ↓
[HUMAN REVIEW]
           ↓
[EXPLAINABLE ASSESSMENT] ----> (The Evidence Balance Sheet)
```

**Explanation:** Raw data enters the Ingestion layer and is mapped to deterministic List-A indicators. A crucial Redaction Boundary scrubs these identifiers from the raw text before passing them to List-B ML models to prevent double-counting. Features are converted to Evidence Candidates and scored. The Fusion engine applies Rarity ($\tau$) and Independence ($k$) limits. Calibrated scores are compiled into an Evidence Balance Sheet for Human Review.

## 5. Layer-by-layer explanation

### 1. Data Ingestion & 2. Source Adapters
*   **PURPOSE:** Safely load raw datasets (e.g., Grams).
*   **IMPLEMENTED:** Canonicalization and extraction of tar archives (`run_cyber_validation.py`). Safely stubs missing archives in demo environments.
*   **SECURITY BOUNDARY:** Archive extraction path traversal (currently uses native `tarfile`, requires hardened filters for production).

### 3. Normalization & 4. Indicator Extraction
*   **PURPOSE:** Map raw text to standardized indicators.
*   **IMPLEMENTED:** PGP extraction, basic BTC regex. 
*   **DEFERRED:** Advanced graph-based normalization.

### 5. Redaction
*   **PURPOSE:** Prevent List-A identifiers from leaking into List-B features.
*   **IMPLEMENTED:** `ai-ml/shared/redaction.py`. Scrubs `[PGP_REDACTED]`, `[BTC_REDACTED]`.
*   **SECURITY BOUNDARY:** Mathematical isolation of probabilistic from deterministic evidence.

### 6. ML Feature Generation
*   **PURPOSE:** Generate behavioral features.
*   **IMPLEMENTED:** Trigram cosines (`text_embeddings.py`), function words (`stylometry.py`).
*   **DEFERRED:** O(N^2) scaling solutions (LSH).

### 7. Evidence Model & 8. Independence Model
*   **PURPOSE:** Package features and detect clones.
*   **IMPLEMENTED:** `EvidenceCandidate` Pydantic contracts. $k$-counting union-find for independence grouping.

### 9. Rarity/Hub Logic & 10. Counter-Evidence
*   **PURPOSE:** Scale scores by uniqueness; apply exculpatory evidence.
*   **IMPLEMENTED:** $\tau$ rarity scaling implemented in `rarity.py`.

### 11. Resolution & 12. Fusion/scoring
*   **PURPOSE:** The mathematical fusion of Log-LR scores.
*   **IMPLEMENTED:** `score_pramana.py`. Enforces family caps (e.g., max 4.0), damping, and the $k \ge 2$ rule.

### 13. Calibration & 14. Evaluation
*   **PURPOSE:** Prove the mathematical bounds of the system.
*   **IMPLEMENTED:** `evaluate.py` (calculates False Merge Rate). `calibration.py` (ECE and Tippett plots).

### 15. Backend/API & 16. Frontend/UI
*   **PURPOSE:** Enterprise access.
*   **IMPLEMENTED:** `backend/app/main.py` (FastAPI). Simulated Kafka ingestion. Live calibration endpoint.
*   **DEFERRED/STUB:** Real Kafka broker, Frontend UI.

### 17. Human Review & 18. LLM Boundary
*   **PURPOSE:** Keep the LLM air-gapped from authoritative scoring.
*   **IMPLEMENTED:** The API explicitly marks promotion blocks. LLMs are restricted to formatting the Balance Sheet, never scoring it.

## 6. End-to-end example

1.  **RAW INPUT:** Two dark web listings (`account_a` and `account_b`) contain the same PGP key and similar linguistic styles.
2.  **INDICATOR:** `List-A` extracts the PGP key. `Redaction` scrubs the key from the text.
3.  **FEATURE:** `text_embeddings.py` calculates a 0.82 cosine similarity on the remaining text.
4.  **EVIDENCE:** Both output `EvidenceCandidate` objects to the fusion engine.
5.  **INDEPENDENCE:** The engine verifies these come from distinct capture origins ($k=2$).
6.  **SCORING:** PGP match grants a high Log-LR (capped at 4.0). Linguistic match grants a low Log-LR (e.g., 0.5).
7.  **REVIEW OBJECT:** The `BalanceSheetResponse` is returned via the API, explicitly listing the independent supporting vectors.

## 7. Data model
*   **Observation:** A raw piece of collected data (e.g., a forum post).
*   **Indicator:** A deterministic string (e.g., a BTC address).
*   **Feature:** A probabilistic vector (e.g., stylometric output).
*   **Evidence:** A quantified Log-LR hypothesis support vector.
*   **Hypothesis:** The claim that `account_a == account_b`.
*   **Assessment:** The final scored Balance Sheet.
*   **Account/Alias/Persona:** Virtual representations. *Persona* is the highest level of pseudonymous clustering.

## 8. Evidence families
*   **F1 Cryptographic:** PGP keys, raw signatures. Cap: 4.0. Implemented.
*   **F2 Infrastructure:** IPs, Tor V3 addresses. Cap: 3.0. Partially stubbed.
*   **F3 Financial:** BTC wallets. Cap: 3.5. Implemented.
*   **F4 Operational:** Timezones, active hours. Cap: 1.5. Stubbed.
*   **F5 Social/Graph:** Shared contacts. Cap: 2.0. Stubbed.
*   **F6 Linguistic:** Stylometry, n-grams. Cap: 1.0. Implemented (with Redaction).
*   **F7 Semantic:** Topic modeling. Cap: 1.0. Deferred.
*   **F8 Behavioral:** TTPs. Cap: 2.0. Deferred.
*   **F9 LLM Analyst:** AI reasoning. Cap: 0.0 (Strictly barred from promotion). Implemented.

## 9. Scoring/fusion
The system utilizes additive base-10 Log-Likelihood Ratios ($log_{10} LR$). 
*   **Priors:** Currently uses design priors ($\lambda = 0.2$), not empirically fitted parameters.
*   **Caps:** Hard mathematical ceilings per family (e.g., F6 cannot exceed 1.0) prevent any single probabilistic model from overwhelming the deterministic facts.
*   **Independence Damping:** $k < 2$ results in an immediate `REFUSED` state.
*   **Verbal Bands:** Scores are mapped to intelligence community standards (e.g., "Moderate Support", "Strong Support").

## 10. Security and governance
*   **LLM Prompt-Injection:** The LLM does not touch raw text during scoring. It only sees the final structured Balance Sheet. PASS.
*   **Tar/Archive Safety:** Currently relies on native `tarfile` without explicit `data_filter`. Vulnerable to tarbombs in a hostile open-world setting. DEMO ONLY.
*   **API Security:** CORS is currently `allow_origins=["*"]`. DEMO ONLY.
*   **Authentication:** Deferred.

## 11. Dataset and testbed model
*   **Synthetic Hidden-Ground-Truth (RANGE-SIM):** Used by `evaluate.py` to prove math bounds.
*   **Public/Historical Data:** `grams.tar.xz` (12M records) is the target for `run_cyber_validation.py`.
*   *Note:* Real-world datasets are not bundled in this repository to prevent massive file sizes and legal exposure.

## 12. Reproducibility
*Requires Python 3.13.*
```bash
# 1. Environment Setup
python -m venv .venv
source .venv/bin/activate  # (or .venv\Scripts\activate on Windows)
pip install -r backend/requirements.txt
pip install -r requirements-research-lock.txt

# 2. Run AI/ML Unit Tests
python -m pytest ai-ml

# 3. Run Synthetic Evaluation (Proves FMR drops to 1.5%)
python -m pramana.evaluate

# 4. Run Cyber Demo (Generates the Balance Sheet)
python cybersec/pramana/run_cyber_demo.py --output-dir demo_out

# 5. Start the Enterprise API Gateway
uvicorn backend.app.main:app --reload
```

## 13. Current implementation status
| Capability | Status | Evidence |
|---|---|---|
| Ingestion / Canonicalization | Partial (Stubbed if missing) | `run_cyber_validation.py` |
| List-A / List-B Redaction | Implemented | `ai-ml/shared/redaction.py` |
| Scoring & Fusion | Implemented | `ai-ml/pramana/score_pramana.py` |
| Calibration (ECE/Tippett) | Implemented | `ai-ml/pramana/calibration.py` |
| API Gateway | Implemented (Simulated Kafka) | `backend/app/main.py` |
| Real-world Deanonymization | Out of Scope / Forbidden | Architecture Specs |

## 14. Current test results
*   **Repository Tests:** `python -m pytest ai-ml` -> **85 passed** (Exit Code 0).
*   **Synthetic Evaluation:** False Merge Rate = **1.5%** (compared to 29.8% for naive algorithms).
*   **Calibration:** Accessible via `/calibration/tippett` on the running API.
*   **Cyber Validation:** Skips gracefully when the massive `grams.tar.xz` is absent.

## 15. Known limitations
1.  **O(N²) Scaling:** Text embeddings use n-gram cosines without Locality Sensitive Hashing (LSH), making all-to-all comparisons computationally unfeasible on datasets larger than the synthetic range.
2.  **Operator Handover:** If an operator sells their dark web account (including PGP keys), PRAMANA merges them. This is an acknowledged residual risk.
3.  **Simulated Kafka:** The `/stream/ingest` endpoint accepts payloads but drops them (no persistent broker).

## 16. Project roadmap
*   **NOW:** Finalized mathematical bounds and simulated enterprise integration.
*   **NEXT:** Implement LSH (MinHash) to resolve O(N²) scaling on List-B features.
*   **FUTURE / DEFERRED:** Deploy a persistent distributed Kafka/PostgreSQL ledger.

## 17. Repository map
*   `ai-ml/`: The mathematical core (extraction, scoring, calibration, tests).
*   `backend/`: The FastAPI enterprise simulation boundary.
*   `cybersec/`: The deterministic ingestion and legacy cyber validation logic.
*   `docs/`: Architecture, frozen specs, and historical audits.
*   `release/`: The Master File Index and Release Manifest.

## 18. How another AI should understand this repository
1. Read this `README.md` first.
2. Read `ARCHITECTURE.md` and `PROJECT_STATUS.md`.
3. Inspect `backend/app/main.py` to understand the API contracts.
4. Inspect `ai-ml/pramana/score_pramana.py` to understand the fusion math.
5. Read `release/FILE_INDEX.md` for a comprehensive file map.
*Rule:* The executed Python code is the ultimate source of truth. If a specification document makes a grander claim than the Python code implements, the Python code is correct.

## 19. Final one-paragraph technical summary
PRAMANA is an advanced, mathematically-bounded evidence ledger for cybersecurity attribution. It ingests pseudonymous records, extracts deterministic and probabilistic features, strictly isolates them to prevent statistical leakage, and fuses them using Log-Likelihood Ratios scaled by population rarity. By actively refusing assessments lacking independent origin captures ($k<2$), it eliminates the hallucination and overconfidence risks inherent in standard black-box AI models, producing statistically calibrated Balance Sheets via a simulated enterprise FastAPI boundary.
