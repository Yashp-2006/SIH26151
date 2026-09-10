"""Explicitly synthetic, reproducible source fixtures. No operator ground truth."""

import csv
import hashlib
import io
import tarfile
from pathlib import Path
from dataclasses import asdict
from adapters.gwern_grams import errors
from adapters.gwern_grams.csv_parser import parse_csv_member
from adapters.gwern_grams.normalizer import normalize_row
from .indicators import BASE58, extract_indicators
from .policy import count_hub, stable_key
from .review import build_review_packet


def synthetic_address():
    # Synthetic payload, no private key, chain lookup, ownership or funding claim.
    payload = b"\x00" + hashlib.sha256(b"PRAMANA synthetic fixture identifier v1").digest()[:20]
    data = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n, encoded = int.from_bytes(data, "big"), ""
    while n:
        n, remainder = divmod(n, 58)
        encoded = BASE58[remainder] + encoded
    return "1" * (len(data) - len(data.lstrip(b"\x00"))) + encoded


def fixture_row(vendor="Account-A", *, token="listing-a", title="Demonstration listing",
                description=None, url="https://market-a.invalid/listing/a"):
    if description is None:
        description = f"Synthetic catalogue text. Reference {synthetic_address()}. BEGIN PGP PUBLIC KEY BLOCK Version Demo"
    return [token, "Market-A", url, vendor, "50.00000000", title, description,
            "", "1400000000", "Unspecified", ""]


def csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(errors.EXPECTED_HEADER)
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def fixture_archive_bytes():
    rows = [fixture_row()]
    # Explicit population controls, not evidence of thirteen real operators.
    for n in range(1, 13):
        rows.append(fixture_row(f"Population-{n:02}", token=f"population-{n}",
                                title=f"Control listing {n}",
                                description=f"Control {n}; public reference {synthetic_address()}",
                                url=f"https://market-a.invalid/control/{n}"))
    rows.append(fixture_row("Account-B", token="listing-b", url="https://market-a.invalid/listing/b"))
    rows.append(fixture_row("Account-C", description="Changed source vendor assertion"))
    rows.append(fixture_row(token="different-token", description="Same URL, different source token"))
    rows.append(fixture_row(token="missing", description="", url="https://market-a.invalid/missing"))
    members = {"grams/2020-01-01/Synthetic.csv": csv_bytes(rows),
               "grams/2020-01-02/Synthetic.csv": csv_bytes([fixture_row()])}
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w", format=tarfile.USTAR_FORMAT) as tar:
        for name, data in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0  # Fixed fixture metadata, never event/capture time.
            tar.addfile(info, io.BytesIO(data))
    return output.getvalue()


def normalize_synthetic_archive(data):
    digest = hashlib.sha256(data).hexdigest()
    records = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:") as tar:
        for ordinal, member in enumerate(tar, 1):
            if not member.isreg():
                raise ValueError("Synthetic fixture requires regular CSV members")
            raw = tar.extractfile(member).read()
            valid, header, rows, issues = parse_csv_member(raw, member.name)
            if not valid or issues:
                raise ValueError(f"Invalid synthetic member: {issues}")
            token = member.name.split("/")[1]
            for row in rows:
                records.append(normalize_row(row.cells, ordinal, member.name, row.row_number,
                    token, ["snapshot", digest, token], hashlib.sha256(raw).hexdigest(),
                    member.mtime, header, fixture_archive_sha256=digest))
    return records


def make_demo(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = fixture_archive_bytes()
    (output_dir / "synthetic_source.tar").write_bytes(data)
    records = normalize_synthetic_archive(data)
    population = records[0].source_record.snapshot_id
    associations = []
    for record in records[:13]:
        indicator = next(i for i in extract_indicators(record) if i["type"] == "bitcoin_base58_lexical")
        associations.append({"indicator": indicator["raw"], "account_id": indicator["observed_account_id"],
            "snapshot_id": population, "record_id": indicator["source_record_id"],
            "validation": indicator["validation"], "eligibility": "eligible", "lineage": "original",
            "decision_ref": "synthetic_fixture_declared_population_v1; not an operational qualification"})
    hub = count_hub(synthetic_address(), associations, snapshot_id=population)
    # A declared fixture decision covering only B's description derivations.
    # Exact equality itself never makes this decision.
    clone_decisions = {stable_key(i["id"]): "synthetic_review_fixture_v1: B description copied from A"
                       for i in extract_indicators(records[13]) if i["field_ref"][1] == 7}
    packet = build_review_packet(records, subject_accounts=[records[0].observed_account.id,
        records[13].observed_account.id], population_ref=population, hub_result=hub,
        clone_decisions=clone_decisions)
    packet["fixture"] = {"synthetic": True, "source_archive": "synthetic_source.tar",
        "source_sha256": hashlib.sha256(data).hexdigest(), "truth_labels": "none",
        "clone_determinations": clone_decisions, "hub_population": associations,
        "note": "Mechanism demonstration, not RANGE-SIM evaluation or a completed human review."}
    return packet
