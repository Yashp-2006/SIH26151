# PRAMANA: Project Status

**Maturity:** Advanced Prototype
**Date:** 2026-09-10

## Implemented Capabilities
- **Independence Accounting ($k \ge 2$):** Actively running in `score_pramana.py`.
- **Rarity Scaling ($	au$):** Functioning.
- **List-A/B Redaction:** Actively stripping crypto hashes from ML text models.
- **Calibration (ECE/Tippett):** Implemented in `calibration.py`.
- **API Boundary:** Strict Pydantic models via FastAPI (`backend/app/main.py`).

## Partial / Stub Capabilities
- **Kafka Streaming:** API acknowledges ingestion but lacks a persistent broker backend.
- **Archive Extraction:** Safely skips if `grams.tar.xz` is absent, but lacks robust path traversal safeguards for hostile files.

## Deferred Items
- **Locality Sensitive Hashing (LSH):** Required to solve O(N²) scaling on text similarity.
- **Real-World Empirical Priors:** Currently using design priors ($\lambda = 0.2$) instead of dataset-fitted priors.
- **Frontend UI:** Completely deferred.

## Known Limitations & Weaknesses
- **Operator Handover:** If an operator sells their account and keys, PRAMANA merges them (False Positive).
- **O(N²) Bottleneck:** All-to-all embedding matching is not production-scalable yet.

## Evaluation & Reproducibility
- **Current Tests:** 85 passed.
- **Synthetic Evaluation:** False Merge Rate = 1.5%.
- **Reproducibility:** Excellent (requirements locked, scripts deterministic).

## DO NOT CLAIM:
- "Production-ready streaming" (it is simulated).
- "Real-world deanonymization" (it is a pseudonymous clustering tool).
