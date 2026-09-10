# PRAMANA AI/ML research components

See the root [README](../README.md) and [hardening report](../HARDENING_REPORT.md)
for current capabilities, exact results and limitations.

The fusion engine is **grouped, capped, rarity-weighted additive log scoring**;
it does not implement Dempster-Shafer fusion. Its scores and verbal bands are
uncalibrated synthetic research outputs. CyberSec evidence promotion is deferred.

`shared/contracts.py` contains the unchanged feature-candidate shape.
`pramana/schema.py` contains the unchanged synthetic fusion shape. They are not
interchangeable. Features from Groups A-G are not automatically scored or promoted.
LLM hypotheses have zero weight and remain non-authoritative even when citation IDs
exist. Missing or invalid inputs do not establish counter-evidence.

After installing the root research lock, from this directory:

```powershell
../.venv/Scripts/python -m pytest -q .
../.venv/Scripts/python -m pramana.range_sim ../hardening-artifacts/range-sim
../.venv/Scripts/python -m pramana.demo
../.venv/Scripts/python -m pramana.evaluate
../.venv/Scripts/python -m pramana.sensitivity
../.venv/Scripts/python -m uvicorn pramana.api:app --host 127.0.0.1 --port 8000
```

The local API supports `/health`, `/assess`, `/precompute` and
`/balance_sheet/{account_a}/{account_b}`. It serves a fixed synthetic corpus,
normalizes pair order, rejects self-pairs, and owns a per-app cache. It is not an
authenticated production ledger service. `create_app(data_dir=...)` selects an
explicit alternative synthetic corpus.

The default text similarity method is deterministic character-trigram cosine.
An explicitly supplied model remains supported by `compute_text_similarity`;
model failures propagate, and no runtime download or silent method switch occurs.
Image similarity uses pHash and raises on unavailable/corrupt inputs. spaCy NER
requires an explicitly installed model; imports never download one.

The Worker and HF service are separate integration surfaces. Their deployment,
Python scoring parity and production security have not been verified by this sprint.
