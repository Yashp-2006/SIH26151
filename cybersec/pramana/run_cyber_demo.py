"""Run the offline synthetic cyber vertical slice; never reads the real archive."""

import argparse
import json
from pathlib import Path
from cyber.demo import make_demo
from cyber.render import render_review


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="docs/cyber/demo")
    args = parser.parse_args()
    packet = make_demo(args.output_dir)
    destination = Path(args.output_dir) / "review_packet.json"
    destination.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (Path(args.output_dir) / "review.html").write_text(render_review(packet), encoding="utf-8")
    print(json.dumps({"output": str(destination), "records": len(packet["normalized_observations"]),
        "indicators": len(packet["deterministic_indicators"]),
        "validated_evidence_candidates": 0, "assessment": None,
        "hub_accounts": packet["hub_check"]["distinct_eligible_accounts"],
        "promotion": packet["promotion_status"]}, indent=2))


if __name__ == "__main__":
    main()
