// Presentation helpers over a real PRAMANA Assessment. No scoring happens here —
// the engine already did it. This only shapes numbers for the screens.

import type { Assessment, FamilyId, VerbalBand } from '../data/model'

export type Verdict = 'STRONG' | 'MODERATELY STRONG' | 'MODERATE' | 'LIMITED' | 'REFUSED' | 'EXCLUDED'

export function verdictOf(a: Assessment): Verdict {
  if (a.excluded) return 'EXCLUDED'
  if (!a.issued) return 'REFUSED'
  return (a.verbal_band ?? 'LIMITED') as Verdict
}

export function verdictLabel(v: Verdict): string {
  switch (v) {
    case 'STRONG':
      return 'Strong support'
    case 'MODERATELY STRONG':
      return 'Moderately strong support'
    case 'MODERATE':
      return 'Moderate support'
    case 'LIMITED':
      return 'Limited support'
    case 'REFUSED':
      return 'No assessment issued'
    case 'EXCLUDED':
      return 'Excluded'
  }
}

export function verdictTone(v: Verdict): { fg: string; dot: string } {
  switch (v) {
    case 'STRONG':
    case 'MODERATELY STRONG':
      return { fg: 'text-[var(--color-support)]', dot: 'bg-[var(--color-support)]' }
    case 'MODERATE':
    case 'LIMITED':
      return { fg: 'text-[var(--color-ink)]', dot: 'bg-[var(--color-ink-soft)]' }
    case 'REFUSED':
      return { fg: 'text-[var(--color-flag)]', dot: 'bg-[var(--color-flag)]' }
    case 'EXCLUDED':
      return { fg: 'text-[var(--color-counter)]', dot: 'bg-[var(--color-counter)]' }
  }
}

// desaturated categorical set — no purple, distinct hues
const FAMILY_COLOR: Record<FamilyId, string> = {
  F1: '#2c5578',
  F2: '#7d6544',
  F3: '#97622a',
  F4: '#2f6b45',
  F5: '#6b6674',
  F6: '#8a8578',
  F7: '#2f7d7d',
  F8: '#777770',
  F9: '#4a6b6e',
}
export const familyColor = (f: FamilyId) => FAMILY_COLOR[f]

export function bandName(b: VerbalBand | string | null): string {
  if (!b) return '—'
  return b.charAt(0) + b.slice(1).toLowerCase()
}

// ---- waterfall: naive accumulation → grouping/hub → caps → counter → total --

export interface WaterfallStep {
  label: string
  kind: 'add' | 'subtract' | 'clip' | 'total'
  delta: number
  running: number
  note?: string
}

/** Parse a naive detail line: "F5 image_id=img_11 x4 -> +3.20" */
function parseNaive(line: string): { family: string; label: string; value: number } | null {
  const m = line.match(/^(F\d)\s+([^\s]+)\s+x(\d+)\s+->\s+([+-]?[\d.]+)/)
  if (!m) return null
  return { family: m[1], label: `${m[1]} ${m[2].split('=')[0]} ×${m[3]}`, value: parseFloat(m[4]) }
}

export function buildWaterfall(a: Assessment): {
  steps: WaterfallStep[]
  naiveTotal: number
  groupedTotal: number
  finalTotal: number
} {
  const steps: WaterfallStep[] = []
  let running = 0

  const naiveItems = a.naive_baseline.detail.map(parseNaive).filter(Boolean) as {
    family: string
    label: string
    value: number
  }[]
  const naiveTotal = naiveItems.reduce((s, x) => s + x.value, 0)

  for (const it of naiveItems) {
    running += it.value
    steps.push({ label: it.label, kind: 'add', delta: it.value, running: round(running) })
  }

  const groupedTotal = a.families.reduce((s, f) => s + f.capped_log_lr, 0)
  const groupingDelta = round(groupedTotal - naiveTotal)
  if (groupingDelta < 0) {
    running += groupingDelta
    const hub = a.families.filter((f) => f.discount_reason.includes('hub')).length
    const collapse = a.families.filter((f) => f.discount_reason.includes('collapsed')).length
    const bits: string[] = []
    if (collapse) bits.push(`${collapse} mirror group${collapse > 1 ? 's' : ''} collapsed`)
    if (hub) bits.push(`${hub} hub indicator${hub > 1 ? 's' : ''} zeroed`)
    steps.push({
      label: 'Independence grouping + hub suppression',
      kind: 'subtract',
      delta: groupingDelta,
      running: round(running),
      note: bits.join(' · ') || undefined,
    })
  }

  const counterDelta = -a.counter_evidence.reduce((s, c) => s + c.delta, 0)
  if (counterDelta < 0) {
    running += counterDelta
    steps.push({
      label: 'Counter-evidence',
      kind: 'subtract',
      delta: round(counterDelta),
      running: round(running),
    })
  }

  const finalTotal = a.issued ? (a.log_lr ?? 0) : 0
  if (a.issued && Math.abs(running - finalTotal) > 0.01) {
    const clip = round(finalTotal - running)
    running = finalTotal
    steps.push({
      label: `Global ceiling (≤ 4.0)`,
      kind: 'clip',
      delta: clip,
      running: round(running),
    })
  }

  steps.push({
    label: a.issued ? 'Fused log₁₀ LR' : 'Refused — k < 2',
    kind: 'total',
    delta: 0,
    running: a.issued ? finalTotal : 0,
  })

  return { steps, naiveTotal: round(naiveTotal), groupedTotal: round(groupedTotal), finalTotal }
}

function round(n: number): number {
  return Math.round(n * 1000) / 1000
}
