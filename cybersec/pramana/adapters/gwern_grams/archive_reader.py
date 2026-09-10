"""Archive reader for grams.tar.xz — N-01 validation and member streaming."""

import hashlib
import lzma
import re
import tarfile
from typing import Optional, Iterator, Tuple

from . import errors
from .identifiers import ARCHIVE_SHA256, source_archive_id, source_member_id, source_snapshot_id
from .models import SourceSnapshot, StructuralError

# Expected member layout pattern: grams/<snapshot_token>/<basename>
_MEMBER_LAYOUT_RE = re.compile(r"^grams/([^/]+)/(.+)$")

# Snapshot token date prefix: YYYY-MM-DD with optional suffix
_SNAPSHOT_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(.*)$")

# Path traversal checks
_UNSAFE_PATH_PATTERNS = ("..", "//", "\\")


def validate_archive_digest(archive_path: str) -> Tuple[bool, str]:
    """Compute SHA-256 of the archive file and compare to pinned digest."""
    h = hashlib.sha256()
    with open(archive_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    computed = h.hexdigest()
    return computed == ARCHIVE_SHA256, computed


def is_safe_path(member_name: str) -> bool:
    """Reject paths with traversal or unsafe components."""
    for pat in _UNSAFE_PATH_PATTERNS:
        if pat in member_name:
            return False
    if member_name.startswith("/"):
        return False
    return True


def parse_member_layout(member_name: str) -> Optional[Tuple[str, str]]:
    """
    Extract (snapshot_token, basename) from member name.
    Returns None if layout doesn't match grams/<token>/<basename>.
    """
    m = _MEMBER_LAYOUT_RE.match(member_name)
    if m:
        return m.group(1), m.group(2)
    return None


def parse_snapshot_token(token: str) -> Optional[Tuple[str, str]]:
    """
    Parse a snapshot token into (date_label, suffix_raw).
    Returns None if the token doesn't start with YYYY-MM-DD.
    """
    m = _SNAPSHOT_DATE_RE.match(token)
    if m:
        return m.group(1), m.group(2)
    return None


def make_snapshot(token: str) -> Optional[SourceSnapshot]:
    """Create a SourceSnapshot from a directory token, or None if unparseable."""
    parsed = parse_snapshot_token(token)
    if parsed is None:
        return None
    date_label, suffix_raw = parsed
    return SourceSnapshot(
        id=source_snapshot_id(token),
        archive_id=source_archive_id(),
        label_raw=token,
        date_label=date_label,
        suffix_raw=suffix_raw,
        meaning="source_snapshot_label",
        timezone=None,
        capture_instant=None,
    )


class ArchiveMember:
    """Represents one tar member with metadata and content access."""
    __slots__ = ("ordinal", "name", "size", "mtime", "is_csv",
                 "snapshot_token", "basename", "layout_valid", "content_bytes",
                 "member_sha256")

    def __init__(self, ordinal: int, name: str, size: int, mtime: int,
                 snapshot_token: Optional[str], basename: Optional[str],
                 layout_valid: bool, content_bytes: Optional[bytes]):
        self.ordinal = ordinal
        self.name = name
        self.size = size
        self.mtime = mtime
        self.is_csv = name.endswith(".csv")
        self.snapshot_token = snapshot_token
        self.basename = basename
        self.layout_valid = layout_valid
        self.content_bytes = content_bytes
        self.member_sha256: Optional[str] = None
        if content_bytes is not None:
            self.member_sha256 = hashlib.sha256(content_bytes).hexdigest()


def iterate_archive(archive_path: str) -> Iterator[Tuple[ArchiveMember, list]]:
    """
    Stream through all regular-file members of grams.tar.xz.
    
    Yields (ArchiveMember, structural_errors) for each member.
    Members are yielded in tar stream order with 1-based ordinals.
    Non-regular files are skipped.
    """
    ordinal = 0
    with lzma.open(archive_path) as xz_stream:
        with tarfile.open(fileobj=xz_stream, mode="r:") as tar:
            for tarinfo in tar:
                if not tarinfo.isreg():
                    continue
                ordinal += 1
                member_errors = []

                # Path safety
                if not is_safe_path(tarinfo.name):
                    member_errors.append(StructuralError(
                        category=errors.UNSUPPORTED_MEMBER_LAYOUT,
                        member_name=tarinfo.name,
                        member_ordinal=ordinal,
                        row_number=None,
                        detail=f"Unsafe path: {tarinfo.name!r}"
                    ))
                    yield ArchiveMember(
                        ordinal=ordinal, name=tarinfo.name,
                        size=tarinfo.size, mtime=tarinfo.mtime,
                        snapshot_token=None, basename=None,
                        layout_valid=False, content_bytes=None
                    ), member_errors
                    continue

                # Parse layout
                layout = parse_member_layout(tarinfo.name)
                snapshot_token = layout[0] if layout else None
                basename = layout[1] if layout else None
                layout_valid = layout is not None

                if not layout_valid:
                    member_errors.append(StructuralError(
                        category=errors.UNSUPPORTED_MEMBER_LAYOUT,
                        member_name=tarinfo.name,
                        member_ordinal=ordinal,
                        row_number=None,
                        detail=f"Does not match grams/<token>/<basename>: {tarinfo.name!r}"
                    ))

                # Read content bytes
                f = tar.extractfile(tarinfo)
                content_bytes = f.read() if f else None

                yield ArchiveMember(
                    ordinal=ordinal, name=tarinfo.name,
                    size=tarinfo.size, mtime=tarinfo.mtime,
                    snapshot_token=snapshot_token, basename=basename,
                    layout_valid=layout_valid, content_bytes=content_bytes
                ), member_errors
