import unittest

import networkx as nx

from .solver import GameSolver
from .util import *


def print_dir():
    print(os.getcwd())


class MyTestCase(unittest.TestCase):
    def test_gen_start_points(self):
        G = gen_grid(4, 4)
        start = gen_start_points(4, 4, 4)
        print(list(start[0])[1])

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
                solver = GameSolver(G, start[1])
                edges, paths = solver.solve()
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
        store_in_json(G, start[1], edges, paths)
        for path in paths:
            print(len(path))
            # print("------------------")
            pass
        draw_result_colorful(edges, paths, G, False)

    def test_solver_constarint(self):
        print(get_src_dir())

    def test_read_jsonl(self):
        print(os.getcwd())
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
        if solver.validate():
            print(instance[0]['width'])
            width = instance[0]['width']
            height = instance[0]['height']
            g = gen_grid(width, height)
            draw_result_colorful(solver.get_result_edges(), solver.get_result_paths(), g, False)
            draw_result_colorful(instance_edges, instance[3], g, True)


if __name__ == '__main__':
    #unittest.main()
    print_dir()
