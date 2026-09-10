"""
Freeze the PRAMANA fusion engine's output into a static snapshot the frontend
bundles as an offline fallback (and its initial data on first paint).

    python frontend/scripts/gen_snapshot.py

Reads the real engine in ai-ml/pramana/. Writes frontend/src/data/snapshot.json.
The engine's own docstring says: precompute once, never infer live in a demo.
"""

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AIML = REPO / "ai-ml"
PRAMANA = AIML / "pramana"
sys.path.insert(0, str(PRAMANA))
sys.path.insert(0, str(AIML))

from stub_features_a import emit_all  # noqa: E402
from rarity import RarityIndex, TAU, REFERENCE_POPULATION  # noqa: E402
import score_pramana  # noqa: E402
import score_naive  # noqa: E402
from evaluate import run, load_key  # noqa: E402

OUT = REPO / "frontend" / "public" / "snapshot.json"

# curated demo cases (from pramana/demo.py) — order matters for the walkthrough
DEMO = [
    ("acc_100", "acc_129", "planted_decoy",
     "Two unrelated vendors on one rare shared host. The gate refuses it."),
    ("acc_024", "acc_025", "true_same_operator",
     "One operator, two marketplaces. Independence-corroborated across families."),
    ("acc_048", "acc_106", "account_handover",
     "A resold account. The system merges it and states plainly why it cannot tell."),
]


def brief(acc: dict) -> dict:
    return {
        "account_id": acc["account_id"],
        "handle": acc["handle"],
        "market": acc["market"],
        "pgp_fp": acc["pgp_fp"],
        "contact_id": acc["contact_id"],
        "asn": acc["asn"],
        "template_id": acc["template_id"],
        "listings": len(acc["listings"]),
    }


def main() -> None:
    accounts, pairs, obs_by_pair = emit_all()
    rarity = RarityIndex()
    key = load_key()

    # ablation metrics (naive / no-grouping / pramana)
    cn, cp, assessments = run(quiet=True)
    _, cg, _ = run(quiet=True, grouping=False)

    def m(c: dict) -> dict:
        return {
            "false_merge_rate": round(c["false_merge_rate"], 4),
            "false_merges": c["fp"],
            "precision": round(c["precision"], 4),
            "recall": round(c["recall"], 4),
            "f1": round(c["f1"], 4),
            "true_merges": c["tp"],
            "missed_links": c["fn"],
        }

    refused = sum(1 for a in assessments.values() if not a.issued and not a.excluded)

    pair_rows = []
    for r in pairs:
        pid = f"{r['account_a']}__{r['account_b']}"
        pair_rows.append({
            "pair_id": pid,
            "account_a": r["account_a"],
            "account_b": r["account_b"],
            "is_same_operator": r["is_same_operator"] == "1",
            "note": r["note"] or "",
        })

    assess_out = {}
    for pid, a in assessments.items():
        d = a.to_dict()
        d["naive_baseline"] = score_naive.score_pair(obs_by_pair[pid], rarity)
        assess_out[pid] = d

    snapshot = {
        "generated_from": "ai-ml/pramana (RANGE-SIM v0.1)",
        "health": {
            "params_version": "v0.1",
            "reference_population": REFERENCE_POPULATION,
            "lambda": score_pramana.LAMBDA,
            "tau": TAU,
            "k_min": score_pramana.K_MIN,
            "ceiling": score_pramana.CEILING,
            "caps": score_pramana.CAPS,
            "merge_threshold": score_pramana.MERGE_THRESHOLD,
        },
        "metrics": {
            "corpus": {
                "pairs": len(pairs),
                "operators": len(set(key.values())),
                "positives": sum(1 for r in pairs if r["is_same_operator"] == "1"),
                "decoys": sum(1 for r in pairs if r["note"] == "PLANTED_DECOY"),
                "refused_k_lt_2": refused,
            },
            "naive": m(cn),
            "no_grouping": m(cg),
            "pramana": m(cp),
        },
        "accounts": [brief(a) for a in accounts.values()],
        "pairs": pair_rows,
        "assessments": assess_out,
        "demo_cases": [
            {
                "account_a": a, "account_b": b, "kind": kind, "caption": cap,
                "pair_id": f"{a}__{b}",
                "detail_a": brief(accounts[a]),
                "detail_b": brief(accounts[b]),
                "operator_a": key.get(a, "?"),
                "operator_b": key.get(b, "?"),
            }
            for a, b, kind, cap in DEMO
        ],
    }

    OUT.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT.relative_to(REPO)}  ({kb:.0f} KB)")
    print(f"  {len(assess_out)} assessments · "
          f"{sum(1 for a in assessments.values() if a.issued)} issued · {refused} refused")
    print(f"  false-merge rate  naive {cn['false_merge_rate']:.1%}  "
          f"-> pramana {cp['false_merge_rate']:.1%}")


if __name__ == "__main__":
    main()
