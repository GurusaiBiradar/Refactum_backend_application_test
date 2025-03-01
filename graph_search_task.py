# ##################################################
# 1) Load workpiece graph and feature graph data from  json file
# ##################################################

# Note: Available files are: workpiece_graph.json, feature_graph.json

import json
import networkx as nx

def load_graph_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    G = nx.Graph()  # Use nx.DiGraph() if the graphs are directed.
    
    # Load nodes from JSON. Each node is given as [id, attributes]
    for node in data.get("nodes", []):
        node_id, attrs = node
        G.add_node(node_id, **attrs)
    
    # Load edges from JSON. Each edge is given as [source, target, attributes]
    for edge in data.get("edges", []):
        source, target, attrs = edge
        G.add_edge(source, target, **attrs)
    
    return G

# Load both graphs.
workpiece_graph = load_graph_from_json("workpiece_graph.json")
feature_graph = load_graph_from_json("feature_graph.json")


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


# TODO

# ##################################################
# 4) Results
# ##################################################

# Print results if matches are found. Return the number of matches and the node ids.

# TODO
