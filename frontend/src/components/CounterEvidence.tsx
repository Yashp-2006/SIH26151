import type { Assessment } from '../data/model'
import { Section, Chip } from '../lib/ui'

const CLASS_LABEL: Record<string, string> = {
  contradictory_identifiers: 'Contradictory identifiers',
  shared_ecosystem_not_shared_control: 'Shared ecosystem, not shared control',
}

export function CounterAndAssessment({ a }: { a: Assessment }) {
  return (
    <Section title="Counter-evidence & limitations">
      {a.counter_evidence.length === 0 ? (
        <p className="text-[12px] text-[var(--color-ink-soft)]">
          No contradiction detector fired on this pair.
        </p>
      ) : (
        <ul className="flex flex-col gap-3">
          {a.counter_evidence.map((c, i) => (
            <li key={i} className="border-l-2 border-[var(--color-counter)] pl-3">
              <div className="flex items-center gap-2">
                <span className="text-[12.5px] font-medium text-[var(--color-ink)]">
                  {CLASS_LABEL[c.contradiction_class] ?? c.contradiction_class}
                </span>
                <Chip tone={c.severity === 'hard' ? 'counter' : 'neutral'}>
                  {c.severity === 'hard' ? 'hard veto' : `−${c.delta.toFixed(2)}`}
                </Chip>
              </div>
              <p className="mt-0.5 max-w-[70ch] text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                {c.explanation}
              </p>
            </li>
          ))}
        </ul>
      )}

      <div className="mt-5 grid gap-4 sm:grid-cols-[0.9fr_1.1fr]">
        <div>
          <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
            Defence hypothesis tested against
          </div>
          <p className="mt-1 text-[12px] leading-relaxed text-[var(--color-ink-soft)]">
            {a.defence_hypothesis}
          </p>
        </div>
        <div>
          <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
            Limitations
          </div>
          <ul className="mt-1 flex flex-col gap-0.5">
            {a.limitations.map((l) => (
              <li key={l} className="flex gap-1.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                <span className="text-[var(--color-ink-faint)]">—</span>
                {l}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </Section>
  )
}
