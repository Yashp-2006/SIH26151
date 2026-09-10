# PRAMANA — Master Project Blueprint

**SIH Problem Statement 26151 — Dark Web Threat Actor De-Anonymization (NTRO)**
Status: authoritative source of truth. Supersedes the Gemini dossier where they conflict.
Date: 2026-08-28. Phase 3 output (synthesis, architecture, execution).

---

## 0. HOW TO READ THIS DOCUMENT

Three things in this blueprint override the research dossier, and the reasoning is in §2:

1. **We reject Dempster-Shafer / Subjective Logic as the fusion engine.** The dossier's headline innovation is mathematically the wrong tool for the problem it was chosen to solve, and its own feasibility audit concedes it is unbuildable by our team. Replaced with independence-aware capped log-likelihood-ratio fusion.
2. **We reject "stylometry is definitively broken" (dossier Tier A/E).** The two cited papers measure a different task and the inference is inverted. Stylometry is demoted, gated, and given a new inverse use. See §2.1 and §18.
3. **We reject the ">85% of attributions are OPSEC failures" figure as stated.** n=5, hand-coded, selection-biased. The direction survives; the number does not.

Everything else in the dossier that affects architecture is either adopted or adopted-with-correction, tracked in §2.

---

## 1. PART I — RESEARCH-TO-DESIGN SYNTHESIS

Not a summary of the dossier. Design consequences only.

### 1.1 What the research proves (Tier A, survives audit)

| Proven | Design consequence |
|---|---|
| Tor v3 descriptors are encrypted under blinded, rotating keys; HSDirs cannot learn or enumerate onion addresses | Discovery is an **OSINT problem, not a cryptographic one**. Collection is seed-driven. Capability 1 becomes a targeted scanner over known addresses, and *seed acquisition* becomes a first-class subsystem (§20) |
| Forensic evidential strength is properly expressed as a likelihood ratio under two competing propositions, not as a match percentage | The system's output primitive is an **LR with a stated defence hypothesis**, never "98% match" (§14) |
| Correlated evidence breaks naive multiplicative fusion; the same artefact mirrored across sites is one observation, not several | Independence accounting must be **in the data model**, not a post-hoc caveat (§12.3) |
| Naive transitive closure collapses adversarial identity graphs into giant components via shared hubs | No automatic transitive merge, ever. Constrained clustering + must-not-link vetoes + hub suppression (§11) |
| Bitcoin CIOH is degraded by CoinJoin/PayJoin/exchange batching; Monero RingCT+ring16 is not forensically traceable | Wallet signals are **capped, probabilistic edges**. A shared address never triggers a merge (§19) |
| LE-operated platforms (Hansa) exist in historical corpora | Source independence and provenance must be modelled per-platform; corpus is assumed partially adversarial (§8, §20) |
| Uncalibrated model scores induce automation bias in analysts | Calibration is a **shipping requirement**, with reliability diagrams in the product, not just the paper (§22) |
| Indirect prompt injection through ingested text is unsolved | LLMs never sit in the decision path and never see un-delimited scraped text with tool access (§15, §25) |
| Random train/test splits leak time; pairwise F1 misleads for ER | Temporal splits + cluster-level metrics + Cllr are mandatory in the harness from Phase 1 (§22) |

### 1.2 What it strongly suggests (Tier B, adopted with named caveats)

- Fellegi-Sunter-style probabilistic linkage beats deep ER at our scale and explains itself. Adopted; Splink as reference implementation, our own scorer for graph-aware signals.
- GNNs underperform simple topological heuristics on sparse cold-start graphs. Adopted for the prototype; not asserted as a general law.
- Historical dark web attribution has been dominated by operator error, financial tracing, and legal process rather than analytics. Adopted **as a framing argument**, not as a statistic.
- Post-takedown migration (multihoming) is the highest-yield behavioural window. Adopted, and made a first-class detector (§17).
- One Postgres carries the prototype. Adopted, aggressively (§29).

### 1.3 What is uncertain

- Base rates. Nobody knows the size of the reference population of dark web vendor operators, so absolute LRs are not obtainable. **Consequence:** we report LRs *relative to an explicitly declared reference population* (the corpus under analysis), state it on every assessment, and never imply population-independent probability.
- Optimal temporal decay functions per indicator class. **Consequence:** decay half-life is a per-indicator-class config value with a visible default, not a hardcoded constant (§9).
- Whether calibration fitted on synthetic/historical ground truth transfers to live data. **Consequence:** we report calibration *on the benchmark we defined*, and say so.

### 1.4 What is overhyped

| Overhyped | Verdict |
|---|---|
| "AI-driven automated attribution" (vendor claims) | Tier E. Uncalibrated similarity search with no defined reference population. Our slide contrasts against this. |
| Agentic autonomous investigation | Tier E for the decision path. Retained only as a scheduled, non-agentic pipeline (§15). |
| Dempster-Shafer / Subjective Logic as the fix for correlated evidence | Tier D→E as applied here. Dempster's rule of combination **assumes independent bodies of evidence** — it is not a remedy for non-independence. See §2.1. |
| GNNs for identity linkage at prototype scale | Tier C. Deferred to V3 with a stated data-volume trigger. |
| Zero-knowledge proofs for intelligence sharing | Tier D. Out of scope. |
| Conformal prediction as a forensic guarantee | Tier C. Exchangeability fails under drift and adversarial shift. Used only for candidate-set sizing in search, never for attribution claims. |

### 1.5 What is obsolete

- HSDir enumeration / passive onion discovery (dead since v2 deprecation, October 2021).
- "Descriptor inconsistency" analysis by third parties as the problem statement intends it.
- Treating a shared Bitcoin address as an identity join.
- Timezone inference from posting rhythm as a primary linkage signal.
- Any design assuming an unauthenticated, crawlable, enumerable dark web.

### 1.6 What is technically infeasible (for us, and stated as such publicly)

- Real-world identification of a person from onion-side data alone.
- Monero tracing to evidentiary standard.
- Passive discovery of unadvertised hidden services.
- Full Subjective Logic fusion over a bitemporal graph in the available time.
- Live authenticated marketplace collection without unlawful acts.
- Calibrated absolute LRs against the true global population of actors.

### 1.7 What is feasible for us

Provenance-sealed capture with hash chains; artefact-level deduplication; deterministic multi-signal extraction; capped log-LR fusion with independence grouping; hub/rarity weighting; must-not-link vetoes; bitemporal evidence ledger with retraction propagation; targeted misconfiguration scanning against a self-hosted Tor range; perceptual image hashing; PGP key-metadata forensics; template/artefact fingerprinting; gated stylometry plus style-discontinuity detection; hybrid search in Postgres; a graph/timeline/evidence analyst workspace; a validated benchmark with Cllr, Tippett plots, ablations and adversarial degradation; a grounded, tool-restricted copilot; sealed exportable reports.

### 1.8 Genuine innovation potential (ranked, all buildable)

1. **Evidence-family independence accounting with capped log-LR fusion** — solves the double-counting failure correctly and visibly. Nothing open-source does this for CTI.
2. **Forensic validation harness for an attribution system** — Cllr, Tippett plots, reliability diagrams, ablation and adversarial degradation as *product surfaces*, not appendices.
3. **Laundering-aware modality gating** — detect LLM-mediated/translated text and mark it stylometrically inadmissible instead of silently scoring it.
4. **Style-discontinuity detection as account-handover evidence** — the inverse use of stylometry the dossier missed entirely; directly attacks account resale, compromise, and staff rotation.
5. **PGP key-metadata forensics** — link *different* keys of one operator via creation-time, algorithm/preference profile, GnuPG version artefacts, subkey structure, user-ID conventions. Survives text laundering because it is not text.
6. **Counter-evidence engine with sequential-unmasking gate** — the system must argue against itself before a human can accept a merge.
7. **Retraction propagation over a bitemporal ledger** — retract one artefact, watch every dependent assessment recompute and re-open for review.

### 1.9 What must be removed from the project

Dempster-Shafer/Subjective Logic engine. GNNs. Kafka. Neo4j. Elasticsearch. Passive onion discovery. Autonomous agentic investigation. Any live crawling of real marketplaces during the hackathon. Any "real-world identity" output. Any percentage-match UI. Monero tracing. Any screen that does not serve the investigation loop.

### 1.10 Central design thesis

> **Attribution fails on the arithmetic of evidence, not on the shortage of it.** The scarce capability is not collection — it is knowing what a trace is *worth* once you accept that the adversary chose which traces you would find, that the same trace reaches you six times through five mirrors, and that some of your sources are hostile. PRAMANA is an evidence-accounting system: it turns fragmented observations into sealed, independence-weighted, rarity-calibrated evidence, fuses it into likelihood ratios under explicitly stated competing hypotheses, argues against its own conclusions, remembers what it believed and when, and hands a human a defensible lead — never a verdict.

---

## 2. RESEARCH INTEGRITY AUDIT

Dossier labels were **not** inherited. Findings that affect architecture were re-graded.

### 2.1 Findings downgraded, with reasons

| # | Dossier claim | Dossier tier | Our tier | Why |
|---|---|---|---|---|
| D4 | "Generative AI fundamentally breaks stylometric verification — LLM paraphrasing drops LUAR below the human cross-author floor" | A | **B, and re-derived** | **Claim–source mismatch, verified.** The cited papers (arXiv 2604.26460; arXiv 2608.19746) measure *LLM stylistic personalization* — whether an LLM can write **as** a target author. Result: LLM output scores 0.484–0.508 LUAR similarity to the target, below the cross-author human floor 0.626 (ceiling 0.756), because the *LLM's own fingerprint dominates*. That is a measurement of LLMs failing to imitate humans, not a measurement of paraphrase defeating a verifier. Also: the two titles are near-identical and almost certainly one body of work — the dossier double-counted its own evidence, committing the exact non-independence error it warns about. Both are 2026 preprints, not peer-reviewed. |
| D2 | ">85% of successful attributions rely on OPSEC failure / financial tracing / infrastructure compromise" | A | **B directional, number rejected** | Derived from a hand-coded table of **n=5** cases, all large public prosecutions. Selection bias: only successes that were charged publicly. Cause coding is unreliable because parallel construction and sealed methods hide the first lead. Direction is almost certainly right; "85%" is false precision. Use as narrative, never as a statistic on a slide. |
| D3 | "ENFSI explicitly prohibits automated categorical identity claims; LR is the sole sanctioned method" | A | **A on substance, C on framing** | ENFSI's evaluative-reporting guideline recommends the LR framework for forensic practitioners' evaluative opinions. It is guidance from a European body, not a prohibition, and carries no authority in India. Keep the LR framework (it is the right engineering answer); drop "prohibits" and "sole sanctioned". Note the guideline's real teeth: LR methods require **empirical validation** (Cllr, Tippett) — which the dossier under-states and we adopt (§22). |
| D10 | "Under BSA 2023 s.63, scraped data lacking immediate unbroken hash chains at ingestion is inadmissible" | A | **B, restated** | Overstated as law. s.63 (successor to IEA s.65B) requires a certificate in the statutory form covering the device/process; hash values appear in the schedule and case law treats hash as strong integrity proof. "No hash at capture ⇒ inadmissible" is not the statutory test. The *engineering* consequence is unchanged and cheap, so we implement seal-at-capture anyway — but we present it as **integrity best practice aligned to s.63**, not as a legal absolute. Cited SC ruling (SCC Online blog, 2026) unverified by us — do not cite from the stage. |
| D21/§36 | "Design the scoring architecture around Dempster-Shafer or Subjective Logic to solve non-independence" | A/B | **D→E as applied** | Two independent defects. (a) **Wrong tool:** Dempster's rule of combination *assumes independent bodies of evidence*; it manages *ignorance*, not correlation. It cannot fix mirrored evidence. It is also known to yield counterintuitive results under high conflict (Zadeh's example). (b) **Citation-by-keyword:** the four supporting sources are domain-adaptation, IoV trust management, and online-game partner selection papers — none concern forensic identity evidence. (c) The dossier's own feasibility audit concedes it is unbuildable and reduces to Splink + UI. Rejected. Replacement in §12. |
| D13 | "Behavioral temporal profiling is trivially defeated" | C | **C, kept, scope narrowed** | Agreed for timezone inference. Not true of *event-driven* co-timing (migration windows), which is a different mechanism and retained (§17). |
| Ref 23 | Rid & Buchanan *Attributing Cyber Attacks* cited as arXiv:2101.02899 | — | **Misattribution, confirmed** | The work is Rid & Buchanan (2015), *Journal of Strategic Studies* 38(1–2):4–37, DOI 10.1080/01402390.2014.977382. arXiv:2101.02899 is unrelated. Cite correctly or not at all. |

### 2.2 Systemic citation-quality defects in the dossier

Load-bearing claims resting on non-primary sources: Monero traceability on a **Reddit thread** (ref 9) and a tutorial site (10, 40); Tor v3 opacity on **Onionbalance API docs** (1) and a **Scribd upload** (39); "Tor cannot be enumerated" on a **vendor marketing blog** (22); Hansa honeypot on vendor blogs (15, 16); DST/SL on four off-domain papers (13, 14, 43, 44). In every case the underlying claim is defensible from primary sources — Tor `rend-spec-v3`, the Monero project's own RingCT/ring-size documentation and OSPEAD work, DOJ/Europol primary filings — so the fix is re-citation, not reversal. **Rule for the team: nothing goes on a slide or in a report citing a Reddit thread, Scribd, or a vendor blog.**

### 2.3 Findings upgraded or added (absent from the dossier)

| Added finding | Tier | Design consequence |
|---|---|---|
| Product-image reuse via perceptual hashing (pHash/dHash) is a strong, cheap cross-market vendor linker and is immune to text laundering | B | First-class modality, family F5 (§11.2) |
| PGP **key metadata** (creation timestamp, algorithm/size, cipher-preference list, GnuPG version artefacts, subkey structure, user-ID conventions) links *different keys* of one operator | C | New modality, family F1; a genuine differentiator (§11.2) |
| Listing/post **template structure** (section order, table layout, unit and price-rounding conventions, signature-block form) survives LLM prose rewriting because operators copy-paste | C | New modality, family F5 — the direct answer to style laundering (§16, §18) |
| Phishing/clone onions dominate mirror space; the clone's tell is **payment-address substitution** against an otherwise byte-similar page | B | Clone detector at ingest; prevents graph poisoning and doubles as evidence (§20.4) |
| Style *discontinuity within one account* is evidence of handover/compromise/staff rotation | C | Inverse stylometry detector (§18.3) |
| Cllr and Tippett plots are the forensic standard for validating an LR system | A | Core evaluation metric, in-product (§22) |
| DPDP Act 2023: a student team is **not** an exempt State instrumentality under s.17; the applicable ground is that personal data made publicly available by the data principal falls outside the Act | B | Data-minimisation is a design requirement, not optional (§25.4) |

---

## 3. PART II — CHALLENGING THE PROBLEM STATEMENT

We satisfy the **intent** of every requirement. We say plainly where the wording assumes a pre-2021 world. Doing this openly is a scoring advantage with an NTRO panel, not a concession.

| # | Original requirement | Problem with it | Modern interpretation | What we actually implement |
|---|---|---|---|---|
| 1 | "Deanonymize dark web threat actors and link them to suspect real-world entities" | Conflates four distinct operations; software cannot produce verified identity | Produce calibrated, evidence-backed **investigative leads** at pseudonym level; real-world identification remains a legal process | Four-tier output ladder (Correlation → Resolution → Hypothesis → Verified) with hard ceilings on what the system may assert (§14) |
| 2 | "Descriptor inconsistencies" in hidden services | Tor v3 encrypts descriptors under blinded rotating keys; third parties cannot enumerate or compare them | The intent is *infrastructure fingerprint inconsistency* — mismatches between what a service claims and what it serves | Targeted descriptor/service probing of **known** addresses: onion-address↔mirror-list consistency, `Onion-Location` mismatch, TLS SAN vs served host, OnionBalance instance-count anomalies, clone/address-substitution detection (§20.4) |
| 3 | "Continuously gathering footprints… autonomous mode" | The onion space cannot be enumerated; full autonomy over evidential conclusions is indefensible | Autonomous **collection and scoring**, human-gated **conclusions** | Scheduled seed-driven collectors + automatic re-scoring on every ingest + a mandatory human review gate before any assessment leaves the system (§5, §14) |
| 4 | "Matching with clearnet infrastructure to point to likely origin servers" | A match may point to a shared CDN, proxy, or bulletproof host, not an origin | Rarity-weighted infrastructure correlation producing *candidate* origin hypotheses | IDF/hub-weighted infra evidence with mandatory shared-hosting counter-check; output is "candidate origin, rarity r, alternative explanations listed" (§20.5) |
| 5 | "Single relationship graph" of handles/PGP/wallets/trust | A single undirected merge graph is exactly what collapses | Typed, provenance-bearing, weighted, bitemporal evidence graph with separate identity-resolution layer | Observation/Evidence/Entity/Hypothesis layer separation; no automatic transitive merge (§6, §10) |
| 6 | "Stylometric persona identification" to link rebranded personas | Degraded by obfuscation, translation, and LLM rewriting; topic-confounded | Stylometry as *candidate generation* and weak corroboration, plus non-prose text features | Gated stylometry with hard LR cap, laundering detector, template/artefact fingerprints as the robust substitute, style-discontinuity as handover evidence (§18) |
| 7 | "Behavioural profiling" | Timezone inference is trivially defeated | Event-driven behavioural continuity around lifecycle shocks | Migration-window co-timing detector, catalogue/price-structure continuity, trust-graph re-vouching patterns (§17) |
| 8 | "Attribution confidence" field | A single number invites misreading | Calibrated LR + verbal band + evidence-family count + explicit defence hypothesis | Assessment object with six fields, not one score (§14) |
| 9 | "Wallets" as identity | Address sharing ≠ same operator; CIOH degraded | Wallet activity as capped probabilistic evidence with uncertainty declared | Wallet edges never merge entities; CoinJoin/batching detection flags suppress clustering (§19) |
| 10 | Export to CSV / JSON / reports | Under-specified for evidential use | Exports must carry provenance or they are worthless downstream | CSV/JSON/STIX-2.1-aligned bundle + sealed PDF report with hash manifest and s.63-aligned integrity annexure (§28) |
| 11 | "Deep web… marketplaces, forums" continuous collection | Most real markets require registration/invite/payment — lawful autonomous access is largely unavailable | Collect from lawful strata only | Public onion index pages, historical released corpora, public CTI, public blockchain, CT logs, and our own Tor range (§20) |

**Requirement coverage note.** Every field the statement demands (actor profiles, handles, PGP keys, wallets, hidden-service indicators, persona linkages, attribution confidence, category, last scan date, source) exists in the data model (§7) and is exportable (§28). We add: provenance seal, evidence-family count, counter-evidence, review status, and validity interval.

---

## 4. PART III — THE PRODUCT

**Name: PRAMANA**
*Pramāṇa* (प्रमाण) is the Sanskrit epistemological term for a **valid means of knowledge** — the warrant that separates knowledge from mere belief. In classical Indian logic a claim without pramāṇa is not knowledge, however plausible. That is precisely this system's thesis, it is credible to an Indian government audience, and it is not a hacker name. Full form for decks: **PRAMANA — Evidence-Centric Attribution Platform for Dark Web Threat Actors**.

**Mission.** Convert fragmented dark web traces into sealed, independence-weighted evidence that yields calibrated, contestable, human-reviewed attribution leads an investigator can defend line by line.

**Problem.** Investigating dark web actors is not limited by data volume — public indexes, released corpora, blockchains and certificate logs already hold more than any team can read. It is limited by *evidential arithmetic*. The same listing reaches an analyst through five mirrors and counts five times. A marketplace's default PGP key merges four hundred unrelated vendors into one phantom actor. A shared bulletproof host "proves" a link between rivals. A framed vendor inherits a rival's planted wallet address. Existing tooling collects and correlates but cannot say how much any of it is worth, cannot show what argues against its own conclusion, and cannot show what it believed last month. The result is confident nonsense — the most expensive output an investigation can produce.

**Core insight.** *Weight of evidence, not volume of evidence.* Three properties decide whether a link is real, and no CTI platform models any of them: **independence** (how many genuinely separate origins does this evidence have?), **rarity** (how many other actors share this indicator?), and **exclusion** (what would have to be false for this link to hold?). PRAMANA makes all three first-class, computed, and visible.

**Core innovation.** Independence-aware, rarity-calibrated, capped log-likelihood-ratio fusion over a bitemporal, provenance-sealed evidence ledger, with a counter-evidence engine that must argue against every hypothesis before a human may accept it — validated with the same metrics forensic science uses to validate an LR method (Cllr, Tippett, reliability diagrams).

**Technical moat.** Not any single model. The moat is the **evidence accounting discipline**: the canonical-artefact deduplication layer, the evidence-family taxonomy with per-family caps, the hub/IDF rarity index, the must-not-link veto semantics, the retraction-propagation ledger, and the validation harness — plus a benchmark (RANGE + DW-ATTRIB-1) that makes our numbers reproducible and everyone else's unfalsifiable. A team that wires Maltego-style APIs to an LLM produces a demo; it cannot produce a Tippett plot.

**Killer interaction.** **The Evidence Balance Sheet** — select two personas, ask *"Why are these linked?"*, and receive a ledger: each supporting evidence item with its family, rarity, raw LR and *discounted* LR; the independence discount shown as an explicit subtraction with the reason ("3 items collapsed to 1 — same canonical artefact, mirrored on 3 sites"); counter-evidence with its own weight; hub suppressions listed; the fused LR, verbal band, and the defence hypothesis it was evaluated against; and a provenance link from any row to the sealed raw capture. One screen contains the entire product argument.

---

## 5. PART IV/V — SYSTEM THESIS AND INTELLIGENCE LIFECYCLE

### 5.1 System thesis

> Do not build a repository of indicators, and do not build a graph of guesses. Build an **evidence ledger** — append-only, sealed at capture, bitemporal — over which every relationship is a *computed, contestable, re-derivable claim* carrying its own independence accounting, its own rarity weighting, its own counter-evidence, and its own review history. The graph is a projection of the ledger, not the system of record. When an artefact is retracted, every conclusion that stood on it falls automatically and visibly.

The single sentence that must survive contact with a judge: **the graph is a view; the ledger is the truth; the human is the author of the conclusion.**

### 5.2 Lifecycle

`SEED → DISCOVERY → COLLECTION → SEAL → VALIDATION → NORMALIZATION → CANONICALIZATION (dedup/clone) → EXTRACTION → RARITY INDEXING → EVIDENCE CREATION → CANDIDATE GENERATION (blocking) → ENTITY RESOLUTION → COUNTER-EVIDENCE → INDEPENDENCE GROUPING → FUSION → ASSESSMENT → SEQUENTIAL-UNMASKING REVIEW → INTELLIGENCE PRODUCT`

Three deliberate departures from the sequence in the brief: **SEAL** is moved to immediately after collection (integrity must precede any transformation, or provenance is retrospective and worthless); **CANONICALIZATION** is promoted ahead of extraction (deduplicating after extraction means the double-counting has already entered the evidence table); **RARITY INDEXING** is inserted before evidence creation (an indicator's weight cannot be assigned without knowing its corpus frequency). **INDEPENDENCE GROUPING** sits between counter-evidence and fusion because grouping must see the full evidence set, positive and negative.

| Stage | Input | Processing | Output | Storage | Confidence effect | Provenance | Attack surface | Failure mode | Mitigation |
|---|---|---|---|---|---|---|---|---|---|
| SEED | Analyst input, index pages, mirror lists, historical corpora manifests | Seed registration with legal-basis tag | `source` rows with legal basis + reliability grade | `source` | none | operator identity, timestamp | poisoned seed lists | crawling a honeypot or clone | mandatory legal-basis + reliability field; clone check before promotion |
| DISCOVERY | Seeds | Follow only in-corpus links; harvest self-declared mirrors | candidate addresses | `onion_service` | none | discovering document hash | adversary-planted mirror lists | corpus inflation with clones | clone detector; degree cap per seed |
| COLLECTION | Addresses | Isolated headless fetch through per-target Tor circuit; WARC write | WARC + response metadata | object store (FS in MVP) | none | fetch time, circuit id, collector version | hostile HTML/JS, exploit, tracking | crawler compromise/deanon | network-isolated ephemeral container, no clearnet egress, JS off by default |
| SEAL | WARC | SHA-256 over payload; append to per-run hash chain; optional RFC 3161 token | `artefact` with `content_hash`, `chain_prev`, `chain_hash` | `artefact` | none | the seal itself | tampering, backdating | unprovable integrity | chain verified on every read; seal before parse; verification endpoint in UI |
| VALIDATION | Sealed artefact | Illegal-content hash screen (drop-on-match, no store), MIME/size checks, robots/legal-basis check | pass / quarantine / drop | `artefact.status` | none | decision logged | CSAM/illegal material ingress | legal and ethical catastrophe | drop-on-match at queue head; no persistence of dropped payload; incident log only |
| NORMALIZATION | Validated artefact | Boilerplate strip, encoding/lang detect, transliteration normalize, timestamp→UTC + declared tz | normalized document | `document` | none | transform id + version | parser injection | silent content mangling | golden-file parser tests; parser version on every doc |
| CANONICALIZATION | documents | content hash, SimHash (64-bit, Hamming ≤3), image pHash, shingle containment for quotes, clone/address-substitution check | `canonical_artefact_id`, mirror/quote/clone edges | `canonical_artefact`, `doc_relation` | **decisive** — sets independence groups | all member doc ids | adversary crafts near-dups to evade grouping | double counting; clone poisoning | thresholds tuned on RANGE; clone flag suppresses all evidence from clone |
| EXTRACTION | normalized docs | regex/checksum validators for BTC/XMR/PGP/jabber/onion; NER for handles/products; PGP packet parse; template structure parse; EXIF | typed `indicator` mentions | `indicator`, `mention` | none yet | doc id + extractor version | prompt injection if LLM used | fabricated indicators | deterministic extractors are authoritative; any LLM extraction flagged `machine_suggested`, requires validator pass |
| RARITY INDEXING | indicator corpus | per-indicator account/site frequency; IDF; hub flag if accounts > τ | `indicator.rarity`, `indicator.is_hub` | `indicator` | scales all LRs | corpus snapshot id | corpus flooding to dilute rarity | hub-driven false merges | hub contribution forced to zero and displayed; rarity recomputed per snapshot, snapshot id stored on evidence |
| EVIDENCE CREATION | indicators + canonical artefacts | instantiate typed evidence linking two accounts/entities, with family, direction, raw LR, validity interval | `evidence` rows | `evidence` | assigns raw weight | full chain to artefact | fabricated linkage | unsupported edges | evidence cannot exist without a canonical artefact reference (FK enforced) |
| CANDIDATE GENERATION | accounts | blocking on identifiers, pHash buckets, template hash, embedding ANN, username variants | candidate pairs | `candidate_pair` | none | blocking key | candidate explosion | O(n²) or missed pairs | multi-key blocking with recall measured on RANGE |
| ENTITY RESOLUTION | candidate pairs + evidence | per-pair scoring, constrained clustering, no transitive closure | `pair_score`, provisional clusters | `pair_score`, `cluster` | pairwise | evidence ids per pair | poisoned edges | giant-component collapse | must-not-link vetoes, hub suppression, cluster-size and purity alarms |
| COUNTER-EVIDENCE | pair + all evidence | run exclusion detectors (§13) | negative evidence + veto flags | `evidence(polarity=neg)`, `must_not_link` | reduces or vetoes | detector version | suppression of counter-evidence | overconfident merge | counter-evidence run is mandatory and its absence is itself displayed ("no exclusion checks passed yet") |
| INDEPENDENCE GROUPING | evidence set | group by `(canonical_artefact, family, source_cluster)`; within-family damping | grouped evidence with discount ledger | `evidence_group` | **decisive** | group membership | crafted diversity of origin | inflated confidence | discount shown as explicit subtraction in UI; family count `k` published |
| FUSION | grouped evidence | capped log-LR sum, counter-evidence subtraction, veto check, calibration map | LR, calibrated posterior, band, `k` | `assessment` | final | full evidence tree | parameter tampering | miscalibration | params version-pinned per assessment; recompute-on-demand; `k<2 ⇒ band capped at "weak"` |
| ASSESSMENT | fused result | attach competing hypotheses, reference population, limitations | `assessment` object | `assessment` | expressed | model+param versions | overclaiming | analyst misreads score | verbal band mandatory, numeric secondary, defence hypothesis printed |
| REVIEW | assessment | sequential unmasking: raw evidence first, strongest counter-evidence second, score last; accept/reject/defer with rationale | reviewed assessment | `review` | human authority | analyst id, time, rationale | confirmation bias, feedback poisoning | rubber-stamping | order enforced by UI; rationale mandatory; analyst-confirmation labels quarantined from calibration set (§24.6) |
| PRODUCT | reviewed assessments | report render, CSV/JSON/STIX export, hash manifest | sealed report + exports | `report` | communicated | manifest of every artefact cited | leakage, tampering | undefensible output | every claim in the report footnotes an artefact hash; report itself sealed and chained |

---

## 6. PART VI — THE INTELLIGENCE FABRIC

Nine layers. The point of the separation is that **every collapse between adjacent layers is a known category of investigative failure**, and naming them makes the failure impossible to commit silently.

| Layer | Holds | Collapse it prevents |
|---|---|---|
| **Observation** | Raw sealed captures, immutable | Treating a re-scrape as a new fact |
| **Evidence** | Observations interpreted as relevant to a question, with family, rarity, validity | Treating raw data as evidence without asking "relevant to what?" |
| **Entity** | Accounts, keys, wallets, services — things that exist | Treating a *hypothesised actor* as a thing that exists |
| **Relationship** | Typed, weighted, time-bounded edges between entities | Treating co-occurrence as a relationship |
| **Temporal** | Valid-time and belief-time for every fact and claim | Treating today's belief as always-true |
| **Hypothesis** | Named competing propositions about identity | Treating a high score as a conclusion |
| **Confidence** | Calibrated LRs, bands, independence counts | Treating an uncalibrated similarity as a probability |
| **Analyst** | Review decisions, rationales, case state | Treating machine output as authored intelligence |
| **Product** | Reports, exports, manifests | Treating a database view as a defensible statement |

The rule enforced in code: **a layer may only reference the layer(s) below it, never above.** Evidence cannot cite a hypothesis. An entity cannot be created by a fusion result. This is a foreign-key discipline, not a philosophy.

---

## 7. PART VII — CANONICAL DATA MODEL

Universal columns on every substantive table: `id`, `created_at` (transaction time), `valid_from` / `valid_to` (valid time), `source_id`, `confidence` (where meaningful), `status`, `provenance_ref`, `extractor_version`, `retracted_at`.

### 7.1 Core entities

| Entity | Key identifiers | Key properties | Notes |
|---|---|---|---|
| `source` | site/corpus id | type, legal_basis, reliability_grade (A–F), credibility_default (1–6), independence_cluster, is_le_operated_suspected | Independence cluster groups mirrors and known-affiliated platforms |
| `artefact` | content_hash | warc_ref, fetch_time, collector_version, chain_prev, chain_hash, rfc3161_token, status | Immutable. Never updated, only superseded |
| `canonical_artefact` | id | representative_artefact, member_count, simhash, phash, clone_of, is_clone | The independence anchor |
| `document` | id | artefact_id, lang, script, normalized_text, template_hash, boilerplate_removed | |
| `account` | (platform, handle) | display_name, registration_time, last_seen, role (vendor/buyer/staff/bot/unknown), status | The *observed* identity. Never merged destructively |
| `persona` | id | label, member_accounts[], formation_evidence[], review_state | A **reviewed** cluster of accounts. Created only by human acceptance |
| `actor` | id | label, member_personas[], assessment_ceiling | Highest abstraction. Explicitly *not* a real-world person |
| `alias` | string | normalized_form, variants[], first_seen, rarity | Handles are evidence, not identity |
| `pgp_key` | fingerprint | algo, bits, created_at, uids[], subkey_struct, cipher_prefs, version_artefact, keyserver_first_seen, is_hub | Metadata fields are what enable cross-key linkage |
| `wallet_address` | address | chain, first_seen, last_seen, cluster_id, cluster_method, cluster_confidence, coinjoin_flag, exchange_flag, is_hub | Cluster membership is an opinion, stored as such |
| `transaction` | txid | chain, time, inputs, outputs, mix_indicators | Retained only where evidentially used |
| `onion_service` | onion_address | v3_pubkey, first_seen, last_seen, uptime_samples, descriptor_observations, is_clone, clone_of | |
| `infra_artefact` | (type, value) | type (tls_cert / favicon_hash / asset_hash / banner / header_order / ssh_hostkey / analytics_id / clock_skew), value, rarity, is_hub | The Capability-1 payload |
| `domain` / `ip` / `certificate` | fqdn / addr / sha256 | first_seen, last_seen, ct_log_ref, san_list, issuer, shared_host_flag | `shared_host_flag` is mandatory before any origin claim |
| `contact_id` | (type, value) | type (jabber/session/telegram/email/tox), value, rarity | Often the strongest non-crypto linker |
| `listing` / `post` / `message` | id | account_id, document_id, category, price, currency, ship_from, ship_to, template_hash, images[] | |
| `image` | phash | dhash, exif_json, first_seen, reuse_count | |
| `indicator` | (type, value) | rarity, idf, account_count, site_count, is_hub, snapshot_id | The rarity index lives here |
| `evidence` | id | family (F1–F9), polarity (+/−), subject_a, subject_b, canonical_artefact_id, raw_log_lr, rarity_factor, validity_interval, detector_version, independence_key | The heart of the model |
| `evidence_group` | id | family, independence_key, member_evidence[], damped_log_lr, discount_reason | Materialised discount ledger |
| `must_not_link` | (a, b) | reason_code, evidence_id, asserted_by, strength (hard/soft) | Hard = veto |
| `hypothesis` | id | proposition, defence_hypothesis, reference_population, subject_a, subject_b, status | Competing propositions are explicit text |
| `assessment` | id | hypothesis_id, log_lr, calibrated_posterior, prior_used, verbal_band, family_count_k, params_version, limitations[], superseded_by | Recomputable, versioned |
| `review` | id | assessment_id, analyst_id, decision, rationale, unmasking_order_log, time | Audit-grade |
| `investigation` / `case` | id | title, question, scope, entities[], assessments[], state, owner | |
| `analyst` | id | role, clearance_attrs, active | ABAC subject |
| `report` | id | case_id, rendered_hash, artefact_manifest[], generated_at, signed_by | Sealed like an artefact |

### 7.2 Relationship (edge) types

Typed, directional where meaningful, always weighted and time-bounded: `uses_key`, `controls_address`, `posted`, `mirrors`, `quotes`, `clone_of`, `serves_on`, `presents_cert`, `shares_infra_artefact`, `contacted`, `vouches_for`, `trades_with`, `migrated_to`, `succeeds` (temporal succession), `same_operator_hypothesis`, `distinct_operator_asserted` (must-not-link), `derived_from` (provenance), `retracts`.

Every edge carries: `type`, `direction`, `strength (damped log-LR contribution)`, `evidence_group_ids[]`, `counter_evidence_ids[]`, `valid_from/valid_to`, `belief_from/belief_to`, `rarity`, `detector_version`, `is_hub_suppressed`. An edge with no `evidence_group_ids` cannot be written — enforced by constraint, not convention.

---

## 8. PART VIII — EVIDENCE MODEL

Evidence is a first-class object with an enforced chain. Every claim in a report can be walked back to a byte range in a sealed capture:

`SOURCE → ARTEFACT (sealed) → CANONICAL_ARTEFACT (dedup anchor) → DOCUMENT (normalized) → INDICATOR (extracted, rarity-indexed) → EVIDENCE (typed, family, weighted) → EVIDENCE_GROUP (independence-discounted) → RELATIONSHIP → HYPOTHESIS → ASSESSMENT → REVIEW → REPORT`

### 8.1 Fields every evidence item carries

| Field | Purpose |
|---|---|
| `acquisition_time` / `event_time` / `valid_interval` | separates when we saw it, when it happened, when it was true |
| `source_reliability` (A–F) and `information_credibility` (1–6) | Admiralty-style grading, stored separately because a reliable source can carry a doubtful item |
| `independence_key` | `(canonical_artefact_id, family, source_independence_cluster)` — the grouping key that makes double counting impossible |
| `rarity_factor` | corpus-derived, with `snapshot_id` so the score is reproducible |
| `raw_log_lr` / `damped_log_lr` | before and after independence discounting; both shown |
| `polarity` | supporting or exclusionary |
| `corroboration_refs` | other *independent* evidence groups agreeing |
| `detector_version` / `model_version` / `params_version` | reproducibility |
| `analyst_notes` | human annotation, never overwriting machine fields |
| `retracted_at` / `retraction_reason` | retraction is a fact, not a delete |
| `revision_of` | evidence is versioned, not edited |

### 8.2 Non-negotiable rules

1. Nothing is ever hard-deleted. Retraction sets `retracted_at` and triggers propagation (§9.3).
2. Evidence without a `canonical_artefact_id` cannot exist.
3. Evidence from a `is_clone = true` artefact is created but permanently `suppressed`, visible with the reason.
4. Analyst annotations and machine outputs occupy different columns and are differently coloured in the UI. Forever.
5. A report may cite only reviewed assessments, and must embed the artefact hash manifest.

---

## 9. PART IX — TEMPORAL INTELLIGENCE

Bitemporal modelling is justified, and for one concrete reason rather than elegance: **the corpus contains platforms that were later revealed to be law-enforcement-operated or clone-operated.** When that revelation arrives, every conclusion built on that platform's content must fall — and an investigator must be able to show a reviewer exactly what was believed before and after. Without belief-time, that is unreconstructible.

### 9.1 Five clocks

| Clock | Meaning | Stored as |
|---|---|---|
| Event time | when the thing happened in the world (post authored, tx mined) | `event_time` |
| Observation time | when we captured it | `artefact.fetch_time` |
| Valid time | interval during which the fact held | `valid_from` / `valid_to` |
| Belief time | interval during which *we asserted* it | `belief_from` / `belief_to` |
| Assessment/revision time | when a conclusion was computed or revised | `assessment.created_at`, `revision_of` |

### 9.2 Queries the system must answer

"What did we know on 12 June?" · "When did we first believe these two were linked?" · "Which of tonight's assessments depend on artefacts we have since retracted?" · "Show this actor's infrastructure as it stood during the migration window" · "Which conclusions changed when we downgraded that source?"

Implementation at prototype scale: `valid_from/valid_to` + `belief_from/belief_to` columns with `tstzrange` and GiST indexes, plus an `as_of(ts)` SQL view layer. No temporal database product needed.

### 9.3 Retraction propagation (a signature capability)

Retract an artefact → mark dependent `evidence` retracted → mark affected `evidence_group` stale → recompute affected `assessment` rows into new versions with `superseded_by` set → set every affected reviewed assessment back to `REVIEW_REQUIRED` and notify the case owner → record the whole cascade in an `impact_log` the analyst can read as "this retraction changed 3 assessments, 1 dropped from *moderate support* to *weak*."

### 9.4 Temporal decay

Per-indicator-class half-life, exposed as configuration with a stated default, because the research offers no consensus and a hidden constant would be a lie: IP/ASN 30 d · TLS certificate 90 d · favicon/asset hash 180 d · contact identifier 365 d · wallet address 365 d · PGP fingerprint none (cryptographic identity does not expire, though *control* may) · image pHash none · template hash 180 d · stylometric 90 d. Decay multiplies the rarity-weighted LR, never the raw evidence record.

---

## 10. PART X — GRAPH ARCHITECTURE

**Decision: the graph is a logical projection over relational tables, not a separate database.** Eight logical layers, one physical store, typed edges, materialised views per layer.

| Logical layer | Edge types | Exists physically? |
|---|---|---|
| Identity | uses_key, alias_of, same_operator_hypothesis, distinct_operator_asserted | typed edges in `relationship` |
| Communication | contacted, shares_contact_id | typed edges |
| Financial | controls_address, co_spends_with, cluster_member | typed edges + `wallet_cluster` table |
| Infrastructure | serves_on, presents_cert, shares_infra_artefact | typed edges |
| Behavioural | migrated_to, succeeds, co_active_window | typed edges, computed |
| Linguistic | style_similar_to, style_discontinuity_at | typed edges, computed, gated |
| Evidence | derived_from, supports, contradicts | FK relations, not user-visible as graph edges |
| Hypothesis | assesses, vetoes | FK relations |

Rationale: at our node counts (10⁴–10⁵ in the prototype, ≤10⁷ projected) recursive CTEs with depth limits outperform the operational cost of a second database, and keeping edges in the same transaction as their evidence is what makes the FK integrity rules of §7.2 enforceable at all. Migration trigger to a dedicated graph engine is stated in §29.4.

### 10.1 Graph principles, enforced mechanically

| Pathology | Mechanism that prevents it |
|---|---|
| Hairball | expand-on-demand only, default depth 1, degree cap 25 per expansion, semantic zoom, no "load all" control exists |
| Hub dominance | rarity index; `is_hub` when an indicator touches > τ accounts (τ default 12, tuned on RANGE); hub edges rendered dashed grey, contribute 0 to fusion, and are *listed* as suppressed |
| Transitive merge collapse | no transitive closure anywhere in the codebase; clustering is constrained, must-not-link is a hard veto; cluster-size and purity alarms at ingest |
| Unsupported edges | FK constraint: no edge without an evidence group |
| Stale edges | decay + `valid_to`; edges outside the view's `as_of` window are hidden, not deleted |
| Hidden provenance | every edge in the UI has a provenance affordance; an edge whose chain fails verification renders red |
| Circular evidence | independence grouping; plus a cycle check that refuses to let an assessment's evidence include anything `derived_from` that assessment |

---

## 11. PART XI — ENTITY RESOLUTION ENGINE

### 11.1 Workflow

`BLOCK → SCORE PER SIGNAL → COUNTER-CHECK → GROUP FOR INDEPENDENCE → FUSE → BAND → GATE → HUMAN DECISION → PERSONA (reviewed)`

Blocking keys (multi-key union, recall measured, never a single key): exact identifier match (PGP fp, wallet, contact id) · pHash bucket · template hash · username normalized form + variant generation (leet/separator/transliteration) · embedding ANN top-k · co-occurrence in the same trust/vouch neighbourhood.

**The system outputs candidate relationships with weights. It never performs an automatic identity merge.** `persona` rows are created only by a human accept action, and remain reversible.

### 11.2 Signal families, with initial caps

Caps are in log₁₀ LR and are **initial priors to be recalibrated empirically on RANGE** — they are a tuning surface, deliberately exposed, not physics.

| Family | Signals | Cap | Why capped there |
|---|---|---|---|
| **F1 Cryptographic** | PGP fingerprint identity; PGP key-metadata similarity (creation time-of-day, algo/bits, cipher-preference vector, version artefact, subkey structure, UID convention); SSH host key reuse | 4.0 | Strongest available, but key sharing, key theft, and vendor-account resale are real; hub check mandatory |
| **F2 Financial** | address reuse; co-spend cluster co-membership; deposit-address overlap; temporal payment cadence | 2.0 | CIOH degraded by CoinJoin/PayJoin/batching; label provenance weak |
| **F3 Infrastructure** | TLS cert/SAN, favicon + static-asset hash, server banner, header order, error-page fingerprint, analytics/ad id, clock skew, SSH hostkey, ASN/host | 2.5 | Shared hosting and CDNs; competent operators remediate; diminishing returns over time |
| **F4 Contact identifiers** | jabber/XMPP, Session, Telegram, tox, email, self-declared mirror lists and PGP-signed migration notices | 3.0 | Rarely shared, often carried across markets deliberately; PGP-signed self-declarations are near-decisive but forgeable in unsigned form |
| **F5 Content artefacts** | product-image pHash reuse; EXIF cluster; listing/post **template structure** hash; price-rounding and unit conventions; verbatim non-boilerplate text reuse; signature-block form | 2.5 | Robust to prose laundering because copy-pasted; but templates are also copied *between* vendors — rarity weighting essential |
| **F6 Linguistic style** | stylometric verification score (char n-gram + style embedding) | **1.0** | Adversarially fragile, topic-confounded, degraded by translation and LLM mediation. Corroboration only, never load-bearing |
| **F7 Behavioural/temporal** | migration-window co-timing; lifecycle co-occurrence; catalogue-continuity; activity-rhythm similarity | 0.7 | Automation and staff rotation defeat rhythm; event-driven co-timing is stronger than continuous rhythm but still coarse |
| **F8 Social/trust** | co-vouching, shared endorsements, reciprocal trade links, moderator statements | 1.0 | Manufacturable by sybils |
| **F9 External corroboration** | public indictments, official takedown notices, credible published research, verified leaks | 3.0 | High value, but honeypot/disinformation risk and provenance must be graded |

**Global output ceiling: 4.0 log₁₀ LR (i.e. "strong support") at pseudonym level. No real-world-identity LR is ever emitted.** We cap ourselves, and we say so on the slide — it is the most credible thing in the deck.

### 11.3 Adversarial cases handled explicitly

| Case | Mechanism |
|---|---|
| Shared / staff / role accounts | `account.role` classification; multi-operator indicator (concurrent sessions, style variance within account, contradictory tz) sets `multi_operator_suspected`, which caps F6/F7 to 0 and warns on any merge |
| Compromised account | style-discontinuity detector + abrupt template/contact change + trust-graph anomaly → emits a **temporal split proposal**: account timeline is divided into segments, and resolution operates on segments, not accounts |
| Account resale / identity leasing | same mechanism as above; a segment boundary with a PGP key rotation and catalogue replacement is the resale signature; `succeeds` edge instead of `same_operator` |
| Hub signals | rarity index, `is_hub`, contribution zeroed and displayed |
| Aliases | treated as evidence with rarity weight, never as identity |
| Impersonation / false flag | rarity + independence (a framing attack usually yields a single evidence family, so `k=1` caps the band at *weak*); plus counter-evidence detectors (§13); plus first-seen ordering check (who used the indicator first) |
| Must-link | analyst-asserted, recorded as evidence with analyst provenance, never silent |
| Must-not-link | hard veto: fusion refuses to emit above *no support*, and the pair is quarantined from clustering |
| Reversible merges | `persona` membership is bitemporal; unmerge is an ordinary operation that triggers §9.3 propagation |

### 11.4 Reference implementation choice

Splink (Fellegi-Sunter, SQL backend, MoJ-maintained) for the tabular identifier-based comparison layer where its m/u-probability machinery is directly applicable; our own scorer for graph-aware, rarity-weighted and grouped signals that Splink does not model. We do not force everything through Splink, and we do not write our own EM estimation — this split is the laziest correct division of labour.

---

## 12. PART XII — EVIDENCE FUSION ENGINE

### 12.1 Options evaluated

| Approach | Explainability | Cost | Handles conflict | Handles correlated evidence | Handles ignorance | Prototype fit | Verdict |
|---|---|---|---|---|---|---|---|
| Naive Bayes / independent LR product | high | trivial | poor | **no — actively broken by it** | no | high | rejected alone |
| **Capped log-LR sum with independence grouping + calibration** | **high** | **trivial** | via signed weights + vetoes | **yes, structurally** | via `k` and explicit *insufficient* class | **high** | **SELECTED** |
| Bayesian network with shared latent parents | medium | medium | good | yes, if structure known | yes | low (structure unknown) | deferred to V2 for the 2–3 correlations we can actually specify |
| Dempster-Shafer | low | high | poorly (Zadeh conflict) | **no — Dempster's rule assumes independent bodies of evidence** | yes | low | **rejected** |
| Subjective Logic | low | high | fair | only via ad-hoc discounting | yes | low | **rejected** |
| Learned pairwise classifier (GBM) | medium (SHAP) | low | learned | no | no | medium | used only as a *candidate ranker*, never as the reported score |

The dossier's central recommendation is rejected on a specific technical ground worth stating aloud to judges: **Dempster's rule of combination presupposes independent bodies of evidence, so it cannot be the remedy for evidence non-independence.** Correlated evidence is fixed *upstream*, by identifying that six observations are one artefact — a data-modelling problem, not a fusion-algebra problem.

### 12.2 The selected computation

```
For each evidence family f:
  groups(f) = evidence in f grouped by independence_key
  for each group g: w_g = rarity_weighted_log_lr(strongest member) * decay(t)
  W_f = max_g(w_g) + λ * Σ_{other g} w_g        # λ = 0.2, diminishing returns
  W_f = min(W_f, cap_f)                          # per-family cap, §11.2
  if any member is_hub or is_clone: contribution forced to 0, recorded

TotalLogLR = Σ_f W_f  −  Σ_f CounterWeight_f
k = count of families with W_f > 0                # evidence-family count

if hard must_not_link exists  → band = EXCLUDED, no numeric emitted
if k < 2                      → band capped at "weak support"    # single-family rule
TotalLogLR = min(TotalLogLR, 4.0)                 # global ceiling

Posterior = calibrate(TotalLogLR, prior_declared)  # isotonic/logistic on RANGE dev set
```

Three properties matter more than the formula: every term is attributable to a named evidence group and printable as a table row; **the single-family rule** (`k < 2 ⇒ weak`) defeats most framing and poisoning attacks for free, because a planted indicator is one family; and the whole thing recomputes in milliseconds, which is what makes retraction propagation and live ablation demonstrable on stage.

### 12.3 Evidence double-counting — the explicit mechanism

One artefact reaching us as a post, a mirror, a quoted repost, a duplicate scrape, a derived indicator and an embedding is **one** piece of evidence. Enforcement, in order:

1. **Exact:** SHA-256 content hash → same `artefact`.
2. **Near-duplicate:** 64-bit SimHash over shingles, Hamming ≤ 3 → same `canonical_artefact`.
3. **Quote/repost:** shingle containment ≥ 0.8 of the shorter document → `quotes` edge, evidence inherits the *original's* independence key.
4. **Image:** pHash Hamming ≤ 6 → same canonical image.
5. **Mirror/site:** platforms whose pairwise document overlap exceeds 0.6 are placed in one `source_independence_cluster`; evidence from the same cluster shares an independence key.
6. **Clone:** byte-similar page with substituted payment address → `is_clone`, all evidence permanently suppressed with reason.
7. **Derivation:** any indicator or embedding inherits the independence key of the document it came from. A derived feature is never independent of its source.

The UI shows this as a subtraction with a sentence, e.g. *"4 items → 1 group. Same canonical artefact, mirrored across market-A, market-A-mirror2, forum-B repost. Discount −1.8 log LR."* This single visible line is the most persuasive thing in the product to anyone who has done real analysis.

---

## 13. PART XIII — COUNTER-EVIDENCE ENGINE

A signature feature: the system must attack its own hypothesis before a human may accept it. Six detector classes run on every scored pair; **their non-execution is displayed**, so silence is never mistaken for absence of contradiction.

| Detector | Fires when | Effect |
|---|---|---|
| **Temporal impossibility** | Accounts show overlapping sessions closer than a plausible switching interval; or one account is active during a window the other is verifiably absent/incarcerated (F9 source) | hard `must_not_link` (overlap) or strong negative weight |
| **Language/competence contradiction** | One account demonstrates competence (idiomatic production, error patterns) the other consistently lacks; script/locale contradictions | negative weight, F6 zeroed |
| **Lifecycle contradiction** | Account A's activity begins only after B's terminal event in a pattern consistent with succession rather than identity; catalogue/price discontinuity | reclassifies edge to `succeeds`, blocks `same_operator` |
| **Independence collapse** | All supporting evidence traces to one canonical artefact or one source cluster (`k = 1`) | band capped at *weak*, warning shown |
| **Hub/rarity contradiction** | The linking indicator is a hub (default key, stock image, market template) | contribution zeroed, edge marked suppressed |
| **Shared-infrastructure alternative** | Infra match explainable by CDN / shared host / hosting panel / common CMS default | negative weight and a printed alternative explanation |
| **Framing-pattern** | Single-family evidence appearing shortly after a public dispute between the two accounts; indicator's first-seen precedes on the *other* account | negative weight + `framing_suspected` flag |

**Output contract for every major relationship** — the six-panel Balance Sheet: Supporting Evidence (grouped, discounted, rarity shown) · Counter-Evidence · Independence (`k`, groups collapsed, discount) · Temporal Consistency · Source Reliability (per source, A–F/1–6, LE-operated suspicion flagged) · Assessment (LR, band, defence hypothesis, limitations, what would change the conclusion).

---

## 14. PART XIV — ATTRIBUTION WORKFLOW AND LANGUAGE

No "98% match" exists anywhere in the product. The assessment object:

```
HYPOTHESIS      Account "greenleaf_77" (market-A) and "GL77" (forum-B)
                are operated by the same operator.
DEFENCE HYP.    They are operated by different operators drawn from the
                vendor population of this corpus (n = 4,182 accounts).
REFERENCE POP.  Corpus snapshot 2026-08-21, vendor accounts, cannabis category.
EVIDENCE        F1 PGP key-metadata similarity      +2.1  (rarity 0.94)
                F4 shared Session ID                +2.6  (rarity 0.99)
                F5 product-image pHash reuse ×7     +1.9  (grouped from 23 items)
                F7 migration co-timing              +0.5
                                    grouped subtotal +7.1 → capped +4.0
COUNTER-EVID.   F3 shared host is a known multi-tenant panel  −0.4
                Style divergence (F6 zeroed: LLM-mediated text detected)
INDEPENDENCE    k = 4 families; 31 raw items → 11 groups; discount −2.7
ASSESSMENT      log10 LR = 3.6  →  STRONG SUPPORT for same-operator
                Calibrated posterior at declared prior 1e-3: 0.80
CALIBRATION     Cllr 0.19 on DW-ATTRIB-1 held-out temporal split
LIMITATIONS     PGP key material could be shared or stolen; image reuse is
                consistent with a reseller relationship; no clearnet evidence.
WOULD CHANGE IT Proof of concurrent sessions; evidence of catalogue resale.
HUMAN STATUS    UNREVIEWED → UNDER REVIEW → ACCEPTED / REJECTED / DEFERRED
```

**Verbal scale** (forensic convention, and the only thing the UI shows large):

| log₁₀ LR | Band |
|---|---|
| < 0 | Support for *different* operators |
| 0 | No support either way |
| 0–1 | Weak support |
| 1–2 | Moderate support |
| 2–3 | Moderately strong support |
| 3–4 | Strong support |
| > 4 | **Not emitted.** Ceiling by policy |
| any, with hard veto | **EXCLUDED** |

Four-tier claim ladder, printed in the UI header of every assessment: **Correlation** (indicators co-occur) → **Identity Resolution** (pseudonym-level, LR-backed) → **Attribution Hypothesis** (structured, reviewed, still a hypothesis) → **Verified Identity** (**out of system scope — requires legal process**). Tier 4 is rendered greyed out and unreachable. That greyed-out box is a deliberate rhetorical device for the judges.

---

## 15. PART XV — AI/ML ARCHITECTURE

Selective by layer. The decision path contains **no** generative model.

| Layer | Techniques | Role | Authority |
|---|---|---|---|
| Deterministic extraction | regex + checksum validators (BTC base58/bech32, XMR, PGP armor + packet parse, onion v3 checksum, jabber/email), EXIF, HTTP/TLS parsing, template structure parse | primary extraction | **authoritative** |
| Classical ML | gradient-boosted pairwise ranker (candidate ordering only); logistic/isotonic calibration; SimHash/pHash/MinHash; TF-IDF rarity | candidate generation, calibration | advisory (ranker), authoritative (calibration map) |
| NLP | multilingual NER for handles/products/locations; language + script ID; transliteration normalization; boilerplate removal | normalization + extraction assist | advisory, validator-gated |
| Embeddings | multilingual sentence embeddings for semantic search; style embeddings for F6; image pHash/embeddings | retrieval + weak corroboration | advisory, capped |
| Graph analysis | recursive-CTE traversal, degree-limited expansion, Jaccard/Adamic-Adar on shared neighbours, weighted shortest path for "strongest path" | structure + explanation | advisory |
| Statistical | rarity/IDF index, Cllr, ECE, bootstrap CIs, temporal splits | measurement | authoritative |
| LLM | normalization assistance, schema-constrained extraction *suggestions*, translation assistance, semantic query expansion, analyst Q&A over retrieved evidence, first-draft report prose | assistance only | **never authoritative** |
| Human | hypothesis acceptance, conclusion authorship | decision | **sole authority** |

### 15.1 LLM rules (hard)

1. No LLM output ever writes to `evidence`, `pair_score`, `assessment`, `must_not_link`, or `persona`. Enforced at the data-access layer, not by prompt.
2. LLM extraction lands in a `machine_suggested` staging table and must pass a deterministic validator (checksum, format, presence in source text) before promotion.
3. Every copilot answer cites `evidence_id`s; an answer with no citation is not rendered.
4. Scraped content reaching a model is delimited, provenance-labelled, and stripped of instruction-like structures; the model has **no tools** in the same context as untrusted text (§25.3).
5. Report prose is a draft that an analyst must edit and sign; generated text is visually marked until signed.
6. No agentic loop plans or executes collection.

---

## 16–18. MODALITY DECISIONS

### 16. Stylometry — demoted, gated, and re-purposed

**Role: candidate generation + weak corroboration. Cap 1.0 log LR. Never load-bearing. Never the reason for a merge.**

| Condition | Behaviour |
|---|---|
| Text < 300 characters | F6 not computed |
| Cross-topic control unavailable | F6 halved and marked *topic-confound unverified* |
| Translated or transliterated text detected | F6 zeroed, marked *translation-laundered* |
| LLM-mediated text detected | F6 zeroed, marked **stylometrically inadmissible** |
| Any F6 use | rendered with the caveat text in the Balance Sheet row |

**Laundering-aware gating (innovation 3).** We do not run a general "AI text detector" and claim reliability — the evidence for those is poor. We use the specific, defensible finding from the authorship-gap literature: LLM-generated text sits in a distinguishable *LLM style region* and its similarity to any claimed human author falls below the human cross-author floor. So the gate is a **style-space plausibility test**, not a detector verdict: if a document's style embedding is closer to the LLM-region centroid than to any human authorial cluster, F6 is declared inadmissible for that document. Two actors both using the same model would otherwise be scored as similar — this gate is precisely what prevents that false merge, and it is the direct answer to the "how do you handle AI-generated text?" question.

**Style discontinuity as handover evidence (innovation 4, inverse use).** Within a single account's timeline, a sustained shift in style embedding, template hash, contact identifiers and catalogue composition, detected by changepoint analysis over the account's posting sequence, is evidence of **account handover** — resale, compromise, or staff rotation. Effect: the account timeline is split into segments and entity resolution runs on segments. This turns stylometry's weakness (sensitivity) into a strength, and it is the mechanism by which we answer "how do you deal with compromised accounts?" with code rather than a caveat.

**Robust substitutes carrying the load instead (F5):** template structure hash, price-rounding and unit conventions, section ordering, signature-block form, product-image pHash, EXIF clustering, verbatim non-boilerplate reuse. Operators copy-paste; paraphrasing prose does not change a copy-pasted table.

### 17. Behavioural intelligence — event-driven only

Dropped: continuous timezone/sleep inference as a linkage signal (kept only as a displayed *context* attribute, never scored).

Kept and built:
- **Migration-window detector.** On a platform terminal event (exit scam, seizure banner, prolonged downtime), open a window and detect account creations, catalogue re-publication, and PGP/contact re-declaration on surviving platforms. Co-timing + catalogue continuity inside a shock window is the highest-yield behavioural evidence available. Cap 0.7 and rarity-weighted by how many vendors migrated in the same window (a mass migration is a weak signal; a two-account co-migration is stronger).
- **Catalogue continuity.** Product set overlap, price-vector correlation, ship-from/ship-to profile, and stock-phrase reuse.
- **Trust-graph re-establishment.** Which vouchers re-vouch for a new account; a re-vouching pattern from the same three moderators is meaningful and hard to fake without those accounts.
- **Multi-operator indicator.** Concurrent-session and intra-account style variance → `multi_operator_suspected`, which suppresses F6/F7.

### 18. Infrastructure intelligence — Capability 1, correctly scoped

**Discovery is OSINT, not cryptanalysis.** Seed channels: public onion index/search services, market and forum mirror lists, PGP-signed migration announcements, clearnet index sites, CT logs for clearnet domains that advertise onion mirrors, `Onion-Location` headers on clearnet sites, historical released corpora, public CTI reporting. We state plainly that unadvertised services cannot be found, and that this is a property of Tor v3, not a gap in our engineering.

**Indicator classes probed against known addresses** (all publicly served content, no authentication bypass, no exploitation): exposed status/info endpoints · TLS certificate and SAN content, plus CT-log pivot to clearnet · favicon and static-asset hashes · server/framework banners and header ordering · default and error-page fingerprints · analytics/ad identifiers in served HTML · source-map and build-artefact leakage · EXIF in served images · `Date`-header clock skew · `Onion-Location` / cross-mirror declarations · SSH host key where publicly presented · payment-address substitution across mirrors (clone detection) · OnionBalance instance-count and descriptor-consistency anomalies for known addresses.

**Every infrastructure match is rarity-weighted and shared-hosting-counter-checked before any origin language is used.** Output phrasing is fixed: *"candidate origin correlation, rarity r = 0.97, alternative explanations: shared hosting panel (checked, 3 other tenants observed)."* A match on a default Apache banner produces rarity ≈ 0 and contributes nothing, and the UI says so.

**Demonstration:** RANGE-TOR, our own Tor test network with deliberately misconfigured hidden services (§21). We demonstrate Capability 1 against infrastructure we own. This is lawful, reproducible, and measurable — and it is a stronger demo than a screenshot of someone else's crime scene.

### 19. Blockchain intelligence — evidence, never identity

Layers: address extraction and validation → public-chain transaction retrieval → address reuse across accounts → co-spend clustering **with method and confidence stored** → mixing/batching detection → temporal cadence → known-service labelling with label provenance graded.

Hard rules: a shared address never triggers a merge, only F2 evidence capped at 2.0. Cluster membership is stored as an opinion with `cluster_method` and `cluster_confidence`, never as a fact. CoinJoin/PayJoin/batching indicators set `coinjoin_flag`, which suppresses CIOH-derived evidence entirely for that transaction. Exchange/service deposit addresses are hub-flagged (thousands of users) and contribute zero. Monero: we model addresses and their observed use as entities, and **we do not attempt tracing** — the UI states "XMR: not traceable to evidentiary standard" rather than showing an empty graph. Label provenance for any address label is displayed with its source grade.

---

## 20. PART XX — SOURCE STRATEGY

| Tier | Sources | Purpose | Legality | Reliability | Freshness | Limitations |
|---|---|---|---|---|---|---|
| **Development** | RANGE-SIM synthetic corpus; PAN authorship corpora; public Reddit/Twitter cross-account linkage sets | build and tune ER, stylometry, blocking | fully lawful, licensed | ground truth known | static | not criminal-domain realistic |
| **Evaluation** | RANGE-SIM (hidden ground truth); released historical marketplace archives (2013–2015 research releases); academic underground-forum corpora obtained under institutional agreement where time permits | measure with ground truth | lawful; agreement-gated corpora used only if access lands in time | ground truth partial | historical | pre-LLM era; access lead time is a project risk |
| **Demonstration** | RANGE-SIM + RANGE-TOR (ours) | deterministic on-stage demo | fully lawful, we own it | ground truth known | static | synthetic by design, disclosed openly |
| **Live public (read-only, safe strata)** | public onion index pages; public CTI feeds; abuse/blocklists; public blockchain nodes/explorers; Certificate Transparency logs; Tor Project CollecTor/Onionoo; Internet Archive | show the collector runs against reality | public data, no authentication, no ToS breach on registration-walled sites | graded per source | live | thin; no market interiors |
| **Excluded, deliberately** | authenticated market interiors; invite-only forums; purchased datasets of unclear provenance; anything requiring credentials, payment, CAPTCHA evasion, or exploitation | — | unlawful or unethical for us | — | — | stated on the legal slide as a scoping decision |

Every `source` row carries `legal_basis`, `reliability_grade`, `credibility_default`, `independence_cluster`, and `is_le_operated_suspected`. Source grades are visible on every evidence row that derives from them.

---

## 21. PART XXI — PRAMANA RANGE (synthetic investigation environment)

Two halves, both ours, both reproducible from a seed.

### 21.1 RANGE-SIM — synthetic multi-platform corpus with hidden ground truth

Generated by a seeded, deterministic generator (not free-form LLM output, so structural properties are controlled): 4 marketplaces + 3 forums, ~2,000 accounts, ~40,000 posts/listings, ~18 months of simulated time.

Ground truth planted, and hidden from the analyst UI:
- **12 true multi-account operators** with varied evidence profiles: one linkable only via PGP metadata; one only via image reuse; one only via template + migration co-timing; one via four weak families (the case that *requires* fusion); one that is linkable only if independence grouping is correct because 30 of its 34 evidence items are mirrors.
- **6 decoy pairs** that look strongly linked through a single family and are not: shared market-default PGP key (hub), shared bulletproof host (hub), stock product photo (hub), copied listing template, planted wallet address (framing attack), imitated writing style.
- **3 account-handover cases**: a resale, a compromise, and a staff-rotation account — each with a style/template/contact changepoint.
- **2 LLM-laundered actors** whose prose is model-rewritten but whose templates and images persist.
- **1 platform later revealed as LE-operated**, used to demo retraction propagation live.
- **1 clone marketplace** with substituted payment addresses.
- Mirrors, quoted reposts, duplicate scrapes, multilingual and transliterated content, and realistic timestamp jitter throughout.

### 21.2 RANGE-TOR — controlled Tor testbed

A local Tor test network (Chutney-style, or isolated real-Tor instances on our own hosts) running 8 hidden services we own, seeded with the misconfiguration classes of §18: one with an exposed status endpoint, one presenting a TLS certificate whose SAN names a clearnet host we also control, two sharing a favicon and asset bundle, one leaking an internal address in a header, one with a distinctive clock skew, one clone of another with a substituted payment address, one clean control. Ground truth: we know which onion maps to which clearnet host. The scanner must recover it, and must **not** produce a link for the clean control or for two services that merely share a default banner.

Disclosure discipline: every demo screen showing RANGE data is watermarked `SYNTHETIC / CONTROLLED TESTBED`. We never imply live criminal data.

---

## 22. PART XXII — EVALUATION LAB (DW-ATTRIB-1)

The benchmark is a deliverable, not an appendix. It is what makes our numbers checkable and competitors' unfalsifiable.

### 22.1 Protocol

Temporal split (train/tune on months 1–12, test on 13–18) — random splits are banned in the harness. Open-set: test contains operators unseen in training. Negative pairs sampled at realistic imbalance (all non-matching pairs within blocking, not a balanced sample). Fixed seeds, pinned corpus snapshot id, released eval harness. Bootstrap 95% CIs on every reported number. Sanity controls: label-shuffled run (must collapse to chance) and a same-family-only run.

### 22.2 Metrics

| Area | Metrics |
|---|---|
| Entity resolution | pairwise precision/recall/F1 **and** cluster-level B-cubed + Variation of Information; **false-merge rate**; giant-component check (largest cluster size vs truth) |
| Attribution / LR quality | **Cllr** (log-LR cost) and Cllr_min, **Tippett plots**, reliability diagram, ECE, Brier; **precision at FPR ≤ 0.1%** |
| Independence accounting | measured inflation avoided: LR with vs without grouping, on the mirror-heavy planted case |
| Stylometry | AUC and c@1 on verification; degradation curve under paraphrase, translation, and imitation; false-merge rate between two LLM-laundered actors with and without the gate |
| Infrastructure | recall of planted onion↔clearnet mappings on RANGE-TOR; false-link rate on the clean control and default-banner pair |
| Blockchain | clustering precision under injected CoinJoin patterns |
| Search | Recall@k, MRR, nDCG@10 for lexical, dense, and hybrid |
| Graph | strongest-path explanation correctness against planted paths; link prediction only if used |
| Adversarial | degradation under each red-team attack in §24, reported as a table (this is a headline result, not a footnote) |
| Analyst | time-to-first-correct-lead; decision accuracy on known-answer cases; **over-reliance rate** (how often an analyst accepts a deliberately wrong high-score assessment) with and without the unmasking gate |
| System | ingest throughput (docs/min), end-to-end ingest→scored latency, search p95, graph expansion p95, full recompute time |

### 22.3 The "not guessing" argument, in one place

Four artefacts, all producible by us: **Cllr < 1** on a held-out temporal split (a system that guesses has Cllr ≥ 1 by construction). **Tippett plot** showing same-operator and different-operator LR distributions separating. **Reliability diagram** near the diagonal. **Ablation table** proving each modality contributes and that removing independence grouping *inflates* confidence without improving accuracy. The last one is the killer: it proves our central claim is a measured effect, not a design opinion.

### 22.4 Ablation (PART XXIII)

Run in the product, live, from a toolbar toggle:

| Configuration | Expected direction | What it proves |
|---|---|---|
| Identifiers only (F1+F4) | high precision, low recall | baseline is strong but blind |
| + F5 content artefacts | recall ↑, precision ~flat | image/template reuse is real signal |
| + F3 infrastructure | recall ↑ | infra adds cases |
| + F7 behavioural (migration) | recall ↑ on migration cases only | event-driven behaviour is narrow but sharp |
| + F6 stylometry | recall ↑ slightly, precision ↓ if ungated | why F6 is capped |
| + F6 **gated** | precision recovers | the gate earns its place |
| + F2 blockchain | recall ↑ on a subset | wallets help, weakly |
| **Full fusion, independence grouping OFF** | **LR inflates, accuracy flat, calibration breaks** | **the central thesis, measured** |
| **Full fusion, grouping ON** | best calibration, Cllr minimum | the shipped configuration |

---

## 24. PART XXIV — ADVERSARIAL RED TEAM

Assume the adversary has read this document. Each attack is scripted against RANGE and its degradation is reported.

| # | Attack | Mechanism | Defence | Residual risk |
|---|---|---|---|---|
| 1 | **Impersonation** | New account copies a known vendor's handle, avatar, template | rarity + first-seen ordering (who used it first) + PGP challenge absence + counter-evidence detector | high-effort clones with stolen key material remain hard |
| 2 | **Identity fragmentation** | One operator splits across many low-activity accounts with no shared indicators | accepted limitation: we detect only what leaves traces; stated openly | real and unsolved |
| 3 | **Identity collision** | Deliberately adopt a rival's indicators to force a merge | single-family rule (`k<2 ⇒ weak`) + framing detector + first-seen ordering | moderate |
| 4 | **Style laundering** | LLM rewrite of all prose | F6 gate declares inadmissible; F5 template/image signals unaffected | prose-only actors become unlinkable — disclosed |
| 5 | **Multilingual laundering** | Machine-translate all content | translation detector zeroes F6; F5/F1/F4 unaffected | disclosed |
| 6 | **Fake wallet signal** | Plant a rival's receiving address in own listing | F2 cap 2.0 + single-family rule + first-seen + framing detector | low impact by construction |
| 7 | **Fake PGP signal** | Publish a rival's public key as one's own | key *material* is public, so possession proves nothing: we score F1 only on **metadata similarity across keys** and signed-artefact provenance, not on republished public keys | moderate |
| 8 | **Decoy infrastructure** | Deliberately misconfigure a service to point at an innocent clearnet host | shared-hosting counter-check + rarity + requirement for a second family + explicit "alternative explanations" field | real; mitigated by never allowing infra alone to conclude |
| 9 | **Graph poisoning** | Sybil accounts manufacture trust edges and mentions | F8 capped at 1.0; degree/velocity anomaly detection on new accounts; vouching from low-age accounts discounted | moderate |
| 10 | **Source poisoning** | Flood a forum with fabricated dox and cross-references | source reliability grading + independence clustering + `k` requirement + corpus-flood alarm on rarity dilution | moderate |
| 11 | **Prompt injection** | Embed instructions in scraped text targeting our copilot | untrusted text never shares a context with tools; delimiting + provenance labelling + instruction-pattern stripping; copilot is read-only over retrieved evidence and cannot write | residual, and stated as residual — this is not solved in the literature |
| 12 | **Clone poisoning** | Stand up mirror clones to inflate apparent corroboration | clone detection via payment-address substitution + independence clustering | low |
| 13 | **Retroactive contamination** | A platform we trusted turns out to be LE- or adversary-operated | retraction propagation (§9.3) | handled, and demoed |
| 14 | **Analyst feedback poisoning** | An insider or biased analyst confirms wrong merges to shift the model | analyst-confirmation labels are quarantined from the calibration set; calibration is fitted only on RANGE/benchmark ground truth; per-analyst agreement telemetry | handled architecturally |
| 15 | **Crawler attack** | Hostile HTML/JS attempts collector compromise or deanon | ephemeral network-isolated container, JS disabled by default, no clearnet egress from collector, per-target circuit isolation | moderate |

---

## 25. PART XXV — SECURITY ARCHITECTURE

The platform aggregates criminal intelligence and is therefore a target. Treat every external byte as hostile.

### 25.1 Trust zones

Four zones, no shortcuts between them: **Z1 Collector** (ephemeral, network-isolated, Tor-only egress, no DB write access — writes to a drop directory only) → **Z2 Ingest/Validation** (reads drop directory, no outbound network at all, seals and validates) → **Z3 Analytical** (Postgres + services, no outbound network) → **Z4 Presentation** (API + UI, authenticated, no direct DB access outside the API).

The collector cannot reach the database. The database cannot reach the internet. Both properties are testable and are tested in Phase 10.

### 25.2 Controls

Authentication with per-analyst identity and MFA-capable IdP hook; **ABAC** on case, source-sensitivity and entity-category attributes (RBAC alone cannot express "this analyst may see this case but not that source"); least privilege per service account; secrets in environment/secret store, never in repo, with a pre-commit secret scan; TLS internally; encryption at rest for the artefact store; **tamper-evident audit log** — append-only, hash-chained, covering every read of an artefact and every review decision; SBOM generated per build with pinned, hash-verified dependencies; container images pinned by digest; **no unauthenticated network-exposed endpoint exists** — the API requires auth on every route including health, and this is asserted by a test.

### 25.3 Hostile content handling

Rendering and parsing of scraped content happens only in Z1/Z2 with JS disabled by default; when JS execution is required, a disposable container with no persistent volume and no clearnet route. Parsers are fuzzed against malformed input in Phase 10. LLM contexts receive untrusted text wrapped in explicit provenance delimiters with instruction-like structures stripped, and **no tool or write capability is present in any context containing untrusted text**. Illegal-content screen at queue head: hash-based drop-on-match with no persistence of the payload, only an incident record; classifier pre-filter as a second layer; documented escalation procedure. For the hackathon this is exercised against synthetic sentinel hashes on RANGE — we demonstrate the control without touching real material.

### 25.4 Privacy and governance

Data minimisation is a design requirement: we store indicators and the artefacts they came from, and we do not build profiles of non-target persons. Under DPDP 2023 we rely on the ground that personal data made publicly available by the data principal falls outside the Act, and we do **not** claim a State-instrumentality exemption we are not entitled to. Retention: raw artefacts 180 days in the prototype with a documented policy, then hash-and-metadata-only. Purpose limitation recorded on every `source`. Deletion and retraction are distinct operations and both are logged. A written ethics note covering incidental personal data, non-target minimisation, and refusal boundaries ships with the repo.

### 25.5 Evidentiary integrity

SHA-256 at the moment of payload capture, before any transformation; per-run hash chain (`chain_prev`, `chain_hash`); optional RFC 3161 timestamp token; WARC as the archival container; verification endpoint that re-walks the chain and reports any break; reports carry an artefact hash manifest and an integrity annexure structured to align with BSA 2023 s.63 certification practice. We present this as **integrity engineering aligned to statutory practice**, and we do not assert that our output is automatically admissible — admissibility is a court's determination with a certifying human, not a feature.

---

## 26. PART XXVI — INVESTIGATOR UX

One workspace. The investigator moves **GRAPH ↔ TIME ↔ EVIDENCE ↔ HYPOTHESIS** through four synchronised panes that share a single selection and a single `as_of` timestamp. Changing the time slider changes all four. That shared state is the whole UX thesis; everything else is layout.

### 26.1 Screens (each justified; anything unjustified was cut)

| Screen | Purpose | Cut if it were only… |
|---|---|---|
| Investigation Workspace (default) | the four synchronised panes; where all real work happens | — |
| Search | hybrid lexical+semantic across documents, indicators, entities; exact-match mode for hashes/addresses | — |
| Entity Profile (Account / Persona / Actor / Key / Wallet / Service) | dossier view: identifiers, timeline, evidence in/out, assessments, review state | — |
| **Evidence Balance Sheet** | the killer interaction (§4) | — |
| Graph Explorer | degree-limited expansion, layer filters, hub highlighting, strongest-path | would be cut if it were a decorative force-directed hairball |
| Timeline | account/persona activity, lifecycle shocks, migration windows, belief-time scrubber | — |
| Persona Comparison | side-by-side account comparison: templates, images, prices, contacts, style, sessions | — |
| Infrastructure Intelligence | onion↔clearnet correlation candidates with rarity and alternative explanations | — |
| Blockchain Intelligence | address/cluster view with method, confidence, mixing flags, label provenance | — |
| Assessment & Review | sequential-unmasking review gate, decision + rationale | — |
| Case Management | cases, questions, scope, assignments, state | — |
| Reports | draft, edit, sign, export with manifest | — |
| Source & Data Health | per-source reliability, freshness, last scan date, ingest errors, hash-chain verification status, corpus snapshot id | — |
| Alerts | new high-band assessments, retraction impacts, hub/flood anomalies, review backlog | — |
| **Evaluation** (in-product) | live Cllr, Tippett, reliability diagram, ablation toggle | this is unusual and deliberate — it makes rigour a feature |

Cut outright: a global "dashboard" of vanity counters, a world map of onion services, a live-threat-feed ticker, anything glowing.

### 26.2 Signature interactions, ranked

1. **Why are these linked?** → Evidence Balance Sheet with the visible independence discount. *The product in one screen.*
2. **Challenge this hypothesis** → runs all counter-evidence detectors, shows what fired, what did not, and what would change the conclusion.
3. **What changed?** → belief-time scrubber + retraction impact ("this retraction dropped 1 assessment from strong to weak").
4. **Show provenance** → any row → evidence → document → sealed artefact → hash-chain verification result.
5. **Show strongest path** → weighted shortest path with per-hop evidence and per-hop rarity, and a warning if the path traverses a hub.
6. **Generate intelligence report** → draft with every claim footnoted to an artefact hash, requiring analyst signature.

### 26.3 Presentation of uncertainty

Verbal band is the largest element; numeric LR is secondary; the evidence-family count `k` is always adjacent to the band. Multi-modal edge uncertainty is drawn as a **stacked bar of family contributions**, not as edge thickness, because thickness conflates strength with count — this is the one HCI decision the research says nobody has empirically settled, so we choose the representation that decomposes rather than aggregates, and we say that it is a choice.

### 26.4 Bias controls in the interface

Sequential unmasking is enforced by the review flow: the analyst sees raw evidence, then the strongest counter-evidence, then the score, and cannot skip forward. Decision requires a free-text rationale. Counter-evidence panels cannot be collapsed by default. Machine text and analyst text are permanently visually distinct. A "no exclusion checks have run" state is shown loudly rather than as an empty panel.

---

## 27. PART XXVII — AI COPILOT (constrained)

Scope: read-only question answering over **retrieved evidence for the current case**, plus report drafting. Nothing else.

Answers it may give, each grounded in cited `evidence_id`s: why two identities are connected; the strongest supporting and contradicting items; what changed in a period; which sources corroborate a claim and how they are graded; what an analyst should verify next (drawn from a fixed checklist of unrun detectors and missing families, not invented); a case summary.

Guarantees: cannot invent evidence, because it can only cite retrieved rows and an uncited sentence is not rendered; expresses uncertainty using the same verbal bands as the engine; labels inference distinctly from evidence in every answer; runs with no tools in any context holding untrusted text; has no write path to any core table; every interaction is logged with the retrieved evidence set so an answer is reproducible. It is a retrieval-grounded explainer, and we describe it that way instead of calling it an agent.

---

## 28. PART XXVIII — REPORTING

Sections, fixed: Investigation identity and question · Scope and reference population · Executive summary (verbal, no numbers first) · Key findings, each footnoted to artefact hashes · Evidence register (family, rarity, group, discounted weight, source grade) · Relationship summary · Timeline · Attribution assessment (hypothesis, defence hypothesis, LR, band, `k`, calibration reference) · Counter-evidence and alternative explanations · Provenance and integrity annexure (artefact hash manifest, chain verification result, collection method and versions) · Uncertainty and limitations · Analyst notes and dissent · Methodology and model/params versions · Signature block.

Exports: CSV (flat entity/indicator/assessment tables), JSON (full nested case bundle with provenance), STIX 2.1-aligned bundle (Identity/Threat-Actor/Relationship/Sighting/Opinion with confidence, plus a custom extension for evidence families and independence keys — the mapping's lossiness is documented), and sealed PDF. Every export carries the corpus snapshot id and params version, so a number in a report can be reproduced months later.

---

## 29. PART XXIX — PRODUCT ARCHITECTURE

### 29.1 Prototype stack (what we build for SIH)

| Layer | Choice | Why | Alternative | Rejection reason | Proto fit | Prod fit |
|---|---|---|---|---|---|---|
| Frontend | React + TypeScript + Vite, Tailwind, TanStack Query, Cytoscape.js (graph), visx/Recharts (charts) | Cytoscape.js gives degree-limited expansion and custom edge styling we need; team familiarity | Sigma.js, D3 from scratch, Linkurious | D3-from-scratch costs days we do not have; Linkurious is commercial | high | high |
| Backend | Python 3.12 + FastAPI + Pydantic | same language as the ML/extraction layer, so no service boundary and no duplicated models | Node, Go | second language for no gain; ML ecosystem is Python | high | medium (split later) |
| Primary store | **PostgreSQL 16** (JSONB, `tstzrange` + GiST, recursive CTEs, `pg_trgm`, `pgvector`, native FTS) | one database serves relational, temporal, graph-traversal, vector, and lexical search at our scale; one transaction covers evidence + edge, which is what makes FK integrity rules enforceable | Neo4j + Elasticsearch + Qdrant | three systems to deploy, three consistency stories, no prototype benefit; cross-store FK integrity is impossible | high | medium (migration path §29.4) |
| Graph | logical projection over Postgres, recursive CTEs, depth+degree limits, materialised views per layer | ≤10⁵ nodes traverses in ms; avoids a second store | Neo4j, Memgraph, AGE | operational cost now; AGE adds an extension risk for a capability CTEs already cover | high | low→migrate |
| Search | Postgres FTS (BM25-like ranking) + pgvector, fused by RRF, optional cross-encoder rerank | hybrid without a second cluster; exact-identifier search needs lexical anyway | OpenSearch | a JVM cluster for a corpus of tens of thousands of documents is unjustifiable | high | medium |
| Vector | pgvector (HNSW) | same store, same transaction | Qdrant, FAISS | separate service, sync problem | high | medium |
| ML / NLP | scikit-learn, sentence-transformers (multilingual), Splink, imagehash, python-gnupg/pgpy, simhash, changepoint via ruptures | all CPU-viable; no GPU dependency on stage | PyTorch fine-tuning, GNN libs | training cost and cold-start; not defensible at our data volume | high | high |
| LLM | pluggable provider behind one adapter, off by default, deterministic-seeded; small local model fallback | demo must not depend on network; adapter keeps it excisable | hard dependency on a hosted API | single point of demo failure and a data-egress question we should not have to answer | high | high |
| Queue | Postgres-backed job table with `SELECT … FOR UPDATE SKIP LOCKED` | zero extra infrastructure; visible, debuggable, restartable | Kafka, Redis, Celery+broker | Kafka for one producer and four consumers is theatre | high | low→migrate |
| Object storage | local filesystem with content-addressed layout (`<hash[0:2]>/<hash>`), S3-compatible adapter interface | works offline; interface makes production swap trivial | MinIO/S3 now | another container for no prototype gain | high | medium |
| Deployment | Docker Compose, four services (collector, worker, api, ui) + Postgres; single `make demo` seeds RANGE and runs everything offline | judged on a laptop with no internet | Kubernetes | absurd at this scale | high | low→migrate |
| Observability | structured JSON logs, Prometheus-format `/metrics`, in-product Data Health screen | enough to debug and to demo pipeline health | full ELK/Grafana stack | operational weight without payoff in 36 hours | high | medium |

### 29.2 Prototype vs production, kept strictly separate

**Prototype principles:** one database, one language, four containers, no network dependency, deterministic seeds, `make demo` reproducible from clean clone, every number regenerable.

**Production additions (documented, not built):** distributed collection with per-source workers and rate governance; Kafka or equivalent for ingest fan-out; object storage on S3-compatible infrastructure with lifecycle policies; dedicated graph engine when traversal p95 breaches budget; OpenSearch when corpus exceeds Postgres FTS comfort; separate calibration/model registry; enterprise IdP with SAML/OIDC and full ABAC policy engine; HSM-backed signing for report seals and RFC 3161 TSA integration; multi-tenant compartmentation; DR and immutable-backup posture; formal model governance and drift monitoring.

### 29.3 Migration triggers (stated numerically so the decision is not aesthetic)

Graph engine when >5×10⁶ edges **or** 3-hop expansion p95 >800 ms. Dedicated search when >5×10⁶ documents **or** search p95 >400 ms. Message bus when sustained ingest >200 docs/s **or** more than 3 independent consumer groups. Object store when artefact volume >2 TB. None of these are near the prototype.

---

## 30. PART XXX — MINIMUM REMARKABLE MVP

**Definition:** one closed-loop investigation, end to end, on lawful data, producing a signed report whose every claim traces to a sealed artefact — and whose conclusion is *correctly refused* when the evidence does not support it.

The loop: seed a case → collect from RANGE-SIM + RANGE-TOR → seal artefacts with hash chain → extract indicators (PGP fingerprints, addresses, contacts, templates, images, sessions, style vectors) → canonicalise artefacts and assign independence keys → resolve accounts to personas via Splink with must-not-link vetoes → generate link hypotheses → fuse with rarity-weighted, independence-discounted, capped log-LR → run counter-evidence detectors → present the Evidence Balance Sheet → analyst reviews under sequential unmasking → export signed report + STIX bundle → verify against hidden ground truth in the Evaluation screen.

### 30.1 MVP filter — every candidate feature tested against "does it make the demo undeniable?"

| Feature | In MVP? | Reason |
|---|---|---|
| Evidence Balance Sheet with independence discount | **yes** | it *is* the differentiator |
| Rarity/IDF weighting + hub suppression | **yes** | without it the graph collapses and the demo fails |
| Counter-evidence detectors + must-not-link veto | **yes** | the refusal moment is the credibility moment |
| Bitemporal store + belief-time scrubber + retraction propagation | **yes** | "what changed?" is unmatched by any comparable tool |
| Splink ER with constrained clustering | **yes** | core of Capability 2 |
| Stylometry as gated corroborator + style-discontinuity detector | **yes** | Capability 3, honestly scoped |
| Targeted infrastructure correlation with alternative-explanation check | **yes** | Capability 1, honestly scoped |
| Graph explorer with degree caps and strongest path | **yes** | required to read the result |
| Calibration + Cllr/Tippett/reliability in-product | **yes** | converts rigour from a claim into a screen |
| Signed report + CSV/JSON/STIX export | **yes** | explicit requirement of the problem statement |
| Blockchain heuristics with method labelling | **yes, limited** | CIOH + labels with provenance grading; no clustering claims beyond that |
| LLM copilot | **yes, off by default** | grounded explainer only; demo works without it |
| Automated broad crawling of live marketplaces | **no** | unlawful/unsafe content handling; RANGE substitutes |
| GNN link prediction | **no** | cold-start on sparse graph; V2 research item |
| Dempster-Shafer / Subjective Logic engine | **no** | rejected on assumptions, sources, and feasibility (§1.6, §12) |
| Real-time streaming ingest | **no** | no demo value |
| Monero tracing | **no** | not achievable to evidentiary standard; we say so on a slide |
| Face recognition / biometric identification | **no** | out of ethical and legal scope |
| Multi-tenancy, SSO, RBAC admin UI | **no** | production concern |

---

## 31. PART XXXI — ROADMAP BEYOND MVP

**V2 (3–6 months):** Bayesian network fusion with explicit shared latent parents (the principled successor to capped additive log-LR, once we have enough labelled pairs to fit it); learned blocking; cross-lingual authorship verification with proper topic control; per-family calibration on a larger reference population; conformal prediction with drift detection guarding exchangeability; analyst-feedback loop with poisoning defences; OpenCTI/MISP bidirectional connectors; case collaboration and dissent workflow.

**V3 (6–18 months):** authorised-partner federation where evidence is exchanged without exposing raw artefacts; graph-native store with temporal indexing; GNN experiments benchmarked *against* the transparent baseline and adopted only if they beat it on Cllr while remaining explainable; automated OPSEC-failure discovery over lawful archives; forensic-grade report tooling aligned to BSA s.63 certification workflow with HSM signing.

**Production hardening:** deployment inside an authorised agency boundary, formal LR method validation per ENFSI, external audit, model governance, DR, tenant compartmentation, throughput SLOs.

**Research frontier (honest open problems, not roadmap promises):** reference populations for the dark-web domain do not exist, so calibration is anchored to synthetic ground truth and that is a real limitation; independence structure among OSINT sources is unmeasured in the literature; adversarial stylometry under LLM assistance is unresolved; there is no accepted HCI standard for presenting multi-modal evidential uncertainty; and no published base rate exists for "two accounts belong to the same operator" in any marketplace corpus, which is the single largest unknown in the entire field.

---

## 32. PART XXXII — ENGINEERING GAMEPLAN (dependency-ordered)

Owners are role codes defined in §33: **PL** platform/backend, **DE** data/collection, **ML** ML/analytics, **FE** frontend, **EV** evaluation/forensics, **PM** product/presentation.

### Phase 0 — Foundation
**Objective:** repo, Compose stack, migrations, CI, `make demo` skeleton that runs offline from a clean clone.
**Rationale:** every later phase's acceptance criterion is "reproducible"; that is only true if it is true from day zero.
**Dependencies:** none. **Owner:** PL (secondary FE).
**Tasks:** monorepo layout; Postgres 16 with pgvector/pg_trgm; Alembic migrations; FastAPI skeleton with health and `/metrics`; Vite app shell; pre-commit (ruff, mypy, prettier); GitHub Actions running lint + tests; digest-pinned images; SBOM generation; `make demo` stub.
**Test strategy:** CI green on empty test suite; clean-clone bootstrap timed.
**Deliverable:** running stack. **Acceptance:** `git clone && make demo` reaches a served page with no internet, in <10 min.
**Demo milestone:** none. **Risk:** yak-shaving. **Fallback:** drop mypy strictness, keep ruff.

### Phase 1 — Canonical data model + bitemporal core
**Objective:** the schema of §7–§9, with `tstzrange` validity, belief-time columns, `as_of()` views, hash-chained audit log, and job table.
**Rationale:** everything downstream writes into this; retrofitting bitemporality later is a rewrite.
**Dependencies:** 0. **Owner:** PL (secondary EV).
**Tasks:** entity/account/persona/actor tables; indicator tables; document + artefact tables with content-addressed paths; evidence table with `independence_key`, family, rarity, decay; assessment tables; `superseded_by` retraction chain; GiST indexes; `as_of(ts)` views; audit chain trigger; job queue with `SKIP LOCKED`.
**Test strategy:** property tests that `as_of` reconstruction of a mutated entity equals the historical snapshot; retraction propagation test asserting dependent assessments are flagged; audit-chain tamper test that mutating a row breaks verification.
**Deliverable:** migrations + repository layer. **Acceptance:** all three tests pass; chain verification endpoint returns OK on seeded data and FAIL after a deliberate row edit.
**Demo milestone:** M1. **Risk:** over-modelling. **Fallback:** collapse assessment revision history to append-only rows without ranges.

### Phase 2 — RANGE-SIM synthetic corpus + hidden ground truth
**Objective:** the generator of §21: multi-marketplace corpus with controlled operator identities, migrations, rebrands, impersonators, shared hosting, style-obfuscated pairs, and colliding-but-distinct actors.
**Rationale:** without ground truth, no calibration, no Cllr, no ablation, no defensible demo — and no lawful data path.
**Dependencies:** 1. **Owner:** DE (secondary EV).
**Tasks:** operator/persona generator with parameterised OPSEC-failure rates; text generation with controlled topic/style separation and a *documented* generation method; PGP keypairs actually generated so fingerprints are real; wallet addresses that are valid-format but never funded; template/image reuse with pHash-detectable variants; injected traps — two operators with identical writing style but must-not-link temporal overlap, one operator whose only link is a hub address; seed-locked determinism; ground-truth file withheld from the pipeline by construction (separate schema, no FK).
**Test strategy:** generator invariants (every planned link is realisable from generated artefacts); leakage test asserting no pipeline module can read the ground-truth schema; regeneration with same seed is byte-identical.
**Deliverable:** `range-sim` CLI + seeded corpus. **Acceptance:** 3 marketplaces, ≥60 accounts, ≥25 operators, ≥400 documents, all traps present, leakage test passes.
**Demo milestone:** M2. **Risk:** generator so tidy the pipeline looks better than reality — mitigated by mandatory noise/obfuscation parameters and by reporting results *with the noise level stated*. **Fallback:** reduce to 2 marketplaces.

### Phase 3 — Collection + sealing
**Objective:** collector service in Z1 with Tor-only egress, WARC/WACZ capture, hash-at-capture, RFC 3161-capable timestamp hook, robots/rate governance, and RANGE-TOR self-hosted misconfigured services.
**Rationale:** provenance is the evidentiary backbone; capture-time sealing cannot be added afterwards.
**Dependencies:** 1, 2. **Owner:** DE (secondary PL).
**Tasks:** Tor client container; fetcher with per-source rate limits and jitter; WARC writer; SHA-256 manifest; chain linkage into the audit log; illegal-content hash screen with drop-on-match and no payload persistence; RANGE-TOR: three self-owned onion services deliberately misconfigured (exposed server-status, clearnet-shared TLS certificate, default banner, descriptor inconsistency), documented as ours; network policy tests.
**Test strategy:** zone test asserting collector cannot open a socket to Postgres and Postgres cannot resolve external DNS; replay a sealed WARC and confirm hash equality; screen test with a benign hash on the blocklist.
**Deliverable:** collector + RANGE-TOR. **Acceptance:** all captures sealed and chain-verifiable; both zone assertions pass in CI.
**Demo milestone:** M3. **Risk:** Tor flakiness on demo network. **Fallback:** pre-sealed WARC replay mode (`--offline`), which is in fact the default demo path.

### Phase 4 — Extraction + canonicalisation + independence keys
**Objective:** turn sealed documents into indicators, and assign every derived evidence item an independence key so double counting is impossible downstream.
**Rationale:** this is where the dossier's central problem is actually solved — in the data layer, not the fusion algebra.
**Dependencies:** 3. **Owner:** ML (secondary PL).
**Tasks:** PGP block parsing to real fingerprints; crypto-address extraction with checksum validation; contact identifiers; price/template/boilerplate extraction; image hashing (pHash); SimHash over shingles; canonical-artefact resolution (SHA-256 exact, SimHash ≤3, containment ≥0.8, pHash ≤6); clone detection via payment-address substitution; source-independence clustering at document overlap >0.6; IDF computation over the indicator corpus with `is_hub` at τ=12; inheritance of parent independence keys by derived features.
**Test strategy:** unit tests per extractor with adversarial inputs (malformed PGP, lookalike addresses, unicode homoglyphs); a *double-count regression test* — the same listing mirrored on 5 sites must yield exactly one independent evidence group; hub test asserting a shared escrow address gets weight 0.
**Deliverable:** extraction workers. **Acceptance:** double-count test and hub test pass; extractor precision on RANGE-SIM ≥0.95 for cryptographic and address indicators.
**Demo milestone:** M4. **Risk:** over-fitting extractors to the synthetic generator — mitigated by validating extractors on real public archives (non-marketplace) and reporting both numbers. **Fallback:** drop image pHash; keep text canonicalisation.

### Phase 5 — Entity resolution engine
**Objective:** Splink-based account→persona resolution with blocking, must-link/must-not-link constraints, and giant-component prevention.
**Dependencies:** 4. **Owner:** ML (secondary EV).
**Tasks:** blocking on multi-key + MinHash LSH; Fellegi-Sunter comparison model with m/u estimation via EM; constrained clustering honouring hard vetoes; transitive-closure guard (component size cap, hub-edge removal before closure, cut-point reporting); B-cubed and VI metrics; false-merge rate as the headline metric.
**Test strategy:** cluster-quality run against hidden ground truth; adversarial trap tests — the impersonator must not merge, the must-not-link overlap pair must not merge, the hub-only pair must not merge; component-size assertion.
**Deliverable:** ER service. **Acceptance:** false-merge rate ≤2% on RANGE-SIM; no component exceeds the cap; all three traps survive.
**Demo milestone:** M5. **Risk:** EM instability on sparse comparisons. **Fallback:** hand-specified m/u priors, disclosed as such.

### Phase 6 — Fusion, calibration, bands
**Objective:** the §12 computation: rarity-weighted, decayed, grouped, capped, damped log-LR; hub/clone zeroing; counter-evidence subtraction; `k`-family floor; global ceiling 4.0; calibrated posterior; verbal bands.
**Dependencies:** 4, 5. **Owner:** ML (secondary EV).
**Tasks:** per-family weight functions and caps; λ=0.2 damping; counter-evidence detectors (temporal impossibility, contradicted identifier, exclusionary key ownership, geolocation/language conflict, known-impersonation pattern); veto logic emitting EXCLUDED with no numeric; Platt/isotonic calibration fitted on RANGE-SIM pairs; band mapping; full computation trace persisted per assessment.
**Test strategy:** golden-case tests where the expected band is fixed by hand; monotonicity tests (adding independent supporting evidence never lowers the score; adding a mirrored duplicate never raises it); a veto test asserting no numeric is emitted; determinism test (same inputs, same params version → identical trace).
**Deliverable:** scoring service. **Acceptance:** all four test classes pass; every assessment stores a replayable trace.
**Demo milestone:** M6. **Risk:** caps chosen by judgement rather than data — acknowledged explicitly in §43 and in the report methodology section; sensitivity analysis over ±50% cap perturbation is a required output. **Fallback:** none; this phase cannot be dropped.

### Phase 7 — Search + graph query layer
**Objective:** hybrid search with RRF and exact-identifier mode; recursive-CTE graph traversal with depth and degree caps; strongest-path; neighbourhood similarity.
**Dependencies:** 1, 4. **Owner:** PL (secondary ML).
**Tasks:** FTS configuration + trigram identifiers; multilingual embeddings into pgvector HNSW; RRF fusion; optional cross-encoder rerank behind a flag; typed-edge projection views per layer; depth-limited recursive CTEs with per-hop degree caps; weighted strongest path; Jaccard/Adamic-Adar neighbourhood scores; `as_of` propagated through every query.
**Test strategy:** latency budget tests on the RANGE corpus; correctness test that `as_of` traversal excludes edges believed later; hub-traversal warning test.
**Deliverable:** query API. **Acceptance:** 3-hop expansion p95 <300 ms; search p95 <250 ms; `as_of` correctness test passes.
**Demo milestone:** M6. **Risk:** CTE blow-up on hubs. **Fallback:** materialised 2-hop neighbourhood views.

### Phase 8 — Stylometry + behavioural analytics
**Objective:** authorship *verification* as a gated corroborator (F6, cap 1.0) plus style-discontinuity detection for account handover.
**Dependencies:** 4. **Owner:** ML (secondary EV).
**Tasks:** char n-gram + function-word baseline; sentence-transformer style embeddings; topic control via topic-stratified negatives and a topic-confound diagnostic that must be reported alongside every AUC; verification scored with AUC and c@1; **style-space plausibility gate** — if a text's embedding lies in a region typical of LLM-assisted rewriting, F6 contribution is suppressed and flagged; changepoint detection (ruptures) over per-account style series to flag handover; behavioural features (session hour histogram, response latency, price-update cadence) capped at 0.7 and explicitly labelled weak.
**Test strategy:** verification metrics on RANGE-SIM held-out pairs; the *obfuscation trap* — the style-obfuscated same-operator pair must not produce a strong claim, and the identical-style different-operator pair must be excluded by the must-not-link veto; ablation showing performance with and without topic control.
**Deliverable:** stylometry service. **Acceptance:** c@1 reported honestly whatever it is; both traps behave; F6 never exceeds cap; topic-confound diagnostic present in output.
**Demo milestone:** M7. **Risk:** weak results. **Fallback:** none needed — a weak, honestly-capped corroborator is the *designed* outcome, and reporting it as weak is the point.

### Phase 9 — Infrastructure correlation (Capability 1, rescoped)
**Objective:** targeted analysis of seeds we are authorised to touch (RANGE-TOR, public archives, self-owned services), producing onion↔clearnet correlation *candidates* with rarity and alternative explanations — never enumeration of the Tor network.
**Dependencies:** 3, 4, 6. **Owner:** DE (secondary ML).
**Tasks:** misconfiguration probes limited to authorised targets (exposed status pages, default banners, directory listings, error-page fingerprints); TLS certificate parsing with SAN cross-referencing; certificate-transparency lookups over public logs; descriptor-metadata consistency checks; favicon/asset hash matching; **shared-hosting counter-check** that queries how many unrelated services share the indicator and forces `is_hub` when the count exceeds τ; explicit rendering of the alternative explanation for every candidate ("this certificate is shared by N unrelated services on this CDN").
**Test strategy:** each RANGE-TOR misconfiguration must be detected; a deliberately-planted shared-CDN certificate must be suppressed as a hub; an assertion in CI that no probe targets a host outside the authorised allowlist.
**Deliverable:** infrastructure intelligence module. **Acceptance:** 4/4 planted misconfigurations found; the shared-CDN decoy scores 0; allowlist assertion passes.
**Demo milestone:** M7. **Risk:** being perceived as scanning the live network — mitigated by the allowlist being a hard-coded, auditable, demonstrable control. **Fallback:** RANGE-TOR only.

### Phase 10 — Blockchain intelligence (limited, labelled)
**Objective:** address/cluster views using CIOH with explicit degradation flags, plus label provenance grading.
**Dependencies:** 4. **Owner:** ML (secondary DE).
**Tasks:** address validation and normalisation; CIOH clustering over the synthetic ledger with CoinJoin/PayJoin/batching detection that *suppresses* the heuristic when patterns match; label ingestion with provenance grade (A: on-chain proof or court record; C: vendor attribution; E: forum assertion) and weight scaled by grade; wallet-reuse evidence capped at F2 = 2.0; a standing "Monero and modern mixing are not traced by this system" statement rendered in the UI, not buried in docs.
**Test strategy:** CIOH suppression test on a synthetic CoinJoin; label-grade weighting test; assertion that no cluster claim is emitted when suppression fired.
**Deliverable:** blockchain module. **Acceptance:** suppression works; grades affect weights measurably; no unlabelled cluster claim can be produced.
**Demo milestone:** M8. **Risk:** overclaiming. **Fallback:** address-level evidence only, no clustering.

### Phase 11 — Frontend workspace
**Objective:** the §26 screens, with the four synchronised panes and the Evidence Balance Sheet as the centrepiece.
**Dependencies:** 6, 7. **Owner:** FE (secondary PM).
**Tasks:** shared selection + `as_of` state store; Cytoscape graph with expand-on-demand, degree caps, semantic zoom, hub highlighting, strongest-path overlay; timeline with belief-time scrubber; Evidence Balance Sheet with stacked family contributions and the visible discount line; counter-evidence panel that cannot be collapsed; sequential-unmasking review flow; persona comparison; infrastructure and blockchain views; report editor; Data Health; Evaluation screen; accessibility pass (keyboard traversal of the graph, ARIA on all controls, contrast ≥4.5:1, no colour-only encoding of confidence).
**Test strategy:** Playwright walk of the entire demo path; axe-core accessibility check in CI; a rendering test that the discount line is present whenever any group was discounted.
**Deliverable:** the UI. **Acceptance:** full demo path automated end to end; zero critical axe violations; the four panes stay in sync under a scripted interaction.
**Demo milestone:** M8. **Risk:** graph performance. **Fallback:** cap initial render at 300 nodes with explicit "expand" affordance (which is the intended design anyway).

### Phase 12 — Evaluation lab
**Objective:** the §22 harness in-product: Cllr and Cllr_min, Tippett plots, reliability diagram, ECE/Brier, false-merge rate, and the ablation grid.
**Dependencies:** 5, 6, 8. **Owner:** EV (secondary ML).
**Tasks:** evaluation runner over hidden ground truth; metric computation; ablation configurations (no rarity weighting · no independence grouping · no counter-evidence · no caps · style-only · crypto-only); plot generation; corpus-snapshot and params-version stamping; a one-command `make evaluate` that regenerates every number in the presentation.
**Test strategy:** metrics validated against hand-computed values on a tiny fixture; ablation determinism.
**Deliverable:** evaluation report + in-product screen. **Acceptance:** the ablation demonstrates a measurable degradation when independence grouping is disabled (this is the empirical claim the whole architecture rests on); every presented figure is regenerable by one command.
**Demo milestone:** M9. **Risk:** the ablation shows *no* effect — in which case we report that honestly and reduce the claim, because the alternative is fabrication. **Fallback:** none.

### Phase 13 — Reports, export, security hardening
**Objective:** signed reports, CSV/JSON/STIX exports, and the §25 controls proven by tests.
**Dependencies:** 6, 11. **Owner:** PL (secondary EV).
**Tasks:** report generator with per-claim artefact footnotes; hash manifest annexure; chain verification endpoint; CSV/JSON exporters covering the problem statement's required fields (actor profiles, handles, PGP keys, wallets, hidden-service indicators, persona linkages, attribution confidence, category, last scan date, source); STIX 2.1 bundle with documented lossiness; ABAC policy enforcement; audit-log completeness; SBOM + digest pinning; prompt-injection isolation test.
**Test strategy:** export round-trip test; STIX schema validation; an injection test where a document containing tool-style instructions is processed and no tool call occurs; an authorisation test matrix.
**Deliverable:** export + hardening. **Acceptance:** every required field present in both CSV and JSON; STIX validates; injection test passes; no unauthenticated endpoint exists (asserted by a route-inventory test).
**Demo milestone:** M9. **Risk:** STIX mapping rabbit hole. **Fallback:** STIX for Identity/Relationship/Sighting only, with the gap documented.

### Phase 14 — Demo, rehearsal, presentation
**Objective:** the deterministic script of §35, rehearsed to time, with fallbacks proven.
**Dependencies:** all. **Owner:** PM (secondary FE).
**Tasks:** `make demo` seeding a fixed case; scripted beats; offline verification (airplane-mode run); fallback video capture of each beat; slide deck per §37–38; judge-defence rehearsal against §39; a pre-flight checklist.
**Test strategy:** three full timed dry runs, one of them with the network physically disabled and one with a deliberately induced service failure to prove the fallback path.
**Deliverable:** demo + deck. **Acceptance:** three consecutive runs within 7–10 minutes with identical on-screen numbers.
**Demo milestone:** M10. **Risk:** last-minute feature creep. **Fallback:** freeze code 24 hours before, and treat that freeze as non-negotiable.

---

## 33. PART XXXIII — TEAM STRUCTURE (6 members)

| Code | Role | Primary ownership | Secondary | Presents |
|---|---|---|---|---|
| PL | Platform / backend | Phases 0, 1, 7, 13 — schema, bitemporality, query layer, API, exports | Phase 3 | architecture slide |
| DE | Data / collection | Phases 2, 3, 9 — RANGE-SIM, collector, sealing, infrastructure correlation | Phase 10 | Capability 1 slide |
| ML | ML / analytics | Phases 4, 5, 6 — extraction, canonicalisation, ER, fusion | 8, 10 | fusion + differentiation slides |
| EV | Evaluation / forensics | Phase 12 + the evidential-reasoning discipline, calibration, audit trail, legal annexure | 1, 5, 6 | credibility slide (how we prevent false attribution) |
| FE | Frontend | Phase 11 — workspace, graph, balance sheet, accessibility | 14 | drives the live demo |
| PM | Product / presentation | Phase 14, slide deck, judge defence, scope discipline, cutting features | 11 | opens and closes |

Every phase has a named primary and a named secondary, so no phase has a single point of failure. PM holds veto power over new features after the Phase 12 freeze, which is the only way a 6-person team ships a system this wide.

---

## 34. PART XXXIV — MILESTONES

| ID | Milestone | Proves | Gate |
|---|---|---|---|
| M1 | Bitemporal core queryable | "what did we believe on date X" works | `as_of` + retraction tests green |
| M2 | RANGE-SIM generated with hidden ground truth | we have a lawful, measurable substrate | traps present, leakage test green |
| M3 | Sealed collection working | provenance chain is real | replay hash equality + zone assertions |
| M4 | Extraction + independence keys live | double counting is structurally prevented | mirrored-listing test yields one group |
| M5 | ER with vetoes, no giant component | the graph does not collapse | false-merge ≤2%, 3 traps survive |
| M6 | Fusion + bands + traces | the score is explainable and replayable | golden + monotonicity + determinism tests |
| M7 | Stylometry gated; infrastructure candidates found | Capabilities 1 and 3 honestly delivered | traps behave; 4/4 misconfigs found; decoy suppressed |
| M8 | Full workspace usable | an investigator can actually work | Playwright walk + axe clean |
| M9 | Evaluation + signed reports | rigour is a screen, not a claim | `make evaluate` reproduces every figure |
| M10 | Demo locked | it will work in the room | 3 timed runs, offline, identical numbers |

---

## 35. PART XXXV — DEMO SCRIPT (deterministic, 7–10 minutes)

Pre-flight: airplane mode ON (to prove offline determinism), `make demo` already seeded, browser at the case landing page, fallback video queued in a second window, corpus snapshot id visible in the footer.

| # | Time | Action | Screen | Data | Subsystem | Intended judge reaction | Fallback |
|---|---|---|---|---|---|---|---|
| 1 | 0:00–0:40 | State the question: "Are vendor `NORDSHADE` on Market A and vendor `V3RDANT` on Market C the same operator?" Show the case scope and the declared prior. | Case Management | seeded case | — | "this is a real investigative question, not a dashboard tour" | slide |
| 2 | 0:40–1:30 | Show ingestion health: sources, last scan dates, sealed artefact count, **hash-chain verification: PASS**. Then break a row in a scratch copy and show verification FAIL. | Source & Data Health | RANGE corpus | Phases 3, 1 | "provenance is enforced, not asserted" | pre-captured screenshots |
| 3 | 1:30–2:30 | Search a PGP fingerprint. Land on the Entity Profile. Expand the graph two hops with degree caps; hubs are greyed and labelled "shared/low-information". | Search → Profile → Graph | RANGE | Phases 4, 7 | "the graph is disciplined; they know hubs poison link analysis" | reduced fixture graph |
| 4 | 2:30–4:15 | **Hero moment.** Click "Why are these linked?" → Evidence Balance Sheet. Walk the families, then the discount line: five sources looked like five, the canonicaliser found one mirrored listing, so the contribution counted once. Toggle "ignore independence" and show the score inflate from moderate to strong. | Evidence Balance Sheet | assessment trace | Phases 4, 6 | "nobody else showed us this. This is the actual hard problem." | video of the toggle |
| 5 | 4:15–5:15 | Click "Challenge this hypothesis". Detectors run; a temporal-impossibility check fires on a *different* candidate pair, and the system emits **EXCLUDED with no numeric score**. | Assessment | trap pair | Phase 6 | "it refuses. That is the credibility signal." | video |
| 6 | 5:15–6:00 | Capability 1: infrastructure candidate — self-owned onion with a TLS certificate shared with a clearnet host, shown next to the counter-check "this CDN certificate is shared by 41 unrelated services", weight forced to zero on the decoy and retained on the genuine, rare indicator. | Infrastructure Intelligence | RANGE-TOR | Phase 9 | "they scoped this lawfully and still made it discriminating" | screenshots |
| 7 | 6:00–6:45 | "What changed?" Drag the belief-time scrubber back two weeks: the link was strong; a retraction of one source dropped it to weak, and the impact log names every affected assessment. | Timeline + Assessment | bitemporal | Phase 1 | "this is audit-grade. No other team has belief time." | video |
| 8 | 6:45–7:45 | Evaluation screen: Cllr, Tippett, reliability diagram against hidden ground truth; then the ablation bar — disabling independence grouping degrades Cllr and raises false merges. | Evaluation | `make evaluate` output | Phase 12 | "they measured their own system instead of claiming accuracy" | static figures |
| 9 | 7:45–8:45 | Generate the report. Show a claim, click its footnote, land on the sealed artefact and its hash. Export CSV + JSON + STIX. Show the "what we do not claim" section already printed inside the report. | Reports | case bundle | Phase 13 | "deployable output, not a demo artefact" | pre-generated PDF |
| 10 | 8:45–9:30 | Close: the claim ladder — we produce *investigative leads with calibrated confidence*, and the top tier, verified identity, is reachable only by lawful process, which is deliberate. | slide | — | — | "mature, honest, usable by NTRO" | — |

Every number on screen is fixed by the seed, so the narration cannot be contradicted by the machine.

---

## 36. PART XXXVI — HERO MOMENT

The single defensible differentiator, in one click: **"Why are these two identities linked?"** answered as a balance sheet with a visible independence discount and a toggle that shows what the naive answer would have been.

Why it lands: every competing system aggregates a similarity score; we decompose it, show what we refused to count and why, and demonstrate the failure mode we avoided. It is simultaneously the technical contribution, the forensic argument, and the reason a judge believes the rest of the demo. The subsystems behind that one click are canonicalisation, independence keying, rarity weighting, hub suppression, capped fusion, and the persisted trace — which means the hero moment is also the integration test for six phases.

---

## 37. PART XXXVII — PRESENTATION DESIGN SYSTEM

Palette: background `#0B1220` (dark navy) and `#151B26` for panels; text `#E6EAF2`; muted `#8B95A7`; single accent `#4C8DFF` used only for the one thing that matters on each slide; two semantic colours, `#3FB68B` for supported and `#D9534F` for excluded/contradicted, used nowhere decoratively. Type: Inter or IBM Plex Sans, 40pt titles, 24pt body, 18pt captions, generous margins, left-aligned, no centred paragraphs. Diagrams are thin-stroke boxes and arrows with labelled edges; every diagram carries a one-line caption stating what it proves.

Banned outright: Matrix rain, hooded figures, skull motifs, neon glow, fake radar sweeps, world maps with arcing attack lines, gratuitous padlocks and shields, stock "hacker" photography, decorative charts with no data, 3-D bars, gradients as ornament, animated transitions beyond a cut. Each slide holds one idea; if a slide needs two ideas it is two slides.

Rule for every chart: it plots numbers that `make evaluate` regenerates, and its axes are labelled with units and n.

---

## 38. PART XXXVIII — SLIDE-BY-SLIDE BLUEPRINT (22 slides)

**Slide 1 — PRAMANA: evidence-graded attribution support for dark-web investigations**
*Question:* what is this? *Takeaway:* a system that turns scattered dark-web traces into calibrated, auditable investigative leads.
*On slide:* product name; one-line descriptor; SIH PS 26151 · NTRO; team name. *Visual:* full-bleed navy, name at optical centre-left, thin accent rule. *No diagram. No chart.*
*Notes:* name the problem statement and the organisation in the first sentence; do not describe features yet. *Judge takeaway:* serious, scoped. *Transition:* "Start with why attribution fails today."

**Slide 2 — The investigator's actual problem**
*Question:* what is broken? *Takeaway:* the bottleneck is not collection, it is deciding which correlations are trustworthy.
*On slide:* three lines — "Data is abundant. Correlations are cheap. Defensible conclusions are rare." plus one sentence naming the consequence: a wrong merge contaminates every downstream conclusion.
*Visual:* three stacked statements, the third in accent. *Diagram:* none. *Chart:* none.
*Notes:* investigators drown in weak links; tooling that outputs a similarity score moves the problem, it does not solve it. *Judge takeaway:* they understand the domain, not just the tech. *Transition:* "So what do we actually build?"

**Slide 3 — What PRAMANA does**
*Question:* what does it do? *Takeaway:* collect and seal, resolve identities, weigh evidence with its dependencies exposed, and report with provenance.
*On slide:* four verbs — SEAL · RESOLVE · WEIGH · DEFEND — each with one clause.
*Visual:* four columns, thin dividers. *Diagram:* single horizontal pipeline strip. *Chart:* none.
*Notes:* WEIGH is where our contribution sits; foreshadow it. *Judge takeaway:* clear mental model in 20 seconds. *Transition:* "The problem statement asked for three capabilities."

**Slide 4 — The three capabilities, honestly scoped**
*Question:* do you meet the brief? *Takeaway:* all three, each delivered at the level the physics and the law actually permit.
*On slide:* three rows — Infrastructure analysis: *targeted, authorised scanning of seeds; no Tor enumeration, which v3 makes impossible.* Cross-marketplace mapping: *one relationship graph with independence-aware weighting.* Persona analysis: *stylometry as a gated corroborator, plus handover detection.*
*Visual:* three rows, each with a small "what we do / what is impossible" pair. *Diagram:* none. *Chart:* none.
*Notes:* say plainly that v2 HSDir enumeration died in October 2021 and v3 descriptors are encrypted under rotating blinded keys, so any team claiming network-wide enumeration is claiming something false. *Judge takeaway:* technical honesty as a competence signal. *Transition:* "Here is the architecture that supports that."

**Slide 5 — Architecture (hero slide 1)**
*Question:* how is it built? *Takeaway:* four trust zones, one Postgres, nine analytical layers, one provenance chain running through all of it.
*On slide:* the zone diagram with two annotations: "the collector cannot reach the database" and "the database cannot reach the internet".
*Visual:* left-to-right Z1→Z4 with the sealed-artefact chain as a spine beneath. *Diagram:* yes, the primary one. *Chart:* none.
*Notes:* the two annotations are testable assertions that run in CI, not intentions. *Judge takeaway:* deployable inside an agency boundary. *Transition:* "Everything rests on the evidence model."

**Slide 6 — Evidence model: nine families, capped**
*Question:* how is evidence represented? *Takeaway:* every item has a family, a rarity, a decay, and a hard ceiling on how much it can ever contribute.
*On slide:* the nine families with their log₁₀ LR caps, and the global ceiling of 4.0.
*Visual:* horizontal bars sized by cap, cryptographic longest, behavioural shortest. *Chart:* the caps themselves.
*Notes:* caps are a design decision, judgement-set and sensitivity-tested at ±50%; we state that rather than implying they are learned. *Judge takeaway:* disciplined, not arbitrary. *Transition:* "But caps are not the hard part."

**Slide 7 — The hard problem: evidence is not independent (hero slide 2)**
*Question:* what is the real technical difficulty? *Takeaway:* five sources repeating one artefact is one piece of evidence, and treating it as five is how false attributions are manufactured.
*On slide:* one mirrored listing appearing on five sites; the naive sum; the correct grouped sum.
*Visual:* five document icons collapsing into one canonical artefact. *Diagram:* yes. *Chart:* two numbers side by side.
*Notes:* this is the failure mode behind confident wrong conclusions in link analysis; it is also the error the research literature we reviewed commits on itself. *Judge takeaway:* this team found the actual problem. *Transition:* "So how do we fix it?"

**Slide 8 — Our answer: fix correlation in the data layer, not the maths (hero slide 3, differentiation)**
*Question:* what is your contribution? *Takeaway:* we canonicalise artefacts and assign independence keys at ingest, so the scorer can never double count.
*On slide:* the canonicalisation rules in short form (SHA-256 exact · SimHash ≤3 · containment ≥0.8 · pHash ≤6 · source clusters at overlap >0.6) and one line: "correlation is a data-model property, not a fusion-algebra problem."
*Visual:* ingest → canonicalise → independence key → grouped fusion. *Diagram:* yes. *Chart:* none.
*Notes:* mention that the popular answer in the literature is Dempster-Shafer or Subjective Logic, and that Dempster's rule of combination *presupposes independent bodies of evidence*, so it cannot repair non-independence — it only hides it behind heavier notation. *Judge takeaway:* they rejected a fashionable answer for a correct one. *Transition:* "The score itself is deliberately boring."

**Slide 9 — The fusion computation**
*Question:* how do you compute confidence? *Takeaway:* rarity-weighted, decayed, grouped, damped, capped log-likelihood ratios, with hubs zeroed and counter-evidence subtracted.
*On slide:* the seven-line pseudocode block from §12, unaltered, plus "two independent families minimum, or the claim stays weak."
*Visual:* monospaced block, one accent highlight on the grouping line. *Chart:* none.
*Notes:* it is transparent by choice; every term is inspectable in the UI and every assessment stores a replayable trace with a params version. *Judge takeaway:* explainable arithmetic beats an opaque model in a forensic setting. *Transition:* "And it is allowed to say no."

**Slide 10 — Counter-evidence and exclusion (hero slide 4, credibility: how we prevent false attribution)**
*Question:* how do you avoid false attribution? *Takeaway:* six independent brakes, any one of which can stop a conclusion.
*On slide:* hub suppression · clone/mirror detection · must-not-link vetoes that emit EXCLUDED with no number · the two-family floor · the global ceiling of 4.0 · sequential unmasking in the review flow.
*Visual:* six items, the veto in the exclusion colour. *Diagram:* none. *Chart:* none.
*Notes:* a system that cannot refuse cannot be trusted; the veto path emits no numeric score at all, precisely so a number cannot be quoted out of context. *Judge takeaway:* this is the slide that makes the rest believable. *Transition:* "We also track what we believed and when."

**Slide 11 — Belief time**
*Question:* what happens when a source is wrong? *Takeaway:* we store event time, observation time and belief time, so retraction propagates and old conclusions are reconstructable rather than silently rewritten.
*On slide:* "What did we believe on 12 March, and why did it change?" plus the retraction impact line.
*Visual:* two-axis lane diagram, event time horizontal, belief time vertical. *Diagram:* yes. *Chart:* none.
*Notes:* investigations are audited months later; a system that overwrites history cannot survive that. *Judge takeaway:* audit-grade, unusual for a hackathon build. *Transition:* "Persona linking is where teams overclaim."

**Slide 12 — Stylometry, scoped honestly**
*Question:* can you link rebranded personas by writing style? *Takeaway:* style is a corroborator capped at 1.0, never a basis for attribution on its own, and its main forensic value is detecting *discontinuity*.
*On slide:* three lines — topic confound is reported with every metric; LLM-assisted rewriting triggers a plausibility gate that suppresses the contribution; a style *break* inside one account is evidence of handover.
*Visual:* a per-account style series with a marked changepoint. *Chart:* yes, that series.
*Notes:* the literature we audited shows current LLMs do not reliably imitate a target author's style (measured similarity sits near the cross-author floor), so the honest framing is degradation and noise, not defeat — and we designed a gate rather than a claim. *Judge takeaway:* calibrated, not credulous. *Transition:* "Same discipline on the money side."

**Slide 13 — Blockchain, scoped honestly**
*Question:* do you trace crypto? *Takeaway:* address-level and heuristic cluster evidence with the heuristic's failure conditions detected and the claim suppressed when they fire; Monero is not traced, and we say so.
*On slide:* "Common Input Ownership Heuristic — degraded by CoinJoin, PayJoin and exchange batching. When detected, the heuristic is suppressed." plus label provenance grades A/C/E.
*Visual:* one address graph with a suppressed region shown greyed. *Diagram:* small. *Chart:* none.
*Notes:* vendor labels are not evidence unless their provenance is graded; we weight by grade. *Judge takeaway:* they know where the tooling industry overclaims. *Transition:* "Now, where does the data come from — lawfully?"

**Slide 14 — Lawful data strategy: PRAMANA RANGE**
*Question:* how do you demonstrate this without touching illegal material? *Takeaway:* a synthetic multi-marketplace corpus with hidden ground truth, plus onion services we own and deliberately misconfigured.
*On slide:* RANGE-SIM (3 markets, 25 operators, 60 accounts, 400+ documents, planted traps, seed-locked) and RANGE-TOR (4 self-owned misconfigurations, allowlisted targets only).
*Visual:* two panels. *Diagram:* none. *Chart:* corpus composition.
*Notes:* ground truth lives in a separate schema with no foreign key into the pipeline, and a CI test asserts no module can read it; that is what makes our accuracy numbers meaningful rather than circular. *Judge takeaway:* rigorous and legally clean. *Transition:* "Which lets us measure ourselves."

**Slide 15 — Evaluation: forensic metrics, not accuracy theatre**
*Question:* how good is it? *Takeaway:* we report Cllr, calibration and false-merge rate against hidden ground truth, because "accuracy" is meaningless for evidential strength.
*On slide:* Cllr and Cllr_min · reliability diagram / ECE · Tippett plot · false-merge rate ≤2% target · corpus snapshot id.
*Visual:* two small plots side by side, reliability and Tippett. *Chart:* both, real output of `make evaluate`.
*Notes:* Cllr penalises confident wrong answers far more than uncertain ones, which is exactly the behaviour a forensic system should be graded on. *Judge takeaway:* they measured, and by the right yardstick. *Transition:* "And we proved the architecture earns its complexity."

**Slide 16 — Ablation: does independence handling actually matter?**
*Question:* is your central idea load-bearing? *Takeaway:* turning off independence grouping measurably worsens Cllr and inflates false merges — the mechanism is validated, not assumed.
*On slide:* the ablation grid (full · no rarity · no grouping · no counter-evidence · no caps · style-only · crypto-only) with Cllr and false-merge for each.
*Visual:* one grouped bar chart, the "no grouping" bar in the exclusion colour. *Chart:* yes, the central empirical claim of the project.
*Notes:* if this experiment had shown no effect, we would have reported that and reduced the claim; the number on the slide is whatever the run produced. *Judge takeaway:* scientific posture. *Transition:* "Here is what an investigator sees."

**Slide 17 — The workspace**
*Question:* is it usable? *Takeaway:* four synchronised panes — graph, time, evidence, hypothesis — sharing one selection and one `as_of` clock.
*On slide:* one clean screenshot, four callouts.
*Visual:* screenshot at 70% width, callouts on the right. *Diagram:* none. *Chart:* none.
*Notes:* uncertainty is shown as decomposed family contributions rather than edge thickness, because thickness conflates strength with count; we note this is an unsettled HCI question and that we chose the decomposing representation deliberately. *Judge takeaway:* built for an analyst, not for a screenshot. *Transition:* "One case, end to end."

**Slide 18 — Case walkthrough (hero slide 5)**
*Question:* does the loop actually close? *Takeaway:* question → sealed evidence → resolution → weighted assessment → challenge → signed report, in one screen sequence.
*On slide:* six thumbnails in order with the outcome under each, ending in a footnote that resolves to an artefact hash.
*Visual:* filmstrip. *Diagram:* none. *Chart:* none.
*Notes:* narrate the discount moment and the exclusion moment; those are the two beats judges remember. *Judge takeaway:* it is a system, not a set of components. *Transition:* "Including what it refuses to do."

**Slide 19 — What we are not claiming**
*Question:* where are the limits? *Takeaway:* we produce investigative leads with calibrated confidence; we do not produce legal identity, and no amount of our evidence substitutes for lawful process.
*On slide:* five negatives — no de-anonymisation of the Tor network · no real-world identity output · no Monero tracing · no claim of automatic court admissibility · no surveillance of private individuals.
*Visual:* five lines, no icons, generous space. *Diagram:* none. *Chart:* none.
*Notes:* the claim ladder tops out at attribution hypothesis; verified identity is reachable only through lawful process, and that ceiling is a design decision. *Judge takeaway:* trustworthy. This slide raises the credibility of every earlier one. *Transition:* "What we do claim is defensible and hard to copy."

**Slide 20 — Why this is hard to replicate**
*Question:* what is the moat? *Takeaway:* the independence-aware evidence layer, the bitemporal belief model, the calibration harness and the refusal machinery are architectural commitments, not features that can be bolted on later.
*On slide:* four ranked items with one clause each.
*Visual:* ranked list, thin rules. *Diagram:* none. *Chart:* none.
*Notes:* any of these retrofitted into an existing similarity-score tool would require rewriting its data model, which is why competitors ship aggregate scores instead. *Judge takeaway:* durable technical position. *Transition:* "And here is the path to a real deployment."

**Slide 21 — Path to deployment**
*Question:* what happens after the hackathon? *Takeaway:* the prototype is one Postgres and four containers by design; the production path, its triggers and its governance requirements are already specified.
*On slide:* prototype vs production columns, plus the numeric migration triggers (5M edges · 800 ms p95 traversal · 200 docs/s ingest) and the governance items (ENFSI-style method validation, BSA s.63 certification workflow, DPDP compliance posture, external audit).
*Visual:* two columns with an arrow and the trigger conditions on the arrow. *Diagram:* yes. *Chart:* none.
*Notes:* migration is triggered by measurements, not by fashion; we are explicit that a student team is not a State instrumentality and inherits no data-protection exemption. *Judge takeaway:* they thought past the demo. *Transition:* "To close."

**Slide 22 — Close**
*Question:* what should we remember? *Takeaway:* PRAMANA makes the strength of an attribution inspectable, and that is the difference between a lead and a liability.
*On slide:* one sentence, the product name, and the four verbs from slide 3.
*Visual:* near-empty slide, accent rule. *Diagram:* none. *Chart:* none.
*Notes:* end on the inspectability claim and stop talking; leave time for questions, which is where slide 10 and slide 19 pay off. *Judge takeaway:* clarity and confidence without overclaim.

Optional appendix slides, shown only if asked: schema diagram, evidence-family cap sensitivity analysis, red-team table, STIX mapping, legal annexure, team and phase plan.

---

## 39. PART XXXIX — JUDGE DEFENCE

**1. "Is this actually de-anonymisation?"** It is attribution *support*. We link pseudonymous identities to each other and to infrastructure indicators with graded confidence, and we stop at an attribution hypothesis. Converting a hypothesis into a legal identity requires lawful process — subpoenas, MLATs, seizure — which no software can or should substitute for. We chose to make that ceiling explicit rather than let a demo imply otherwise.

**2. "Can you de-anonymise Tor?"** No, and neither can anyone by enumeration. v2 was deprecated in October 2021; v3 descriptors are encrypted under rotating blinded keys, so the directory-scraping approach that older papers describe no longer exists. What remains exploitable is operator error — a status page left exposed, a certificate shared with a clearnet host, a reused template. We analyse those, on targets we are authorised to touch.

**3. "Where does your data come from? Is it legal?"** Synthetic corpus with hidden ground truth, plus onion services we own and deliberately misconfigured, plus public archives. We never purchase, never handle inherently illegal material, and a drop-on-match hash screen prevents such payloads from ever being persisted. Probe targets are constrained by a hard-coded allowlist asserted in CI.

**4. "Your accuracy numbers come from synthetic data — so they mean nothing?"** They mean something specific and limited: they measure whether the mechanisms behave as designed under known noise and known traps, and they let us run ablations no real corpus would permit because no real corpus has labels. We state the generation parameters alongside every metric, and we do not claim the numbers transfer to live marketplaces. That is exactly the distinction most tooling vendors blur.

**5. "Why not use Dempster-Shafer or Subjective Logic? That is what the literature recommends."** Because Dempster's rule of combination assumes independent bodies of evidence. Our central problem is that our evidence is *not* independent, so the framework's core operator is invalid in precisely the case we care about, and Zadeh's conflict pathology makes it worse under contradiction. We fixed independence upstream by canonicalising artefacts, which makes a simple grouped log-LR sum sound. A Bayesian network with explicit shared latent parents is the principled next step, and it is on the V2 roadmap with the honest reason it is deferred: we do not yet have enough labelled pairs to fit it.

**6. "Why not a GNN, or an LLM, as the decision engine?"** A GNN cold-starts badly on a sparse graph of this size and would be unexplainable in a forensic context; we would not be able to answer "why" for any edge. An LLM cannot be the authority for an identity claim because its reasoning is not reproducible, not calibrated, and not auditable. The LLM in our system is a retrieval-grounded explainer with no write path and no tools in any context containing untrusted text, and the demo runs with it disabled.

**7. "How do you prevent false attribution?"** Six independent brakes: hub suppression via IDF, clone and mirror detection, hard must-not-link vetoes that emit EXCLUDED with no numeric score, a two-independent-family minimum before any claim rises above weak, a global ceiling of 4.0 log₁₀ LR, and sequential unmasking in the review flow so the analyst sees counter-evidence before the score. The ablation in slide 16 measures what happens when we remove them.

**8. "What stops the graph collapsing into one giant blob?"** Hub detection at τ=12 forces shared indicators to zero weight, hub edges are removed before transitive closure, cluster components are size-capped, must-not-link constraints veto merges, and we report false-merge rate as the headline ER metric rather than recall. Component size is a CI assertion, not a hope.

**9. "An adversary reads your paper. How do they beat you?"** Style laundering, deliberate indicator sharing to create hubs, planting our own detectors' signatures on innocents, and fragmenting operations so no two accounts share anything. Our red-team table lists fifteen such attacks with mechanism, defence and residual risk. Several residual risks are real and we name them; a well-run adversary with disciplined compartmentation is not detectable by this or any correlation system, and claiming otherwise would be the dishonest answer.

**10. "Could this be used to target innocent people?"** That is the risk we designed against hardest. It cannot output a real-world identity. Its highest claim is a hypothesis with a stated defence hypothesis. It refuses rather than guesses when exclusion criteria fire. Analyst review is mandatory, logged and non-skippable, and every claim in every report resolves to a sealed artefact so a wrong conclusion is traceable to its cause rather than laundered into a confident summary.

**11. "How is this admissible in court?"** We do not claim admissibility; that is a judicial determination. We build the preconditions: capture-time sealing, SHA-256 manifests, hash-chained audit logs, RFC 3161 timestamping support, ISO/IEC 27037-aligned acquisition documentation, and a certification workflow compatible with s.63 of the Bharatiya Sakshya Adhiniyam 2023. Method validation to ENFSI standards for likelihood-ratio reporting is scoped as production work, not claimed as done.

**12. "What about DPDP Act compliance?"** We process publicly available data, we minimise, and we log purpose. We explicitly do not claim the s.17 exemption available to State instrumentalities, because a student team is not one. In an authorised deployment the operating agency's lawful basis governs; that boundary is documented rather than assumed away.

**13. "What is genuinely novel here versus Maltego, OpenCTI or Chainalysis?"** Those tools either visualise links you assert or output an aggregate score. None of them, to our knowledge, model evidence *non-independence* as a first-class data property, or store belief time so a retraction propagates through past conclusions, or ship a calibration harness that grades their own confidence with Cllr. Our contribution is not a new algorithm; it is an architecture where the strength of a conclusion is inspectable and where the system is capable of refusing.

**14. "The score caps look arbitrary."** They are expert-judgement priors, and we say so in the report methodology rather than implying they were learned. We run a sensitivity analysis perturbing every cap by ±50% and report how band assignments shift; the design intent is that no single family can carry a conclusion alone, which is robust to cap choice. Fitting caps empirically requires a labelled reference population that does not exist for this domain — which is itself one of our stated open problems.

**15. "Can it scale?"** At prototype scale — ≤10⁵ nodes, tens of thousands of documents — one Postgres with recursive CTEs, GiST temporal indexes and pgvector meets our latency budgets, and we publish those budgets. Migration triggers are numeric: a graph engine at 5×10⁶ edges or 800 ms p95 three-hop traversal, dedicated search at 5×10⁶ documents, a message bus above 200 docs/s. We deliberately did not deploy Kafka and Neo4j for a corpus that Postgres handles in milliseconds.

**16. "What if the demo breaks?"** It runs offline with a fixed seed, so every number on screen is deterministic; the collector defaults to replaying pre-sealed WARCs rather than live fetching; and each beat has a pre-captured fallback. We rehearse three timed runs, one with the network physically disabled and one with a deliberately induced service failure.

**17. "Six students built all this?"** Six phases with named primary and secondary owners, one database, one backend language, four containers, and a hard feature freeze after the evaluation phase. The scope discipline is the reason it works: we cut broad crawling, GNNs, streaming, multi-tenancy and Monero tracing, and each cut is recorded with the condition under which it would be added.

**18. "Why should NTRO care?"** Because the operational failure mode in attribution work is not missing a link — it is acting on a confident wrong one. This system makes the strength of every link inspectable, records what was believed and when, refuses when evidence contradicts, and produces reports whose every claim resolves to a sealed artefact. That is the property an agency needs before automated correlation can be trusted in an investigation.

---

## 40. PART XL — WHAT WE CLAIM AND WHAT WE DO NOT

**We claim:** sealed, provenance-verifiable collection from lawful sources; cross-marketplace account-to-persona resolution with measured false-merge rate; evidence weighting that groups non-independent items and suppresses low-information hubs; calibrated verbal confidence bands with a persisted, replayable computation trace; bitemporal belief tracking with retraction propagation; detection of authorised, self-owned hidden-service misconfigurations and their correlation to clearnet indicators, with alternative explanations shown; stylometric corroboration within a hard cap plus style-discontinuity detection; a system that emits EXCLUDED rather than a number when exclusion criteria fire; signed reports and CSV/JSON/STIX exports carrying corpus snapshot and params versions.

**We do not claim:** de-anonymisation of the Tor network or any capability against Tor's cryptography; production of any real-world identity; Monero or modern-mixer tracing; that our synthetic-corpus metrics transfer to live marketplaces; automatic court admissibility; validated likelihood-ratio methodology to ENFSI standard (scoped, not done); any government endorsement, deployment history, or "proven in the field" status; any claim that the system replaces analyst judgement; and no percentage about how attributions historically succeed, because the sample behind that widely-repeated figure is five hand-coded cases and cannot carry it.

---

## 41. PART XLI — TECHNICAL MOAT, RANKED

1. **Independence-aware evidence layer.** Canonical artefact identity and independence keys assigned at ingest. Retrofitting this into a similarity-score tool requires rewriting its data model, which is why none of them have it.
2. **Bitemporal belief model with retraction propagation.** Event, observation and belief time as first-class columns. Cannot be added later without rewriting every write path.
3. **Calibration and refusal machinery.** Cllr, Tippett, reliability diagrams, exclusion vetoes, the two-family floor and the global ceiling. Requires ground truth, which requires the synthetic range — so the moat includes the data-generation capability.
4. **Ablation-validated architecture.** The claim that independence handling matters is measured, not asserted; the harness that measures it is itself a deliverable.
5. **Lawful demonstrability.** RANGE-SIM plus self-owned misconfigured onion services means the system can be shown, audited and reproduced by anyone without touching illegal material.

---

## 42. PART XLII — WHAT WOULD HAVE TO BE TRUE FOR THIS TO BECOME A SERIOUS PRODUCT

A reference population for the domain would have to exist, or be constructed under an authorised agency, so likelihood ratios could be calibrated against real base rates instead of synthetic ones. The independence structure of open sources would need empirical measurement rather than our threshold-based approximation. Method validation to ENFSI standard would need completing, with external review. Deployment would need to sit inside an agency's lawful boundary, with its own basis for processing and its own retention rules. A labelled pair corpus large enough to fit a Bayesian network with shared latent parents would replace the capped additive model. Analyst feedback would need poisoning-resistant incorporation. And the false-merge rate would need continuous monitoring in production, because the failure mode that matters is silent contamination, not visible error.

Absent those, this is a defensible research prototype and an investigative aid — which is what we present it as.

---

## 43. PART XLIII — FINAL DECISION MATRIX

| Decision | Chosen | Rejected | Why | Confidence | Reversible? |
|---|---|---|---|---|---|
| Fusion framework | capped, grouped, rarity-weighted additive log-LR | Dempster-Shafer, Subjective Logic, full Bayesian network | DS/SL assume independent evidence, which is the exact thing we lack; BN needs labels we do not have | high | yes, BN is a drop-in successor |
| Where correlation is handled | data layer (canonical artefacts + independence keys) | fusion algebra | correlation is a property of artefacts, not of arithmetic | high | no, this is architectural |
| Primary store | one PostgreSQL 16 | Neo4j + Elasticsearch + Qdrant + Kafka | one transaction covers evidence and edges; cross-store FK integrity is impossible; no prototype benefit | high | yes, with numeric triggers |
| Graph | logical projection, recursive CTEs | graph database | ≤10⁵ nodes traverses in ms | high | yes |
| Temporal model | bitemporal with belief time | single timestamp, or event-sourcing only | audits ask "what did you believe then" | high | no |
| ER engine | Splink / Fellegi-Sunter with constraints | bespoke scorer, embeddings-only clustering | interpretable m/u probabilities, and vetoes are expressible | high | yes |
| Stylometry role | gated corroborator, cap 1.0, plus changepoint detection | primary linkage signal | topic confound and adversarial rewriting make it unsafe alone | high | cap is tunable |
| LLM role | retrieval-grounded explainer, off by default | decision engine or agent | not reproducible, not calibrated, not auditable | high | yes |
| Capability 1 scope | targeted, allowlisted, authorised probing | network-wide enumeration | v3 makes enumeration impossible and it would be unlawful anyway | high | no |
| Blockchain scope | CIOH with suppression + graded labels | full cluster attribution, Monero tracing | not achievable to evidentiary standard | high | no |
| Data strategy | RANGE-SIM + RANGE-TOR + public archives | live marketplace crawling | lawful, safe, and the only way to get ground truth | high | no |
| Output ceiling | 4.0 log₁₀ LR, no identity claim | unbounded score, identity output | prevents the failure mode that matters most | high | no |
| Uncertainty display | decomposed family contributions | edge thickness / single score | thickness conflates strength with count | medium — unsettled in the literature | yes |
| Family caps | expert-judgement priors, ±50% sensitivity-tested | learned weights | no reference population exists to learn from | medium, stated as such | yes |
| Queue | Postgres job table with SKIP LOCKED | Kafka, Celery | one producer, four consumers | high | yes |
| Deployment | Docker Compose, offline `make demo` | Kubernetes, cloud-hosted | judged on a laptop with no network | high | yes |

---

## 44. PART XLIV — ONE-PAGER

**PRAMANA** — evidence-graded attribution support for dark-web investigations. SIH PS 26151, NTRO.

**Problem.** Investigators are not short of data or correlations; they are short of defensible conclusions. The operational failure is acting on a confident wrong link, and the mechanism behind confident wrong links is counting the same underlying artefact many times.

**Thesis.** Attribution confidence is only meaningful if the *dependence* between pieces of evidence is modelled. So we canonicalise artefacts and assign independence keys at ingest, and the scorer can never double count.

**System.** Four trust zones — an isolated Tor-only collector, an ingest zone with no outbound network, an analytical zone, a presentation zone. One PostgreSQL 16 carrying relational, bitemporal, graph, lexical and vector workloads. Nine analytical layers over one provenance chain: capture and sealing, extraction, canonicalisation, entity resolution, evidence weighting, fusion, counter-evidence, assessment, reporting.

**Method.** Nine evidence families with log₁₀ LR caps from 0.7 (behavioural) to 4.0 (cryptographic). Rarity weighting by IDF; hubs above τ=12 forced to zero. Non-independent items grouped, strongest member counted, others damped at λ=0.2. Per-family caps, counter-evidence subtracted, a two-independent-family floor, and a global ceiling of 4.0. Hard must-not-link vetoes emit EXCLUDED with no numeric score at all.

**Honesty.** Highest output is an attribution hypothesis with a stated defence hypothesis. No real-world identity. No Tor de-anonymisation. No Monero tracing. No admissibility claim. Synthetic-corpus metrics reported with generation parameters and not claimed to transfer.

**Data.** RANGE-SIM: three synthetic marketplaces, 25 operators, 60+ accounts, 400+ documents, planted traps, hidden ground truth in an unreachable schema, seed-locked. RANGE-TOR: four self-owned, deliberately misconfigured hidden services on a CI-asserted allowlist.

**Evidence it works.** Cllr and Cllr_min, reliability diagram and ECE, Tippett plots, false-merge rate ≤2%, and an ablation grid showing that disabling independence grouping degrades performance — regenerated by `make evaluate`.

**Differentiator, in one click.** "Why are these linked?" returns a balance sheet with the independence discount visible and a toggle showing the inflated naive answer.

**Delivery.** 15 dependency-ordered phases, 6 owners with named backups, 10 milestones, a deterministic 7–10 minute offline demo, a 22-slide briefing deck, and a hard feature freeze before rehearsal.

---

## 45. PART XLV — FINAL RED TEAM (against this blueprint itself)

**The riskiest claim in this document** is that independence grouping measurably improves evidential quality. It is currently a design argument supported by first principles, not yet a measured result. Phase 12 is where it becomes empirical, and if the ablation shows no effect, this blueprint requires amendment rather than defence. That is written into the phase's acceptance criteria deliberately.

**The second riskiest** is the evidence-family caps. They are judgement, dressed in arithmetic. The sensitivity analysis mitigates the risk of a specific cap being wrong; it does not mitigate the possibility that the whole cap-based approach is a poor approximation of the underlying evidential structure. We state this in the report methodology, and it is the reason the Bayesian network is on the roadmap rather than described as unnecessary.

**Where synthetic data could mislead us.** RANGE-SIM's traps are traps *we* designed, so the system is being tested against our own imagination of adversary behaviour. Real operators will fail and succeed in ways we did not model. The stated mitigation — noise parameters and validating extractors against real public archives — reduces but does not remove this circularity, and no amount of engineering removes it. Anyone reading our metrics should read them as "the mechanisms behave as specified", not "the system works in the wild".

**Scope risk.** This blueprint describes more than six people build comfortably. The most likely failure is Phase 11 and Phase 12 colliding at the end, with the evaluation harness sacrificed to finish the UI. That would be the wrong trade, because the evaluation harness is the credibility of the entire submission; the correct sacrifice, if one is needed, is the blockchain module, the copilot and the STIX exporter, in that order.

**Presentation risk.** Slides 7 through 10 carry the whole argument, and they are the abstract ones. If they are rushed, the demo becomes an ordinary link-analysis tool with good manners. Rehearsal time should be allocated disproportionately to those four slides and to the two demo beats — the discount and the exclusion — that make them concrete.

**The most likely judge objection we cannot fully answer** is question 9: a disciplined adversary who shares nothing across identities is invisible to us, and no correlation system can fix that. We answer it by naming it, which is better than pretending otherwise but is not a solution.

**What would make us abandon a core assumption.** If a labelled real-world corpus became available and showed that naive additive scoring calibrates as well as grouped scoring, the independence layer would be over-engineering and should be simplified. If stylometric verification on multilingual marketplace text proved to hold up under topic control at high c@1, the 1.0 cap on F6 would be indefensibly conservative and should rise. Both are empirical questions, and both are stated as such rather than settled by assertion here.

---

## Verification checklist

- [x] Every dossier finding re-graded independently; Gemini's tiers not inherited (§2)
- [x] The ">85% of attributions depend on OPSEC failures" claim traced to its n=5 sample, downgraded to directional, and barred from slide use (§2.1, §40)
- [x] Citation defects catalogued: Rid & Buchanan misattributed to arXiv; two near-identical LLM-personalisation papers double-counted; four off-domain DS/SL sources; Reddit, Scribd and vendor blogs used as load-bearing evidence (§2.2)
- [x] The dossier's headline recommendation (Dempster-Shafer / Subjective Logic) rejected with three independent reasons and replaced (§1.6, §12, §39 Q5)
- [x] Observation / Evidence / Correlation / Entity Resolution / Attribution Hypothesis / Verified Identity kept distinct, with no silent promotion between tiers (§8, §14)
- [x] SIH prototype architecture and production architecture separated, with numeric migration triggers (§29.2, §29.3)
- [x] Minimum remarkable MVP defined as one closed-loop investigation, with an explicit in/out filter (§30)
- [x] Deterministic 7–10 minute demo, offline, seed-locked, with per-beat fallbacks (§35)
- [x] 22-slide briefing deck with a restrained dark-navy design system and an explicit ban list; no Matrix rain, skulls, neon, fake radar or decorative charts (§37, §38)
- [x] Judge defence covering all 18 questions, including the ones we cannot fully answer (§39)
- [x] Explicit "what we are not claiming", including no government-endorsement or field-proven claims (§40)
- [x] Final decision matrix with confidence and reversibility per decision (§43)
- [x] Self-red-team naming the riskiest claim in this document and the conditions that would overturn it (§45)
- [x] Lawful, defensive scope throughout: no unauthorised access, exploitation, malware, credential theft, Tor attacks, private-individual de-anonymisation, or illegal-content handling
- [x] LLMs excluded from the decision path; used only as a retrieval-grounded explainer with no tools and no write access

*End of blueprint.*























