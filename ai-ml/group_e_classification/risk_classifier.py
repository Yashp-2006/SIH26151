"""
Group E: Threat Tier & Risk Classification.
Maps extracted indicators and primary category into risk tiers: low, medium, high, critical.
"""

from typing import List, Dict, Any

HIGH_RISK_CATEGORIES = {"cyber", "credential"}
CRITICAL_INDICATORS = {"ransomware", "malware", "exploit", "cve"}


def classify_risk(category: str, indicators: List[str]) -> Dict[str, Any]:
    """
    Score risk tier based on taxonomy category and presence of weaponized indicators.
    Returns: {"tier": "low"|"medium"|"high"|"critical", "score": float, "factors": list}
    """
    factors = []
    score = 0.0

    if category in HIGH_RISK_CATEGORIES:
        score += 0.4
        factors.append(f"high_risk_category_{category}")
    elif category in {"drug", "fraud", "counterfeit"}:
        score += 0.25
        factors.append(f"illicit_category_{category}")

    for ind in indicators:
        ind_lower = ind.lower()
        if any(c in ind_lower for c in CRITICAL_INDICATORS):
            score += 0.3
            factors.append(f"critical_keyword_{ind}")

    score = min(1.0, round(score, 2))
    if score >= 0.7:
        tier = "critical"
    elif score >= 0.4:
        tier = "high"
    elif score >= 0.2:
        tier = "medium"
    else:
        tier = "low"

    return {"tier": tier, "score": score, "factors": factors}
