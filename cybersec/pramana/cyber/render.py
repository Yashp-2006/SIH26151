"""Escaped, self-contained offline view of the same review packet; no decisions."""

import html
import json


def render_review(packet):
    def esc(value):
        return html.escape(str(value), quote=True)

    def pretty(value):
        return esc(json.dumps(value, ensure_ascii=False, indent=2))

    def section(title, value):
        return f"<details><summary>{esc(title)}</summary><pre>{pretty(value)}</pre></details>"

    content = ["<!doctype html><html lang='en'><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>PRAMANA Cyber Review Input</title>",
        "<style>body{font:16px/1.6 system-ui;margin:2rem auto;max-width:1100px;padding:0 1rem;color:#152238;background:#f5f7fa}"
        "h1,h2{line-height:1.2}section,details{background:white;padding:1rem;margin:1rem 0;border:1px solid #ced8e1;border-radius:8px}"
        "pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}summary{cursor:pointer;font-weight:600}"
        ".notice{border-left:5px solid #ad6410}a{color:#164a8a}</style>",
        "<body><h1>PRAMANA · Cyber review input</h1>",
        "<section class='notice'><strong>SYNTHETIC MECHANISM DEMO · AWAITING HUMAN REVIEW</strong>"
        "<p>This is an investigation input, not an attribution result. Evidence promotion is blocked by DC-06. "
        "No score, accepted persona, identity merge or real-person identification is produced.</p>"
        "<p>Address checksum validity establishes format only. Copy and hub findings restrict support; "
        "they do not prove different operators.</p></section>",
        f"<section><h2>Executable path</h2><p>{len(packet['normalized_observations'])} normalized occurrences → "
        f"{len(packet['deterministic_indicators'])} deterministic derivations → provenance and restriction checks → "
        "review input.</p><p>Validated evidence candidates: <strong>0</strong>. Completed assessments: <strong>0</strong>.</p>"
        "<p><a href='review_packet.json'>Complete machine-readable packet</a> · "
        "<a href='synthetic_source.tar'>Reproducible synthetic source archive</a></p></section>",
        section("Investigation question and competing explanation", packet["hypothesis_input"]),
        section("Counter-check execution states", packet["counter_checks"]),
        section("Hub count: declared eligible accounts and exclusions", packet["hub_check"]),
        section("Source discrepancies — review only", packet["source_discrepancies"]),
        section("Repetition — no automatic independence or identity", packet["repetition_references"]),
        section("Missing information — not negative evidence", packet["missing_information"]),
        "<h2>Indicators and promotion restrictions</h2>"]
    for index, (indicator, review) in enumerate(zip(packet["deterministic_indicators"], packet["promotion_review_items"]), 1):
        content.append(section(f"{index}. {indicator['type']} · {indicator['eligible_family']} · {indicator['validation']}",
                               {"derivation": indicator, "promotion_review": review}))
    content.append("<h2>Source replay</h2>")
    for index, record in enumerate(packet["normalized_observations"], 1):
        content.append(section(f"Occurrence {index}: exact raw cells and provenance", record))
    content += [section("Unsupported modalities", packet["unsupported"]),
                section("Synthetic scope and declared fixture decisions", packet["fixture"]), "</body></html>"]
    return "\n".join(content)
