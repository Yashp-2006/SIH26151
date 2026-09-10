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
      const existing = inputs.find(a => clusters[a]) ? clusters[inputs.find(a => clusters[a])!] : inputs[0];
      for (const addr of inputs) clusters[addr] = existing;
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
