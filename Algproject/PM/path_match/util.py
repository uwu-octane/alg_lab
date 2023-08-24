import colorsys
import json
import os
import random
from typing import Tuple

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx

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
    return coordinates


def gen_grid(grid_width, grid_height):
    return nx.grid_2d_graph(grid_width, grid_height, False)


def is_clear_color(hex_color, brightness_threshold=0.4, saturation_threshold=0.3):
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    # 将RGB颜色转换为HSL颜色模式
    h, l, s = colorsys.rgb_to_hls(red / 255.0, green / 255.0, blue / 255.0)

    # 检查亮度和饱和度是否符合条件
    return brightness_threshold <= l <= 0.5 and saturation_threshold <= s <= 0.5


def generate_random_rgb_from_hex():
    while True:
        color = random.choice(list(mcolors.CSS4_COLORS.values()))
        if is_clear_color(color):
            return color


def hex_to_rgb(hex_color):
    # remove the potential signal “#”
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


def draw_result_colorful(paths, with_laber=False):
    """
    draw grid graph
    """
    edges = []
    for path in paths:
        edges.extend(path)

    grid_graph = nx.Graph()
    grid_graph.add_edges_from(edges)

    pos = {(x, y): (y, -x) for (x, y) in grid_graph.nodes()}  # 计算节点的布局
    # color = [('red' if e in edges else 'none') for e in G.nodes()]
    plt.clf()

    nx.draw_networkx_nodes(grid_graph, pos, node_color='skyblue', node_size=1)  # draw nodes
    if with_laber:
        nx.draw_networkx_labels(grid_graph, pos)

    for path in paths:
        """
        for every path generate a random color
        """
        color = generate_random_rgb_from_hex()
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


def draw_result_edges(edges):
    """
    draw grid graph
    """
    g = nx.Graph()
    g.add_edges_from(edges)
    pos = {(x, y): (y, -x) for (x, y) in g.nodes()}  # 计算节点的布局
    # color = [('red' if e in edges else 'none') for e in G.nodes()]
    plt.clf()

    nx.draw_networkx_nodes(g, pos, node_color='skyblue', node_size=1)  # draw nodes
    # nx.draw_networkx_labels(g, pos)
    nx.draw_networkx_edges(g, pos, edgelist=edges, edge_color='red', width=2.0)  # draw edges we want to show

    nx.draw_networkx_edges(g, pos, edgelist=list(set(g.edges()) - set(edges)),
                           edge_color='none')  # hide other edges

    plt.show()


"""
def json_to_graph(json_str):
    graph_data = json.loads(json_str)
    # Extract the source and target information from each edge
    points_data = graph_data['points']
    points = [(point['x'], point['y']) for point in points_data]
    edges_data = graph_data['edges']
    edges = [(edge['source'], edge['target']) for edge in edges_data]
    edges = tuple((tuple(coord1), tuple(coord2)) for coord1, coord2 in edges)
    return points, edges
"""


def __get_jsonl_dir():
    utils_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.dirname(utils_dir) + "/src/instances.jsonl"
    return src_dir


def store_in_json(start_points, paths):
    """
    store the result in json file
    """

    start_points = [{'x': x, 'y': y} for x, y in start_points]

    path = [[{'source': x, 'target': y} for x, y in p] for p in paths]
    instance = {
        "start_points": start_points,
        "paths": path
    }
    file_path = __get_jsonl_dir()
    with open(file_path, 'a') as f:
        json.dump(instance, f)
        f.write("\n")


def read_json_lines():
    """
    Read and parse JSON Lines from a file.
    Returns a list of parsed JSON objects.
    """
    file_path = __get_jsonl_dir()
    data_list = []
    with open(file_path, 'r') as f:
        for line in f:
            # Strip the newline character from the end of the line
            line = line.strip()

            # Parse the JSON object in the line
            data = json.loads(line)
            data_list.append(data)

    return data_list


def handel_json_data(data_list):
    instances = []
    for data in data_list:
        points_data = data['start_points']
        start_points = [(point['x'], point['y']) for point in points_data]

        paths_data = data['paths']
        paths = []
        for path in paths_data:
            path_edges = [(edge['source'], edge['target']) for edge in path]
            path_edges = [(tuple(coord1), tuple(coord2)) for coord1, coord2 in path_edges]
            paths.append(path_edges)
        instance = (start_points, paths)
        instances.append(instance)
    return instances
