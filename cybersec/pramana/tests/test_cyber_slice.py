"""Offline mechanism fixtures; no actor labels, network or large archive reads."""

from copy import deepcopy
from dataclasses import asdict
import hashlib
import io
import json
import tarfile
import pytest

from cyber.demo import fixture_archive_bytes, normalize_synthetic_archive, make_demo, synthetic_address
from cyber.indicators import extract_indicators, validate_bitcoin_base58check, verify_indicator_span
from cyber.policy import count_hub, positive_band_ceiling, screen_indicator, stable_key
from cyber.review import build_review_packet


@pytest.fixture
def records():
    return normalize_synthetic_archive(fixture_archive_bytes())


@pytest.fixture
def demo(tmp_path):
    return make_demo(tmp_path)


def test_repeated_snapshot_not_independent(demo):
    refs = demo["repetition_references"]
    assert any(r["type"] == "exact_row_match" and r["cross_snapshot"] for r in refs)
    assert demo["independence"]["eligible_k"] is None
    assert demo["independence"]["key"] is None
    assert len(demo["normalized_observations"]) == 18


def test_copied_content_not_same_operator(demo):
    assert any(r["type"] == "exact_content_match" for r in demo["repetition_references"])
    assert demo["assessment"] is None
    assert demo["review_state"] == "awaiting_human_review"
    assert demo["validated_evidence_candidates"] == []
    assert demo["authoritative_evidence"] == []


@pytest.mark.parametrize("reason", ["same_source_hash_changed_vendor", "same_url_different_source_hash"])
def test_discrepancy_not_handover_or_counterweight(demo, reason):
    hits = [d for d in demo["source_discrepancies"] if d["reason"].startswith(reason)]
    assert hits and all(d["effect"] == "review_only" and not d["negative_evidence"] for d in hits)
    assert all(r["listing_observation"]["canonical_listing_id"] is None for r in demo["normalized_observations"])


def test_damaged_pgp_not_f1_evidence(records):
    pgp = next(i for i in extract_indicators(records[0]) if i["type"] == "pgp_like_marker")
    assert pgp["raw"] == "BEGIN PGP PUBLIC KEY BLOCK"
    result = screen_indicator(pgp, records[0])
    assert result["eligible_family"] == "F1"
    assert not result["positive_support_allowed"]
    assert result["promotion"] == "blocked"
    assert any(s["rule"] == "CY-POL-014" for s in result["suppressions"])


def test_missing_field_not_negative(demo):
    assert any(m["field"] == "description" for m in demo["missing_information"])
    assert all(not m["negative_evidence"] for m in demo["missing_information"])


@pytest.mark.parametrize("count,expected", [(12, False), (13, True)])
def test_hub_boundary(demo, count, expected):
    associations = demo["fixture"]["hub_population"][:count]
    result = count_hub(synthetic_address(), associations, snapshot_id=associations[0]["snapshot_id"])
    assert result["is_hub"] is expected
    assert result["distinct_eligible_accounts"] == count
    assert not result["negative_evidence"]


def test_mentions_not_accounts_and_excluded_origins(demo):
    associations = deepcopy(demo["fixture"]["hub_population"])
    associations += deepcopy(associations[:3])
    associations[0]["lineage"] = "mirror"
    # Remove the duplicate for that account, so it is actually outside population.
    associations = [a for a in associations if a["account_id"] != associations[-3]["account_id"]]
    result = count_hub(synthetic_address(), associations, snapshot_id=associations[0]["snapshot_id"])
    assert result["distinct_eligible_accounts"] == 12
    assert result["is_hub"] is False


@pytest.mark.parametrize("field,value", [("lineage", "mirror"), ("lineage", "confirmed_clone"),
                                       ("eligibility", "rejected"), ("eligibility", "quarantined")])
def test_population_exclusions(demo, field, value):
    associations = deepcopy(demo["fixture"]["hub_population"])
    associations[-1][field] = value
    result = count_hub(synthetic_address(), associations, snapshot_id=associations[0]["snapshot_id"])
    assert result["distinct_eligible_accounts"] == 12
    assert len(result["excluded"]) == 1
    assert result["is_hub"] is False


def test_unknown_population_is_not_clean_check(demo):
    associations = deepcopy(demo["fixture"]["hub_population"])
    associations[-1]["lineage"] = "unknown"
    result = count_hub(synthetic_address(), associations, snapshot_id=associations[0]["snapshot_id"])
    assert result["is_hub"] is None
    assert result["population_status"] == "inconclusive"


def test_mixed_snapshots_rejected(demo):
    associations = deepcopy(demo["fixture"]["hub_population"])
    associations[-1]["snapshot_id"] = ["other"]
    with pytest.raises(ValueError):
        count_hub(synthetic_address(), associations, snapshot_id=associations[0]["snapshot_id"])


def test_hub_suppression_stays_in_snapshot_and_indicator_scope(demo):
    items = demo["promotion_review_items"]
    hub_items = [i for i in items if any(s["reason"] == "hub" for s in i["suppressions"])]
    assert hub_items
    assert all(i["eligible_family"] == "F2" for i in hub_items)
    assert all(i["provenance"]["snapshot_id"] == demo["hub_check"]["snapshot_id"] for i in hub_items)
    assert all(not i["negative_evidence"] for i in hub_items)


def test_clone_suppression_is_explicit_and_does_not_delete_origin(demo):
    suppressed = [i for i in demo["promotion_review_items"]
                  if any(s["reason"] == "confirmed_clone_lineage" for s in i["suppressions"])]
    assert suppressed and all(i["field_ref"][1] == 7 for i in suppressed)
    assert all(i["provenance"]["row_number"] == 14 for i in suppressed)
    assert any(i["provenance"]["row_number"] == 1 and not any(s["reason"] == "confirmed_clone_lineage"
               for s in i["suppressions"]) for i in demo["promotion_review_items"])


def test_hard_contradiction_not_invented(demo):
    assert demo["hard_veto"] == {"status": "deferred_DC-05", "result": None}
    assert demo["score"] is None
    assert demo["assessment"] is None
    assert next(c for c in demo["counter_checks"] if c["class"] == "temporal_impossibility")["status"] == "unimplemented"


@pytest.mark.parametrize("k,ceiling", [(0, "Weak"), (1, "Weak"), (2, None), (9, None)])
def test_k_ceiling_is_restriction_not_assessment(k, ceiling):
    assert positive_band_ceiling(k) == {"status": "restriction_only", "maximum_positive_band": ceiling}


@pytest.mark.parametrize("value", [-1, True, "1", 1.5])
def test_invalid_k_rejected(value):
    with pytest.raises(ValueError):
        positive_band_ceiling(value)


def test_provenance_replays_every_span(records):
    data = fixture_archive_bytes()
    assert records[0].provenance.archive_sha256 == hashlib.sha256(data).hexdigest()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as tar:
        for r in records:
            raw = tar.extractfile(r.provenance.member_name_raw).read()
            assert hashlib.sha256(raw).hexdigest() == r.provenance.member_sha256
            for i in extract_indicators(r):
                assert verify_indicator_span(i, r)
                assert r.source_record.raw_values[i["field_ref"][2]][i["start"]:i["end"]] == i["raw"]
                assert screen_indicator(i, r)["provenance"] == asdict(r.provenance)


@pytest.mark.parametrize("mutation", ["raw", "start", "family", "provenance", "id"])
def test_tampered_derivation_cannot_pass(records, mutation):
    i = deepcopy(extract_indicators(records[0])[0])
    if mutation == "raw": i["raw"] += "!"
    if mutation == "start": i["start"] += 1
    if mutation == "family": i["eligible_family"] = "F9"
    if mutation == "provenance": i["provenance"]["row_number"] = 999
    if mutation == "id": i["id"] = ["invented"]
    assert screen_indicator(i, records[0])["status"] == "invalid_derivation"


def test_crypto_known_vectors_and_bad_checksum():
    # Public format test vectors only; never demo actors or ownership assertions.
    assert validate_bitcoin_base58check("1BoatSLRHtKNngkdXEeobR76b53LETtpyT") == "checksum_valid"
    assert validate_bitcoin_base58check("3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy") == "checksum_valid"
    assert validate_bitcoin_base58check("1BoatSLRHtKNngkdXEeobR76b53LETtpyU") == "invalid_checksum"
    assert validate_bitcoin_base58check(synthetic_address()) == "checksum_valid"


def test_unicode_offset_and_no_repair(records):
    r = records[0]
    r.source_record.raw_values["description"] = "Ω🙂 prefix " + synthetic_address() + " suffix"
    address = next(i for i in extract_indicators(r) if i["type"] == "bitcoin_base58_lexical")
    assert address["start"] == len("Ω🙂 prefix ")
    assert verify_indicator_span(address, r)


def test_no_substring_from_longer_token(records):
    r = records[0]
    r.source_record.raw_values["description"] = "abc" + synthetic_address() + "xyz"
    assert not any(i["type"] == "bitcoin_base58_lexical" for i in extract_indicators(r))


def test_review_packet_deterministic_and_no_truth_labels(tmp_path):
    first = make_demo(tmp_path)
    assert first == make_demo(tmp_path)
    assert first["fixture"]["truth_labels"] == "none"
    assert all(r["observed_account"]["source_namespace"] == "synthetic-grams"
               for r in first["normalized_observations"] if r["observed_account"])


def test_duplicate_occurrence_ids_rejected(records):
    with pytest.raises(ValueError):
        build_review_packet([records[0], records[0]], subject_accounts=[records[0].observed_account.id,
            records[13].observed_account.id], population_ref="test")


def test_repeated_mentions_never_increase_hub_accounts(demo):
    association = demo["fixture"]["hub_population"][0]
    result = count_hub(synthetic_address(), [association] * 50, snapshot_id=association["snapshot_id"])
    assert result["distinct_eligible_accounts"] == 1
    assert result["is_hub"] is False


def test_different_dataset_ids_do_not_prove_independence(records):
    # A second acquisition has distinct archive bytes/digest but the same cells.
    other = normalize_synthetic_archive(fixture_archive_bytes() + b"\x00" * 512)[0]
    packet = build_review_packet([records[0], records[13], other],
        subject_accounts=[records[0].observed_account.id, records[13].observed_account.id], population_ref="fixture")
    assert any(r["type"] == "exact_row_match" for r in packet["repetition_references"])
    assert packet["independence"]["key"] is None
    assert packet["validated_evidence_candidates"] == []


def test_html_escapes_untrusted_source(demo):
    from cyber.render import render_review
    demo["normalized_observations"][0]["source_record"]["raw_values"]["description"] = "<script>alert('x')</script>"
    rendered = render_review(demo)
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "http://" not in rendered.replace("https://", "")


def test_hub_validation_cannot_be_claimed_for_bad_address(demo):
    associations = deepcopy(demo["fixture"]["hub_population"])
    for a in associations:
        a["indicator"] = "1BoatSLRHtKNngkdXEeobR76b53LETtpyU"
    result = count_hub(associations[0]["indicator"], associations, snapshot_id=associations[0]["snapshot_id"])
    assert result["distinct_eligible_accounts"] == 0
    assert result["is_hub"] is None


def test_missing_or_inconsistent_provenance_blocks_extraction(records):
    r = records[0]
    r.provenance.row_number = 999
    with pytest.raises(ValueError, match="lineage"):
        extract_indicators(r)


def test_tampered_hub_result_rejected(records, demo):
    indicator = next(i for i in extract_indicators(records[0]) if i["type"] == "bitcoin_base58_lexical")
    hub = deepcopy(demo["hub_check"])
    hub["distinct_eligible_accounts"] = 1000
    with pytest.raises(ValueError, match="replay"):
        screen_indicator(indicator, records[0], hub_result=hub)
