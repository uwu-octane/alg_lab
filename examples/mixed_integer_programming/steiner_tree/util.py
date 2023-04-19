from typing import List, Set, Optional, Any, Tuple
import networkx as nx
import matplotlib.pyplot as plt

Node = Any
Edge = Tuple[Node, Node]

def parse_graph_from_edgelist_file(path: str) -> nx.Graph:
    """
    A simple method for parsing an undirected graph from a list of edges in the following format:
    
    1-2
    1-5
    2-3
    3-4
    3-5
    """

    graph = nx.Graph()
    with open(path, "r") as f:
        for line in f.read().split():
            t = line.split("-")
            assert len(t) == 2
            p, q = t
            assert str(p).isdigit() and str(q).isdigit()
            graph.add_edge(p, q)
    return graph

def visualize_fvs(graph: nx.Graph, feedback_vertex_set: Set[Node]):
    """
    Draws a 'before-after' visualization of a given Feedback Vertex Set solution on a given graph.
    """
    layout = nx.layout.kamada_kawai_layout(graph)
    nx.draw_networkx(graph, pos=layout, node_color=["red" if p in feedback_vertex_set else "cyan" for p in graph.nodes()])
    plt.show()
    _graph = graph.copy()
    _graph.remove_nodes_from(feedback_vertex_set)
    nx.draw_networkx(_graph, pos=layout, node_color="cyan")
    plt.show()