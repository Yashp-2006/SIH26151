# PRAMANA_CYBER_INTELLIGENCE_SPEC_v1

**Policy / domain layer only**  
**Version:** CYBER_SPEC_v1  
**Date:** 2026-09-08  
**Status:** Frozen policy baseline; computational and data dependencies remain explicitly deferred.  
**Accountable domain owner:** The sole PRAMANA Cybersecurity / Threat-Intelligence owner (Cyber).

This document specifies evidence meaning, eligibility, provenance, collection boundaries and engineering responsibilities. It is not a numerical scoring specification, database migration, dataset verification report or statement that a capability is implemented. Rule compliance requires implementation and fixture evidence; publication of this document does not demonstrate compliance.

## Authority and interpretation

| Reference | Source | Application |
|---|---|---|
| S | [PRAMANA_SIH_PS_26151.txt](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA_SIH_PS_26151.txt) | Supplied SIH requirement and separately labelled PRAMANA interpretation boundary. |
| B | [PRAMANA_Master_Blueprint.md](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA_Master_Blueprint.md) | Controlling project source wherever it has an explicit rule. |
| M | [PRAMANA_AI_ML_Module_Dataset_Plan_v2.pdf](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA_AI_ML_Module_Dataset_Plan_v2.pdf) | Supporting workstream/data mapping; subordinate to B. |
| D | [PRAMANA_Technical_Project_Dossier.pdf](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA_Technical_Project_Dossier.pdf) | Supporting explanation; subordinate to B. |
| R | [PRAMANA Dataset Intelligence Report.txt](<C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA Dataset Intelligence Report.txt>) | Candidate dataset mappings, not proof of archive fields. |
| 2A / 2B / 2C | Source-of-truth audit and design decisions in the originating project conversation | Explicit reconciliation decisions incorporated below. They are not independent empirical verification. |

The specific reconciliations are recorded here so another engineering team does not need the originating conversation. Unresolved contradictions are not resolved by silent implementation defaults.

**Reading the rule fields:** INPUT and OUTPUT describe logical contract contents, not newly asserted dataset columns or new database tables. SUPPRESSION CONDITION describes eligibility restriction; collection rejection, feature non-computation and evidence suppression remain distinct operations. COUNTER-EVIDENCE CONDITION never supplies an unstated penalty or automatic veto. "None automatic" does not mean a contradiction check passed. OWNER identifies delivery responsibility and domain/evaluation review roles.

**Execution-state vocabulary:** Unimplemented, not run, failed, inconclusive and completed with no finding are distinct logical outcomes. These names are not a prescribed database enum. Only the last outcome can support a claim that the specified check ran without finding its target condition.

## 1. Cyber workstream scope and ownership

- **RULE_ID:** CY-POL-001
- **RULE:** Cyber owns source qualification, cyber semantics, evidence eligibility, threat interpretation, lawful boundaries and domain acceptance. DE owns acquisition, range generation and infrastructure collection; ML owns analytical implementation; EV owns evaluation and method validation; PL owns persistence, API, access enforcement and exports. Cyber ownership does not transfer every programming task or investigator decision to Cyber. No automatic identity merge, automatic persona acceptance or real-world identity output is permitted.
- **INPUT:** Project requirements, sources, proposed features and delivery responsibilities.
- **OUTPUT:** Role-assigned cyber deliverables and domain acceptance requirements.
- **EVIDENCE/INDICATOR FAMILY:** All; ownership itself is not evidence.
- **SUPPRESSION CONDITION:** Out-of-scope or unqualified work cannot be presented as supported functionality.
- **COUNTER-EVIDENCE CONDITION:** None automatic; ownership is not an evidential proposition.
- **PROVENANCE REQUIREMENT:** Requirement source, rule/version and recorded implementation/acceptance responsibility.
- **OWNER:** Cyber accountable for domain; DE/ML/EV/PL deliver their assigned work.

Source: B §§32–33; 2C issue 22. M's Person A/B labels must be mapped to these roles rather than override them.

## 2. Source qualification

- **RULE_ID:** CY-POL-002
- **RULE:** Qualify each source for a stated purpose before operational use. Record acquisition authority/legal basis, access restrictions, reliability grade, information credibility separately, independence affiliations, freshness and contamination concerns. Public availability is not blanket authorisation. A reliable publisher can carry an unreliable assertion. Suspicion of LE/adversary operation is a qualified source concern, not automatic proof every statement is false.
- **INPUT:** Identified source, access method, intended use and supporting qualification material.
- **OUTPUT:** Qualified source record or explicit unresolved/rejected qualification.
- **EVIDENCE/INDICATOR FAMILY:** All; may inform F9 qualification without itself creating F9 support.
- **SUPPRESSION CONDITION:** Unqualified access/use blocks collection or promotion as applicable; lack of qualification is not a numeric penalty.
- **COUNTER-EVIDENCE CONDITION:** Documented source deception, copying or contamination prompts review; retraction requires an identified basis.
- **PROVENANCE REQUIREMENT:** Source identity, purpose, access basis, grade rationale, assessor and qualification/revision time; B's source fields retained.
- **OWNER:** Cyber qualifies; DE observes access constraints; PL stores/enforces; EV reviews grading discipline.

Source: B §§5.2, 7.1, 8.1, 20, 25; 2C issues 4, 15.

## 3. Dataset verification

- **RULE_ID:** CY-POL-003
- **RULE:** Dataset-specific programming uses an inspected release, not candidate field names from R. Verification requires release/archive identity, acquisition record, permitted use/access, inspected representative records, actual structure, account/time semantics, raw/derived separation, available modalities and missing-data limitations. Verification is release-specific. Gwern and CrimeBB schemas remain unverified in the supplied record; CrimeBB priority is conditional on access. Public dataset labels are not PRAMANA actor ground truth.
- **INPUT:** Actual release and access documentation; proposed mappings from R/M.
- **OUTPUT:** Release-specific verification record and grounded adapter fixtures, or explicit outstanding requirements.
- **EVIDENCE/INDICATOR FAMILY:** Depends on verified contents, not dataset name.
- **SUPPRESSION CONDITION:** Missing verification blocks the affected adapter/feature promotion; do not invent columns or zero-fill absent observations.
- **COUNTER-EVIDENCE CONDITION:** Copies, uncertain labels, contradictory timestamps and source contamination are documented limitations, not assumed counterweights.
- **PROVENANCE REQUIREMENT:** Release identity, inspected record references, acquisition provenance, verifier, scope and date.
- **OWNER:** Cyber verification; DE acquisition; ML/PL consume verified contracts; EV checks label suitability.

Source: R §§2–9; B §20; 2C issue 15. R's BUILD NOW wording denotes priority, not available data.

## 4. PRAMANA entity semantics

- **RULE_ID:** CY-POL-004
- **RULE:** Preserve B's distinctions: account = observed platform/handle identity; alias = observed name/variant; persona = human-accepted, reversible account cluster; actor = higher pseudonymous abstraction, not a real person. Keys, wallets, services, contacts, documents and transactions remain observed/represented entities. Wallet clustering is an opinion. A username never maps directly to a real actor; a fusion result cannot silently create an accepted persona.
- **INPUT:** Qualified observations, entity references, proposals and recorded reviews.
- **OUTPUT:** Typed entities and qualified relationships without destructive identity merging.
- **EVIDENCE/INDICATOR FAMILY:** Relevant family by fact; entity existence alone has no family weight.
- **SUPPRESSION CONDITION:** Unsupported relationship interpretation is not promoted; original observations remain distinguishable.
- **COUNTER-EVIDENCE CONDITION:** Shared/staff accounts, resale, compromise and contradictory ownership claims require qualified analysis.
- **PROVENANCE REQUIREMENT:** Entity source/mentions, relationship basis, temporal scope and persona-acceptance review.
- **OWNER:** Cyber semantics; ML provisional resolution; PL storage/review enforcement.

Source: B §§6–7, 11.1–11.3, 14; 2C issues 20, 22.

## 5. Indicator taxonomy

- **RULE_ID:** CY-POL-005
- **RULE:** Preserve typed identifiers and observations from B: aliases; PGP fingerprints/metadata; wallet addresses and observed transaction properties; onion/domain/IP/certificate/service artefacts; contact IDs; image/EXIF/template/text artefacts; linguistic features; event/lifecycle observations; trust assertions; external statements. Validate deterministic formats/checksums where applicable. Type validity is not claim validity. Alias-based scoring-family assignment remains deferred; aliases may support retrieval/candidates without invented family weight.
- **INPUT:** Source-supported mentions or qualified feature outputs.
- **OUTPUT:** Typed indicators with validation and occurrence provenance, or unpromoted suggestions.
- **EVIDENCE/INDICATOR FAMILY:** Allocation under CY-POL-006; no new F10 or generic identity family.
- **SUPPRESSION CONDITION:** Invalid format, unsupported source presence or missing validation blocks authoritative promotion.
- **COUNTER-EVIDENCE CONDITION:** Homoglyphs, copied IDs, shared defaults and incompatible declarations require examination, not automatic exclusion.
- **PROVENANCE REQUIREMENT:** Source location, original representation, normalisation and validator versions.
- **OWNER:** ML implements; Cyber validates meaning; PL preserves mentions.

Source: B §§7.1, 15, 32 Phase 4; 2A alias-mapping finding; 2C issue 21.

## 6. F1–F9 definitions and allocation

- **RULE_ID:** CY-POL-006
- **RULE:** Preserve the definitions below. Allocate each atomic evidential fact to one scoring family. Additional descriptive interpretations do not create duplicate support. Use the explicit allocation precedence below for overlapping cases. Different facts in one document still retain common origin; this rule does not resolve cross-family aggregation or eligible k.
- **INPUT:** Validated facts with propositions and origin lineage.
- **OUTPUT:** One family allocation per fact plus descriptive relationships and dependence information.
- **EVIDENCE/INDICATOR FAMILY:** F1–F9 only, as defined below.
- **SUPPRESSION CONDITION:** Duplicate allocation of the same fact cannot add support; underlying observations remain available.
- **COUNTER-EVIDENCE CONDITION:** Common origin triggers dependence handling, not an automatic opposing weight.
- **PROVENANCE REQUIREMENT:** Fact/source location, allocation rationale, rule version and common-origin references.
- **OWNER:** Cyber allocation; ML deduplication/eligibility; PL traceability; EV fixture review.

| Family | Canonical definition from B §11.2 |
|---|---|
| **F1 Cryptographic** | PGP fingerprint identity; key-metadata similarity: creation time-of-day, algorithm/bits, cipher preferences, version artefact, subkey structure, UID convention; SSH host-key reuse. |
| **F2 Financial** | Address reuse; co-spend cluster co-membership; deposit-address overlap; temporal payment cadence. |
| **F3 Infrastructure** | TLS certificate/SAN; favicon/static-asset hashes; server banner; header order; error-page fingerprint; analytics/ad ID; clock skew; SSH hostkey; ASN/host. |
| **F4 Contact identifiers** | Jabber/XMPP, Session, Telegram, Tox, email; self-declared mirror lists and PGP-signed migration notices. |
| **F5 Content artefacts** | Product-image pHash reuse; EXIF cluster; listing/post template structure; price-rounding/unit conventions; verbatim non-boilerplate text reuse; signature-block form. |
| **F6 Linguistic style** | Stylometric verification features, including character n-grams and style embeddings. |
| **F7 Behavioural/temporal** | Migration-window co-timing; lifecycle co-occurrence; catalogue continuity; activity-rhythm similarity appears in the canonical list but is context-only under the frozen event-driven policy. |
| **F8 Social/trust** | Co-vouching, shared endorsements, reciprocal trade links, moderator statements. |
| **F9 External corroboration** | Public indictments, official takedown notices, credible published research, verified leaks. |

| Overlap | Frozen allocation precedence |
|---|---|
| SSH key reuse also recorded as infrastructure | Key-reuse support allocated to F1; service association can remain infrastructure context without another F3 vote from the same reuse. |
| Signature and signed migration assertion | Cryptographic fact F1; declaration/contact fact F4; common origin retained. No claim that these count as two independent families. |
| Static template/catalogue features and continuity over time | Static reuse F5; separately established event-anchored continuity F7; shared inputs retain dependence. |
| Re-vouching around migration | Trust assertion F8; an independently described event-timing fact may be F7, with shared provenance retained. |
| External document quoting an existing assertion | F9 eligibility is assessed on the external corroborating proposition, not granted simply by republication. |

Sources: B §§11.2, 12.3, 17; 2C issue 1. This precedence is an explicit reconciliation of overlapping definitions, not a claim that B listed mutually exclusive signals. Numeric caps remain in the numerical baseline, not redefined here.

## 7. RAW OBSERVATION

- **RULE_ID:** CY-POL-007
- **RULE:** A raw observation records acquired bytes, source-reported statements or response metadata and how they were obtained. It establishes what was observed, not the truth of a statement or the identity of its author. An acquisition repeat remains separately traceable without automatically becoming independent corroboration.
- **INPUT:** Authorised capture or verified archive import admitted under collection policy.
- **OUTPUT:** Capture/observation with integrity and acquisition context.
- **EVIDENCE/INDICATOR FAMILY:** None until an eligible fact is interpreted.
- **SUPPRESSION CONDITION:** Rejected content follows CY-POL-031; accepted observations are not deleted merely because they support no hypothesis.
- **COUNTER-EVIDENCE CONDITION:** Source contradictions may be observed but do not become weighted opposition at capture.
- **PROVENANCE REQUIREMENT:** Source, acquisition time/method/version, content integrity reference and available response/archive metadata.
- **OWNER:** DE capture; Cyber source meaning; PL integrity registration.

Source: B §§5–9, 25; 2C concepts and issue 14.

## 8. DETERMINISTIC DERIVATION

- **RULE_ID:** CY-POL-008
- **RULE:** Parsing, checksum validation, normalisation, hashing and other deterministic transforms produce reproducible derived facts. Preserve input lineage and relevant original representation. A valid PGP fingerprint or address checksum is not evidence of ownership. Derived records do not acquire independent origin because a new ID or transform exists.
- **INPUT:** Accepted observations or previously traceable derivations.
- **OUTPUT:** Typed, source-backed derivation with validation result.
- **EVIDENCE/INDICATOR FAMILY:** Candidate family under CY-POL-006, not automatic scored evidence.
- **SUPPRESSION CONDITION:** Failed validation or unverifiable source presence blocks promotion; report failure explicitly.
- **COUNTER-EVIDENCE CONDITION:** Invalid content is a validation result, not automatically an identity contradiction.
- **PROVENANCE REQUIREMENT:** Input references/locations, transform parameters and version, output and validation outcome.
- **OWNER:** ML extraction implementation; Cyber interpretation; PL persistence.

Source: B §§5.2, 12.3, 15; R §§5, 7.

## 9. ML FEATURE

- **RULE_ID:** CY-POL-009
- **RULE:** Embeddings, NER suggestions, style features and detector predictions retain model/input lineage and advisory status until their specified validator/gate passes. Generative or advisory output cannot self-promote to evidence, pair scores, assessments, must-not-link or accepted personas. The authorised deterministic scoring/calibration pipeline is not prohibited merely because it uses statistical methods.
- **INPUT:** Permitted, traceable model inputs.
- **OUTPUT:** Versioned feature/suggestion and gate/execution outcome.
- **EVIDENCE/INDICATOR FAMILY:** F6 or other qualified downstream family; feature generation itself creates no independent vote.
- **SUPPRESSION CONDITION:** Missing validation, failed gates or unavailable models prevent evidential promotion; do not report an unrun check as passed.
- **COUNTER-EVIDENCE CONDITION:** Model disagreement alone is not a hard contradiction.
- **PROVENANCE REQUIREMENT:** Input set, model/configuration/version, feature method and validation record.
- **OWNER:** ML implements; Cyber domain gates; EV validates; PL enforces write authority.

Source: B §15; M p. 1 corrected by 2B/2C authority resolution.

## 10. EVIDENCE

- **RULE_ID:** CY-POL-010
- **RULE:** Evidence interprets a validated fact against a specified pseudonymous comparison proposition. It carries subjects, one family, polarity, canonical origin, temporal applicability, eligibility and reproducible methodology. Scored evidence additionally requires approved weighting inputs/methods. An unweighted candidate, model similarity or family cap cannot masquerade as raw_log_lr. Missing calculations remain missing; no placeholder zero makes them computed. Suppressed and retracted records remain distinguishable from active evidence.
- **INPUT:** Qualified observations/derivations/features plus an explicit interpretation and authorised promotion.
- **OUTPUT:** Traceable evidence candidate or completed evidence object, clearly distinguished by the agreed contract.
- **EVIDENCE/INDICATOR FAMILY:** Exactly one F1–F9 allocation per fact.
- **SUPPRESSION CONDITION:** Clone/hub and modality gates apply; missing provenance prevents promotion.
- **COUNTER-EVIDENCE CONDITION:** Opposing evidence requires an identified proposition and qualified basis; absence is not automatically opposition.
- **PROVENANCE REQUIREMENT:** B §§7–8 lineage, source quality, clocks, subjects and relevant method/model/parameter versions.
- **OWNER:** ML generation; Cyber eligibility; EV method review; PL schema/enforcement.

Source: B §§7–8, 12–15; 2C issue 21. Exact physical representation and numerical fields are deferred in DC-01–DC-06.

## 11. EVIDENCE GROUP

- **RULE_ID:** CY-POL-011
- **RULE:** A group consolidates evidence according to origin dependence in the existing family/key model. Preserve B's independence-key tuple: (canonical_artefact_id, family, source_independence_cluster). Different tuple values, record IDs or datasets do not prove independence. Derived/quoted/mirrored facts retain origin dependence. Complete grouping, cross-family contribution and eligible-k semantics remain deferred; an engineer cannot substitute a local grouping heuristic.
- **INPUT:** Eligible evidence, canonical/derivation relations and source-cluster context.
- **OUTPUT:** Origin/dependence information; a completed group only when the required grouping contract is available.
- **EVIDENCE/INDICATOR FAMILY:** Family-associated grouping with cross-family dependence preserved.
- **SUPPRESSION CONDITION:** Suppressed members cannot become counted strongest members or increase support; group scope is not permission to suppress unrelated family evidence.
- **COUNTER-EVIDENCE CONDITION:** Dependence is not automatically negative evidence; negative grouping is also deferred.
- **PROVENANCE REQUIREMENT:** Members, origins, derivation relations, cluster snapshot and grouping/parameter version.
- **OWNER:** ML grouping; Cyber origin interpretation; EV validation; PL lineage storage.

Source: B §§8.1, 12.2–12.3, 13; 2C issues 2–4. See DC-01.

## 12. HYPOTHESIS

- **RULE_ID:** CY-POL-012
- **RULE:** State the proposition, competing defence proposition, pseudonymous subjects, temporal scope and declared reference population. A candidate relationship is not an accepted hypothesis or a fact of shared control. Hypotheses and prior assessments cannot recursively serve as independent evidence for themselves.
- **INPUT:** Candidate relationship and source-backed investigative question.
- **OUTPUT:** Explicit, contestable hypothesis for evaluation/review.
- **EVIDENCE/INDICATOR FAMILY:** Consumes qualified families; not a new evidence family.
- **SUPPRESSION CONDITION:** Unsupported or out-of-scope propositions cannot be promoted as attribution claims.
- **COUNTER-EVIDENCE CONDITION:** Alternatives such as sharing, copying, resale and common infrastructure remain visible for testing.
- **PROVENANCE REQUIREMENT:** Subjects, proposition/defence wording, scope, reference population and originating basis/version.
- **OWNER:** Cyber domain formulation; ML candidate support; PL storage; reviewing analyst authors acceptance decisions.

Source: B §§6–7, 10.1, 14.

## 13. ASSESSMENT

- **RULE_ID:** CY-POL-013
- **RULE:** An assessment is a versioned result of approved computation applied to a hypothesis, with limits, counter-evidence, family count, methodology and review state. k<2 means a maximum Weak positive band, not EXCLUDED or numeric zero; zero/negative support is never upgraded to positive. Approved hard vetoes remain outside numeric scoring and emit EXCLUDED with no numeric LR or posterior. Missing computation/calibration cannot be displayed as measured/calibrated. No automatic persona acceptance, identity merge or real-world identity output occurs.
- **INPUT:** Hypothesis, eligible groups, approved computation and check outcomes.
- **OUTPUT:** Reproducible assessment or explicit inability to complete it; separate human review record.
- **EVIDENCE/INDICATOR FAMILY:** Qualified supporting families only; suppressed, negative-only and unavailable families do not increase supporting k.
- **SUPPRESSION CONDITION:** Underlying eligibility rules apply; a deferred check is not silently treated as passed.
- **COUNTER-EVIDENCE CONDITION:** Approved hard constraints veto; soft aggregation awaits DC-02. k eligibility awaits DC-01.
- **PROVENANCE REQUIREMENT:** Evidence tree, population/snapshot, method/parameter versions, calibration basis if available and review history.
- **OWNER:** ML assessment; EV validation; PL presentation/review enforcement; Cyber claim discipline.

Source: B §§12–14, 28; 2B band/veto resolution; 2C issue 9. Numerical methods and endpoint implementation remain in the separately approved numerical contract.

## 14. PGP intelligence

- **RULE_ID:** CY-POL-014
- **RULE:** Unsigned public PGP republication = no positive F1 weight. Parse and retain valid blocks/fingerprints for observation, retrieval and candidate discovery. Verified signed-artefact provenance and cross-key metadata similarity are eligible F1 inputs only through qualified interpretation. Signature validity does not establish a human, exclusive key control or uninterrupted operator continuity. Missing keys/signatures do not automatically oppose a link.
- **INPUT:** Actual key material, signed artefacts and source-supported metadata where present.
- **OUTPUT:** Separate publication, fingerprint, signature-validation and continuity interpretations.
- **EVIDENCE/INDICATOR FAMILY:** F1; declaration content may be F4 under CY-POL-006 with common origin retained.
- **SUPPRESSION CONDITION:** Bare unsigned republication has no positive F1 support; invalid signatures, hub/clone origin and missing required validation prevent the affected promotion.
- **COUNTER-EVIDENCE CONDITION:** Key sharing/theft, resale, impersonation and conflicting control assertions are alternative explanations; no automatic numeric penalty.
- **PROVENANCE REQUIREMENT:** Exact material, source location, parser/signature validator versions and verification outcome.
- **OWNER:** Cyber interpretation; ML validation/extraction; PL provenance; EV adversarial fixtures.

Source: B §§11.2, 24 attack 7; R §§5, 8 corrected by 2C issue 5.

## 15. Financial intelligence

- **RULE_ID:** CY-POL-015
- **RULE:** Record validated addresses and actually available transaction observations. Address reuse never triggers an identity merge. Cluster membership remains an opinion with method, version, confidence basis and limitations. Detected CoinJoin/PayJoin/batching conditions suppress the affected CIOH-derived evidence for that transaction; they do not invalidate every unrelated address observation. Service/exchange reuse is evaluated under hub rules. XMR address observation is permitted; tracing is not. BitcoinHeist/SNAP descriptions do not establish missing transaction inputs or mixing labels.
- **INPUT:** Verified addresses, available chain observations and qualified label sources.
- **OUTPUT:** Address/transaction facts and conditional financial-evidence candidates.
- **EVIDENCE/INDICATOR FAMILY:** F2.
- **SUPPRESSION CONDITION:** Affected heuristic suppressed when its defined mixing/batching conditions fire; hubs/clones also apply. Unimplemented detection remains visible.
- **COUNTER-EVIDENCE CONDITION:** Shared services, planted addresses and weak label provenance are alternatives, not automatic penalties.
- **PROVENANCE REQUIREMENT:** Observation/transaction references, label source/grade, cluster method/version and suppression reason.
- **OWNER:** ML analytical implementation; Cyber semantics/labels; DE acquisition; PL opinion/provenance storage; EV tests.

Source: B §19, Phase 10; R §§3, 6; 2A financial-data findings.

## 16. Infrastructure intelligence

- **RULE_ID:** CY-POL-016
- **RULE:** Interpret only observations actually acquired or preserved: certificates/SANs, banners, headers, assets, error pages, service declarations and other B-listed artefacts. Every origin interpretation remains a candidate with shared-host/CDN/default alternatives. A match alone is not origin proof. Archive HTML cannot stand in for missing TLS, header, clock or descriptor telemetry. Descriptor/OnionBalance and clock-observation methods require the deferred method/fixture contract before implementation claims.
- **INPUT:** Authorised source-supported infrastructure observations.
- **OUTPUT:** Typed artefacts, documented alternatives and qualified candidate correlations; unavailable checks identified.
- **EVIDENCE/INDICATOR FAMILY:** F3; SSH reuse allocation follows F1 precedence.
- **SUPPRESSION CONDITION:** Common/hub indicators and clones cannot carry support; unchecked shared-hosting alternatives prevent an origin claim.
- **COUNTER-EVIDENCE CONDITION:** Shared hosting, common panels/CDNs, default assets and deliberate decoys challenge origin interpretation; magnitudes remain deferred.
- **PROVENANCE REQUIREMENT:** Target, authorisation, acquisition mode/time, raw observable, probe/parser version and alternative-check outcome.
- **OWNER:** DE infrastructure acquisition/module; ML analytical support; Cyber qualification; PL enforcement; EV controls.

Source: B §§7.1, 18, Phase 9; 2C issue 16. See DC-07.

## 17. Contact intelligence

- **RULE_ID:** CY-POL-017
- **RULE:** Contacts and self-declared mirror/migration assertions are observations requiring validation and contextual interpretation. Identifier persistence can support a candidate, not prove the same operator. Unsigned declarations remain self-assertions. Signed notices separate declaration content from signature validation while retaining origin dependence. SNAP topology is not automatically contact evidence.
- **INPUT:** Source-present contact identifiers, mirror lists or migration statements.
- **OUTPUT:** Typed contact/declaration facts and qualified continuity candidates.
- **EVIDENCE/INDICATOR FAMILY:** F4; cryptographic validation may be F1, without assumed independence.
- **SUPPRESSION CONDITION:** Failed validation, hub/clone origin or unsupported source presence blocks affected support.
- **COUNTER-EVIDENCE CONDITION:** Shared/staff contacts, copied notices, account transfer and conflicting declarations require review.
- **PROVENANCE REQUIREMENT:** Exact mention/statement, platform, time semantics and validation/signature context.
- **OWNER:** ML extraction; Cyber meaning; DE source access; PL mentions/provenance.

Source: B §§7.1, 11.2; R §3; 2C issues 1, 5.

## 18. Content, templates, canonicalisation and clones

- **RULE_ID:** CY-POL-018
- **RULE:** Treat static template/image/EXIF/non-boilerplate reuse as F5 candidates, not organic authorship. Preserve acquisition records separately from canonical content. Mirrors and quoted portions inherit origin dependence; new surrounding commentary remains separately interpretable. Clone-derived evidence = suppressed, not deleted, and its derivations cannot score or increase k. Preserve clone_of separately; a clone cannot replace/suppress the original merely by copying it. Suspicion is not confirmed clone status. Unrelated evidence in the same family remains eligible.
- **INPUT:** Admitted captures, source portions, images and content-comparison outputs.
- **OUTPUT:** Canonical membership, mirrors/quotes/clone relations, F5 candidates and explicit suppression reasons.
- **EVIDENCE/INDICATOR FAMILY:** F5; provenance/suppression affects all families derived from the material.
- **SUPPRESSION CONDITION:** Confirmed clone lineage suppresses derived evidence; stock/default hubs suppress affected support only.
- **COUNTER-EVIDENCE CONDITION:** Reselling, shared templates, copied catalogues and payment substitution challenge identity interpretations; suppression is not automatically negative evidence.
- **PROVENANCE REQUIREMENT:** Compared inputs/portions, membership history, origin links, transform/configuration versions and clone determination.
- **OWNER:** ML canonicalisation; Cyber interpretation; DE captures; PL lineage; EV adversarial tests.

Source: B §§8.2, 12.3, 16; R §4; 2C issues 3, 11. B's SHA-256/SimHash/pHash/containment/overlap defaults remain identified configuration, not verified detection performance; unresolved origin grouping stays in DC-01.

## 19. Linguistic and stylometric intelligence

- **RULE_ID:** CY-POL-019
- **RULE:** F6 is weak corroboration/candidate support, never a solitary reason for identity acceptance. Preserve B §16 gates: under 300 characters, F6 is not computed; detected translation/transliteration or LLM mediation suppresses F6; absent cross-topic control is explicitly marked topic-confound unverified. The documented topic adjustment belongs to the numerical contract, not an invented policy formula. A gate is not a claim of universally reliable AI-text detection. Template structure remains F5. Validated multi-operator conditions suppress F6/F7.
- **INPUT:** Traceable text and qualified feature/gate outputs.
- **OUTPUT:** Gated F6 feature/evidence candidate and visible limitations/execution state.
- **EVIDENCE/INDICATOR FAMILY:** F6; static structural artefacts F5.
- **SUPPRESSION CONDITION:** Defined length, translation, mediation and multi-operator gates; missing detector execution cannot masquerade as a clean text result.
- **COUNTER-EVIDENCE CONDITION:** Qualified competence/style contradictions may oppose continuity; style change alone does not prove handover or justify hard exclusion.
- **PROVENANCE REQUIREMENT:** Source text span, preprocessing, topic-control status, model/gate versions and outcomes.
- **OWNER:** ML implements; Cyber domain suitability; EV evaluates; PL exposes caveats.

Source: B §§11.3, 16, Phase 8; R §4; 2C issues 6, 20. Exact gate/weight methods not already defined remain deferred.

## 20. Behavioural and temporal intelligence

- **RULE_ID:** CY-POL-020
- **RULE:** F7 scoring is event-driven only. Require a documented migration/lifecycle event and source-supported continuity observations. Continuous sleep/timezone inference, unanchored rhythm similarity and response latency are context only. Static reuse is F5; event-anchored continuity may be F7 with shared input dependence retained. No scrape-time or ordinary posting overlap automatically becomes a hard veto or invented soft penalty.
- **INPUT:** Qualified events, observations and their distinct clocks/uncertainty.
- **OUTPUT:** Event-linked behavioural candidates, contextual attributes and explicit unavailable/inconclusive checks.
- **EVIDENCE/INDICATOR FAMILY:** F7; relevant other facts retain their canonical allocation.
- **SUPPRESSION CONDITION:** Unanchored rhythm has no F7 support; validated multi-operator conditions suppress F6/F7.
- **COUNTER-EVIDENCE CONDITION:** Succession, mass migration, staff/automation and genuine timing incompatibility require qualification; temporal hard-veto eligibility is deferred.
- **PROVENANCE REQUIREMENT:** Event definition/source, observation links, timing basis and detector/version.
- **OWNER:** Cyber event meaning; ML features; DE source data; PL clocks; EV timing fixtures.

Source: B §§11.2–11.3, 13, 17; 2C issues 6–7. Specific event-window parameters are not supplied by this policy.

## 21. Social and trust intelligence

- **RULE_ID:** CY-POL-021
- **RULE:** F8 covers co-vouching, endorsements, reciprocal trade links and moderator statements. Separate a source's assertion from a demonstrated relationship. Graph proximity, generic co-membership and SNAP trust rows are not automatically PRAMANA attribution evidence. The F8 generator remains unimplemented/unspecified unless a bounded source/validation contract and fixtures are supplied; reserved family support does not count as implemented coverage.
- **INPUT:** Verified trust assertions and their source contexts, when available.
- **OUTPUT:** Traceable assertions/candidates or explicit modality unavailability.
- **EVIDENCE/INDICATOR FAMILY:** F8.
- **SUPPRESSION CONDITION:** Clone/hub and validation rules apply; unavailable generators add no evidence or k.
- **COUNTER-EVIDENCE CONDITION:** Sybils, reciprocal fabrication, copied endorsements and compromised accounts challenge the assertion.
- **PROVENANCE REQUIREMENT:** Asserting account, actual statement/edge source, observed/event times where known and validation/version.
- **OWNER:** Cyber qualification; ML generator; EV adversarial validation; PL execution/provenance state.

Source: B §§11.2, 24 attack 9; 2C issue 17. See DC-08.

## 22. External corroboration

- **RULE_ID:** CY-POL-022
- **RULE:** F9 includes qualified public indictments, official takedown notices, credible research and verified leaks within lawful scope. Preserve what the source actually asserts and its status; an indictment is not automatically a proven fact. Official-looking text and repetition do not establish authenticity or independent corroboration. No privileged legal-process returns or unlawfully acquired leaks are assumed available. F9 generation/weighting remains contingent on its deferred contract.
- **INPUT:** Lawfully obtained external statements with verifiable source context.
- **OUTPUT:** Qualified statement and candidate corroboration, or unavailable/unverified status.
- **EVIDENCE/INDICATOR FAMILY:** F9; not automatic actor ground truth.
- **SUPPRESSION CONDITION:** Unverified authenticity/access, clone dependence or missing qualification prevents authoritative promotion.
- **COUNTER-EVIDENCE CONDITION:** Retractions, disinformation, incompatible statements and common underlying sources require review; source status alone supplies no counterweight.
- **PROVENANCE REQUIREMENT:** Original publication, precise supporting passage, authority/status, dates, verification and underlying-source lineage.
- **OWNER:** Cyber verification; ML generation; EV evidential review; PL traceability.

Source: B §§11.2, 20, 24; D's expanded legal-return examples narrowed by 2C issue 17.

## 23. Rarity and hubs

- **RULE_ID:** CY-POL-023
- **RULE:** Hub = >12 distinct eligible observed accounts per validated indicator in a declared snapshot under the default threshold. Exactly 12 does not trigger that default. Accounts use the observed (platform, handle) identity, not resolved personas; repeat mentions/captures do not add accounts. Rejected, quarantined and confirmed-clone-derived associations are outside the scoring population. Mirror acquisitions do not create originating accounts. Keep site count separate. Hub-dependent support is zero; unrelated evidence remains eligible. Rarity formula and grade effects are deferred, not inferred from this counting rule.
- **INPUT:** Validated indicator-account associations and snapshot eligibility.
- **OUTPUT:** Reproducible account/site counts, hub decision and affected-support restriction.
- **EVIDENCE/INDICATOR FAMILY:** All applicable families.
- **SUPPRESSION CONDITION:** Hub-linked contributions cannot support a hypothesis or increase k; do not zero an entire family automatically.
- **COUNTER-EVIDENCE CONDITION:** Shared defaults/escrow/services explain reuse; hub status is not automatically negative evidence.
- **PROVENANCE REQUIREMENT:** Snapshot membership, deduplicated account associations, threshold/config version and exclusions.
- **OWNER:** ML counts; Cyber eligibility; PL snapshot storage; EV boundary tests.

Source: B §§5.2, 10.1; 2C issue 10. The population exclusion rule is an explicit Step 2C reconciliation, not an empirically validated rarity model.

## 24. Cross-dataset dependence

- **RULE_ID:** CY-POL-024
- **RULE:** Dataset boundaries do not imply independence. Original, quotation, mirror, later report, embedding and re-ingestion preserve shared origin where applicable. A different publisher, dataset, record ID or transformation is insufficient to establish a separate observation opportunity. Record uncertain origins as uncertain; do not claim established independence. Cross-dataset comparisons do not promote public labels to actor truth.
- **INPUT:** Combined qualified records and underlying-source/derivation information.
- **OUTPUT:** Cross-source lineage and dependence qualifications for grouping.
- **EVIDENCE/INDICATOR FAMILY:** All, including external corroboration.
- **SUPPRESSION CONDITION:** Duplicate derivations cannot earn extra independent support; exact aggregation awaits DC-01.
- **COUNTER-EVIDENCE CONDITION:** Dependence reduces claimed corroboration; it is not automatically evidence for different operators.
- **PROVENANCE REQUIREMENT:** Both acquisition dataset and underlying origin, source-cluster membership/version and known copy relationships.
- **OWNER:** Cyber origin investigation; ML cross-corpus matching; PL lineage; EV tests.

Source: B §12.3; R §8; 2C issue 4.

## 25. Provenance, time, retention and retraction

- **RULE_ID:** CY-POL-025
- **RULE:** Preserve acquisition/observation, event, valid, belief and assessment/revision meanings. Historical archive observation and PRAMANA acquisition remain distinct. A displayed date remains source-reported; missing time is unknown, not ingestion time. Preserve raw time/timezone representation and normalisation lineage. Retraction revises eligibility and propagates recomputation/review reopening without erasing history. Raw-payload expiry is distinct from retraction; the B 180-day policy has unresolved lifecycle details and does not authorise guessed cascade deletion.
- **INPUT:** Captures, source time statements, transforms, revisions and qualified retraction requests.
- **OUTPUT:** Traceable temporal records, versioned evidence/assessment history and retraction impacts.
- **EVIDENCE/INDICATOR FAMILY:** All.
- **SUPPRESSION CONDITION:** Retracted inputs cannot continue as active support; unknown timing blocks claims requiring that timing rather than fabricating it.
- **COUNTER-EVIDENCE CONDITION:** Actual incompatible events need qualification; payload unavailability or retraction alone is not a numeric opposing fact.
- **PROVENANCE REQUIREMENT:** All relevant clocks, raw representations, revision reason/actor/time and affected dependency history.
- **OWNER:** PL temporal/retraction implementation; Cyber interpretation; DE acquisition times; ML recomputation; EV replay tests.

Source: B §§8–9, 25.4; R §7; 2C issues 14, 19. See DC-04 and OD-03.

## 26. Counter-evidence taxonomy

- **RULE_ID:** CY-POL-026
- **RULE:** Preserve all seven named B §13 classes below; its statement "six" is a counting error. Record execution state and actual findings. Suppression, opposing evidence, succession proposal and hard veto are distinct effects. No absent/unrun finding counts as a clean check. Hard veto eligibility must be approved and remains outside scoring. Automatic temporal-overlap vetoes and numeric negative aggregation remain deferred. No engine may improvise a soft penalty in their place.
- **INPUT:** Candidate proposition, all qualified observations and detector definitions.
- **OUTPUT:** Class-specific check outcomes, qualified opposing candidates, suppressions or approved constraints.
- **EVIDENCE/INDICATOR FAMILY:** Relevant underlying F1–F9; no separate negative-evidence family.
- **SUPPRESSION CONDITION:** Hub/clone/modality rules apply independently; suppression does not automatically create counterweight.
- **COUNTER-EVIDENCE CONDITION:** The seven classes below, subject to their defined evidence and execution requirements.
- **PROVENANCE REQUIREMENT:** Examined inputs, proposition, detector/version, effect, execution state and approving basis for hard constraints.
- **OWNER:** Cyber domain rules; ML detectors; EV validation; PL effect/state persistence.

| Class | Domain meaning / permitted policy effect |
|---|---|
| Temporal impossibility | Qualified incompatibility; automatic overlap-veto preconditions remain deferred. |
| Language/competence contradiction | Qualified inconsistent competence/style; B's F6 eligibility restriction applies when its defined condition is established. |
| Lifecycle contradiction | Possible succession rather than identity; route through versioned interpretation/segmentation policy. |
| Independence collapse | Support depends on a common origin; no invented numeric opposition or extra family count. |
| Hub/rarity contradiction | A shared/default indicator cannot provide the affected support; no automatic penalty. |
| Shared-infrastructure alternative | Common host/CDN/panel/default explanation; candidate-origin limitations and qualified counter-evidence. |
| Framing pattern | Source-supported planting/dispute/first-seen pattern; suspicion is not a proven identity fact. |

Source: B §13 versus Phase 6/M p. 4/D p. 12 summaries; 2C issues 7–8.

## 27. Account handover and segmentation

- **RULE_ID:** CY-POL-027
- **RULE:** A detector proposes a time-bounded handover/segmentation interpretation with uncertainty. It cannot silently split the unit of resolution or create an accepted persona. A recorded human decision activates a boundary for resolution; rejection/deferral leaves membership unchanged. Preserve the original account. Accepted boundaries remain versioned and reversible; dependent assessments are revised/reopened as appropriate. A style shift or succeeds relation does not prove a new real person.
- **INPUT:** Qualified changes in style/template/contact/catalogue or related observations.
- **OUTPUT:** Proposal and review outcome; accepted versioned boundary only after human decision.
- **EVIDENCE/INDICATOR FAMILY:** Underlying F4/F5/F6/F7/F8 or other qualified facts; no automatic independent combination.
- **SUPPRESSION CONDITION:** No automatic persona acceptance; validated multi-operator conditions affect F6/F7 independently of a proposed split.
- **COUNTER-EVIDENCE CONDITION:** Staff rotation, topic change, automation and compromise/resale alternatives remain explicit.
- **PROVENANCE REQUIREMENT:** Supporting timeline, uncertain boundary, detector/version, review/rationale and supersession history.
- **OWNER:** ML proposals; Cyber interpretation; reviewing analyst decision; PL history; EV tests.

Source: B §§11.3, 16; 2C issue 20 explicitly resolves automatic-split versus proposal language. Interval/schema mechanics await DC-06.

## 28. RANGE-SIM policy

- **RULE_ID:** CY-POL-028
- **RULE:** RANGE-SIM evaluates pseudonymous attribution/resolution/fusion and associated controlled adversarial behaviour. Keep truth outside operational inference and analyst UI. Evaluator-only comparison with frozen predictions is permitted; fitting uses designated development labels, never held-out answers. Preserve temporal/open-set evaluation discipline. No public label becomes synthetic actor truth. Disclose synthetic origin and generation conditions. Conflicting B corpus counts require one selected manifest; none is claimed generated here.
- **INPUT:** Selected seeded fixture, separate truth manifest and declared evaluation partition.
- **OUTPUT:** Reproducible scenario inputs and task-specific evaluation outputs when implemented.
- **EVIDENCE/INDICATOR FAMILY:** All deliberately represented families; unrepresented families are not fabricated.
- **SUPPRESSION CONDITION:** Truth leakage invalidates the affected evaluation claim; it does not become operational counter-evidence.
- **COUNTER-EVIDENCE CONDITION:** Planted traps test specified mechanisms, not live-world effectiveness.
- **PROVENANCE REQUIREMENT:** Seed/generation version, manifest, snapshot, partition, predictions and evaluation version.
- **OWNER:** DE generator; Cyber scenarios; EV evaluation/truth boundary; ML predictions; PL access enforcement.

Source: B §§21–22, Phases 2/12; 2C issues 12–13. Public attribution accuracy and achieved fixture counts are not claimed.

## 29. RANGE-TOR policy

- **RULE_ID:** CY-POL-029
- **RULE:** RANGE-TOR evaluates controlled infrastructure observations/mappings and false links on shared/default and clean controls. It remains separate from RANGE-SIM's attribution domain. A known onion/clearnet mapping is not automatically a same-operator label. Only self-owned/authorised allowlisted targets participate. Disclose controlled-testbed origin; unresolved service/misconfiguration/control counts require a selected manifest.
- **INPUT:** Controlled target inventory, observation methods and separate expected mappings/controls.
- **OUTPUT:** Infrastructure test observations and task-specific evaluation results when executed.
- **EVIDENCE/INDICATOR FAMILY:** Primarily F3, with other facts classified separately; not pooled actor truth.
- **SUPPRESSION CONDITION:** Shared-default/hub/clone and method-validity rules apply; an absent probe result is not a passed control.
- **COUNTER-EVIDENCE CONDITION:** Clean and shared-host controls challenge unjustified origin claims.
- **PROVENANCE REQUIREMENT:** Ownership/allowlist, fixture version, actual observations, known mapping source and evaluator output.
- **OWNER:** DE testbed/probes; Cyber cases; EV evaluation; ML analytical support; PL controls.

Source: B §§21.2, 22, Phase 9; 2C issue 12.

## 30. Infrastructure collection boundaries

- **RULE_ID:** CY-POL-030
- **RULE:** All operational collection is lawful, allowlisted and controlled. Known/publicly advertised targets do not imply authorisation. Register permitted targets and methods before fetching/probing. No authentication bypass, credentials acquisition, CAPTCHA evasion, exploitation, broad live-marketplace crawling or Tor enumeration. Archive analysis uses actual preserved material; controlled infrastructure demonstration uses RANGE-TOR/self-owned targets. Acquisition cannot be planned/executed by an autonomous LLM loop.
- **INPUT:** Qualified source, target/method inventory and authorisation.
- **OUTPUT:** Permitted collection job or explicit refusal/unresolved scope.
- **EVIDENCE/INDICATOR FAMILY:** F3 and other collected modalities; authorisation itself is not evidence weight.
- **SUPPRESSION CONDITION:** Out-of-allowlist/unauthorised jobs are rejected before collection, not merely zero-scored afterward.
- **COUNTER-EVIDENCE CONDITION:** Collection failure is not evidence of actor evasion or different identity.
- **PROVENANCE REQUIREMENT:** Target, authorised method/scope, job/collector version, timestamps and result.
- **OWNER:** Cyber scope; DE execution; PL enforcement; EV boundary tests.

Source: S interpretation boundary; B §§18, 20, 25, Phase 9; 2C issue 16.

## 31. Security, admission and sealing boundaries

- **RULE_ID:** CY-POL-031
- **RULE:** Preserve B's existing four zones and offline prototype. Before durable payload storage: authorise collection, receive bounded content transiently, compute capture hash before transformation, and run admission screening. Reject/discard denied payloads with only permitted incident metadata; screening error cannot silently admit. For admitted captures, DE writes capture plus metadata to the existing drop path. Z2 verifies the capture hash before parsing and registers/verifies the chain. Only accepted provenance-verified inputs reach analysis. Z1 cannot write the DB; Z2/Z3 have no outbound network. Use benign synthetic screening sentinels, not actual prohibited material.
- **INPUT:** Authorised transient bytes and admission controls.
- **OUTPUT:** Admitted sealed capture or logged rejection/failure without rejected-payload persistence.
- **EVIDENCE/INDICATOR FAMILY:** All; screening is not attribution evidence.
- **SUPPRESSION CONDITION:** Admission rejection prevents storage/promotion; accepted evidence suppression remains a different operation.
- **COUNTER-EVIDENCE CONDITION:** Integrity failure prevents promotion; it is not an automatic identity penalty.
- **PROVENANCE REQUIREMENT:** Capture hash, collection method/version, admission result, Z2 verification and chain registration; no prohibited payload in incident logs.
- **OWNER:** DE capture/screening; PL zones/access/chain; Cyber admission policy; EV verification.

Source: B §§5.2, 25, 29; 2C issue 18 explicitly reconciles capture-before-screening wording. The sequence is a policy requirement, not a claim the screen detects all prohibited content. Existing B §25 controls also govern authenticated routes, least privilege/ABAC, secrets, audit trails, protected storage and pinned dependencies. Copilot content has no tools/write authority in untrusted contexts; hosted inference is not a required prototype dependency.

## 32. Cyber → ML contract

- **RULE_ID:** CY-POL-032
- **RULE:** Cyber supplies verified source semantics, atomic facts/family allocation, origin dependence, eligibility, temporal meaning, alternatives and domain fixtures. ML supplies traceable feature/detector outputs and approved computational definitions with EV. Neither side invents the other's facts. Operational features never consume held-out truth. All handoffs identify missing verification/methods and check state. Scored evidence requires the deferred contract; source observations remain usable as observations without fabricated numbers.
- **INPUT:** Qualified source/domain package and implemented analytical outputs.
- **OUTPUT:** Versioned logical contracts listed in section C, with explicit unresolved items.
- **EVIDENCE/INDICATOR FAMILY:** All implemented/qualified families, with availability declared.
- **SUPPRESSION CONDITION:** Unsupported fields, weights, origins or validators block affected promotion.
- **COUNTER-EVIDENCE CONDITION:** Alternative explanations and opposing candidates are delivered separately from suppressions/vetoes.
- **PROVENANCE REQUIREMENT:** Source record/location, versions, qualification basis, population/partition where relevant and acceptance record.
- **OWNER:** Cyber producer of domain package; ML analytical producer/consumer; EV method/fixture acceptance.

Source: B §§7–8, 15, 32–33; M p. 7; 2C issue 22 and contracts.

## 33. Cyber → Backend contract

- **RULE_ID:** CY-POL-033
- **RULE:** Cyber supplies authorised sources/targets, verified mappings, evidence semantics, security and review requirements, report limitations and fixtures. PL implements existing-schema persistence, access, temporal history, suppression/retraction effects and coherent exports; DE implements collection. The API/UI renders ledger assessments and execution state, not independently rederived scores. Reports cite reviewed assessments and preserve sources, integrity, scope, alternatives and versions. Raw expiry is not implemented through guessed deletion defaults.
- **INPUT:** Domain contracts, DE captures and ML-approved outputs.
- **OUTPUT:** Enforced records/interfaces and traceable reviewed reports/exports.
- **EVIDENCE/INDICATOR FAMILY:** All; no new score assigned at transport/presentation.
- **SUPPRESSION CONDITION:** Missing authority, review or provenance prevents the corresponding publication/promotion; suppressed records remain auditable.
- **COUNTER-EVIDENCE CONDITION:** Preserve check findings and limitations; empty/unrun panels are not clean checks.
- **PROVENANCE REQUIREMENT:** Full source-to-report lineage, snapshot/method versions and human review/rationale.
- **OWNER:** PL delivery; Cyber domain acceptance; DE/ML component outputs; EV audit/evaluation review.

Source: S expected solution; B §§7–9, 14, 25, 28, Phase 13; 2C contracts. CSV/JSON/report outputs satisfy the supplied export requirement; STIX is a Blueprint addition, not a quoted SIH requirement.

## 34. Required fixtures and expected behaviour

- **RULE_ID:** CY-POL-034
- **RULE:** Use the fixture register in section D to verify policy behaviour. Each fixture identifies inputs, truth/expected interpretation, permitted output state and applicable rule IDs. A policy fixture is not a measured benchmark. Numeric expectations require approved ML/EV definitions; do not invent a score to make a test pass. Unimplemented tests and failed tests remain explicit.
- **INPUT:** Versioned benign/synthetic or lawfully sourced fixtures and applicable contracts.
- **OUTPUT:** Reproducible policy acceptance results, with limitations and unexecuted cases.
- **EVIDENCE/INDICATOR FAMILY:** As specified per fixture.
- **SUPPRESSION CONDITION:** Failed fixture acceptance blocks claiming compliance for the affected behaviour.
- **COUNTER-EVIDENCE CONDITION:** Decoys test alternatives; they do not prove live-world effectiveness.
- **PROVENANCE REQUIREMENT:** Fixture version, expected basis, run/config version and actual outcome.
- **OWNER:** Cyber cases; EV acceptance methodology; ML/DE/PL execute component tests.

Source: B §§21–24, 32; 2C required fixtures.

## 35. Out-of-scope capabilities and claims

- **RULE_ID:** CY-POL-035
- **RULE:** No real-world identity output, automatic identity merge/persona acceptance, unauthorised collection, Tor enumeration/cryptographic defeat, Monero tracing, biometric identification or autonomous agentic attribution. No generative decision authority, public-label-to-actor-truth promotion, fabricated data/metrics, guaranteed court admissibility, government endorsement, completed formal validation or live-world performance claim without evidence. DS/SL fusion and GNN linkage are not prototype implementations. Existing prototype architecture is preserved; no new technology is introduced here.
- **INPUT:** Proposed feature, output, source or claim.
- **OUTPUT:** In-scope qualified requirement or explicit exclusion/deferred-roadmap status.
- **EVIDENCE/INDICATOR FAMILY:** All; none overrides these boundaries.
- **SUPPRESSION CONDITION:** Out-of-scope collection is refused; out-of-scope claims are not emitted. This is not an evidential penalty.
- **COUNTER-EVIDENCE CONDITION:** None automatic; scope refusal says nothing about actor identity.
- **PROVENANCE REQUIREMENT:** Scope decision and requirement/rule reference; empirical claims require actual result provenance.
- **OWNER:** Cyber scope/claim discipline; all implementers enforce; EV checks measurement claims; PL output boundary.

Source: S interpretation boundary; B §§1, 14–15, 20, 25, 29–31, 40, 45; M p. 7; D p. 27.

## DEFERRED COMPUTATION CONTRACT

The following are explicit gaps, not permission to choose convenient defaults. ML supplies computational definitions; EV supplies independent validation and expected cases; Cyber supplies domain meaning. PL maps approved definitions into the existing schema. No new engine, datastore or technology is authorised by this list.

| ID | Missing contract | Why it cannot be inferred | Required ML/EV deliverable |
|---|---|---|---|
| DC-01 | Complete origin grouping, quote/multiple-origin handling, source-cluster application, cross-family aggregation and eligible k | B's tuple, inheritance prose and single-origin/family descriptions do not determine one behaviour. Single-family allocation does not solve cross-family dependence. | ML origin-to-group decision table and versioned method; EV fixtures with expected keys, members, contribution eligibility and k, including common-origin facts in different families. |
| DC-02 | Negative sign/magnitude convention, aggregation, dependence, damping/caps and effect interactions | B leaves CounterWeight_f undefined; suppression/veto/negative evidence are different mechanisms. Positive rules cannot simply be copied. | ML counterweight contract; EV hand-calculated cases for duplicate negatives, conflicting polarity, suppress-plus-oppose and hard veto. |
| DC-03 | Per-signal raw LR derivation, source-grade effect and rarity formula | Family caps and corpus counts are not LR functions or a rarity normalisation. | ML versioned definitions, permitted input domains and population basis; EV validation/sensitivity protocol. No invented empirical coefficients. |
| DC-04 | Decay function, time anchor, uncertain/missing-time treatment | B lists half-life defaults but not a complete function/application contract. | ML exact temporal application definitions; EV boundary/missing-time fixtures; Cyber validates clock meaning. |
| DC-05 | Temporal-overlap hard-veto eligibility and soft alternatives | Switching interval, genuine activity/session meaning, uncertainty and automation/staff exclusions are unspecified. | Cyber/ML detector decision table; EV plausible-overlap counterexamples and approved logical-incompatibility cases. No fallback invented soft penalty. |
| DC-06 | Exact evidence-row mappings, promotion representation, nullability, group contribution ownership and segmentation intervals | B §§7–8/M p. 7 use distributed/abbreviated fields and different clock/validity names. Logical semantics here do not settle SQL/API mapping. | ML+PL field-level interface mapped to existing records; EV valid/invalid payload fixtures. Cyber signs off meaning, not fabricated source columns. |
| DC-07 | Descriptor/OnionBalance, clock-observation and other incompletely defined infrastructure methods | Listing a capability does not specify its observable or valid acquisition conditions. | DE/ML target-method-observable contract; EV controlled positive/shared-default/clean cases; Cyber confirms authorisation and interpretation. |
| DC-08 | Initial F8/F9 generation, qualification and weighting | Canonical families exist, but no bounded implemented generators or verified source contracts are supplied. | Cyber source/statement definitions; ML generator contract; EV forged/copied/sybil/control cases and method validation. |
| DC-09 | Exact remaining model gates and event-window parameters | Policy names a gate/event without establishing detector thresholds, windows or validated performance. | ML defined inputs/method/version and unavailable/inconclusive semantics; EV topic/laundering/migration controls and validation results when run. |

Already explicit numerical provisions in B and Step 2B remain controlling inputs to a future numerical specification, not gaps to redesign: family/global caps, fixed subsequent-group damping, band/veto policy and the published band-boundary reconciliation. This document neither replaces them nor claims that they complete DC-01–DC-09.

### Outstanding data and operational contracts (not scoring mathematics)

| ID | Missing item | Responsible delivery and acceptance |
|---|---|---|
| OD-01 | Verified Gwern/CrimeBB release, permissions/access, inspected examples and field/time mappings | Cyber verifies; DE acquires lawfully; ML/PL consume; EV checks label suitability. Required before affected source-specific adapters. |
| OD-02 | One initial RANGE-SIM manifest and one RANGE-TOR manifest resolving inconsistent counts and distinguishing services, conditions and controls | DE drafts; Cyber defines cases; EV accepts expected domains/outcomes. Counts are not silently selected from conflicting B sections. |
| OD-03 | Retention start event, duplicate treatment, normalised/derived-content retention, exceptions and post-expiry replay/report behaviour | Cyber policy with PL/DE lifecycle mapping and EV audit fixtures. No invented expiry/deletion mechanics. |
| OD-04 | Executable admission/probe limits, accepted input formats and operational acceptance fixtures | DE/PL implement the frozen sequence/boundaries; Cyber qualifies permitted handling; EV verifies. No unprovided numeric limits or claimed screening completeness. |

These dependencies do not invalidate the frozen policy. They limit which components can claim implementation readiness.

## A. FROZEN POLICY

CY-POL-001–CY-POL-035 freeze the policy and domain layer only, with their declared dependencies. In particular:

- Unsigned public PGP republication has no positive F1 weight.
- F7 scored behaviour is event-driven.
- k<2 permits no positive band above Weak.
- Default hub detection is >12 distinct eligible accounts.
- Clone-derived evidence is suppressed, not deleted.
- Dataset boundaries and record IDs do not establish independence.
- RANGE-SIM and RANGE-TOR retain separate evaluation domains.
- Observation, event, validity, belief and assessment/revision times retain distinct meanings.
- No automatic persona acceptance, automatic identity merge, real-world identity output or unauthorised collection.
- Suppression, opposing evidence, hard veto, rejection, retraction and payload expiry remain distinct.

Explicit reconciliations embedded here: single-family fact allocation with SSH precedence (006); account-based eligible hub population (023); pre-persistence screening/capture-hash versus Z2 registration (031); reviewed segmentation activation (027); role-level ownership (001). Each resolves an identified source ambiguity and makes no empirical claim.

## B. DEFERRED COMPUTATION

DC-01–DC-09 are not frozen numerical behaviour. No complete scorer, grouping engine, calibrated assessment, temporal veto or unspecified generator may be claimed on the basis of this policy document alone. Missing computations are not zero values, clean checks or successful validations. ML/EV must supply the listed definitions and fixtures; Cyber and PL resolve their domain/schema dependencies.

## C. REQUIRED DATA CONTRACTS

| Contract | Required logical contents | Producer → consumer |
|---|---|---|
| Source qualification | Identity, purpose/access basis, source/item grades and rationales, affiliations, limits, revision history | Cyber/DE → ML/PL/EV |
| Verified dataset adapter input | Actual release/record examples, raw structures, available modalities, account/time semantics, label limits and permissions | Cyber/DE → ML/PL |
| Observation/derivation | Source location, acquisition and original observation context, integrity, original value, transforms/validators and versions | DE/ML → PL/ML |
| Feature | Input lineage, model/config version, feature output, validator/gate/execution state and limits | ML → approved evidence-generation path |
| Evidence candidate/scored evidence | Subjects/proposition, family, polarity, canonical origin, dependence, clocks, eligibility and actual methodology; scored fields only when approved | Cyber semantics + ML generation → PL/scoring; exact mapping DC-06 |
| Group/assessment | Members, origin qualifications, approved contribution trace, hypothesis/defence, population, method versions, limitations and review state | ML → PL/EV; DC-01–DC-04 apply |
| Detector outcome | What ran, inputs, finding, uncertainty and effect; distinguish unimplemented/not-run/failed/inconclusive/completed-no-finding | ML/DE → PL/Cyber/EV |
| Review/segmentation/retraction | Proposed change, underlying evidence, decision/rationale, reviewer/time, revisions and impact | Reviewing analyst + PL → affected analytical consumers |
| Range/evaluation | Fixture/seed/snapshot, observed inputs, separately protected truth, task/partition, predictions and actual run outputs | DE/Cyber → ML/EV; evaluator output → PL |
| Report/export | Reviewed assessments, source/artefact references, alternatives, scope, integrity manifest, snapshot and method versions | PL → investigator/product consumer |

This table specifies contract meaning, not verified external dataset fields. No part grants the operational pipeline access to held-out answers.

## D. REQUIRED FIXTURES

| ID | Case | Expected policy behaviour | Rule IDs |
|---|---|---|---|
| FX-01 | Same payload, repeated acquisitions | Preserve acquisition history; no extra attribution independence. | 007, 018, 024, 025 |
| FX-02 | Gwern original, CrimeBB quote, later report | Shared material retains origin dependence across datasets; no independent votes from packaging. | 006, 011, 024 |
| FX-03 | Quotation with new commentary | Keep quoted and original portions distinguishable; no blanket fresh independence. | 008, 018, 024 |
| FX-04 | SSH reuse also described as infrastructure | One F1 reuse allocation, not duplicate F1/F3 support. | 006, 016 |
| FX-05 | Signed migration announcement | Separate signature/declaration facts, retain common origin; independent k awaits DC-01. | 006, 014, 017 |
| FX-06 | Rival's public key pasted unsigned | Valid parse/retrieval possible; no positive F1 support from republication. | 014 |
| FX-07 | Invalid signature and unavailable verifier | Invalid and not-run remain different; neither presented as verified continuity. | 009, 014 |
| FX-08 | 12 versus 13 eligible accounts; repeated mentions | Default hub at 13, not 12; repetitions do not add accounts. | 023 |
| FX-09 | Confirmed clone plus legitimate original | Clone lineage suppressed and retained; original not suppressed solely because copied. | 018, 023 |
| FX-10 | One hub and unrelated same-family evidence | Affected support zero; unrelated eligible evidence survives. | 011, 023 |
| FX-11 | Duplicate negatives and suppression plus opposition | No invented double penalty; numeric expectations await DC-02. | 026 |
| FX-12 | Overlapping scrape/post times | No automatic temporal hard veto or fabricated soft weight. | 020, 025, 026 |
| FX-13 | Approved hard constraint | EXCLUDED without numeric LR/posterior; no persona merge. | 013, 026 |
| FX-14 | One eligible supporting family | Maximum Weak positive band; not automatic EXCLUDED or zero. | 013 |
| FX-15 | Continuous rhythm with no qualifying event | Context only; no F7 score. | 020 |
| FX-16 | Short/translated/mediated text; topic control absent | Correct F6 gate/qualification; unavailable detector not treated as passed. | 019 |
| FX-17 | Archive observation, later ingestion, missing event time | Distinct clocks; unknown event time retained. | 007, 025 |
| FX-18 | Shared CDN/default banner and rare controlled observation | Shared/default alternatives visible; no origin proof from common match. Exact scoring awaits contract. | 016, 029 |
| FX-19 | Outside-allowlist target or unsupported archive telemetry | Collection refused / missing observable explicit; no invented evidence. | 016, 030 |
| FX-20 | Protected truth access | Operational paths denied; evaluator permitted; held-out answers absent from fitting/prediction. | 028, 029 |
| FX-21 | Benign rejected-content sentinel and screen error | No durable rejected payload; permitted incident only; error does not silently admit. | 031 |
| FX-22 | Capture changed before Z2 verification | Integrity failure blocks analytical promotion. | 031 |
| FX-23 | Handover proposal accepted, rejected and deferred | No automatic change; accepted boundary versioned/reversible; original account preserved. | 027 |
| FX-24 | F8/F9 unavailable or forged/copied assertion | No fabricated support/k and no false clean-check claim. | 021, 022 |
| FX-25 | Retraction versus raw expiry | Retraction revises/reopens dependent assessments; expiry distinct; expiry fixture awaits OD-03. | 025 |
| FX-26 | CoinJoin/PayJoin/batching condition in controlled data | Affected CIOH evidence suppressed; unrelated observations not universally discarded. | 015 |
| FX-27 | Machine suggestion/source mismatch or prompt injection | No authoritative self-promotion or tool/write capability from untrusted content. | 009, 031 |
| FX-28 | Review-required report export | No unreviewed assessment published as authored conclusion; lineage/limits retained. | 013, 033 |

Rule IDs in this table omit the CY-POL- prefix for compactness. Tests verify the behaviour stated, not implementation-shaped assumptions. There are no measured pass rates or benchmark outcomes in this document.

## E. IMPLEMENTATION OWNERS

| Role | Accountable deliverables | Boundary |
|---|---|---|
| **Cyber (sole owner)** | Source/dataset meaning and verification; lawful scope; taxonomy/allocation; evidence eligibility and alternatives; domain fixtures; claim discipline and domain acceptance | Does not fabricate computations, replace EV validation or automatically author every investigator conclusion. |
| **DE** | Authorised acquisition, provenance at capture, source manifests, range generation/testbed and infrastructure acquisition/module delivery | No independent change to evidence semantics or permission boundaries. |
| **ML** | Deterministic extraction/canonicalisation, features and gates, evidence generation, resolution/fusion/calibration, computational contracts | No invented source facts; no self-promoting advisory outputs; no held-out-truth leakage. |
| **EV** | Evaluation protocols, truth-domain/access tests, methodological validation, numerical/fixture expectations and honest measurement | Targets and fixtures are not achieved results; reports limitations. |
| **PL / Backend** | Existing schema/API, access/security enforcement, temporal/provenance history, review, suppression/retraction effects and exports | No independent score reconstruction, destructive identity merge or guessed retention implementation. |

Person A/B labels from M map to these responsibilities; they do not displace B's DE/ML/EV/PL ownership. Named staffing can be added without changing these role boundaries.

## F. OUT-OF-SCOPE

Under CY-POL-035, excluded capabilities/claims include:

- Real-world identity production, automatic persona acceptance and automatic/destructive identity merging.
- Unauthorised access/probing, exploitation, credential theft, CAPTCHA evasion, authenticated criminal-market collection and broad live marketplace crawling.
- Tor enumeration, attacks on its cryptography, Monero tracing and biometric identification.
- Autonomous agentic attribution/collection and generative authority over core evidence/decisions.
- DS/SL fusion and GNN linkage as prototype implementations; new infrastructure not authorised by the existing Blueprint.
- Public datasets as PRAMANA actor truth, fabricated fields/weights/metrics, targets presented as achieved accuracy and synthetic results presented as live-world validation.
- Guaranteed court admissibility, automatic legal compliance, government endorsement, completed formal method validation or deployed/working capability without evidence.

Lawful source qualification and the engineering controls here are requirements, not fresh legal advice or claims of legal certification. Deferred work is not automatically out of scope: it remains explicitly conditional on its required contract and validation.

## G. VERSION = CYBER_SPEC_v1

**Artifact:** PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md  
**Layer:** Policy / domain  
**Frozen:** CY-POL-001–CY-POL-035, within their stated scope  
**Deferred:** DC-01–DC-09 and outstanding data/operational contracts OD-01–OD-04  
**Implementation/benchmark status:** Not established by this document  
**Change discipline:** Amendments identify affected rule IDs, source conflict/decision, contract and fixture impacts. Computational definitions require ML/EV delivery and validation; domain changes require Cyber review. This version does not silently amend project source files.
