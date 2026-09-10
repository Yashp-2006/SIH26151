import type { ReactNode } from 'react'
import { useApp } from '../data/store'
import { ArrowRight } from '../lib/icons'

export type View = 'overview' | 'case' | 'workspace' | 'evaluation' | 'review'

const NAV: { id: View; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'case', label: 'Evidence Balance Sheet' },
  { id: 'workspace', label: 'Workspace' },
  { id: 'review', label: 'Assessment & Review' },
  { id: 'evaluation', label: 'Evaluation' },
]

function Glyph() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" aria-hidden>
      <rect x="1" y="1" width="14" height="14" rx="2" fill="var(--color-ink)" />
      <path
        d="M4.5 11.5V4.5h3.2a2 2 0 0 1 0 4H4.5"
        stroke="var(--color-surface)"
        strokeWidth="1.4"
        fill="none"
        strokeLinecap="round"
      />
    </svg>
  )
}

function Download({ size = 14 }: { size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d="M12 3v12m0 0 4-4m-4 4-4-4M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
    </svg>
  )
}

export function Shell({
  view,
  onView,
  onHome,
  title,
  topRight,
  onDownload,
  children,
}: {
  view: View
  onView: (v: View) => void
  onHome: () => void
  title: string
  topRight?: ReactNode
  onDownload?: () => void
  children: ReactNode
}) {
  const { source } = useApp()
  return (
    <div className="flex min-h-[100dvh] flex-col bg-[var(--color-paper)] lg:flex-row">
      {/* mobile top bar */}
      <div className="sticky top-0 z-30 flex items-center gap-3 overflow-x-auto border-b border-[var(--color-hairline)] bg-[var(--color-surface)] px-4 py-2.5 lg:hidden">
        <span className="shrink-0 text-[12px] font-semibold tracking-[0.14em] text-[var(--color-ink)]">
          PRAMANA
        </span>
        <nav className="flex gap-1">
          {NAV.map((n) => (
            <button
              key={n.id}
              type="button"
              onClick={() => onView(n.id)}
              className={`shrink-0 whitespace-nowrap rounded-[var(--r)] px-2 py-1 text-[11.5px] font-medium ${
                view === n.id
                  ? 'bg-[var(--color-accent-wash)] text-[var(--color-accent)]'
                  : 'text-[var(--color-ink-soft)]'
              }`}
            >
              {n.label}
            </button>
          ))}
          <button
            type="button"
            onClick={onHome}
            className="shrink-0 whitespace-nowrap rounded-[var(--r)] px-2 py-1 text-[11.5px] font-medium text-[var(--color-ink-faint)]"
          >
            Home
          </button>
        </nav>
      </div>

      {/* sidebar — sticky, full height */}
      <aside className="sticky top-0 hidden h-[100dvh] w-[210px] shrink-0 flex-col border-r border-[var(--color-hairline)] bg-[var(--color-surface)] lg:flex">
        <div className="flex items-center gap-2 border-b border-[var(--color-hairline)] px-4 py-4">
          <Glyph />
          <div>
            <div className="text-[13px] font-semibold tracking-[0.14em] text-[var(--color-ink)]">
              PRAMANA
            </div>
            <div className="text-[10px] text-[var(--color-ink-faint)]">Attribution console</div>
          </div>
        </div>

        <nav className="flex flex-col py-2">
          {NAV.map((n) => {
            const on = view === n.id
            return (
              <button
                key={n.id}
                type="button"
                onClick={() => onView(n.id)}
                className={`relative px-4 py-2 text-left text-[12.5px] transition-colors ${
                  on
                    ? 'font-semibold text-[var(--color-ink)]'
                    : 'font-medium text-[var(--color-ink-soft)] hover:text-[var(--color-ink)]'
                }`}
              >
                {on && (
                  <span className="absolute inset-y-1 left-0 w-[2px] rounded-full bg-[var(--color-accent)]" />
                )}
                {n.label}
              </button>
            )
          })}
        </nav>

        <div className="mt-auto flex flex-col gap-3 border-t border-[var(--color-hairline)] px-4 py-3">
          <button
            type="button"
            onClick={onHome}
            className="group flex items-center gap-1.5 text-[11.5px] font-medium text-[var(--color-ink-soft)] transition-colors hover:text-[var(--color-ink)]"
          >
            <ArrowRight size={13} className="rotate-180" />
            Back to home
          </button>
          <div>
            <div className="flex items-center gap-1.5 text-[10.5px] text-[var(--color-ink-faint)]">
              <span className="inline-block h-1.5 w-1.5 rounded-full bg-[var(--color-support)]" />
              <span className="num">fusion engine {source === 'service' ? '· gateway' : 'online'}</span>
            </div>
            <div className="num mt-1 text-[10px] text-[var(--color-ink-faint)]">
              params v0.1 · RANGE-SIM
            </div>
          </div>
        </div>
      </aside>

      {/* main */}
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-20 flex items-center justify-between gap-3 border-b border-[var(--color-hairline)] bg-[var(--color-surface)]/95 px-4 py-3 backdrop-blur lg:px-8">
          <h1 className="shrink-0 text-[14px] font-semibold tracking-[-0.01em] text-[var(--color-ink)] lg:text-[15px]">
            {title}
          </h1>
          <div className="flex items-center gap-2">
            {topRight}
            {onDownload && (
              <button
                type="button"
                onClick={onDownload}
                className="flex items-center gap-1.5 rounded-[var(--r)] border border-[var(--color-hairline-strong)] bg-[var(--color-surface)] px-3 py-1.5 text-[12px] font-medium text-[var(--color-ink)] transition-colors hover:border-[var(--color-ink-faint)]"
              >
                <Download /> Download report
              </button>
            )}
          </div>
        </header>
        <main className="min-w-0 flex-1 overflow-x-hidden px-4 py-5 lg:px-8 lg:py-7">
          <div key={view} className="rise mx-auto max-w-[940px]">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
