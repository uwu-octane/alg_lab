import unittest

import networkx as nx

from .solver import GameSolver
from .util import *

class MyTestCase(unittest.TestCase):
    def test_gen_start_points(self):
        G = gen_grid(4, 4)
        start = gen_start_points(4, 4, 4)
        print(list(start[0])[1])


    def test_solver(self):
        G = gen_grid(5, 10)
        start = gen_start_points(20, G)
        #start = [(0, 1), (1, 1)]
        #start = [(0, 0), (3,0), (0,1),(3,1),(0,2),(3,2),(0,3),(3,3)]
        #print(start[1])
        edges=[]
        paths=[]
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

        #print(paths))
        #print(start[1])
    # draw_result_edges(edges, G)

        draw_result_colorful(edges, paths, G, False)


    def test_solver_constarint(self):
        G = gen_grid(10, 10)
        start = gen_start_points(6, G)
        solver = GameSolver(G, start[1])
        solver.constraints_test()

if __name__ == '__main__':
    unittest.main()
