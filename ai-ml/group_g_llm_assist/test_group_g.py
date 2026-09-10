import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_g_llm_assist.prompt_builder import build_investigation_prompt
from group_g_llm_assist.citation_validator import extract_citations, validate_citations
from group_g_llm_assist.hypothesis_generator import generate_candidate_hypothesis


def test_build_investigation_prompt():
    obs = [
        {"id": "OBS-1", "family": "F1", "description": "PGP key fingerprint match"},
        {"id": "OBS-2", "family": "F3", "description": "Shared ASN 13335"},
    ]
    res = build_investigation_prompt("vendor_alpha", "vendor_beta", obs)

    assert "OBS-1" in res["valid_ids"]
    assert "OBS-2" in res["valid_ids"]
    assert "[OBS-1]" in res["user"]
    assert "vendor_alpha" in res["user"]
    assert "CRITICAL CONSTRAINT" in res["system"]


def test_citation_validator_valid():
    text = "Subjects are likely coordinated based on [OBS-1] and [OBS-2] infrastructure."
    val = validate_citations(text, ["OBS-1", "OBS-2", "OBS-3"])

    assert val["is_grounded"] is True
    assert val["valid_citations"] == ["OBS-1", "OBS-2"]
    assert len(val["invalid_citations"]) == 0


def test_citation_validator_hallucinated():
    text = "Subjects share bank drop per [OBS-999] which reveals collusion."
    val = validate_citations(text, ["OBS-1", "OBS-2"])

    assert val["is_grounded"] is False
    assert "OBS-999" in val["invalid_citations"]


def test_hypothesis_generator_grounded():
    text = "Coordinated operations indicated by matching PGP [OBS-1] and shared subnet [OBS-2]."
    res = generate_candidate_hypothesis(
        "subj_a", "subj_b", text, ["OBS-1", "OBS-2"], "doc_g1"
    )

    assert res.is_valid is True
    assert res.is_authoritative is False
    assert res.candidate is not None
    assert res.candidate.family == "F9"
    assert res.candidate.extra["authoritative"] is False
    assert res.candidate.extra["citations"] == ["OBS-1", "OBS-2"]


def test_hypothesis_generator_rejected_on_hallucination():
    text = "Known alias from external leak [OBS-FAKE]."
    res = generate_candidate_hypothesis(
        "subj_a", "subj_b", text, ["OBS-1", "OBS-2"], "doc_g2"
    )

    assert res.is_valid is False
    assert res.candidate is None
    assert "OBS-FAKE" in res.invalid_citations


if __name__ == "__main__":
    test_build_investigation_prompt()
    test_citation_validator_valid()
    test_citation_validator_hallucinated()
    test_hypothesis_generator_grounded()
    test_hypothesis_generator_rejected_on_hallucination()
    print("All Group G tests passed.")
