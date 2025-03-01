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

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = nx.Graph()
    for node in data.get("nodes", []):
        node_id, attrs = node
        G.add_node(node_id, **attrs)
    for edge in data.get("edges", []):
        source, target, attrs = edge
        G.add_edge(source, target, **attrs)
    return G

# Load graphs
script_dir = os.path.dirname(os.path.abspath(__file__))
feature_graph = load_graph_from_json(os.path.join(script_dir, 'feature_graph.json'))
workpiece_graph = load_graph_from_json(os.path.join(script_dir, 'workpiece_graph.json'))

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

def visualize_graph(graph, title):
    plt.figure(figsize=(12, 8))
    
    # Create node colors based on type
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
    
    # Generate layout positions
    pos = nx.spring_layout(graph, seed=42)
    
    # Draw graph elements
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

# Note: Optional task - Visualize the graph
# Example code:
# from pyvis.network import Network
# nt = Network()
# nt.from_nx(workpiece_graph)
# nt.show("graph.html", notebook=False)

# ##################################################
# 3) Check if the feature graph is a subgraph of the workpiece workpiece and find any other matching subgraphs
# ##################################################

def node_match(node1, node2):
    return node1.get('type') == node2.get('type')

def edge_match(edge1, edge2):
    return edge1.get('angular_type') == edge2.get('angular_type')

def find_matching_subgraphs(feature_g, workpiece_g):
    matcher = GraphMatcher(workpiece_g, feature_g, node_match=node_match, edge_match=edge_match)
    return list(matcher.subgraph_isomorphisms_iter())

matching_subgraphs = find_matching_subgraphs(feature_graph, workpiece_graph)

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.

def print_results(matches):
    if not matches:
        print("No matching subgraphs found.")
        return
    
    print(f"Found {len(matches)} matching subgraphs:")
    for i, mapping in enumerate(matches, 1):
        print(f"Match {i}:")
        for fg_node, wp_node in mapping.items():
            print(f"  Feature node {fg_node} -> Workpiece node {wp_node}")

print_results(matching_subgraphs)
