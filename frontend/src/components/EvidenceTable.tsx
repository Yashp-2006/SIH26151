import type { Assessment, FamilyId } from '../data/model'
import { useApp } from '../data/store'
import { Section, FamilyTag, Lr } from '../lib/ui'

export function EvidenceTable({ a }: { a: Assessment }) {
  const { snapshot } = useApp()
  const caps = snapshot.health.caps

  return (
    <Section title="Evidence by family" aside={<>{a.families.length} observed</>}>
      <ul className="flex flex-col divide-y divide-[var(--color-hairline)]">
        {a.families.map((f) => {
          const suppressed = f.capped_log_lr === 0
          return (
            <li key={f.family} className="py-3 first:pt-0 last:pb-0">
              <div className="flex items-center justify-between gap-3">
                <FamilyTag family={f.family as FamilyId} muted={suppressed} />
                <div className="flex items-center gap-4">
                  <span className="num text-[10px] text-[var(--color-ink-faint)]">
                    cap {caps[f.family as FamilyId]?.toFixed(1)}
                  </span>
                  <span className="num text-[13px] font-semibold">
                    <Lr value={f.capped_log_lr} />
                  </span>
                </div>
              </div>
              <p className="mt-1 max-w-[70ch] text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                {suppressed && <span className="text-[var(--color-counter)]">contributes 0 — </span>}
                {f.discount_reason}
              </p>
            </li>
          )
        })}
      </ul>
      {a.naive_baseline.detail.length > 0 && (
        <div className="mt-3.5 rounded-[var(--r)] bg-[var(--color-paper)] px-3 py-2.5">
          <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
            What naive scoring counted
          </div>
          <ul className="num mt-1 flex flex-col gap-0.5 text-[11px] text-[var(--color-ink-soft)]">
            {a.naive_baseline.detail.map((d, i) => (
              <li key={i}>{d}</li>
            ))}
          </ul>
        </div>
      )}
    </Section>
  )
}
