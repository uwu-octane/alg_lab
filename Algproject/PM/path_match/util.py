import colorsys
import random
from typing import List, Set, Tuple, Iterable, Optional
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import matplotlib.colors as mcolors

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
    print(color)

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
