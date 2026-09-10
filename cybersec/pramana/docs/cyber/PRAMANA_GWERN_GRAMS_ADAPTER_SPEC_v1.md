# PRAMANA Gwern/Grams Cyber Adapter Specification v1

**Version:** GWERN_GRAMS_ADAPTER_SPEC_v1  
**Final inspection date:** 2026-09-09  
**Status:** Frozen deterministic domain/data contract for the archive identified below. Unresolved source meanings are deliberately retained as unknown.  
**Layer:** Source adapter; no attribution, entity resolution, scoring, fusion, clustering or identity inference.

## 1. Purpose and scope

Define how the inspected Grams marketplace CSV records become provenance-preserving PRAMANA normalized observations. The contract covers parsing, deterministic representation, source-local references, missing values and handoff eligibility. It does not create positive evidence or infer operators.

The boundary is:

**RAW OBSERVATION → DETERMINISTIC DERIVATION → ML FEATURE → EVIDENCE CANDIDATE**

The adapter implements only the first two stages and supplies inputs to the ML FEATURE boundary. Feature representation does not itself require a learned model, but candidate promotion remains a separate downstream operation governed by frozen Cyber policy. No stage may silently promote its output to authoritative evidence. A field's existence, family eligibility and eventual positive evidence are three different claims.

The archive also contains an older HTML/assets crawl. This v1 inventories those members but does not parse them into CSV listing observations, join their images to CSV rows, or fetch anything from their links. Their presence and limits are documented rather than incorrectly describing the whole archive as CSV-only.

## 2. Authoritative inputs

| Input | Authority and inspected status |
|---|---|
| [PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md) | Controlling domain policy. Not modified. SHA-256 at inspection: `ab288d7ee4b9cdeb7c6246693aea67a5e373448f252af222f50e7384a3562779`. References below use its CY-POL rule IDs. |
| [grams.tar.xz](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/grams.tar.xz) | Controlling structure/field source. Actually present at repository root; compressed size **69,740,360 bytes**; SHA-256 **`0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6`**. |
| [OPUS_GWERN_VERIFICATION_REPORT.md](C:/Users/revan/OneDrive/Documents/ChatGPT/pramana/OPUS_GWERN_VERIFICATION_REPORT.md) | Acquisition/provenance context only. Its source URLs, licensing descriptions, coverage and completeness claims are not substituted for archive inspection or source qualification. |

**Path discrepancy:** `data/raw/gwern/grams.tar.xz` was not present. This specification was verified against the root archive above; it was not moved. Relocation is permissible as a storage operation, but identity is the actual archive digest, not an assumed path. No external authenticity/signature check for this archive is claimed by computing that digest.

Inspection comprised a complete member inventory, strict UTF-8 decoding and CSV parsing of every CSV member, field-value profiling, within-member duplicate checks and repeated-key/content comparisons. Selected original records and archived HTML were reopened to check the examples and source explanations. Counts below are archive-inspection facts, not benchmark performance.

## 3. Verified Grams dataset structure

### 3.1 Inventory

| Property | Verified result |
|---|---|
| Archive members | **1,910**, all regular-file entries; no repeated member names observed. |
| Sum of member payload sizes | **9,575,600,359 bytes**; not a claimed filesystem extraction footprint. |
| CSV members | **1,865**. |
| Parsed CSV data records | **12,384,326**, excluding each file's header. |
| CSV snapshot labels | **254** distinct directory tokens with **253** distinct date prefixes, spanning `2014-06-09` through `2015-07-12`. |
| Additional snapshot token | `2014-06-11-2` exists and is distinct from `2014-06-11`. Its suffix does not establish a capture time or ordering. |
| CSV basename variants | **21**; raw `market_name` values across all rows: **20**. |
| Non-CSV members | **45**, under `grams/2014-05-28/`: HTML/site resources, CSS, fonts and images. |
| CSV encoding/parser outcome | All CSVs decoded as UTF-8, no BOM; no decoding/CSV parser errors in the completed scan. All records have 11 positional cells. |
| Line structure | Both LF-only and CRLF-containing files occur; quoted values can contain newlines. CSV record numbers are not physical line numbers. |

CSV members follow the observed layout `grams/<snapshot_label>/<basename>.csv`. The archive's member order is not chronological. Do not infer time from iteration order.

### 3.2 CSV filenames and market labels

The basename is a file label, not the authoritative row market name. The following mappings were verified from the first data record of every member with that basename; all-row profiling independently verified the raw market-value set. No claim that a basename is an immutable market ID is made.

| Basename, exact | Member count | Observed first-record `market_name`, exact |
|---|---:|---|
| `1776.csv` | 1 | `1776` |
| `Abraxas.csv` | 42 | `Abraxas` |
| `ADM.csv` | 79 | `Andromeda` |
| `Agora.csv` | 247 | `Agora` |
| `Alpaca.csv` | 41 | `Alpaca` |
| `Alpha.csv` | 76 | `Alphabay` |
| `BB.csv` | 205 | `Black Bank` |
| `Bungee54.csv` | 96 | `Bungee54` |
| `C9.csv` | 94 | `Cloud Nine` |
| `EVO.csv` | 172 | `Evolution` |
| `EVO2.csv` | 25 | `Evolution` |
| `Haven.csv` | 12 | `Haven` |
| `ME.csv` | 222 | `Middle Earth` |
| `NK.csv` | 107 | `Nucleus` |
| `OutLaw.csv` | 143 | `Outlaw` |
| `Oxygen .csv` | 27 | `Oxygen `, with a trailing U+0020 space |
| `Pandora.csv` | 46 | `Pandora` |
| `Silkkitie.csv` | 24 | `Silkkitie` |
| `SilkRoad.csv` | 85 | `Silk Road 2` |
| `TOM.csv` | 45 | `Onion Market` |
| `TPM.csv` | 76 | `The Pirate Market` |

The adapter uses each row's exact `market_name`; it does not fill it from this table, merge different labels, or assign meaning to the numeric prefix of `hash`.

### 3.3 Ancillary material and scope

Verified examples include:

- `grams/2014-05-28/faq`, `contact`, `markets`, `index.html`, `trends` and `results/1`.
- Thirteen JPEG files under `grams/2014-05-28/assets/img/items/`, including `2-25688.jpg` and `2-28111.jpg`.
- Other image, advertisement, favicon, CSS and font resources.

The archived `results/1` HTML refers to local Grams item-image paths as well as remote market image URLs. This establishes that some historical image bytes are bundled; it does **not** establish a complete or validated mapping to the later CSV records.

The archived `contact` page contains a service contact email, a donation-address string and a PGP keyserver lookup link. These concern the Grams page's own assertions, not every vendor. It does not contain a downloaded key merely because it links to one. This adapter does not follow the link.

## 4. Verified raw schema

Every CSV has this exact ordered parsed header:

`["hash", "market_name", "item_link", "vendor_name", "price", "name", "description", "image_link", "add_time", "ship_from", ""]`

The eleventh column has an **empty header and an empty value in every inspected row**. It is a structural trailing cell, not an additional named business field. The adapter validates and preserves its presence; it must not fabricate a name or treat it as a second shipping field.

All CSV cells are strings after CSV decoding. CSV contains no intrinsic integer, decimal, SQL NULL or JSON-null datatype. Integer/decimal representations below are deterministic derivations.

| Position | Exact field | Empty-string records | Additional observed forms |
|---:|---|---:|---|
| 1 | `hash` | 0 | Length 3–82; many values are not hexadecimal digests. |
| 2 | `market_name` | 0 | 20 exact labels, including trailing-space `Oxygen `. |
| 3 | `item_link` | 0 | All begin `http://`; this is lexical observation, not proof of reachability or valid infrastructure. |
| 4 | `vendor_name` | 538 | 3,026 additional whitespace-only values; Unicode and control/newline-bearing values occur. |
| 5 | `price` | 0 | All match nonnegative decimal-string form `[0-9]+\.[0-9]+`; no currency column exists. Zero values occur. |
| 6 | `name` | 8,867 | Literal `none`, `None`, `nan` occur; strings, not native nulls. |
| 7 | `description` | 47,506 | Literal `none` occurs. Observed values are ASCII and contain no C0 controls; length up to 65,535 characters. This does not prove original author prose or lossless capture. |
| 8 | `image_link` | 485,906 | HTTP/HTTPS-prefixed strings, opaque values such as `18-344`, Unicode/space-bearing strings and directory-like URLs. |
| 9 | `add_time` | 0 | Every value contains exactly 10 ASCII digits; numeric range 1,397,951,961–1,436,663,562. Meaning/epoch/units unresolved. |
| 10 | `ship_from` | 5,672 | 55 additional whitespace-only values; `n/a`, `None`, `Unspecified`, broad regions and newlines occur. |
| 11 | Empty header | 12,384,326 | Always empty; structural validation only. |

These observed counts are not input constraints on future content. Structural/schema variation requires explicit rejection or a new adapter version; nullable content remains supported as specified below.

## 5. Field-by-field mapping table

### 5.1 Common rules inherited by every mapping

**Source/schema:** Each row below refers to its exact header position in section 4 in the actual CSV member, never to an inferred marketplace page schema.

**P — provenance:** Every mapped value carries `source_record_id` and the exact 1-based CSV column position/name. Raw decoded strings remain retrievable unchanged through the original archive/member/row. Section 13 defines the full chain.

**S — snapshot:** Every mapping inherits the exact source snapshot label and its date-prefix derivation. This is source packaging context, not a field's actor-event time.

**D — duplicates/dependence:** Repetition never creates independence automatically. Preserve all row occurrences; exact equality is a comparison result, not identity or a PRAMANA independence key. Section 8 applies to every field.

**C — counter-evidence:** No field directly emits negative evidence, suppresses another actor, sets a hard veto or proves cloning. A discrepancy is a source-record discrepancy for downstream review. Missing values mean unavailable information, not evasion or contradiction.

These defaults are part of **every** field's mapping; the per-field overrides below complete the contract.

### 5.2 Datatype, normalization and canonicalization

`present(s)` means that removing only boundary ASCII whitespace (`U+0009`–`U+000D`, `U+0020`) would leave at least one character. This test does not change the raw string. No Unicode folding, transliteration, case folding or identifier trimming is used for identity keys.

| Field / position | Raw datatype and empty/null behaviour | Deterministic normalization | Canonicalization boundary |
|---|---|---|---|
| `hash` / 1 | String. Missing/blank token has no source-hash reference; raw cell preserved. | Copy to `source_hash_raw`; opaque text, no digest validation or prefix splitting. | Exact `(market_name_raw, hash_raw)` may be supplied as a repetition-reference tuple, not canonical listing identity. |
| `market_name` / 2 | String. Blank market leaves account and market-scoped repetition references unavailable. | Copy exact text; optional display text uses boundary ASCII trim only and never feeds keys. | Exact source label scoped to `gwern-grams`; no alias merging, including EVO/EVO2 assumptions. |
| `item_link` / 3 | String. Blank yields no listing reference. | Preserve exact text and assign lexical reference kind under section 9; do not fetch, percent-decode, lowercase, strip queries or infer endpoints. | Exact market/string equality is a repetition reference only. URL reuse is not guaranteed listing identity. |
| `vendor_name` / 4 | String. Empty or whitespace-only yields `observed_account = null`; no shared empty-name account. | Preserve exact text; optional ASCII-trimmed display string is not identity. Unicode and internal/newline characters are retained. | Account label key is exact `(source_namespace, market_name_raw, vendor_name_raw)` when both are present. No person/persona canonicalization. |
| `price` / 5 | String. Empty/blank becomes missing parsed amount; malformed values become invalid parsed amount. Raw always retained. | Accept exactly `[0-9]+\.[0-9]+`; derive an arbitrary-precision decimal value, serialized as the canonical decimal string in section 9. Currency remains null. | Decimal spelling normalization is arithmetic representation only; not price equivalence across currencies, times or markets. |
| `name` / 6 | String. Empty/whitespace-only yields nullable content title. Literal `none`/`None`/`nan` remain strings. | Copy nonblank source text unchanged; no HTML entity decoding or prose repair. | No canonical content/author/listing ID. Exact title equality alone is not a content match. |
| `description` / 7 | String. Empty/whitespace-only yields nullable description; literal `none` retained. | Copy nonblank source text unchanged. Preserve boundaries separately from title. No punctuation restoration, PGP repair or inferred original wording. | Exact `(name_raw, description_raw)` comparison may be provided downstream; canonical artefact grouping is downstream. |
| `image_link` / 8 | String. Empty/whitespace-only yields no image-reference object. Other tokens are retained, including directory-like URLs. | Preserve text; classify lexical reference kind. `18-344` is an opaque token, not a verified relative filename. | No URL-to-image, token-to-path or image-content canonicalization in this adapter. |
| `add_time` / 9 | String. Blank/invalid values preserve raw text and report parse status. | Ten ASCII digits yield integer value only; classification UNKNOWN, semantic status UNRESOLVED, epoch/unit/timezone/instant null. | No time-based deduplication or event inference. Changes do not establish updates or actor activity. |
| `ship_from` / 10 | String. Empty/whitespace-only yields no shipping claim; `n/a`, `None`, `Worldwide`, `EU`, `Unspecified` remain uninterpreted source strings. | Preserve claim text; optional trimmed display only. No country-code/geolocation inference. | Exact spelling is not geographic equivalence; no country or jurisdiction entity automatically created. |
| Empty header / 11 | String required to be empty. Nonempty value is schema violation. | Preserve as `trailing_empty_cell = ""`. | No entity, identifier or evidential interpretation. |

### 5.3 PRAMANA meaning, stage and family eligibility

**Direct evidence candidate creation is NO for every field.** A row does not compare two subjects or establish the validations needed for an attribution candidate. The adapter emits observations and deterministic representations only. Downstream extraction may produce validated candidate inputs under CY-POL-006–014; it must not treat them as positive evidence automatically.

| Field | Entity / observation type | Stage | Eligible family and reason, if later validated |
|---|---|---|---|
| `hash` | Source-provided listing-reference token | RAW copy; reference tuple is DETERMINISTIC DERIVATION | None by itself. Its name does not make it cryptographic evidence. |
| `market_name` | Source marketplace label/context | RAW copy; context key is DETERMINISTIC DERIVATION | None by itself. Market membership is not attribution. |
| `item_link` | Listing-location reference claim | RAW copy; lexical classification is DETERMINISTIC DERIVATION | No F3 infrastructure weight from a URL alone. Actual authorised infrastructure observations would require another source/module. |
| `vendor_name` | OBSERVED ACCOUNT label, source/market-scoped | RAW copy; observed-account key is DETERMINISTIC DERIVATION | No automatic family. Alias scoring assignment remains deferred by CY-POL-005. |
| `price` | Source-reported listing price, unknown currency | RAW copy; parsed decimal is DETERMINISTIC DERIVATION | Potential F5 formatting/price-convention feature only after suitable validation; not an F2 wallet/transaction observation. No economic comparison without currency semantics. |
| `name` | Listing title/content | RAW copy; nullable wrapper is DETERMINISTIC DERIVATION | Potential F5 content and gated F6 text input. Other embedded identifiers need independent extraction/validation. |
| `description` | Listing content, not verified verbatim authored prose | RAW copy; nullable wrapper is DETERMINISTIC DERIVATION | Potential F5; gated F6; possible F1/F2/F4 candidates only if actual recoverable material passes validators. PGP-like text is not a parsed key. |
| `image_link` | Image-reference assertion, not an image entity with bytes | RAW copy; reference kind is DETERMINISTIC DERIVATION | No pHash/EXIF/F5 image match from a link alone. Image features require separately proven byte provenance. |
| `add_time` | Unresolved source time token | RAW copy; integer parse is DETERMINISTIC DERIVATION | None directly. Cannot anchor actor-event F7 scoring while meaning is unresolved. |
| `ship_from` | Unverified shipping-origin claim/context | RAW copy; nullable wrapper is DETERMINISTIC DERIVATION | Possible contextual input to later event-anchored catalogue continuity; no direct F7 weight, F3 location evidence or actual location inference. |
| Empty header | CSV structure | RAW structural cell | None. |

### 5.4 Time, provenance, repetition, counter-evidence and forbidden interpretations

All fields inherit **P/S/D/C** above. The following are field-specific qualifications, not additional automatic detectors.

| Field | Timestamp meaning | Repetition / independence / discrepancy implications | Limitations and forbidden interpretation |
|---|---|---|---|
| `hash` | None supplied by the token | Repeats and changes in associated URL/vendor/content/time are observed; preserve both records. | Not an archive checksum, stable vendor ID, guaranteed immutable listing key or control proof. |
| `market_name` | Inherits snapshot packaging only | Same label across snapshots is context; different CSV basenames do not imply independent markets. | Do not map basename aliases or trim identity strings silently. |
| `item_link` | No fetch/event time encoded by this adapter | One URL can occur with different hashes/content; identical URL is not independent corroboration. | No live reachability, Tor-version capability, server ownership or origin-IP inference. |
| `vendor_name` | Label occurrence in source snapshot, not registration/login | Same exact source/market/name key preserves repeated label observations; changed name is a discrepancy, not handover proof. | Not a person, stable platform-issued vendor ID, verified author or cross-market same operator. |
| `price` | Listing field in snapshot; no trade/payment time | Changes may reflect unknown currency/processing or a source update, not necessarily vendor behaviour. | No currency assumption, revenue, sale, transaction, denomination conversion or zero-price availability claim. |
| `name` | No author/posting time | Exact/copied titles may be templates or reselling, not authorship. | Literal missing-like words remain data; no product/category truth inferred. |
| `description` | No author/posting time | Shared content across markets is directly observed; copying direction and common operator remain unresolved. | No reconstruction of missing punctuation/key bytes or ungated stylometric authorship. |
| `image_link` | No image capture/publication time | Same reference is a repeated reference only; it may name a placeholder/directory. | No image bytes, perceptual similarity, EXIF, actual photo reuse or network retrieval. |
| `add_time` | **UNKNOWN / UNRESOLVED** | It can remain equal or change for a repeated source token; neither behaviour resolves its meaning. | Not actor EVENT TIME, capture time, listing creation time or last-update time without further source proof. |
| `ship_from` | No shipping event time | Changed claims may be source inconsistency; not automatic geographic contradiction. | Not actual vendor location, shipment, destination, customs/jurisdiction or country code. |
| Empty header | None | Repeated structural empty adds no information. | Not a hidden business field. |

## 6. Entity mapping

Normalized objects are source-adapter views, not newly authorised identity tables:

- `source_record`: one logical CSV data-record occurrence.
- `source_snapshot`: exact dated directory token, scoped to the archive.
- `observed_account`: exact nonblank source/market/vendor label key. This preserves label occurrences; it does not resolve distinct operators sharing a label.
- `listing_observation`: record-scoped listing/content representation; there is **no canonical listing ID** in this v1.
- `image_reference`: nullable source string with lexical kind; no inferred image bytes/entity.
- `timestamp`: raw `add_time`, parse status and unknown semantics, plus separate snapshot/acquisition context.
- `shipping_claim`: nullable unverified source statement.
- `provenance`: archive/member/snapshot/row/field lineage.
- `relations`: adapter-local provenance and source-declaration associations only.

No persona or actor is created. No transaction is created from price. Embedded keys/wallets/contacts remain separate potential observed entities for downstream validated extraction; they do not become attributes proving an account's ownership.

## 7. Timestamp semantics

### 7.1 What was established

All CSV `add_time` values are ten-digit integer strings. They are compatible in form with an epoch-style representation, but compatibility is not a source definition.

Archived `grams/2014-05-28/faq`, under **“How often do you index the markets?”**, says Grams searches for new listings daily, updates existing listings every three days in its older system, and updates API-connected markets every 24 hours. This is an archived service claim, not proof each later dump follows that schedule. It does not define `add_time`.

Example: `grams/2015-04-20/Abraxas.csv`, data row 4, and `grams/2015-06-02/Abraxas.csv`, data row 11, share source hash `7-444e070f52290075ac7fabd157bd11db`, but `add_time` changes from `1429352928` to `1433159496`. Therefore the adapter must not declare the field an immutable listing-creation timestamp.

### 7.2 Frozen classifications

| Value | Classification | Output |
|---|---|---|
| CSV `add_time` | **UNKNOWN**; meaning **UNRESOLVED** | Raw string; optional parsed integer; no assigned epoch, unit, timezone or instant. |
| Directory date prefix | Source snapshot-label date, not an event instant | Calendar date at day precision; timezone null. |
| Suffix `-2` | Source packaging discriminator | Preserve raw suffix/token; no inferred time or ordinal chronology. |
| Tar member `mtime` | Archive filesystem metadata | Preserve if needed as archive metadata; not source capture/event/belief time. |
| Actual PRAMANA acquisition/import | OBSERVATION/CAPTURE TIME for PRAMANA's own acquisition, if supplied by its capture process | Separate operational provenance; never substituted for historical capture or actor time. |
| Actor EVENT TIME / original capture time / SOURCE-PUBLISHED TIME | Not established by this CSV schema | Null/unknown, not copied from `add_time`. |
| Belief/assessment time | Downstream system activity | Not produced or backdated by this adapter. |

No relative-time phrases were observed in `add_time`. No absolute-time conversion is authorised until epoch, units and field meaning are established. This uncertainty does not block lossless normalization.

## 8. Snapshot/repetition semantics

Each CSV is a source-file observation within a snapshot label. Snapshot dates are incomplete/irregular, and same-day alternative tokens exist. Do not infer daily completeness, disappearance, inactivity or market shutdown from missing files/records.

The inspection found **297,854 distinct `(market_name, hash)` pairs** and **297,681 distinct `(market_name, item_link)` pairs** across the 12,384,326 occurrences. These are exact source-value reference counts—not counts of canonical listings, accounts or actors. Source hash and URL associations can conflict.

Specific verified cases:

| Case | Original source locations | Consequence |
|---|---|---|
| Repeated row across snapshots | `grams/2015-04-20/Abraxas.csv` row 1 and `grams/2015-04-21/Abraxas.csv` row 1 | Preserve two observations; no independent evidence increment. |
| Same hash, changed vendor string | `grams/2014-06-15/ADM.csv` row 665 (`NOWTHATSTHESTUFF`) and `grams/2014-08-25/ADM.csv` row 1453 (`THEPAWNSHOP`) | Preserve discrepancy; do not infer handover or merge the names. |
| Same URL, different hashes | `grams/2014-06-09/SilkRoad.csv` rows 12209 and 12223 | URL is not a safe unique listing ID. |
| Same hash, changed URL | `grams/2014-07-18/TPM.csv` row 610 and `grams/2014-07-20/TPM.csv` row 610 | Source hash is not proven immutable resource identity. |
| Same exact title/description across markets | `grams/2014-06-09/1776.csv` row 10 and `grams/2015-04-20/Abraxas.csv` row 94 | Content equality is observed; copying direction, independence and operator identity remain unresolved. |

No duplicate full decoded row was found **within an individual CSV** in the completed scan. That does not remove the adapter's requirement to handle duplicates or contradict cross-snapshot repetition.

Optional downstream exact comparisons use ordered tuples, not concatenated strings with ambiguous delimiters:

- Row-value equality: all 11 decoded cells in order.
- Source-hash repetition reference: exact source namespace, market string, hash string.
- Source-URL repetition reference: exact source namespace, market string, URL string.
- Content equality input: exact `(name_raw, description_raw)` tuple. Empty pairs convey no corroborative information.

The adapter exposes these operands but performs no clustering or origin-group assignment. Repetition comparisons must not overwrite prior records.

## 9. Deterministic normalization rules

### N-01 — Input and member validation

For this pinned archive, validate the digest and inventory. Read only regular CSV members at the verified layout. Preserve tar member names exactly; do not interpret them as arbitrary filesystem destinations. Non-CSV members receive inventory-only status. Schema drift, unsafe paths, new member types or changed bytes require a new verification, not automatic acceptance under this archive's verified status.

### N-02 — CSV grammar

Decode UTF-8 strictly. Use comma delimiter, double-quote quote character and doubled double-quotes for quoted quote characters; preserve embedded quoted newlines. No backslash escape reinterpretation. Validate the exact 11-cell header and the empty eleventh header/value. Count logical records after the header starting at 1. LF/CRLF is transport structure, not an additional record when inside a quoted cell.

Malformed encoding/CSV or an unexpected header makes the member unaccepted; a structurally wrong row is quarantined with its available source location. Do not shift cells, truncate extras or silently synthesize missing columns. Publish a member's normalized output only after its structural validation succeeds; field-value issues described below are not structural failures.

### N-03 — Raw values and missingness

Keep every decoded cell exactly, including spaces, newlines, punctuation and Unicode. Empty and ASCII-whitespace-only values may produce nullable normalized optional objects; preserve their different raw values. Literal `None`, `none`, `nan`, `n/a` and `Unspecified` are not CSV nulls and are not globally converted to null. No absent vendor placeholder account is created.

### N-04 — Text and account labels

No destructive Unicode normalization, case folding, transliteration, punctuation restoration, boilerplate stripping, HTML decoding or vendor-name repair. Display-only ASCII boundary trimming is optional and must not affect stored raw values, keys or downstream source offsets. Escape hostile content at rendering, not by modifying evidence text. `Omega²` remains different from `Omega2`.

### N-05 — Price

An exact match to `[0-9]+\.[0-9]+` yields `parse_status=parsed_decimal`. Serialize the decimal without exponent: remove redundant leading integer zeros and trailing fractional zeros; remove the decimal point if no fractional digits remain; zero serializes as `"0"`. Preserve original scale/string in raw provenance. Do not use binary floating point, rounding or currency conversion.

Blank produces `parse_status=missing`; any other lexical form produces `parse_status=invalid_decimal`, amount null, and a field issue while retaining the row. A future integer-only value is invalid under this pinned v1 grammar, not silently accepted as an observed source form. Currency is always null; zero is a reported numeric value, not proof an item is free, in stock or sold.

### N-06 — Reference strings

Classify nonblank `item_link`/`image_link` strings by exact prefix only:

- `http://` → `http_reference_candidate`.
- `https://` → `https_reference_candidate`.
- Otherwise → `opaque_reference`.

This is intentionally **not URL validation**. Do not parse or infer a host, dereference a URL, repair spaces/Unicode, add a base URL, append a file extension, strip query parameters or treat a directory as image bytes. Empty references are null. `18-344` remains opaque; a filename such as `2-25688.jpg` is not invented from a token.

### N-07 — Time

Exactly ten ASCII digits in `add_time` yield `parsed_integer` and `parse_status=parsed_integer`. Blank yields missing; other text yields invalid_integer. In every case semantic class stays UNKNOWN and semantic status UNRESOLVED. No epoch conversion or timestamp-derived event is produced.

### N-08 — Snapshot label

Preserve the complete directory token. For the verified `YYYY-MM-DD` tokens and `2014-06-11-2`, derive the valid calendar date from the first ten characters. Keep any suffix verbatim. Snapshot identity includes the entire token. Future unfamiliar formats are unaccepted until reviewed; do not guess dates from them. The date is not converted to midnight UTC.

### N-09 — Shipping claim

Preserve nonblank `ship_from` exactly, with `interpretation=unverified_source_claim`. Do not split composite regions, translate countries or infer ship-to, vendor residence, origin server or actual shipments. Preserve `n/a` as an uninterpreted source string; its absence-like meaning is not an ISO-country mapping.

### N-10 — Output eligibility

Valid structure permits normalization even when description/image/shipping/account is missing or a price/time field has a value issue. Dependent optional objects become null; unrelated data remains. No adapter flag automatically creates negative evidence, clone status, a hard veto or positive family support. Downstream validators receive raw lineage and limitations, not invented default confidence.

## 10. Canonicalization boundary

This adapter performs representation canonicalization only: tuple reference construction, deterministic numeric spelling, nullable wrappers and exact field preservation. It does not create a PRAMANA `canonical_artefact_id` or `independence_key`.

Neither `hash` nor `item_link` has been proven safe as an immutable listing ID. Their verified conflicting associations prohibit promoting either into a globally canonical listing identifier. The normalized listing is therefore **record-scoped**, while separate source-reference tuples permit later comparisons.

Content hashing, near-duplicate detection, SimHash/pHash, quote inheritance, clone/payment-substitution detection and origin-aware canonical artefact assignment belong to the frozen downstream modules. They require their own input lineage and unresolved computation contracts. Images require actual, linked image bytes; a URL is not a perceptual hash input.

Exact source-label equality is not entity resolution. Distinct raw account labels—including whitespace/Unicode variants—remain distinct label keys. Later normalization/alias proposals may compare them without this adapter accepting a persona or merging identities.

## 11. Evidence-family eligibility

| Family | What the archive establishes | Adapter boundary / downstream condition |
|---|---|---|
| **F1 Cryptographic** | Description text contains PGP-marker-like material; inspected example at Abraxas 2015-04-20 row 4252 starts `BEGIN PGP PUBLIC KEY BLOCK Version GnuPG v2...` without standard armour delimiters. The full name/description scan found no exact `-----BEGIN PGP PUBLIC KEY BLOCK-----`, `-----BEGIN PGP MESSAGE-----` or `-----BEGIN PGP SIGNATURE-----` markers. | Not a verified parsable key/signature corpus. Do not reconstruct lost punctuation/base64 or infer fingerprint validity. Actual downstream parsing must establish validity; unsigned republication still earns no positive F1 weight. Ancillary keyserver link is not downloaded key material. |
| **F2 Financial** | Numeric price strings and lexical Bitcoin-address-shaped substrings occur; the archived Grams contact page also presents a donation-address string. No dedicated wallet/transaction/inputs/outputs columns. | Regex matches are not checksum validation and may occur inside damaged key material. No verified wallet corpus or actor-linked transaction data is claimed. Price alone creates no F2 evidence. |
| **F3 Infrastructure** | Listing/image reference strings, plus ancillary static HTML/assets. No CSV TLS, IP, response-header, clock-sample or descriptor fields. | A link is a location claim, not a probe result or origin correlation. This adapter emits no F3 infrastructure evidence. |
| **F4 Contact identifiers** | Contact-related words occur in prose; no dedicated contact column. A conventional email-pattern scan found no matching name/description strings; ancillary `contact` contains a Grams service email. | Words such as JABBER/EMAIL are not validated contact IDs. No blanket claim of contact absence beyond the tested pattern. Do not attribute service-page contacts to vendors. |
| **F5 Content artefacts** | Titles/descriptions and price-formatting input exist. Image references exist; some unrelated-in-time ancillary item image bytes are bundled. Exact title/description equality across markets was verified. | Text/template features are eligible inputs, subject to copying/rarity/origin checks. No positive reuse evidence, image match or clone inference is emitted here. |
| **F6 Linguistic style** | Text strings exist, but original unmodified author prose is not established. Description values inspected across the CSVs are ASCII/control-free and may include PGP-like damaged text or templates. | NER/language/style features are advisory. Frozen length/topic/translation/mediation gates apply downstream. No authorship truth or ungated F6 evidence. |
| **F7 Behavioural/temporal** | Repeated labelled snapshots, catalogue fields and unresolved `add_time`. | Supports observation history, not actor activity or migration events automatically. Event-driven scoring needs independently qualified event/time semantics. |
| **F8 Social/trust** | No forum relationship, review/feedback, vouching or transaction-edge columns. The FAQ discusses prospective review-based search features, not exported relationships. | Descriptive boasts or mentions are not verified reviews/trust edges. No F8 generator is supplied. |
| **F9 External corroboration** | No CSV official corroboration or ground-truth field. | The archive/report itself is not automatic F9 corroboration of every listing claim. No F9 generator is supplied. |

**Inspection limits:** lexical scans did not validate every possible crypto/contact format. They establish tested pattern presence/absence, not universal absence of hidden identifiers. No cryptographic validation, image-content analysis, attribution benchmark or field-completeness claim is made.

## 12. ML input boundary

| Permitted input | Permitted use | Boundary |
|---|---|---|
| Separate raw title and description strings | NER, language/script detection, text/template features | Preserve field offsets and source record; outputs are features/suggestions. |
| Account label and source/market context | Identifier-format analysis and source-context features | No cross-market/persona inference or automatic account merge. |
| Exact content tuples and source repetition references | Downstream duplicate/clone research inputs | Equality is not independence, clone status or identity. |
| Raw/parsed price with currency null | Formatting features | No economic/payment inference or cross-currency comparison. |
| Snapshot label and unresolved time object | Observation-history analysis | No actor event-time or continuous-rhythm scoring. |
| Shipping claim text | Source-claim/context features | No actual location inference. |
| Image reference | Reference-quality features only | No pHash, image embedding or EXIF without separately linked bytes. |
| Actual independently qualified image material | Later separately specified image path | Ancillary image/CSV joins are unresolved in v1. |

This adapter does not concatenate fields into invented original prose or assign language labels. Any downstream combination records its boundaries and transform version. ML outputs remain advisory until the frozen promotion rules pass. **No ML output may directly write to `evidence`, `pair_score`, `assessment` or `must_not_link`.** The adapter also creates no persona/actor, scored graph edge or accepted relationship.

## 13. Provenance contract

The trace is:

**archive digest → exact tar member occurrence → CSV bytes/schema → snapshot token → logical data-record number → original column position/name → decoded raw value**

### 13.1 Reproducible identifiers

Identifiers below are **ordered structured tuples**, serialized as JSON arrays when transported. Their component values and order define equality; no concatenated delimiter string, random UUID, process time, locale or implementation hash is permitted to define source identity.

Let `A` be the lowercase archive SHA-256, `O` the 1-based ordinal of the regular member in the tar stream, `P` its exact member name, `T` the exact snapshot directory token and `N` the 1-based logical data-record number after the header:

| Identifier | Exact components |
|---|---|
| `source_archive_id` | `["archive", A]` |
| `source_member_id` | `["member", A, O, P]` |
| `source_snapshot_id` | `["snapshot", A, T]` |
| `source_record_id` | `["record", A, O, P, N]` |
| `observed_account_id` | `["observed_account", "gwern-grams", market_name_raw, vendor_name_raw]`, only for present market/vendor strings |
| `listing_observation_id` | `["listing_observation", source_record_id]` |
| `image_reference_id` | `["image_reference", source_record_id, 8]`, only when present |
| `shipping_claim_id` | `["shipping_claim", source_record_id, 10]`, only when present |
| `timestamp_id` | `["source_time", source_record_id, 9]` |
| `field_ref` | `[source_record_id, column_position, exact_header_name]` |

All inspected members are regular files and member names are unique. Retaining ordinal makes the exact occurrence explicit; it is **not chronology**. A future archive version has another digest and must not silently reuse this verified archive identity. Observed-account keys deliberately represent exact labels in the source namespace, not archival record identity or a globally stable account/person.

### 13.2 Integrity and acquisition

Compute member SHA-256 over exact uncompressed member bytes if supplied; it is distinct from the raw field named `hash`. For example, `grams/2014-06-09/1776.csv` is 50,478 bytes and has SHA-256 `d290f9caae27b73388cab9ab1a282ad6c8405f705af7f810fc4515ddfd2a1b9d`.

Every normalized field is recoverable by replaying the pinned CSV grammar on the identified member. Physical start/end line numbers may be logged for diagnostics but never replace logical record number. Original CSV quoting and bytes are recoverable from the immutable member, not reconstructed from display text.

Acquisition URI, acquisition time and verification-document references are separate provenance supplied by the actual acquisition process. If absent, keep them null/unknown. OPUS context may be cited as reported context, not substituted as proof of the local download time, signature verification or original historical capture. The adapter adds its specification/transform version; processing time does not enter deterministic record IDs.

## 14. Independence considerations

- One repeated listing row across snapshots is multiple source observations, not multiple independent identity signals.
- Two vendors/markets using identical content might reflect copying, templates, reselling or other causes. This adapter establishes no causal direction or same operator.
- A key, contact or style feature extracted from a description inherits that record/content origin; a new feature ID does not create independence.
- Multiple CSV basenames, snapshot labels and archive imports do not establish independent sources.
- The adapter emits no `independence_key`, positive `k`, canonical evidence group or independence weight. Those belong to the frozen downstream contract, including its deferred cross-family/origin decisions.
- Missing/changed records cannot prove migration, inactivity, compromise or distinct operators.

These restrictions apply even when comparison tuples differ. Tuple inequality is not proof of independent origin.

## 15. Counter-evidence considerations

The adapter can expose **data-quality/source discrepancies**, not counterweights:

| Observation | Permitted interpretation | Forbidden automatic result |
|---|---|---|
| Same source token with changed vendor/content/link/time | Conflicting or changed source record values | Handover, framing, different actor or hard veto |
| Same content across markets | Exact source-content equality | Same author/operator or proven plagiarism direction |
| Missing description/image/shipping/vendor | Source field unavailable | Evasion, contradiction or negative LR |
| Different shipping claims | Different source assertions | Impossible travel or geolocation contradiction |
| Changed price/time | Changed source values with unresolved semantics | Payment cadence, currency-adjusted behaviour or actor update event |
| Malformed field | Parsing/validation issue | Fraud attribution, clone status or identity exclusion |
| Repeated image reference | Repeated reference string | Actual same image or independent image evidence |

Downstream review may investigate these observations using additional qualified inputs. Suppression is not automatically negative evidence; hard vetoes remain outside numeric scoring and outside this adapter.

## 16. Normalized record schema

This is a logical transport contract, not a requirement to introduce new database tables. Existing PRAMANA persistence can store these objects with explicit mapping. `null` below is a **normalized absence marker**, never a claim the CSV contained native null. All listed keys are present; only explicitly nullable values may be null. Strings are decoded Unicode strings. ID types are the tuples in section 13.

### 16.1 `source_record`

| Field | Type / required value |
|---|---|
| `id` | Required `source_record_id`. Unique occurrence, not unique listing. |
| `archive_id`, `member_id`, `snapshot_id` | Required corresponding IDs. |
| `row_number` | Required integer ≥1, header excluded. |
| `raw_values` | Required object with exactly the ten named headers, each mapped to its decoded source string. No guessed fields. |
| `trailing_empty_cell` | Required empty string. |
| `field_issues` | Required list, empty if none. Each issue: `field_position`, `code`; permitted value codes `invalid_decimal`, `invalid_integer`. Missing optional values use their nullable fields, not fabricated errors. |
| `adapter_version` | Required literal `GWERN_GRAMS_ADAPTER_SPEC_v1`. |

Structural failures are reported separately with available archive/member/record location and error category (`encoding_error`, `header_mismatch`, `csv_parse_error`, `row_width_mismatch`, `nonempty_trailing_cell`, `unsupported_member_layout`). They do not produce a falsely accepted record. A member failing structural validation is not published as fully normalized.

### 16.2 `source_snapshot`

| Field | Type / required value |
|---|---|
| `id`, `archive_id` | Required IDs. |
| `label_raw` | Required exact directory token. |
| `date_label` | Required valid first-ten-character calendar date for accepted labels. Not a timestamp. |
| `suffix_raw` | Required string; `""` for plain labels, `"-2"` for `2014-06-11-2`. |
| `meaning` | Required literal `source_snapshot_label`. |
| `timezone`, `capture_instant` | Required null. |

Unique per `(archive digest, exact label)`. One snapshot may contain multiple market CSV members; membership is established from the path, not from a claim of simultaneous capture.

### 16.3 `observed_account`

The enclosing record's `observed_account` is null when either market or vendor is not present. Otherwise:

| Field | Type / required value |
|---|---|
| `id` | Required exact observed-account tuple. |
| `source_namespace` | Required literal `gwern-grams`. |
| `market_name_raw`, `vendor_name_raw` | Required present exact strings from columns 2 and 4. |
| `source_record_id` | Required occurrence linkage; repeated keys retain separate record associations. |
| `market_field_ref`, `vendor_field_ref` | Required field provenance. |

No platform-issued vendor ID, persona ID, actor ID, ownership confidence or inferred alias exists in this object. The same label across snapshots does not prove uninterrupted control. The same label in different markets yields different keys.

### 16.4 `listing_observation`

| Field | Type / required value |
|---|---|
| `id`, `source_record_id`, `snapshot_id` | Required occurrence IDs. |
| `source_hash_raw` | Required raw string, including blank if present in a future admitted content fixture. |
| `source_hash_reference` | Nullable tuple `["source_hash_reference", "gwern-grams", market_name_raw, hash_raw]`; null if either is not present. Not canonical identity. |
| `source_url_reference` | Nullable tuple `["source_url_reference", "gwern-grams", market_name_raw, item_link_raw]`; null if either is not present. |
| `item_reference` | Nullable object: `raw`, `kind`, `field_ref`, using N-06. |
| `observed_account_id` | Nullable, exactly the associated observed-account ID. |
| `title`, `description` | Nullable unchanged source strings according to N-03; no text concatenation. |
| `price` | Required object: `raw`, `parse_status` (`parsed_decimal`, `missing`, `invalid_decimal`), nullable `amount_decimal`, `currency=null`, `field_ref`. |
| `canonical_listing_id`, `canonical_artefact_id` | Required null: downstream/unresolved, never filled from `hash` or URL. |

Unique by record occurrence. Source-hash/URL-reference tuples are not uniqueness constraints. Title/description values link to columns 6/7; normalized nulls still have their raw cells in `source_record`.

### 16.5 `image_reference`

Null if column 8 is not present. Otherwise required fields: `id`, `source_record_id`, `raw`, `kind` (N-06), `field_ref`; plus `image_bytes_ref=null` and `verified_archive_image_member=null`.

Uniqueness is record/field-scoped. An HTTP-looking directory or placeholder remains a reference. No image object, local file path, hash, EXIF or dimensions are inferred.

### 16.6 `timestamp`

Required fields: `id`, `source_record_id`, `field_ref`, `raw`; `parse_status` is `parsed_integer`, `missing` or `invalid_integer`; `parsed_integer` is nullable; `classification="UNKNOWN"`; `semantic_status="UNRESOLVED"`; `epoch=null`, `unit=null`, `timezone=null`, `instant=null`.

Uniqueness is record/column-9-scoped. Snapshot date and actual acquisition metadata are separate objects/context, not substitutes for `instant`.

### 16.7 `shipping_claim`

Null if column 10 is not present. Otherwise required fields: `id`, `source_record_id`, `raw`, `interpretation="unverified_source_claim"`, `field_ref`, `country_code=null`, `actual_location=null`.

Uniqueness is record/field-scoped. No `ship_to` is emitted because no such column was found.

### 16.8 `provenance`

Required fields: `archive_id`, `archive_sha256`, `member_id`, `member_name_raw`, `member_ordinal`, `member_sha256`, `snapshot_id`, `row_number`, `schema_header` (the exact 11 strings), `adapter_version`.

Nullable supplied metadata: `acquisition_uri`, `acquired_at`, `acquisition_report_ref`. Tar `mtime`, if included, is explicitly `archive_member_mtime`, not evidence event time. Original field/value recovery uses `field_ref` plus the pinned parser; raw values remain in `source_record`. No timestamp is populated from a guessed archive-download date.

Member digest is deterministic over original uncompressed bytes. This is an integrity measure for replay, not proof of authenticity or source truth.

### 16.9 `relations`

Required list of adapter-local associations. Each association contains `type`, `from_id`, `to_id`, `source_record_id` and `field_refs` (empty only for path/record containment):

| Allowed type | Meaning / emission condition |
|---|---|
| `record_in_snapshot` | Record → its path-derived snapshot. |
| `listing_observed_in_record` | Listing observation → source record. |
| `record_declares_vendor` | Record → nonnull observed-account key; supported by columns 2/4. |
| `record_has_image_reference` | Record → nonnull image reference; column 8. |
| `record_has_shipping_claim` | Record → nonnull shipping claim; column 10. |
| `record_has_time_value` | Record → timestamp object; column 9, including explicit missing/invalid representation. |

These are **data-lineage/source-declaration associations**, not writes to PRAMANA's scored relationship graph. No `same_operator`, `controls_address`, `posted`, trust edge, migration edge or accepted persona relation is emitted. Exact repetition comparisons, if performed downstream, are not appended as inferred identity relations.

## 17. Validation fixtures

Fixture row numbers are logical data-record numbers excluding the header. Archive examples are verified source locations. Mutation fixtures are explicitly synthetic changes to a valid row and are not claimed present in the archive. All preserve raw provenance and stage boundaries.

| ID | Input | Expected normalized result |
|---|---|---|
| G-01 Normal listing | `grams/2014-06-09/1776.csv`, row 1 | Market `1776`; vendor `ACAB23`; exact scoped observed account; amount `"50"`, currency null; shipping claim `Austria`; time integer 1399918210 with UNKNOWN/UNRESOLVED semantics; image reference only; no evidence/persona. |
| G-02 Missing description | `grams/2014-06-09/Agora.csv`, row 9747 | Raw description `""`; normalized description null; row retained; no negative finding. |
| G-03 Missing image | `grams/2014-06-09/ADM.csv`, row 465 | Raw image `""`; image_reference null; no image relation/feature. |
| G-04 Missing shipping | `grams/2014-06-09/ADM.csv`, row 11 | Raw shipping `""`; shipping_claim null; no guessed country. |
| G-05 Repeated listing across snapshots | Abraxas 2015-04-20 row 1 and 2015-04-21 row 1 | Distinct source-record/snapshot/listing-observation IDs; equal source-reference operands retained; no canonical listing ID or independent support. |
| G-06 Same vendor across snapshots | Same pair as G-05 | Same exact observed-account label key; two provenance associations; no proof of stable operator control. |
| G-07 Malformed price | Synthetic G-01 with price `"USD 50"` | Raw retained; invalid_decimal; amount null; currency still null; field issue at position 5; unrelated fields retained. |
| G-08 Malformed timestamp | Synthetic G-01 with add_time `"yesterday"` | invalid_integer; parsed_integer/instant null; UNKNOWN/UNRESOLVED; no invented relative date. |
| G-09 Duplicate source row | Synthetic member containing G-01 twice at rows 1 and 2 | Different source-record/listing occurrence IDs; equal values/account key; no dedup deletion or independence claim. No such within-member full-row duplicate was observed in this release. |
| G-10 Empty fields / null-like words | Synthetic blank vendor plus description `"none"`, name `"nan"`, ship_from `"n/a"` | No account; literal words retained; shipping remains unverified claim string; no native-null coercion. |
| G-11 Unicode vendor | `grams/2015-04-04/Alpha.csv`, row 1896 | Exact vendor `Omega²`; distinct from synthetic `Omega2`; no Unicode folding. |
| G-12 Whitespace vendor | `grams/2014-06-09/Agora.csv`, row 1 | Raw newline/spaces retained; observed_account null; do not create a shared blank account. |
| G-13 Whitespace shipping | `grams/2014-08-25/ADM.csv`, row 1237 | Raw `" "` preserved; shipping_claim null. |
| G-14 Identical content across markets | 1776 2014-06-09 row 10 and Abraxas 2015-04-20 row 94 | Equal title/description operands, distinct market/account/record contexts; no clone, authorship or same-operator inference. |
| G-15 Conflicting repeated source token | ADM 2014-06-15 row 665 and 2014-08-25 row 1453 | Both vendor strings retained with separate observed-account keys; same source-hash reference; no overwrite, handover or identity merge. |
| G-16 Changed add_time | Abraxas 2015-04-20 row 4 and 2015-06-02 row 11 | Preserve both raw integers; semantic class remains unknown, not listing creation/update. |
| G-17 Same-day suffix | `grams/2014-06-11-2/Agora.csv`, row 1 | Label preserved; date_label `2014-06-11`, suffix `-2`; snapshot distinct from plain date; no capture ordering. |
| G-18 Opaque image token | `grams/2014-08-29/Alpaca.csv`, row 2 | `image_reference.raw="18-344"`, kind opaque_reference; no invented `18-344.jpg` path. |
| G-19 Directory-like image reference | Abraxas 2015-04-20 row 1 | HTTP reference candidate ending `/uploads/`; bytes/member null; no image-exists assertion. |
| G-20 Damaged PGP-like prose | Abraxas 2015-04-20 row 4252 | Source text preserved; no key repair, verified fingerprint or positive F1 evidence. |
| G-21 Trailing column | Valid header/row versus synthetic nonempty position 11 | Empty accepted/preserved; nonempty structural violation, no guessed extra field. |
| G-22 Multiline quoted cells | Source vendor/ship strings with embedded newlines; synthetic escaped-quote variant | CSV logical record boundaries preserved; row ID independent of physical line count. |
| G-23 URL collision | SilkRoad 2014-06-09 rows 12209 and 12223 | Same URL reference does not collapse different source hashes/occurrences. |
| G-24 Hash is not a digest | `grams/2014-06-09/ADM.csv`, row 1 | Opaque `8-TEaDzSDOO3ucVc8KMaoPtAsJ7XVL3MVWq5A0YeOM`; no MD5/PGP interpretation. |
| G-25 Source market spacing | `grams/2015-06-09/Oxygen .csv`, row 1; synthetic identical label without trailing space | Preserve exact `Oxygen ` in keys; display trim, if used, never changes identity. |
| G-26 Integrity/schema failure | Mutated archive/member bytes, extra header, truncated row or invalid UTF-8 | Reject affected verification/member publication with explicit issue; no silent recovery or field shifting. |

A concrete G-01 source-record ID is `["record", "0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6", 1, "grams/2014-06-09/1776.csv", 1]`. Its account key is `["observed_account", "gwern-grams", "1776", "ACAB23"]`. These are deterministic representation choices, not claims of a source-issued vendor ID.

## 18. Forbidden interpretations

- `hash` is not assumed cryptographic, a fingerprint, an immutable listing ID or an account ID.
- `vendor_name` is not a threat actor/person/persona; market membership is not attribution evidence.
- Repeated snapshots/rows/URLs/content are not automatically independent observations of identity.
- `add_time` is not silently actor event, capture, creation or update time; directory dates are not UTC instants.
- Price is not assigned BTC/USD or converted using an archived UI currency selector. A CSV record is not a sale or transaction.
- Image reference is not image bytes; opaque tokens are not fabricated filenames. No live link fetching is part of the adapter.
- Description markers/word mentions are not validated PGP keys, wallets, contacts, reviews or trust relationships.
- Identical text does not prove copying direction, same author, clone status or operator identity.
- Shipping text is not actual geographic location or shipping destination.
- No scores, LR values, rarity/decay formulas, calibrated confidence, hard vetoes, clustering, persona acceptance or identity decisions are emitted.
- No write to authoritative evidence/pair_score/assessment/must_not_link from adapter or advisory ML output.
- No benchmark performance, dataset completeness, legal admissibility or live-market accuracy is claimed.

## 19. UNRESOLVED / REQUIRES LATER DECISION

| Item | What is missing | Required later artifact / current safe behaviour |
|---|---|---|
| `add_time` meaning | Source definition of event represented, epoch, units and timezone; archived FAQ does not define the field. | Grams export/source-code/data-dictionary evidence tied to this release. Keep UNKNOWN/UNRESOLVED with integer parse only. |
| Price currency and changes | No currency field or verified export-denomination contract. Archived UI supports multiple currencies but does not define CSV price. | Release-specific export documentation. Keep currency null; no price comparability/behaviour inference. |
| Source `hash` stability | Generation algorithm, uniqueness scope and reuse guarantees absent; contradictory associations observed. | Source implementation/documentation plus conflict review. Keep opaque repetition reference; canonical listing ID null. |
| Stable vendor identity / raw formatting | No platform-issued vendor ID; label/control/newline variants can differ. | Separate reviewed source-account/alias policy if needed. Exact label keys remain conservative observations. |
| Original text fidelity | Exact preprocessing/truncation and original author text not established. | Source extraction history/original pages and domain validation. No restoration or ungated stylometry. |
| PGP/wallet/contact recovery | Marker/candidate presence does not establish valid material; lexical scans are not exhaustive validators. | Authorised deterministic validators and original-source evidence where needed. No heuristic repair presented as observed bytes. |
| Image-byte association | Limited 2014-05-28 images exist, but no verified complete join to later CSV image references. | Separate image/HTML adapter contract with explicit source joins and fixtures. V1 emits references only. |
| Snapshot-label capture meaning | Dates/suffixes do not define exact collection instants, completeness or update cadence. | Release-specific capture/export metadata. Preserve labels; no synthetic chronology. |
| Cross-record origin/canonicalisation | Equal strings do not settle common origin, direction of copying or evidence independence. | Frozen downstream canonicalisation and deferred computation contracts. Emit operands/lineage, no grouping. |
| Acquisition/licensing qualification | OPUS supplies reported context, not a verified local acquisition record or complete per-component permission proof. | Cyber/DE release qualification and acquisition manifest. Do not invent download times, signature verification or usage rights. |
| Operational retention and downstream scoring | Remain deferred in CYBER_SPEC_v1. | Existing owners resolve them; this adapter does not amend them. |

These uncertainties do not prevent deterministic source normalization because the output explicitly preserves unknowns. They do prevent downstream claims requiring the missing meaning or validation.

## 20. Change/version notes

**Version:** GWERN_GRAMS_ADAPTER_SPEC_v1. Applies to the archive digest in section 2. Frozen normalization choices are explicitly distinguished from verified raw fields; no new raw source fields are claimed.

**Owner:** Cyber owns domain meaning and verification scope; DE owns lawful acquisition; ML implements deterministic parsing/feature handoff within this contract; PL maps normalized objects/provenance to existing storage; EV validates fixtures and downstream method claims.

**Final cross-check:** All ten named fields and the trailing unnamed cell were checked across all 1,865 CSV headers and 12,384,326 records. Inventory paths/counts, snapshot suffix, example rows, raw market labels and changing source references were checked against the archive. Ancillary FAQ/contact/results statements were read from bundled members, not inferred from OPUS. Crypto validity, add_time semantics, price currency, stable listing/vendor identity, image-to-CSV joins and complete source rights remain explicitly unverified/unresolved.

The frozen `PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md` is unchanged. This release supplies the previously missing Grams-specific structure/normalization evidence; it does not rewrite F1–F9, resolve general scoring contracts or imply that all Gwern subarchives share this schema.

Changes to accepted schema, identifier construction, missingness, text normalization, time meaning or image joins require a new adapter-contract version and updated fixtures. Reinspection of another digest is required before transferring this archive's verification claims.
