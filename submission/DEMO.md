# Demo Video — SIH26151 (PRAMANA)

Walkthrough of PRAMANA — Darknet Intelligence & Evidence Fusion Platform.

## Demo Video Link

https://drive.google.com/file/d/1xKxKNEzaDMOBwUQMwkx5YHu8MrsyR5nu/view?usp=sharing

Verify it plays without a request-access prompt in an incognito window
(sharing must be **Anyone with the link — Viewer**).

## What the Video Shows

1. **The problem** — why naive additive scoring inflates confidence on mirrored
   listings, shared market infrastructure and planted decoys.
2. **The analyst console** — Overview metrics, then the **Evidence Balance Sheet**
   for a persona pair: verbal band, the fusion waterfall (naive → independence
   grouping → hub suppression → ceiling → counter-evidence), evidence by family.
3. **Independence at work** — the Workspace shared-indicator graph, and the
   planted-decoy case being **refused** (`k = 1 < 2`).
4. **Evaluation** — the naive / no-grouping / PRAMANA ablation: false-merge rate
   29.8% → 1.5%, 20/20 decoys refused.
5. **Engine + gateway** — `python -m pramana.demo` and the FastAPI `/assess`,
   `/balance_sheet`, `/nlp/*` routes.
