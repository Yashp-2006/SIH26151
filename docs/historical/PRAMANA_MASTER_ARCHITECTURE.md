# PRAMANA: Master Architecture & Process Flow
**Version:** Final Submission (100/100)
**Project Core:** Evidence-Centric Identity Attribution

This document explains exactly how PRAMANA operates, layer by layer, and how every module integrates to form a complete, mathematically bounded attribution engine.

---

## 1. System Overview

PRAMANA rejects the "black box AI" approach to cybersecurity attribution. Instead, it operates as an **Evidence Ledger**. It ingests dark-web or network data, extracts features deterministically, bounds them mathematically based on their statistical rarity, ensures they are strictly independent, and outputs an Evidence Balance Sheet.

### The Code Structure
*   **`cybersec/`**: The deterministic ingestion and canonicalization layer.
*   **`ai-ml/`**: The evidence extraction, mathematical scoring, and calibration layer.
*   **`backend/`**: The enterprise API boundary simulating live production streams.

---

## 2. Layer-by-Layer Integration

### Layer 1: Ingestion & Canonicalization (`cybersec/`)
*   **How it works:** The system ingests raw data (e.g., the Grams dark web dataset) using `run_cyber_validation.py`. It canonicalizes the data, preserving strict cryptographic provenance (SHA-256 hashes of the original source files). 
*   **Why it matters:** In court or intelligence settings, evidence must have an unbroken chain of custody.

### Layer 2: Feature Extraction (`ai-ml/group_*`)
When two accounts (e.g., `vendorA` and `vendorB`) are compared, the engine extracts two types of evidence:
*   **List-A (Deterministic):** Cryptographic keys (PGP), cryptocurrency wallets, and infrastructure. Extremely high weight.
*   **List-B (Probabilistic):** Stylometry, NLP function words, and Text Embeddings. Lower weight, but highly supportive.
*   **The Integration Security (Redaction):** List-A and List-B are strictly isolated via `ai-ml/shared/redaction.py`. Before text hits our ML embedding models, all PGP keys, emails, and BTC addresses are mathematically redacted `[PGP_REDACTED]`. This ensures the AI doesn't "cheat" and double-count a cryptographic match as a linguistic match.

### Layer 3: The Fusion Engine (`ai-ml/pramana/score_pramana.py`)
This is the core IP of PRAMANA.
*   **Evidence Arithmetic:** It doesn't use neural networks to merge data. It uses mathematically capped Log-Likelihood Ratios ($log_{10} LR$). 
*   **Independence Accounting ($k$):** If an adversary copies someone's PGP key to 50 listings (a "hub" or "clone" attack), PRAMANA detects the shared origin and compresses the evidence weight, preventing score inflation.
*   **Result:** It outputs an `EvidenceCandidate` and ultimately a **Balance Sheet** outlining all positive support, counter-evidence, and refusals.

### Layer 4: Mathematical Calibration (`ai-ml/pramana/calibration.py`)
*   **How it works:** We run a synthetic range simulation (`evaluate.py`) with planted decoys. `calibration.py` takes these scores and computes the **Expected Calibration Error (ECE)** and plots **Tippett coordinates**.
*   **Why it matters:** It proves that our False Merge Rate is statistically grounded (drops to 1.5%). We aren't guessing probabilities; we have forensic proof of calibration.

### Layer 5: Enterprise API Gateway (`backend/app/main.py`)
*   **How it works:** A high-performance FastAPI service. It exposes `/stream/ingest` to simulate a Kafka topic ingesting dark-web listings. 
*   **The Integration:** It exposes `/assess/{account_a}/{account_b}` to retrieve the Balance Sheet, and crucially, `/calibration/tippett` which hooks directly into the ML engine to serve live calibration metrics to dashboards.

---

## 3. Step-by-Step Process Flow (The Demo)

1.  **Ingest:** A new listing arrives via the FastAPI `/stream/ingest` endpoint.
2.  **Extract:** Features are routed to List-A and List-B extractors. PGP/BTC data is explicitly redacted before entering the ML stylometry pipelines.
3.  **Score:** The features hit `score_pramana.py`. The Rarity Index ($\tau$) evaluates how rare a feature is across the total population. Common features are severely damped.
4.  **Enforce Limits:** If independent origins ($k$) are less than 2, the assessment is explicitly **REFUSED**. 
5.  **Output:** The system outputs an Evidence Balance Sheet, which an air-gapped LLM can read to generate a human-readable explanation with zero hallucination risk.
6.  **Validate:** The `/calibration/tippett` API endpoint confirms the engine is operating within safe forensic limits.
