"""Normalized object dataclasses per Section 16 of GWERN_GRAMS_ADAPTER_SPEC_v1."""

from __future__ import annotations
from dataclasses import dataclass, field as dc_field
from typing import Optional


@dataclass
class FieldIssue:
    field_position: int
    field_name: str
    code: str
    raw_value: str


@dataclass
class FieldRef:
    record_id: list
    column_position: int
    header_name: str


@dataclass
class SourceRecord:
    id: list
    archive_id: list
    member_id: list
    snapshot_id: list
    row_number: int
    raw_values: dict
    trailing_empty_cell: str
    field_issues: list
    adapter_version: str


@dataclass
class SourceSnapshot:
    id: list
    archive_id: list
    label_raw: str
    date_label: str
    suffix_raw: str
    meaning: str
    timezone: None = None
    capture_instant: None = None


@dataclass
class ObservedAccount:
    id: list
    source_namespace: str
    market_name_raw: str
    vendor_name_raw: str
    source_record_id: list
    market_field_ref: FieldRef
    vendor_field_ref: FieldRef


@dataclass
class PriceObject:
    raw: str
    parse_status: str
    amount_decimal: Optional[str]
    currency: None = None
    field_ref: Optional[FieldRef] = None


@dataclass
class ItemReference:
    raw: str
    kind: str
    field_ref: Optional[FieldRef] = None


@dataclass
class ListingObservation:
    id: list
    source_record_id: list
    snapshot_id: list
    source_hash_raw: str
    source_hash_reference: Optional[list]
    source_url_reference: Optional[list]
    item_reference: Optional[ItemReference]
    observed_account_id: Optional[list]
    title: Optional[str]
    description: Optional[str]
    price: PriceObject
    canonical_listing_id: None = None
    canonical_artefact_id: None = None


@dataclass
class ImageReference:
    id: list
    source_record_id: list
    raw: str
    kind: str
    field_ref: FieldRef
    image_bytes_ref: None = None
    verified_archive_image_member: None = None


@dataclass
class Timestamp:
    id: list
    source_record_id: list
    field_ref: FieldRef
    raw: str
    parse_status: str
    parsed_integer: Optional[int]
    classification: str = "UNKNOWN"
    semantic_status: str = "UNRESOLVED"
    epoch: None = None
    unit: None = None
    timezone: None = None
    instant: None = None


@dataclass
class ShippingClaim:
    id: list
    source_record_id: list
    raw: str
    interpretation: str = "unverified_source_claim"
    field_ref: Optional[FieldRef] = None
    country_code: None = None
    actual_location: None = None


@dataclass
class Provenance:
    archive_id: list
    archive_sha256: str
    member_id: list
    member_name_raw: str
    member_ordinal: int
    member_sha256: Optional[str]
    snapshot_id: list
    row_number: int
    schema_header: list
    adapter_version: str
    acquisition_uri: Optional[str] = None
    acquired_at: Optional[str] = None
    acquisition_report_ref: Optional[str] = None
    archive_member_mtime: Optional[int] = None


@dataclass
class Relation:
    type: str
    from_id: list
    to_id: list
    source_record_id: list
    field_refs: list


@dataclass
class StructuralError:
    category: str
    member_name: Optional[str]
    member_ordinal: Optional[int]
    row_number: Optional[int]
    detail: str


@dataclass
class NormalizedRecord:
    source_record: SourceRecord
    listing_observation: ListingObservation
    observed_account: Optional[ObservedAccount]
    image_reference: Optional[ImageReference]
    timestamp: Timestamp
    shipping_claim: Optional[ShippingClaim]
    provenance: Provenance
    relations: list


@dataclass
class MemberResult:
    member_id: list
    member_name: str
    member_ordinal: int
    snapshot: Optional[SourceSnapshot]
    is_csv: bool
    accepted: bool
    record_count: int
    records: list
    structural_errors: list
    member_sha256: Optional[str]


@dataclass
class AdapterResult:
    archive_id: list
    archive_sha256: str
    archive_valid: bool
    adapter_version: str
    total_members: int
    csv_members: int
    non_csv_members: int
    accepted_members: int
    rejected_members: int
    total_records: int
    field_issues_by_type: dict
    snapshots: dict
    member_results: list
    structural_errors: list
