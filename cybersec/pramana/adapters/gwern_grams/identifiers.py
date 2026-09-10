"""Deterministic identifier construction per Section 13 of GWERN_GRAMS_ADAPTER_SPEC_v1."""

ARCHIVE_SHA256 = "0cecd5e78416328caf06614ee6a8fabee0d91b8aecddd9ca2d67f059ff7497d6"
ADAPTER_VERSION = "GWERN_GRAMS_ADAPTER_SPEC_v1"
SOURCE_NAMESPACE = "gwern-grams"


def source_archive_id() -> list:
    return ["archive", ARCHIVE_SHA256]


def source_member_id(ordinal: int, member_name: str) -> list:
    return ["member", ARCHIVE_SHA256, ordinal, member_name]


def source_snapshot_id(snapshot_token: str) -> list:
    return ["snapshot", ARCHIVE_SHA256, snapshot_token]


def source_record_id(ordinal: int, member_name: str, row_number: int) -> list:
    return ["record", ARCHIVE_SHA256, ordinal, member_name, row_number]


def observed_account_id(market_name_raw: str, vendor_name_raw: str) -> list:
    return ["observed_account", SOURCE_NAMESPACE, market_name_raw, vendor_name_raw]


def listing_observation_id(record_id: list) -> list:
    return ["listing_observation", record_id]


def image_reference_id(record_id: list) -> list:
    return ["image_reference", record_id, 8]


def shipping_claim_id(record_id: list) -> list:
    return ["shipping_claim", record_id, 10]


def timestamp_id(record_id: list) -> list:
    return ["source_time", record_id, 9]


def field_ref(record_id: list, column_position: int, header_name: str) -> list:
    return [record_id, column_position, header_name]


def source_hash_reference(market_name_raw: str, hash_raw: str) -> list:
    return ["source_hash_reference", SOURCE_NAMESPACE, market_name_raw, hash_raw]


def source_url_reference(market_name_raw: str, item_link_raw: str) -> list:
    return ["source_url_reference", SOURCE_NAMESPACE, market_name_raw, item_link_raw]
