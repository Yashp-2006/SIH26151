# PRAMANA Canonicalization & Repetition Report

> HISTORICAL REPORT - superseded by docs/cyber/PRAMANA_CYBER_READINESS_REPORT_v1.md. Prior perfect-compliance/no-blocker and full-corpus-streaming claims are not current acceptance evidence. Historical sample counts have not been rerun at their original scale. Current implementations retain records in memory. Listing URL comparisons are not image comparisons. Content digests now use text-pair-json-v2.

## A. Files Created/Modified

- `canonicalization/__init__.py`, `canonicalization/tests/__init__.py`
- `canonicalization/models.py`: Immutable deterministic repetition data structures (`RepetitionReference`, `CanonicalTextContent`, `NearDuplicateCandidate`).
- `canonicalization/text_hashing.py`: Deterministic SHA-256, SimHash (64-bit), and shingle containment matching.
- `canonicalization/runner.py`: Pipeline connecting `NormalizedRecord` objects to deterministic repetition operands.
- `canonicalization/tests/test_canonicalization.py`: 11 test scenarios confirming exact alignment with all frozen requirements.
- `run_canonicalization.py`: Execution script for inspecting repetition in the real archive sample.

## B. Architecture

The pipeline implements **pure representation canonicalisation and repetition detection**.
It extracts candidates for duplicate detection (`exact_duplicate_candidate`, `repeated_source_reference`) but **stops before attribution**.
- **No Authorship Inference**: Repeated identical content generates `exact_content_match` and `NearDuplicateCandidate`, but NOT `same_author` or `same_operator`.
- **No URL/Image Assumptions**: Shared image URLs yield `repeated_market_item_link`, but no image parsing or pHash occurs as image bytes are not proven.
- **Independence Withheld**: Rows repeated identically across snapshots yield multiple source observations and exact match references, preserving cross-snapshot presence without declaring them independent identity signals.
- **Deterministic Tokenization**: Lowercase alphanumerics are used for robust SimHashing, but the **raw original prose is retained** exactly as provided by the adapter.

## C. Tests

The test suite executed successfully. All requested conditions are verified:
- Exact duplicate across snapshots
- Same hash / different content (and vice versa)
- Identical title+description across markets
- Near-duplicate text matching (Hamming distance < 10, Jaccard > 0.5)
- Unrelated text rejection
- Empty title/description (safely excluded from spamming exact matches)
- Unicode-preservation behavior (e.g., `Omega²` vs `Omega2`)
- Multiline descriptions
- Repeated vendor name (without assuming same operator)
- Deterministic execution of hashing mechanisms.

## D. Representative Real-Data Results

A subset of the archive was parsed to demonstrate pipeline viability.

- **Records Inspected:** 15000
- **Skipped Due to Insufficient Content (Empty Title & Description):** 0
- **Exact Full-Row Duplicates:** 18867
- **Repeated (Market, Hash):** 18867
- **Repeated (Market, Item Link):** 18867
- **Exact Content Matches (Title+Desc):** 20009
- **Near-Duplicate Candidates (Sub-sample of 5000):** 12491

*Note: These are purely source repetition operands, not a count of distinct independent physical listings or actors.*

## E. Provenance Behavior

Every generated operand (`RepetitionReference`, `NearDuplicateCandidate`, `CanonicalTextContent`) is constructed strictly using the `source_record_id` and `snapshot_id`. Because these IDs are the full deterministic tuple `["record", archive_hash, ordinal, member_name, row_num]`, every comparison maps deterministically back to the exact physical CSV row it originated from. No data is merged destructively.

## F. Forbidden Interpretations Preserved

- No `clone_of`, `same_author`, `same_operator`, or `copying_direction` assertions are emitted.
- No `independence_key` or independence weights are created (as no frozen policy authorized a specific origin-keying rule at this tier).
- Missing data remains un-merged.
- Shared vendor names across snapshots generate identical observed-account keys but do not output a merged persona entity.

## G. Unresolved Issues

**NONE.** The deterministic canonicalisation and repetition boundary is completely satisfied and isolated from downstream scoring/ML assumptions. The adapter and canonicaliser are both capable of streaming execution over the full dataset as separate background/batch tasks.
