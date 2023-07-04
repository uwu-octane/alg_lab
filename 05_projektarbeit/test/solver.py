from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
import networkx as nx


class GameSolver:

    def __make_vars(self):
        # graph.nodes
        self.node_vars = {n: tuple(self.model.NewBoolVar(f'{n}_{i}') for i in range(self.num_of_paths)) for n in
                          list(self.graph.nodes)}
        self.edge_vars = {e: tuple(self.model.NewBoolVar(f'{e}_{i}') for i in range(self.num_of_paths)) for e in
                          list(self.graph.edges)}

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
            self.model.Add(sum(self.node_vars[v]) == 1)

        """
        Enforce that each edge can only be used once
        """
        for e in nx.edges(self.graph):
            self.model.Add(sum(self.edge_vars[e]) == 1)

    def __connectivity_constraint(self):
        """ 
        Each path has to be continuous
        """
        for e in self.graph.edges:
            for path in range(self.num_of_paths):
                self.model.Add(self.node_vars[e[0]][path] + self.node_vars[e[1]][path] == 2) \
                    .OnlyEnforceIf(self.edge_vars[e][path])

    def __degree_constraint(self):
        """ 
        Enforce degree on each node
        """
        # Todo: maybe add OnlyEnforceIf(node_vars[v][i])
        for v in list(self.graph.nodes):
            # Check if v is a start node
            if v not in [n for t in self.start for n in t]:
                for path in range(self.num_of_paths):
                    v_in = sum(self.edge_vars[e][path] for e in self.graph.in_edges(v))
                    v_out = sum(self.edge_vars[e][path] for e in self.graph.out_edges(v))
                    self.model.Add(v_in + v_out == 2)
            else:
                for path in range(self.num_of_paths):
                    v_in = sum(self.edge_vars[e][path] for e in self.graph.in_edges(v))
                    v_out = sum(self.edge_vars[e][path] for e in self.graph.out_edges(v))
                    self.model.Add(v_in + v_out == 1)

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
