"""
Group E: Keyword Evasion & Obfuscation Detector.
Identifies leetspeak, spaced characters, and delimiter padding used to evade filters.
"""

import re
from typing import Dict, Any

LEET_MAP = {
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "5": "s",
    "7": "t",
    "@": "a",
    "$": "s",
}

EVASION_TARGETS = ["cocaine", "fentanyl", "heroin", "malware", "exploit", "botnet", "passport"]


def normalize_leetspeak(text: str) -> str:
    """Normalize simple leetspeak substitutions."""
    result = []
    for ch in text.lower():
        result.append(LEET_MAP.get(ch, ch))
    return "".join(result)


def detect_evasion(text: str) -> Dict[str, Any]:
    """
    Detect whether text contains obfuscated or evasive keywords.
    Returns: {"has_evasion": bool, "detected": list[dict], "normalized_text": str}
    """
    detected = []
    lower = text.lower()

    # 1. Spaced-out character detection (e.g., "c o c a i n e")
    spaced_matches = re.findall(r"\b(?:[a-z]\s+){3,}[a-z]\b", lower)
    for sm in spaced_matches:
        collapsed = re.sub(r"\s+", "", sm)
        if any(target in collapsed for target in EVASION_TARGETS):
            detected.append({"pattern": sm, "normalized": collapsed, "type": "spaced_characters"})

    # 2. Leetspeak detection
    norm = normalize_leetspeak(lower)
    for target in EVASION_TARGETS:
        if target in norm and target not in lower:
            detected.append({"pattern": target, "type": "leetspeak_substitution"})

    return {
        "has_evasion": len(detected) > 0,
        "detected": detected,
        "normalized_text": norm,
    }
