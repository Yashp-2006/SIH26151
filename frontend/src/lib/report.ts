import { jsPDF } from 'jspdf'
import type { Assessment, AccountBrief, Health } from '../data/model'
import { FAMILY_NAME } from '../data/model'
import { verdictOf, verdictLabel } from './engine'

/** Render the Evidence Balance Sheet as a PDF and download it. */
export function downloadReport(a: Assessment, accounts: AccountBrief[], health: Health): void {
  const acc = (id: string) => accounts.find((x) => x.account_id === id)
  const A = acc(a.account_a)
  const B = acc(a.account_b)
  const v = verdictOf(a)

  const doc = new jsPDF({ unit: 'pt', format: 'a4' })
  const M = 54
  const W = doc.internal.pageSize.getWidth()
  let y = M

  const line = (h = 14) => {
    y += h
    if (y > doc.internal.pageSize.getHeight() - M) {
      doc.addPage()
      y = M
    }
  }
  const text = (s: string, opts: { size?: number; bold?: boolean; color?: number[]; x?: number } = {}) => {
    doc.setFont('courier', opts.bold ? 'bold' : 'normal')
    doc.setFontSize(opts.size ?? 9)
    doc.setTextColor(...((opts.color ?? [28, 28, 26]) as [number, number, number]))
    doc.text(s, opts.x ?? M, y)
  }
  const rule = () => {
    doc.setDrawColor(215, 215, 211)
    doc.setLineWidth(0.75)
    doc.line(M, y, W - M, y)
  }
  const wrap = (s: string, indent = 0) => {
    for (const l of doc.splitTextToSize(s, W - 2 * M - indent) as string[]) {
      text(l, { x: M + indent, size: 8.5 })
      line(11)
    }
  }

  text('PRAMANA', { size: 13, bold: true })
  text(new Date().toISOString().slice(0, 19).replace('T', '  '), {
    size: 8,
    color: [140, 140, 132],
    x: W - M - 110,
  })
  line(6)
  text('Evidence Balance Sheet', { size: 10, color: [90, 90, 85] })
  line(10)
  rule()
  line(16)

  text(`assessment   ${a.pair_id}`)
  line()
  text(
    `parameters   ${a.params_version}   lambda ${health.lambda} · tau ${health.tau} · k_min ${health.k_min} · ceiling ${health.ceiling}`,
  )
  line(20)

  text('SUBJECTS', { bold: true, color: [90, 90, 85] })
  line()
  text(A ? `A  ${A.handle}  (${A.market})   ${A.pgp_fp} / ${A.contact_id} / ${A.asn}` : `A  ${a.account_a}`)
  line()
  text(B ? `B  ${B.handle}  (${B.market})   ${B.pgp_fp} / ${B.contact_id} / ${B.asn}` : `B  ${a.account_b}`)
  line(18)

  text('HYPOTHESIS', { bold: true, color: [90, 90, 85] })
  line()
  wrap('The two accounts are operated by the same operator.')
  text('DEFENCE', { bold: true, color: [90, 90, 85] })
  line()
  wrap(a.defence_hypothesis)
  line(6)
  rule()
  line(18)

  const accentColor = a.excluded ? [162, 58, 47] : a.issued ? [47, 107, 69] : [151, 98, 42]
  text(`VERDICT   ${verdictLabel(v).toUpperCase()}`, { bold: true, size: 12, color: accentColor })
  line(15)
  if (a.issued) {
    text(
      `log10 LR ${a.log_lr?.toFixed(3)}   ·   k ${a.family_count_k} over ${a.distinct_independence_keys} capture origin(s)`,
      { color: [90, 90, 85] },
    )
  } else {
    wrap(a.refusal_reason, 0)
  }
  line(18)
  rule()
  line(18)

  text('EVIDENCE BY FAMILY', { bold: true, color: [90, 90, 85] })
  line(15)
  for (const f of a.families) {
    text(
      `${f.family} ${FAMILY_NAME[f.family].padEnd(16)} raw ${f.raw_log_lr.toFixed(2).padStart(6)}   ` +
        `damped ${f.damped_log_lr.toFixed(2).padStart(6)}   capped ${f.capped_log_lr.toFixed(2).padStart(6)}   cap ${health.caps[f.family]}`,
      { bold: true },
    )
    line(12)
    for (const note of f.discount_reason.split('; ')) wrap(`- ${note}`, 16)
    line(4)
  }

  line(6)
  text('NAIVE BASELINE', { bold: true, color: [90, 90, 85] })
  line(13)
  text(`total ${a.naive_baseline.log_lr.toFixed(2)}   ${a.naive_baseline.verbal_band}`)
  line(12)
  for (const d of a.naive_baseline.detail) wrap(`- ${d}`, 16)

  if (a.counter_evidence.length) {
    line(12)
    text('COUNTER-EVIDENCE', { bold: true, color: [90, 90, 85] })
    line(13)
    for (const c of a.counter_evidence) {
      text(`[${c.severity}] ${c.contradiction_class}   ${c.severity === 'hard' ? 'VETO' : `-${c.delta.toFixed(2)}`}`, {
        bold: true,
      })
      line(12)
      wrap(c.explanation, 16)
    }
  }

  line(12)
  text('LIMITATIONS', { bold: true, color: [90, 90, 85] })
  line(13)
  for (const l of a.limitations) wrap(`- ${l}`, 16)

  line(14)
  rule()
  line(14)
  wrap(
    'This is an investigative assessment at pseudonym level. It is not a real-world identity claim and is not evidence of a criminal act.',
  )

  doc.save(`pramana_${a.pair_id}.pdf`)
}
