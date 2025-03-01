import json
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

# ##################################################
# 1) Load workpiece graph and feature graph data from  json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    graph = nx.Graph()
    
    # Add nodes
    for node_entry in data['nodes']:
        node_id = node_entry[0]
        attributes = node_entry[1]
        graph.add_node(node_id, **attributes)
    
    # Add edges
    for edge_entry in data['edges']:
        source = edge_entry['source']
        target = edge_entry['target']
        attributes = edge_entry['attributes']
        graph.add_edge(source, target, **attributes)
    
    return graph

# Load graphs
feature_graph = load_graph_from_json('feature_graph.json')
workpiece_graph = load_graph_from_json('workpiece_graph.json')

# ##################################################
# 2) Create graphs from loaded data
# ##################################################

# Hint: The library networkx helps you to create a graph. You can use the nx.Graph() class to create a graph.
# Note: Other appraoches are also possible.

# TODO

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

# TODO
