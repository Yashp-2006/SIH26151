"""End-to-end adapter pipeline: archive → normalized records."""

import json
import sys
from collections import defaultdict
from typing import Optional

from . import errors
from . import identifiers as ids
from .archive_reader import (
    validate_archive_digest, iterate_archive, make_snapshot, ArchiveMember,
)
from .csv_parser import parse_csv_member
from .normalizer import normalize_row
from .models import (
    SourceSnapshot, StructuralError, MemberResult, AdapterResult, NormalizedRecord,
)


def run_adapter(archive_path: str, max_records: Optional[int] = None,
                progress_interval: int = 100) -> AdapterResult:
    """
    Run the complete Gwern/Grams adapter pipeline.

    Args:
        archive_path: Path to grams.tar.xz
        max_records: If set, stop after this many total records (for testing)
        progress_interval: Print progress every N members
    """
    if max_records is not None and (type(max_records) is not int or max_records <= 0):
        raise ValueError("max_records must be a positive integer or None")
    if progress_interval <= 0:
        raise ValueError("progress_interval must be positive")
    # Step 1: Validate archive digest (N-01)
    archive_valid, computed_digest = validate_archive_digest(archive_path)
    if not archive_valid:
        return AdapterResult(
            archive_id=ids.source_archive_id(),
            archive_sha256=computed_digest,
            archive_valid=False,
            adapter_version=ids.ADAPTER_VERSION,
            total_members=0, csv_members=0, non_csv_members=0,
            accepted_members=0, rejected_members=0, total_records=0,
            field_issues_by_type={}, snapshots={},
            member_results=[], structural_errors=[
                StructuralError(
                    category="archive_digest_mismatch",
                    member_name=None, member_ordinal=None, row_number=None,
                    detail=f"Expected {ids.ARCHIVE_SHA256}, got {computed_digest}"
                )
            ],
        )

    # Step 2: Iterate members
    snapshots = {}
    member_results = []
    all_structural_errors = []
    total_records = 0
    csv_count = 0
    non_csv_count = 0
    accepted_count = 0
    rejected_count = 0
    field_issues_by_type = defaultdict(int)
    stop_early = False

    for member, member_errors in iterate_archive(archive_path):
        if stop_early:
            break

        all_structural_errors.extend(member_errors)

        # Register snapshot
        snapshot = None
        if member.snapshot_token:
            if member.snapshot_token not in snapshots:
                snapshot = make_snapshot(member.snapshot_token)
                if snapshot:
                    snapshots[member.snapshot_token] = snapshot
            else:
                snapshot = snapshots[member.snapshot_token]

        if member.is_csv:
            csv_count += 1
        else:
            non_csv_count += 1
            # Non-CSV: inventory only per spec
            member_results.append(MemberResult(
                member_id=ids.source_member_id(member.ordinal, member.name),
                member_name=member.name,
                member_ordinal=member.ordinal,
                snapshot=snapshot,
                is_csv=False,
                accepted=False,
                record_count=0,
                records=[],
                structural_errors=member_errors,
                member_sha256=member.member_sha256,
            ))
            continue

        # CSV member: parse and normalize
        if not member.layout_valid or member.content_bytes is None:
            rejected_count += 1
            member_results.append(MemberResult(
                member_id=ids.source_member_id(member.ordinal, member.name),
                member_name=member.name,
                member_ordinal=member.ordinal,
                snapshot=snapshot,
                is_csv=True,
                accepted=False,
                record_count=0,
                records=[],
                structural_errors=member_errors,
                member_sha256=member.member_sha256,
            ))
            continue

        header_valid, header_cells, parsed_rows, csv_errors = parse_csv_member(
            member.content_bytes, member.name
        )

        # Convert CSV errors to StructuralError objects
        for code, detail, row_num in csv_errors:
            se = StructuralError(
                category=code,
                member_name=member.name,
                member_ordinal=member.ordinal,
                row_number=row_num,
                detail=detail,
            )
            all_structural_errors.append(se)
            member_errors.append(se)

        if not header_valid or csv_errors or member_errors:
            rejected_count += 1
            member_results.append(MemberResult(
                member_id=ids.source_member_id(member.ordinal, member.name),
                member_name=member.name,
                member_ordinal=member.ordinal,
                snapshot=snapshot,
                is_csv=True,
                accepted=False,
                record_count=0,
                records=[],
                structural_errors=member_errors,
                member_sha256=member.member_sha256,
            ))
            continue

        # Normalize rows
        snapshot_id = snapshot.id if snapshot else ids.source_snapshot_id(member.snapshot_token)
        records = []
        for parse_result in parsed_rows:
            if not parse_result.valid:
                continue

            nr = normalize_row(
                cells=parse_result.cells,
                member_ordinal=member.ordinal,
                member_name=member.name,
                row_number=parse_result.row_number,
                snapshot_token=member.snapshot_token,
                snapshot_id=snapshot_id,
                member_sha256=member.member_sha256,
                member_mtime=member.mtime,
                header=header_cells,
            )
            records.append(nr)

            # Count field issues
            for issue in nr.source_record.field_issues:
                field_issues_by_type[issue.code] += 1

            total_records += 1
            if max_records and total_records >= max_records:
                stop_early = True
                break

        accepted_count += 1
        member_results.append(MemberResult(
            member_id=ids.source_member_id(member.ordinal, member.name),
            member_name=member.name,
            member_ordinal=member.ordinal,
            snapshot=snapshot,
            is_csv=True,
            accepted=True,
            record_count=len(records),
            records=records,
            structural_errors=member_errors,
            member_sha256=member.member_sha256,
        ))

        if stop_early:
            break  # Do not decompress the next member just to stop.

        if (accepted_count % progress_interval) == 0:
            print(f"  Processed {accepted_count} CSV members, {total_records} records...",
                  file=sys.stderr)

    return AdapterResult(
        archive_id=ids.source_archive_id(),
        archive_sha256=ids.ARCHIVE_SHA256,
        archive_valid=True,
        adapter_version=ids.ADAPTER_VERSION,
        total_members=csv_count + non_csv_count,
        csv_members=csv_count,
        non_csv_members=non_csv_count,
        accepted_members=accepted_count,
        rejected_members=rejected_count,
        total_records=total_records,
        field_issues_by_type=dict(field_issues_by_type),
        snapshots=snapshots,
        member_results=member_results,
        structural_errors=all_structural_errors,
    )


def record_to_dict(nr: NormalizedRecord) -> dict:
    """Serialize a NormalizedRecord to a JSON-compatible dict for output."""
    def fref_dict(fr):
        if fr is None:
            return None
        return {"record_id": fr.record_id, "column_position": fr.column_position,
                "header_name": fr.header_name}

    result = {
        "source_record": {
            "id": nr.source_record.id,
            "archive_id": nr.source_record.archive_id,
            "member_id": nr.source_record.member_id,
            "snapshot_id": nr.source_record.snapshot_id,
            "row_number": nr.source_record.row_number,
            "raw_values": nr.source_record.raw_values,
            "trailing_empty_cell": nr.source_record.trailing_empty_cell,
            "field_issues": [
                {"field_position": fi.field_position, "field_name": fi.field_name,
                 "code": fi.code, "raw_value": fi.raw_value}
                for fi in nr.source_record.field_issues
            ],
            "adapter_version": nr.source_record.adapter_version,
        },
        "listing_observation": {
            "id": nr.listing_observation.id,
            "source_record_id": nr.listing_observation.source_record_id,
            "snapshot_id": nr.listing_observation.snapshot_id,
            "source_hash_raw": nr.listing_observation.source_hash_raw,
            "source_hash_reference": nr.listing_observation.source_hash_reference,
            "source_url_reference": nr.listing_observation.source_url_reference,
            "item_reference": {
                "raw": nr.listing_observation.item_reference.raw,
                "kind": nr.listing_observation.item_reference.kind,
                "field_ref": fref_dict(nr.listing_observation.item_reference.field_ref),
            } if nr.listing_observation.item_reference else None,
            "observed_account_id": nr.listing_observation.observed_account_id,
            "title": nr.listing_observation.title,
            "description": nr.listing_observation.description,
            "price": {
                "raw": nr.listing_observation.price.raw,
                "parse_status": nr.listing_observation.price.parse_status,
                "amount_decimal": nr.listing_observation.price.amount_decimal,
                "currency": None,
                "field_ref": fref_dict(nr.listing_observation.price.field_ref),
            },
            "canonical_listing_id": None,
            "canonical_artefact_id": None,
        },
        "observed_account": {
            "id": nr.observed_account.id,
            "source_namespace": nr.observed_account.source_namespace,
            "market_name_raw": nr.observed_account.market_name_raw,
            "vendor_name_raw": nr.observed_account.vendor_name_raw,
            "source_record_id": nr.observed_account.source_record_id,
            "market_field_ref": fref_dict(nr.observed_account.market_field_ref),
            "vendor_field_ref": fref_dict(nr.observed_account.vendor_field_ref),
        } if nr.observed_account else None,
        "image_reference": {
            "id": nr.image_reference.id,
            "source_record_id": nr.image_reference.source_record_id,
            "raw": nr.image_reference.raw,
            "kind": nr.image_reference.kind,
            "field_ref": fref_dict(nr.image_reference.field_ref),
            "image_bytes_ref": None,
            "verified_archive_image_member": None,
        } if nr.image_reference else None,
        "timestamp": {
            "id": nr.timestamp.id,
            "source_record_id": nr.timestamp.source_record_id,
            "field_ref": fref_dict(nr.timestamp.field_ref),
            "raw": nr.timestamp.raw,
            "parse_status": nr.timestamp.parse_status,
            "parsed_integer": nr.timestamp.parsed_integer,
            "classification": nr.timestamp.classification,
            "semantic_status": nr.timestamp.semantic_status,
            "epoch": None, "unit": None, "timezone": None, "instant": None,
        },
        "shipping_claim": {
            "id": nr.shipping_claim.id,
            "source_record_id": nr.shipping_claim.source_record_id,
            "raw": nr.shipping_claim.raw,
            "interpretation": nr.shipping_claim.interpretation,
            "field_ref": fref_dict(nr.shipping_claim.field_ref),
            "country_code": None, "actual_location": None,
        } if nr.shipping_claim else None,
        "provenance": {
            "archive_id": nr.provenance.archive_id,
            "archive_sha256": nr.provenance.archive_sha256,
            "member_id": nr.provenance.member_id,
            "member_name_raw": nr.provenance.member_name_raw,
            "member_ordinal": nr.provenance.member_ordinal,
            "member_sha256": nr.provenance.member_sha256,
            "snapshot_id": nr.provenance.snapshot_id,
            "row_number": nr.provenance.row_number,
            "schema_header": nr.provenance.schema_header,
            "adapter_version": nr.provenance.adapter_version,
            "acquisition_uri": nr.provenance.acquisition_uri,
            "acquired_at": nr.provenance.acquired_at,
            "acquisition_report_ref": nr.provenance.acquisition_report_ref,
            "archive_member_mtime": nr.provenance.archive_member_mtime,
        },
        "relations": [
            {"type": r.type, "from_id": r.from_id, "to_id": r.to_id,
             "source_record_id": r.source_record_id,
             "field_refs": [fref_dict(fr) for fr in r.field_refs]}
            for r in nr.relations
        ],
    }
    return result
