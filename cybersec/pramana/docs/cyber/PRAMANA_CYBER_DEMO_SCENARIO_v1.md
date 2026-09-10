# PRAMANA Cyber Demo Scenario v1

Version: CYBER_DEMO_v1 · 2026-09-09. Offline synthetic mechanism demonstration, governed by CYBER_SPEC_v1 and the Grams adapter contract. This is a reviewable investigation input, not an accepted assessment or RANGE-SIM benchmark.

## Run and inspect

From the repository root, using Python 3.13 (tested) and pytest 9.0.2 for tests:

```powershell
python run_cyber_demo.py
python -m pytest -q
```

Open [offline review](demo/review.html). The same command generates its [JSON packet](demo/review_packet.json) and [synthetic source archive](demo/synthetic_source.tar). Application code uses the standard library. It fetches no URLs/images and calls no model, database or service. HTML is static, escapes source text and makes no acceptance decision.

Optional bounded real-source verification:

```powershell
python run_cyber_validation.py
```

This hashes the compressed root archive, then reads only its first two CSV members: 4,397 records. Do not substitute a full ingestion command. The older tests' `--archive-fixtures` option can seek deeply through the archive and was not used in this pass.

## Scenario

The reviewer compares **Market-A / Account-A** and **Market-A / Account-B**. The question is whether their catalogue material warrants further lawful investigation of shared operation. The defence proposition is separate operators sharing public identifiers, templates or copied listings. Neither is accepted by the software.

The synthetic source has 18 occurrences across two labelled snapshots:

- A listing from Account-A contains catalogue text, a synthetic checksum-valid address-format reference and damaged PGP-like wording. No private key, blockchain activity or address ownership is generated.
- Account-B has identical title/description with a different listing token and URL. Equality produces repetition references, not copying direction or common-operator proof.
- Twelve separately named population-control accounts contain the same address-format reference. With Account-A, the declared first-snapshot population contains 13 eligible observed accounts. These are fixture declarations, not inferred operators or application-authored source qualifications.
- Account-A's listing repeats in a second snapshot. It retains separate provenance without becoming independent support. The first snapshot's hub restriction is not extrapolated to the second.
- A source token appears with Account-C; a listing URL appears with another source token. Both become review discrepancies, not handover or canonical listing identity.
- Another occurrence lacks a description: unavailable information, not opposing evidence.

An **explicit synthetic review declaration** marks only Account-B's description-derived occurrences as copied from Account-A. The fixture supplies this decision; equality detection does not make it. Those occurrences get clone restrictions and remain traceable. Account-A's original remains intact. Without the declaration, equality is only a comparison operand.

The address is reproducibly encoded from a fixed synthetic payload in `cyber.demo.synthetic_address()`. It is a format fixture, not an actor address or a claim of non-use on a public chain. Production extraction never manufactures addresses. `add_time` remains UNKNOWN/UNRESOLVED; directory dates are source labels, not actor events.

## Demonstrated stages

| Stage | Result | Boundary |
|---|---|---|
| RAW OBSERVATION | Reproducible synthetic tar and 11-cell CSV rows | Synthetic namespace and actual fixture digest; never masquerades as the real Grams archive. |
| NORMALIZED OBSERVATION | 18 source occurrences with scoped accounts, raw cells, unknown times and row provenance | No persona/actor or stable-operator assertion. |
| CANONICALIZATION / REPETITION | Exact rows/content/source-reference comparisons and discrepancy notes | No canonical-origin assignment or identity resolution; near-match heuristics are unnecessary here. |
| DETERMINISTIC INDICATOR | 53 derivations with F5 text, F1-related PGP-marker and F2-related address-format labels | Three eligibility labels, not three validated supporting families. |
| ML FEATURE boundary | Derivation IDs exposed as deterministic feature inputs | No learned model runs or self-promotes. |
| VALIDATION / RESTRICTIONS | Span replay, checksum checks, scoped clone and >12-account hub restrictions | Format validity is not ownership. |
| EVIDENCE CANDIDATE | Empty; promotion explicitly blocked | DC-06 and source/context/origin qualification remain incomplete. |
| INDEPENDENCE / COUNTER-CHECKS | Repetition operands and all seven check states; common-indicator suppression executed | Full origin grouping/k, numerical opposition and hard-veto detection deferred. |
| REVIEW INPUT | Competing propositions, subjects, population, limits and replayable provenance | `assessment=null`, `score=null`, `awaiting_human_review`; no completed review claimed. |

## Five-minute walkthrough

1. Read the synthetic/unscored status before presenting any identifier.
2. Open the two accounts' raw cells and show field offsets plus archive/member/row provenance.
3. Show repeated observations and equal text remaining separate occurrences with no independent votes.
4. Show the declared hub population: 13 distinct eligible accounts, restriction only. Tests show 12 does not trigger, repeat mentions do not add accounts, and mirrors/clones/rejected observations are excluded.
5. Inspect B's scoped clone restriction, the preserved original, source discrepancies and missing information. Show the counter-check states; unimplemented is not clean.
6. End at the blocked promotion boundary and explain the missing contracts before any numeric assessment.

## Executable fixtures

| Requirement | Test in `tests/test_cyber_slice.py` / expected result |
|---|---|
| Repeated snapshots | `test_repeated_snapshot_not_independent`: separate occurrences, null group/k. |
| Copied content | `test_copied_content_not_same_operator`: equality only; explicit clone declaration tested separately. |
| Changed vendor / URL collision | Parameterized discrepancy test: review only, no handover, counterweight or listing collapse. |
| Damaged PGP | `test_damaged_pgp_not_f1_evidence`: no repair, fingerprint or positive F1. |
| Missing fields | `test_missing_field_not_negative`: unavailable, not opposition. |
| Hub/commonness | 12/13 boundary, repeated mentions, origin exclusions, unknown population, mixed snapshot and tampered-result tests. |
| Hard contradiction | `test_hard_contradiction_not_invented`: no EXCLUDED because DC-05 is unresolved. A positive EXCLUDED fixture is deferred. |
| k<2 | Ceiling-only guard gives Weak maximum for supplied approved k=0/1; no band assignment, score or exclusion. Actual eligible k stays unknown. |
| Provenance | Member-byte replay, exact payload checks, Unicode offsets, malformed lineage and tampering tests. |

Additional regression fixtures cover structural member rejection, exact numeric grammar, complete returned records, digest framing and HTML escaping. No synthetic fixture is claimed to be an observed Grams fact.

## Local pre-promotion contract

This is an in-process derivation/report format, **not** the unresolved DC-06 evidence-row or database/API contract. It adds no tables.

| Object / field | Meaning |
|---|---|
| `indicator.id` | `[indicator, cyber-indicators-v1, source_record_id, column_position, start, end, type]`; deterministic, no random ID. |
| `raw`, `field_ref`, offsets | Exact decoded source substring; zero-based half-open Unicode code-point offsets. Source columns remain one-based: name=6, description=7. No byte-offset claim. |
| `type` | `text_content`, `pgp_like_marker`, `bitcoin_base58_lexical`; checksum success does not change a lexical occurrence into ownership. |
| `validation` | Exact-span status, unvalidated PGP material, or explicit Base58Check outcome. Failure is not negative identity evidence. |
| `eligible_family` | F5/F1/F2 input eligibility. Whole-text and contained-marker interpretations cannot add duplicate support. |
| `value_sha256` | Exact UTF-8 substring digest; comparison/integrity operand, not canonical origin. |
| `provenance` | Archive/member digests, exact path/ordinal, row, snapshot and schema; observation remains separate from derivation. |
| `canonical_artefact_id`, `independence_key` | Null; no inferred grouping. |
| `promotion_review_items` | Replay-validated derivations with blockers/restrictions; not validated evidence candidates. |
| Evidence arrays | `validated_evidence_candidates=[]`, `authoritative_evidence=[]`; no storage writers. |
| Hub association | Exact indicator/account/record/snapshot, validation, eligibility, origin state and external decision reference. Reject mixed snapshots/indicators. Unknown qualification prevents a definitive non-hub result. |
| `hub_check` | Declared snapshot, included/excluded/unresolved associations, deduplicated account/site counts and replayable >12 restriction; no rarity formula. |
| Clone declaration | Nonempty external decision reference for an exact indicator occurrence; no inferred clone status or propagation beyond that portion. |
| `counter_checks` | Seven CY-POL-026 classes with visible execution states and effect; no numeric counterweight. |
| `hypothesis_input` | Two source-observed account subjects, competing propositions, time limits and reference population. |
| `assessment`, `score` | Null; no LR, confidence or calibration. |

**Validator limits:** Bitcoin legacy mainnet Base58Check length/version/double-SHA256 only; Bech32, XMR and other formats unsupported. ASCII alphanumeric token boundaries avoid extracting parts of longer tokens, potentially missing candidates in damaged text. PGP discovery recognizes case-sensitive BEGIN wording with optional existing dashes; it does not restore armour, parse packets or verify signatures. Contacts, F3 telemetry, F6 style, F7 events and F8/F9 generators are explicitly unsupported. No precision/recall claim.

**Owners:** Cyber accepts meanings/source qualification; ML owns extractor and eventual promotion/grouping; DE owns acquisition/population manifests; PL owns eventual access/persistence/review history; EV owns fixtures/evaluation. Fixture eligibility and clone declarations are not an operational adjudication service.
