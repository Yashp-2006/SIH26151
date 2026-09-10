# PRAMANA AI-ML Modules

Evidence Generation, Classification, Graph Topology, and Evidence Fusion modules for the SIH26151 dark-web attribution platform.

## Architecture

The AI-ML subsystem is split into two primary suites adhering to the frozen `EvidenceCandidate` contract (`shared/contracts.py`):

### List A — Deterministic & Lexical Baselines
- `shared/`: Frozen contract (`EvidenceCandidate`) and data loaders.
- `group_a_deterministic/`: Canonicalization, exact repetition, PGP metadata extraction (F1, F3, F5).
- `group_b_nlp/`: Stylometry, language detection, NER, and template extraction (F5).
- `group_c_wallet_infra/`: Wallet clustering, temporal overlap, and server banner extraction (F2, F3).
- `cloudflare-workers/`: Edge deployment Worker running lightweight heuristic extractors.

### List B — NLP, Embeddings, Graph, and Fusion Engine
- `group_d_embeddings/`: Sentence and perceptual embedding similarity, ANN search index (F6).
- `group_e_classification/`: Multi-label category tagging, threat risk tiering, keyword evasion/leetspeak detection (F7).
- `group_f_graph/`: Entity co-occurrence graphs, ego-network extraction, shortest path proximity (F8).
- `group_g_llm_assist/`: Grounded investigation prompts, strict citation validator, candidate link hypotheses (F9 non-authoritative).
- `pramana/`: PRAMANA Evidence Fusion Engine (independence grouping, within-family damping, family caps, false-merge suppression).

## Interface Contract Rules

- All sub-modules return `EvidenceCandidate` records.
- Feature-level extra details belong strictly in `extra: dict`.
- No module may directly output an authoritative merge decision, pair confidence score, or modify `evidence` / `assessment` state.
- Fusion Engine (`ai-ml/pramana/`) performs non-linear Dempster-Shafer style Bayesian likelihood-ratio synthesis with strict $k \ge 2$ independent family origin gates.

## Verification & Testing

### Running List B Tests
```bash
pytest group_d_embeddings/ group_e_classification/ group_f_graph/ group_g_llm_assist/ tests/
```

### Running PRAMANA Fusion Engine Range-Sim & Demo
```bash
python -m pramana.range_sim
python -m pramana.demo
```

### Typechecking Cloudflare Worker
```bash
cd cloudflare-workers
npm install
npx tsc --noEmit
```
