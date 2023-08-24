import unittest

from .solver import GameSolver
from .util import *


def print_dir():
    print(os.getcwd())


class MyTestCase(unittest.TestCase):
    def test_solver(self):
        G = gen_grid(10, 10)
        start = gen_start_points(10, G)
        # start = [(0, 1), (1, 1)]
        # start = [(0, 0), (3,0), (0,1),(3,1),(0,2),(3,2),(0,3),(3,3)]

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
                start = gen_start_points(10, G)
                continue

        # print(paths))
        # print(start[1])
        # draw_result_edges(edges, G)
        print(solver.get_start_points())
        draw_result_colorful(paths, True)
        # draw_result_edges(edges)

    def test_read_jsonl(self):
        data_list = read_json_lines()
        instances = handel_json_data(data_list)
        print(instances[0])
        # print(data['edges'])
        # print(data['paths'])

    def test_validate(self):
        data_list = read_json_lines()
        instances = handel_json_data(data_list)
        instance = instances[-1]
        instance_paths = instance[1]
        G = nx.Graph()
        for path in instance_paths:
            for edge in path:
                G.add_edge(edge[0], edge[1])
        start_points = instance[0]
        solver = GameSolver(G, start_points)
        solver.constraints_test()


if __name__ == '__main__':
    # unittest.main()
    print_dir()
