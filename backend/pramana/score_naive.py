"""
NAIVE BASELINE - deliberately wrong, on purpose.

This is the conventional correlation tool PRAMANA argues against, and it fails
in exactly the ways the Blueprint's "Conventional failure" column describes:

  * a shared indicator is treated as highly informative regardless of how
    common it is  -> no rarity, no hub suppression
  * five copies of one artefact count as five votes -> no canonicalisation,
    no independence grouping
  * every match is an independent vote -> plain addition
  * no family caps, no k requirement, no counter-evidence, no ceiling

It is a first-class module because without it there is no ablation.
"""

try:
    from pramana.schema import verbal_band
except ModuleNotFoundError:
    from schema import verbal_band

# fixed per-indicator weights, the way a rule-based correlation tool assigns them
NAIVE_WEIGHTS = {
    "pgp_fp":      3.0,    # "a shared PGP key is damning"
    "contact_id":  2.5,
    "asn":         1.0,
    "template_id": 1.0,
    "image_id":    0.8,    # ...per raw retrieval
}

MERGE_THRESHOLD = 2.0      # same threshold both systems are judged at


def score_pair(observations, rarity=None):
    total, lines = 0.0, []
    for o in observations:
        w = NAIVE_WEIGHTS.get(o.indicator_type, 0.5)
        contrib = w * o.n_raw_hits              # NO canonicalisation
        total += contrib                        # NO grouping, NO cap
        lines.append(f"{o.family} {o.indicator_type}={o.indicator_value} "
                     f"x{o.n_raw_hits} -> +{contrib:.2f}")
    return {"log_lr": round(total, 3), "verbal_band": verbal_band(total),
            "merged": total >= MERGE_THRESHOLD, "detail": lines}
