# PRAMANA Final Project Handoff v1

**Version:** FINAL_PROJECT_HANDOFF_v1 · **Verified:** 2026-09-09. This is the authoritative **team consolidation of current repository state**, not a replacement for frozen policy or a declaration that planned services are complete.

**Start:** [TEAM_README](TEAM_README.md) · **Run:** [Reproduction guide](docs/PRAMANA_REPRODUCTION_GUIDE_v1.md) · **Inspect:** [Offline demo](docs/cyber/demo/review.html).

### Authority and claim discipline

1. [CYBER_SPEC_v1](PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md): frozen cyber policy.
2. [Grams adapter specification](docs/cyber/PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md): frozen Grams data contract; actual pinned archive bytes establish source structure/content.
3. Actual repository code and executed tests: implementation evidence; a defect cannot amend policy.
4. [CYBER_READINESS_v1](docs/cyber/PRAMANA_CYBER_READINESS_REPORT_v1.md) and its status/demo/validation artifacts: repository-state baseline, reconfirmed here.
5. Supplied `PRAMANA_FINAL_CYBER_TEAM_HANDOFF_v1_FINAL2.md`: communication draft, reconciled in Appendix A; not a policy authority.
6. Other reports: supporting context only. The [Master Blueprint](PRAMANA_Master_Blueprint.md) remains the existing architectural plan under the frozen reconciliations.

Labels throughout: **IMPLEMENTED** = runnable code; **TESTED** = named passing cases, within their scope; **REPRESENTATIVE VALIDATION** = bounded real-source execution, not a benchmark; **SPECIFIED** = documented design without completed software; **DEFERRED** = a missing approved contract/input prevents implementation; **OUT OF SCOPE** = excluded from this MVP or prohibited by policy. A subsystem can have more than one label for different parts.

## 1. Project mission and thesis

PRAMANA addresses SIH PS 26151 through evidence discipline: source-backed, contestable, human-reviewed **pseudonymous** investigation. Thesis: “Attribution fails on the arithmetic of evidence, not on the shortage of it.” Independence, commonness and counter-evidence must be explicit before making an inference.

The current software demonstrates the deterministic foundation and an unscored review input. It does not identify real people, accept personas, establish operator identity or produce calibrated attribution. The planned ledger records sourced assertions and history; it does not make those assertions true and is not a blockchain.

## 2. System architecture

Preserve Blueprint §§5–10, 25, 29 and Cyber policy. The planned architecture is authorised collection → admission/validation → provenance-bearing observations/derivations → qualified evidence → independence/counter-evidence/resolution/fusion → assessment → human review. Graphs are views over evidence, not automatic merge graphs.

The planned prototype uses PostgreSQL 16, a Python/FastAPI backend, local content-addressed storage and the Blueprint's React/TypeScript frontend. Its Z1 collection, Z2 validation, Z3 analysis and Z4 presentation trust zones are **SPECIFIED**, not deployed by this repository. No new stack is introduced. The Blueprint names Python 3.12 for the backend; the present offline slice was tested on Python 3.13.7, without revising that plan.

Currently there are standard-library Python packages and command-line entry points, plus static HTML/JSON outputs. No running database/API, auth service, collector, learned model or investigator web application is part of the demonstrated path.

## 3. Current implementation status

| Subsystem | Status | Evidence and exact limit |
|---|---|---|
| Archive digest/member reading | IMPLEMENTED, TESTED, REPRESENTATIVE VALIDATION | `adapters/gwern_grams/archive_reader.py`, adapter runner, two-member validation; no demonstrated full-corpus memory bound. |
| CSV normalization/IDs/provenance/time | IMPLEMENTED, TESTED, REPRESENTATIVE VALIDATION | Parser/normalizer/models/identifiers; exact raw cells, atomic structural rejection, complete returned records and unknown times. |
| Exact repetition and source discrepancies | IMPLEMENTED, TESTED | `canonicalization/runner.py`, `cyber/review.py`; synthetic demo/fixtures. Older real sample reports are historical, not rerun canonicalization evidence. |
| SimHash/shingles/content digest | IMPLEMENTED, TESTED | `canonicalization/text_hashing.py`; heuristic comparison operands, not origin/identity decisions. Current real validation does not execute them. |
| Text spans / PGP-like markers | IMPLEMENTED, TESTED, REPRESENTATIVE VALIDATION | `cyber/indicators.py`; 8,794 text spans and one unvalidated marker. |
| Legacy Bitcoin format validation | IMPLEMENTED, TESTED | Synthetic/format vectors; zero lexical matches in the current real sample. No real-wallet validation claim. |
| Hub restriction | IMPLEMENTED, TESTED | `cyber/policy.py`; >12-account rule for supplied **Bitcoin Base58Check** associations and declared snapshot. Not a universal F1–F9 rarity service or automatic population qualification. |
| Clone restriction | IMPLEMENTED, TESTED | Externally declared occurrence/portion scope; no autonomous clone adjudication or general lineage propagation engine. |
| k<2 positive ceiling | IMPLEMENTED, TESTED guard | Supplied approved k=0/1 caps positive band at Weak. Actual k, scores and bands are not computed. |
| Counter-evidence | IMPLEMENTED, TESTED restricted handling; remainder DEFERRED/SPECIFIED | Seven check states, hub/clone restrictions, repetition/discrepancy notes. No complete seven-detector engine, numeric opposition or veto. |
| Offline review packet/HTML | IMPLEMENTED, TESTED | `cyber/review.py`, `cyber/render.py`, synthetic demo. Escaped static presentation; no persisted decision. |
| Evidence promotion/groups/resolution/fusion | DEFERRED | DC-01–DC-06; no authoritative evidence, group/k or completed assessment. |
| Persistent ledger/API/access/retraction | SPECIFIED, NOT IMPLEMENTED | Planned backend; exact promoted-row mapping also depends on DC-06. |
| F6/F7/F8/F9 generators, additional infrastructure methods | SPECIFIED / DEFERRED | Frozen modality rules plus DC-07–DC-09; no claimed implementation. |
| RANGE-SIM / RANGE-TOR / calibration | SPECIFIED / DEFERRED | No completed manifests, protected truth harness or outcome benchmark. |
| Real identity, automatic merge/acceptance, unauthorized collection, autonomous investigation | OUT OF SCOPE | No such outputs or actions in the slice. |

## 4. Cyber workstream

Cyber owns source qualification, semantic meaning, eligibility, counter-evidence interpretation, lawful boundaries and domain acceptance (CY-POL-001). ML/DE/PL/EV implement their assigned components; Cyber ownership is not ownership of all programming or numerical methods.

Frozen family names remain **F1 Cryptographic; F2 Financial; F3 Infrastructure; F4 Contact identifiers; F5 Content artefacts; F6 Linguistic style; F7 Behavioural/temporal; F8 Social/trust; F9 External corroboration**. Exact definitions and overlap precedence are CY-POL-006; no reinterpretation of F8/F9 as generative or “advanced” signals is allowed.

| Family | Current source/implementation boundary |
|---|---|
| F1 | PGP-like marker occurrences only. No key packet/signature verification. Unsigned public-key republication gives no positive F1 weight, not “one independent vote.” |
| F2 | Legacy Bitcoin format validator and lexical extraction; real bounded sample has no matches. Price currency is unknown; no transaction, ownership, co-spend or tracing output. |
| F3 | CSV link strings are references, not TLS/banner/descriptor telemetry or origin evidence. Controlled infrastructure work remains planned. |
| F4 | No implemented contact-ID extractor or verified contact-ID fixture for this CSV path. |
| F5 | Exact text spans and comparison operands; no validated non-boilerplate reuse evidence or image features. |
| F6 | Text may eventually feed gated style analysis; no model/gates currently executed. Tradecraft/SOP is not its definition. |
| F7 | Snapshot context exists, but no qualified event-driven scoring. Continuous rhythm/timezone inference is context-only under policy. |
| F8 | Co-vouching, endorsements, reciprocal trade links and moderator statements; no bounded generator/source contract implemented. |
| F9 | Qualified external corroborating statements; no generator/qualification/weighting path implemented. |

Clone-derived support is suppressed, not deleted. Suppression is not negative evidence. Missing fields are unavailable, not opposition. Changed vendor/source references are discrepancies, not handover proof. Hard vetoes remain outside numeric scoring; no eligible automatic veto detector is implemented.

## 5. AI/ML workstream

ML presently delivers deterministic extraction/validation, comparison operands and restrictions—not a trained model. The packet's ML-feature boundary contains derivation references; it does not mean embeddings, NER or style inference ran.

ML owns the eventual qualified evidence generator, origin grouping and approved numerical methods with Cyber interpretation and EV validation. Feature/LLM output cannot directly write `evidence`, `pair_score`, `assessment` or `must_not_link`, accept a persona or fabricate a missing value. Human approval alone does not resolve DC-06 or turn an unvalidated feature into evidence.

## 6. Data / acquisition workstream

DE supplies lawfully acquired, release-qualified bytes and acquisition provenance; source verification is not inferred from a report title. The actual root `grams.tar.xz` is pinned to SHA-256:

`0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6`

The prior adapter specification records 1,865 CSVs and 12,384,326 data rows from structure inspection. That is **not full application ingestion**. This consolidation reran only the two-member, 4,397-record application validation.

Raw schema: `hash, market_name, item_link, vendor_name, price, name, description, image_link, add_time, ship_from`, plus an empty eleventh header/value. Raw cells are strings; exact CSV parsing and normalization are distinct.

- `vendor_name` with exact source/market context identifies an observed account label, not a persona, actor or person.
- `hash` is an opaque source token, not a digest or guaranteed immutable listing ID.
- `item_link`/`image_link` are reference strings; image references may be opaque rather than URLs. No fetch or pixel analysis is performed.
- Some ancillary image bytes exist in the archive; the CSV-to-image join is unresolved. Image analysis is outside this adapter v1, not permanently outside PRAMANA.
- `price` is a parsed decimal string with unknown currency; no volatility or transaction inference.
- `add_time` parses only as a ten-digit integer where valid; epoch, units, timezone and meaning are unresolved. Observation, event, belief and assessment times remain distinct.
- `ship_from` is an unverified source claim, not actual location.
- Repeated snapshots/different datasets do not imply independence. Canonical listing and origin IDs remain unset.

OPUS provides acquisition context, not substitute source fields or blanket usage rights. CrimeBB and additional datasets are not implemented sources here.

## 7. Persistence / backend status

**SPECIFIED:** PostgreSQL evidence/history storage, APIs, access control, review persistence, graph projection and retraction. **DEFERRED:** exact authoritative evidence mapping/promotion under DC-06. Current in-memory dataclasses and JSON files are not a deployed append-only ledger, immutable database, chain of custody or blockchain.

PL may integrate the existing pre-promotion review representation while preserving its status and nulls. It must not silently map review items into authoritative evidence tables, manufacture group IDs or expose an accepted assessment just by changing labels.

## 8. Evaluation status

EV has executable mechanism/regression tests and bounded source replay evidence (§§12–13). These do not measure recall, precision, false merges, Cllr, calibration or leak-free full-corpus performance.

RANGE-SIM evaluates resolution/attribution/fusion; RANGE-TOR evaluates controlled infrastructure behaviour. Separate manifests, task labels, held-out truth and access boundaries remain required (CY-POL-028/029, OD-02). The current synthetic demo has no actor truth labels and is neither completed range. Public Grams labels must not become operator ground truth.

## 9. Frontend / demo status

The current frontend is an escaped, script-free static HTML view of generated JSON (`cyber/render.py`). It displays observations, comparison references, restrictions and competing propositions. It has no login, query API, graph app, signed export, persisted review, accepted persona or score.

FRONTEND should consume the existing packet as **review input**, preserve raw/provenance access and render unknown/deferred states. Do not invent percentage-match UI, independent-family counts or an “approve identity” control. Persistent analyst workflow is future PL/FRONTEND work under frozen review semantics.

## 10. Integration contracts and team ownership

RAW OBSERVATION → DETERMINISTIC DERIVATION → ML FEATURE → EVIDENCE CANDIDATE remains the boundary. Current execution supplies deterministic feature inputs and **blocks** the last transition. Evidence groups, hypotheses and assessments are separate concepts, not alternate names for indicators.

| Existing interface | Producer → consumer | Preserve / do not infer |
|---|---|---|
| `NormalizedRecord`, `record_to_dict` | Adapter → canonicalizer/indicator/review layer | Raw cells, exact account tuples, archive/member/row provenance, unknown times, nullable objects; adapter §16. |
| `RepetitionReference`, `CanonicalTextContent`, `NearDuplicateCandidate` | Canonicalizer → review/future grouping | Exact vs near-match distinction; source occurrences and `text-pair-json-v2` version. No canonical identity, origin adjudication or k. |
| `extract_indicators`, `verify_indicator_span` | Deterministic extraction → review/feature consumers | Typed occurrence, original field/span, validation/method and provenance. F1/F2/F5 labels are input eligibility. |
| `count_hub` | Declared qualified Bitcoin associations → policy restriction | Indicator/account/record/snapshot, eligible/rejected/quarantined/unknown, original/mirror/clone/unknown, decision reference; counts not corpus rarity. |
| `screen_indicator` | Traceable indicator plus scoped declarations → review item | Recompute validation, retain blockers/restrictions; no positive support or promotion. |
| `build_review_packet` | Bounded observations and declarations → static UI/future PL integration | Hypothesis/defence input, missingness, seven check states, null assessment/score, empty candidate/evidence arrays. |

These are local pre-promotion interfaces, not a newly frozen DC-06 SQL/API schema. Field-level detail: [demo contract](docs/cyber/PRAMANA_CYBER_DEMO_SCENARIO_v1.md#local-pre-promotion-contract).

**Provenance:** archive digest → member digest/name/ordinal → snapshot token → logical data-row number → original field → zero-based, half-open **Unicode code-point offsets** → derivation. Byte offsets are not emitted. Example verified PGP marker: `grams/2015-04-20/Abraxas.csv`, regular member ordinal 2, data row 4252, description column 7, span `[1214,1240)`. Its status is `unvalidated_pgp_material`.

Actual indicator ID structure is `["indicator", "cyber-indicators-v1", ["record", archive_sha256, member_ordinal, member_name, row_number], column_position, start, end, type]`; there is no invented compact `grams_..._row42` source key. Fixture IDs use their actual synthetic archive digest and synthetic account namespace.

| Role | Owns | Consumes | Produces | Dependencies | Must not modify/unilaterally decide |
|---|---|---|---|---|---|
| CYBER | Domain/source qualification, family meaning, lawful boundaries, acceptance | Verified observations, method proposals, EV results | Qualification/gate decisions, scenarios, domain review | Actual source evidence and documented authority | Frozen F1–F9, unresolved math, automatic identity acceptance |
| ML | Extraction, comparison, future grouping/generation/scoring | Qualified normalized inputs and frozen policy | Derivations/features now; versioned methods and candidates only after contracts | DC-01–DC-06/09, Cyber/EV sign-off | Raw facts, unknown times, advisory/promotion boundary |
| DE | Acquisition provenance, controlled collection and range generation | Approved targets/access and verified release contracts | Exact source bytes/manifests; future separate range inputs | Source permission, OD-01/02/04, Cyber/EV | Pinned source bytes/meaning or covert collection scope |
| PL | Persistence/API/access/review/retraction implementation | Existing review input and later approved evidence contracts | Stored lineage/review history and APIs when built | DC-06, OD-03/04; Cyber semantics | Empty/null states into scores or accepted evidence; destructive merges |
| EV | Test/evaluation design, validation, protected truth | Implementations, manifests and approved methods | Reproducible results, expected fixtures, future calibration evaluation | Separate range manifests, DC method definitions | Held-out truth into inference/UI; unmeasured benchmark claims |
| FRONTEND | Presentation and review interaction under PL access boundary | Authoritative API when built; current unscored packet now | Faithful visible provenance, alternatives and execution states | PL read/review interfaces; Cyber wording | Re-derived scores, unsupported status labels, automatic acceptance |

All roles preserve frozen policy/adapter contracts; changes require an explicit separately reviewed version, not an implementation convenience. These assignments restate CY-POL-001/032/033, not a new workstream architecture.

## 11. Current end-to-end executable path

The single primary demonstration is **synthetic tar/CSV bytes → deterministic normalizer → exact repetition analysis → source-span indicators → validation/restrictions → review JSON/HTML**. It needs no real archive.

`run_cyber_demo.py` calls `cyber.demo.make_demo`, uses the same normalization/extraction components in explicit fixture scope, and creates 18 occurrences/53 derivations. Its declared first-snapshot population has 13 eligible accounts for a synthetic Bitcoin-format reference. It explicitly declares B's description-derived clone scope; the equality detector does not make that decision.

Counter-evidence handling is demonstrated as common-indicator restriction, dependence awareness and explicit unavailable/unimplemented states—not a computed opposing score. The human can inspect competing propositions; no human decision is recorded by the software.

Real Grams validation is a **separate** bounded command. It verifies normalization/extraction/blocked promotion; it does not build a real-source review packet or run real-source canonicalization. Do not splice these two runs into an unsupported claim that the full real-data assessment path is implemented.

## 12. Verified test evidence

Consolidation rerun: **76 passed, 13 skipped, zero failed**, Python **3.13.7**, pytest **9.0.2**. [JUnit artifact](docs/cyber/validation/pytest.xml) records case-level results; no deep-archive opt-in was used.

| Test location | Verified scope |
|---|---|
| `tests/test_fixtures.py` | Default synthetic/fallback parser/normalizer cases; 13 old archive-seeking cases skipped, not passed. |
| `tests/test_adapter_regressions.py` | Atomic structural rejection, no returned-row loss, exact numeric grammar, escaped CSV newlines, malformed quotes, provenance serialization, digest framing. |
| `canonicalization/tests/test_canonicalization.py` | Exact/near comparison operands, repetition, Unicode/multiline input and determinism. |
| `tests/test_cyber_slice.py` | Source spans/checksum vectors, provenance tampering, 12/13 hub threshold, account deduplication, origin exclusions/unknowns, scoped clone restriction, discrepancies, no invented negatives/veto, supplied-k ceiling, deterministic packet and HTML escaping. |

A missing hard-veto implementation is tested to remain unavailable; this is not a positive EXCLUDED detector test. A scope-local restriction does not constitute a full counter-evidence engine or prove attribution improvements.

## 13. Verified real-data validation

The executed `python run_cyber_validation.py` produced [representative_validation.json](docs/cyber/validation/representative_validation.json), including code and source digests.

| Result | Observed |
|---|---:|
| CSV members | 2 |
| `grams/2014-06-09/1776.csv` records | 83 |
| `grams/2015-04-20/Abraxas.csv` records | 4,314 |
| Total normalized records / structural errors | 4,397 / 0 |
| Exact text spans / PGP-like markers | 8,794 / 1 |
| Span/payload replay checks / blocked-promotion checks | 8,795 / 8,795 |
| Bitcoin lexical matches in this sample | 0 |
| Validated evidence candidates / authoritative evidence / assessments | 0 / 0 / 0 |

This confirms bounded source compatibility and derivation replay. It proves neither memory-leak freedom, scaling, extraction accuracy nor operator attribution. The sample is the first two pinned members, not a random or representative-of-all-modalities sample. Bitcoin format tests must not be described as validated real Grams wallet findings.

## 14. Remaining P0 / P1 / P2 work

Priorities below are delivery triage, not new policy or permission to invent missing methods. The offline demonstration already runs.

| Priority / target | Owner and prerequisite | Acceptance artifact |
|---|---|---|
| P0 — integrated unscored review | PL + FRONTEND, Cyber semantics | Planned viewer/API with source replay, explicit blocked/null states and persisted reviewer notes; no promoted evidence shortcut. |
| P0 — any candidate-promotion claim | ML + PL + Cyber, EV; DC-06 and source/context qualification | Field-level promotion contract, permitted predicates, valid/invalid fixtures and provenance requirements. Until supplied, candidates stay empty. |
| P0 — any independent-support claim | ML + EV, Cyber; DC-01 | Origin/group/k decision table and expected quote/mirror/copy/cross-family fixtures. |
| P0 — any scored/veto/calibrated claim | ML + EV, Cyber/PL; DC-02/03/04/05 plus approved interfaces | Negative aggregation, LR/rarity, temporal application and hard-veto eligibility definitions; validated computation fixtures. No fallback constants. |
| P0 — any outcome benchmark claim | DE + EV, Cyber/ML; OD-02 and methods | Separate RANGE-SIM and RANGE-TOR manifests, evaluator-only truth boundary, partitions and reproducible results. |
| P0 — any operational deployment/collection claim | Cyber + DE + PL, EV; OD-01/03/04 | Qualified sources/authority, admission controls, roles/access, retention/retraction and controlled probe acceptance. |
| P1 — additional qualified modalities | ML/DE + Cyber/EV | Verified material and validators for PGP/contact/images; DC-07–DC-09 contracts before affected telemetry/generators/gates. |
| P1 — packaging/scalability | ML + PL + EV | Reproducible dependency/environment packaging, compatibility evidence, bounded-memory/bounded-comparison design within frozen contracts before large runs. |
| P2 — beyond-MVP roadmap | Assigned Blueprint owners after prerequisites | Only previously planned extensions; no prohibited technology or autonomy added for feature count. |

DC-01 grouping/k, DC-02 negative aggregation, DC-03 LR/rarity/grade, DC-04 decay/time, DC-05 veto, DC-06 promotion/schema, DC-07 infrastructure methods, DC-08 F8/F9 and DC-09 gates/windows all remain unresolved to the extent recorded in CYBER_SPEC_v1. Human review does not supply missing mathematics. Current in-memory retention and quadratic comparisons are visible engineering risks, not reasons to change the architecture.

## 15. Security boundaries

Current execution is local and offline. No fetch of untrusted URLs, Tor probe, exploit, credential bypass, private-key creation, chain query or external model/service occurs. Static rendering escapes source text; it is not a general sandbox, source admission scanner or deployed Z1–Z4 enforcement system.

No LLM/ML/direct adapter write to authoritative evidence, pair scores, assessments or must-not-link exists. Unknown/unrun checks remain visible; declarations of population/clone qualification are caller inputs, not authenticated operational adjudications. No automatic merge/accepted persona or real-person output.

## 16. Legal / ethical boundaries

All work remains within authorised public/historical, synthetic or controlled environments. Public availability does not establish unrestricted use or source truth. Acquiring the pinned archive does not automatically prove rights for every component; Cyber/DE retain qualification responsibility.

No blanket claim that software identifies only illicit actors or automatically vets all subjects is supported. No unauthorised collection, live real-marketplace crawling for the MVP, mass enumeration, targeting private individuals or autonomous investigation. Controlled authorised RANGE-TOR work remains planned; Tor use is not categorically forbidden by this handoff. Monero tracing is out of scope; observing a source-present XMR address is allowed by policy but unimplemented here.

## 17. SIH judge claims and Q&A

**30-second answer:** “PRAMANA is designed to make investigative links show their sources, dependence and alternatives. Our working offline slice normalizes archived-style data, derives traceable indicators and displays repetition and scoped restrictions without accepting an identity. We passed 76 tests and replay-validated 4,397 real-source records. Scoring and evidence promotion remain deferred; today's output is an auditable review input.”

**Two-minute extension:** Show Account-A and Account-B's distinct source occurrences; open exact text spans and member/row provenance. Show equality references without a same-operator decision. Explain the explicitly supplied B-clone declaration and Bitcoin-format hub population, then show missing information and unimplemented counter-checks. End on empty evidence candidates and null assessment. Say “this is where approved promotion and grouping methods must connect,” not “the human approves a machine attribution score.”

| Judge question | Defensible answer |
|---|---|
| What runs today? | Offline normalization, repetition operands, typed derivations, validation/restrictions and review export. |
| Did you identify a person? | No; no real-world identity output or accepted persona. |
| Is the evidence ledger deployed? | No; it is specified. Present outputs are JSON/HTML and source fixtures. |
| Is the ledger a blockchain? | No. The planned append-only software ledger is not a blockchain. |
| Did you process all 12.3M rows? | No full application ingestion. Current real validation processed 4,397 rows; prior structure inspection is separate. |
| What is your accuracy/false-merge rate? | Unmeasured; tests are mechanism checks, not attribution benchmarks. |
| Did memory use scale without leaks? | No such measurement. Records are retained and comparisons can be quadratic. |
| What does a repeated PGP marker prove? | Only repeated wording. Even unsigned public-key republication has no positive F1 weight. |
| Are signatures verified? | No; marker recognition is not cryptographic validation. |
| Are Bitcoin addresses owned by these accounts? | No ownership inference. Legacy Base58Check format validation only; no real sample match. |
| What actually triggers the shown hub restriction? | More than 12 distinct eligible accounts in a supplied snapshot population for the validated Bitcoin-format indicator, not templates generally. |
| Does equal text automatically become a clone? | No. Equality is an operand; this demo separately declares B's clone scope. |
| Are all negative checks running? | No; seven states are displayed. Only narrow restrictions/review handling execute, with unimplemented checks visible. |
| How do you derive k or LR? | We do not; DC-01–DC-06 definitions/fixtures are required before the relevant computations. |
| Are offsets bytes? | No: Unicode code points in decoded source cells, with archive/member integrity references. |
| Are URLs infrastructure evidence? | No; this CSV path supplies references, not measured service telemetry. |
| Are images permanently excluded? | No; current CSV-to-byte joins/features are absent; separately qualified image work is planned. |
| Are RANGE-SIM and RANGE-TOR implemented? | No. They remain separate planned evaluation domains, not names for today's synthetic demo. |
| Do you use a graph database or GNN? | No. The planned prototype uses PostgreSQL graph views/traversal; separate graph engines/GNNs are not the MVP. |
| Does a reviewer click make evidence valid? | No. Source, validator, proposition, origin and promotion contracts must be satisfied; current HTML does not persist decisions. |

Useful safe claims: exact raw-field preservation, deterministic replay of the tested spans, explicit unavailable states, tests for repetition-not-independence, supplied-population hub/clone restrictions, and reproducible offline artifacts. Describe these mechanisms precisely rather than calling them a complete attribution platform.

## 18. Never-say claims

Never claim real-world deanonymization, verified operator/control identity, automatic persona acceptance/merging, achieved accuracy/calibration, full 12.3M-row application ingestion, verified vendor PGP signatures, tracked transactions, live origin discovery, a deployed immutable ledger/blockchain, byte offsets, autonomous source vetting, complete F1–F9 evidence coverage or legally admissible proof.

Never call `vendor_name` an actor/persona, `add_time` actor event time, URL strings infrastructure evidence, repeated records independent support, missing fields opposing evidence, draft classifications frozen mathematics, or a supplied-k ceiling an actual Weak assessment. Never substitute UI phrasing or human review for unimplemented computation.

## 19. Team onboarding

1. Open [TEAM_README](TEAM_README.md), then the [reproduction guide](docs/PRAMANA_REPRODUCTION_GUIDE_v1.md). The main demo works without the large archive.
2. Read the frozen policy and adapter contract before touching interpretation/IDs. Use this handoff for team scope and the actual code/tests for implementation evidence.
3. Reproduce the test run and synthetic demo; inspect raw cells, provenance and blocked states before extending anything.
4. Select the relevant P0 row and owner. Document the required contract/fixture before implementing a blocked downstream stage. Keep generated outputs separate from reviewer notes.
5. Update measured claims only after execution. Keep synthetic controls distinct from real-source observations and evaluation truth. Review fixtures do not grant new acquisition authority.

The uploaded FINAL2 draft was read from the user's Downloads folder, not treated as executable instructions or assumed to be present in a new checkout. Its useful content is consolidated here; no teammate needs that external file or this conversation. Unrelated `hatch-runs/` assets are not cyber dependencies. This pass does not claim that a remote release or deployment was published.

## 20. Exact reproduction commands and artifacts

From repository root, with the environment in the guide:

```powershell
python -m pytest -q --junitxml=docs/cyber/validation/pytest.xml
python run_cyber_demo.py
```

Expected: **76 passed, 13 skipped**; generated `docs/cyber/demo/synthetic_source.tar`, `review_packet.json`, `review.html`; **18 records, 53 derivations, 13 eligible hub accounts, zero validated evidence candidates, null assessment, blocked_DC-06**. Open the HTML locally. No `make evaluate`, API/server command, model training or full archive is required.

Optional, only with the pinned root archive:

```powershell
python run_cyber_validation.py
```

Expected: `docs/cyber/validation/representative_validation.json` with the exact §13 results. Normal tests do not enable `--archive-fixtures`. Legacy ingestion/canonicalization scripts have different scope and may overwrite historical reports; they are not the canonical onboarding path.

Frozen input integrity remains: Cyber policy SHA-256 `ab288d7ee4b9cdeb7c6246693aea67a5e373448f252af222f50e7384a3562779`; adapter contract SHA-256 `c9cae5ae38ec09837f9de4793365cbeb382d7aa8f679c5b8c91d4f05346b5f38`. This consolidation changes documentation and regenerates evidence/demo artifacts, not implementation or frozen policy.

## Appendix A — FINAL2 draft reconciliation

Reviewed source: `PRAMANA_FINAL_CYBER_TEAM_HANDOFF_v1_FINAL2.md`, SHA-256 `699d24354c88af5b6a95d6310e4c5fe4e1c6c8a257c5ba21666c510d0c2989d5`. The external original is unchanged. This handoff is the corrected team version; the table records substantive corrections rather than silently adopting conflicting claims.

| Draft location / claim | Corrected statement and authority |
|---|---|
| Header: frozen authoritative repository state | Draft is communication context; policy, data contract and code/tests have higher authority. |
| §§2/13/14: Cyber owns fusion/math; PL alone owns candidates; human produces a final pair score | ML methods/generation, Cyber domain acceptance, PL interface/persistence, EV validation and analyst review are separate; CY-POL-001/010/013/032/033. |
| §2: checksum validation in deferred candidate stage | Checksum validation is implemented derivation; candidate promotion is deferred. `screen_indicator` emits review items, not replayed evidence candidates. |
| §§3/11: streams without OOM, proves no leaks | Bounded compatibility/replay only. Adapter/canonicalizer retain records; no memory/scalability measurement. |
| §3: Bitcoin real-data validation; current SimHash real validation | Bitcoin: tests only, zero sample matches. Current real validator does not execute canonicalization/SimHash. Historical comparisons are labelled historical. |
| §§4/5: image links only URLs; image bytes/pixel work globally out of scope | Opaque references also exist; some ancillary bytes exist, CSV join unresolved. Only this adapter v1 excludes image processing. Adapter §§3/5/11/19. |
| §5: price linkage excluded due to volatility; raw add_time integer | No measured volatility claim. Raw cells are strings; decimal/integer parsing is derived, currency/time meaning unknown. |
| §6: flattened invented source ID; §§12/16: byte offsets/every byte replay | Nested tuple IDs and decoded-cell code-point spans, validated against available source/member bytes. No byte-offset or universal byte-replay feature. |
| §7: equal text emits NearDuplicateCandidate; prevents measured score inflation | Exact equality emits `exact_content_match`; near comparisons are separate. No scorer/ablation establishes measured prevention. |
| §8: F6 tradecraft/SOP; F8/F9 generative/advanced | Preserve CY-POL-006: linguistic style, social/trust, external corroboration respectively. No new taxonomy. |
| §§9/16: >12 hub qualification and templates suppressed | Qualification is caller-supplied. Current helper validates Bitcoin Base58Check associations; not a general template/PGP hub service. |
| §16: marker across 20 markets is one independent evidence item | Marker is no verified crypto evidence; unsigned public key reuse has no positive F1 weight. Grouping remains DC-01. |
| §16: cloned texts automatically trigger restriction | Restriction requires the externally declared occurrence-specific clone reference; equality does not adjudicate it. |
| §§13/15/17: human oversight alone explains/resolves promotion/math deferral | Explicit missing contracts and validation are blockers; review alone cannot supply them. |
| §16 Q&A: deployed append-only poisoning handling, anomalies are counter-evidence | Ledger not implemented; source discrepancies are review notes, not automatic negative evidence. |
| §16 Q&A: all Tor collection/Monero capability out of scope; graph DB specified | Authorised RANGE-TOR is planned; XMR observation allowed but unimplemented, tracing excluded; MVP uses PostgreSQL, not a separate graph DB. |
| §16 ethics: platform only targets illicit actors via vetted streams | No implemented automatic vetting/subject classification. Preserve lawful scoped source qualification, not an unsupported guarantee. |
| §16 incomplete numbered question placeholders | Replaced by 20 concrete, repository-grounded answers without pretending additional Q&A exists. |
| §§17/19: ledger replay/completed full vertical-slice language | Offline pre-promotion review path only; exact tests/real validation stated, all downstream gaps retained. |

Useful thesis, team integration intent, staged demo language, test counts, limitations and judge-facing format are preserved with these corrections. The three final package documents are sufficient for immediate team onboarding without external draft access.
