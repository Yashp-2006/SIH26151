# Screenshots — SIH26151 (PRAMANA)

Captures of the running analyst console (`frontend/`) with the gateway (`backend/`) live.
1440 px, 2× density.

| File | View |
|---|---|
| `01-landing.png` | Landing page — the problem, the evidence-ledger schematic panel |
| `02-overview.png` | Console overview — RANGE-SIM headline metrics and the three attribution cases |
| `03-evidence-balance-sheet.png` | Evidence Balance Sheet — verdict, "how the number is built" waterfall, evidence by family, counter-evidence, limitations |
| `04-investigation-workspace.png` | Investigation Workspace — shared-indicator graph between two personas |
| `05-assessment-review.png` | Assessment & Review — sequential-unmasking review gate |
| `06-evaluation-ablation.png` | Evaluation — naive / no-grouping / PRAMANA ablation table |
| `07-api-docs.png` | FastAPI gateway OpenAPI docs (`:8000/docs`) |

Regenerate: run the gateway (`:8000`) and `frontend` (`:5173`), then drive the app
with a headless browser (Playwright/Puppeteer) capturing each view.

Do not commit images containing real credentials or unredacted confidential data.
