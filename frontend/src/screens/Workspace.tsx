import { useState } from 'react'
import type { Assessment, AccountBrief, FamilyId } from '../data/model'
import { FAMILY_NAME } from '../data/model'
import { useApp } from '../data/store'
import { familyColor, verdictOf, verdictLabel, verdictTone } from '../lib/engine'
import { Card, Chip, FamilyTag, Lr } from '../lib/ui'

/** the shared value behind each family, read straight off the two accounts */
function sharedValue(f: FamilyId, A: AccountBrief, B: AccountBrief): string {
  switch (f) {
    case 'F1':
      return A.pgp_fp === B.pgp_fp ? A.pgp_fp : '—'
    case 'F3':
      return A.asn === B.asn ? A.asn : '—'
    case 'F4':
      return A.contact_id === B.contact_id ? A.contact_id : '—'
    case 'F5':
      return A.template_id === B.template_id ? A.template_id : 'shared image'
    default:
      return '—'
  }
}

function Terminal({ acc, side }: { acc: AccountBrief; side: 'l' | 'r' }) {
  return (
    <div
      className={`flex w-[140px] shrink-0 flex-col rounded-[var(--r)] border border-[var(--color-ink)] bg-[var(--color-surface)] px-3 py-2 ${
        side === 'l' ? 'items-start' : 'items-end text-right'
      }`}
    >
      <div className="num text-[12px] font-semibold text-[var(--color-ink)]">{acc.handle}</div>
      <div className="num text-[10px] text-[var(--color-ink-faint)]">{acc.market}</div>
      <div className="num mt-1 text-[9.5px] leading-tight text-[var(--color-ink-soft)]">
        {acc.pgp_fp}
        <br />
        {acc.contact_id} · {acc.asn}
      </div>
    </div>
  )
}

function Graph({ a, A, B }: { a: Assessment; A: AccountBrief; B: AccountBrief }) {
  const [sel, setSel] = useState<string | null>(null)

  return (
    <>
      <div className="flex items-stretch gap-3">
        <Terminal acc={A} side="l" />

        <div className="flex flex-1 flex-col justify-center gap-2 py-1">
          {a.families.map((f) => {
            const suppressed = f.capped_log_lr === 0
            const on = sel === f.family
            return (
              <button
                key={f.family}
                type="button"
                onClick={() => setSel(on ? null : f.family)}
                className={`group relative flex items-center gap-3 rounded-[var(--r)] border px-3 py-1.5 text-left transition-colors ${
                  on ? 'border-[var(--color-ink-faint)] bg-[var(--color-paper)]' : 'border-[var(--color-hairline)]'
                }`}
              >
                {/* connector stubs */}
                <span
                  className="pointer-events-none absolute right-full top-1/2 h-px w-3"
                  style={{ background: suppressed ? 'var(--color-suppressed)' : familyColor(f.family) }}
                />
                <span
                  className="pointer-events-none absolute left-full top-1/2 h-px w-3"
                  style={{ background: suppressed ? 'var(--color-suppressed)' : familyColor(f.family) }}
                />
                <span
                  className="h-2.5 w-2.5 shrink-0 rounded-[2px]"
                  style={{ background: suppressed ? 'var(--color-suppressed)' : familyColor(f.family) }}
                />
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5">
                    <span className="num text-[10.5px] font-medium text-[var(--color-ink-soft)]">
                      {f.family}
                    </span>
                    <span className="text-[11px] text-[var(--color-ink-faint)]">
                      {FAMILY_NAME[f.family]}
                    </span>
                    {suppressed && <Chip tone="counter">hub · 0</Chip>}
                  </div>
                  <div className="num truncate text-[11px] text-[var(--color-ink)]">
                    {sharedValue(f.family, A, B)}
                  </div>
                </div>
                <span className="num shrink-0 text-[12px] font-semibold">
                  <Lr value={f.capped_log_lr} />
                </span>
              </button>
            )
          })}
        </div>

        <Terminal acc={B} side="r" />
      </div>

      {sel && (
        <p className="mt-3 rounded-[var(--r)] bg-[var(--color-paper)] px-3 py-2.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
          {a.families.find((f) => f.family === sel)?.discount_reason}
        </p>
      )}
      <p className="mt-2 text-[11px] text-[var(--color-ink-faint)]">
        Each row is an indicator both accounts share. Grey rows are hubs — common enough that they
        contribute nothing. Select a row for its discount reason.
      </p>
    </>
  )
}

export function Workspace({ a }: { a: Assessment }) {
  const { snapshot } = useApp()
  const acc = (id: string) => snapshot.accounts.find((x) => x.account_id === id)
  const A = acc(a.account_a)
  const B = acc(a.account_b)
  const v = verdictOf(a)
  if (!A || !B) return null

  return (
    <div className="grid gap-4 lg:grid-cols-[1.25fr_0.75fr]">
      <Card title="Shared-indicator graph" aside={<>projection over the ledger</>}>
        <Graph a={a} A={A} B={B} />
      </Card>

      <div className="flex flex-col gap-4">
        <Card title="Hypothesis">
          <p className="text-[12.5px] leading-relaxed text-[var(--color-ink)]">
            {A.handle} and {B.handle} — same operator?
          </p>
          <div className={`mt-2 text-[19px] font-semibold ${verdictTone(v).fg}`}>
            {verdictLabel(v)}
          </div>
          <div className="num mt-1 text-[11.5px] text-[var(--color-ink-soft)]">
            {a.issued ? `log₁₀ LR ${a.log_lr?.toFixed(2)} · ` : ''}k {a.family_count_k} over{' '}
            {a.distinct_independence_keys} capture origin
            {a.distinct_independence_keys === 1 ? '' : 's'}
          </div>
        </Card>

        <Card title="Evidence on this pair">
          <ul className="flex flex-col divide-y divide-[var(--color-hairline)]">
            {a.families.map((f) => (
              <li
                key={f.family}
                className="flex items-center justify-between gap-3 py-2 first:pt-0 last:pb-0"
              >
                <FamilyTag family={f.family as FamilyId} muted={f.capped_log_lr === 0} />
                <span className="num text-[12px] font-semibold">
                  <Lr value={f.capped_log_lr} />
                </span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  )
}
