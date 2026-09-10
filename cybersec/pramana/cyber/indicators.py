"""CY-POL-005/008/014/015/018: source-bound derivations, not attribution.

Offsets are zero-based, half-open Python Unicode code-point positions in the
decoded original CSV cell. No Unicode normalization, repair or field joining.
"""

from dataclasses import asdict
import hashlib
import re

VERSION = "cyber-indicators-v1"
BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
# ASCII alphanumeric boundaries prevent harvesting pieces of longer tokens.
BTC_PATTERN = re.compile(r"(?<![A-Za-z0-9])[13][1-9A-HJ-NP-Za-km-z]{25,34}(?![A-Za-z0-9])")
PGP_PATTERN = re.compile(r"(?:-----)?BEGIN PGP (?:PUBLIC KEY BLOCK|MESSAGE|SIGNATURE)(?:-----)?")


def validate_bitcoin_base58check(value):
    """Legacy mainnet P2PKH/P2SH format only; no chain/control validation."""
    if not isinstance(value, str) or not 26 <= len(value) <= 35:
        return "invalid_length"
    if any(c not in BASE58 for c in value):
        return "invalid_alphabet"
    number = 0
    for c in value:
        number = number * 58 + BASE58.index(c)
    decoded = number.to_bytes((number.bit_length() + 7) // 8, "big")
    decoded = b"\x00" * (len(value) - len(value.lstrip("1"))) + decoded
    if len(decoded) != 25:
        return "invalid_payload_length"
    if decoded[0] not in (0, 5):
        return "unsupported_version"
    expected = hashlib.sha256(hashlib.sha256(decoded[:-4]).digest()).digest()[:4]
    return "checksum_valid" if decoded[-4:] == expected else "invalid_checksum"


def extract_indicators(record):
    """Extract only observed modalities. A result's family is eligibility, not weight."""
    sr = record.source_record
    p = record.provenance
    if p is None or not re.fullmatch(r"[0-9a-f]{64}", p.archive_sha256 or "") or not re.fullmatch(r"[0-9a-f]{64}", p.member_sha256 or ""):
        raise ValueError("Archive/member integrity provenance required")
    expected_record = ["record", p.archive_sha256, p.member_ordinal, p.member_name_raw, p.row_number]
    expected_member = ["member", p.archive_sha256, p.member_ordinal, p.member_name_raw]
    if (sr.id != expected_record or sr.member_id != expected_member or p.member_id != expected_member
            or sr.archive_id != ["archive", p.archive_sha256] or p.archive_id != sr.archive_id
            or sr.snapshot_id != p.snapshot_id or sr.row_number != p.row_number
            or record.listing_observation.source_record_id != sr.id
            or record.listing_observation.snapshot_id != sr.snapshot_id):
        raise ValueError("Inconsistent normalized source lineage")
    if record.observed_account is not None:
        account = record.observed_account
        expected_account = ["observed_account", account.source_namespace,
                            sr.raw_values["market_name"], sr.raw_values["vendor_name"]]
        if (account.id != expected_account or account.source_record_id != sr.id
                or record.listing_observation.observed_account_id != account.id):
            raise ValueError("Inconsistent observed-account lineage")
    elif record.listing_observation.observed_account_id is not None:
        raise ValueError("Unbacked observed-account reference")
    result = []
    for field, position in (("name", 6), ("description", 7)):
        text = sr.raw_values[field]
        spans = []
        if text.strip(" \t\r\n\v\f"):
            spans.append((0, len(text), "text_content", "F5", "exact_source_span"))
        for m in PGP_PATTERN.finditer(text):
            spans.append((*m.span(), "pgp_like_marker", "F1", "unvalidated_pgp_material"))
        for m in BTC_PATTERN.finditer(text):
            spans.append((*m.span(), "bitcoin_base58_lexical", "F2",
                          validate_bitcoin_base58check(m.group())))
        for start, end, kind, family, validation in sorted(spans):
            raw = text[start:end]
            result.append({
                "id": ["indicator", VERSION, sr.id, position, start, end, kind],
                "stage": "DETERMINISTIC_DERIVATION", "type": kind,
                "eligible_family": family, "validation": validation,
                "raw": raw, "start": start, "end": end,
                "offset_unit": "unicode_code_points", "field_ref": [sr.id, position, field],
                "source_record_id": sr.id, "snapshot_id": sr.snapshot_id,
                "observed_account_id": record.listing_observation.observed_account_id,
                "provenance": asdict(record.provenance), "validator_version": VERSION,
                "value_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "canonical_artefact_id": None, "independence_key": None,
                "authoritative_evidence": False,
                "interpretation": "source_occurrence_only; no ownership or control",
            })
    return result


def verify_indicator_span(indicator, record):
    """Re-derive and compare the complete payload; caller flags cannot self-promote."""
    try:
        return any(indicator == expected for expected in extract_indicators(record))
    except (ValueError, TypeError, AttributeError):
        return False


UNSUPPORTED = {
    "pgp_key_or_signature_validation": "Not implemented; markers are not keys or signatures (F1).",
    "other_crypto_formats": "Bech32, XMR and other formats are not implemented; no absence claim.",
    "contact_identifier": "No verified CSV contact-ID fixture; contact words alone do not support F4.",
    "infrastructure_telemetry": "CSV URLs are context, not F3 telemetry.",
    "image_features": "No verified CSV-to-image-byte join; references only.",
    "stylometry": "F6 gates/model not implemented; no style evidence.",
    "event_behaviour": "F7 event/time contract unavailable for add_time.",
    "social_trust": "F8 generator unavailable (DC-08).",
    "external_corroboration": "F9 generator unavailable (DC-08).",
}
