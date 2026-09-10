"""Shared test utilities and archive-backed fixture helpers."""

import os
import sys
import csv
import io
import hashlib
import lzma
import tarfile
from typing import Optional

# Ensure adapters package is importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

ARCHIVE_PATH = os.path.join(PROJECT_ROOT, "grams.tar.xz")
ARCHIVE_FIXTURES_ENABLED = False


def pytest_addoption(parser):
    parser.addoption("--archive-fixtures", action="store_true", default=False,
                     help="Opt in to older fixtures that seek deep into grams.tar.xz")


def pytest_configure(config):
    global ARCHIVE_FIXTURES_ENABLED
    ARCHIVE_FIXTURES_ENABLED = config.getoption("--archive-fixtures")

from adapters.gwern_grams import errors
from adapters.gwern_grams.identifiers import ARCHIVE_SHA256


def archive_exists() -> bool:
    return ARCHIVE_FIXTURES_ENABLED and os.path.isfile(ARCHIVE_PATH)


def read_member_bytes(member_name: str) -> Optional[bytes]:
    """Read a specific member's bytes from the real archive."""
    if not archive_exists():
        return None
    with lzma.open(ARCHIVE_PATH) as xz:
        with tarfile.open(fileobj=xz, mode="r:") as tar:
            for ti in tar:
                if ti.name == member_name and ti.isreg():
                    f = tar.extractfile(ti)
                    return f.read() if f else None
    return None


def get_member_ordinal(member_name: str) -> Optional[int]:
    """Get the 1-based ordinal of a member in the archive."""
    if not archive_exists():
        return None
    ordinal = 0
    with lzma.open(ARCHIVE_PATH) as xz:
        with tarfile.open(fileobj=xz, mode="r:") as tar:
            for ti in tar:
                if not ti.isreg():
                    continue
                ordinal += 1
                if ti.name == member_name:
                    return ordinal
    return None


def parse_csv_row(content_bytes: bytes, row_number: int) -> Optional[list]:
    """Extract a specific logical row (1-based, after header) from CSV bytes."""
    text = content_bytes.decode("utf-8")
    reader = csv.reader(io.StringIO(text), delimiter=",", quotechar='"', doublequote=True)
    next(reader)  # skip header
    current = 0
    for row in reader:
        current += 1
        if current == row_number:
            return row
    return None


def build_synthetic_csv(rows: list, header: Optional[list] = None) -> bytes:
    """Build a CSV bytes object from header and rows (each row is list of 11 strings)."""
    if header is None:
        header = list(errors.EXPECTED_HEADER)
    output = io.StringIO()
    writer = csv.writer(output, delimiter=",", quotechar='"', doublequote=True,
                        lineterminator="\n")
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def build_synthetic_tar(members: dict) -> bytes:
    """
    Build a tar.xz archive from {member_name: content_bytes}.
    Returns the compressed archive bytes.
    """
    import io as _io
    tar_buf = _io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w") as tar:
        for name, data in members.items():
            ti = tarfile.TarInfo(name=name)
            ti.size = len(data)
            tar.addfile(ti, _io.BytesIO(data))
    tar_bytes = tar_buf.getvalue()
    return lzma.compress(tar_bytes)
