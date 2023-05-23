from typing import List, Set, Tuple, Iterable, Optional
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import random

Node = Tuple[int, int]
Edge = Tuple[Node, Node]

def squared_distance(p1: Node, p2: Node):
    """
    Calculate the squared euclidian distance between two points p1, p2.
    """
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def all_edges_sorted(points: Iterable[Node]) -> List[Node]:
    """
    Create a list containing all edges between each two points of the given
    point set/list and returns them in sorted, ascending order. 
    """
    edges = [(v,w) for v, w in itertools.combinations(points, 2)]
    edges.sort(key=lambda e: squared_distance(*e))  # *e is like e[0], e[1]
    return edges

def draw_edges(edges):
    """
    Draws the list of edges as a graph using networkx. The bottleneck
    edge is highlighted using a thicker stroke and red color.
    """
    draw_graph = nx.Graph(edges)
    g_edges = draw_graph.edges()
    max_length = max((squared_distance(*e) for e in g_edges))
    color = [('red' if squared_distance(*e) == max_length else 'black') for e in g_edges]
    width = [(1.0 if squared_distance(*e) == max_length else 0.5) for e in g_edges]
    plt.clf()
    fig, ax = plt.gcf(), plt.gca()
    fig.set_size_inches(8,6)
    nx.draw_networkx(draw_graph, pos={p: p for p in draw_graph.nodes}, node_size=8,
                     with_labels=False, edgelist=g_edges, edge_color=color, width=width, ax=ax)
    plt.show()
    
def random_points(n, w=10_000, h=10_000) -> Set[Node]:
    """
    n random points with integer coordinates within the w * h rectangle.
    :param n: Number of points
    :param w: The width of the rectangle.
    :param h: The height of the rectangle.
    :return: A set of points as (x,y)-tuples.
    """
    return set((random.randint(0,w), random.randint(0,h)) for _ in range(n))