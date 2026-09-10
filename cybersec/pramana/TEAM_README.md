# PRAMANA — start here

PRAMANA is designed to support contestable, human-reviewed pseudonymous intelligence. The current software is an **offline deterministic cyber review slice**, not a deanonymization platform or completed evidence ledger.

Read the [final project handoff](PRAMANA_FINAL_PROJECT_HANDOFF_v1.md) for team authority/ownership and the [reproduction guide](docs/PRAMANA_REPRODUCTION_GUIDE_v1.md) for setup and replay.

## Quick start

Run from the repository root. Verified environment: Python **3.13.7**, pytest **9.0.2**. The application uses the Python standard library. Tests require pytest. No database, model, Tor service or real archive is needed for the synthetic demo.

```powershell
python --version
python -m pytest -q
python run_cyber_demo.py
```

Expected: **76 passed, 13 skipped**; demo **18 records, 53 derivations, 13 eligible hub accounts**, zero validated evidence candidates, null assessment. Open [review.html](docs/cyber/demo/review.html). It is an escaped, static review input; no review decision is persisted.

If the verified `grams.tar.xz` is available at repository root, optionally run:

```powershell
python run_cyber_validation.py
```

This validates **4,397 records in two CSV members**, not the full corpus. Expect 8,794 text spans, one unvalidated PGP-like marker, zero Bitcoin matches, and 8,795 passing replay checks.

## Folder map

| Path | Purpose |
|---|---|
| `adapters/gwern_grams/` | Pinned archive reader, CSV parser, normalization, source IDs/provenance |
| `canonicalization/` | Exact repetition and bounded near-match comparison operands |
| `cyber/` | Deterministic indicators, restrictions, review packet and static HTML |
| `tests/`, `canonicalization/tests/`, `pytest.ini` | Offline tests; deep archive fixtures are opt-in |
| `docs/cyber/demo/` | Generated synthetic tar, review JSON and HTML |
| `docs/cyber/validation/` | JUnit and bounded real-source validation evidence |
| `docs/cyber/` | Frozen adapter contract and supporting workstream reports |
| `hatch-runs/` | Unrelated existing assets; not a cyber runtime dependency |

## Frozen authorities

1. [Cyber policy](PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md).
2. [Grams adapter/data contract](docs/cyber/PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md).
3. Code and executed tests establish implementation, not permission to override policy.

[Master Blueprint](PRAMANA_Master_Blueprint.md) supplies the existing architectural plan. The final handoff consolidates team communication; it does not supersede frozen contracts. Older reports and the supplied FINAL2 draft are supporting context, not current implementation authority.

## Current limits and next work

**IMPLEMENTED / TESTED:** normalization, repetition operands, text/PGP-marker extraction, legacy Bitcoin format validation, lineage checks, declared Bitcoin-population hub restrictions, scoped clone restrictions and review export.

**REPRESENTATIVE VALIDATION:** two real CSVs; no demonstrated wallet finding or performance benchmark.

**SPECIFIED / DEFERRED:** ledger/backend/API, persistent review, complete origin grouping/k, promotion (DC-06), LR/rarity/decay, numerical counter-evidence, calibration, hard veto, RANGE-SIM/TOR and unimplemented modalities.

**OUT OF SCOPE:** real-world identity, automatic persona acceptance/merging, unauthorized/live-marketplace collection, autonomous investigation, Monero tracing and prohibited MVP technologies.

Next: PL/FRONTEND integrate the existing review-input contract without inventing scores; Cyber/ML/PL/EV resolve DC-06 and source/context fixtures before candidate promotion, then DC-01 before independent support counting. Ownership and P0 acceptance criteria are in the final handoff.

Avoid legacy `run_ingestion.py`, `run_canonicalization.py`, full ingestion and `--archive-fixtures` for onboarding: they are not this bounded demonstration path. Keep raw fields, exact IDs and unknown times intact. Do not call the planned software ledger a blockchain.
