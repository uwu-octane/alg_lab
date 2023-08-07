import colorsys
import random
from typing import List, Set, Tuple, Iterable, Optional
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import matplotlib.colors as mcolors
import json
import os
import time

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
    # color = random.choice(list(mcolors.CSS4_COLORS.keys()))
    # print(color)
    # 获取所有颜色及其对应的RGB值
    colors_with_rgb = mcolors.CSS4_COLORS
    color = random.choice(list(mcolors.CSS4_COLORS.values()))
    # 打印所有颜色及其对应的RGB值
    # print(color)

    return color


def is_bright_color(hex_color, threshold=128):
    hex_color = hex_color.lstrip("#")
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)

    # 计算亮度（Luminance）
    luminance = (0.2126 * red) + (0.7152 * green) + (0.0722 * blue)

    # 根据给定的阈值判断是否为亮色
    return luminance >= threshold


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
        color = generate_random_rgb()
        if is_clear_color(color):
            return color


def draw_result_colorful(edges, paths, grid_graph, with_laber=False):
    """
    draw grid graph
    """
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


def store_in_json(grid, start_points, edges, paths, instance_file_path):
    """
    store the result in json file
    """
    if not os.path.exists(instance_file_path):
        project_dir = os.getcwd()  # Get the current working directory (project directory)

        instance_file_name = "instances" + ".jsonl"
        instance_file_path = os.path.join(project_dir, instance_file_name)

    nodes = list(grid.nodes())
    width = max([node[0] for node in nodes]) + 1
    height = max([node[1] for node in nodes]) + 1

    start_points = [{'x': x, 'y': y} for x, y in start_points]
    edges = [{'source': v, 'target': w} for v, w in edges]
    path = [[{'source': x, 'target': y} for x, y in p] for p in paths]
    instance = {
        "grid": [{'width': width, 'height': height}],
        "start_points": start_points,
        "edges": edges,
        "paths": path
    }

    with open(instance_file_path, 'a') as f:
        json.dump(instance, f)
        f.write("\n")


def read_json_lines(file_path):
    """
    Read and parse JSON Lines from a file.
    Returns a list of parsed JSON objects.
    """
    data_list = []
    with open(file_path, 'r') as f:
        for line in f:
            # Strip the newline character from the end of the line
            line = line.strip()

            # Parse the JSON object in the line
            data = json.loads(line)
            data_list.append(data)

    return data_list


def handel_json_data():
    data_list = read_json_lines("../instances.jsonl")
    instances = []
    for data in data_list:
        grid_data = data['grid']
        points_data = data['start_points']
        start_points = [(point['x'], point['y']) for point in points_data]

        edges_data = data['edges']
        edges = [(edge['source'], edge['target']) for edge in edges_data]
        edges = [(tuple(coord1), tuple(coord2)) for coord1, coord2 in edges]

        paths_data = data['paths']
        paths = []
        for path in paths_data:
            path_edges = [(edge['source'], edge['target']) for edge in path]
            path_edges = [(tuple(coord1), tuple(coord2)) for coord1, coord2 in path_edges]
            paths.append(path_edges)
        instance = (grid_data, start_points, edges, paths)
        instances.append(instance)
    return instances