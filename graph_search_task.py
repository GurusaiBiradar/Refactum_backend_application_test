import json
import os
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from pyvis.network import Network
import matplotlib.pyplot as plt

# ##################################################
# 1) Load workpiece graph and feature graph data from  json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

def load_graph(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = nx.Graph()
    
    # Add nodes
    for node_entry in data.get("nodes", []):
        node_id, attrs = node_entry
        G.add_node(node_id, **attrs)
    
    # Add edges 
    if "edges" in data:
        # Case 1: Explicit edges (like in feature_graph.json)
        for edge in data.get("edges", []):
            src, dst, attrs = edge
            G.add_edge(src, dst, **attrs)
    else:
        # Case 2: Edges from connected_faces (like in workpiece_graph.json)
        for node_entry in data.get("nodes", []):
            node_id, attrs = node_entry
            for neighbor in attrs.get("connected_faces", []):
                # Use default angular_type if not specified
                edge_attrs = {"angular_type": "CONVEX"}
                G.add_edge(node_id, neighbor, **edge_attrs)
    
    return G

# Load graphs
script_dir = os.path.dirname(os.path.abspath(__file__))
workpiece_graph = load_graph(os.path.join(script_dir, "workpiece_graph.json"))
feature_graph = load_graph(os.path.join(script_dir, "feature_graph.json"))

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

def visualize_graph(graph, title):
    plt.figure(figsize=(12, 8))
    
    # Node styling
    color_map = {
        'plane': '#2ecc71',    # Green
        'cylinder': '#e74c3c', # Red
        'cone': '#f39c12',     # Orange
        'torus': '#3498db',    # Blue
        'other': '#9b59b6'     # Purple
    }
    
    node_colors = []
    labels = {}
    for node in graph.nodes():
        node_type = graph.nodes[node]['type']
        node_colors.append(color_map.get(node_type, color_map['other']))
        labels[node] = f"{node}\n({node_type})"
    
    pos = nx.spring_layout(graph, seed=42)
    
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=800)
    nx.draw_networkx_edges(graph, pos, width=2, alpha=0.7)
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_color='black')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Visualize both graphs
print("Visualizing workpiece graph...")
visualize_graph(workpiece_graph, "Workpiece Graph")

print("\nVisualizing feature graph...")
visualize_graph(feature_graph, "Feature Graph")

# ##################################################
# 3) Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs
# ##################################################

def node_match(n1_attrs, n2_attrs):
    """Match nodes based on type"""
    return n1_attrs.get("type") == n2_attrs.get("type")

def edge_match(e1_attrs, e2_attrs):
    """Match edges based on angular_type"""
    return e1_attrs.get("angular_type") == e2_attrs.get("angular_type")

GM = GraphMatcher(
    workpiece_graph,  # Supergraph
    feature_graph,    # Subgraph
    node_match=node_match,
    edge_match=edge_match
)

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.

print("\n--- Results ---")
print("Feature graph is a subgraph of workpiece graph:", GM.subgraph_is_isomorphic())

if GM.subgraph_is_isomorphic():
    matches = list(GM.subgraph_isomorphisms_iter())
    print(f"Number of matches: {len(matches)}")
    for idx, mapping in enumerate(matches, 1):
        print(f"\nMatch {idx}:")
        for workpiece_node, feature_node in mapping.items():
            print(f"  Feature node {feature_node} ({feature_graph.nodes[feature_node]['type']}) "
                  f"→ Workpiece node {workpiece_node} ({workpiece_graph.nodes[workpiece_node]['type']})")
else:
    print("No matches found.")
