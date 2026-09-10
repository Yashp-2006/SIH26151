"""Bounded real-source validation: first TWO inspected CSVs, 4,397 records.

Reads compressed bytes for SHA-256, then decompresses only the first two members.
Does not run the full corpus, near-duplicate all-pairs analysis or external calls.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from adapters.gwern_grams.runner import run_adapter
from cyber.indicators import extract_indicators, verify_indicator_span, VERSION
from cyber.policy import screen_indicator

EXPECTED = [
    ("grams/2014-06-09/1776.csv", 83, "d290f9caae27b73388cab9ab1a282ad6c8405f705af7f810fc4515ddfd2a1b9d"),
    ("grams/2015-04-20/Abraxas.csv", 4314, "9da13515007b3519668804b273158d65eb189677e743f49ea280b78cf19ccbd8"),
]


def validate(archive_path):
    result = run_adapter(str(archive_path), max_records=4397)
    if not result.archive_valid or result.structural_errors:
        raise ValueError("Pinned archive/member validation failed")
    actual = [(m.member_name, m.record_count, m.member_sha256) for m in result.member_results]
    if actual != EXPECTED:
        raise ValueError(f"Bounded sample differs from inspected member manifest: {actual}")
    counts, validations, examples = Counter(), Counter(), {}
    total = 0
    for member in result.member_results:
        for record in member.records:
            for indicator in extract_indicators(record):
                if not verify_indicator_span(indicator, record):
                    raise AssertionError("Indicator lineage mismatch")
                review = screen_indicator(indicator, record)
                if review["promotion"] != "blocked" or review["positive_support_allowed"]:
                    raise AssertionError("Unexpected promotion")
                counts[indicator["type"]] += 1
                validations[indicator["validation"]] += 1
                key = indicator["type"] + ":" + indicator["validation"]
                examples.setdefault(key, {"record_id": indicator["source_record_id"],
                    "field_ref": indicator["field_ref"], "start": indicator["start"], "end": indicator["end"],
                    "value_sha256": indicator["value_sha256"], "validation": indicator["validation"]})
                total += 1
    return {"validation_version": "cyber-bounded-validation-v1", "extractor_version": VERSION,
            "archive_sha256": result.archive_sha256, "scope": "first_two_CSV_members_only",
            "members": [{"path": p, "records": n, "sha256": h} for p, n, h in actual],
            "normalized_records": result.total_records, "structural_errors": len(result.structural_errors),
            "indicator_counts": dict(counts), "validation_counts": dict(validations),
            "span_replay_checks_passed": total, "blocked_promotion_checks_passed": total,
            "examples": examples, "validated_evidence_candidates": 0, "authoritative_evidence": 0,
            "hub_population_qualification": "not_run", "assessments": 0,
            "limits": ["No full-corpus ingestion", "No ownership or attribution validation",
                       "No precision/recall or calibration measurement", "No universal absence claims"],
            "code_sha256": {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [
                "cyber/indicators.py", "cyber/policy.py", "adapters/gwern_grams/normalizer.py",
                "adapters/gwern_grams/runner.py", "adapters/gwern_grams/csv_parser.py"]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", default="grams.tar.xz")
    parser.add_argument("--output", default="docs/cyber/validation/representative_validation.json")
    args = parser.parse_args()
    report = validate(args.archive)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["scope", "normalized_records", "indicator_counts",
        "validation_counts", "span_replay_checks_passed", "validated_evidence_candidates"]}, indent=2))


if __name__ == "__main__":
    main()
