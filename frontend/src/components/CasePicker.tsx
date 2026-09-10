import { useState } from 'react'
import { useApp } from '../data/store'
import { ChevronDown, Search } from '../lib/icons'

const KIND_LABEL: Record<string, string> = {
  planted_decoy: 'planted decoy',
  true_same_operator: 'true pair',
  account_handover: 'account handover',
}

export function CasePicker({ pairId, onPick }: { pairId: string; onPick: (pid: string) => void }) {
  const { snapshot } = useApp()
  const [open, setOpen] = useState(false)
  const [q, setQ] = useState('')

  const current =
    snapshot.demo_cases.find((c) => c.pair_id === pairId) ??
    snapshot.pairs.find((p) => p.pair_id === pairId)
  const label =
    current && 'detail_a' in current
      ? `${current.detail_a.handle} / ${current.detail_b.handle}`
      : pairId

  const matches = q
    ? snapshot.pairs
        .filter((p) => p.pair_id.includes(q) || p.account_a.includes(q) || p.account_b.includes(q))
        .slice(0, 8)
    : []

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 rounded-[var(--r)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] px-3 py-1.5 text-[12.5px] font-medium text-[var(--color-ink)] transition-colors hover:border-[var(--color-ink-faint)]"
      >
        <span className="num">{label}</span>
        <ChevronDown className="text-[var(--color-ink-faint)]" />
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />
          <div className="absolute right-0 z-20 mt-1.5 w-[320px] rounded-[var(--r-lg)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] p-1.5 shadow-[0_10px_30px_-12px_rgba(28,28,26,0.18)]">
            <div className="px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.07em] text-[var(--color-ink-faint)]">
              Cases
            </div>
            {snapshot.demo_cases.map((c) => (
              <button
                key={c.pair_id}
                type="button"
                onClick={() => {
                  onPick(c.pair_id)
                  setOpen(false)
                }}
                className={`block w-full rounded-[var(--r)] px-2 py-1.5 text-left hover:bg-[var(--color-paper)] ${
                  c.pair_id === pairId ? 'bg-[var(--color-accent-wash)]' : ''
                }`}
              >
                <div className="num text-[12px] text-[var(--color-ink)]">
                  {c.detail_a.handle} / {c.detail_b.handle}
                </div>
                <div className="text-[10.5px] text-[var(--color-ink-faint)]">
                  {KIND_LABEL[c.kind] ?? c.kind}
                </div>
              </button>
            ))}
            <div className="mt-1 flex items-center gap-1.5 border-t border-[var(--color-hairline)] px-2 pb-1 pt-2">
              <Search className="text-[var(--color-ink-faint)]" />
              <input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                placeholder="search all 900 pairs — acc_024…"
                className="num w-full bg-transparent text-[11px] outline-none placeholder:text-[var(--color-ink-faint)]"
              />
            </div>
            {matches.map((p) => (
              <button
                key={p.pair_id}
                type="button"
                onClick={() => {
                  onPick(p.pair_id)
                  setOpen(false)
                }}
                className="num block w-full rounded-[var(--r)] px-2 py-1 text-left text-[11.5px] text-[var(--color-ink-soft)] hover:bg-[var(--color-paper)]"
              >
                {p.account_a} / {p.account_b}
                {p.note && <span className="ml-1 text-[var(--color-flag)]">· {p.note}</span>}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
