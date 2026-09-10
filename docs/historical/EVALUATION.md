# Evaluation Methodology

## Datasets
- **RANGE-SIM:** A synthetic, closed-world dataset containing 900 pairs (99 positive, 801 negative) of simulated dark-web interactions with planted decoys.
- **GRAMS (Missing/Quarantined):** A 12-million record historical dark web dataset. `run_cyber_validation.py` operates on a 4,397-record bounded subset but skips if the archive is absent.

## Metrics
- **False Merge Rate (FMR):** The critical metric. The percentage of non-target pairs falsely attributed to the same operator.
- **Expected Calibration Error (ECE):** Evaluates if the output Log-LR actually correlates with real-world probability.
- **Tippett Plots:** Cumulative Distribution Functions of same-source vs different-source comparisons.

## What it Proves
The evaluation proves that applying Independence Accounting ($k$) to evidence fusion dramatically reduces FMR compared to naive additive algorithms.
