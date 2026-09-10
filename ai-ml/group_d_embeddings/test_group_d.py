import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_d_embeddings.text_embeddings import compute_text_similarity, build_text_embedding_candidate
from group_d_embeddings.similarity_index import SimilarityIndex


def test_text_similarity_identical():
    sim = compute_text_similarity("Vendor delivery worldwide 24/7", "Vendor delivery worldwide 24/7")
    assert sim >= 0.99


def test_text_similarity_different():
    sim = compute_text_similarity("Vendor delivery worldwide 24/7", "Completely unrelated text about astronomy")
    assert sim < 0.5


def test_candidate_contract():
    cand = build_text_embedding_candidate("acc_1", "acc_2", "Same text", "Same text", "doc_01")
    assert cand.subject_a == "acc_1"
    assert cand.subject_b == "acc_2"
    assert cand.family == "F6"
    assert cand.raw_log_lr > 0
    assert "similarity_score" in cand.extra


def test_similarity_index():
    index = SimilarityIndex()
    index.add("doc_a", "PGP encrypted communication only")
    index.add("doc_b", "PGP encrypted communication direct")
    index.add("doc_c", "Fresh apples and oranges for sale")

    results = index.search("PGP encrypted communication", top_k=2)
    assert len(results) >= 1
    assert results[0][0] in ("doc_a", "doc_b")


if __name__ == "__main__":
    test_text_similarity_identical()
    test_text_similarity_different()
    test_candidate_contract()
    test_similarity_index()
    print("All Group D tests passed.")
