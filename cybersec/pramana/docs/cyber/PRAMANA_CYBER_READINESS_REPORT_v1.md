# PRAMANA Cyber Readiness Report v1

Date: 2026-09-09 · CYBER_READINESS_v1. **Ready for an offline, auditable cyber mechanism demo. Not ready to claim completed attribution, evidence fusion or a production intelligence platform.**

## 1. Implemented capabilities

- `adapters/gwern_grams/`: pinned archive hashing, CSV normalization, exact raw values, scoped accounts, provenance and unknown-time handling. This pass repairs atomic member rejection, strict malformed-quote parsing, numeric trailing-newline acceptance, lost returned rows and omitted acquisition fields.
- `canonicalization/`: exact row/content/source-reference comparisons and existing near-match heuristics. SHA-256 content framing is now `text-pair-json-v2`; no delimiter collision or null/empty ambiguity. No canonical-origin adjudication or identity merge.
- `cyber/indicators.py`: exact title/description spans, PGP-like markers, legacy Bitcoin Base58Check validation, deterministic IDs, lineage validation and tamper rejection.
- `cyber/policy.py`: declared-snapshot hub counting, occurrence-scoped clone/hub restrictions, supplied-k ceiling and blocked promotion. Requires externally qualified inputs; no scorer.
- `cyber/review.py`, `cyber/render.py`, `run_cyber_demo.py`: pseudonymous hypothesis/defence input, repetition/discrepancy notes, seven counter-check states, JSON and escaped offline HTML.

## 2. Tested capabilities

Command: `python -m pytest -q --junitxml=docs/cyber/validation/pytest.xml`.

**76 passed, 13 skipped, zero failures**, Python 3.13 / pytest 9.0.2. [JUnit results](validation/pytest.xml) contain actual outcomes. The skipped tests are older deep-archive fixtures; no passing claim is made for those in this run. Default tests are offline and bounded; deep archive fixtures require opt-in.

Coverage includes raw preservation, malformed input rejection, returned-record integrity, deterministic repetition, 12/13-account boundaries, population exclusions/unknowns, clone scope, no automatic negatives/handovers, k-ceiling-only semantics, no invented veto, Bitcoin format vectors, Unicode spans, spoofed provenance/derivation/hub rejection, reproducible demo output and hostile-text escaping. These tests demonstrate mechanisms, not attribution accuracy.

## 3. Representative validation

Command: `python run_cyber_validation.py`. [Validation JSON](validation/representative_validation.json) records archive/member and code digests.

| Measured in the bounded run | Result |
|---|---:|
| CSV members | 2 |
| Normalized records | 4,397 |
| Structural errors | 0 |
| Exact text-span derivations | 8,794 |
| PGP-like markers | 1 |
| Span/payload replay checks passed | 8,795 |
| Blocked-promotion checks passed | 8,795 |
| Bitcoin lexical matches in sample | 0 |
| Validated evidence candidates / assessments | 0 / 0 |

Members: `grams/2014-06-09/1776.csv` (83 records) and `grams/2015-04-20/Abraxas.csv` (4,314). The PGP-like example remains damaged/unvalidated. No real-source checksum-valid wallet finding is demonstrated. Bitcoin validation is supported by synthetic/format tests; previously reported corpus-wide lexical substrings were not rescanned or promoted to verified wallets.

The old 25,000-record ingestion and 15,000-record canonicalization reports remain historical evidence with correction notices. Their counts were not rerun at those scales; “perfect”, “no blockers” and full-corpus streaming assertions are not current acceptance evidence. The canonicalizer's repeated-market-item-link comparison concerns listing URLs, not image URLs.

## 4. Specified but unfinished

CY-POL-002/025/030–033 and Blueprint §§5–10/14/25/28 require operational source qualification, admission/sealing, persistence/access control, append-only review history, retraction propagation and assessment APIs/exports. Static HTML/JSON does not implement these services. Hashing is not a custody hash chain or admissibility guarantee.

PGP packet/signature validation, verified contacts, image-byte joins/features, event-qualified F7, qualified F6 detectors and complete counter-evidence execution are absent. Their unimplemented states remain visible.

## 5. Intentionally deferred

| Contract | Missing authority / next delivery |
|---|---|
| DC-01 | Complete origin grouping, cross-family dependence and eligible k: ML method + EV expected-key/contribution fixtures. |
| DC-02 | Negative sign/magnitude, aggregation and effect interactions: ML contract + EV cases. |
| DC-03 | Per-signal LR, source-grade effects and rarity: ML definitions + EV population/validation basis. Hub threshold alone is insufficient. |
| DC-04 | Decay/time anchors: ML method + EV boundary fixtures; Cyber validates clocks. |
| DC-05 | Temporal hard-veto eligibility: Cyber/ML decision table + EV logical-incompatibility and ordinary-overlap controls. No EXCLUDED emitted. |
| DC-06 | Evidence-row promotion/nullability/group ownership/segmentation: ML/PL interface + EV payload fixtures. No validated evidence candidates emitted. |
| DC-07 | Unspecified infrastructure methods: DE observable/method contract + controlled EV fixtures. |
| DC-08 | Bounded F8/F9 generation/qualification: Cyber/ML/EV contract. |
| DC-09 | Remaining feature gates/event windows: ML method + EV controls. |

Grams structure now has release-specific verification, but OD-01 operational use/acquisition qualification and CrimeBB remain separate. OD-02 range manifests, OD-03 retention and OD-04 executable admission/probe contracts remain unfinished. RANGE-SIM and RANGE-TOR were not built/evaluated here. Public labels are not actor truth.

## 6. Current end-to-end demo path

**Synthetic CSV bytes → normalized observation → repetition operands → deterministic indicator → exact validation/restrictions → provenance-backed review input.**

The [demo scenario](PRAMANA_CYBER_DEMO_SCENARIO_v1.md) documents 18 occurrences, 53 derivations with F1/F2/F5 eligibility labels, a declared 13-account hub population, scoped clone restrictions, discrepancies and missingness. These are not three independent supporting families. Promotion is blocked and assessment remains null.

The same extractor runs on actual normalized Grams records in the bounded validation. The requested validated-evidence → fusion → assessed-attribution path is not complete; the demo stops visibly at the authorised boundary.

## 7. Major remaining engineering tasks

1. Cyber/ML/PL freeze DC-06's narrow promotion interface and source/context qualification fixtures. Format validity alone cannot establish a qualified comparison proposition.
2. ML/EV finish DC-01's origin/quote/mirror fixtures before independent-family counting. Repetition references are inputs, not a grouping engine.
3. PL expose these exact observations/restrictions/provenance in the planned viewer and persist human-review notes/history. Do not rename the static packet an accepted assessment.
4. DE/EV select separate RANGE-SIM/RANGE-TOR manifests, isolate truth and implement controlled evaluation. This source-only synthetic demo has no hidden actor labels and is not a calibration corpus.
5. Resolve LR/counterweight/decay methods before fusion/calibration. Add telemetry only through existing controlled infrastructure contracts.

## 8. Security and collection boundaries

Local historical/synthetic processing only: no URL fetch, Tor access, bypass, exploitation, external datasets, private-key generation, blockchain queries or autonomous investigation. HTML has no scripts and escapes source text. No authoritative evidence/score/assessment/must-not-link database writer exists in this slice.

Operational authorisation, screening, roles/access, retention and custody/retraction remain unimplemented services. Archive hashing establishes byte identity, not source authenticity, usage rights or statement truth. The source archive remains at repository root, as recorded by the adapter specification.

## 9. Evaluation methodology

Keep these levels separate:

1. **Mechanism tests:** synthetic/adversarial fixtures with explicit expected lineage/restrictions; code behaviour only.
2. **Representative source validation:** two named, digest-pinned CSVs with observed formats and replay checks. This is not a random corpus sample or an extraction precision/recall benchmark.
3. **Future outcome evaluation:** separate RANGE-SIM resolution/fusion and RANGE-TOR infrastructure tasks with partitioned truth, frozen predictions and approved metrics. No accuracy, Cllr, false-merge rate or calibration is measured now.

The 12,384,326-record corpus count comes from the prior adapter specification's verification. No full-corpus ingestion or new large reconnaissance was performed in this pass.

## 10. Exact claims safe for SIH judges

- “We can reproduce normalized Grams observations and trace deterministic indicators to original CSV fields and row provenance.”
- “Our offline fixtures enforce that repeated records, copied content and missing information do not automatically become independent support or negative evidence.”
- “We implement the frozen >12 eligible-account hub restriction and occurrence-scoped clone restrictions using explicit qualification inputs.”
- “Our synthetic review demo exposes competing explanations and unimplemented checks; it does not claim an attribution score.”
- “This run passed 76 tests, skipped 13 older archive fixtures, and separately validated 4,397 real-source records.”

## 11. Claims that must NOT be made

Do not claim real-person identification, automatic persona acceptance, verified ownership/control, complete F1–F9 coverage, solved origin grouping, real Grams wallet findings from this sample, verified PGP signatures, live infrastructure discovery, source admission/sealing, production review controls, full-corpus scalability, numerical counter-evidence/fusion, calibrated confidence, accuracy or forensic admissibility.

Do not call review items validated evidence candidates or the demo a RANGE-SIM benchmark. Do not pool RANGE-TOR infrastructure truth with actor labels. A Weak ceiling at k=1 is not a Weak assessment; no positive result was computed.

## 12. Highest-risk technical gaps

| Risk | Containment / remaining work |
|---|---|
| Valid-looking identifier misinterpreted | Format checks separate, promotion blocked; context/ownership alternatives and source qualification still required. |
| Common origin counted repeatedly | Repetition exposed; no grouping/k/scoring. DC-01 is the critical downstream blocker. |
| Caller declarations mistaken for adjudication | Population and clone references visible; no operational decision authentication or automatic origin adjudication claimed. |
| Unknown times turned into behaviour | add_time remains UNKNOWN/UNRESOLVED; F7/veto unavailable. |
| Scaling beyond samples | Adapter retains normalized results; canonicalizer stores records and can emit quadratic pairs. No full-corpus performance claim. |
| Review/custody persistence | Offline exports only; PL access/history/screening/retraction services needed. |

## Final acceptance answers

1. **Executable:** bounded normalization, exact repetition, text/PGP-marker extraction, Bitcoin format validation, provenance checks, declared hub/clone restrictions, supplied-k ceiling and offline review export.
2. **End-to-end demo:** synthetic source bytes through a replayable, pseudonymous, unscored review input; real-source extraction separately demonstrated on two CSVs.
3. **Tested:** 76 passing tests; 13 explicitly skipped archive tests; 8,795 real-source derivations replayed.
4. **Only specified:** full ledger/backend, source/admission services, persistent analyst review/retraction, additional modalities and ranges.
5. **Deferred:** DC-01–DC-09 and outstanding operational/data contracts. No scoring, grouping or veto defaults invented.
6. **Smallest remaining work for a convincing SIH prototype:** the offline review already works. For integration, PL needs the planned viewer with these exact provenance/restriction objects and persisted reviewer notes. For validated candidate-generation claims, first freeze DC-06 and source/context acceptance fixtures. Scored attribution additionally needs DC-01–DC-05 and evaluation; adding a score field cannot replace them.

**Frozen policy unchanged:** CYBER_SPEC_v1 SHA-256 `ab288d7ee4b9cdeb7c6246693aea67a5e373448f252af222f50e7384a3562779`. Adapter specification and F1–F9 taxonomy unchanged. IMPLEMENTED, TESTED, SPECIFIED and DEFERRED remain separate.
