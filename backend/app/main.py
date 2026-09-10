"""
PRAMANA backend — the gateway between the frontend dashboard and the evidence
fusion engine in ai-ml/pramana/.

    python -m uvicorn backend.app.main:app --port 8000     (run from repo root)

This imports the real engine directly (no HTTP hop, no model, pure arithmetic),
precomputes every candidate pair at startup, and serves the results plus the
RANGE-SIM ablation. Persistence (PostgreSQL ledger, auth, retraction log) stays
deferred per docs/architecture.md — this is the read path only.
"""

from __future__ import annotations

import csv
import sys
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .nlp import router as nlp_router

REPO = Path(__file__).resolve().parents[2]
PRAMANA = REPO / "ai-ml" / "pramana"
sys.path.insert(0, str(PRAMANA))
sys.path.insert(0, str(REPO / "ai-ml"))

from stub_features_a import emit_all, observations_for_pair  # noqa: E402
from rarity import RarityIndex, TAU, REFERENCE_POPULATION  # noqa: E402
import score_pramana  # noqa: E402
import score_naive  # noqa: E402
from evaluate import run, load_key  # noqa: E402

app = FastAPI(title="PRAMANA Gateway", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(nlp_router)

_accounts, _pairs, _obs = emit_all()
_rarity = RarityIndex()
_key = load_key()
_cache: dict[str, dict] = {}


def _assess(pid: str) -> dict:
    if pid in _cache:
        return _cache[pid]
    a, b = pid.split("__")
    if a not in _accounts or b not in _accounts:
        raise HTTPException(404, "unknown account_id")
    obs = _obs.get(pid) or observations_for_pair(pid, _accounts[a], _accounts[b])
    d = score_pramana.assess(pid, a, b, obs, _rarity, _accounts).to_dict()
    d["naive_baseline"] = score_naive.score_pair(obs, _rarity)
    _cache[pid] = d
    return d


def _brief(acc: dict) -> dict:
    return {
        "account_id": acc["account_id"],
        "handle": acc["handle"],
        "market": acc["market"],
        "pgp_fp": acc["pgp_fp"],
        "contact_id": acc["contact_id"],
        "asn": acc["asn"],
        "template_id": acc["template_id"],
        "listings": len(acc["listings"]),
        "operator_id": _key.get(acc["account_id"], "?"),
    }


@lru_cache(maxsize=1)
def _metrics() -> dict:
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
    return {
        "corpus": {
            "pairs": len(_pairs),
            "operators": len(set(_key.values())),
            "positives": sum(1 for r in _pairs if r["is_same_operator"] == "1"),
            "decoys": sum(1 for r in _pairs if r["note"] == "PLANTED_DECOY"),
            "refused_k_lt_2": refused,
        },
        "naive": m(cn),
        "no_grouping": m(cg),
        "pramana": m(cp),
    }


DEMO = [
    ("acc_100", "acc_129", "planted_decoy",
     "Two unrelated vendors on one rare shared host. The gate refuses it."),
    ("acc_024", "acc_025", "true_same_operator",
     "One operator, two marketplaces. Independence-corroborated across families."),
    ("acc_048", "acc_106", "account_handover",
     "A resold account. The system merges it and states plainly why it cannot tell."),
]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "params_version": "v0.1",
        "reference_population": REFERENCE_POPULATION,
        "lambda": score_pramana.LAMBDA,
        "tau": TAU,
        "k_min": score_pramana.K_MIN,
        "ceiling": score_pramana.CEILING,
        "caps": score_pramana.CAPS,
        "merge_threshold": score_pramana.MERGE_THRESHOLD,
        "accounts": len(_accounts),
        "pairs": len(_pairs),
    }


@app.get("/accounts")
def accounts():
    return [_brief(a) for a in _accounts.values()]


@app.get("/pairs")
def pairs():
    return [
        {
            "pair_id": f"{r['account_a']}__{r['account_b']}",
            "account_a": r["account_a"],
            "account_b": r["account_b"],
            "is_same_operator": r["is_same_operator"] == "1",
            "note": r["note"] or "",
        }
        for r in _pairs
    ]


@app.get("/assess/{account_a}/{account_b}")
def assess(account_a: str, account_b: str):
    return _assess(f"{account_a}__{account_b}")


# alias — the engine's own route name
@app.get("/balance_sheet/{account_a}/{account_b}")
def balance_sheet(account_a: str, account_b: str):
    return _assess(f"{account_a}__{account_b}")


@app.get("/metrics")
def metrics():
    return _metrics()


@app.get("/demo")
def demo():
    out = []
    for a, b, kind, cap in DEMO:
        out.append({
            "pair_id": f"{a}__{b}",
            "account_a": a,
            "account_b": b,
            "kind": kind,
            "caption": cap,
            "detail_a": _brief(_accounts[a]),
            "detail_b": _brief(_accounts[b]),
            "assessment": _assess(f"{a}__{b}"),
        })
    return out


# serve the built dashboard if it exists (single-origin demo deployment)
_dist = REPO / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="dashboard")
