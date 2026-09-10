import type { Assessment } from '../data/model'
import { useApp } from '../data/store'
import { Verdict } from '../components/Verdict'
import { Waterfall } from '../components/Waterfall'
import { EvidenceTable } from '../components/EvidenceTable'
import { CounterAndAssessment } from '../components/CounterEvidence'

function PersonaLine({ a }: { a: Assessment }) {
  const { snapshot } = useApp()
  const acc = (id: string) => snapshot.accounts.find((x) => x.account_id === id)
  const A = acc(a.account_a)
  const B = acc(a.account_b)
  if (!A || !B) return null
  return (
    <div className="mb-5 flex flex-wrap items-baseline gap-x-3 gap-y-1">
      <span className="text-[14px] font-semibold text-[var(--color-ink)]">{A.handle}</span>
      <span className="num text-[11px] text-[var(--color-ink-faint)]">{A.market}</span>
      <span className="text-[var(--color-ink-faint)]">/</span>
      <span className="text-[14px] font-semibold text-[var(--color-ink)]">{B.handle}</span>
      <span className="num text-[11px] text-[var(--color-ink-faint)]">{B.market}</span>
      <span className="num ml-1 text-[10.5px] text-[var(--color-ink-faint)]">{a.pair_id}</span>
    </div>
  )
}

export function Case({ a }: { a: Assessment }) {
  return (
    <div>
      <PersonaLine a={a} />
      <Verdict a={a} />
      <div className="mt-6 flex flex-col gap-6">
        <Waterfall a={a} />
        <EvidenceTable a={a} />
        <CounterAndAssessment a={a} />
      </div>
    </div>
  )
}
