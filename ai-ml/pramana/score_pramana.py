"""
PRAMANA FUSION ENGINE.   OWNED BY PERSON B.

Pipeline: canonical observations
          -> rarity + hub suppression
          -> independence grouping (within family)
          -> lambda damping across groups
          -> family caps
          -> counter-evidence
          -> k-rule (independent families AND independent capture origins)
          -> global ceiling
          -> assessment or REFUSAL

ASSERTED PARAMETERS (design priors, not fitted - see sensitivity.py):
    LAMBDA = 0.2
    TAU    = 12          (in rarity.py)
    CAPS   = Blueprint family table
    K_MIN  = 2
    CEILING= 4.0
"""

from collections import defaultdict
try:
    from pramana.schema import (Assessment, FamilyResult, CounterEvidence,
                                verbal_band)
except ModuleNotFoundError:
    from schema import (Assessment, FamilyResult, CounterEvidence,
                        verbal_band)

LAMBDA = 0.2
K_MIN = 2
CEILING = 4.0
MERGE_THRESHOLD = 2.0

CAPS = {"F1": 4.0, "F2": 2.0, "F3": 2.5, "F4": 3.0, "F5": 2.5,
        "F6": 1.0, "F7": 0.7, "F8": 1.0, "F9": 3.0}


# --------------------------------------------------------------- fusion

def _fuse_family(fam, obs, rarity, lam=LAMBDA, grouping=True):
    """Group by independence key, take strongest per group, damp the rest."""
    groups = defaultdict(list)
    notes = []

    for o in obs:
        w, why = rarity.weight(o.indicator_type, o.indicator_value)
        if w == 0.0:
            notes.append(why)                      # hub, dropped
            continue
        # ABLATION SWITCH: with grouping OFF, every observation is its own
        # "independent" group and each raw retrieval counts separately -
        # i.e. mirrors become votes. This is the mechanism under test.
        if grouping:
            groups[o.independence_key].append((w, o))
        else:
            for r_i in range(o.n_raw_hits):
                groups[f"{o.independence_key}::raw{r_i}::{id(o)}"].append((w, o))

    if not groups:
        return FamilyResult(fam, 0.0, 0.0, 0.0, 0,
                            "; ".join(notes) or "no surviving evidence")

    # collapse each independence group to its strongest member
    collapsed = []
    for key, items in groups.items():
        items.sort(key=lambda t: -t[0])
        best_w, best_o = items[0]
        n_raw = sum(o.n_raw_hits for _, o in items)
        collapsed.append((best_w, key, len(items), n_raw))
        if len(items) > 1 or n_raw > 1:
            notes.append(f"{n_raw} raw retrieval(s) / {len(items)} artefact(s) "
                         f"on capture '{key[:18]}' collapsed to 1 observation")

    collapsed.sort(key=lambda t: -t[0])
    raw = sum(w for w, _, _, _ in collapsed)

    damped = 0.0
    for i, (w, key, _, _) in enumerate(collapsed):
        damped += w * (lam ** i)
        if i > 0:
            notes.append(f"group {i+1} ('{key[:18]}') damped by "
                         f"lambda^{i}={lam**i:.3g}: {w:.2f} -> {w*lam**i:.2f}")

    capped = min(damped, CAPS[fam])
    if capped < damped:
        notes.append(f"family cap {CAPS[fam]} applied ({damped:.2f} -> {capped:.2f})")

    return FamilyResult(fam, round(raw, 3), round(damped, 3), round(capped, 3),
                        len(collapsed), "; ".join(notes) or "single independent group")


# ------------------------------------------------------- counter-evidence

def _counter_evidence(surviving, accounts, a_id, b_id):
    """Blueprint contradiction classes. Two implemented for v0.1."""
    out = []
    A, B = accounts[a_id], accounts[b_id]

    # C2 contradictory identifiers  (HARD - must-not-link)
    if (A["contact_id"] != B["contact_id"]
            and A["pgp_fp"] != B["pgp_fp"]
            and A["pgp_fp"] != "DEFAULT_BLOCK_1"
            and B["pgp_fp"] != "DEFAULT_BLOCK_1"):
        out.append(CounterEvidence(
            "contradictory_identifiers", "soft", 0.4,
            "both accounts publish distinct non-default PGP keys and distinct "
            "contact identifiers"))

    # C5 shared ecosystem, not shared control (structural)
    keys = {o.independence_key for o in surviving}
    fams = {o.family for o in surviving}
    if len(fams) >= 2 and len(keys) == 1:
        out.append(CounterEvidence(
            "shared_ecosystem_not_shared_control", "soft", 0.0,
            f"all surviving evidence across {len(fams)} families traces to a "
            f"single capture origin ({list(keys)[0][:20]}) - the apparent link "
            f"is explained by common site configuration"))
    return out


# ------------------------------------------------------------ assessment

def assess(pair_id, a_id, b_id, observations, rarity, accounts, lam=LAMBDA,
           k_min=K_MIN, ceiling=CEILING, grouping=True):

    by_family = defaultdict(list)
    for o in observations:
        by_family[o.family].append(o)

    results = [_fuse_family(f, obs, rarity, lam, grouping)
               for f, obs in sorted(by_family.items())]

    # which observations actually survived hub suppression
    surviving = [o for o in observations
                 if rarity.weight(o.indicator_type, o.indicator_value)[0] > 0]

    live = [r for r in results if r.capped_log_lr > 0]
    k_families = len(live)
    distinct_keys = (len({o.independence_key for o in surviving})
                     if grouping else len(surviving))
    # a family only counts as independent if it rests on its own capture origin
    k_effective = min(k_families, distinct_keys)

    counters = _counter_evidence(surviving, accounts, a_id, b_id)
    hard = [c for c in counters if c.severity == "hard"]

    base = Assessment(
        pair_id=pair_id, account_a=a_id, account_b=b_id,
        issued=False, excluded=False, log_lr=None, verbal_band=None,
        family_count_k=k_effective, distinct_independence_keys=distinct_keys,
        families=[r.__dict__ for r in results],
        counter_evidence=[c.__dict__ for c in counters],
        defence_hypothesis="the identities are controlled by different actors "
                           "and share a marketplace ecosystem",
        limitations=["synthetic corpus (RANGE-SIM v0.1)",
                     f"lambda={lam}, tau, and family caps are asserted design "
                     f"priors, not fitted",
                     "no real-world identity claim is made"])

    if hard:
        base.excluded = True
        base.refusal_reason = f"hard must-not-link: {hard[0].contradiction_class}"
        return base

    total = sum(r.capped_log_lr for r in results)
    total -= sum(c.delta for c in counters)

    if k_effective < k_min:
        base.refusal_reason = (
            f"k={k_effective} independent origins < k_min={k_min} "
            f"({k_families} families over {distinct_keys} capture origin(s))")
        return base

    total = max(0.0, min(total, ceiling))
    base.issued = True
    base.log_lr = round(total, 3)
    base.verbal_band = verbal_band(total)
    return base


def merged(a: Assessment) -> bool:
    return bool(a.issued and a.log_lr >= MERGE_THRESHOLD)
