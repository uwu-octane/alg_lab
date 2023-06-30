from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
import networkx as nx

class GameSolver:
    
    def __make_vars(self):
        self.vars = {n : tuple(self.model.NewBoolVar(f'x_{i}') for i in range(self.k)) for n in list(self.graph)}

        # Start points which have to be connected
        for i in range(self.k):
            self.vars[start[i][0]] = 1
            self.vars[start[i][1]] = 1

    def __single_selection_constraint(self):
        """ 
        Enforce that each node can only be once
        """ 
        for v in nx.nodes(self.graph):
            self.model.Add(cp_model.LinearExpr.Sum(self.vars[v]) == 1)
            #self.model.Add(cp_model.LinearExpr.Sum(cp_model.NewIntVar(self.vars[v][i]) for i in range(len(self.vars[v]))) == 1)

    def __connectivity_constraint(self):
        """ 
        Each path has to be continious
        """ 
        for e in nx.edges(self.graph):
            for i in range(self.k):
                self.model.Add(self.vars[e[0]][i] + self.vars[e[1]][i] == 2)

    def __degree_constraint(self):
        """ 
        Enfore degree on each node
        """ 
        for v in list(self.graph):
            # Check if v is a start node
            if v not in [n for t in self.start for n in t]:
                for i in range(self.k):
                    self.model.Add(cp_model.LinearExpr.Sum(self.vars[w][i] for w in nx.all_neighbors(self.graph,v)) == 2)
            else:
                for i in range(self.k):
                    self.model.Add(cp_model.LinearExpr.Sum(self.vars[w][i] for w in nx.all_neighbors(self.graph,v)) == 1)

        
    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.k = len(start)
        self.model = cp_model.CpModel()
        self.__make_vars()
        self.__single_selection_constraint()
        self.__connectivity_constraint()
        self.__degree_constraint()

    def solve(self):
        solver = self.model.CpSolver()
        status = solver.Solve(self.model)
        if status == self.model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if status != self.model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!") 

        return [n for n,b in self.vars.items if solver.Value(b) != 0]




G = nx.grid_2d_graph(5, 5)
start = [(list(G)[1], list(G)[21])]
solver = GameSolver(G, start)
print(solver.solve())

