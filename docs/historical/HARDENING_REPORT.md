# PRAMANA hardening sprint — 2026-09-10

Implementation completed directly in the extracted workspace. No Git operations were used in this sprint. This is a hardened research prototype, not a production-ready or policy-complete attribution system.

## Exact source/document files changed and why

Each row states the implementation and the defect or reproducibility need it addresses. Frozen CyberSec specifications, the master blueprint, both frozen dataclass shapes, frontend and backend files were left byte-for-byte unchanged.

| File | Change and reason |
|---|---|
| `README.md` | Replaced stale capability/deployment claims with current boundaries, reproducible commands, measured baseline and explicit limitations. |
| `ai-ml/README.md` | Corrected fusion mathematics and documented feature methods, API scope and separate frozen interfaces. |
| `ai-ml/requirements.txt` | Added missing test/graph dependencies and Python 3.13 PGPy compatibility dependency. |
| `requirements-research-lock.txt` | New exact environment freeze including the pinned spaCy model URL/hash; reproduces this Windows Python 3.13 test environment. |
| `ai-ml/pramana/data.py` | New validated account loader: rejects empty populations, duplicate IDs and missing/null indicator/provenance fields; defaults resolve from package location. |
| `ai-ml/pramana/rarity.py` | Uses validated population and instance-owned tau; removes CWD selection and global tau dependence while retaining rarity formula and unseen-count convention. |
| `ai-ml/pramana/stub_features_a.py` | Uses explicit, context-managed corpus loading; rejects duplicate/reversed, self and unknown-account candidate pairs. |
| `ai-ml/pramana/score_pramana.py` | Validates mutable Observation inputs, pair ownership, finite parameters and provenance; rejects cross-family allocation of the same fact, unsupported F9 promotion and non-Observation inputs. Stable sorting and ablation IDs replace object addresses; explanations retain full origins and indicator traces. Adds honest limitations and guards evaluation threshold against excluded/nonfinite outputs. Numerical priors unchanged. |
| `ai-ml/pramana/api.py` | Adds create_app with per-instance data/cache, atomic cache publication, defensive response copies, canonical pair order and self-pair validation; retains all four routes and optional naive results. Describes API as a synthetic demo. |
| `ai-ml/pramana/evaluate.py` | Uses explicit corpus directory, validates ground-truth coverage and labels, rejects mismatched/nonbinary confusion inputs, actually uses tau argument, and computes residual-failure count dynamically. |
| `ai-ml/pramana/range_sim.py` | Uses local seeded RNG without modifying global random state; writes seed/count/SHA-256 manifest and corrects obsolete 500-pair output label. Generated fixture content preserved. |
| `ai-ml/pramana/sensitivity.py` | Passes tau explicitly rather than mutating module state; removes an unsupported recommendation to change hub policy. |
| `ai-ml/group_g_llm_assist/hypothesis_generator.py` | Removes positive LLM candidate weight; sets zero weight, blocked promotion, scoring-ineligible flag and citation-ID-only validation scope without changing the frozen shape. |
| `ai-ml/group_d_embeddings/image_embeddings.py` | Removes false file-size fallback and silent missing-file similarity; decoding/dependency errors propagate; image files close deterministically. |
| `ai-ml/group_d_embeddings/text_embeddings.py` | Makes deterministic trigram cosine the explicit default and retains optional caller-supplied model execution; removes implicit downloads/method switching and reports the actual candidate method. Rejects nonfinite model output and treats whitespace-only input as empty. |
| `ai-ml/group_b_nlp/lang_ner.py` | Removes import-time model download; allows explicit model injection, gives actionable missing-model error, uses locally seeded language detector and sorted output lists. |
| `ai-ml/group_c_wallet_infra/wallet_cluster.py` | Fixes component bridging through non-root addresses with stable union-find representatives; adds explicit optional risk CSV path for isolated tests. |
| `ai-ml/group_f_graph/co_occurrence.py` | Makes identical document replay idempotent and rejects conflicting content under an existing document ID before graph mutation. |
| `ai-ml/group_a_deterministic/test_group_a.py` | Retains original remote validator as command-line checks; adds five assertion-based offline pytest tests instead of collecting functions requiring an undefined gt fixture. |
| `ai-ml/group_b_nlp/test_group_b.py` | Moves generated text fixtures into automatically cleaned temporary directories. |
| `ai-ml/group_c_wallet_infra/test_group_c.py` | Moves generated CSV into an automatically cleaned temporary directory and passes its path explicitly; stops overwriting checked-in data. |
| `ai-ml/tests/test_hardening.py` | Adds 46 parameterized regression cases covering integrity, deterministic replay, validation, API caches, authority boundaries and failure paths. |
| `HARDENING_REPORT.md` | This exact change/result/limitations report. |

The checked-in Bitcoin fixture was temporarily rewritten by an existing test, then restored to its original SHA-256. It is not a final source change. A workspace `.venv/` was created; installed third-party files are environment artifacts, recorded by the lock rather than source changes.

## Tests and verification — actual final runs

Python 3.13.7, Windows, pytest 9.1.1. Full command arguments, working directories and exit codes are in `hardening-artifacts/runs.json`; corresponding `.txt` files contain complete stdout/stderr.

| Run | Exact result |
|---|---|
| Complete root suite: `python -m pytest -q -ra` | 161 passed, 13 skipped, 3 warnings in 12.02s; exit 0 |
| AI/ML: `python -m pytest -q ai-ml` | 85 passed, 3 warnings in 8.93s; exit 0 |
| CyberSec: `python -m pytest -q cybersec/pramana` | 76 passed, 13 skipped in 0.67s; exit 0 |
| Fusion and adversarial tests: `python -m pytest -q ai-ml/tests` | 56 passed, 2 warnings in 5.74s; exit 0 |
| `python -m pip check` | No broken requirements found; exit 0 |
| `python -m pramana.demo` | Exit 0; decoy refused; true fixture pair score 3.672 STRONG; handover fixture score 3.32 STRONG (known false positive) |
| `python -m pramana.range_sim <output>` | Exit 0; 60 synthetic operators, 137 accounts, 555 listings, 900 pairs (99 positive, 801 negative); manifest saved |
| `python -m pramana.evaluate` | Exit 0; unchanged ablation results below |
| `python -m pramana.sensitivity` | Exit 0; lambda and tau sweeps completed |
| `python run_cyber_demo.py --output-dir <output>` | Exit 0; 18 records, 53 indicators, 13 hub accounts, 0 promoted candidates, null assessment, blocked_DC-06 |
| `python run_cyber_validation.py --output <output>` | Exit 1: FileNotFoundError for absent grams.tar.xz; real-source validation NOT measured |

All `python` commands above used the workspace `.venv/Scripts/python.exe`. The verifier itself returns exit 1 because real-source validation failed; it does not hide that failure. Thirteen skips are the existing opt-in archive fixtures. Three warnings come from PGPy/imghdr compatibility and Starlette/httpx/AnyIO deprecations, not failed assertions.

Baseline: system Python could not collect five AI/ML modules because dependencies were absent. The unchanged CyberSec baseline was 76 passed, 13 skipped. The first installed full-suite attempt found PGPy's missing imghdr on Python 3.13, resolved with standard-imghdr. Original remote Group A validation was retained but not run against external HF data; the five offline tests do not validate that remote corpus.

## Measured synthetic evaluation

| Method | False positives before → after | TP / FP / FN / TN after | FMR after | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| Naive | 239 → 239 | 94 / 239 / 5 / 562 | 0.2983770287141074 | 0.2822822822822823 | 0.9494949494949495 | 0.43518518518518523 |
| No grouping | 28 → 28 | 85 / 28 / 14 / 773 | 0.03495630461922597 | 0.7522123893805309 | 0.8585858585858586 | 0.8018867924528301 |
| PRAMANA | 12 → 12 | 85 / 12 / 14 / 789 | 0.0149812734082397 | 0.8762886597938144 | 0.8585858585858586 | 0.8673469387755102 |

803 refusals before and after. The 12 false positives comprise 10 planted handovers and 2 ordinary negatives. Regenerated-corpus metrics match the package corpus. Two generated runs are byte-identical, and fixture text matches the original corpus (allowing platform line-ending differences). SHA-256 manifests cover accounts, pairs and answer key. No scoring constants, thresholds or penalties were tuned.

Lambda 0, 0.1, 0.2, 0.3, 0.4 and 0.6 gave the same reported metrics. Tau 6/9 gave 84.8% recall; 12 gave 85.9%; 18/25 gave 86.9%; all had 1.5% rounded FMR. Tau 1,000,000 gave 3.5% rounded FMR and 87.9% recall. Exact default metrics are retained in `metrics.json`; full sweep output is in `sensitivity.txt`.

No controlled latency, throughput or memory benchmark was performed. Union-find correctness, model reuse through explicit injection and removal of repeated implicit model loading are engineering changes; no speedup number is claimed. Test durations are runner observations, not performance benchmarks.

## Security and adversarial regressions

New cases cover malformed/empty/NaN/infinite inputs, invalid parameters, pair contamination, repeated observations, mirror hit counts, conflicting family allocation, shared origins, empty evidence, soft contradictions, injected hard-veto branch behavior, mutable inputs, iterator inputs, order invariance, process-independent explanation IDs, CWD poisoning, invalid/duplicate populations, hub threshold boundaries, tau isolation, global RNG preservation, manifest checks, label isolation, unequal confusion vectors, API pair order/self-pairs/cache contamination, zero-weight LLM envelopes, blocked CyberSec packet promotion, corrupt/missing images, explicit model failures, wallet component bridging and graph-document replay.

Hard-veto regression uses a clearly named injected test fixture solely to exercise the existing branch. No real detector, veto qualification rule or identity capability was invented. No external targets were accessed. Dependency/model downloads were setup actions only.

## Remaining issues and deferred capabilities

**P0 — barriers to operational evidence use:** DC-01 general origin adjudication and cross-family dependence remain unresolved; synthetic k is only a count heuristic. DC-05 qualified veto detectors and DC-06 promotion remain deferred. Feature family mappings and synthetic score semantics are not an approved CyberSec interface. F9 promotion is rejected until qualified; LLM citation checks cannot validate factual entailment. The pipeline must not be used to establish identity or accepted personas.

**P1 — research/robustness gaps:** no held-out independent evaluation or calibrated likelihood ratios, Cllr/ECE/Tippett analysis; all-positive-plus-sampled-negative pair selection does not measure retrieval recall or operational prevalence. Simulator traps can reuse accounts and overwrite earlier planted signals; multi-seed trap survival needs a separately versioned evaluation design. Missing-vs-contradictory temporal facts need qualified semantics. Synthetic unseen indicators still use the existing count-one convention. The feature emitter still assumes capture keys and reduces image provenance to a per-image mapping; ambiguous multiple captures need an approved contract. General clone detection and cross-dataset decontamination remain deferred.

**P1 — deployment gaps:** Worker scoring is duplicated and not parity-tested with Python; it still has permissive client-supplied priors/counts. HF wrapper and deployment were not exercised. API remains a local synthetic demonstration without authentication, persistent ledger, multi-process cache coordination or operational resource limits. Real archive is absent. No external security audit or dependency vulnerability scan was performed.

**P2:** consolidate historical handoff claims after team review, add supported-platform CI and portable lock strategy, resolve upstream deprecations, expand actual image/model validation and scalability measurements. Historical frozen/specification claims were not rewritten; the current READMEs explicitly distinguish specification from implementation.

Persistent ledger, retraction propagation, trained classification/semantic model validation, authorised live collection/RANGE-TOR, source qualification workflows, operational calibration and human persona acceptance remain deferred or unvalidated.

## Claims the team can and cannot make

**Safe:** an offline CyberSec review prototype preserves raw provenance and blocks evidence promotion; a separate deterministic synthetic fusion experiment suppresses repeated/hub support under its declared assumptions; measured v0.1 outcomes and residual false positives are reproducible; this sprint added explicit failures, deterministic execution and regression coverage without changing frozen policy.

**Unsafe:** production-ready, full CY-POL compliance, validated attribution, real-world identity inference, calibrated likelihood ratios/confidence, ownership proof, automatic persona acceptance, implemented operational vetoes, independent real-world accuracy, proven general source independence, verified deployed services, or performance gains not measured here.

## Artifact inventory

`hardening-artifacts/changed-files.json` lists all final source changes and generated artifacts (excluding virtualenv/caches). `before-sha256.json` records the inspected source baseline; `protected-files.json` records unchanged protected files. Logs, corpus/manifest, demo review packet/HTML and exact metrics are retained. `hardening-artifacts/verify.py` repeats the acceptance commands and returns nonzero on any failed command.
