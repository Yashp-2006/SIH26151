"""Tests for the Canonicalization and Repetition layer."""

import pytest
from canonicalization.runner import CanonicalizationPipeline
from canonicalization.text_hashing import compute_sha256, compute_simhash, _tokenize, compute_shingles
from adapters.gwern_grams.identifiers import source_record_id, source_snapshot_id, source_archive_id
from adapters.gwern_grams.models import NormalizedRecord, SourceRecord, ListingObservation, ObservedAccount, PriceObject

def mock_record(ordinal: int, row_num: int, m_name: str, h_val: str, url: str, vendor: str, title: str, desc: str, snap: str) -> NormalizedRecord:
    rec_id = source_record_id(ordinal, f"grams/{snap}/{m_name}.csv", row_num)
    raw = {
        "hash": h_val,
        "market_name": m_name,
        "item_link": url,
        "vendor_name": vendor,
        "price": "50.0",
        "name": title,
        "description": desc,
        "image_link": "http://img",
        "add_time": "1400000000",
        "ship_from": "earth"
    }
    
    sr = SourceRecord(
        id=rec_id, archive_id=source_archive_id(), member_id=["member", "hash", ordinal, m_name],
        snapshot_id=source_snapshot_id(snap), row_number=row_num, raw_values=raw,
        trailing_empty_cell="", field_issues=[], adapter_version="test"
    )
    
    lo = ListingObservation(
        id=["lo", rec_id], source_record_id=rec_id, snapshot_id=sr.snapshot_id,
        source_hash_raw=h_val, source_hash_reference=None, source_url_reference=None,
        item_reference=None, observed_account_id=["oa", vendor], title=title, description=desc,
        price=PriceObject("50.0", "parsed_decimal", "50")
    )
    
    oa = ObservedAccount(["oa", vendor], "gwern-grams", m_name, vendor, rec_id, None, None)
    
    return NormalizedRecord(
        source_record=sr, listing_observation=lo, observed_account=oa,
        image_reference=None, timestamp=None, shipping_claim=None,
        provenance=None, relations=[]
    )

def test_exact_duplicate_across_snapshots():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "t1", "d1", "snap1")
    r2 = mock_record(2, 1, "m1", "h1", "u1", "v1", "t1", "d1", "snap2")
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    
    exact_refs = [r for r in refs if r.type == "exact_row_match"]
    assert len(exact_refs) == 1
    assert exact_refs[0].cross_snapshot is True
    
    # Must preserve all source occurrences (both r1 and r2 exist)
    assert len(pipeline.exact_rows[list(pipeline.exact_rows.keys())[0]]) == 2

def test_same_hash_different_content():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "t1", "d1", "snap1")
    r2 = mock_record(2, 2, "m1", "h1", "u2", "v2", "t2", "d2", "snap1")
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    
    h_refs = [r for r in refs if r.type == "repeated_market_hash"]
    assert len(h_refs) == 1
    
    c_refs = [r for r in refs if r.type == "exact_content_match"]
    assert len(c_refs) == 0

def test_same_url_different_hash():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "t1", "d1", "snap1")
    r2 = mock_record(2, 2, "m1", "h2", "u1", "v1", "t2", "d2", "snap1")
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    
    u_refs = [r for r in refs if r.type == "repeated_market_item_link"]
    assert len(u_refs) == 1
    
    h_refs = [r for r in refs if r.type == "repeated_market_hash"]
    assert len(h_refs) == 0

def test_identical_title_description_across_markets():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "Special Item", "Great quality product.", "snap1")
    r2 = mock_record(2, 2, "m2", "h2", "u2", "v2", "Special Item", "Great quality product.", "snap1")
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    
    c_refs = [r for r in refs if r.type == "exact_content_match"]
    assert len(c_refs) == 1
    assert c_refs[0].from_record_id == r1.source_record.id
    assert c_refs[0].to_record_id == r2.source_record.id

def test_near_duplicate_text():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "Item", "This is a very long description for a product that is high quality and ships fast.", "snap1")
    r2 = mock_record(2, 2, "m1", "h2", "u2", "v2", "Item", "This is a very long description for a product that is high quality and ships quickly.", "snap1")
    pipeline.process_records([r1, r2])
    
    nd = pipeline.compute_near_duplicates(max_hamming=10, min_jaccard=0.5)
    assert len(nd) == 1
    assert nd[0].hamming_distance < 10
    assert nd[0].jaccard_similarity > 0.5

def test_unrelated_text():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "Apples", "Fresh organic apples from the farm.", "snap1")
    r2 = mock_record(2, 2, "m2", "h2", "u2", "v2", "Laptops", "High performance gaming laptop with fast GPU.", "snap1")
    pipeline.process_records([r1, r2])
    
    nd = pipeline.compute_near_duplicates(max_hamming=20, min_jaccard=0.1)
    assert len(nd) == 0

def test_empty_title_description():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "", "", "snap1")
    r2 = mock_record(2, 2, "m2", "h2", "u2", "v2", "", "", "snap1")
    pipeline.process_records([r1, r2])
    
    # Excluded from exact_content_match spam
    refs = pipeline.extract_repetition_references()
    c_refs = [r for r in refs if r.type == "exact_content_match"]
    assert len(c_refs) == 0

def test_unicode_preservation_behavior():
    pipeline = CanonicalizationPipeline()
    r1 = mock_record(1, 1, "m1", "h1", "u1", "Omega²", "T1", "D1", "s1")
    r2 = mock_record(2, 2, "m1", "h2", "u2", "Omega2", "T1", "D1", "s1")
    pipeline.process_records([r1, r2])
    
    # Should not be exact row matches because the raw vendor string is different
    assert len(pipeline.exact_rows) == 2

def test_repeated_vendor_name_no_operator_assumption():
    # Vendor names are equal, but pipeline does not output 'same_operator' 
    r1 = mock_record(1, 1, "m1", "h1", "u1", "VendorX", "T1", "D1", "s1")
    r2 = mock_record(2, 2, "m1", "h2", "u2", "VendorX", "T2", "D2", "s1")
    pipeline = CanonicalizationPipeline()
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    assert all(r.type != "same_operator" for r in refs)

def test_multiline_descriptions():
    d1 = "Line 1\nLine 2\nLine 3"
    d2 = "Line 1\nLine 2\nLine 3"
    r1 = mock_record(1, 1, "m1", "h1", "u1", "v1", "T1", d1, "s1")
    r2 = mock_record(2, 2, "m2", "h2", "u2", "v2", "T1", d2, "s1")
    pipeline = CanonicalizationPipeline()
    pipeline.process_records([r1, r2])
    refs = pipeline.extract_repetition_references()
    c_refs = [r for r in refs if r.type == "exact_content_match"]
    assert len(c_refs) == 1

def test_deterministic_repeated_execution():
    d = "Determinism check prose."
    assert compute_simhash("T1", d) == compute_simhash("T1", d)
    assert compute_sha256("T1", d) == compute_sha256("T1", d)
    assert compute_shingles("T1", d) == compute_shingles("T1", d)
