import { useState } from 'react'
import { useApp } from '../data/store'
import type { MetricRow } from '../data/model'

type Col = 'naive' | 'no_grouping' | 'pramana'
const COL_LABEL: Record<Col, string> = {
  naive: 'Naive additive',
  no_grouping: 'No grouping',
  pramana: 'PRAMANA',
}
const COLS: Col[] = ['naive', 'no_grouping', 'pramana']
const pct = (x: number) => `${(x * 100).toFixed(1)}%`

export function Evaluation() {
  const { snapshot } = useApp()
  const m = snapshot.metrics
  const [col, setCol] = useState<Col>('pramana')
  const active = m[col] as MetricRow

  const rows: { label: string; get: (r: MetricRow) => string }[] = [
    { label: 'False-merge rate', get: (r) => pct(r.false_merge_rate) },
    { label: 'False merges (count)', get: (r) => String(r.false_merges) },
    { label: 'Precision', get: (r) => pct(r.precision) },
    { label: 'Recall', get: (r) => pct(r.recall) },
    { label: 'F1', get: (r) => r.f1.toFixed(3) },
    { label: 'True merges', get: (r) => String(r.true_merges) },
    { label: 'Missed links', get: (r) => String(r.missed_links) },
  ]

  const tiles = [
    { label: 'False-merge rate', value: pct(active.false_merge_rate), warn: col !== 'pramana' },
    { label: 'Precision', value: pct(active.precision), warn: false },
    { label: 'F1', value: active.f1.toFixed(3), warn: false },
  ]

  return (
    <div className="flex flex-col gap-6">
      <p className="max-w-[64ch] text-[13px] leading-relaxed text-[var(--color-ink-soft)]">
        RANGE-SIM v0.1 · {m.corpus.pairs} pairs, {m.corpus.positives} true, {m.corpus.decoys} planted
        decoys. Design priors (λ, τ, family caps) are asserted, not fitted.
      </p>

      <div className="flex gap-1.5">
        {COLS.map((c) => (
          <button
            key={c}
            type="button"
            onClick={() => setCol(c)}
            className={`rounded-[var(--r)] border px-3 py-1.5 text-[12px] font-medium transition-colors ${
              col === c
                ? 'border-[var(--color-accent)] bg-[var(--color-accent-wash)] text-[var(--color-accent)]'
                : 'border-[var(--color-hairline-strong)] text-[var(--color-ink-soft)] hover:border-[var(--color-ink-faint)]'
            }`}
          >
            {COL_LABEL[c]}
          </button>
        ))}
      </div>

      <div className="grid divide-y divide-[var(--color-hairline)] rounded-[var(--r-lg)] border border-[var(--color-hairline)] bg-[var(--color-surface)] sm:grid-cols-3 sm:divide-x sm:divide-y-0">
        {tiles.map((t) => (
          <div key={t.label} className="px-4 py-3.5">
            <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
              {t.label}
            </div>
            <div
              className={`num mt-1 text-[24px] font-semibold ${
                t.warn ? 'text-[var(--color-counter)]' : 'text-[var(--color-ink)]'
              }`}
            >
              {t.value}
            </div>
          </div>
        ))}
      </div>

      <div className="border-t border-[var(--color-hairline)] pt-5">
        <div className="mb-3 text-[10.5px] font-semibold uppercase tracking-[0.09em] text-[var(--color-ink-faint)]">
          Ablation — does independence accounting change the behaviour?
        </div>
        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-[12px]">
            <thead>
              <tr className="border-b border-[var(--color-hairline)] text-[10px] uppercase tracking-[0.05em] text-[var(--color-ink-faint)]">
                <th className="py-1.5 pr-3 font-semibold">Metric</th>
                {COLS.map((c) => (
                  <th
                    key={c}
                    className={`px-3 py-1.5 text-right font-semibold ${
                      col === c ? 'text-[var(--color-accent)]' : ''
                    }`}
                  >
                    {COL_LABEL[c]}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.label} className="border-b border-[var(--color-hairline)] last:border-0">
                  <td className="py-2 pr-3 text-[var(--color-ink)]">{r.label}</td>
                  {COLS.map((c) => (
                    <td
                      key={c}
                      className={`num px-3 py-2 text-right ${
                        col === c
                          ? 'font-semibold text-[var(--color-ink)]'
                          : 'text-[var(--color-ink-soft)]'
                      }`}
                    >
                      {r.get(m[c] as MetricRow)}
                    </td>
                  ))}
                </tr>
              ))}
              <tr>
                <td className="py-2 pr-3 text-[var(--color-ink)]">Pairs refused (k &lt; 2)</td>
                <td className="num px-3 py-2 text-right text-[var(--color-ink-faint)]">n/a</td>
                <td className="num px-3 py-2 text-right text-[var(--color-ink-faint)]">n/a</td>
                <td className="num px-3 py-2 text-right font-semibold text-[var(--color-ink)]">
                  {m.corpus.refused_k_lt_2}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="mt-3.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
          Naive scoring merges {m.naive.false_merges} unrelated pairs — mirrored listings and shared
          market infrastructure counted as independent votes. Grouping mirrored evidence and zeroing
          hub indicators drops that to {m.pramana.false_merges} ({m.pramana.true_merges} true merges
          held). The {m.pramana.false_merges} residual are planted account handovers — a resold
          account genuinely carries the seller's identifiers.
        </p>
      </div>
    </div>
  )
}
