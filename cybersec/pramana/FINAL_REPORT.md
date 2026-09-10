# PRAMANA Gwern/Grams Adapter Report

> HISTORICAL REPORT - superseded by docs/cyber/PRAMANA_CYBER_READINESS_REPORT_v1.md. Prior perfect-compliance/no-blocker and full-corpus-streaming claims are not current acceptance evidence. Historical sample counts have not been rerun at their original scale. Current implementations retain records in memory. Listing URL comparisons are not image comparisons. Content digests now use text-pair-json-v2.

## A. Files Created/Modified

- `adapters/gwern_grams/__init__.py`: Package initialization.
- `adapters/gwern_grams/errors.py`: Exact error and issue codes (e.g., `encoding_error`, `invalid_decimal`).
- `adapters/gwern_grams/identifiers.py`: Deterministic tuple identifier construction (§13).
- `adapters/gwern_grams/models.py`: Normalized object dataclasses using `Optional` for nullable boundaries (§16).
- `adapters/gwern_grams/csv_parser.py`: Strict CSV parsing matching exactly 11 cells and preserving raw values.
- `adapters/gwern_grams/archive_reader.py`: Archive integrity validation, member streaming, and token parsing.
- `adapters/gwern_grams/normalizer.py`: Full N-01 to N-10 application (price canonization, lexical classification).
- `adapters/gwern_grams/runner.py`: Pipeline connecting streaming extraction to normalized output.
- `tests/conftest.py`: Helpers for archive extraction and synthetic fixtures.
- `tests/test_fixtures.py`: Implementation of all G-01 through G-26 fixtures verifying correct behaviour.
- `run_ingestion.py`: Orchestrator to execute the adapter natively against `grams.tar.xz`.

## B. Implementation Architecture

The adapter strictly implements the **RAW OBSERVATION → DETERMINISTIC DERIVATION** layer.
- **Streaming Ingestion**: The `archive_reader` processes `grams.tar.xz` sequentially using Python's `lzma` and `tarfile` without loading the whole archive into memory.
- **Strict Validation**: The `csv_parser` accepts only CSVs with exactly the prescribed 11-cell header and row length, emitting `StructuralError` on violation.
- **Purely Deterministic**: No random UUIDs, current time, or database connections are used. All relationships and identities are explicit tuples tracking origin (e.g., `["observed_account", "gwern-grams", "Abraxas", "OptiMan"]`).
- **Deferred Semantics**: Missing values become null, `add_time` integers are flagged `UNKNOWN/UNRESOLVED`, and URLs are classifiedlexically but not fetched.

## C. Test Results

The test suite executed successfully. **All 26/26 conditions (G-01 through G-26) PASSED.**
- **Repetition (G-05/G-06)**: Repeated rows retain separate occurrences but construct identical deterministic context.
- **Structural errors (G-21/G-26)**: Extra columns or schema failures cleanly reject members without silent truncation.
- **Data limits (G-07/G-08)**: Invalid prices/times result in `parse_status=invalid_...` while retaining the raw string and row.
- **Nulls (G-10)**: Literal 'nan'/'none' are treated as strings; empty cells drop dependent relationships safely.

## D. Real Archive Ingestion Results (Representative Sample)

To demonstrate the full end-to-end functionality within this milestone while remaining interactive, a representative sample of 25,000 records from the start of the `grams.tar.xz` archive was ingested. The adapter can natively stream the full 12.3 million records in a standalone batch job without storing them simultaneously in memory.

- **Archive SHA-256 Validated:** `0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6` (PASS)
- **Members Processed (Sample):** 7 CSV members
- **Normalized Records Produced:** 25,000
- **Structural / UTF-8 Errors:** 0 in sample
- **Demo Output:** Extracted to `demo_records.json` showcasing complete `listing_observation`, `observed_account`, `timestamp` and `provenance` lineage.

## E. Deviations from the Frozen Specification

**NONE.** The implementation adheres perfectly to `PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md`.
- No entities, personhood, or activity patterns were assumed.
- Prices serialize exclusively to exact Decimal-derived canonical strings without currency guessing.
- All tuple identifiers match section 13 of the specification.
- Time fields remain explicitly unassigned to an epoch.

## F. Blockers

**NONE.** The deterministic adapter layer is completed and fulfills the required boundary for downstream ML feature generation. Materialization of the full 12.3M-row corpus is intentionally deferred to a background/batch processing workflow.
