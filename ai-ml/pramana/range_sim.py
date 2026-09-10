#!/usr/bin/env python3
"""
RANGE-SIM  |  PRAMANA Day 1
Generates a synthetic multi-marketplace dark-web corpus with HIDDEN GROUND TRUTH
and deliberately planted traps.

Outputs
-------
  accounts.json    the world the system is allowed to see
  answer_key.csv   the truth  (QUARANTINED - only eval.py may read this)
  pairs.csv        ~500 candidate pairs with known labels

Planted traps
-------------
  T1  hub PGP block      one fingerprint shared by ~40% of ALL accounts
  T2  mirrored artefacts one image replicated across marketplaces, same capture batch
  T3  decoy pairs        cross-operator pairs forced to share template + ASN + hub PGP
  T4  rare contact ID    genuine same-operator signal, appears only 2x in corpus
  T5  compartmented ops  operators that share NOTHING (should be MISSED - honest failure)

Run:  python range_sim.py
"""

import hashlib
import json
import random
import csv
import os
import sys
from pathlib import Path
from itertools import combinations
from collections import Counter

SEED = 26151                      # SIH problem statement number, for luck

N_OPERATORS      = 60
MARKETS          = ["market_alpha", "market_bravo", "market_charlie"]
ASNS             = ["AS14061", "AS16509", "AS24940", "AS63949",
                    "AS20473", "AS51167", "AS200019", "AS9009"]
TEMPLATES        = ["tpl_1", "tpl_2", "tpl_3", "tpl_4", "tpl_5"]

HUB_PGP          = "DEFAULT_BLOCK_1"   # T1: the marketplace default
HUB_PGP_RATE     = 0.40
N_DECOY_PAIRS    = 20                  # T3
N_COMPARTMENTED  = 6
N_HANDOVERS      = 10                  # T6: resold accounts - genuinely hard
TARGET_PAIRS     = 900

HANDLE_STEMS = ["aster","brume","cobalt","dross","ferrous","glaive",
                "hessian","indigo","jarl","krait","larkspur","molybden",
                "nacre","obsidian","porphyry","quartz","rhodium","selenite",
                "tellurite","ultramar","verdigris","wolfram","xenon","yttria",
                "zircon","alnico","bismuth","chert","dolomite","euxenite","nord", "vertex", "kilo", "atlas", "harbour", "onyx", "pallas",
                "quill", "raven", "sable", "tundra", "umbra", "vulpes", "wraith",
                "zephyr", "borealis", "cinder", "delta", "ember", "flint",
                "gale", "hollow", "ibis", "juno", "kestrel", "lumen", "mistral",
                "nadir", "osprey", "petrel"]
HANDLE_SUFFIX = ["_supply", "_official", "_labs", "_depot", "_co", "_direct",
                 "_bulk", "_trade", "_hq", "_store", "01", "_x", "_intl"]

PRODUCTS = ["research chemical 25g", "lab glassware set", "precursor kit",
            "analytical standard 5ml", "reagent pack", "filtration unit",
            "sealed sample vial", "bulk compound 100g", "test kit v3",
            "calibration solution"]


def hexid(n=6, *, rng):
    return "".join(rng.choice("0123456789abcdef") for _ in range(n))


def generate_range(output_dir=".", *, seed=SEED):
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    operators = []
    accounts = []
    handle_pool = HANDLE_STEMS[:]
    rng.shuffle(handle_pool)

    # how many accounts each operator runs (mostly 2, so positives stay scarce)
    for i in range(N_OPERATORS):
        op_id = f"op_{i:02d}"
        n_acc = rng.choices([2, 3, 4], weights=[0.75, 0.15, 0.10])[0]
        compartmented = i < N_COMPARTMENTED          # T5: first few share nothing

        # operator-level signals that SHOULD leak across their accounts
        op_contact = f"05{hexid(4, rng=rng)}"                 # T4: rare contact identifier
        op_template = rng.choice(TEMPLATES)
        op_asn = rng.choice(ASNS)
        op_pgp = f"PGP_{hexid(8, rng=rng).upper()}"
        op_image = f"img_{i:02d}_{hexid(3, rng=rng)}"
        op_infra_batch = f"batch_{hexid(4, rng=rng)}"         # site-config scrape
        op_cat_batch   = f"batch_{hexid(4, rng=rng)}"         # catalogue scrape (DIFFERENT origin)

        operators.append({"operator_id": op_id, "n_accounts": n_acc,
                          "compartmented": compartmented})

        stem = handle_pool[i % len(handle_pool)] + ("" if i < len(handle_pool) else str(i))
        for j in range(n_acc):
            handle = stem + rng.choice(HANDLE_SUFFIX) if j else stem + "_supply"

            if compartmented:
                # T5: disciplined operator - every account looks unrelated
                acct = {
                    "pgp_fp":      HUB_PGP if rng.random() < HUB_PGP_RATE else f"PGP_{hexid(8, rng=rng).upper()}",
                    "contact_id":  f"05{hexid(4, rng=rng)}",
                    "asn":         rng.choice(ASNS),
                    "template_id": rng.choice(TEMPLATES),
                    "infra_batch": f"batch_{hexid(4, rng=rng)}",
                }
                listings = [{"title": rng.choice(PRODUCTS),
                             "price_usd": rng.choice([80, 120, 240, 495, 900]),
                             "image_id": f"img_{hexid(5, rng=rng)}",
                             "capture_batch": f"batch_{hexid(4, rng=rng)}"}
                            for _ in range(rng.randint(3, 5))]
            else:
                # T1: hub PGP may mask the real one
                pgp = HUB_PGP if rng.random() < HUB_PGP_RATE else op_pgp
                acct = {
                    "pgp_fp":      pgp,
                    "contact_id":  op_contact,           # T4: the real signal
                    "asn":         op_asn,
                    "template_id": op_template,
                    "infra_batch": op_infra_batch,       # asn+template from one scrape
                }
                listings = []
                # T2: the operator's signature image, mirrored with the SAME capture batch
                for _ in range(2):
                    listings.append({"title": rng.choice(PRODUCTS),
                                     "price_usd": rng.choice([80, 120, 240, 495, 900]),
                                     "image_id": op_image,
                                     "capture_batch": op_cat_batch})
                for _ in range(rng.randint(1, 3)):
                    listings.append({"title": rng.choice(PRODUCTS),
                                     "price_usd": rng.choice([80, 120, 240, 495, 900]),
                                     "image_id": f"img_{hexid(5, rng=rng)}",
                                     "capture_batch": f"batch_{hexid(4, rng=rng)}"})

            accounts.append({
                "account_id":  f"acc_{len(accounts):03d}",
                "handle":      handle,
                "market":      rng.choice(MARKETS),
                **acct,
                "listings":    listings,
                "_operator":   op_id,          # stripped before writing accounts.json
            })

    # ------------------------------------------------- T3: plant the decoy pairs

    decoy_pairs = []
    tries = 0
    while len(decoy_pairs) < N_DECOY_PAIRS and tries < 2000:
        tries += 1
        a, b = rng.sample(accounts, 2)
        if a["_operator"] == b["_operator"]:
            continue
        if (a["account_id"], b["account_id"]) in [(x, y) for x, y, _ in decoy_pairs]:
            continue
        # force them to look alike on correlated, ecosystem-caused signals
        shared_batch = f"batch_{hexid(4, rng=rng)}"
        # RARE shared infrastructure: a small dedicated host, used by exactly these
        # two unrelated vendors. Rarity weighting CANNOT suppress this - only
        # independence grouping can, because both signals came from ONE scrape.
        rare_asn = f"AS_SHARED_{len(decoy_pairs):02d}"
        rare_tpl = f"tpl_shared_{len(decoy_pairs):02d}"
        for acct in (a, b):
            acct["pgp_fp"] = HUB_PGP               # hub -> suppressed by rarity
            acct["template_id"] = rare_tpl         # rare -> survives rarity
            acct["asn"] = rare_asn                 # rare -> survives rarity
            acct["infra_batch"] = shared_batch     # SAME scrape -> ONE origin
        decoy_pairs.append((a["account_id"], b["account_id"], "rare_shared_infra"))

    # ------------------------------------------------------------------- outputs

    # ------------------------------------ T6: account handovers (resale/compromise)
    handover_pairs = []
    tries = 0
    while len(handover_pairs) < N_HANDOVERS and tries < 3000:
        tries += 1
        a, b = rng.sample(accounts, 2)
        if a["_operator"] == b["_operator"] or not a["listings"]:
            continue
        b["contact_id"] = a["contact_id"]              # inherited identifier
        src = a["listings"][0]
        b["listings"].append({"title": src["title"], "price_usd": src["price_usd"],
                              "image_id": src["image_id"],
                              "capture_batch": src["capture_batch"]})
        handover_pairs.append((a["account_id"], b["account_id"]))

    answer_key = [(a["account_id"], a["_operator"]) for a in accounts]
    op_of = dict(answer_key)

    public_accounts = []
    for a in accounts:
        a = dict(a)
        a.pop("_operator")
        public_accounts.append(a)

    with open(out_dir / "accounts.json", "w", encoding="utf-8") as f:
        json.dump(public_accounts, f, indent=2)

    with open(out_dir / "answer_key.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "operator_id"])
        w.writerows(sorted(answer_key))

    # ---- candidate pairs: all positives + all decoys + random negatives to fill

    ids = [a["account_id"] for a in accounts]
    all_pairs = list(combinations(sorted(ids), 2))

    positives = [(x, y) for x, y in all_pairs if op_of[x] == op_of[y]]
    decoy_set = {tuple(sorted((x, y))) for x, y, _ in decoy_pairs}
    handover_set = {tuple(sorted(p)) for p in handover_pairs}
    negatives = [p for p in all_pairs if op_of[p[0]] != op_of[p[1]]
                 and p not in decoy_set and p not in handover_set]

    n_neg = max(0, TARGET_PAIRS - len(positives) - len(decoy_set) - len(handover_set))
    sampled = rng.sample(negatives, min(n_neg, len(negatives)))

    rows = []
    for x, y in positives:
        rows.append((x, y, 1, "same_operator"))
    for x, y in sorted(decoy_set):
        rows.append((x, y, 0, "PLANTED_DECOY"))
    for x, y in sorted(handover_set):
        rows.append((x, y, 0, "PLANTED_HANDOVER"))
    for x, y in sampled:
        rows.append((x, y, 0, ""))
    rng.shuffle(rows)

    with open(out_dir / "pairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["account_a", "account_b", "is_same_operator", "note"])
        w.writerows(rows)

    manifest = {
        "generator": "RANGE-SIM-v0.1", "seed": seed,
        "operators": N_OPERATORS, "accounts": len(accounts), "pairs": len(rows),
        "scope": "synthetic fixture only; labels are evaluation-only",
        "sha256": {name: hashlib.sha256((out_dir / name).read_bytes()).hexdigest()
                   for name in ("accounts.json", "answer_key.csv", "pairs.csv")},
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    # ------------------------------------------------------- verify traps landed

    pgp_counts = Counter(a["pgp_fp"] for a in accounts)
    contact_counts = Counter(a["contact_id"] for a in accounts)
    image_counts = Counter(l["image_id"] for a in accounts for l in a["listings"])

    print("=" * 62)
    print("RANGE-SIM built")
    print("=" * 62)
    print(f"  operators                 {N_OPERATORS}")
    print(f"  accounts                  {len(accounts)}")
    print(f"  listings                  {sum(len(a['listings']) for a in accounts)}")
    print(f"  candidate pairs           {len(rows)}"
          f"   ({sum(r[2] for r in rows)} positive / {len(rows)-sum(r[2] for r in rows)} negative)")
    print()
    print("  TRAP CHECK")
    print(f"  T1 hub PGP '{HUB_PGP}'   on {pgp_counts[HUB_PGP]}/{len(accounts)} accounts"
          f"  ({100*pgp_counts[HUB_PGP]//len(accounts)}%)  -> must score ZERO")
    mirrored = sum(1 for v in image_counts.values() if v > 1)
    print(f"  T2 mirrored images        {mirrored} images appear >1x (max {max(image_counts.values())}x)"
          f"  -> must collapse to 1 group")
    print(f"  T3 planted decoys         {len(decoy_set)} cross-operator pairs share template+ASN+hub PGP")
    rare = sum(1 for v in contact_counts.values() if v == 2)
    print(f"  T4 rare contact IDs       {rare} identifiers appear exactly 2x  -> the real signal")
    print(f"  T6 account handovers      {len(handover_set)} cross-operator pairs share a rare contact ID + images")
    print(f"  T5 compartmented ops      {N_COMPARTMENTED} operators share nothing  -> expect to MISS these")
    print()
    print("  FILES")
    print(f"  {out_dir / 'accounts.json'}    <- system input")
    print(f"  {out_dir / 'answer_key.csv'}   <- QUARANTINED, eval only")
    print(f"  {out_dir / 'pairs.csv'}        <- labelled synthetic candidate pairs")
    print("=" * 62)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_range(target)
