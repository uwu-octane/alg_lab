import random
from typing import List, Set, Tuple, Iterable, Optional
import matplotlib.pyplot as plt
import networkx as nx
import itertools

Node = Tuple[int, int]
Edge = Tuple[Node, Node]


def gen_start_points(points_num, graph):
    if points_num % 2 != 0:
        raise ValueError("points_num must be even")

    nodes = list(graph.nodes())
    width = max([node[0] for node in nodes]) + 1
    height = max([node[1] for node in nodes]) + 1

    coordinates = set()
    while len(coordinates) < points_num:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        coordinates.add((x, y))
    coordinates = list(coordinates)
    start_points = {(coordinates[i], coordinates[i + 1]) for i in range(0, points_num, 2)}
    return start_points, coordinates


def gen_grid(grid_width, grid_height):
    return nx.grid_2d_graph(grid_width, grid_height, False)


def generate_random_rgb():
    r = random.random()
    g = random.random()
    b = random.random()
    return r, g, b


def draw_result_colorful(edges, paths, grid_graph):
    """
    draw grid graph
    """
    pos = {(x, y): (y, -x) for (x, y) in grid_graph.nodes()}  # 计算节点的布局
    # color = [('red' if e in edges else 'none') for e in G.nodes()]
    plt.clf()

    nx.draw_networkx_nodes(grid_graph, pos, node_color='skyblue', node_size=100)  # draw nodes
    nx.draw_networkx_labels(grid_graph, pos)

    for path in paths:
        """
        for every path generate a random color
        """
        color = generate_random_rgb()
        nx.draw_networkx_edges(grid_graph, pos, edgelist=path, edge_color=color, width=2.0)

        """
        highlight the start and end node
        """
        start_node = path[0][0]
        end_node = path[-1][1]
        nx.draw_networkx_nodes(grid_graph, pos, nodelist=[start_node, end_node], node_color="red", node_size=100)

    """
    hide other edges
    """
    nx.draw_networkx_edges(grid_graph, pos, edgelist=list(set(grid_graph.edges()) - set(edges)),
                           edge_color='none')  # hide other edges

    plt.show()


def draw_result_edges(edges, grid_graph):
    """
    draw grid graph
    """
    pos = {(x, y): (y, -x) for (x, y) in grid_graph.nodes()}  # 计算节点的布局
    # color = [('red' if e in edges else 'none') for e in G.nodes()]
    plt.clf()

    nx.draw_networkx_nodes(grid_graph, pos, node_color='skyblue', node_size=100)  # draw nodes
    nx.draw_networkx_labels(grid_graph, pos)
    nx.draw_networkx_edges(grid_graph, pos, edgelist=edges, edge_color='red', width=2.0)  # draw edges we want to show

    nx.draw_networkx_edges(grid_graph, pos, edgelist=list(set(grid_graph.edges()) - set(edges)),
                           edge_color='none')  # hide other edges

    plt.show()
