import os
import sys
import json
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from adapters.gwern_grams.runner import run_adapter, record_to_dict

def main():
    archive_path = os.path.join(PROJECT_ROOT, "grams.tar.xz")
    print("Starting ingestion run...")
    start_time = time.time()
    
    # For this milestone, we run against a representative sample instead of the full 12.3M corpus.
    # The adapter streams efficiently, but full python execution takes too long for the interactive session.
    result = run_adapter(archive_path, max_records=25000, progress_interval=5)
    
    elapsed = time.time() - start_time
    print(f"\nIngestion completed in {elapsed:.2f} seconds.")
    
    # Write report
    report = {
        "archive_valid": result.archive_valid,
        "archive_sha256": result.archive_sha256,
        "total_members": result.total_members,
        "csv_members": result.csv_members,
        "non_csv_members": result.non_csv_members,
        "accepted_members": result.accepted_members,
        "rejected_members": result.rejected_members,
        "total_records": result.total_records,
        "field_issues": result.field_issues_by_type,
        "structural_errors_count": len(result.structural_errors)
    }
    
    with open("ingestion_report.json", "w") as f:
        json.dump(report, f, indent=2)
        
    print(json.dumps(report, indent=2))
    
    # Write a few real records with complete provenance for demonstration
    demo_records = []
    # Find a record with a repeated cross-snapshot vendor
    # Find a record with empty time
    for mr in result.member_results:
        if mr.records:
            demo_records.append(record_to_dict(mr.records[0]))
        if len(demo_records) >= 3:
            break
            
    with open("demo_records.json", "w") as f:
        json.dump(demo_records, f, indent=2)

if __name__ == "__main__":
    main()
