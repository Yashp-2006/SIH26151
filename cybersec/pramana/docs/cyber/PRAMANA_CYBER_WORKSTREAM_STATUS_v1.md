# PRAMANA Cyber Workstream Status v1

Inventory date: 2026-09-09. Controlling sources: CYBER_SPEC_v1, Master Blueprint, Grams adapter spec. This report distinguishes code inspection, executable tests, historical reports and policy. No full-corpus run is authorised for this pass.

## Baseline inventory before this completion pass

| Category | Capability | Evidence and limits |
|---|---|---|
| A — implemented; tests present, rerun pending | CSV parsing/normalization, tuple IDs, unknown timestamps, missingness | `adapters/gwern_grams/`; `tests/test_fixtures.py`. Presence of tests alone is not a current passing run. |
| A — implemented; tests present, rerun pending | Exact row/content/source-reference comparisons; SHA-256/SimHash/shingles | `canonicalization/`; `canonicalization/tests/test_canonicalization.py`. These are comparison operands, not canonical origin adjudication or identity resolution. |
| B — implemented + reported representative validation | Adapter sample; repetition sample | `ingestion_report.json` reports 25,000 records/7 CSV members; `CANONICALIZATION_REPORT.md` reports 15,000 records and a 5,000-text near-match subset. Historical outputs, not rerun or benchmark measurements in this pass. Pair counts are not unique listings. |
| C — specified, absent | Typed indicator extraction, qualified evidence promotion, analyst review UI/API, ledger sealing/retraction, authorised collection enforcement | CY-POL-005, 008–010, 025, 030–033; no corresponding implementations found. |
| C — specified, absent | Account-based hub threshold and scope-local clone suppression | CY-POL-018/023. Count/suppression rules are frozen; rarity mathematics is not. |
| D — deferred by policy | Complete independence groups/k, negative aggregation, LR/rarity/decay, temporal hard veto, evidence-row promotion, infrastructure methods, F8/F9, remaining gates | DC-01–DC-09. No implementation may fill these with defaults. |
| C/D — partial policy, no executable range | RANGE-SIM and RANGE-TOR | CY-POL-028/029, OD-02. Separate manifests and evaluation/access boundaries still required. |
| E — not required / prohibited for MVP | Live marketplace collection, real-world identity, automatic persona acceptance/merges, Monero tracing, autonomous investigation, DS/SL, GNNs, Kafka/Neo4j/Elasticsearch | CY-POL-035; Blueprint §1.4/§1.6. These are not completion targets. |

## Baseline defects and report corrections

1. `runner.py` accepted members with row-level structural errors and discarded all but five normalized records from each member's returned result. That contradicts adapter N-02 and prevents a complete downstream handoff.
2. CSV parsing did not enable strict malformed-quote handling. Numeric regex `$` could accept a final newline, violating exact raw grammar.
3. Serialized provenance omitted acquisition fields declared by the contract.
4. Canonicalization retains records and uses pairwise comparisons; it is not a proven bounded-memory full-corpus streaming engine. A delimiter-based text digest also required unambiguous field framing.
5. `FINAL_REPORT.md` claims “perfect” compliance/no blockers; `CANONICALIZATION_REPORT.md` claims no unresolved issues and confuses listing URLs with image references. These statements are superseded by this inventory and the final readiness report.

## Selected completion scope

Complete deterministic indicator extraction with exact field-span lineage, validation results and a review packet. Repair upstream defects needed for this slice. Implement only frozen suppression/policy guards, with explicit caller-supplied eligibility decisions. Do not implement scored evidence, DC-06 promotion, independence groups, actual family k, attribution or hard-veto detection.

Final executable test results and delivery classification are recorded below after validation and in `PRAMANA_CYBER_READINESS_REPORT_v1.md`.

## Completion-pass result

| Category | Current capability | Executable evidence |
|---|---|---|
| A — IMPLEMENTED + TESTED | Atomic CSV member rejection; complete returned record handoff; exact numeric grammar; acquisition-field serialization; versioned content hashing | `tests/test_adapter_regressions.py`; upstream defects corrected. |
| A — IMPLEMENTED + TESTED | Text spans; PGP-like markers; Bitcoin legacy Base58Check; provenance replay and altered-payload rejection | `cyber/indicators.py`; `tests/test_cyber_slice.py`. No PGP packet/signature verification. |
| A — IMPLEMENTED + TESTED | >12 eligible-account hub threshold, explicit origin exclusions, occurrence-scoped clone restriction, supplied-k band ceiling | `cyber/policy.py`; boundary/adversarial fixtures. Population/clone qualification remains externally supplied. No rarity, automatic clone adjudication or actual k calculation. |
| A — IMPLEMENTED + TESTED | Repetition/discrepancy review packet and escaped offline HTML | `cyber/review.py`, `cyber/render.py`, `run_cyber_demo.py`; deterministic replay/escaping tests. |
| B — IMPLEMENTED + REPRESENTATIVE VALIDATION | Pinned archive → normalization → text/PGP-like derivation → replay → blocked promotion | `validation/representative_validation.json`: two CSVs, 4,397 records, 8,795 checked derivations. No Bitcoin matches in this bounded sample. |
| C — SPECIFIED, NOT IMPLEMENTED | Full ledger, review API/persistence, capture sealing/retraction, operational source qualification/access enforcement, additional modalities | Frozen Cyber rules and Blueprint phases; no product-service completion claimed. |
| D — DEFERRED | Promotion/row mapping (DC-06), complete grouping/k (DC-01), scoring/counterweights/decay/calibration dependencies, veto detector, remaining generator/method/gate contracts | DC-01–DC-09 preserved. Candidate arrays are empty and assessment is null. |
| E — NOT REQUIRED / OUT OF SCOPE | Prohibited MVP technologies and collection/identity behaviours listed above | No implementation added. |

**Current tests:** 76 passed, 13 skipped, zero failures (`validation/pytest.xml`). Skips are older deep-archive fixtures, opt-in via `--archive-fixtures`; they were not run. Default tests are offline and bounded. Representative validation is a separate bounded command.

**Supporting-source reconciliations retained:** AI/ML Plan p. 4 mixes evaluation domains and summarizes five contradiction classes; Dossier p. 12 also summarizes five. CY-POL-026/028/029 control: seven classes and separate RANGE-SIM/RANGE-TOR. AI/ML Plan p. 7 requires the evidence-row handoff to be frozen; DC-06 remains open. Dossier p. 27 disclaims achieved benchmark numbers. No contradiction was silently translated into code.

**Dataset scope:** Grams structure is verified for the pinned release; OPUS remains acquisition context. CrimeBB is still unverified/unavailable here. No new rights, acquisition times, actor truth or corpus-wide indicator statistics were inferred.
