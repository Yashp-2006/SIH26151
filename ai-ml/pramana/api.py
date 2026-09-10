"""Local synthetic demonstration API; no ledger or evidence promotion."""
from copy import deepcopy
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pramana.stub_features_a import emit_all, observations_for_pair
from pramana.rarity import RarityIndex, TAU, REFERENCE_POPULATION
from pramana import score_pramana, score_naive


class PairRequest(BaseModel):
    account_a: str = Field(min_length=1, max_length=256)
    account_b: str = Field(min_length=1, max_length=256)
    include_naive: bool = False


def create_app(data_dir=None):
    """Each instance owns its corpus and cache. Explicit paths select a corpus."""
    directory = Path(data_dir) if data_dir is not None else Path(__file__).resolve().parent
    accounts, pairs, observations = emit_all(directory / "accounts.json", directory / "pairs.csv")
    rarity = RarityIndex(directory / "accounts.json")
    cache = {}
    lock = Lock()
    app = FastAPI(title="PRAMANA Synthetic Fusion Demo", version="0.1")

    @app.get("/health")
    def health():
        return {"status": "ok", "params_version": "v0.1",
                "reference_population": REFERENCE_POPULATION,
                "asserted_priors": {"lambda": score_pramana.LAMBDA, "tau": rarity.tau,
                    "k_min": score_pramana.K_MIN, "ceiling": score_pramana.CEILING,
                    "caps": dict(score_pramana.CAPS)},
                "note": "Synthetic experiment only; priors are not fitted; DC-06 promotion is deferred"}

    @app.post("/assess")
    def assess(req: PairRequest):
        a, b = sorted((req.account_a, req.account_b))
        if a == b:
            raise HTTPException(422, "two distinct account IDs required")
        if a not in accounts or b not in accounts:
            raise HTTPException(404, "unknown account_id")
        pid = f"{a}__{b}"
        with lock:
            result = deepcopy(cache.get(pid))
        obs = observations.get(pid)
        if obs is None:
            obs = observations_for_pair(pid, accounts[a], accounts[b])
        if result is None:
            result = score_pramana.assess(pid, a, b, obs, rarity, accounts).to_dict()
        if req.include_naive:
            result["naive_baseline"] = score_naive.score_pair(obs, rarity)
        return result

    @app.post("/precompute")
    def precompute():
        computed = {}
        for row in pairs:
            a, b = sorted((row["account_a"], row["account_b"]))
            pid = f"{a}__{b}"
            obs = observations_for_pair(pid, accounts[a], accounts[b])
            computed[pid] = score_pramana.assess(pid, a, b, obs, rarity, accounts).to_dict()
        with lock:
            cache.clear()
            cache.update(computed)
        issued = sum(v["issued"] for v in computed.values())
        return {"pairs": len(computed), "issued": issued, "refused": len(computed) - issued}

    @app.get("/balance_sheet/{account_a}/{account_b}")
    def balance_sheet(account_a: str, account_b: str):
        return assess(PairRequest(account_a=account_a, account_b=account_b, include_naive=True))

    return app


app = create_app()
