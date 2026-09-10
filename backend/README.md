# PRAMANA — Backend & Evidence Fusion Engine (List B)

Person B's deliverable: Evidence Fusion Engine, independence-aware scoring, and FastAPI service.

No GPU or heavy ML model is required. `/assess` executes pure arithmetic over the provenance-qualified ledger and can run beside PostgreSQL or edge environments.

---

## Performance on RANGE-SIM v0.1

| Metric | Naive Additive | No Grouping | PRAMANA (Shipped) |
|---|---|---|---|
| **False-Merge Rate** | 29.8% | 3.5% | **1.5%** |
| False Merges (Count) | 239 | 28 | **12** |
| **Precision** | 28.2% | 75.2% | **87.6%** |
| **Recall** | 94.9% | 85.9% | **85.9%** |
| **F1 Score** | 0.435 | 0.802 | **0.867** |
| Decoys Refused | 0/20 | 20/20 | **20/20** |
| Assessments Refused ($k < 2$) | 0 | — | **803** |

*Corpus: 900 candidate pairs across 60 synthetic operators (99 positive, 801 negative, 20 planted decoys, 10 planted handovers).*
*Residual failures: 10 of the 12 false merges are planted account handovers (resold accounts genuinely inheriting seller identifiers, measuring residual risk).*

---

## Core Mechanisms

1. **Hub Suppression ($\tau = 12$):** Indicators appearing across $> 12$ accounts (e.g. default PGP blocks appearing on 69/137 accounts) are forced to zero weight.
2. **Independence Grouping:** Observations sharing an `independence_key` (same capture batch / site scrape) collapse to their strongest observation rather than accumulating duplicate votes.
3. **$\lambda$-Damping ($\lambda = 0.2$):** Successive independent groups within the same evidence family damp by $\lambda^i$.
4. **Family Caps:** Bounded maximum likelihood contribution per family ($F_1$: 4.0, $F_2$: 2.0, $F_3$: 2.5, $F_4$: 3.0, $F_5$: 2.5, $F_6$: 1.0, $F_7$: 0.7, $F_8$: 1.0, $F_9$: 3.0).
5. **Counter-Evidence:** $C_2$ contradictory identifier penalties and $C_5$ shared-ecosystem-not-shared-control detection.
6. **$k$-Origin Rule ($k \ge 2$):** System refuses to issue an assessment unless evidence spans $\ge 2$ independent evidence families across distinct capture origins.

---

## API Endpoints (`pramana.api`)

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Service status, pinned parameter version (`v0.1`), asserted priors |
| `POST` | `/assess` | Score pair given `{ account_a, account_b, include_naive? }` |
| `POST` | `/precompute` | Evaluates all candidate pairs at startup into memory cache |
| `GET` | `/balance_sheet/{a}/{b}` | Outputs complete Evidence Balance Sheet with family breakdowns and discount traces |

---

## Reproduction & Testing

```bash
# 1. Regenerate synthetic corpus (deterministic seed 26151)
python -m pramana.range_sim

# 2. Run ablation evaluation table
python -m pramana.evaluate

# 3. Run full demo (ablation + 3 balance sheets + sensitivity sweep)
python -m pramana.demo

# 4. Run parameter sensitivity sweeps
python -m pramana.sensitivity

# 5. Run test suite
pytest tests/test_fusion.py -v

# 6. Start FastAPI server
uvicorn pramana.api:app --port 8000
```
