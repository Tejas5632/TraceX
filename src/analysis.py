from __future__ import annotations

import math
from typing import Any, Dict, List

import networkx as nx

from src.graph import build_case_graph


def _safe_div(value: float) -> float:
    if value == 0:
        return 0.0
    return round(value, 4)


def analyze_case_graph(graph: nx.Graph) -> List[Dict[str, Any]]:
    if graph.number_of_nodes() == 0:
        return []

    degree = dict(graph.degree())
    betweenness = nx.betweenness_centrality(graph, normalized=True)
    pagerank = nx.pagerank(graph)

    ranking = []
    for node, attrs in graph.nodes(data=True):
        d = degree.get(node, 0)
        b = betweenness.get(node, 0.0)
        p = pagerank.get(node, 0.0)
        inf = _safe_div((d * 0.4) + (b * 60) + (p * 100))
        ranking.append(
            {
                "canonical_id": node,
                "canonical_name": attrs.get("canonical_name") or node,
                "entity_type": attrs.get("entity_type") or "UNKNOWN",
                "degree": d,
                "betweenness": round(b, 4),
                "pagerank": round(p, 4),
                "influence_score": inf,
            }
        )

    ranking.sort(key=lambda x: x["influence_score"], reverse=True)
    return ranking
