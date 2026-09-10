/**
 * pramana-workers — 6 routes porting Group A/B/C Python functions.
 * Routes: /extract /rarity /wallet /temporal /infra /template
 */

export default {
  async fetch(request: Request): Promise<Response> {
    const { pathname } = new URL(request.url);

    // Health check — GET only, no auth, for warmup pings
    if (pathname === "/health") {
      return json({ status: "ok" });
    }

    if (request.method !== "POST") {
      return apiError("METHOD_NOT_ALLOWED", "POST required", 405);
    }

    let body: unknown;
    try {
      body = await request.json();
    } catch {
      return apiError("INVALID_JSON", "Request body must be valid JSON", 400);
    }

    if (typeof body !== "object" || body === null || Array.isArray(body)) {
      return apiError("INVALID_BODY", "Request body must be a JSON object", 400);
    }

    switch (pathname) {
      case "/extract":  return handleExtract(body);
      case "/rarity":   return handleRarity(body);
      case "/wallet":   return handleWallet(body);
      case "/temporal": return handleTemporal(body);
      case "/infra":    return handleInfra(body);
      case "/template": return handleTemplate(body);
      case "/assess":   return handleAssess(body);
      default:          return apiError("NOT_FOUND", `No route at ${pathname}`, 404);
    }
  },
} satisfies ExportedHandler;

// ── helpers ──────────────────────────────────────────────────────────────────

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

/** Consistent structured error shape for all failure responses. */
function apiError(code: string, message: string, status: number): Response {
  return json({ error: { code, message } }, status);
}

// ── /extract — port of extractors.py ─────────────────────────────────────────

const RE_BTC_LEGACY = /\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b/g;
const RE_BTC_BECH32 = /\bbc1[a-z0-9]{25,90}\b/g;
const RE_PGP_START  = /-----BEGIN PGP PUBLIC KEY BLOCK-----/g;
const RE_PGP_END    = /-----END PGP PUBLIC KEY BLOCK-----/g;
const RE_ONION_V3   = /\b[a-z2-7]{56}\.onion\b/g;
const RE_EMAIL      = /\b[\w.+-]+@[\w.-]+\.\w{2,}\b/g;
const RE_JABBER     = /\b[\w.+-]+@(?:jabber|xmpp)\.[\w.-]+\.\w{2,}\b/gi;
const RE_TELEGRAM   = /(?:t\.me|telegram\.me)\/[\w]{5,}/g;

type Indicator = { type: string; value: string };

function handleExtract(body: unknown): Response {
  const { text } = body as { text?: string };
  if (typeof text !== "string") return apiError("MISSING_FIELD", "text (string) required", 400);

  const results: Indicator[] = [];
  for (const m of text.matchAll(RE_BTC_LEGACY))  results.push({ type: "btc_legacy",    value: m[0] });
  for (const m of text.matchAll(RE_BTC_BECH32))  results.push({ type: "btc_bech32",    value: m[0] });
  for (const m of text.matchAll(RE_PGP_START))   results.push({ type: "pgp_block_start", value: m[0] });
  for (const m of text.matchAll(RE_PGP_END))     results.push({ type: "pgp_block_end",   value: m[0] });
  for (const m of text.matchAll(RE_ONION_V3))    results.push({ type: "onion_v3",       value: m[0] });

  const jabberHits = new Set<string>();
  for (const m of text.matchAll(RE_JABBER)) {
    results.push({ type: "jabber", value: m[0] });
    jabberHits.add(m[0]);
  }
  for (const m of text.matchAll(RE_EMAIL)) {
    if (!jabberHits.has(m[0])) results.push({ type: "email", value: m[0] });
  }
  for (const m of text.matchAll(RE_TELEGRAM)) results.push({ type: "telegram", value: m[0] });

  return json({ indicators: results });
}

// ── /rarity — port of rarity.py ──────────────────────────────────────────────

const HUB_THRESHOLD = 12;

function handleRarity(body: unknown): Response {
  const { indicator, corpus_counts } = body as {
    indicator?: string;
    corpus_counts?: Record<string, number>;
  };
  if (typeof indicator !== "string" || typeof corpus_counts !== "object" || corpus_counts === null) {
    return apiError("MISSING_FIELD", "indicator (string) and corpus_counts (object) required", 400);
  }

  const count = corpus_counts[indicator] ?? 0;
  const is_hub = count > HUB_THRESHOLD;

  // Unseen indicator → maximum rarity; rarity_score omitted (callers check is_seen: false)
  if (count === 0) {
    return json({ is_seen: false, rarity_score: null, is_hub: false });
  }

  const n = Object.values(corpus_counts).reduce((a, b) => a + b, 0) || 1;
  const rarity_score = Math.log(n / count);
  return json({ is_seen: true, rarity_score, is_hub });
}

// ── /wallet — port of wallet_cluster.py (cluster_wallets + lookup_risk) ──────

interface Tx { txid?: string; inputs?: string[]; outputs?: string[] }

function handleWallet(body: unknown): Response {
  const { transactions, address, risk_labels } = body as {
    transactions?: Tx[];
    address?: string;
    risk_labels?: Record<string, string>;  // caller supplies label map (CSV not available in Worker)
  };

  if (!Array.isArray(transactions)) {
    return apiError("MISSING_FIELD", "transactions (array) required", 400);
  }

  // cluster_wallets: same-tx multi-input co-spend heuristic
  const clusters: Record<string, string> = {};
  for (const tx of transactions) {
    const inputs = tx.inputs ?? [];
    if (inputs.length > 1) {
      const existing = inputs.find(a => clusters[a]);
      const target = existing ? clusters[existing] : inputs[0];
      for (const addr of inputs) clusters[addr] = target;
    }
  }
  // path compression
  for (const k of Object.keys(clusters)) {
    let v = clusters[k];
    while (clusters[v] && clusters[v] !== v) v = clusters[v];
    clusters[k] = v;
  }

  // lookup_risk: use caller-supplied label map; default "unknown"
  const risk_label = address
    ? (risk_labels?.[address] ?? "unknown")
    : "unknown";

  return json({ clusters, risk_label });
}

// ── /temporal — port of temporal.py ──────────────────────────────────────────

function handleTemporal(body: unknown): Response {
  const { events_a, events_b, window_days } = body as {
    events_a?: string[];
    events_b?: string[];
    window_days?: number;
  };

  if (!Array.isArray(events_a) || !Array.isArray(events_b) || typeof window_days !== "number") {
    return apiError("MISSING_FIELD", "events_a (string[]), events_b (string[]), window_days (number) required", 400);
  }
  if (events_a.length === 0 || events_b.length === 0) {
    return json({ overlap_ratio: 0.0 });
  }

  const windowMs = window_days * 24 * 60 * 60 * 1000;
  const tsA = events_a.map(e => new Date(e).getTime());
  const tsB = events_b.map(e => new Date(e).getTime());

  let overlaps = 0;
  for (const tA of tsA) {
    if (tsB.some(tB => Math.abs(tB - tA) <= windowMs)) overlaps++;
  }

  return json({ overlap_ratio: overlaps / tsA.length });
}

// ── /infra — port of infra_fp.py ─────────────────────────────────────────────

function handleInfra(body: unknown): Response {
  const { metadata } = body as {
    metadata?: {
      tls?: { subject?: string; san?: string[] };
      favicon_hash?: string;
      headers?: Record<string, string>;
    };
  };
  if (typeof metadata !== "object" || metadata === null) {
    return apiError("MISSING_FIELD", "metadata (object) required", 400);
  }

  return json({
    tls_subject:  metadata.tls?.subject  ?? "",
    tls_san:      metadata.tls?.san      ?? [],
    favicon_hash: metadata.favicon_hash  ?? "",
    headers:      metadata.headers       ?? {},
  });
}

// ── /template — port of template_fp.py ───────────────────────────────────────

async function handleTemplate(body: unknown): Promise<Response> {
  const { text } = body as { text?: string };
  if (typeof text !== "string") return apiError("MISSING_FIELD", "text (string) required", 400);
  if (!text) return json({ fingerprint: "" });

  const lines = text.split("\n");

  // Heading sequence
  const headings: string[] = [];
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (line.endsWith(":") || line.startsWith("#")) {
      headings.push(line.includes(":") ? line.split(":")[0] : line.split(/\s+/)[0]);
    }
  }

  // Price-decimal pattern
  const hasPrices = /(\$|BTC|XMR)?\s*\d+\.\d{2,8}\s*(\$|BTC|XMR)?/i.test(text) ? "Y" : "N";

  // Standard fields
  const stdFields = ["item", "price", "contact", "shipping", "refund"];
  const textLower = text.toLowerCase();
  const fieldsPresent = stdFields.filter(f => textLower.includes(`${f}:`));

  const fpRaw = `H:${headings.join("|")}|P:${hasPrices}|F:${fieldsPresent.join("|")}`;

  // SHA-256 via Web Crypto
  const encoded = new TextEncoder().encode(fpRaw);
  const hashBuf = await crypto.subtle.digest("SHA-256", encoded);
  const hashHex = Array.from(new Uint8Array(hashBuf))
    .map(b => b.toString(16).padStart(2, "0"))
    .join("")
    .slice(0, 16);

  return json({ fingerprint: hashHex });
}

// ── /assess — port of score_pramana.py (PRAMANA Fusion Engine) ───────────────

const FUSION_CAPS: Record<string, number> = {
  F1: 4.0, F2: 2.0, F3: 2.5, F4: 3.0, F5: 2.5,
  F6: 1.0, F7: 0.7, F8: 1.0, F9: 3.0,
};

interface FusionObs {
  family: string;
  indicator_type: string;
  indicator_value: string;
  match_type: string;
  independence_key: string;
  similarity?: number;
  n_raw_hits?: number;
}

interface AccountInfo {
  contact_id?: string;
  pgp_fp?: string;
  [key: string]: unknown;
}

function verbalBand(x: number): string {
  if (x >= 3.0) return "STRONG";
  if (x >= 2.0) return "MODERATELY STRONG";
  if (x >= 1.0) return "MODERATE";
  return "LIMITED";
}

function handleAssess(body: unknown): Response {
  const req = body as {
    pair_id?: string;
    account_a?: string;
    account_b?: string;
    observations?: FusionObs[];
    counts?: Record<string, number>;
    total_accounts?: number;
    accounts?: Record<string, AccountInfo>;
    lambda?: number;
    tau?: number;
    k_min?: number;
    ceiling?: number;
  };

  const observations = req.observations;
  if (!Array.isArray(observations)) {
    return apiError("MISSING_FIELD", "observations (array) required", 400);
  }

  const pairId = req.pair_id ?? "unknown__pair";
  const accountA = req.account_a ?? "acc_a";
  const accountB = req.account_b ?? "acc_b";
  const lam = req.lambda ?? 0.2;
  const tau = req.tau ?? 12;
  const kMin = req.k_min ?? 2;
  const ceiling = req.ceiling ?? 4.0;
  const totalN = req.total_accounts ?? 137;
  const counts = req.counts ?? {};
  const accounts = req.accounts ?? {};

  // Rarity weight helper
  function getWeight(itype: string, val: string): { w: number; isHub: boolean; note: string } {
    const key = `${itype}::${val}`;
    const c = counts[key] ?? counts[val] ?? 1;
    if (c > tau) {
      return { w: 0.0, isHub: true, note: `hub: '${val}' seen ${c}x in corpus (tau=${tau}) -> forced to 0` };
    }
    const w = Math.round(Math.log10(totalN / c) * 1000) / 1000;
    return { w, isHub: false, note: `rarity: seen ${c}/${totalN} -> log10(${totalN}/${c})=${w.toFixed(2)}` };
  }

  // Group by family
  const byFamily: Record<string, FusionObs[]> = {};
  for (const o of observations) {
    if (!byFamily[o.family]) byFamily[o.family] = [];
    byFamily[o.family].push(o);
  }

  const familyResults: Array<{
    family: string;
    raw_log_lr: number;
    damped_log_lr: number;
    capped_log_lr: number;
    n_groups: number;
    discount_reason: string;
  }> = [];

  const survivingObs: FusionObs[] = [];

  for (const [fam, obsList] of Object.entries(byFamily)) {
    const groups: Record<string, Array<{ w: number; o: FusionObs }>> = {};
    const notes: string[] = [];

    for (const o of obsList) {
      const { w, isHub, note } = getWeight(o.indicator_type, o.indicator_value);
      if (isHub || w === 0.0) {
        notes.push(note);
        continue;
      }
      survivingObs.push(o);
      const key = o.independence_key;
      if (!groups[key]) groups[key] = [];
      groups[key].push({ w, o });
    }

    if (Object.keys(groups).length === 0) {
      familyResults.push({
        family: fam,
        raw_log_lr: 0.0,
        damped_log_lr: 0.0,
        capped_log_lr: 0.0,
        n_groups: 0,
        discount_reason: notes.join("; ") || "no surviving evidence",
      });
      continue;
    }

    const collapsed: Array<{ bestW: number; key: string; count: number; nRaw: number }> = [];
    for (const [key, items] of Object.entries(groups)) {
      items.sort((a, b) => b.w - a.w);
      const bestW = items[0].w;
      const nRaw = items.reduce((acc, it) => acc + (it.o.n_raw_hits ?? 1), 0);
      collapsed.push({ bestW, key, count: items.length, nRaw });
      if (items.length > 1 || nRaw > 1) {
        notes.push(`${nRaw} raw retrieval(s) / ${items.length} artefact(s) on capture '${key.slice(0, 18)}' collapsed to 1 observation`);
      }
    }

    collapsed.sort((a, b) => b.bestW - a.bestW);
    const raw = collapsed.reduce((sum, c) => sum + c.bestW, 0);

    let damped = 0.0;
    for (let i = 0; i < collapsed.length; i++) {
      const factor = Math.pow(lam, i);
      damped += collapsed[i].bestW * factor;
      if (i > 0) {
        notes.push(`group ${i + 1} ('${collapsed[i].key.slice(0, 18)}') damped by lambda^${i}=${factor.toPrecision(3)}: ${collapsed[i].bestW.toFixed(2)} -> ${(collapsed[i].bestW * factor).toFixed(2)}`);
      }
    }

    const cap = FUSION_CAPS[fam] ?? 3.0;
    const capped = Math.min(damped, cap);
    if (capped < damped) {
      notes.push(`family cap ${cap} applied (${damped.toFixed(2)} -> ${capped.toFixed(2)})`);
    }

    familyResults.push({
      family: fam,
      raw_log_lr: Math.round(raw * 1000) / 1000,
      damped_log_lr: Math.round(damped * 1000) / 1000,
      capped_log_lr: Math.round(capped * 1000) / 1000,
      n_groups: collapsed.length,
      discount_reason: notes.join("; ") || "single independent group",
    });
  }

  // Counter-evidence
  const counterEvidence: Array<{
    contradiction_class: string;
    severity: string;
    delta: number;
    explanation: string;
  }> = [];

  const accA = accounts[accountA];
  const accB = accounts[accountB];
  if (accA && accB) {
    if (
      accA.contact_id &&
      accB.contact_id &&
      accA.contact_id !== accB.contact_id &&
      accA.pgp_fp &&
      accB.pgp_fp &&
      accA.pgp_fp !== accB.pgp_fp &&
      accA.pgp_fp !== "DEFAULT_BLOCK_1" &&
      accB.pgp_fp !== "DEFAULT_BLOCK_1"
    ) {
      counterEvidence.push({
        contradiction_class: "contradictory_identifiers",
        severity: "soft",
        delta: 0.4,
        explanation: "both accounts publish distinct non-default PGP keys and distinct contact identifiers",
      });
    }
  }

  const survivingKeys = new Set(survivingObs.map(o => o.independence_key));
  const survivingFams = new Set(survivingObs.map(o => o.family));
  if (survivingFams.size >= 2 && survivingKeys.size === 1) {
    counterEvidence.push({
      contradiction_class: "shared_ecosystem_not_shared_control",
      severity: "soft",
      delta: 0.0,
      explanation: `all surviving evidence across ${survivingFams.size} families traces to a single capture origin (${Array.from(survivingKeys)[0].slice(0, 20)}) - the apparent link is explained by common site configuration`,
    });
  }

  const live = familyResults.filter(r => r.capped_log_lr > 0);
  const kFamilies = live.length;
  const distinctKeys = survivingKeys.size;
  const kEffective = Math.min(kFamilies, distinctKeys);

  const baseAssessment = {
    pair_id: pairId,
    account_a: accountA,
    account_b: accountB,
    issued: false,
    excluded: false,
    log_lr: null as number | null,
    verbal_band: null as string | null,
    family_count_k: kEffective,
    distinct_independence_keys: distinctKeys,
    families: familyResults,
    counter_evidence: counterEvidence,
    defence_hypothesis: "the identities are controlled by different actors and share a marketplace ecosystem",
    limitations: [
      "synthetic corpus (RANGE-SIM v0.1)",
      `lambda=${lam}, tau=${tau}, and family caps are asserted design priors, not fitted`,
      "no real-world identity claim is made",
    ],
    refusal_reason: "",
    params_version: "v0.1",
  };

  const hard = counterEvidence.filter(c => c.severity === "hard");
  if (hard.length > 0) {
    baseAssessment.excluded = true;
    baseAssessment.refusal_reason = `hard must-not-link: ${hard[0].contradiction_class}`;
    return json(baseAssessment);
  }

  let totalScore = familyResults.reduce((sum, r) => sum + r.capped_log_lr, 0);
  totalScore -= counterEvidence.reduce((sum, c) => sum + c.delta, 0);

  if (kEffective < kMin) {
    baseAssessment.refusal_reason = `k=${kEffective} independent origins < k_min=${kMin} (${kFamilies} families over ${distinctKeys} capture origin(s))`;
    return json(baseAssessment);
  }

  const finalScore = Math.max(0.0, Math.min(totalScore, ceiling));
  baseAssessment.issued = true;
  baseAssessment.log_lr = Math.round(finalScore * 1000) / 1000;
  baseAssessment.verbal_band = verbalBand(finalScore);

  return json(baseAssessment);
}

