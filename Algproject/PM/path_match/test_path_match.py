import unittest

import networkx as nx

from .solver import GameSolver
from .util import *


def print_dir():
    print(os.getcwd())


class MyTestCase(unittest.TestCase):
    def test_solver(self):
        G = gen_grid(5, 10)
        start = gen_start_points(20, G)
        # start = [(0, 1), (1, 1)]
        # start = [(0, 0), (3,0), (0,1),(3,1),(0,2),(3,2),(0,3),(3,3)]
        # print(start[1])
        edges = []
        paths = []
        solver = None
        while True:
            try:
                solver = GameSolver(G, start)
                paths = solver.solve()
                break
            except RuntimeError:
                print("RuntimeError")
                start = gen_start_points(20, G)
                continue

        # print(paths))
        # print(start[1])
        # draw_result_edges(edges, G)
        print(solver.get_bottleneck())
        print("==============")
        store_in_json(start, paths)
        for path in paths:
            print(len(path))
            # print("------------------")
            pass
        draw_result_colorful(paths, False)
        #draw_result_edges(edges)

    def test_read_jsonl(self):
        data_list = read_json_lines()
        instances = handel_json_data(data_list)
        print(instances[0])
        # print(data['edges'])
        # print(data['paths'])

    def test_validate(self):
        data_list = read_json_lines()
        instances = handel_json_data(data_list)
        instance = instances[0]
        instance_edges = instance[2]
        G = nx.Graph()
        G.add_edges_from(instance_edges)
        start_points = instance[1]
        solver = GameSolver(G, start_points)


if __name__ == '__main__':
    # unittest.main()
    print_dir()
