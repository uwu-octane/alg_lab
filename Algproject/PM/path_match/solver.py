import networkx as nx
from matplotlib import pyplot as plt

from ortools.sat.python import cp_model
import itertools


class GameSolver:
    def __make_vars(self):
        # graph.nodes

        # self.edge_vars = {(v, w): self.model.NewBoolVar(f'x_{v},{w}')
        #                  for v, w in self.edges}

        self.edge_vars = {(v, w): self.model.NewBoolVar(f'x_{v},{w}')
                          for v in self.nodes for w in list(self.graph.neighbors(v))}

        self.node_vars = {v: self.model.NewBoolVar(f'x_{v}') for v in self.nodes}

        self.node_to_path = {n: tuple(self.model.NewBoolVar(f'{n}_{i}')
                                      for i in range(self.num_paths)) for n in self.nodes}

        self.depth_vars = {v: self.model.NewIntVar(0, self.num_nodes - 1, f'd_{v}') for v in self.nodes}

        """
        
        
        self.node_vars = {v: self.model.NewBoolVar(f'x_{v}') for v in range(self.num_nodes)}
        self.edge_vars = {e: self.model.NewBoolVar(f'x_{e}') for e in range(len(self.edges))}
        self.depth_vars = {v: self.model.NewIntVar(0, self.num_nodes - 1, f'd_{v}') for v in self.nodes}
        self.node_to_path = {n: tuple(self.model.NewBoolVar(f'{n}_{i}') for i in range(self.num_paths)) for n in
                             range(self.num_nodes)}
        """

    def constraints_test(self):
        # print(self.node_to_path)
        self.model.Add(self.node_to_path[(0, 0)][0] == 1)
        for v in self.nodes:
            # "Count" the number of incoming and outgoing edges.
            vin, vout = 0, 0
            v_neighbors = list(self.graph.neighbors(v))
            neighbors_edges = list(self.graph.edges(v))
            # print("v_neighbor for ", v, " : ", v_neighbors)
            print("neighbors_edges for ", v, " : ", neighbors_edges)
        # print(self.edge_vars)

    def __single_selection_constraint(self):
        """
        Enforce that each node has be used once
        """
        self.model.Add(sum(self.node_vars.values()) == self.num_nodes)

        self.model.Add(sum(self.edge_vars.values()) == self.num_nodes - self.num_paths)

    def __path_selection_constraint(self):
        """
        if node in paths[i], node cant be in other paths
        """
        for v in self.nodes:
            self.model.Add(sum(self.node_to_path[v][i] for i in range(self.num_paths)) == 1)

    def __add_degree_constraints(self):
        """
        Add an upper limit to the degree of every node.
        """

        for v in self.nodes:
            # "Count" the number of incoming and outgoing edges.
            vin, vout = 0, 0
            for w in list(self.graph.neighbors(v)):
                vin += self.edge_vars[w, v]
                vout += self.edge_vars[v, w]

            if v in self.start_points:
                self.model.Add(vin + vout == 1)
            else:
                self.model.Add(vin == 1)  # exactly one incoming edge
                self.model.Add(vout == 1)  # exactly one outgoing edge

    def __forbid_bidirectional_edges(self):
        """
        Add the (redundant) constraints x_{v,w} -> !x_{w, v}.

        for v in self.nodes:
            for w in list(self.graph.neighbors(v)):
                self.model.AddBoolOr([self.edge_vars[v, w].Not(), self.edge_vars[w, v].Not()])
        """
        for v, w in self.edge_vars:
            self.model.AddBoolOr([self.edge_vars[v, w].Not(), self.edge_vars[w, v].Not()])

    def __add_depth_constraints(self):
        """
        Add the depth constraints x_{v,w} -> d_w = d_v + 1 which guarantee the
        validity of the arborescence.
        hier this constratins works to ensuer no subcrycles in the solution
        """

        # without loss of generality, force one node to be the root.
        for i in range(len(self.start_points), 2):
            self.model.Add(self.depth_vars[self.start_points[i]] == 0)
            for w in self.nodes:
                self.model.Add(self.edge_vars[w, self.start_points[i]].Not())

        # If the edge v -> w is selected, d(v) + 1 == d(w) must hold.
        for (v, w), x_vw in self.edge_vars.items():
            """
            force the depth of w to be one greater than the depth of v if the edge v -> w is selected.
            """
            self.model.Add(self.depth_vars[w] == self.depth_vars[v] + 1).OnlyEnforceIf(x_vw)

    def __init__(self, graph, start_points):
        self.graph = graph
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

        # self.start_points_paar = list({(start_points[i], start_points[i + 1]) for i in range(0, len(start_points), 2)})
        self.start_points = start_points

        self.num_nodes = len(self.graph.nodes)
        self.num_paths = len(start_points) // 2

        self.model = cp_model.CpModel()
        self.__make_vars()
        # self.constraints_test()
        self.__add_degree_constraints()
        self.__single_selection_constraint()
        self.__forbid_bidirectional_edges()
        self.__add_depth_constraints()
        self.__path_selection_constraint()


    def solve(self):
        """
        Find the optimal solution to the initialized instance.
        Returns the DBST edges as a list of coordinate tuple tuples ((x1,y1),(x2,y2)).
        """
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")
        """
        for v, v_p in self.node_vars.items():
            print(f'Node {v}')
        """
        edges = [(v, w) for (v, w), x_vw in self.edge_vars.items() if solver.Value(x_vw) != 0]
        paths_nodes = []
        for i in range(self.num_paths):
            path_node = []
            for v in self.nodes:
                if solver.Value(self.node_to_path[v][i]) != 0:
                    path_node.append(v)
            paths_nodes.append(path_node)
        """
        make points sequence to edges
        """
        paths = []
        for path_node in paths_nodes:
            path = []
            for i in range(len(path_node) - 1):
                path.append((path_node[i], path_node[i + 1]))
            paths.append(path)
        return edges, paths
