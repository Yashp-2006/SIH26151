# PRAMANA Reproduction Guide v1

Operational companion to [the final project handoff](../PRAMANA_FINAL_PROJECT_HANDOFF_v1.md). Verified during consolidation: Python 3.13.7 / pytest 9.0.2 on Windows. Run all commands **from the repository root**, not from `docs/` or a package subdirectory.

## 1. Environment

The demo and bounded validator use the standard library (`csv`, `tarfile`, `lzma`, `hashlib`, JSON and dataclasses). No web service, API key, database, GPU, model or Tor process is required. The tests require pytest.

```powershell
python --version
python -m pytest --version
```

Expected tested versions: Python 3.13.7 and pytest 9.0.2. If pytest is absent, install it into the interpreter you intend to use:

```powershell
python -m pip install pytest==9.0.2
```

The installation is ordinary environment setup and may need network access; running the demo/tests does not. No dependency lockfile or fully provisioned container is shipped. The Blueprint's planned backend uses Python 3.12; this pass verifies 3.13.7 only and does not revise the planned architecture or claim 3.12 compatibility testing.

## 2. Required files

For tests and the synthetic demo, retain these from the project download/checkout:

- `adapters/`, `canonicalization/`, `cyber/`, including their `__init__.py` files.
- `tests/`, `canonicalization/tests/`, `pytest.ini`.
- `run_cyber_demo.py`; the output directory must be writable.

For optional real-source validation, additionally retain `run_cyber_validation.py` and the verified `grams.tar.xz`. Do not rename a different release to satisfy the path. The archive is not required for the normal tests or synthetic demo; obtain any missing release through the team's authorised DE process, not from a guessed URL.

Read the frozen [Cyber policy](../PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md) and [adapter specification](cyber/PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md) before making changes. Neither the downloaded FINAL2 draft nor this conversation is needed to run the package.

## 3. Verify the optional Grams archive

Actual expected location: repository root `grams.tar.xz`, not `data/raw/gwern/grams.tar.xz`.

PowerShell byte-identity check:

```powershell
Get-FileHash -LiteralPath .\grams.tar.xz -Algorithm SHA256
```

Expected SHA-256:

```text
0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6
```

The archive is 69,740,360 compressed bytes in the verified release. Hashing compressed bytes is not corpus ingestion. A match establishes byte identity only, not authenticity, licensing, ownership assertions or actor truth. `run_cyber_validation.py` repeats the digest check and rejects a mismatch; never modify the pinned digest to force another archive through.

## 4. Run the tests

```powershell
python -m pytest -q --junitxml=docs/cyber/validation/pytest.xml
```

Expected current result: **76 passed, 13 skipped, 0 failed** (89 collected cases). The skips are old archive-seeking fixtures, deliberately disabled by default even when the archive exists. Do not pass `--archive-fixtures` for this demonstration. Some legacy tests use their synthetic fallback when archive fixtures are disabled; the JUnit record is the exact case-level evidence.

The command regenerates `docs/cyber/validation/pytest.xml`. Timing and timestamp metadata can change between runs. Passing mechanism tests are not a measured extraction/attribution benchmark.

## 5. Run the one canonical demo

```powershell
python run_cyber_demo.py
```

The script generates a small deterministic **synthetic tar**, normalizes its CSVs in the explicit `synthetic-grams` namespace, computes repetition operands, derives indicators, applies declared restrictions and writes the review artifacts. It does not load `grams.tar.xz` or create actor truth labels.

Expected console values:

```json
{
  "records": 18,
  "indicators": 53,
  "validated_evidence_candidates": 0,
  "assessment": null,
  "hub_accounts": 13,
  "promotion": "blocked_DC-06"
}
```

The console also reports the review JSON path; path separators depend on the operating system.

## 6. Inspect outputs

| File | Meaning |
|---|---|
| [demo/synthetic_source.tar](cyber/demo/synthetic_source.tar) | Reproducible fixture bytes; actual fixture digest is recorded in the packet. Not real Grams and not a RANGE-SIM truth corpus. |
| [demo/review_packet.json](cyber/demo/review_packet.json) | Normalized source values, indicators, field spans, provenance, supplied population/clone declarations, restrictions and competing propositions. |
| [demo/review.html](cyber/demo/review.html) | Escaped static view of that packet. Open locally in a browser; no server/start command needed. No review decisions are recorded. |

The script overwrites these generated artifacts on rerun. Keep manual reviewer notes outside generated files. For an alternate output folder the existing CLI supports:

```powershell
python run_cyber_demo.py --output-dir docs/cyber/demo_local
```

Do not interpret family labels as positive evidence. The three labels F1/F2/F5 cover unvalidated PGP wording, address-format candidates and text spans. No supporting k is calculated. A checksum does not establish address control, and exact text equality does not adjudicate a clone. The demo explicitly supplies a clone determination for B's description and eligibility for its first-snapshot Bitcoin-format hub population.

## 7. Optional bounded real-data validation

```powershell
python run_cyber_validation.py
```

Expected generated file: [validation/representative_validation.json](cyber/validation/representative_validation.json). Expected scope/results:

| Check | Expected |
|---|---|
| `grams/2014-06-09/1776.csv` | 83 records |
| `grams/2015-04-20/Abraxas.csv` | 4,314 records |
| Total normalization | 4,397 records, zero structural errors |
| Derivations | 8,794 text spans and 1 unvalidated PGP-like marker |
| Replay / blocked-promotion checks | 8,795 each |
| Bitcoin matches | 0 in this sample |
| Validated evidence candidates / assessments | 0 / 0 |

The report includes pinned member digests, source locations and relevant code hashes. This command validates normalization/extraction/promotion blocking; it does **not** run real-source canonicalization, build a real-source review packet, qualify real hub populations or establish absence of crypto material elsewhere. It reads two known CSV members only; it does not ingest the full 12,384,326-record corpus.

An alternate archive path is supported by the existing `--archive` argument, but its bytes must match the pin. Keep defaults for the canonical reproduction.

## 8. Intentional stopping points

- `validated_evidence_candidates` and `authoritative_evidence` are empty; promotion is blocked by DC-06 and qualification/origin requirements.
- `assessment` and `score` are null. Independence key and eligible k are unknown; the supplied-k ceiling test does not calculate a band.
- Counter-checks distinguish not-run, unimplemented and inconclusive. Temporal hard veto is deferred; no automatic EXCLUDED.
- PGP signatures, contacts, infrastructure telemetry, image features, F6/F7/F8/F9 generators, full ledger/API, persisted human review, scoring/calibration and RANGE-SIM/TOR are not completed.

## 9. Troubleshooting / acceptance

| Symptom | Action |
|---|---|
| `No module named pytest` | Install the stated pytest version into the same `python` interpreter. |
| Package import/path failure | Return to repository root and verify all three packages and test directories are present. |
| Archive missing | Run the synthetic demo/tests; omit optional real validation until DE supplies the pinned release. |
| Archive digest/member mismatch | Stop source-specific validation; check file integrity/release. Do not change frozen IDs/schema. |
| 13 skipped tests | Expected default behaviour, not 13 passing archive tests. |
| Blank score or blocked promotion | Expected safety boundary, not a failed demo. |
| Historical report differs | Use current test output and bounded validation with the final handoff, not older unqualified completion claims. |

Do not use `run_ingestion.py`, `run_canonicalization.py`, unlimited `run_adapter(...)` or full/deep-archive fixtures as onboarding shortcuts. Those are legacy paths with different scope and can overwrite historical reports. No `make evaluate`, backend server or model-training command exists for this completed slice.
