"""
Group G: Citation Validator.
Extracts observation citations and validates that all cited IDs exist in the source observations.
"""

import re
from typing import List, Set, Dict, Any


def extract_citations(text: str) -> List[str]:
    """
    Extract citation IDs bracketed in text (e.g., [OBS-1], [OBS_002], [DOC-ABC]).
    """
    # Matches patterns like [OBS-1], [OBS_1], [REF-123]
    matches = re.findall(r"\[([A-Za-z0-9_\-]+)\]", text)
    # Deduplicate while preserving encounter order
    seen = set()
    res = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            res.append(m)
    return res


def validate_citations(text: str, valid_ids: List[str]) -> Dict[str, Any]:
    """
    Validate that all citations present in text correspond to known valid observation IDs.
    Returns:
        {
            "is_grounded": bool,
            "cited_ids": list[str],
            "valid_citations": list[str],
            "invalid_citations": list[str],
            "missing_coverage": bool,
        }
    """
    cited = extract_citations(text)
    valid_set = set(valid_ids)

    valid_citations = [c for c in cited if c in valid_set]
    invalid_citations = [c for c in cited if c not in valid_set]

    # Grounded if at least one citation exists and zero invalid/hallucinated citations exist
    is_grounded = len(valid_citations) > 0 and len(invalid_citations) == 0

    return {
        "is_grounded": is_grounded,
        "cited_ids": cited,
        "valid_citations": valid_citations,
        "invalid_citations": invalid_citations,
        "citation_count": len(cited),
    }
