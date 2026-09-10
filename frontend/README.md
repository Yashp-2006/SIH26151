# frontend/

PRAMANA analyst dashboard — React 18 + TypeScript + Vite + Tailwind v4.

## Run

```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
```

The dashboard reads a **static snapshot** of the fusion engine's output
(`public/snapshot.json`) so the demo never makes a live inference call — this is
what `ai-ml/pramana/api.py` itself recommends. When the backend is running
(`../backend`, port 8000) the dashboard uses it for live re-scoring and falls
back to the snapshot otherwise.

## Snapshot

`public/snapshot.json` is generated from the real engine in `ai-ml/pramana/`:

```bash
python frontend/scripts/gen_snapshot.py
```

It carries: engine params (`lambda`, `tau`, caps, `k_min`, ceiling), the
RANGE-SIM v0.1 ablation metrics (naive / no-grouping / PRAMANA), all 900
candidate-pair assessments with family breakdowns and counter-evidence, the
account list, and the three curated demo cases.

## Structure

```
src/
  data/model.ts   TypeScript mirror of the engine's Assessment schema
  data/store.tsx  loads snapshot.json, probes the gateway, exposes assess()
  lib/engine.ts   verdict/band/waterfall helpers over an Assessment (no scoring)
  lib/ui.tsx      primitives — Card, Section, Chip, FamilyTag, Button
  lib/icons.tsx   inline SVG icon set (no icon library)
  screens/        Landing · Login · Overview · Case · Workspace · Review · Evaluation
  components/     Shell (sidebar), CasePicker, Verdict, Waterfall, EvidenceTable, CounterEvidence
scripts/gen_snapshot.py   regenerate public/snapshot.json from ai-ml/pramana
```

## Flow

Landing → sign-in → console with a left sidebar:

- **Overview** — RANGE-SIM headline metrics and the representative cases
- **Evidence Balance Sheet** — one persona pair: verdict, the fusion waterfall
  (naive → grouping/hub → ceiling → counter-evidence), evidence by family with
  the engine's own discount reasons, counter-evidence, limitations
- **Workspace** — shared-indicator graph, hub-suppressed edges dashed
- **Assessment & Review** — sequential-unmasking review gate
- **Evaluation** — the naive / no-grouping / PRAMANA ablation

Design tokens live in `src/index.css` — neutral zinc, one muted slate-blue
accent used flat, colour reserved for evidence data.
