import type { Assessment } from '../data/model'
import { useApp } from '../data/store'
import { verdictOf, verdictLabel, verdictTone } from '../lib/engine'
import { Check, Minus } from '../lib/icons'

function Gate({ ok, label, detail }: { ok: boolean; label: string; detail: string }) {
  return (
    <div className="flex items-start gap-2">
      <span
        className={`mt-[1px] grid h-4 w-4 shrink-0 place-items-center rounded-full ${
          ok
            ? 'bg-[var(--color-support-wash)] text-[var(--color-support)]'
            : 'bg-[var(--color-counter-wash)] text-[var(--color-counter)]'
        }`}
      >
        {ok ? <Check size={11} /> : <Minus size={11} />}
      </span>
      <div>
        <div className="text-[12px] font-medium text-[var(--color-ink)]">{label}</div>
        <div className="text-[11px] text-[var(--color-ink-soft)]">{detail}</div>
      </div>
    </div>
  )
}

export function Verdict({ a }: { a: Assessment }) {
  const { snapshot } = useApp()
  const h = snapshot.health
  const v = verdictOf(a)
  const tone = verdictTone(v)
  const refused = v === 'REFUSED' || v === 'EXCLUDED'

  return (
    <section className="rounded-[var(--r-lg)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] p-6">
      <div className="grid gap-6 md:grid-cols-[1.1fr_1fr] md:gap-10">
        <div>
          <div className="text-[10.5px] font-semibold uppercase tracking-[0.08em] text-[var(--color-ink-faint)]">
            Same-operator assessment
          </div>
          <div className={`mt-1.5 text-[29px] font-semibold leading-[1.1] tracking-[-0.02em] ${tone.fg}`}>
            {verdictLabel(v)}
          </div>

          {refused ? (
            <p className="mt-2 max-w-[44ch] text-[12.5px] leading-relaxed text-[var(--color-ink-soft)]">
              {a.refusal_reason || 'A hard contradiction fired — no numeric score is emitted.'}
            </p>
          ) : (
            <div className="mt-4 flex flex-wrap gap-x-8 gap-y-2">
              <div>
                <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                  log₁₀ LR
                </div>
                <div className="num mt-0.5 text-[20px] font-semibold text-[var(--color-ink)]">
                  {a.log_lr?.toFixed(2)}
                  <span className="ml-1 text-[11px] font-normal text-[var(--color-ink-faint)]">
                    / {h.ceiling.toFixed(1)} ceiling
                  </span>
                </div>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-[0.06em] text-[var(--color-ink-faint)]">
                  k · independent families
                </div>
                <div className="num mt-0.5 text-[20px] font-semibold text-[var(--color-ink)]">
                  {a.family_count_k}
                  <span className="ml-1 text-[11px] font-normal text-[var(--color-ink-faint)]">
                    / {h.k_min} floor
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="md:border-l md:border-[var(--color-hairline)] md:pl-10">
          <div className="text-[10px] font-semibold uppercase tracking-[0.08em] text-[var(--color-ink-faint)]">
            Gates
          </div>
          <div className="mt-2.5 grid gap-2.5">
            <Gate
              ok={a.family_count_k >= h.k_min}
              label={`k ≥ ${h.k_min} independent origins`}
              detail={
                a.family_count_k >= h.k_min
                  ? `${a.family_count_k} families over ${a.distinct_independence_keys} capture origins`
                  : `only ${a.family_count_k} — refused`
              }
            />
            <Gate
              ok
              label={`Global ceiling ≤ ${h.ceiling.toFixed(1)}`}
              detail={a.issued && (a.log_lr ?? 0) >= h.ceiling ? 'applied' : 'not reached'}
            />
            <Gate
              ok={!a.excluded}
              label="Must-not-link veto"
              detail={a.excluded ? 'hard contradiction' : 'none fired'}
            />
          </div>
        </div>
      </div>
    </section>
  )
}
