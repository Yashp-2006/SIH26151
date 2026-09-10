import type { ReactNode } from 'react'
import type { FamilyId } from '../data/model'
import { FAMILY_NAME } from '../data/model'
import { familyColor } from './engine'

export function Chip({
  children,
  tone = 'neutral',
}: {
  children: ReactNode
  tone?: 'neutral' | 'support' | 'counter' | 'flag' | 'accent'
}) {
  const tones: Record<string, string> = {
    neutral: 'bg-[var(--color-paper)] text-[var(--color-ink-soft)] border-[var(--color-hairline-strong)]',
    support: 'bg-[var(--color-support-wash)] text-[var(--color-support)] border-transparent',
    counter: 'bg-[var(--color-counter-wash)] text-[var(--color-counter)] border-transparent',
    flag: 'bg-[var(--color-flag-wash)] text-[var(--color-flag)] border-transparent',
    accent: 'bg-[var(--color-accent-wash)] text-[var(--color-accent)] border-transparent',
  }
  return (
    <span
      className={`num inline-flex items-center gap-1 rounded-[4px] border px-1.5 py-0.5 text-[10.5px] font-medium uppercase tracking-[0.05em] ${tones[tone]}`}
    >
      {children}
    </span>
  )
}

export function FamilyTag({ family, muted = false }: { family: FamilyId; muted?: boolean }) {
  return (
    <span className="inline-flex items-center gap-1.5 whitespace-nowrap">
      <span
        className="inline-block h-2 w-2 rounded-[2px]"
        style={{ background: muted ? 'var(--color-suppressed)' : familyColor(family) }}
        aria-hidden
      />
      <span className="num text-[11px] font-medium text-[var(--color-ink-soft)]">{family}</span>
      <span className="text-[12px] text-[var(--color-ink-faint)]">{FAMILY_NAME[family]}</span>
    </span>
  )
}

export function Lr({ value }: { value: number }) {
  const s = value > 0 ? `+${value.toFixed(2)}` : value.toFixed(2)
  const c =
    value === 0
      ? 'text-[var(--color-suppressed)]'
      : value < 0
        ? 'text-[var(--color-counter)]'
        : 'text-[var(--color-ink)]'
  return <span className={`num ${c}`}>{s}</span>
}

/** small-caps section label used to group content with negative space, not boxes */
export function Label({ children }: { children: ReactNode }) {
  return (
    <div className="text-[10.5px] font-semibold uppercase tracking-[0.09em] text-[var(--color-ink-faint)]">
      {children}
    </div>
  )
}

/** a flat content section separated by a hairline — the default grouping unit */
export function Section({
  title,
  aside,
  children,
}: {
  title: string
  aside?: ReactNode
  children: ReactNode
}) {
  return (
    <section className="border-t border-[var(--color-hairline)] pt-5">
      <div className="mb-3 flex items-baseline justify-between gap-3">
        <Label>{title}</Label>
        {aside && <div className="num text-[11px] text-[var(--color-ink-faint)]">{aside}</div>}
      </div>
      {children}
    </section>
  )
}

/** an elevated card — used only where elevation communicates hierarchy */
export function Card({
  title,
  aside,
  children,
  accent = false,
}: {
  title?: string
  aside?: ReactNode
  children: ReactNode
  accent?: boolean
}) {
  return (
    <section
      className={`rounded-[var(--r-lg)] border bg-[var(--color-surface)] ${
        accent ? 'border-[var(--color-hairline-strong)]' : 'border-[var(--color-hairline)]'
      }`}
    >
      {title && (
        <header className="flex items-baseline justify-between gap-3 border-b border-[var(--color-hairline)] px-4 py-2.5">
          <h2 className="text-[13px] font-semibold text-[var(--color-ink)]">{title}</h2>
          {aside && <div className="num text-[11px] text-[var(--color-ink-faint)]">{aside}</div>}
        </header>
      )}
      <div className="p-4">{children}</div>
    </section>
  )
}

/** primary / secondary button with tactile feedback */
export function Button({
  children,
  onClick,
  variant = 'primary',
  type = 'button',
  disabled,
}: {
  children: ReactNode
  onClick?: () => void
  variant?: 'primary' | 'ghost'
  type?: 'button' | 'submit'
  disabled?: boolean
}) {
  const styles =
    variant === 'primary'
      ? 'bg-[var(--color-ink)] text-[var(--color-surface)] hover:bg-[#33322d]'
      : 'border border-[var(--color-hairline-strong)] text-[var(--color-ink)] hover:border-[var(--color-ink-faint)]'
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`rounded-[var(--r)] px-4 py-2 text-[12.5px] font-medium transition-[transform,background-color,border-color] duration-150 active:translate-y-px disabled:opacity-40 disabled:active:translate-y-0 ${styles}`}
    >
      {children}
    </button>
  )
}
