import unittest

from .solver import GameSolver
from .util import *


def test_gen_start_points():
    G = gen_grid(4, 4)
    start = gen_start_points(4, 4, 4)
    print(list(start[0])[1])


def test_solver():
    G = gen_grid(2, 4)
    #start = gen_start_points(6, G)
    start = [(0, 1), (1, 1)]
    #start = [(0, 0), (3,0), (0,1),(3,1),(0,2),(3,2),(0,3),(3,3)]
    #print(start[1])
    edges=[]
    paths=[]
    solver = GameSolver(G, start)
    edges, paths = solver.solve()
    """
    while True:
        try:
            solver = GameSolver(G, start)
            edges, paths = solver.solve()
            break
        except RuntimeError:
            start = gen_start_points(4, G)
            continue
    """
    #print(edges)
    draw_result_edges(edges, G)
    #draw_result_colorful(edges, paths, G)


def test_solver_constarint():
    G = gen_grid(2, 4)
    start = gen_start_points(2, G)
    solver = GameSolver(G, start)
    print(G.edges())
    draw_result_edges(G.edges, G)
    #solver.constraints_test()
    #print(list(G.edges((3,3))))
    #draw_result(solver.solve(), G)


class MyTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
