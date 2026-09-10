import { useState } from 'react'
import type { Assessment, FamilyId } from '../data/model'
import { Card, Chip, FamilyTag, Lr, Button } from '../lib/ui'
import { verdictOf, verdictLabel, verdictTone } from '../lib/engine'

const STAGES = [
  { label: 'Raw evidence', hint: 'What matched, before any score.' },
  { label: 'Counter-evidence', hint: 'What argues against it. Cannot be skipped.' },
  { label: 'Verdict', hint: 'Revealed last, on purpose.' },
]
type Decision = 'ACCEPTED' | 'REJECTED' | 'DEFERRED'

export function Review({ a }: { a: Assessment }) {
  const [stage, setStage] = useState(0)
  const [decision, setDecision] = useState<Decision | null>(null)
  const [rationale, setRationale] = useState('')
  const [signed, setSigned] = useState(false)
  const v = verdictOf(a)
  const tone = verdictTone(v)

  return (
    <div className="mx-auto flex max-w-[660px] flex-col gap-4">
      <div className="num text-[11px] text-[var(--color-ink-faint)]">{a.pair_id}</div>

      <ol className="flex gap-1.5">
        {STAGES.map((s, i) => (
          <li
            key={s.label}
            className={`flex-1 rounded-[var(--r)] border px-3 py-2 ${
              i === stage
                ? 'border-[var(--color-ink)] bg-[var(--color-surface)]'
                : i < stage
                  ? 'border-[var(--color-hairline)] bg-[var(--color-surface)]'
                  : 'border-dashed border-[var(--color-hairline-strong)]'
            }`}
          >
            <div className="flex items-center gap-1.5">
              <span className="num text-[10px] text-[var(--color-ink-faint)]">0{i + 1}</span>
              <span
                className={`text-[12px] font-semibold ${
                  i <= stage ? 'text-[var(--color-ink)]' : 'text-[var(--color-ink-faint)]'
                }`}
              >
                {s.label}
              </span>
            </div>
            <p className="mt-0.5 text-[10px] text-[var(--color-ink-soft)]">{s.hint}</p>
          </li>
        ))}
      </ol>

      {stage === 0 && (
        <Card title="Raw evidence">
          <ul className="flex flex-col divide-y divide-[var(--color-hairline)]">
            {a.families.map((f) => (
              <li key={f.family} className="py-2.5 first:pt-0 last:pb-0">
                <div className="flex items-center justify-between">
                  <FamilyTag family={f.family as FamilyId} muted={f.capped_log_lr === 0} />
                  <span className="num text-[12px] font-semibold">
                    <Lr value={f.capped_log_lr} />
                  </span>
                </div>
                <p className="mt-0.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                  {f.discount_reason}
                </p>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {stage === 1 && (
        <Card title="Counter-evidence">
          {a.counter_evidence.length === 0 ? (
            <p className="text-[12px] text-[var(--color-ink-soft)]">No detector fired on this pair.</p>
          ) : (
            <ul className="flex flex-col gap-2.5">
              {a.counter_evidence.map((c, i) => (
                <li key={i} className="border-l-2 border-[var(--color-counter)] pl-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[12px] font-medium text-[var(--color-ink)]">
                      {c.contradiction_class}
                    </span>
                    <Chip tone={c.severity === 'hard' ? 'counter' : 'neutral'}>
                      {c.severity === 'hard' ? 'hard veto' : `−${c.delta.toFixed(2)}`}
                    </Chip>
                  </div>
                  <p className="mt-0.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
                    {c.explanation}
                  </p>
                </li>
              ))}
            </ul>
          )}
          <div className="mt-3.5 rounded-[var(--r)] bg-[var(--color-paper)] px-3 py-2.5 text-[11.5px] leading-relaxed text-[var(--color-ink-soft)]">
            <span className="text-[var(--color-ink)]">Defence hypothesis:</span>{' '}
            {a.defence_hypothesis}
          </div>
        </Card>
      )}

      {stage === 2 && (
        <Card title="Verdict">
          <div className={`text-[25px] font-semibold tracking-[-0.02em] ${tone.fg}`}>
            {verdictLabel(v)}
          </div>
          <div className="num mt-1 text-[12px] text-[var(--color-ink-soft)]">
            {a.issued
              ? `log₁₀ LR ${a.log_lr?.toFixed(2)} · k ${a.family_count_k} · params ${a.params_version}`
              : a.refusal_reason}
          </div>
          <ul className="mt-2 flex flex-col gap-0.5 text-[11px] text-[var(--color-ink-soft)]">
            {a.limitations.map((l) => (
              <li key={l}>— {l}</li>
            ))}
          </ul>
        </Card>
      )}

      {stage < 2 ? (
        <div className="flex justify-end">
          <Button onClick={() => setStage(stage + 1)}>
            {stage === 0 ? 'Next — counter-evidence' : 'Next — reveal verdict'}
          </Button>
        </div>
      ) : signed ? (
        <Card title="Ledger entry — signed">
          <div className="num text-[12px] leading-relaxed text-[var(--color-ink)]">
            <div>assessment · {a.pair_id}</div>
            <div>
              decision ·{' '}
              <span
                className={
                  decision === 'ACCEPTED'
                    ? 'text-[var(--color-support)]'
                    : decision === 'REJECTED'
                      ? 'text-[var(--color-counter)]'
                      : 'text-[var(--color-ink-soft)]'
                }
              >
                {decision}
              </span>
            </div>
            <div>
              at decision · {a.issued ? `${a.verbal_band} (${a.log_lr?.toFixed(2)})` : 'refused'}, k{' '}
              {a.family_count_k}
            </div>
            <div>analyst-04 · sealed and appended, history not overwritten</div>
            <div className="mt-1 whitespace-pre-wrap text-[var(--color-ink-soft)]">
              rationale · {rationale}
            </div>
          </div>
        </Card>
      ) : (
        <Card title="Decision">
          <div className="flex flex-wrap gap-1.5">
            {(['ACCEPTED', 'REJECTED', 'DEFERRED'] as Decision[]).map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => setDecision(d)}
                className={`num rounded-[var(--r)] border px-3 py-1.5 text-[11.5px] uppercase tracking-[0.05em] transition-colors ${
                  decision === d
                    ? 'border-[var(--color-ink)] bg-[var(--color-ink)] text-[var(--color-surface)]'
                    : 'border-[var(--color-hairline-strong)] text-[var(--color-ink-soft)] hover:border-[var(--color-ink-faint)]'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
          <label className="mt-3 flex flex-col gap-1.5">
            <span className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
              Rationale — recorded with your identity
            </span>
            <textarea
              value={rationale}
              onChange={(e) => setRationale(e.target.value)}
              rows={3}
              placeholder="State the basis for the decision."
              className="w-full rounded-[var(--r)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] p-2.5 text-[12.5px] outline-none transition-colors focus:border-[var(--color-accent)]"
            />
          </label>
          <div className="mt-2">
            <Button disabled={!decision || rationale.trim().length < 12} onClick={() => setSigned(true)}>
              Sign and record
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
}
