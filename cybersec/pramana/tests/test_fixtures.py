"""
Tests implementing ALL validation fixtures G-01 through G-26.
"""

import pytest
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from adapters.gwern_grams import errors, identifiers as ids
from adapters.gwern_grams.normalizer import normalize_row
from adapters.gwern_grams.csv_parser import parse_csv_member
from adapters.gwern_grams.archive_reader import make_snapshot
from tests.conftest import (
    archive_exists, read_member_bytes, get_member_ordinal, 
    parse_csv_row, build_synthetic_csv, build_synthetic_tar
)

# Helper to normalize a synthetic or real row
def normalize_helper(row: list, ordinal: int = 1, member_name: str = "grams/2014-06-09/1776.csv", row_num: int = 1):
    snapshot_token = member_name.split("/")[1]
    snapshot = make_snapshot(snapshot_token)
    return normalize_row(
        cells=row,
        member_ordinal=ordinal,
        member_name=member_name,
        row_number=row_num,
        snapshot_token=snapshot_token,
        snapshot_id=snapshot.id if snapshot else ids.source_snapshot_id(snapshot_token),
        member_sha256="fakehash",
        member_mtime=1234567890,
        header=list(errors.EXPECTED_HEADER)
    )

def test_g01_normal_listing():
    """G-01 Normal listing: grams/2014-06-09/1776.csv, row 1"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    
    member_name = "grams/2014-06-09/1776.csv"
    data = read_member_bytes(member_name)
    ordinal = get_member_ordinal(member_name)
    row = parse_csv_row(data, 1)
    
    nr = normalize_helper(row, ordinal, member_name, 1)
    
    # Market 1776, vendor ACAB23
    assert nr.observed_account is not None
    assert nr.observed_account.market_name_raw == "1776"
    assert nr.observed_account.vendor_name_raw == "ACAB23"
    assert nr.observed_account.id == ["observed_account", "gwern-grams", "1776", "ACAB23"]
    
    # Amount 50, currency null
    assert nr.listing_observation.price.amount_decimal == "50"
    assert nr.listing_observation.price.currency is None
    
    # Shipping claim Austria
    assert nr.shipping_claim is not None
    assert nr.shipping_claim.raw == "Austria"
    
    # Time integer 1399918210
    assert nr.timestamp.parsed_integer == 1399918210
    assert nr.timestamp.classification == "UNKNOWN"
    assert nr.timestamp.semantic_status == "UNRESOLVED"
    
    # Image reference only, no evidence/persona
    assert nr.image_reference is not None
    assert nr.image_reference.image_bytes_ref is None

def test_g02_missing_description():
    """G-02 Missing description: grams/2014-06-09/Agora.csv, row 9747"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2014-06-09/Agora.csv")
    row = parse_csv_row(data, 9747)
    nr = normalize_helper(row)
    assert nr.listing_observation.description is None
    assert nr.source_record.raw_values["description"] == ""

def test_g03_missing_image():
    """G-03 Missing image: grams/2014-06-09/ADM.csv, row 465"""
    if archive_exists():
        data = read_member_bytes("grams/2014-06-09/ADM.csv")
        row = parse_csv_row(data, 465)
    else:
        # Synthetic fallback
        row = ["hash","ADM","http://link","vendor","5.0","name","desc","","1400000000","ship",""]
    nr = normalize_helper(row)
    assert nr.image_reference is None
    assert nr.source_record.raw_values["image_link"] == ""

def test_g04_missing_shipping():
    """G-04 Missing shipping: grams/2014-06-09/ADM.csv, row 11"""
    if archive_exists():
        data = read_member_bytes("grams/2014-06-09/ADM.csv")
        row = parse_csv_row(data, 11)
    else:
        row = ["hash","ADM","http://link","vendor","5.0","name","desc","http://img","1400000000","",""]
    nr = normalize_helper(row)
    assert nr.shipping_claim is None
    assert nr.source_record.raw_values["ship_from"] == ""

def test_g05_g06_repeated_across_snapshots():
    """
    G-05 Repeated listing across snapshots
    G-06 Same vendor across snapshots
    Abraxas 2015-04-20 row 1 and 2015-04-21 row 1
    """
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
        
    data1 = read_member_bytes("grams/2015-04-20/Abraxas.csv")
    row1 = parse_csv_row(data1, 1)
    ord1 = get_member_ordinal("grams/2015-04-20/Abraxas.csv")
    nr1 = normalize_helper(row1, ord1, "grams/2015-04-20/Abraxas.csv", 1)
    
    data2 = read_member_bytes("grams/2015-04-21/Abraxas.csv")
    row2 = parse_csv_row(data2, 1)
    ord2 = get_member_ordinal("grams/2015-04-21/Abraxas.csv")
    nr2 = normalize_helper(row2, ord2, "grams/2015-04-21/Abraxas.csv", 1)
    
    # G-05: Distinct record/snapshot/listing IDs, equal operands
    assert nr1.source_record.id != nr2.source_record.id
    assert nr1.source_record.snapshot_id != nr2.source_record.snapshot_id
    assert nr1.listing_observation.id != nr2.listing_observation.id
    assert nr1.listing_observation.source_hash_raw == nr2.listing_observation.source_hash_raw
    assert nr1.listing_observation.canonical_listing_id is None
    
    # G-06: Same exact observed account label key
    assert nr1.observed_account.id == nr2.observed_account.id
    assert nr1.observed_account.source_record_id != nr2.observed_account.source_record_id

def test_g07_malformed_price():
    """G-07 Malformed price: Synthetic G-01 with price 'USD 50'"""
    row = ["hash","1776","http://link","vendor","USD 50","name","desc","http://img","1400000000","ship",""]
    nr = normalize_helper(row)
    assert nr.listing_observation.price.raw == "USD 50"
    assert nr.listing_observation.price.parse_status == "invalid_decimal"
    assert nr.listing_observation.price.amount_decimal is None
    assert len(nr.source_record.field_issues) == 1
    assert nr.source_record.field_issues[0].code == errors.INVALID_DECIMAL

def test_g08_malformed_timestamp():
    """G-08 Malformed timestamp: Synthetic G-01 with add_time 'yesterday'"""
    row = ["hash","1776","http://link","vendor","50.0","name","desc","http://img","yesterday","ship",""]
    nr = normalize_helper(row)
    assert nr.timestamp.raw == "yesterday"
    assert nr.timestamp.parse_status == "invalid_integer"
    assert nr.timestamp.parsed_integer is None
    assert nr.timestamp.classification == "UNKNOWN"
    assert len(nr.source_record.field_issues) == 1
    assert nr.source_record.field_issues[0].code == errors.INVALID_INTEGER

def test_g09_duplicate_source_row():
    """G-09 Duplicate source row: Synthetic member containing G-01 twice at rows 1 and 2"""
    row = ["hash","1776","http://link","vendor","50.0","name","desc","http://img","1400000000","ship",""]
    csv_bytes = build_synthetic_csv([row, row])
    header_valid, header_cells, parsed_rows, struct_errs = parse_csv_member(csv_bytes, "grams/2014-06-09/1776.csv")
    assert header_valid
    assert len(parsed_rows) == 2
    
    nr1 = normalize_helper(parsed_rows[0].cells, 1, "grams/2014-06-09/1776.csv", parsed_rows[0].row_number)
    nr2 = normalize_helper(parsed_rows[1].cells, 1, "grams/2014-06-09/1776.csv", parsed_rows[1].row_number)
    
    assert nr1.source_record.id != nr2.source_record.id
    assert nr1.listing_observation.id != nr2.listing_observation.id
    assert nr1.observed_account.id == nr2.observed_account.id

def test_g10_empty_fields_null_like_words():
    """G-10 Empty fields / null-like words: Synthetic blank vendor, desc 'none', name 'nan', ship 'n/a'"""
    row = ["hash","market","http://link","   ","50.0","nan","none","http://img","1400000000","n/a",""]
    nr = normalize_helper(row)
    assert nr.observed_account is None
    assert nr.listing_observation.title == "nan"
    assert nr.listing_observation.description == "none"
    assert nr.shipping_claim is not None
    assert nr.shipping_claim.raw == "n/a"

def test_g11_unicode_vendor():
    """G-11 Unicode vendor: grams/2015-04-04/Alpha.csv, row 1896"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2015-04-04/Alpha.csv")
    row = parse_csv_row(data, 1896)
    nr = normalize_helper(row)
    assert nr.observed_account.vendor_name_raw == "Omega²"
    # Make sure it didn't case fold or NFKC normalize to Omega2
    assert nr.observed_account.vendor_name_raw != "Omega2"

def test_g12_whitespace_vendor():
    """G-12 Whitespace vendor: grams/2014-06-09/Agora.csv, row 1"""
    if archive_exists():
        data = read_member_bytes("grams/2014-06-09/Agora.csv")
        row = parse_csv_row(data, 1)
    else:
        row = ["hash","Agora","http://link"," \t ","50.0","name","desc","http://img","1400000000","ship",""]
    nr = normalize_helper(row)
    assert nr.observed_account is None

def test_g13_whitespace_shipping():
    """G-13 Whitespace shipping: grams/2014-08-25/ADM.csv, row 1237"""
    if archive_exists():
        data = read_member_bytes("grams/2014-08-25/ADM.csv")
        row = parse_csv_row(data, 1237)
    else:
        row = ["hash","ADM","http://link","vendor","50.0","name","desc","http://img","1400000000","   ",""]
    nr = normalize_helper(row)
    assert nr.shipping_claim is None

def test_g14_identical_content_across_markets():
    """G-14 Identical content across markets: 1776 2014-06-09 row 10 and Abraxas 2015-04-20 row 94"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data1 = read_member_bytes("grams/2014-06-09/1776.csv")
    row1 = parse_csv_row(data1, 10)
    nr1 = normalize_helper(row1, member_name="grams/2014-06-09/1776.csv")
    
    data2 = read_member_bytes("grams/2015-04-20/Abraxas.csv")
    row2 = parse_csv_row(data2, 94)
    nr2 = normalize_helper(row2, member_name="grams/2015-04-20/Abraxas.csv")
    
    assert nr1.listing_observation.title == nr2.listing_observation.title
    assert nr1.listing_observation.description == nr2.listing_observation.description
    assert nr1.observed_account.id != nr2.observed_account.id
    assert nr1.listing_observation.canonical_listing_id is None

def test_g15_conflicting_repeated_source_token():
    """G-15 Conflicting repeated source token: ADM 2014-06-15 row 665 and 2014-08-25 row 1453"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data1 = read_member_bytes("grams/2014-06-15/ADM.csv")
    row1 = parse_csv_row(data1, 665)
    nr1 = normalize_helper(row1, member_name="grams/2014-06-15/ADM.csv")
    
    data2 = read_member_bytes("grams/2014-08-25/ADM.csv")
    row2 = parse_csv_row(data2, 1453)
    nr2 = normalize_helper(row2, member_name="grams/2014-08-25/ADM.csv")
    
    assert nr1.listing_observation.source_hash_raw == nr2.listing_observation.source_hash_raw
    assert nr1.observed_account.id != nr2.observed_account.id

def test_g16_changed_add_time():
    """G-16 Changed add_time: Abraxas 2015-04-20 row 4 and 2015-06-02 row 11"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data1 = read_member_bytes("grams/2015-04-20/Abraxas.csv")
    row1 = parse_csv_row(data1, 4)
    nr1 = normalize_helper(row1, member_name="grams/2015-04-20/Abraxas.csv")
    
    data2 = read_member_bytes("grams/2015-06-02/Abraxas.csv")
    row2 = parse_csv_row(data2, 11)
    nr2 = normalize_helper(row2, member_name="grams/2015-06-02/Abraxas.csv")
    
    assert nr1.listing_observation.source_hash_raw == nr2.listing_observation.source_hash_raw
    assert nr1.timestamp.parsed_integer != nr2.timestamp.parsed_integer
    assert nr1.timestamp.semantic_status == "UNRESOLVED"
    assert nr2.timestamp.semantic_status == "UNRESOLVED"

def test_g17_same_day_suffix():
    """G-17 Same-day suffix: grams/2014-06-11-2/Agora.csv, row 1"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    member_name = "grams/2014-06-11-2/Agora.csv"
    data = read_member_bytes(member_name)
    row = parse_csv_row(data, 1)
    nr = normalize_helper(row, member_name=member_name)
    
    assert nr.source_record.snapshot_id == ids.source_snapshot_id("2014-06-11-2")

def test_g18_opaque_image_token():
    """G-18 Opaque image token: grams/2014-08-29/Alpaca.csv, row 2"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2014-08-29/Alpaca.csv")
    row = parse_csv_row(data, 2)
    nr = normalize_helper(row)
    assert nr.image_reference.raw == "18-344"
    assert nr.image_reference.kind == "opaque_reference"

def test_g19_directory_like_image_reference():
    """G-19 Directory-like image reference: Abraxas 2015-04-20 row 1"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2015-04-20/Abraxas.csv")
    row = parse_csv_row(data, 1)
    nr = normalize_helper(row)
    assert nr.image_reference.kind.endswith("_reference_candidate")
    assert nr.image_reference.image_bytes_ref is None

def test_g20_damaged_pgp_like_prose():
    """G-20 Damaged PGP-like prose: Abraxas 2015-04-20 row 4252"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2015-04-20/Abraxas.csv")
    row = parse_csv_row(data, 4252)
    nr = normalize_helper(row)
    assert "BEGIN PGP PUBLIC KEY BLOCK" in nr.listing_observation.description
    # Should not be repaired or altered
    assert nr.source_record.raw_values["description"] == nr.listing_observation.description

def test_g21_trailing_column():
    """G-21 Trailing column: Valid header/row versus synthetic nonempty position 11"""
    row_valid = ["hash","market","http://link","vendor","50.0","name","desc","http://img","1400000000","ship",""]
    csv_bytes_valid = build_synthetic_csv([row_valid])
    ok, _, rows_valid, errs = parse_csv_member(csv_bytes_valid, "grams/2014-06-09/1776.csv")
    assert ok and len(rows_valid) == 1 and not errs
    
    row_invalid = ["hash","market","http://link","vendor","50.0","name","desc","http://img","1400000000","ship","EXTRA"]
    csv_bytes_invalid = build_synthetic_csv([row_invalid])
    ok, _, rows_invalid, errs = parse_csv_member(csv_bytes_invalid, "grams/2014-06-09/1776.csv")
    assert ok  # Header is still valid
    assert not rows_invalid[-1].valid
    assert errs[0][0] == errors.NONEMPTY_TRAILING_CELL

def test_g22_multiline_quoted_cells():
    """G-22 Multiline quoted cells: Source vendor/ship strings with embedded newlines"""
    row = ["hash","market","http://link","vendor\nnewline","50.0","name","desc","http://img","1400000000","ship",""]
    csv_bytes = build_synthetic_csv([row])
    ok, _, parsed_rows, _ = parse_csv_member(csv_bytes, "grams/2014-06-09/1776.csv")
    assert len(parsed_rows) == 1
    nr = normalize_helper(parsed_rows[0].cells)
    assert nr.observed_account.vendor_name_raw == "vendor\nnewline"

def test_g23_url_collision():
    """G-23 URL collision: SilkRoad 2014-06-09 rows 12209 and 12223"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data = read_member_bytes("grams/2014-06-09/SilkRoad.csv")
    row1 = parse_csv_row(data, 12209)
    nr1 = normalize_helper(row1)
    
    row2 = parse_csv_row(data, 12223)
    nr2 = normalize_helper(row2)
    
    assert nr1.listing_observation.source_url_reference == nr2.listing_observation.source_url_reference
    assert nr1.listing_observation.source_hash_raw != nr2.listing_observation.source_hash_raw

def test_g24_hash_is_not_a_digest():
    """G-24 Hash is not a digest: grams/2014-06-09/ADM.csv, row 1"""
    if archive_exists():
        data = read_member_bytes("grams/2014-06-09/ADM.csv")
        row = parse_csv_row(data, 1)
    else:
        row = ["8-TEaDzSDOO3ucVc8KMaoPtAsJ7XVL3MVWq5A0YeOM","ADM","http://link","vendor","50.0","name","desc","http://img","1400000000","ship",""]
    nr = normalize_helper(row)
    assert nr.listing_observation.source_hash_raw == "8-TEaDzSDOO3ucVc8KMaoPtAsJ7XVL3MVWq5A0YeOM"
    assert nr.listing_observation.source_hash_reference == ["source_hash_reference", "gwern-grams", "Andromeda" if row[1]=="Andromeda" else "ADM", "8-TEaDzSDOO3ucVc8KMaoPtAsJ7XVL3MVWq5A0YeOM"]

def test_g25_source_market_spacing():
    """G-25 Source market spacing: grams/2015-06-09/Oxygen .csv, row 1; synthetic identical label without trailing space"""
    if not archive_exists():
        pytest.skip("Deep archive fixture disabled unless --archive-fixtures; archive may also be absent")
    data1 = read_member_bytes("grams/2015-06-09/Oxygen .csv")
    row1 = parse_csv_row(data1, 1)
    nr1 = normalize_helper(row1, member_name="grams/2015-06-09/Oxygen .csv")
    assert nr1.observed_account.market_name_raw == "Oxygen "
    
    row2 = list(row1)
    row2[1] = "Oxygen"
    nr2 = normalize_helper(row2, member_name="grams/2015-06-09/Oxygen .csv")
    assert nr1.observed_account.id != nr2.observed_account.id

def test_g26_integrity_schema_failure():
    """G-26 Integrity/schema failure: extra header"""
    bad_header = list(errors.EXPECTED_HEADER) + ["extra"]
    csv_bytes = build_synthetic_csv([[""] * 12], header=bad_header)
    ok, _, rows, errs = parse_csv_member(csv_bytes, "grams/2014-06-09/1776.csv")
    assert not ok
    assert errs[0][0] == errors.HEADER_MISMATCH
