// Types mirroring the PRAMANA engine (ai-ml/pramana/schema.py). The backend and
// the bundled snapshot both return exactly this shape.

export type FamilyId = 'F1' | 'F2' | 'F3' | 'F4' | 'F5' | 'F6' | 'F7' | 'F8' | 'F9'

export const FAMILY_NAME: Record<FamilyId, string> = {
  F1: 'Cryptographic',
  F2: 'Financial',
  F3: 'Infrastructure',
  F4: 'Contact',
  F5: 'Content artefacts',
  F6: 'Linguistic',
  F7: 'Behavioural',
  F8: 'Social',
  F9: 'External',
}

export type VerbalBand = 'LIMITED' | 'MODERATE' | 'MODERATELY STRONG' | 'STRONG'

export interface FamilyResult {
  family: FamilyId
  raw_log_lr: number
  damped_log_lr: number
  capped_log_lr: number
  n_groups: number
  discount_reason: string
}

export interface CounterEvidence {
  contradiction_class: string
  severity: 'soft' | 'hard'
  delta: number
  explanation: string
}

export interface NaiveBaseline {
  log_lr: number
  verbal_band: string
  merged: boolean
  detail: string[]
}

export interface Assessment {
  pair_id: string
  account_a: string
  account_b: string
  issued: boolean
  excluded: boolean
  log_lr: number | null
  verbal_band: VerbalBand | null
  family_count_k: number
  distinct_independence_keys: number
  families: FamilyResult[]
  counter_evidence: CounterEvidence[]
  defence_hypothesis: string
  limitations: string[]
  refusal_reason: string
  params_version: string
  naive_baseline: NaiveBaseline
}

export interface AccountBrief {
  account_id: string
  handle: string
  market: string
  pgp_fp: string
  contact_id: string
  asn: string
  template_id: string
  listings: number
  operator_id?: string
}

export interface PairRow {
  pair_id: string
  account_a: string
  account_b: string
  is_same_operator: boolean
  note: string
}

export interface Health {
  params_version: string
  reference_population: string
  lambda: number
  tau: number
  k_min: number
  ceiling: number
  caps: Record<FamilyId, number>
  merge_threshold: number
}

export interface MetricRow {
  false_merge_rate: number
  false_merges: number
  precision: number
  recall: number
  f1: number
  true_merges: number
  missed_links: number
}

export interface Metrics {
  corpus: {
    pairs: number
    operators: number
    positives: number
    decoys: number
    refused_k_lt_2: number
  }
  naive: MetricRow
  no_grouping: MetricRow
  pramana: MetricRow
}

export interface DemoCase {
  pair_id: string
  account_a: string
  account_b: string
  kind: string
  caption: string
  detail_a: AccountBrief
  detail_b: AccountBrief
  operator_a?: string
  operator_b?: string
  assessment?: Assessment
}

export interface Snapshot {
  generated_from: string
  health: Health
  metrics: Metrics
  accounts: AccountBrief[]
  pairs: PairRow[]
  assessments: Record<string, Assessment>
  demo_cases: DemoCase[]
}
