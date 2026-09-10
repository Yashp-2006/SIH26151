# cybersec/ — PRAMANA Cyber Intelligence Slice

Offline deterministic cyber review slice. Source-backed, contestable, human-reviewed pseudonymous investigation.

**Verified environment:** Python 3.13.7, pytest 9.0.2. Standard library only — no DB, model, Tor, or GPU needed.

## Quick start

Run from `cybersec/pramana/` (the repo root for this slice):

```powershell
cd cybersec/pramana
python -m pytest -q
python run_cyber_demo.py
```

Expected: **76 passed, 13 skipped**. Demo output: 18 records, 53 derivations, 13 hub accounts, null assessment.

Open `docs/cyber/demo/review.html` locally to inspect the review packet.

## Folder map

| Path | Purpose |
|---|---|
| `pramana/adapters/gwern_grams/` | Pinned archive reader, CSV parser, normalization, provenance |
| `pramana/canonicalization/` | Exact repetition and near-match comparison operands |
| `pramana/cyber/` | Deterministic indicators, restrictions, review packet, static HTML |
| `pramana/tests/` + `pramana/canonicalization/tests/` | Offline tests (76 pass, 13 archive-opt-in skipped) |
| `pramana/docs/cyber/demo/` | Generated synthetic tar, review JSON and HTML |
| `pramana/docs/cyber/validation/` | JUnit and bounded real-source validation evidence |

## Authority documents

| Document | Purpose |
|---|---|
| [`TEAM_README.md`](TEAM_README.md) | Team start-here + folder map |
| [`PRAMANA_FINAL_PROJECT_HANDOFF_v1.md`](PRAMANA_FINAL_PROJECT_HANDOFF_v1.md) | Authoritative team consolidation, status, boundaries |
| [`PRAMANA_REPRODUCTION_GUIDE_v1.md`](PRAMANA_REPRODUCTION_GUIDE_v1.md) | Step-by-step reproduction with exact expected outputs |
| `pramana/PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md` | Frozen cyber policy |
| `pramana/docs/cyber/PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md` | Frozen Grams adapter/data contract |

## What is implemented

- Archive digest/member reading and CSV normalization
- Exact repetition and source discrepancies (canonicalization)
- Text spans / PGP-like markers / legacy Bitcoin format validation
- Hub restriction (>12 accounts, declared snapshot)
- Clone restriction (externally declared scope)
- Counter-evidence check states (7 states, narrow restrictions)
- Offline review packet (JSON) + static HTML viewer

## What is deferred / not yet implemented

Evidence promotion (DC-06), persistence/ledger/API, F6–F9 generators, RANGE-SIM/TOR, scoring, calibration, hard veto.

See §14 of the handoff for full P0/P1/P2 priority table and ownership.
