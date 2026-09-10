"""Adversarial regressions for the synthetic boundary and reproducibility."""
import copy
import hashlib
import json
import random
from dataclasses import replace
from itertools import permutations
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pramana.api import create_app
from pramana.data import DATA_DIR
from pramana.evaluate import confusion, run
from pramana.range_sim import generate_range
from pramana.rarity import RarityIndex, TAU
from pramana.schema import Observation, CounterEvidence
from pramana.score_pramana import assess, merged
from pramana.stub_features_a import load


ACCOUNTS = {"a": {"contact_id": "c", "pgp_fp": "p"}, "b": {"contact_id": "c", "pgp_fp": "p"}}
OBS = [Observation("a__b", "F4", "contact_id", "c", "exact", "origin-contact"),
       Observation("a__b", "F5", "image_id", "img", "phash", "origin-image")]


def result(obs=None, **kwargs):
    return assess("a__b", "a", "b", OBS if obs is None else obs, RarityIndex(), ACCOUNTS, **kwargs)


@pytest.mark.parametrize("field,value", [
    ("pair_id", "wrong"), ("family", "F10"), ("family", "F9"),
    ("independence_key", ""), ("indicator_value", None),
    ("similarity", float("nan")), ("similarity", float("inf")),
    ("similarity", -1), ("similarity", True),
    ("n_raw_hits", 0), ("n_raw_hits", -1), ("n_raw_hits", True),
    ("match_type", "llm")])
def test_invalid_observation(field, value):
    with pytest.raises(ValueError):
        result([replace(OBS[0], **{field: value})])


@pytest.mark.parametrize("kwargs", [{"lam": float("nan")}, {"lam": 1.1},
    {"lam": -1}, {"k_min": 0}, {"k_min": True}, {"ceiling": float("inf")},
    {"ceiling": 5}, {"grouping": "yes"}])
def test_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        result(**kwargs)


def test_generator_and_permutation_equivalence():
    reference = result().to_dict()
    assert result(iter(OBS)).to_dict() == reference
    for ordering in permutations(OBS):
        assert result(ordering).to_dict() == reference


def test_duplicate_and_mirror_no_score_increase():
    base = result()
    repeated = result(OBS * 4)
    assert (base.log_lr, base.family_count_k) == (repeated.log_lr, repeated.family_count_k)
    assert result([replace(o, n_raw_hits=1000000) for o in OBS]).log_lr == base.log_lr


def test_cross_family_double_allocation_rejected():
    with pytest.raises(ValueError, match="multiple families"):
        result([OBS[0], replace(OBS[0], family="F3")])


def test_shared_origin_refused_and_empty_refused():
    out = result([replace(o, independence_key="shared") for o in OBS])
    assert not out.issued and out.log_lr is None and out.family_count_k == 1
    assert out.counter_evidence[0]["contradiction_class"] == "shared_ecosystem_not_shared_control"
    assert result([]).log_lr is None


def test_veto_path_dominates_score(monkeypatch):
    # Exercise the existing branch; this does not introduce a veto detector.
    import pramana.score_pramana as scorer
    monkeypatch.setattr(scorer, "_counter_evidence", lambda *args: [
        CounterEvidence("test_fixture_only", "hard", 0.0, "injected regression fixture")])
    out = result()
    assert out.excluded and not out.issued
    assert out.log_lr is None and out.verbal_band is None and not merged(out)


def test_soft_counter_evidence():
    accounts = copy.deepcopy(ACCOUNTS)
    accounts["b"] = {"contact_id": "different", "pgp_fp": "different"}
    out = assess("a__b", "a", "b", OBS, RarityIndex(), accounts)
    assert out.counter_evidence[0]["delta"] == 0.4
    assert out.counter_evidence[0]["severity"] == "soft" and not out.excluded


def test_ablation_explanations_are_stable():
    assert result(grouping=False).to_dict() == result(copy.deepcopy(OBS), grouping=False).to_dict()


def test_default_data_ignores_working_directory(tmp_path, monkeypatch):
    (tmp_path / "accounts.json").write_text("[]")
    (tmp_path / "pairs.csv").write_text("invalid")
    monkeypatch.chdir(tmp_path)
    assert RarityIndex().n == len(load()[0]) > 0


@pytest.mark.parametrize("mutation", ["empty", "duplicate", "null"])
def test_invalid_population(tmp_path, mutation):
    rows = json.loads((DATA_DIR / "accounts.json").read_text())
    if mutation == "empty": rows = []
    elif mutation == "duplicate": rows.append(rows[0])
    else: rows[0]["pgp_fp"] = None
    path = tmp_path / "accounts.json"
    path.write_text(json.dumps(rows))
    with pytest.raises(ValueError): RarityIndex(path)


def test_hub_boundary_and_instance_isolation():
    a, b = RarityIndex(tau=12), RarityIndex(tau=13)
    for index in (a, b): index.counts[("pgp_fp", "fixture")] = 13
    assert a.weight("pgp_fp", "fixture")[0] == 0
    assert b.weight("pgp_fp", "fixture")[0] > 0
    assert TAU == 12


def test_tau_evaluation_argument_is_used():
    _, normal, _ = run(quiet=True)
    _, suppressed, _ = run(tau=0, quiet=True)
    assert normal["tp"] > 0 and suppressed["tp"] == 0
    assert run(quiet=True)[1] == normal


def test_range_replay_and_global_rng(tmp_path):
    before = random.getstate()
    for directory in (tmp_path / "one", tmp_path / "two"):
        generate_range(directory)
    assert random.getstate() == before
    for name in ("accounts.json", "pairs.csv", "answer_key.csv"):
        assert (tmp_path / "one" / name).read_bytes() == (tmp_path / "two" / name).read_bytes()
        # ZIP fixture may use a different line-ending convention.
        assert (tmp_path / "one" / name).read_text() == (DATA_DIR / name).read_text()
    manifest = json.loads((tmp_path / "one/manifest.json").read_text())
    for name, digest in manifest["sha256"].items():
        assert hashlib.sha256((tmp_path / "one" / name).read_bytes()).hexdigest() == digest
    _, metrics, assessments = run(data_dir=tmp_path / "one", quiet=True)
    assert {k: metrics[k] for k in ("tp", "fp", "fn", "tn")} == {"tp": 85, "fp": 12, "fn": 14, "tn": 789}
    assert sum(not a.issued for a in assessments.values()) == 803
    assert all("_operator" not in row for row in json.loads((tmp_path / "one/accounts.json").read_text()))


def test_evaluation_rejects_length_mismatch_and_nonbinary():
    with pytest.raises(ValueError): confusion([True], [])
    with pytest.raises(ValueError): confusion([float("nan")], [1])


def test_api_order_self_pair_and_cache():
    with TestClient(create_app()) as client:
        payload = {"account_a": "acc_024", "account_b": "acc_025"}
        before = client.post("/assess", json=payload).json()
        assert client.post("/precompute").json() == {"pairs": 900, "issued": 97, "refused": 803}
        assert client.post("/assess", json=payload).json() == before
        reverse = {"account_a": "acc_025", "account_b": "acc_024"}
        assert client.post("/assess", json=reverse).json() == before
        assert "naive_baseline" in client.post("/assess", json=dict(payload, include_naive=True)).json()
        assert "naive_baseline" not in client.post("/assess", json=payload).json()
        assert client.post("/assess", json={"account_a": "acc_024", "account_b": "acc_024"}).status_code == 422
        assert client.post("/assess", json={"account_a": "unknown", "account_b": "acc_024"}).status_code == 404


def test_llm_envelope_has_no_scoring_authority():
    from group_g_llm_assist.hypothesis_generator import generate_candidate_hypothesis
    hypothesis = generate_candidate_hypothesis("a", "b", "Unsupported assertion [OBS-1]", ["OBS-1"], "doc")
    assert hypothesis.candidate.raw_log_lr == 0
    assert hypothesis.candidate.extra["scoring_eligible"] is False
    with pytest.raises(ValueError, match="DC-06"):
        result([hypothesis.candidate])


def test_corrupt_image_is_not_similarity(tmp_path):
    from group_d_embeddings.image_embeddings import compute_image_similarity
    from PIL import UnidentifiedImageError, Image
    path = tmp_path / "bad.png"
    path.write_bytes(b"not an image")
    with pytest.raises(UnidentifiedImageError): compute_image_similarity(str(path), str(path))
    with pytest.raises(FileNotFoundError): compute_image_similarity("missing.png", str(path))
    Image.new("RGB", (16, 16), "red").save(path)
    assert compute_image_similarity(str(path), str(path)) == 1.0


def test_wallet_component_bridge_and_order():
    from group_c_wallet_infra.wallet_cluster import cluster_wallets
    transactions = [{"inputs": ["a", "b"]}, {"inputs": ["c", "d"]}, {"inputs": ["b", "d"]}]
    for order in permutations(transactions):
        assert cluster_wallets(order) == dict.fromkeys("abcd", "a")


def test_ner_missing_model_explicit(monkeypatch):
    from group_b_nlp.lang_ner import load_ner_model
    import spacy
    def absent(*args): raise OSError("missing")
    monkeypatch.setattr(spacy, "load", absent)
    with pytest.raises(RuntimeError, match="explicitly"): load_ner_model()


def test_graph_document_replay_does_not_double_count():
    from group_f_graph.co_occurrence import CoOccurrenceGraph
    graph = CoOccurrenceGraph()
    graph.add_document("doc", ["a", "b", "a"])
    graph.add_document("doc", ["b", "a"])
    assert graph.get_co_occurrence("a", "b") == 1
    assert graph.graph.nodes["a"]["doc_count"] == 1
    with pytest.raises(ValueError): graph.add_document("doc", ["a", "c"])
    assert graph.get_co_occurrence("a", "c") == 0


def test_text_method_explicit_and_model_failure():
    from group_d_embeddings.text_embeddings import compute_text_similarity, build_text_embedding_candidate
    assert compute_text_similarity(" ", " ") == 0
    assert build_text_embedding_candidate("a", "b", "text", "text", "doc").extra["method"] == "character_trigram_cosine"
    class BrokenModel:
        def encode(self, text): raise RuntimeError("model failed")
    with pytest.raises(RuntimeError): compute_text_similarity("a", "b", model=BrokenModel())


def test_frozen_cyber_boundary_stays_unpromoted():
    # Source paths are deliberately separate; the shared shape is not an adapter.
    from shared.contracts import EvidenceCandidate
    from dataclasses import fields
    assert [f.name for f in fields(EvidenceCandidate)] == [
        "subject_a", "subject_b", "family", "raw_log_lr", "rarity_factor",
        "independence_key", "polarity", "detector_version", "doc_ref", "extra"]
    with pytest.raises(ValueError, match="DC-06"):
        result([{"promotion_status": "blocked_DC-06", "assessment": None}])


def test_malformed_pair_corpus(tmp_path):
    import csv
    for rows in [
        [("acc_000", "acc_001"), ("acc_001", "acc_000")],
        [("acc_000", "acc_000")], [("acc_000", "missing")]]:
        path = tmp_path / "pairs.csv"
        with path.open("w", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(["account_a", "account_b"])
            writer.writerows(rows)
        with pytest.raises(ValueError): load(pairs_path=path)


def test_missing_counter_identifiers_are_not_negative_evidence():
    accounts = copy.deepcopy(ACCOUNTS)
    accounts["a"]["pgp_fp"] = None
    with pytest.raises(ValueError, match="Counter-evidence"):
        assess("a__b", "a", "b", OBS, RarityIndex(), accounts)
