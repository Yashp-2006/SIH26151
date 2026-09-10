# PRAMANA — Gwern DNM Archive Independent Verification Report

**Date**: 2026-09-08  
**Verification Method**: Primary source inspection (Gwern.net, Internet Archive metadata API, HTTP HEAD requests)

---

## 1. Gemini's Previous Claim — DEBUNKED

| Claim | Status |
|---|---|
| URL: `https://archive.org/download/darknetmarketarchives/evolution.tar.xz` | **❌ INVALID** |
| IA identifier: `darknetmarketarchives` | **❌ DOES NOT EXIST** |
| File size: ~5.1 GB | **❌ WRONG** |

**Evidence**:
- `https://archive.org/metadata/darknetmarketarchives` returns empty JSON `{}` — item does not exist
- `https://archive.org/details/darknetmarketarchives` returns HTTP 404
- `https://archive.org/download/darknetmarketarchives/evolution.tar.xz` returns **HTTP 503 Service Unavailable** (item not found)
- The identifier, URL, and file size were all fabricated

---

## 2. Verified Source

| Field | Value |
|---|---|
| **Dataset** | Dark Net Market archives, 2011–2015 |
| **Creator** | Gwern Branwen et al. |
| **IA Identifier** | `dnmarchives` |
| **IA Item Page** | https://archive.org/details/dnmarchives |
| **IA Download Index** | https://archive.org/download/dnmarchives |
| **Documentation** | https://www.gwern.net/DNM-archives |
| **License** | CC0 (Gwern's portion); CC-BY-NC (Christin SR1 subset) |
| **Upload Date** | 2015-07-12 |
| **Total Archive Size** | ~49.4 GB compressed (~1.6 TB uncompressed) |
| **Total Files** | 183 files |
| **Markets Covered** | 89 DNMs + 37+ forums |

---

## 3. Evolution Market — Verified Downloadable Files

### 3a. `evolution.tar.xz` (Market Scrapes)

| Field | Value |
|---|---|
| **Filename** | `evolution.tar.xz` |
| **Exact URL** | `https://archive.org/download/dnmarchives/evolution.tar.xz` |
| **File Size** | **3,630,091,004 bytes** (~3.38 GB) |
| **Format** | xz-compressed tarball |
| **MD5** | `5be1b5d833618be9a22916a74ac77892` |
| **SHA-1** | `a1f9a5b628d381895432e231bb150eaa1e005c1e` |
| **CRC32** | `5c5e9f22` |
| **SHA-256** | `a6a0ccd588635903f1e914390f36bb9a56f562d37b9e92d6e58dac6364b35b8a` |
| **mtime** | 1436870138 (2015-07-14T10:35:38 UTC) |
| **HTTP HEAD** | ✅ **302 Found** → `https://dn710702.ca.archive.org/0/items/dnmarchives/evolution.tar.xz` |

### 3b. `evolution-forums.tar.xz` (Forum Scrapes)

| Field | Value |
|---|---|
| **Filename** | `evolution-forums.tar.xz` |
| **Exact URL** | `https://archive.org/download/dnmarchives/evolution-forums.tar.xz` |
| **File Size** | **1,178,191,380 bytes** (~1.10 GB) |
| **MD5** | `0da5fa640eb6519e06f7b1be28ac8975` |
| **SHA-1** | `80eba37a6c48767052e04ad250e6ec2b39fa425d` |
| **CRC32** | `7167f33e` |
| **SHA-256** | `109eb980c11ed37b29321f6403cb5e95614f3c44525a549164d95d0a52eb94cf` |
| **mtime** | 1436806885 (2015-07-13T17:01:25 UTC) |
| **HTTP HEAD** | ✅ **302 Found** → `https://dn710702.ca.archive.org/0/items/dnmarchives/evolution-forums.tar.xz` |

### 3c. `evolution-forums-2014093020141016-rasmusandersen.tar.xz` (Earlier Forum Crawl)

| Field | Value |
|---|---|
| **Filename** | `evolution-forums-2014093020141016-rasmusandersen.tar.xz` |
| **Exact URL** | `https://archive.org/download/dnmarchives/evolution-forums-2014093020141016-rasmusandersen.tar.xz` |
| **File Size** | **25,173,436 bytes** (~24.0 MB) |
| **MD5** | `15f699a63f40adbed623c692aa9222b8` |
| **SHA-1** | `1255e2945f214eb915e564a9019e9380d512adac` |
| **CRC32** | `713002d5` |
| **SHA-256** | `23449de611a42899bcb27db8186d194f7b805ee7e55034ec5ab17adee226aecd` |

---

## 4. Agora Market — Verified Downloadable Files

### 4a. `agora.tar.xz` (Market Scrapes)

| Field | Value |
|---|---|
| **Filename** | `agora.tar.xz` |
| **Exact URL** | `https://archive.org/download/dnmarchives/agora.tar.xz` |
| **File Size** | **5,873,623,344 bytes** (~5.47 GB) |
| **MD5** | `4224bcaf1b021789f4136a523dc6a9ff` |
| **SHA-1** | `b573276ee98d5c49f48e2e77f065d2c74dca1d8c` |
| **CRC32** | `0ea27353` |
| **SHA-256** | `4e7d5d4f63be66956037d4c27f3b97c0b980addd3ed5029b24904ab69f705c9d` |
| **HTTP HEAD** | ✅ **302 Found** → `https://dn710702.ca.archive.org/0/items/dnmarchives/agora.tar.xz` |

### 4b. `agora-forums.tar.xz` (Forum Scrapes)

| Field | Value |
|---|---|
| **Filename** | `agora-forums.tar.xz` |
| **Exact URL** | `https://archive.org/download/dnmarchives/agora-forums.tar.xz` |
| **File Size** | **869,224,556 bytes** (~829.0 MB) |

---

## 5. Smallest Practical Archives for PRAMANA MVP

> [!IMPORTANT]
> The Grams CSV dataset is by far the most practical for MVP: pre-parsed, structured, small, and covers Evolution + Agora listings.

| Option | File | Size | Contents | Ease of Use |
|---|---|---|---|---|
| **1. Grams CSV (Recommended)** | `grams.tar.xz` | **66.5 MB** | Daily CSV exports of marketplace listings from 18+ markets including Evolution & Agora (2014-06 to 2015-07). Structured: vendor, price, description, ship_from. | ⭐⭐⭐⭐⭐ |
| **2. Grams CSV v2** | `grams-20150714-20160417.tar.xz` | **64.6 MB** | Second wave CSV exports covering Agora, AlphaBay, etc. (2015-07 to 2016-04). | ⭐⭐⭐⭐⭐ |
| **3. Kaggle Agora CSV** | [Kaggle dataset](https://www.kaggle.com/datasets/philipjames11/dark-net-marketplace-drug-data-agora-20142015) | ~10 MB CSV | ~109k parsed Agora listings. Gwern mirror: `2017-12-05-philipjames11-darknetmarketplacedataagora20142015.csv.xz` | ⭐⭐⭐⭐⭐ |
| **4. Evolution Forums (Rasmus)** | `evolution-forums-2014093020141016-rasmusandersen.tar.xz` | **24 MB** | Earlier Evolution forum crawl subset | ⭐⭐⭐ |
| **5. Evolution Forums (Full)** | `evolution-forums.tar.xz` | **1.10 GB** | Complete Evolution forum scrapes (HTML) | ⭐⭐⭐ |
| **6. Evolution Market (Full)** | `evolution.tar.xz` | **3.38 GB** | Complete Evolution market scrapes (HTML + images) | ⭐⭐ |
| **7. Agora Market (Full)** | `agora.tar.xz` | **5.47 GB** | Complete Agora market scrapes (HTML + images) | ⭐⭐ |

---

## 6. PRAMANA MVP Recommendation

For an MVP, acquire in this priority order:

1. **`grams.tar.xz`** (66.5 MB) — Structured CSV, covers Evolution + Agora, immediately parseable
2. **Kaggle Agora CSV** (~10 MB) — Cleanest structured data, single market
3. **`evolution-forums.tar.xz`** (1.10 GB) — If raw HTML forum data is needed
4. **`evolution.tar.xz`** (3.38 GB) — Only if full market pages + images are needed

> [!TIP]
> The Grams archive contains CSVs like `EVO.csv`, `EVO2.csv`, `Agora.csv` per day. These are API-sourced exports that Gwern describes as "close to 100% complete & accurate" — far more reliable than the wget crawl scrapes.

---

## 7. Data Integrity Verification

The archive includes:
- **PAR2 error-correction files** (`ecc.par2` + volume sets) for up to 10% damage repair
- **PGP-signed SHA-256 hashes** (in the Gwern page, signed block includes all files)
- **Per-file MD5, SHA-1, CRC32** in the IA metadata API

Post-download verification command:
```bash
# SHA-256 verification (from Gwern's signed hash list)
sha256sum -c <<< "a6a0ccd588635903f1e914390f36bb9a56f562d37b9e92d6e58dac6364b35b8a  evolution.tar.xz"

# PAR2 verification
par2verify ecc.par2
```

---

## 8. Confidence Assessment

| Claim | Confidence | Basis |
|---|---|---|
| IA identifier is `dnmarchives` | **Verified Fact** | Gwern page, IA metadata API, IA details page |
| `evolution.tar.xz` exists and is downloadable | **Verified Fact** | HTTP HEAD returns 302 with redirect to storage server |
| File size is 3,630,091,004 bytes | **Verified Fact** | IA metadata API JSON response |
| SHA-256 hash is `a6a0cc...35b8a` | **Verified Fact** | Gwern's PGP-signed hash block + IA metadata cross-reference |
| Gemini's previous URL was fabricated | **Verified Fact** | HTTP 503, empty metadata, 404 on details page |
| Grams CSV is best for MVP | **High confidence inference** | Based on Gwern's documentation describing CSV structure and API-sourced completeness |
| Internal archive structure is `YYYY-MM-DD` dated wget crawls | **Verified Fact** | Gwern documentation explicitly states this |

### Unresolved Issues

1. **Internal file structure of `evolution.tar.xz`**: Cannot verify without downloading and extracting. Gwern states contents are `YYYY-MM-DD` dated wget crawls with HTML/CSS/images, but exact subdirectory layout is unknown until extracted. **Do not assume paths like `evolution/vendors/`** — these were fabricated.
2. **Decompressed size**: Not stated for Evolution specifically. The full 49.4 GB archive decompresses to ~1.6 TB total. The largest single archive decompresses to <250 GB (per Gwern).
3. **Download speed**: IA may throttle large downloads. Torrent download (`dnmarchives_archive.torrent`) is recommended by Gwern for reliability and bandwidth.
4. **Kaggle mirror availability**: The Gwern-hosted mirror CSV is accessible at `https://www.gwern.net/doc/darknet-market/agora/2017-12-05-philipjames11-darknetmarketplacedataagora20142015.csv.xz` — not independently verified via HEAD request in this session.
