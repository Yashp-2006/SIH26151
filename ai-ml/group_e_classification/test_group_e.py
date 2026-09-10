import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_e_classification.category_tagger import tag_category, build_category_candidate
from group_e_classification.risk_classifier import classify_risk
from group_e_classification.evasion_detector import detect_evasion


def test_tag_category():
    res_drug = tag_category("High purity chemical sample vial 100mg capsule")
    assert res_drug["primary_category"] == "drug"
    assert res_drug["confidence"] > 0

    res_cyber = tag_category("Zero-day exploit cve payload and ransomware botnet")
    assert res_cyber["primary_category"] == "cyber"

    res_other = tag_category("General conversation regarding weather and morning coffee")
    assert res_other["primary_category"] == "other"


def test_build_category_candidate():
    text_1 = "Malware payload and exploit rat"
    text_2 = "Exploit botnet cve builder"
    cand = build_category_candidate("sub_1", "sub_2", text_1, text_2, "doc_e1")

    assert cand.subject_a == "sub_1"
    assert cand.subject_b == "sub_2"
    assert cand.family == "F7"
    assert cand.polarity == "+"
    assert cand.extra["cat_a"] == "cyber"
    assert cand.extra["cat_b"] == "cyber"
    assert cand.extra["match"] is True


def test_risk_classifier():
    risk_crit = classify_risk("cyber", ["ransomware", "cve exploit"])
    assert risk_crit["tier"] == "critical"
    assert risk_crit["score"] >= 0.7

    risk_low = classify_risk("other", ["standard_delivery"])
    assert risk_low["tier"] == "low"


def test_evasion_detector():
    spaced = detect_evasion("Offering premium c o c a i n e right now")
    assert spaced["has_evasion"] is True
    assert any(d["type"] == "spaced_characters" for d in spaced["detected"])

    leet = detect_evasion("New m4lw4r3 available for download")
    assert leet["has_evasion"] is True
    assert any(d["type"] == "leetspeak_substitution" for d in leet["detected"])


if __name__ == "__main__":
    test_tag_category()
    test_build_category_candidate()
    test_risk_classifier()
    test_evasion_detector()
    print("All Group E tests passed.")
