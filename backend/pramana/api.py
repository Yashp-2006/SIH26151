"""
LIST B INTEGRATION SURFACE.  One container, one endpoint, no GPU, no model.

    uvicorn pramana.api:app --port 8000

Deployment note: this is pure arithmetic over the ledger. It does NOT belong on
Hugging Face Spaces - free Spaces sleep and cold-start 30-60s, which will hang a
live demo. Run it beside Postgres, or let the backend import score_pramana
directly. Only the heavy models (stylometry embeddings, DarkBERT copilot) need
HF, and those are Person A's, capped at 1.0 log-LR.

FOR THE DEMO: hit /precompute once at startup, then the UI reads cached
assessments. Never make a live inference call in front of judges.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from pramana.stub_features_a import emit_all, observations_for_pair
    from pramana.rarity import RarityIndex, TAU, REFERENCE_POPULATION
    from pramana import score_pramana, score_naive
except ModuleNotFoundError:
    from stub_features_a import emit_all, observations_for_pair
    from rarity import RarityIndex, TAU, REFERENCE_POPULATION
    import score_pramana, score_naive

app = FastAPI(title="PRAMANA Evidence Fusion", version="0.1")

_accounts, _pairs, _obs = emit_all()
_rarity = RarityIndex()
_cache = {}


class PairRequest(BaseModel):
    account_a: str
    account_b: str
    include_naive: bool = False        # for the side-by-side demo view


@app.get("/health")
def health():
    return {"status": "ok", "params_version": "v0.1",
            "reference_population": REFERENCE_POPULATION,
            "asserted_priors": {"lambda": score_pramana.LAMBDA, "tau": TAU,
                                "k_min": score_pramana.K_MIN,
                                "ceiling": score_pramana.CEILING,
                                "caps": score_pramana.CAPS},
            "note": "priors are design assertions, not fitted parameters"}


@app.post("/assess")
def assess(req: PairRequest):
    a, b = req.account_a, req.account_b
    if a not in _accounts or b not in _accounts:
        raise HTTPException(404, "unknown account_id")
    pid = f"{a}__{b}"
    obs = _obs.get(pid)
    if obs is None:
        obs = observations_for_pair(pid, _accounts[a], _accounts[b])

    result = score_pramana.assess(pid, a, b, obs, _rarity, _accounts).to_dict()
    if req.include_naive:
        result["naive_baseline"] = score_naive.score_pair(obs, _rarity)
    return result


@app.post("/precompute")
def precompute():
    """Run every candidate pair once and cache. Call at demo startup."""
    for pid, obs in _obs.items():
        a, b = pid.split("__")
        _cache[pid] = score_pramana.assess(pid, a, b, obs, _rarity,
                                           _accounts).to_dict()
    issued = sum(1 for v in _cache.values() if v["issued"])
    return {"pairs": len(_cache), "issued": issued,
            "refused": len(_cache) - issued}


@app.get("/balance_sheet/{account_a}/{account_b}")
def balance_sheet(account_a: str, account_b: str):
    """Exactly the object the Evidence Balance Sheet renders. No re-derived
    scores - the frontend shows the ledger's own numbers."""
    return assess(PairRequest(account_a=account_a, account_b=account_b,
                              include_naive=True))
