from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
import networkx as nx


class GameSolver:

    def __make_vars(self):
        # graph.nodes
        self.vars = {n: tuple(self.model.NewBoolVar(f'{n}_{i}') for i in range(self.num_of_paths)) for n in
                     list(self.graph.nodes)}

        # Start points which have to be connected
        for i in range(self.num_of_paths):
            n1, n2 = start[i]
            self.model.Add(self.vars[n1][i] == 1)
            self.model.Add(self.vars[n2][i] == 1)

    def __single_selection_constraint(self):
        """ 
        Enforce that each node can only be used once
        """
        for v in nx.nodes(self.graph):
            self.model.Add(sum(self.vars[v]) == 1)
            # self.model.Add(cp_model.LinearExpr.Sum(cp_model.NewIntVar(self.vars[v][i]) for i in range(len(
            # self.vars[v]))) == 1)

    def __connectivity_constraint(self):
        """ 
        Each path has to be continuous
        """
        for e in nx.edges(self.graph):
            self.model.Add((sum(self.vars[e[0]]) + sum(self.vars[e[1]])) == 2)

    def __degree_constraint(self):
        """ 
        Enforce degree on each node
        """
        for v in list(self.graph.nodes):
            # Check if v is a start node
            if v not in [n for t in self.start for n in t]:
                for i in range(self.num_of_paths):
                    self.model.Add(
                        sum(self.vars[w][i] for w in nx.all_neighbors(self.graph, v)) == 2)
            else:
                for i in range(self.num_of_paths):
                    self.model.Add(
                        sum(self.vars[w][i] for w in nx.all_neighbors(self.graph, v)) == 1)

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.num_of_paths = len(start)
        self.model = cp_model.CpModel()
        self.__make_vars()
        self.__single_selection_constraint()
        self.__connectivity_constraint()
        self.__degree_constraint()

    def solve(self):
        _solver = cp_model.CpSolver()
        status = _solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")

        return [n for n, b in self.vars.items if _solver.Value(b) != 0]


G = nx.grid_2d_graph(5, 5)

print(list(G.nodes))
start = [(list(G)[0], list(G)[20])]
print(start)
solver = GameSolver(G, start)
print(solver.solve())
