# pramana/features/ — additional evidence-family generators

From `archive/data-ml-capabilities`. Each emits a `shared.contracts.EvidenceCandidate`;
none makes a merge decision.

| File | Family | Method | Deps |
|---|---|---|---|
| `f7_semantic.py` | F7 | LDA topic-distribution similarity between two text corpora | `scikit-learn` (optional) |
| `f8_behavioral.py` | F8 | active-posting-hour (TTP) temporal overlap | stdlib |

`../fit_priors.py` fits an empirical damping λ from the RANGE-SIM answer key
(≈ 0.1) as a check against the asserted design prior (0.2).
