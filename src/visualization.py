from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import networkx as nx

from src.graph import build_case_graph
from src.ingestion import load_case


def create_network_html(case_id: str, height: int = 650) -> str:
    graph = build_case_graph(case_id)
    nodes = []
    for node, attrs in graph.nodes(data=True):
        color = '#1f77b4'
        if attrs.get('entity_type') == 'ORGANIZATION':
            color = '#2ca02c'
        elif attrs.get('entity_type') == 'LOCATION':
            color = '#ff7f0e'
        nodes.append({
            'id': node,
            'label': attrs.get('canonical_name') or node,
            'group': attrs.get('entity_type') or 'PERSON',
            'title': attrs.get('canonical_name') or node,
            'value': max(15, graph.degree(node) * 10 + 10),
            'color': color,
        })

    edges = []
    for src, dst, attrs in graph.edges(data=True):
        edges.append({
            'from': src,
            'to': dst,
            'label': attrs.get('relationship_type', 'ASSOCIATED_WITH'),
            'title': attrs.get('relationship_type', 'ASSOCIATED_WITH'),
        })

    payload = {
        'nodes': nodes,
        'edges': edges,
        'height': height,
    }

    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <script type="text/javascript" src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
        <link href="https://unpkg.com/vis-network@9.1.2/dist/dist/vis-network.min.css" rel="stylesheet" type="text/css" />
        <style>
          body {{ margin: 0; padding: 0; background: #0e1117; color: #e6eef3; }}
          #mynetwork {{ width: 100%; height: {height}px; border: 1px solid rgba(255,255,255,0.06); }}
        </style>
      </head>
      <body>
        <div id="mynetwork"></div>
        <script>
          const nodes = new vis.DataSet({json.dumps(payload['nodes'])});
          const edges = new vis.DataSet({json.dumps(payload['edges'])});
          const container = document.getElementById('mynetwork');
          const data = {{ nodes: nodes, edges: edges }};
          const options = {{
            physics: {{ enabled: true, stabilization: {{ enabled: true, iterations: 250 }}, barnesHut: {{ gravitationalConstant: -2500, springLength: 180 }} }},
            nodes: {{ shape: 'dot', size: 18, font: {{ color: '#ffffff', size: 16 }}, borderWidth: 2 }},
            edges: {{ color: {{ color:'#9aa4ae' }}, font: {{ align: 'horizontal', size: 12, color: '#e6eef3' }}, smooth: {{ enabled: true, type: 'dynamic' }} }},
            interaction: {{ hover: true, multiselect: false, dragNodes: true, zoomView: true }},
            layout: {{ improvedLayout: true }}
          }};
          const network = new vis.Network(container, data, options);
        </script>
      </body>
    </html>
    """
    return html
