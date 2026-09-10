# PRAMANA: Post-Audit Reconciliation Plan & Current State Map

**Date:** 2026-09-10
**Author:** AI Project Lead (Taking over from Astra, Gemini, and Opus)

## 1. The Audit Conflict: Two Separate Workstreams

A significant architectural and auditing conflict was identified during this handover:
* **The Gemini Audit & Astra Sprint:** Focused on the `SIH26151-main` repository. This is the **Dark Web Identity Attribution** workstream (List-A deterministic evidence, List-B probabilistic evidence, Grams dataset, offline fusion, and evidence ledgers). 
* **The Opus Audit:** Focused on the `SIH-2026-compiled` repository. This is the **Live Network Intrusion Fusion** workstream (AlertBus, live PCAP replays, incident tracking, DDoS/Port Scan detectors). 

Because of this repository split, the Opus P0/P1 fixes (fixing `time.time()` wall-clock leakage in `bus.py`, and fixing TP inflation in `tools/evaluate.py`) were applied to the live-network engine, **not** the dark-web intelligence engine. These findings do not directly apply to the `SIH26151-main` repository, which operates completely offline and has a different evaluation harness (`ai-ml/pramana/evaluate.py` doing pairwise link classification).

## 2. Authoritative Current-State Map (`SIH26151-main`)

Based on the frozen CY-POL specifications and the actual code present in this repository, the current state is:

1. **Ingestion & Canonicalization (CyberSec):** Deterministic extraction of the Grams dataset is implemented. Provenance is preserved.
2. **List-A Deterministic Evidence:** Fully implemented (PGP, wallets, infrastructure).
3. **List-B Probabilistic Evidence:** Implemented (Text Embeddings, Stylometry, NLP). *However, prior to this handover, it suffered from severe List-A to List-B leakage.*
4. **Fusion & Bounded Scoring (AI/ML):** `score_pramana.py` correctly bounds the log10 LR scores, respects maximum family caps, and utilizes the Rarity factor (Tau). Astra successfully removed zero-weight LLM inflation and locked the mathematical bounds.
5. **Evaluation Harness:** Synthetic `range_sim.py` operates properly. It evaluates False Merge Rates (FMR) and pairwise precision/recall.
6. **LLM Authority:** Properly suppressed. LLMs act only as explainers over the evidence balance sheet, not as evidence creators.

## 3. Highest-Value Verified Fixes Implemented in this Sprint

**P0 Fix: List-A Identifier Masking before List-B (Gemini Finding)**
* **The Vulnerability:** Raw listing text containing PGP keys, Bitcoin addresses, and Onion URLs was passed directly into `text_embeddings.py` (character 3-gram cosine similarity) and `stylometry.py`. Because a PGP key block is textually unique, two listings sharing a PGP key would produce an artificial 1.0 embedding similarity. The fusion engine would then treat List-A (PGP Match) and List-B (Embedding Match) as independent evidence, illegitimately double-counting the signal and breaking the "evidence arithmetic" core thesis.
* **The Fix:** Created `ai-ml/shared/redaction.py` with deterministic regex filters to scrub `[PGP_REDACTED]`, `[BTC_REDACTED]`, `[EMAIL_REDACTED]`, `[URL_REDACTED]`, and `[ONION_REDACTED]`. Applied this sanitization to the input pipelines of `text_embeddings.py` and `stylometry.py`.

## 4. Immediate Next Steps & Deferred Actions

* **Consolidation:** The SIH project must formally decide whether the live-network intrusion system (`SIH-2026-compiled`) and the dark-web attribution system (`SIH26151-main`) are being merged into a single API backend, or presented as two separate verticals. 
* **Calibration (Deferred P1):** The scoring parameters (Lambda, K_min, ceilings) are still design priors. Empirical calibration against a hold-out real-world corpus is required before claiming "calibrated probabilities".
* **Real-World Open Evaluation (Deferred P1):** The synthetic benchmark performs well, but we must eventually evaluate against the true `grams.tar.xz` dataset to prove open-world distractor resistance.
* **Security & Input Handling (P2):** API paths remain local-only and lack authentication. Archive extraction path traversal guarantees rely heavily on standard libraries and must be audited with adversarial zip payloads.

**Final Verdict:** PRAMANA remains a highly advanced, defensible research prototype for evidence-centric attribution. The architecture holds up conceptually; the implementations are strictly isolated and deterministic. We must strictly adhere to the language policy: we produce "evidence-weighted hypothesis assessments", not "guaranteed identity deanonymization".
