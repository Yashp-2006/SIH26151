# Repository Folder Structure — SIH26151 (PRAMANA)

This document provides the fully-expanded, complete directory tree of the repository, followed by a structured grouping of the cybersecurity and intelligence modules.

---

## 1. Complete Expanded Directory Tree

```text
SIH26151/
├── .gitignore
├── FOLDER_STRUCTURE.md
├── LICENSE
├── README.md
├── SUBMISSION_GUIDE.md
├── requirements.txt
├── assets/
│   └── screenshots/
│       └── README.md
├── docs/
│   └── architecture.md
├── submission/
│   ├── DEMO.md
│   └── PRESENTATION.md
├── ai-ml/
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   ├── conftest.py
│   ├── requirements.txt
│   ├── cloudflare-workers/
│   │   ├── deploy.ps1
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── wrangler.jsonc
│   │   ├── dist/
│   │   │   ├── README.md
│   │   │   ├── index.js
│   │   │   └── index.js.map
│   │   └── src/
│   │       └── index.ts
│   ├── data/
│   │   ├── bitcoinheist_sample.csv
│   │   ├── darknet_archives_sample/
│   │   │   └── sample1.txt
│   │   └── stylometry_sample/
│   │       ├── stylo1.txt
│   │       ├── stylo2.txt
│   │       └── stylo3.txt
│   ├── group_a_deterministic/
│   │   ├── __init__.py
│   │   ├── canonicalise.py
│   │   ├── extractors.py
│   │   ├── pgp_meta.py
│   │   ├── rarity.py
│   │   └── test_group_a.py
│   ├── group_b_nlp/
│   │   ├── __init__.py
│   │   ├── lang_ner.py
│   │   ├── style_shift.py
│   │   ├── stylometry.py
│   │   ├── template_fp.py
│   │   └── test_group_b.py
│   ├── group_c_wallet_infra/
│   │   ├── infra_fp.py
│   │   ├── temporal.py
│   │   ├── test_group_c.py
│   │   └── wallet_cluster.py
│   ├── group_d_embeddings/
│   │   ├── __init__.py
│   │   ├── image_embeddings.py
│   │   ├── similarity_index.py
│   │   ├── test_group_d.py
│   │   └── text_embeddings.py
│   ├── group_e_classification/
│   │   ├── __init__.py
│   │   ├── category_tagger.py
│   │   ├── evasion_detector.py
│   │   ├── risk_classifier.py
│   │   └── test_group_e.py
│   ├── group_f_graph/
│   │   ├── __init__.py
│   │   ├── co_occurrence.py
│   │   ├── path_features.py
│   │   ├── subgraph_extractor.py
│   │   └── test_group_f.py
│   ├── group_g_llm_assist/
│   │   ├── __init__.py
│   │   ├── citation_validator.py
│   │   ├── hypothesis_generator.py
│   │   ├── prompt_builder.py
│   │   └── test_group_g.py
│   ├── hf-space/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── pramana/
│   │   ├── __init__.py
│   │   ├── accounts.json
│   │   ├── answer_key.csv
│   │   ├── api.py
│   │   ├── demo.py
│   │   ├── evaluate.py
│   │   ├── pairs.csv
│   │   ├── range_sim.py
│   │   ├── rarity.py
│   │   ├── schema.py
│   │   ├── score_naive.py
│   │   ├── score_pramana.py
│   │   ├── sensitivity.py
│   │   └── stub_features_a.py
│   ├── shared/
│   │   ├── contracts.py
│   │   └── data_loader.py
│   └── tests/
│       └── test_fusion.py
├── backend/
│   ├── README.md
│   └── requirements.txt
├── frontend/
│   ├── .gitkeep
│   └── README.md
└── cybersec/
    ├── PRAMANA_FINAL_PROJECT_HANDOFF_v1.md
    ├── PRAMANA_REPRODUCTION_GUIDE_v1.md
    ├── README.md
    ├── TEAM_README.md
    └── pramana/
        ├── .gitignore
        ├── CANONICALIZATION_REPORT.md
        ├── FINAL_REPORT.md
        ├── OPUS_GWERN_VERIFICATION_REPORT.md
        ├── PRAMANA Dataset Intelligence Report.txt
        ├── PRAMANA_AI_ML_Module_Dataset_Plan_v2.pdf
        ├── PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md
        ├── PRAMANA_FINAL_PROJECT_HANDOFF_v1.md
        ├── PRAMANA_Master_Blueprint.md
        ├── PRAMANA_SIH_PS_26151.txt
        ├── PRAMANA_Technical_Project_Dossier.pdf
        ├── TEAM_README.md
        ├── demo_records.json
        ├── ingestion_output.txt
        ├── ingestion_report.json
        ├── pytest.ini
        ├── run_canonicalization.py
        ├── run_cyber_demo.py
        ├── run_cyber_validation.py
        ├── run_ingestion.py
        ├── adapters/
        │   ├── __init__.py
        │   └── gwern_grams/
        │       ├── __init__.py
        │       ├── archive_reader.py
        │       ├── csv_parser.py
        │       ├── errors.py
        │       ├── identifiers.py
        │       ├── models.py
        │       ├── normalizer.py
        │       └── runner.py
        ├── canonicalization/
        │   ├── __init__.py
        │   ├── models.py
        │   ├── runner.py
        │   ├── text_hashing.py
        │   └── tests/
        │       ├── __init__.py
        │       └── test_canonicalization.py
        ├── cyber/
        │   ├── __init__.py
        │   ├── demo.py
        │   ├── indicators.py
        │   ├── policy.py
        │   ├── render.py
        │   └── review.py
        ├── docs/
        │   ├── PRAMANA_REPRODUCTION_GUIDE_v1.md
        │   └── cyber/
        │       ├── PRAMANA_CYBER_DEMO_SCENARIO_v1.md
        │       ├── PRAMANA_CYBER_READINESS_REPORT_v1.md
        │       ├── PRAMANA_CYBER_WORKSTREAM_STATUS_v1.md
        │       ├── PRAMANA_GWERN_GRAMS_ADAPTER_SPEC_v1.md
        │       ├── demo/
        │       │   ├── review.html
        │       │   ├── review_packet.json
        │       │   └── synthetic_source.tar
        │       └── validation/
        │           ├── pytest.xml
        │           └── representative_validation.json
        ├── hatch-runs/
        │   └── starjotaro-v2/
        │       ├── decoded/
        │       │   ├── base-atlas-clean.png
        │       │   ├── look-anchors-approved.png
        │       │   ├── look-cardinals.png
        │       │   ├── look-row-10.png
        │       │   ├── look-row-9.png
        │       │   ├── neutral-cell.png
        │       │   └── look-anchors/
        │       │       ├── 000.png
        │       │       ├── 090.png
        │       │       ├── 180.png
        │       │       └── 270.png
        │       ├── final/
        │       │   ├── assembly-manifest.json
        │       │   ├── despill-extended.json
        │       │   ├── pet.json
        │       │   ├── spritesheet-clean.png
        │       │   ├── spritesheet-clean.webp
        │       │   ├── spritesheet.png
        │       │   ├── spritesheet.webp
        │       │   ├── validation-extended-clean.json
        │       │   ├── validation-extended.json
        │       │   └── validation-installed.json
        │       ├── qa/
        │       │   ├── contact-sheet-base.png
        │       │   ├── contact-sheet-extended-clean.png
        │       │   ├── contact-sheet-extended.png
        │       │   ├── despill-base.json
        │       │   ├── look-cardinals-extract.json
        │       │   ├── look-directions.png
        │       │   ├── validation-base-clean.json
        │       │   └── validation-base.json
        │       └── source/
        │           ├── base-atlas.webp
        │           └── pet.json
        └── tests/
            ├── __init__.py
            ├── conftest.py
            ├── test_adapter_regressions.py
            ├── test_cyber_slice.py
            └── test_fixtures.py
```

---

## 2. Structured Grouping of Cybersecurity Modules (`cybersec/`)

The `cybersec/` subsystem represents the offline, deterministic cyber intelligence, ingestion, and evidence-review slice of PRAMANA. To prevent chaotic file sprawl, its modules are grouped into six distinct functional subsystems:

| Group / Subsystem | Location | Key Components | Functional Scope |
|---|---|---|---|
| **CS-01: Ingestion & Archive Adapters** | `cybersec/pramana/adapters/gwern_grams/` | `archive_reader.py`, `csv_parser.py`, `normalizer.py`, `identifiers.py`, `models.py`, `runner.py`, `errors.py` | Reads immutable archive tarballs (`grams.tar.xz`), validates cryptographic SHA-256 digests, standardizes raw vendor listings into unified schema records, and assigns provenance tracking IDs. |
| **CS-02: Canonicalization & Text Hashing** | `cybersec/pramana/canonicalization/` | `runner.py`, `models.py`, `text_hashing.py`, `tests/test_canonicalization.py` | Performs deterministic normalization and cryptographically hashes body text to distinguish verbatim cross-marketplace reposts from independent authored text. |
| **CS-03: Cyber Indicators, Policy & Review** | `cybersec/pramana/cyber/` | `indicators.py`, `policy.py`, `review.py`, `render.py`, `demo.py` | Lexical validation of Base58Check Bitcoin addresses and PGP markers; enforcement of hard policy suppression (e.g. `hub_restriction` for >12 accounts sharing deposit addresses, `clone_restriction`); exports standalone JSON review packets and self-contained static HTML inspectors. |
| **CS-04: Test Suite & Offline Drivers** | `cybersec/pramana/tests/` + Root Runners | `test_cyber_slice.py`, `test_adapter_regressions.py`, `test_fixtures.py`, `run_cyber_demo.py`, `run_cyber_validation.py`, `run_canonicalization.py`, `run_ingestion.py` | Automated offline verification suite (76 passed, 13 archive-opt-in skipped); zero network, database, or GPU requirement. |
| **CS-05: Documentation, Reports & Evidence** | `cybersec/pramana/docs/` + Root Dossiers | `docs/cyber/` (`demo/review.html`, `validation/pytest.xml`), `PRAMANA_CYBER_INTELLIGENCE_SPEC_v1.md`, `PRAMANA_Master_Blueprint.md`, `PRAMANA_Technical_Project_Dossier.pdf` | Architectural blueprints, formal cyber policy definitions, reproduction guides, benchmark reports, and forensic audit records. |
| **CS-06: Verification Assets & QA Runs** | `cybersec/pramana/hatch-runs/` | `starjotaro-v2/` (`decoded/`, `final/`, `qa/`, `source/`) | Quality assurance visual assets, contact sheets, anchor alignments, and sprite manifests supporting offline validation and prototype verification. |
