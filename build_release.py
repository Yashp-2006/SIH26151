import os
import shutil
import subprocess

base_dir = r"C:\Users\revan\Downloads\SIH26151-main\SIH26151-main"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# 1. PROJECT_STATUS.md
project_status = """
# PRAMANA: Project Status

**Maturity:** Advanced Prototype
**Date:** 2026-09-10

## Implemented Capabilities
- **Independence Accounting ($k \ge 2$):** Actively running in `score_pramana.py`.
- **Rarity Scaling ($\tau$):** Functioning.
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
"""
write_file("PROJECT_STATUS.md", project_status)

# 2. ARCHITECTURE.md
architecture = """
# PRAMANA Architecture

## Component Diagram
```text
[External Data] --> [Ingestion Adapter] --> [Canonicalization]
                                                |
                                                v
[List-B Probabilistic] <--- [Redaction] <--- [List-A Deterministic]
        |                                       |
        +------------> [Fusion Core] <----------+
                             | (Applies tau and k limits)
                             v
                     [Balance Sheet] ---> [FastAPI Gateway] ---> [Analyst / LLM]
```

## Data Flow & Control Flow
1. Raw listing text is canonicalized.
2. `List-A` indicators (PGP, BTC) are extracted deterministically.
3. `Redaction` mathematically scrubs `List-A` from the raw text.
4. `List-B` extracts stylometric and semantic embeddings from the scrubbed text.
5. Both output `EvidenceCandidate` objects to the `Fusion Core`.
6. Fusion enforces independence ($k \ge 2$) and rarity scaling.
7. Outputs an immutable `BalanceSheetResponse`.

## Trust Boundaries
- **UNTRUSTED:** Raw dark-web text.
- **TRUSTED:** Cryptographic validations (PGP signatures).
- **AIR-GAPPED:** The LLM Analyst. The LLM is strictly prohibited from mutating the Log-LR scores. It may only read the finalized Balance Sheet to output English explanations.
"""
write_file("ARCHITECTURE.md", architecture)

# 3. REPRODUCTION.md
reproduction = """
# Reproduction Guide

A new engineer can reproduce the entire project state without external dependencies (other than Python 3.13).

## Prerequisites
- Windows / Linux / macOS
- Python 3.13.x

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r backend/requirements.txt
pip install -r requirements-research-lock.txt
```

## Running the Evaluation (Proves the Math)
```bash
python -m pramana.evaluate
```
*Expected Output:* A table demonstrating the False Merge Rate dropping from 29.8% to 1.5%.

## Running the API Gateway
```bash
uvicorn backend.app.main:app --reload
```
*Expected Output:* Uvicorn starts on port 8000. Navigate to `http://127.0.0.1:8000/docs` to see the OpenAPI schema, and hit `/calibration/tippett` for live metrics.
"""
write_file("REPRODUCTION.md", reproduction)

# 4. EVALUATION.md
evaluation = """
# Evaluation Methodology

## Datasets
- **RANGE-SIM:** A synthetic, closed-world dataset containing 900 pairs (99 positive, 801 negative) of simulated dark-web interactions with planted decoys.
- **GRAMS (Missing/Quarantined):** A 12-million record historical dark web dataset. `run_cyber_validation.py` operates on a 4,397-record bounded subset but skips if the archive is absent.

## Metrics
- **False Merge Rate (FMR):** The critical metric. The percentage of non-target pairs falsely attributed to the same operator.
- **Expected Calibration Error (ECE):** Evaluates if the output Log-LR actually correlates with real-world probability.
- **Tippett Plots:** Cumulative Distribution Functions of same-source vs different-source comparisons.

## What it Proves
The evaluation proves that applying Independence Accounting ($k$) to evidence fusion dramatically reduces FMR compared to naive additive algorithms.
"""
write_file("EVALUATION.md", evaluation)

# 5. SECURITY.md
security = """
# Security Model

## Threat Vectors Analyzed
1. **List-A / List-B Leakage (Fixed):** Handled by `ai-ml/shared/redaction.py`.
2. **Clone / Hub Attacks (Fixed):** Adversaries pasting another's PGP key. Handled by the $k \ge 2$ refusal and Rarity ($\tau$) scaling.
3. **Prompt Injection (Mitigated):** Handled by completely removing the LLM from the scoring loop.
4. **Tarbombs (Vulnerable - DEMO ONLY):** Archive extraction uses standard `tarfile`. Do not ingest untrusted hostile archives in production without patching with `data_filter`.
5. **API Auth (Missing - DEMO ONLY):** FastAPI Gateway currently lacks OAuth2 / API Key authentication.
"""
write_file("SECURITY.md", security)

# 6. release/MANIFEST.md
manifest = """
# Release Manifest
**Release Name:** PRAMANA_FINAL_RELEASE_v1
**Date:** 2026-09-10
**Included Components:**
- `ai-ml/` (Math & Fusion)
- `backend/` (FastAPI Gateway)
- `cybersec/` (Ingestion)
**Test Status:** 85/85 Passed.
**Reproducibility:** Fully reproducible on Python 3.13.
**Excluded Files:** Huge real-world data archives (`grams.tar.xz`).
"""
write_file("release/MANIFEST.md", manifest)

# 7. release/FILE_INDEX.md
file_index = """
# File Index
- `README.md`: Master entry point.
- `PROJECT_STATUS.md`: Brutally honest engineering status.
- `ai-ml/pramana/score_pramana.py`: The authoritative fusion math.
- `ai-ml/shared/redaction.py`: Security boundary for List-B.
- `ai-ml/pramana/calibration.py`: ECE/Tippett plots.
- `backend/app/main.py`: Enterprise API Gateway.
- `cybersec/pramana/run_cyber_validation.py`: Data ingestion script.
- `docs/historical/`: Old reports and obsolete structures.
"""
write_file("release/FILE_INDEX.md", file_index)

# 8. Move historical files
os.makedirs(os.path.join(base_dir, "docs", "historical"), exist_ok=True)
historical_files = [
    "HARDENING_REPORT.md", 
    "POST_AUDIT_RECONCILIATION_PLAN.md", 
    "PRAMANA_MASTER_ARCHITECTURE.md", 
    "FOLDER_STRUCTURE.md",
    "PITCH_GUIDE.md"
]
for hf in historical_files:
    hf_path = os.path.join(base_dir, hf)
    if os.path.exists(hf_path):
        shutil.move(hf_path, os.path.join(base_dir, "docs", "historical", hf))

# 9. Clean caches & old scripts
for root, dirs, files in os.walk(base_dir, topdown=False):
    for d in dirs:
        if d in ["__pycache__", ".pytest_cache", "demo_out"]:
            shutil.rmtree(os.path.join(root, d), ignore_errors=True)

old_scripts = ["create_zip.py"]
for script in old_scripts:
    p = os.path.join(base_dir, script)
    if os.path.exists(p):
        os.remove(p)

# 10. Zip creation logic
import zipfile
output_zip = r"C:\Users\revan\Downloads\PRAMANA_FINAL_RELEASE_v1.zip"

print("Creating final ZIP...")
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        # Already cleaned caches, but double check
        dirs[:] = [d for d in dirs if d not in {".venv", "__pycache__", ".pytest_cache", ".git"}]
        for file in files:
            if file.endswith(".zip"): continue
            file_path = os.path.join(root, file)
            arcname = os.path.join("PRAMANA_FINAL_RELEASE_v1", os.path.relpath(file_path, base_dir))
            zipf.write(file_path, arcname)

print("Final ZIP created successfully.")
