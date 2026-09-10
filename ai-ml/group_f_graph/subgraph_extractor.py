"""
Group F: Ego-Network and Subgraph Extraction.
Extracts localized graph neighborhoods for targeted target analysis.
"""

from typing import Dict, Any, List
import networkx as nx


def extract_ego_subgraph(graph: nx.Graph, center_node: str, radius: int = 1) -> nx.Graph:
    """
    Extract ego network centered at center_node with specified radius (hops).
    Returns empty graph if center_node is not in graph.
    """
    if not graph.has_node(center_node):
        return nx.Graph()
    return nx.ego_graph(graph, center_node, radius=radius, undirected=True)


def summarize_subgraph(subgraph: nx.Graph) -> Dict[str, Any]:
    """
    Summarize subgraph metrics for downstream feature analysis.
    """
    num_nodes = subgraph.number_of_nodes()
    num_edges = subgraph.number_of_edges()

    if num_nodes == 0:
        return {
            "num_nodes": 0,
            "num_edges": 0,
            "density": 0.0,
            "nodes": [],
        }

    density = round(nx.density(subgraph), 3)
    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "nodes": list(subgraph.nodes()),
    }
