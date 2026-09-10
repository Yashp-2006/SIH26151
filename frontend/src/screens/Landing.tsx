import { ArrowRight } from '../lib/icons'
import { TracePanel } from './landing/TracePanel'
import { Reveal } from './landing/Reveal'

const NAV = [
  { label: 'The problem', href: '#problem' },
  { label: 'How it works', href: '#how' },
  { label: 'Evaluation', href: '#proof' },
]

const PROBLEM = [
  {
    h: 'The same trace, six times',
    p: 'One listing reaches an analyst through five mirrors and counts five times. Confidence inflates without a single new fact.',
  },
  {
    h: 'Common indicators look decisive',
    p: 'A shared escrow address or a market-default PGP key merges hundreds of unrelated vendors into one impossible actor.',
  },
  {
    h: 'One false merge poisons the case',
    p: 'A wrong link becomes a lead, gains apparent corroboration as it is reused, and compounds through every assessment built on it.',
  },
]

const STEPS = [
  {
    h: 'Seal every observation',
    p: 'Captures are hashed and chained at collection. Provenance is established at the moment of contact, never reconstructed afterward.',
  },
  {
    h: 'Weigh, then fuse',
    p: 'Each signal is scored by rarity. Mirrored evidence collapses to one artefact, families are capped, contradictions subtract — into a single likelihood ratio.',
  },
  {
    h: 'A human signs it',
    p: 'The engine argues against its own conclusion before anyone sees a score. An analyst reviews the evidence, then authors the assessment.',
  },
]

const DIFF = [
  {
    h: 'Independence discount',
    p: 'Twenty-three mirrored observations become one, shown as an explicit subtraction on the ledger.',
  },
  {
    h: 'Counter-evidence engine',
    p: 'Detectors look for reasons the link is wrong. When none fire, the silence is shown — not hidden.',
  },
  {
    h: 'Hard k ≥ 2 gate',
    p: 'Support from a single family is refused outright. One hundred percent of planted single-vector decoys rejected.',
  },
  {
    h: 'A likelihood ratio, never a percentage',
    p: 'Every assessment carries a verbal band and the defence hypothesis it was tested against.',
  },
]

function Nav({ onEnter }: { onEnter: () => void }) {
  return (
    <header className="fixed inset-x-0 top-0 z-30 border-b border-[var(--color-hairline)] bg-[var(--color-surface)]/92 backdrop-blur">
      <div className="mx-auto flex max-w-[1240px] items-center justify-between px-6 py-3.5">
        <span className="text-[15px] font-semibold tracking-[0.18em] text-[var(--color-ink)]">
          PRAMANA
        </span>
        <nav className="hidden gap-7 md:flex">
          {NAV.map((n) => (
            <a
              key={n.href}
              href={n.href}
              className="text-[12.5px] font-medium text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink)]"
            >
              {n.label}
            </a>
          ))}
        </nav>
        <button
          type="button"
          onClick={onEnter}
          className="rounded-[var(--r)] bg-[var(--color-ink)] px-3.5 py-1.5 text-[12.5px] font-medium text-[var(--color-surface)] transition-transform active:translate-y-px"
        >
          Open console
        </button>
      </div>
    </header>
  )
}

export function Landing({ onEnter }: { onEnter: () => void }) {
  const head = 'Attribution is an evidence problem'.split(' ')

  return (
    <div className="min-h-[100dvh] bg-[var(--color-surface)]">
      <Nav onEnter={onEnter} />

      {/* hero — split, full-bleed dark panel right */}
      <section className="grid lg:min-h-[100dvh] lg:grid-cols-[1.02fr_0.98fr]">
        <div className="flex flex-col justify-center px-6 pb-14 pt-24 sm:px-10 lg:px-14 lg:pt-28">
          <h1 className="display words max-w-[15ch] text-[clamp(2.6rem,6.4vw,5.1rem)] text-[var(--color-ink)]">
            {head.map((w, i) => (
              <span key={i}>
                <span className="inline-block" style={{ '--w': i } as React.CSSProperties}>
                  {w === 'evidence' ? (
                    <span className="relative">
                      evidence
                      <svg
                        className="brush absolute -bottom-1.5 left-0 w-full"
                        height="16"
                        viewBox="0 0 300 16"
                        preserveAspectRatio="none"
                        aria-hidden
                      >
                        <path
                          d="M3 10C52 4 132 3 192 6c40 2 78 4 105 2"
                          fill="none"
                          stroke="#c9532f"
                          strokeWidth="4"
                          strokeLinecap="round"
                        />
                      </svg>
                    </span>
                  ) : (
                    w
                  )}
                  {i === head.length - 1 ? '.' : ''}
                </span>
                {i < head.length - 1 ? ' ' : ''}
              </span>
            ))}
          </h1>

          <p className="mt-7 max-w-[46ch] text-[15px] leading-relaxed text-[var(--color-ink-soft)] rise-late">
            PRAMANA turns fragmented dark-web traces into sealed, independence-weighted evidence —
            and a calibrated, contestable link an investigator can defend line by line.
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-x-6 gap-y-3 rise-later">
            <button
              type="button"
              onClick={onEnter}
              className="group flex items-center gap-2 rounded-[var(--r)] bg-[var(--color-accent)] px-5 py-2.5 text-[13.5px] font-medium text-white transition-transform active:translate-y-px"
            >
              Open the console
              <ArrowRight className="transition-transform duration-200 group-hover:translate-x-0.5" />
            </button>
            <a
              href="#problem"
              className="text-[13px] font-medium text-[var(--color-ink-soft)] underline decoration-[var(--color-hairline-strong)] underline-offset-4 transition-colors hover:decoration-[var(--color-ink)]"
            >
              Why attribution fails
            </a>
          </div>

          <div className="mt-12 flex items-center gap-2 text-[11px] text-[var(--color-ink-faint)]">
            <span className="inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-[var(--color-support)]" />
            <span className="num">SIH 2026 · Problem Statement 26151 · NTRO</span>
          </div>
        </div>

        <TracePanel />
      </section>

      {/* problem */}
      <section id="problem" className="border-t border-[var(--color-hairline)] bg-[var(--color-paper)]">
        <div className="mx-auto max-w-[1080px] px-6 py-20 sm:px-10 lg:px-14">
          <Reveal>
            <p className="display max-w-[16ch] text-[clamp(1.8rem,3.4vw,2.7rem)] text-[var(--color-ink)]">
              Not a shortage of data. A failure of evidential arithmetic.
            </p>
          </Reveal>
          <ol className="mt-12 flex flex-col divide-y divide-[var(--color-hairline-strong)]">
            {PROBLEM.map((c, i) => (
              <Reveal as="li" key={c.h} delay={i * 70} className="grid gap-2 py-7 sm:grid-cols-[0.9fr_1.6fr] sm:gap-10">
                <h3 className="text-[17px] font-semibold text-[var(--color-ink)]">{c.h}</h3>
                <p className="max-w-[56ch] text-[13.5px] leading-relaxed text-[var(--color-ink-soft)]">
                  {c.p}
                </p>
              </Reveal>
            ))}
          </ol>
        </div>
      </section>

      {/* how it works */}
      <section id="how" className="border-t border-[var(--color-hairline)]">
        <div className="mx-auto max-w-[1080px] px-6 py-20 sm:px-10 lg:px-14">
          <Reveal>
            <h2 className="display text-[clamp(1.8rem,3.4vw,2.7rem)] text-[var(--color-ink)]">
              How it works
            </h2>
          </Reveal>
          <div className="mt-12 grid gap-x-10 gap-y-10 md:grid-cols-3">
            {STEPS.map((s, i) => (
              <Reveal key={s.h} delay={i * 80} className="border-t-2 border-[var(--color-ink)] pt-4">
                <h3 className="text-[16px] font-semibold text-[var(--color-ink)]">{s.h}</h3>
                <p className="mt-2 text-[13px] leading-relaxed text-[var(--color-ink-soft)]">{s.p}</p>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* proof / difference */}
      <section id="proof" className="border-t border-[var(--color-hairline)] bg-[var(--color-paper)]">
        <div className="mx-auto max-w-[1080px] px-6 py-20 sm:px-10 lg:px-14">
          <Reveal>
            <h2 className="display text-[clamp(1.8rem,3.4vw,2.7rem)] text-[var(--color-ink)]">
              What no other tool models
            </h2>
          </Reveal>
          <div className="mt-12 grid gap-x-12 gap-y-10 sm:grid-cols-2">
            {DIFF.map((c, i) => (
              <Reveal key={c.h} delay={i * 70} className="border-l border-[var(--color-hairline-strong)] pl-5">
                <h3 className="text-[15px] font-semibold text-[var(--color-ink)]">{c.h}</h3>
                <p className="mt-1.5 max-w-[46ch] text-[13px] leading-relaxed text-[var(--color-ink-soft)]">
                  {c.p}
                </p>
              </Reveal>
            ))}
          </div>
          <Reveal delay={120}>
            <button
              type="button"
              onClick={onEnter}
              className="group mt-14 flex items-center gap-2 rounded-[var(--r)] bg-[var(--color-accent)] px-5 py-2.5 text-[13.5px] font-medium text-white transition-transform active:translate-y-px"
            >
              Open the console
              <ArrowRight className="transition-transform duration-200 group-hover:translate-x-0.5" />
            </button>
          </Reveal>
        </div>
      </section>

      <footer className="border-t border-[var(--color-hairline)]">
        <div className="mx-auto flex max-w-[1080px] flex-col gap-1.5 px-6 py-10 sm:px-10 lg:px-14">
          <span className="display text-[16px] text-[var(--color-ink)]">
            The graph is a view. The ledger is the truth. The human authors the conclusion.
          </span>
          <span className="num text-[11px] text-[var(--color-ink-faint)]">
            PRAMANA — Evidence-Centric Attribution Platform · SIH 2026 · PS 26151 · NTRO
          </span>
        </div>
      </footer>
    </div>
  )
}
