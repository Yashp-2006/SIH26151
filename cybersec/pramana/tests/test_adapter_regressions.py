"""Regression checks for contract violations found during the completion pass."""

import pytest
from adapters.gwern_grams import identifiers as ids
from adapters.gwern_grams.archive_reader import ArchiveMember
from adapters.gwern_grams.csv_parser import parse_csv_member
from adapters.gwern_grams.normalizer import _normalize_price, _normalize_add_time
from adapters.gwern_grams import runner
from canonicalization.text_hashing import compute_sha256
from cyber.demo import csv_bytes, fixture_row


def mock_member(data):
    return ArchiveMember(1, "grams/2020-01-01/Test.csv", len(data), 0,
                         "2020-01-01", "Test.csv", True, data)


def patch_archive(monkeypatch, data):
    monkeypatch.setattr(runner, "validate_archive_digest", lambda _: (True, ids.ARCHIVE_SHA256))
    monkeypatch.setattr(runner, "iterate_archive", lambda _: iter([(mock_member(data), [])]))


@pytest.mark.parametrize("bad_row", [fixture_row()[:-1], fixture_row()[:-1] + ["unexpected"]])
def test_atomic_member_rejection(monkeypatch, bad_row):
    patch_archive(monkeypatch, csv_bytes([fixture_row(), bad_row]))
    result = runner.run_adapter("mocked-source")
    assert result.total_records == 0
    assert result.rejected_members == 1
    assert not result.member_results[0].accepted
    assert not result.member_results[0].records


def test_return_all_normalized_rows(monkeypatch):
    patch_archive(monkeypatch, csv_bytes([fixture_row()] * 8))
    result = runner.run_adapter("mocked-source")
    assert result.total_records == len(result.member_results[0].records) == 8
    out = runner.record_to_dict(result.member_results[0].records[0])
    assert {"acquisition_uri", "acquired_at", "acquisition_report_ref"} <= out["provenance"].keys()


def test_limit_does_not_read_next_member(monkeypatch):
    data = csv_bytes([fixture_row()] * 8)
    patch_archive(monkeypatch, data)
    def members(_):
        yield mock_member(data), []
        raise AssertionError("Read beyond requested normalized-record limit")
    monkeypatch.setattr(runner, "iterate_archive", members)
    result = runner.run_adapter("mocked-source", max_records=6)
    assert len(result.member_results[0].records) == result.total_records == 6


def test_unterminated_csv_quote_rejected(monkeypatch):
    data = csv_bytes([]) + b'"unterminated'
    assert parse_csv_member(data, "test.csv")[3]
    patch_archive(monkeypatch, data)
    assert runner.run_adapter("mocked-source").rejected_members == 1


@pytest.mark.parametrize("price,time", [("50.0\n", "1400000000\n"), ("50.0 ", "1400000000 ")])
def test_numeric_grammar_does_not_trim(price, time):
    assert _normalize_price(price)[0] == "invalid_decimal"
    assert _normalize_add_time(time)[0] == "invalid_integer"


def test_decimal_no_rounding():
    value = "000123456789012345678901234567890.1234567890123456789000"
    assert _normalize_price(value)[1] == "123456789012345678901234567890.1234567890123456789"


def test_content_digest_has_unambiguous_framing():
    assert compute_sha256("a\x00b", "c") != compute_sha256("a", "b\x00c")
    assert compute_sha256(None, "a") != compute_sha256("", "a")


def test_embedded_crlf_preserved():
    row = fixture_row(description="line1\r\nline2")
    parsed = parse_csv_member(csv_bytes([row]), "test.csv")
    assert not parsed[3]
    assert parsed[2][0].cells[6] == "line1\r\nline2"
