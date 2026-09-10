import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from group_f_graph.co_occurrence import CoOccurrenceGraph, build_cooccurrence_candidate
from group_f_graph.subgraph_extractor import extract_ego_subgraph, summarize_subgraph
from group_f_graph.path_features import compute_path_distance, build_path_candidate
import networkx as nx


def test_co_occurrence_graph():
    cog = CoOccurrenceGraph()
    cog.add_document("doc1", ["entity_a", "entity_b", "entity_c"])
    cog.add_document("doc2", ["entity_a", "entity_b"])

    assert cog.get_co_occurrence("entity_a", "entity_b") == 2
    assert cog.get_co_occurrence("entity_a", "entity_c") == 1
    assert cog.get_co_occurrence("entity_b", "entity_c") == 1
    assert cog.get_co_occurrence("entity_a", "entity_d") == 0


def test_cooccurrence_candidate():
    cog = CoOccurrenceGraph()
    cog.add_document("doc1", ["ent_1", "ent_2"])
    cand = build_cooccurrence_candidate(cog, "ent_1", "ent_2", "doc_ref_1", min_count=1)

    assert cand.subject_a == "ent_1"
    assert cand.subject_b == "ent_2"
    assert cand.family == "F8"
    assert cand.polarity == "+"
    assert cand.raw_log_lr > 0
    assert cand.extra["co_occurrence_count"] == 1


def test_ego_subgraph():
    g = nx.Graph()
    g.add_edge("node_a", "node_b")
    g.add_edge("node_b", "node_c")
    g.add_edge("node_c", "node_d")

    sub = extract_ego_subgraph(g, "node_b", radius=1)
    summary = summarize_subgraph(sub)

    assert summary["num_nodes"] == 3
    assert set(summary["nodes"]) == {"node_a", "node_b", "node_c"}
    assert summary["density"] > 0


def test_path_features():
    g = nx.Graph()
    g.add_edge("user_1", "user_2")
    g.add_edge("user_2", "user_3")
    g.add_node("user_isolated")

    # Direct connection (1 hop)
    cand_direct = build_path_candidate(g, "user_1", "user_2", "doc_path_1")
    assert cand_direct.family == "F8"
    assert cand_direct.polarity == "+"
    assert cand_direct.extra["path_distance"] == 1
    assert cand_direct.raw_log_lr == 0.8

    # 2 hops
    cand_2hop = build_path_candidate(g, "user_1", "user_3", "doc_path_2")
    assert cand_2hop.polarity == "+"
    assert cand_2hop.extra["path_distance"] == 2
    assert cand_2hop.raw_log_lr == 0.4

    # Unreachable
    cand_unreach = build_path_candidate(g, "user_1", "user_isolated", "doc_path_3")
    assert cand_unreach.polarity == "-"
    assert cand_unreach.extra["path_distance"] is None
    assert cand_unreach.raw_log_lr == 0.0


if __name__ == "__main__":
    test_co_occurrence_graph()
    test_cooccurrence_candidate()
    test_ego_subgraph()
    test_path_features()
    print("All Group F tests passed.")
