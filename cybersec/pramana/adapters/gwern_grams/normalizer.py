"""Deterministic normalizer implementing N-01 through N-10."""

import re
from typing import Optional
from decimal import Decimal, InvalidOperation

from . import errors
from . import identifiers as ids
from .models import (
    FieldIssue, FieldRef, SourceRecord, ObservedAccount, PriceObject,
    ItemReference, ListingObservation, ImageReference, Timestamp,
    ShippingClaim, Provenance, Relation, NormalizedRecord,
)
from .csv_parser import raw_values_dict

# N-05: exact price grammar
_PRICE_RE = re.compile(r"^[0-9]+\.[0-9]+$")

# N-07: exactly 10 ASCII digits
_ADD_TIME_RE = re.compile(r"^[0-9]{10}$")


def _is_present(s: str) -> bool:
    """True if removing only boundary ASCII whitespace leaves at least one character (§5.2)."""
    return len(s.strip(" \t\n\r\x0b\x0c")) > 0


def _classify_reference(raw: str) -> str:
    """N-06: classify by exact prefix only."""
    if raw.startswith("http://"):
        return "http_reference_candidate"
    elif raw.startswith("https://"):
        return "https_reference_candidate"
    else:
        return "opaque_reference"


def _normalize_price(raw: str) -> tuple:
    """
    N-05: parse price string.
    Returns (parse_status, amount_decimal_str_or_None, field_issue_or_None).
    """
    if not _is_present(raw):
        return "missing", None, None

    if not _PRICE_RE.fullmatch(raw):
        return "invalid_decimal", None, FieldIssue(
            field_position=5, field_name="price",
            code=errors.INVALID_DECIMAL, raw_value=raw
        )

    # Arbitrary-precision decimal, canonical serialization per N-05:
    # Remove redundant leading zeros from integer part, trailing zeros from fractional part.
    # Remove decimal point if no fractional digits remain. Zero serializes as "0".
    d = Decimal(raw)
    # Normalize: remove trailing fractional zeros
    # Decimal('50.00000000') -> Decimal('5E+1') with normalize, but we need "50"
    # Use custom serialization
    sign, digits, exponent = d.as_tuple()
    # Reconstruct without exponent notation
    num_digits = len(digits)
    if exponent >= 0:
        # No fractional part
        int_str = "".join(str(d) for d in digits) + "0" * exponent
        result = int_str.lstrip("0") or "0"
    else:
        # Has fractional part
        abs_exp = -exponent
        if num_digits <= abs_exp:
            # All digits are fractional: e.g., 0.005
            frac = "0" * (abs_exp - num_digits) + "".join(str(d) for d in digits)
            frac = frac.rstrip("0")
            if frac:
                result = "0." + frac
            else:
                result = "0"
        else:
            int_part = "".join(str(d) for d in digits[:num_digits - abs_exp])
            frac_part = "".join(str(d) for d in digits[num_digits - abs_exp:])
            frac_part = frac_part.rstrip("0")
            int_part = int_part.lstrip("0") or "0"
            if frac_part:
                result = int_part + "." + frac_part
            else:
                result = int_part

    return "parsed_decimal", result, None


def _normalize_add_time(raw: str) -> tuple:
    """
    N-07: parse add_time.
    Returns (parse_status, parsed_integer_or_None, field_issue_or_None).
    """
    if not _is_present(raw):
        return "missing", None, None

    if _ADD_TIME_RE.fullmatch(raw):
        return "parsed_integer", int(raw), None

    return "invalid_integer", None, FieldIssue(
        field_position=9, field_name="add_time",
        code=errors.INVALID_INTEGER, raw_value=raw
    )


def normalize_row(cells: list, member_ordinal: int, member_name: str,
                   row_number: int, snapshot_token: str,
                   snapshot_id: list, member_sha256: Optional[str],
                   member_mtime: Optional[int],
                   header: list, *, fixture_archive_sha256: Optional[str] = None) -> NormalizedRecord:
    """
    Normalize one valid 11-cell CSV row into a complete NormalizedRecord.
    Implements N-01 through N-10 and §13/§16 contracts.
    """
    raw = raw_values_dict(cells)
    record_id = ids.source_record_id(member_ordinal, member_name, row_number)
    archive_id = ids.source_archive_id()
    member_id = ids.source_member_id(member_ordinal, member_name)
    archive_digest = ids.ARCHIVE_SHA256
    source_namespace = ids.SOURCE_NAMESPACE
    if fixture_archive_sha256 is not None:
        # Explicit synthetic-fixture scope; the production archive runner never sets it.
        if not re.fullmatch(r"[0-9a-f]{64}", fixture_archive_sha256):
            raise ValueError("Synthetic archive digest must be SHA-256")
        archive_digest = fixture_archive_sha256
        source_namespace = "synthetic-grams"
        record_id = ["record", archive_digest, member_ordinal, member_name, row_number]
        archive_id = ["archive", archive_digest]
        member_id = ["member", archive_digest, member_ordinal, member_name]
        snapshot_id = ["snapshot", archive_digest, snapshot_token]
    field_issues = []

    # --- Field refs ---
    def fref(col: int, name: str) -> FieldRef:
        return FieldRef(record_id=record_id, column_position=col, header_name=name)

    # --- Price (N-05) ---
    price_status, price_amount, price_issue = _normalize_price(raw["price"])
    if price_issue:
        field_issues.append(price_issue)
    price_obj = PriceObject(
        raw=raw["price"],
        parse_status=price_status,
        amount_decimal=price_amount,
        currency=None,
        field_ref=fref(5, "price"),
    )

    # --- Timestamp (N-07) ---
    time_status, time_int, time_issue = _normalize_add_time(raw["add_time"])
    if time_issue:
        field_issues.append(time_issue)
    ts = Timestamp(
        id=ids.timestamp_id(record_id),
        source_record_id=record_id,
        field_ref=fref(9, "add_time"),
        raw=raw["add_time"],
        parse_status=time_status,
        parsed_integer=time_int,
    )

    # --- Observed account (N-04, §5.2, §16.3) ---
    market_present = _is_present(raw["market_name"])
    vendor_present = _is_present(raw["vendor_name"])
    observed_account = None
    observed_account_id_val = None
    if market_present and vendor_present:
        observed_account_id_val = ids.observed_account_id(
            raw["market_name"], raw["vendor_name"]
        )
        observed_account_id_val[1] = source_namespace
        observed_account = ObservedAccount(
            id=observed_account_id_val,
            source_namespace=source_namespace,
            market_name_raw=raw["market_name"],
            vendor_name_raw=raw["vendor_name"],
            source_record_id=record_id,
            market_field_ref=fref(2, "market_name"),
            vendor_field_ref=fref(4, "vendor_name"),
        )

    # --- Item reference (N-06) ---
    item_ref = None
    if _is_present(raw["item_link"]):
        item_ref = ItemReference(
            raw=raw["item_link"],
            kind=_classify_reference(raw["item_link"]),
            field_ref=fref(3, "item_link"),
        )

    # --- Source hash/URL references ---
    hash_ref = None
    if market_present and _is_present(raw["hash"]):
        hash_ref = ids.source_hash_reference(raw["market_name"], raw["hash"])
        hash_ref[1] = source_namespace

    url_ref = None
    if market_present and _is_present(raw["item_link"]):
        url_ref = ids.source_url_reference(raw["market_name"], raw["item_link"])
        url_ref[1] = source_namespace

    # --- Title / description (N-03, N-04) ---
    title = raw["name"] if _is_present(raw["name"]) else None
    description = raw["description"] if _is_present(raw["description"]) else None

    # --- Image reference (N-06, §16.5) ---
    image_reference = None
    if _is_present(raw["image_link"]):
        image_reference = ImageReference(
            id=ids.image_reference_id(record_id),
            source_record_id=record_id,
            raw=raw["image_link"],
            kind=_classify_reference(raw["image_link"]),
            field_ref=fref(8, "image_link"),
        )

    # --- Shipping claim (N-09, §16.7) ---
    shipping_claim = None
    if _is_present(raw["ship_from"]):
        shipping_claim = ShippingClaim(
            id=ids.shipping_claim_id(record_id),
            source_record_id=record_id,
            raw=raw["ship_from"],
            interpretation="unverified_source_claim",
            field_ref=fref(10, "ship_from"),
        )

    # --- Listing observation (§16.4) ---
    listing_obs_id = ids.listing_observation_id(record_id)
    listing_obs = ListingObservation(
        id=listing_obs_id,
        source_record_id=record_id,
        snapshot_id=snapshot_id,
        source_hash_raw=raw["hash"],
        source_hash_reference=hash_ref,
        source_url_reference=url_ref,
        item_reference=item_ref,
        observed_account_id=observed_account_id_val,
        title=title,
        description=description,
        price=price_obj,
        canonical_listing_id=None,
        canonical_artefact_id=None,
    )

    # --- Source record (§16.1) ---
    source_rec = SourceRecord(
        id=record_id,
        archive_id=archive_id,
        member_id=member_id,
        snapshot_id=snapshot_id,
        row_number=row_number,
        raw_values=raw,
        trailing_empty_cell=cells[10],
        field_issues=field_issues,
        adapter_version=ids.ADAPTER_VERSION,
    )

    # --- Provenance (§16.8) ---
    provenance = Provenance(
        archive_id=archive_id,
        archive_sha256=archive_digest,
        member_id=member_id,
        member_name_raw=member_name,
        member_ordinal=member_ordinal,
        member_sha256=member_sha256,
        snapshot_id=snapshot_id,
        row_number=row_number,
        schema_header=list(header),
        adapter_version=ids.ADAPTER_VERSION,
        archive_member_mtime=member_mtime,
    )

    # --- Relations (§16.9) ---
    relations = []
    # record_in_snapshot
    relations.append(Relation(
        type="record_in_snapshot",
        from_id=record_id,
        to_id=snapshot_id,
        source_record_id=record_id,
        field_refs=[],
    ))
    # listing_observed_in_record
    relations.append(Relation(
        type="listing_observed_in_record",
        from_id=listing_obs_id,
        to_id=record_id,
        source_record_id=record_id,
        field_refs=[],
    ))
    # record_declares_vendor
    if observed_account is not None:
        relations.append(Relation(
            type="record_declares_vendor",
            from_id=record_id,
            to_id=observed_account_id_val,
            source_record_id=record_id,
            field_refs=[fref(2, "market_name"), fref(4, "vendor_name")],
        ))
    # record_has_image_reference
    if image_reference is not None:
        relations.append(Relation(
            type="record_has_image_reference",
            from_id=record_id,
            to_id=image_reference.id,
            source_record_id=record_id,
            field_refs=[fref(8, "image_link")],
        ))
    # record_has_shipping_claim
    if shipping_claim is not None:
        relations.append(Relation(
            type="record_has_shipping_claim",
            from_id=record_id,
            to_id=shipping_claim.id,
            source_record_id=record_id,
            field_refs=[fref(10, "ship_from")],
        ))
    # record_has_time_value — always present per §16.9
    relations.append(Relation(
        type="record_has_time_value",
        from_id=record_id,
        to_id=ts.id,
        source_record_id=record_id,
        field_refs=[fref(9, "add_time")],
    ))

    return NormalizedRecord(
        source_record=source_rec,
        listing_observation=listing_obs,
        observed_account=observed_account,
        image_reference=image_reference,
        timestamp=ts,
        shipping_claim=shipping_claim,
        provenance=provenance,
        relations=relations,
    )
