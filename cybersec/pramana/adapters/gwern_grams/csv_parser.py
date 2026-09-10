"""Strict CSV parser for Gwern/Grams adapter (N-02, N-03)."""

import csv
import io
from typing import Optional
from . import errors


class CSVParseResult:
    """Result of parsing one CSV data row."""
    __slots__ = ("row_number", "cells", "error", "detail")

    def __init__(self, row_number: int, cells: Optional[list] = None,
                 error: Optional[str] = None, detail: str = ""):
        self.row_number = row_number
        self.cells = cells
        self.error = error
        self.detail = detail

    @property
    def valid(self) -> bool:
        return self.error is None


def parse_csv_member(content_bytes: bytes, member_name: str):
    """
    Parse a CSV member's bytes strictly per the adapter contract.

    Returns:
        (header_valid, header_cells, parsed_rows, structural_errors)

        header_valid: True if header matches EXPECTED_HEADER exactly
        header_cells: the parsed header row if readable, else None
        parsed_rows: list of CSVParseResult (only populated if header valid)
        structural_errors: list of (error_code, detail, row_number_or_None)
    """
    structural_errors = []

    # Strict UTF-8 decode — no BOM per spec §3.1
    try:
        text = content_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        structural_errors.append((errors.ENCODING_ERROR, str(e), None))
        return False, None, [], structural_errors

    reader = csv.reader(io.StringIO(text, newline=""), delimiter=",",
                        quotechar='"', doublequote=True, strict=True)

    # Read header
    try:
        header = next(reader)
    except StopIteration:
        structural_errors.append((errors.HEADER_MISMATCH, "Empty CSV file", None))
        return False, None, [], structural_errors
    except csv.Error as e:
        structural_errors.append((errors.CSV_PARSE_ERROR, f"Header parse error: {e}", None))
        return False, None, [], structural_errors

    # Validate header exactly
    if header != errors.EXPECTED_HEADER:
        structural_errors.append((
            errors.HEADER_MISMATCH,
            f"Expected {errors.EXPECTED_HEADER!r}, got {header!r}",
            None
        ))
        return False, header, [], structural_errors

    # Parse data rows — logical record numbers start at 1
    parsed_rows = []
    row_number = 0

    try:
        for row in reader:
            row_number += 1

            if len(row) != 11:
                structural_errors.append((
                    errors.ROW_WIDTH_MISMATCH,
                    f"Row {row_number}: expected 11 cells, got {len(row)}",
                    row_number
                ))
                parsed_rows.append(CSVParseResult(
                    row_number, error=errors.ROW_WIDTH_MISMATCH,
                    detail=f"expected 11 cells, got {len(row)}"
                ))
                continue

            if row[10] != "":
                structural_errors.append((
                    errors.NONEMPTY_TRAILING_CELL,
                    f"Row {row_number}: trailing cell is {row[10]!r}",
                    row_number
                ))
                parsed_rows.append(CSVParseResult(
                    row_number, error=errors.NONEMPTY_TRAILING_CELL,
                    detail=f"trailing cell is {row[10]!r}"
                ))
                continue

            parsed_rows.append(CSVParseResult(row_number, cells=row))
    except csv.Error as e:
        structural_errors.append((
            errors.CSV_PARSE_ERROR,
            f"CSV parse error after row {row_number}: {e}",
            row_number
        ))

    return True, header, parsed_rows, structural_errors


def raw_values_dict(cells: list) -> dict:
    """Convert 11-cell row to dict with the 10 named headers. Preserves exact strings."""
    return {
        "hash": cells[0],
        "market_name": cells[1],
        "item_link": cells[2],
        "vendor_name": cells[3],
        "price": cells[4],
        "name": cells[5],
        "description": cells[6],
        "image_link": cells[7],
        "add_time": cells[8],
        "ship_from": cells[9],
    }
