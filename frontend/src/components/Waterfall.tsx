import type { Assessment } from '../data/model'
import { buildWaterfall } from '../lib/engine'
import { Section } from '../lib/ui'

const MAX = 10 // 0..10 log₁₀ LR spans the track

const FILL = {
  add: 'var(--color-support)',
  subtract: 'var(--color-counter)',
  clip: 'var(--color-suppressed)',
  total: 'var(--color-ink)',
} as const

export function Waterfall({ a }: { a: Assessment }) {
  const { steps, naiveTotal, finalTotal } = buildWaterfall(a)

  return (
    <Section
      title="How the number is built"
      aside={
        <>
          naive {naiveTotal >= 0 ? '+' : ''}
          {naiveTotal.toFixed(2)} &rarr; {a.issued ? finalTotal.toFixed(2) : 'refused'}
        </>
      }
    >
      <div className="relative">
        {/* ceiling marker */}
        <div
          className="pointer-events-none absolute bottom-1 top-0 border-l border-dashed border-[var(--color-ink-faint)]"
          style={{ left: `${(4 / MAX) * 100}%` }}
        >
          <span className="num absolute -top-0.5 left-1 text-[9px] text-[var(--color-ink-faint)]">
            ceiling 4.0
          </span>
        </div>

        <ul className="stagger flex flex-col">
          {steps.map((s, i) => {
            const isTotal = s.kind === 'total'
            const from = s.kind === 'add' ? s.running - s.delta : isTotal ? 0 : s.running
            const to = s.kind === 'add' ? s.running : isTotal ? s.running : s.running - s.delta
            const left = (Math.min(from, to) / MAX) * 100
            const width = (Math.abs(to - from) / MAX) * 100
            const prev = steps[i - 1]

            return (
              <li
                key={i}
                style={{ '--i': i } as React.CSSProperties}
                className="grid grid-cols-[1fr_auto] items-center gap-x-4 py-[5px]"
              >
                <div className="min-w-0">
                  <div
                    className={`truncate text-[11.5px] ${
                      isTotal ? 'font-semibold text-[var(--color-ink)]' : 'text-[var(--color-ink-soft)]'
                    }`}
                    title={s.note ? `${s.label} — ${s.note}` : s.label}
                  >
                    {s.label}
                  </div>
                  {s.note && (
                    <div className="truncate text-[10px] text-[var(--color-ink-faint)]">{s.note}</div>
                  )}
                  {/* the bar track */}
                  <div className="relative mt-1 h-3 rounded-[3px] bg-[var(--color-paper)]">
                    {/* connector from the previous step's running total */}
                    {prev && !isTotal && (
                      <span
                        className="absolute -top-1 h-1 border-l border-[var(--color-hairline-strong)]"
                        style={{ left: `${(prev.running / MAX) * 100}%` }}
                      />
                    )}
                    <span
                      className="absolute top-0 h-full rounded-[3px] transition-[left,width] duration-300"
                      style={{ left: `${left}%`, width: `${Math.max(width, 0.6)}%`, background: FILL[s.kind] }}
                    />
                  </div>
                </div>

                <span
                  className={`num w-16 shrink-0 self-end pb-0.5 text-right text-[11.5px] ${
                    s.kind === 'subtract' || s.kind === 'clip'
                      ? 'text-[var(--color-counter)]'
                      : isTotal
                        ? 'font-semibold text-[var(--color-ink)]'
                        : 'text-[var(--color-ink)]'
                  }`}
                >
                  {isTotal
                    ? a.issued
                      ? s.running.toFixed(2)
                      : '—'
                    : s.delta > 0
                      ? `+${s.delta.toFixed(2)}`
                      : s.delta.toFixed(2)}
                </span>
              </li>
            )
          })}
        </ul>
      </div>

      <p className="mt-3 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
        Naive additive scoring reads{' '}
        <span className="num text-[var(--color-ink)]">
          {naiveTotal >= 0 ? '+' : ''}
          {naiveTotal.toFixed(2)}
        </span>{' '}
        ({a.naive_baseline.verbal_band}). Counting mirrored evidence once and zeroing shared-hub
        indicators leaves{' '}
        <span className="num font-semibold text-[var(--color-ink)]">
          {a.issued ? finalTotal.toFixed(2) : 'no issued score'}
        </span>
        {a.issued ? ` (${a.verbal_band}).` : '.'}
      </p>
    </Section>
  )
}
