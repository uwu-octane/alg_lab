from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
import networkx as nx

class GameSolver:
    
    def __make_vars(self):
        self.vars = {n : tuple(self.model.NewBoolVar(f'{n}_{i}') for i in range(self.k)) for n in nx.nodes(self.graph)}

        for i in range(self.k):
            self.vars[start[i][0]] = 1
            self.vars[start[i][1]] = 1

    def __single_selection_constraint(self):
        """ 
        Enforce that each node can only be once
        """ 
        for v in nx.nodes(self.graph):
            self.model.Add(sum(self.vars[v]) == 1)

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
        for v in nx.nodes(self.graph):
            for i in range(self.k):
                self.model.Add(sum(self.vars[w][i] for w in nx.all_neighbors(self.graph,v)) == 2)

        
    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.k = len(start)
        self.model = cp_model.CpModel()

    def solve(self):
        self.__make_vars()
        self.__single_selection_constraint()
        self.__connectivity_constraint()
        self.__degree_constraint()
        


G = nx.grid_2d_graph(5, 5)
start = [(G.nodes[1], G.nodes[21])]
solver = GameSolver(G, start)

