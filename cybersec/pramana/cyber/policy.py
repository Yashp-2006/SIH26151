"""Executable frozen restrictions only. No scoring, grouping or promotion engine."""

import json
from .indicators import verify_indicator_span, validate_bitcoin_base58check


def stable_key(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def count_hub(indicator_raw, associations, *, snapshot_id):
    """CY-POL-023; population is supplied/qualified, never inferred from raw mention count.

    Each association has indicator, account_id, snapshot_id, record_id,
    validation, eligibility, lineage and decision_ref. Eligibility is eligible,
    rejected, quarantined or unknown; lineage is original, mirror, confirmed_clone
    or unknown. Unknown eligibility/origin prevents a definitive non-hub result.
    """
    if not snapshot_id or not indicator_raw:
        raise ValueError("Declared population snapshot and exact indicator required")
    accounts, sites, included, excluded, unresolved = set(), set(), [], [], []
    for a in associations:
        required = {"indicator", "account_id", "snapshot_id", "record_id", "validation",
                    "eligibility", "lineage", "decision_ref"}
        if not required <= a.keys():
            raise ValueError("Incomplete indicator-account association")
        if a["snapshot_id"] != snapshot_id:
            raise ValueError("Mixed population snapshots")
        if a["indicator"] != indicator_raw:
            raise ValueError("Mixed indicators")
        if a["eligibility"] not in {"eligible", "rejected", "quarantined", "unknown"}:
            raise ValueError("Unknown eligibility state")
        if a["lineage"] not in {"original", "mirror", "confirmed_clone", "unknown"}:
            raise ValueError("Unknown origin state")
        if not a["record_id"]:
            raise ValueError("Missing observation lineage")
        if a["eligibility"] in {"rejected", "quarantined"} or a["lineage"] in {"mirror", "confirmed_clone"}:
            excluded.append(a)
            continue
        account = a["account_id"]
        if (a["validation"] != "checksum_valid" or validate_bitcoin_base58check(indicator_raw) != "checksum_valid"
                or a["eligibility"] != "eligible"
                or a["lineage"] != "original" or not a["decision_ref"] or not account):
            unresolved.append(a)
            continue
        if (not isinstance(account, list) or len(account) != 4
                or account[0] != "observed_account" or not all(isinstance(x, str) and x for x in account)):
            raise ValueError("Expected scoped observed-account tuple")
        accounts.add(stable_key(account))
        sites.add(stable_key(account[1:3]))
        included.append(a)
    hub = len(accounts) > 12
    return {"rule": "CY-POL-023", "indicator": indicator_raw, "snapshot_id": snapshot_id,
            "threshold": 12, "distinct_eligible_accounts": len(accounts), "distinct_sites": len(sites),
            "is_hub": True if hub else (None if unresolved else False),
            "population_status": "inconclusive" if unresolved else "completed",
            "included": included, "excluded": excluded, "unresolved": unresolved,
            "positive_support_suppressed": hub, "negative_evidence": False,
            "scope": "declared_associations_only; not corpus rarity"}


def positive_band_ceiling(eligible_k):
    """CY-POL-013 policy guard, NOT a k calculator or assessment.

    Does not upgrade zero/negative support; no input score is supplied or emitted.
    """
    if eligible_k is None:
        return {"status": "deferred_DC-01", "maximum_positive_band": None}
    if type(eligible_k) is not int or eligible_k < 0:
        raise ValueError("eligible_k must be an approved nonnegative integer or unknown")
    return {"status": "restriction_only", "maximum_positive_band": "Weak" if eligible_k < 2 else None}


def screen_indicator(indicator, record, *, confirmed_clone_ref=None, hub_result=None):
    """Validate derivation then return a non-promoted review item.

    No upstream policy flag can approve DC-06. Clone ref is an explicit external
    determination covering this occurrence, not the canonicalizer's similarity.
    """
    if not verify_indicator_span(indicator, record):
        return {"indicator_id": indicator.get("id"), "status": "invalid_derivation",
                "promotion": "blocked", "reasons": ["source_span_or_payload_mismatch"]}
    suppressions = []
    if confirmed_clone_ref is not None:
        if not isinstance(confirmed_clone_ref, str) or not confirmed_clone_ref.strip():
            raise ValueError("Clone determination reference required")
        suppressions.append({"rule": "CY-POL-018", "reason": "confirmed_clone_lineage",
                             "determination_ref": confirmed_clone_ref})
    if hub_result is not None:
        replayed = count_hub(hub_result["indicator"], hub_result["included"] + hub_result["excluded"] + hub_result["unresolved"],
                            snapshot_id=hub_result["snapshot_id"])
        if replayed != hub_result:
            raise ValueError("Hub result does not replay from its population")
        if (hub_result["indicator"] != indicator["raw"]
                or indicator["validation"] != "checksum_valid"
                or hub_result["snapshot_id"] != indicator["snapshot_id"]):
            raise ValueError("Hub restriction must refer to this validated indicator")
        if hub_result["positive_support_suppressed"]:
            suppressions.append({"rule": "CY-POL-023", "reason": "hub",
                                 "snapshot_id": hub_result["snapshot_id"]})
    if indicator["type"] == "pgp_like_marker":
        suppressions.append({"rule": "CY-POL-014", "reason": "no_validated_signed_material; no_positive_F1"})
    blockers = ["DC-06_promotion_contract", "DC-01_origin_grouping", "source_qualification_required"]
    if indicator["type"] == "bitcoin_base58_lexical":
        if indicator["validation"] != "checksum_valid":
            blockers.append("address_validation_failed")
        blockers.append("address_context_and_proposition_not_validated")
    if indicator["type"] == "text_content":
        blockers.append("non_boilerplate_reuse_and_origin_not_validated")
    return {"indicator_id": indicator["id"], "status": "validated_derivation_only",
            "eligible_family": indicator["eligible_family"], "promotion": "blocked",
            "blockers": blockers, "suppressions": suppressions,
            "positive_support_allowed": False, "negative_evidence": False,
            "canonical_artefact_id": None, "independence_key": None,
            "provenance": indicator["provenance"], "field_ref": indicator["field_ref"]}
