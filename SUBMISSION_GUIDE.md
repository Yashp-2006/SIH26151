# SIH 2026 Submission Guide — SIH26151 (PRAMANA)

Use this checklist before sharing your GitHub repository link for evaluation.

## Required Repository Content

- [x] Actual source code is present in `ai-ml/`, `cybersec/`, `backend/`, and `frontend/`.
- [x] `README.md` explains the project clearly across all 13 required sections.
- [x] PS ID (`SIH26151`) and PS Title are prominently included.
- [x] Problem statement and proposed solution are thoroughly explained.
- [x] Key features and capabilities are documented in tabular format.
- [x] Complete technology stack is listed across all tiers.
- [x] Setup, installation, and run instructions are tested and verified.
- [x] Team information and role allocation are detailed.
- [x] High-level architecture and subsystem data flow are documented in `docs/architecture.md`.
- [x] Screenshots and prototype assets are maintained in `assets/screenshots/`.
- [x] Final presentation placeholder is established in `submission/PRESENTATION.md`.
- [x] Demo video link is configured in `submission/DEMO.md`.
- [x] Repository and all external links remain public and accessible without credentials.

## Recommended Structure

```text
SIH26151/
├── README.md                  # Sections 1-13, exactly as defined — never remove a section
├── SUBMISSION_GUIDE.md        # Pre-submission verification checklist
├── FOLDER_STRUCTURE.md        # Comprehensive, fully-expanded tree of all files and folders
├── requirements.txt           # Unified top-level Python dependencies
├── .gitignore                 # Secrets, cache, and build artifact exclusions
├── LICENSE                    # Open-source MIT License
├── submission/
│   ├── PRESENTATION.md        # Final PPT or accessible viewer link
│   └── DEMO.md                # Demo video link (YouTube/Google Drive)
├── docs/
│   └── architecture.md        # System architecture and end-to-end data flow
├── assets/
│   └── screenshots/
│       └── README.md          # Screenshot inventory, examples, and naming conventions
├── ai-ml/                     # List-A deterministic extractors + List-B ML models & Fusion Engine
├── cybersec/                  # PRAMANA offline cyber review, adapters, canonicalization, policy
├── backend/                   # FastAPI REST service, PostgreSQL ledger, auth (Planned)
└── frontend/                  # React/TypeScript investigation dashboard (Planned)
```

## Presentation

Upload the final PPT/PPTX to the `submission/` folder when file size permits. Use a clear filename such as:

`SIH26151_PRAMANA_Presentation.pptx`

If the PPT file is too large for GitHub, host it on Google Drive or OneDrive with public viewer permissions and place the link in `submission/PRESENTATION.md`.

## Demo Video

The demo video is strongly recommended. Add the YouTube or Google Drive video link to `submission/DEMO.md` and verify that external reviewers can play it without authentication or permission requests.

## Screenshots / Prototype Photos

Put screenshots, dashboard mockups, and validation outputs in `assets/screenshots/`. Include key workflow views:
- Investigation summary dashboard
- Evidence Balance Sheet and family discount traces
- Co-spend wallet cluster visualization
- Temporal activity overlap timelines
- Offline HTML review packet (`docs/cyber/demo/review.html`)

## Do Not Upload

- Passwords or private encryption keys
- API keys, JWT secrets, or auth tokens
- `.env` files containing real production credentials
- Personal credentials or unredacted raw PII

## README Verification Checklist

1. What problem does PRAMANA solve? (Cross-persona attribution in adversarial darknet ecosystems)
2. What is the proposed solution? (Grounded evidence extraction + independence-aware Bayesian likelihood fusion)
3. How does it work? (Deterministic indicators -> ML feature candidates -> Independence discounting -> Balance sheet review)
4. Which technologies are used? (Python 3.11/3.13, FastAPI, PyTest, Hugging Face, Cloudflare Workers, TypeScript)
5. How can a reviewer run it? (Direct offline pytest commands, demo scripts, local uvicorn server)
6. What does the final output look like? (Reproducible JSON review packet + tabular evidence balance sheets)
7. What are the key features and impact? (87.6% precision on synthetic benchmarks, 20/20 decoys refused, human-in-the-loop auditability)

## Before Submission

Open the repository in a private/incognito browser window while signed out. Confirm that code, documentation, architecture diagrams, and all linked resources are accessible to reviewers without restriction.
