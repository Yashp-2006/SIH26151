"""Bounded, offline review packet. This is not an assessment or evidence row."""

from dataclasses import asdict
from canonicalization.runner import CanonicalizationPipeline
from adapters.gwern_grams.runner import record_to_dict
from .indicators import extract_indicators, UNSUPPORTED, VERSION
from .policy import screen_indicator, stable_key, positive_band_ceiling


def build_review_packet(records, *, subject_accounts, population_ref, hub_result=None,
                        clone_decisions=None):
    if len(subject_accounts) != 2 or subject_accounts[0] == subject_accounts[1]:
        raise ValueError("Two distinct observed-account subjects required")
    if not population_ref:
        raise ValueError("Declared reference population required")
    by_id = {stable_key(r.source_record.id): r for r in records}
    if len(by_id) != len(records):
        raise ValueError("Duplicate occurrence IDs; repeated records need separate row lineage")
    known = {stable_key(r.observed_account.id) for r in records if r.observed_account}
    if any(stable_key(a) not in known for a in subject_accounts):
        raise ValueError("Subjects must be source-observed accounts in this packet")
    pipeline = CanonicalizationPipeline()
    pipeline.process_records(records)
    repetitions = [asdict(r) for r in pipeline.extract_repetition_references()]
    discrepancies = []
    for ref in repetitions:
        left = by_id[stable_key(ref["from_record_id"])].source_record.raw_values
        right = by_id[stable_key(ref["to_record_id"])].source_record.raw_values
        reason = None
        if ref["type"] == "repeated_market_hash" and left["vendor_name"] != right["vendor_name"]:
            reason = "same_source_hash_changed_vendor; not_handover_proof"
        if ref["type"] == "repeated_market_item_link" and left["hash"] != right["hash"]:
            reason = "same_url_different_source_hash; not_canonical_identity"
        if reason:
            discrepancies.append({"reason": reason, "reference": ref,
                                  "effect": "review_only", "negative_evidence": False})
    indicators, review_items, missing = [], [], []
    clone_decisions = clone_decisions or {}
    for record in records:
        for field in ("name", "description", "vendor_name", "image_link", "ship_from"):
            if not record.source_record.raw_values[field].strip(" \t\r\n\v\f"):
                missing.append({"record_id": record.source_record.id, "field": field,
                                "status": "unavailable", "negative_evidence": False})
        for indicator in extract_indicators(record):
            indicators.append(indicator)
            matching_hub = hub_result if (hub_result and hub_result["indicator"] == indicator["raw"]
                                         and hub_result["snapshot_id"] == indicator["snapshot_id"]
                                         and indicator["validation"] == "checksum_valid") else None
            review_items.append(screen_indicator(
                indicator, record, hub_result=matching_hub,
                confirmed_clone_ref=clone_decisions.get(stable_key(indicator["id"]))))
    checks = [
        {"class": "temporal_impossibility", "status": "unimplemented", "effect": "none", "blocker": "DC-05"},
        {"class": "language_competence", "status": "unimplemented", "effect": "none", "blocker": "DC-09"},
        {"class": "lifecycle_contradiction", "status": "unimplemented", "effect": "none",
         "note": "Source discrepancies above are not a qualified lifecycle detector."},
        {"class": "independence_collapse", "status": "inconclusive", "effect": "no_independence_claim",
         "note": "Exact repetition operands computed; general origin adjudication/grouping deferred DC-01."},
        {"class": "hub_rarity_contradiction", "status": hub_result["population_status"] if hub_result else "not_run",
         "finding": hub_result["is_hub"] if hub_result else None, "effect": "suppression_only" if hub_result and hub_result["is_hub"] else "none"},
        {"class": "shared_infrastructure_alternative", "status": "unimplemented", "effect": "none"},
        {"class": "framing_pattern", "status": "unimplemented", "effect": "none"},
    ]
    return {
        "version": "cyber-review-packet-v1", "extractor_version": VERSION,
        "stage": "REVIEWABLE_ASSESSMENT_INPUT", "review_state": "awaiting_human_review",
        "hypothesis_input": {"subjects": subject_accounts,
            "proposition": "Do the two observed accounts share an operator within the selected source scope?",
            "defence": "Separate operators may share public identifiers, templates or copied listings.",
            "temporal_scope": "selected snapshot labels only; actor event times unknown",
            "reference_population": population_ref},
        "normalized_observations": [record_to_dict(r) for r in records],
        "deterministic_indicators": indicators,
        "ml_feature_boundary": {"status": "deterministic_inputs_available; no_model_run",
                                "indicator_ids": [i["id"] for i in indicators]},
        "promotion_review_items": review_items,
        "validated_evidence_candidates": [], "authoritative_evidence": [],
        "promotion_status": "blocked_DC-06", "repetition_references": repetitions,
        "source_discrepancies": discrepancies, "missing_information": missing,
        "independence": {"status": "deferred_DC-01", "key": None, "eligible_k": None,
                         "rule": "No independent support inferred from records, datasets or transforms."},
        "counter_checks": checks, "hub_check": hub_result,
        "positive_band_guard": positive_band_ceiling(None),
        "assessment": None, "score": None, "hard_veto": {"status": "deferred_DC-05", "result": None},
        "unsupported": UNSUPPORTED,
    }
