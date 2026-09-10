import { useApp } from '../data/store'
import { verdictOf, verdictLabel, verdictTone } from '../lib/engine'
import type { View } from '../components/Shell'
import { ArrowRight, Link2 } from '../lib/icons'

const KIND_LABEL: Record<string, string> = {
  planted_decoy: 'Planted decoy',
  true_same_operator: 'True pair',
  account_handover: 'Account handover',
}

export function Overview({ onOpenCase }: { onOpenCase: (pid: string, v: View) => void }) {
  const { snapshot } = useApp()
  const m = snapshot.metrics

  const stats = [
    {
      label: 'False-merge rate',
      value: `${(m.pramana.false_merge_rate * 100).toFixed(1)}%`,
      sub: `from ${(m.naive.false_merge_rate * 100).toFixed(1)}% naive`,
    },
    {
      label: 'Precision',
      value: `${(m.pramana.precision * 100).toFixed(1)}%`,
      sub: `from ${(m.naive.precision * 100).toFixed(1)}%`,
    },
    {
      label: 'Pairs refused · k < 2',
      value: m.corpus.refused_k_lt_2.toLocaleString(),
      sub: 'single-family, not enough',
    },
    {
      label: 'Decoys refused',
      value: `${m.corpus.decoys} / ${m.corpus.decoys}`,
      sub: 'planted single-vector traps',
    },
  ]

  const featured = snapshot.demo_cases.find((c) => c.kind === 'true_same_operator')
  const rest = snapshot.demo_cases.filter((c) => c !== featured)
  const A = featured && (featured.assessment ?? snapshot.assessments[featured.pair_id])

  return (
    <div className="flex flex-col gap-8">
      <p className="max-w-[62ch] text-[13px] leading-relaxed text-[var(--color-ink-soft)]">
        <span className="num text-[var(--color-ink)]">{m.corpus.pairs}</span> candidate persona pairs
        across <span className="num text-[var(--color-ink)]">{m.corpus.operators}</span> operators.
        Independence accounting is the whole difference between the naive column and the shipped one.
      </p>

      {/* stat bar — one bordered strip, internal dividers (not four cards) */}
      <div className="grid divide-y divide-[var(--color-hairline)] rounded-[var(--r-lg)] border border-[var(--color-hairline)] bg-[var(--color-surface)] sm:grid-cols-4 sm:divide-x sm:divide-y-0">
        {stats.map((s) => (
          <div key={s.label} className="px-4 py-3.5">
            <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
              {s.label}
            </div>
            <div className="num mt-1 text-[22px] font-semibold text-[var(--color-ink)]">
              {s.value}
            </div>
            <div className="mt-0.5 text-[10.5px] text-[var(--color-ink-soft)]">{s.sub}</div>
          </div>
        ))}
      </div>

      {/* cases */}
      <div>
        <h2 className="text-[11px] font-semibold uppercase tracking-[0.09em] text-[var(--color-ink-faint)]">
          Attribution cases
        </h2>
        <div className="mt-3 grid gap-3 lg:grid-cols-[1.5fr_1fr]">
          {featured && A && (
            <button
              type="button"
              onClick={() => onOpenCase(featured.pair_id, 'case')}
              className="group flex flex-col rounded-[var(--r-lg)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] p-5 text-left"
            >
              <div className="text-[10.5px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                {KIND_LABEL[featured.kind]}
              </div>
              <div className="num mt-1 flex items-center gap-1.5 text-[14px] font-medium text-[var(--color-ink)]">
                {featured.detail_a.handle}
                <Link2 className="text-[var(--color-ink-faint)]" />
                {featured.detail_b.handle}
              </div>
              <div className={`mt-3 text-[22px] font-semibold ${verdictTone(verdictOf(A)).fg}`}>
                {verdictLabel(verdictOf(A))}
                {A.issued && (
                  <span className="num ml-2 text-[13px] font-normal text-[var(--color-ink-faint)]">
                    log₁₀ LR {A.log_lr?.toFixed(2)}
                  </span>
                )}
              </div>
              <p className="mt-2 max-w-[46ch] text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                {featured.caption}
              </p>
              <span className="mt-auto flex items-center gap-1 pt-4 text-[11.5px] font-medium text-[var(--color-accent)]">
                Open balance sheet <ArrowRight size={13} />
              </span>
            </button>
          )}
          <div className="stagger flex flex-col gap-3">
            {rest.map((c, i) => {
              const a = c.assessment ?? snapshot.assessments[c.pair_id]
              const v = verdictOf(a)
              return (
                <button
                  key={c.pair_id}
                  type="button"
                  style={{ '--i': i } as React.CSSProperties}
                  onClick={() => onOpenCase(c.pair_id, 'case')}
                  className="flex flex-1 flex-col rounded-[var(--r-lg)] border border-[var(--color-hairline)] bg-[var(--color-surface)] p-4 text-left transition-colors hover:border-[var(--color-hairline-strong)]"
                >
                  <div className="text-[10.5px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                    {KIND_LABEL[c.kind]}
                  </div>
                  <div className="num mt-1 flex items-center gap-1.5 text-[12.5px] text-[var(--color-ink)]">
                    {c.detail_a.handle}
                    <Link2 className="text-[var(--color-ink-faint)]" />
                    {c.detail_b.handle}
                  </div>
                  <div className={`mt-1.5 text-[14px] font-semibold ${verdictTone(v).fg}`}>
                    {verdictLabel(v)}
                  </div>
                  <p className="mt-1 text-[11px] leading-relaxed text-[var(--color-ink-soft)]">
                    {c.caption}
                  </p>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
