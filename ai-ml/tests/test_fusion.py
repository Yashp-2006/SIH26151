"""
PRAMANA Fusion Engine & API Test Suite.
Verifies Person B fusion mathematics, independence grouping, hub suppression,
counter-evidence, and FastAPI endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from pramana.schema import Observation, Assessment, FamilyResult, CounterEvidence, verbal_band
from pramana.score_pramana import assess, merged, _fuse_family, LAMBDA, CAPS
from pramana.rarity import RarityIndex, TAU
from pramana.api import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_verbal_bands():
    assert verbal_band(0.5) == "LIMITED"
    assert verbal_band(1.5) == "MODERATE"
    assert verbal_band(2.5) == "MODERATELY STRONG"
    assert verbal_band(3.5) == "STRONG"
    assert verbal_band(4.0) == "STRONG"
    assert verbal_band(-0.1) == "LIMITED"


def test_hub_suppression():
    rarity = RarityIndex()
    # Hub PGP default block appears on 69 accounts in RANGE-SIM (tau=12)
    assert rarity.is_hub("pgp_fp", "DEFAULT_BLOCK_1")
    w, note = rarity.weight("pgp_fp", "DEFAULT_BLOCK_1")
    assert w == 0.0
    assert "forced to 0" in note

    # Rare indicator
    rare_w, rare_note = rarity.weight("contact_id", "non_existent_rare")
    assert rare_w > 1.0


def test_family_caps():
    # F6 cap is 1.0
    fam = "F6"
    obs = [
        Observation("p1", fam, "style", "val1", "exact", "batch1", 1.0, 1),
        Observation("p1", fam, "style", "val2", "exact", "batch2", 1.0, 1),
        Observation("p1", fam, "style", "val3", "exact", "batch3", 1.0, 1),
    ]
    rarity = RarityIndex()
    result = _fuse_family(fam, obs, rarity, lam=1.0, grouping=True)
    assert result.capped_log_lr <= CAPS["F6"]
    assert result.capped_log_lr == 1.0


def test_independence_grouping_collapses_mirrors():
    rarity = RarityIndex()
    # Multiple hits on same capture origin should collapse into 1 group
    obs = [
        Observation("p1", "F5", "image_id", "img1", "phash", "batch_shared", 1.0, 5),
        Observation("p1", "F5", "image_id", "img2", "phash", "batch_shared", 1.0, 3),
    ]
    res_grouped = _fuse_family("F5", obs, rarity, grouping=True)
    assert res_grouped.n_groups == 1

    res_ungrouped = _fuse_family("F5", obs, rarity, grouping=False)
    assert res_ungrouped.n_groups == 8  # 5 + 3 raw retrievals


def test_refusal_when_k_less_than_two():
    rarity = RarityIndex()
    accounts = {
        "acc_a": {"contact_id": "c1", "pgp_fp": "p1"},
        "acc_b": {"contact_id": "c1", "pgp_fp": "p2"},
    }
    # Only 1 family and 1 origin -> k=1 < 2
    obs = [
        Observation("acc_a__acc_b", "F4", "contact_id", "c1", "exact", "origin_1", 1.0, 1)
    ]
    res = assess("acc_a__acc_b", "acc_a", "acc_b", obs, rarity, accounts, k_min=2)
    assert not res.issued
    assert "k=1 independent origins < k_min=2" in res.refusal_reason


def test_api_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["asserted_priors"]["tau"] == 12
    assert data["asserted_priors"]["k_min"] == 2


def test_api_assess_refused(client):
    # acc_100 vs acc_129 is the planted decoy (k < 2)
    res = client.post("/assess", json={"account_a": "acc_100", "account_b": "acc_129"})
    assert res.status_code == 200
    data = res.json()
    assert data["issued"] is False
    assert "k=1 independent origins < k_min=2" in data["refusal_reason"]


def test_api_assess_true_pair(client):
    # acc_024 vs acc_025 is true same operator
    res = client.post("/assess", json={"account_a": "acc_024", "account_b": "acc_025", "include_naive": True})
    assert res.status_code == 200
    data = res.json()
    assert data["issued"] is True
    assert data["verbal_band"] == "STRONG"
    assert data["log_lr"] > 3.0
    assert "naive_baseline" in data


def test_api_balance_sheet(client):
    res = client.get("/balance_sheet/acc_024/acc_025")
    assert res.status_code == 200
    data = res.json()
    assert len(data["families"]) > 0
    assert "defence_hypothesis" in data


def test_api_precompute(client):
    res = client.post("/precompute")
    assert res.status_code == 200
    data = res.json()
    assert data["pairs"] > 0
    assert "issued" in data
    assert "refused" in data
