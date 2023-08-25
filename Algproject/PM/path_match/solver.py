import networkx as nx

from ortools.sat.python import cp_model


class GameSolver:
    def __make_vars(self):

        self.edge_vars = {(v, w): self.model.NewBoolVar(f'x_{v},{w}')
                          for v in self.nodes for w in list(self.graph.neighbors(v))}

        self.node_to_path = {n: tuple(self.model.NewBoolVar(f'{n}_{i}')
                                      for i in range(self.num_paths)) for n in self.nodes}

        self.depth_vars = {v: self.model.NewIntVar(0, self.num_nodes - 1, f'd_{v}') for v in self.nodes}
        self.bottleneck_var = self.model.NewIntVar(0, len(self.nodes) - 1, 'b')
        self.model.Minimize(self.bottleneck_var)

    def __add_bottleneck_constraints(self):
        """
        Add the constraints to ensure that only
        """
        for v in self.depth_vars.keys():
            self.model.Add(self.bottleneck_var >= self.depth_vars[v])

    def constraints_test(self):
        # print(self.node_to_path)

        for v in self.start_points:
            for j in range(self.num_paths):
                if self.solver.Value(self.node_to_path[v][j]) == 1:
                    print(v, j)
                    continue

    def __edge_number_constraint(self):
        """
        Cause every node has to be used once, and the path num is known, so we can get the number of edges in graph
        let |path| be the number of nodes in a path, then |path| - 1 = |edges| in this case
        |path_1| -1 + |path_2| -1 + ... + |path_n| -1 = num_nodes - num_paths
        """
        self.model.Add(sum(self.edge_vars.values()) == self.num_nodes - self.num_paths)

    def __path_selection_constraint(self):
        """
        if node in paths[i], node cant be in other paths
        """
        for v in self.nodes:
            self.model.Add(sum(self.node_to_path[v][i] for i in range(self.num_paths)) == 1)

        """
        give every start_points a path var and ensure the start, end of a path share the same var
        """
        count = 0
        for i in range(len(self.start_points)):
            # Only use every second node to select one of the start and end points to be on the path
            if i % 2 == 0:
                self.model.Add(self.node_to_path[self.start_points[i]][count] == 1)
                self.model.Add(self.node_to_path[self.start_points[i + 1]][count] == 1)
                count += 1

        """
        for connected nodes we set the same path var
        """
        for (v, w), x_vw in self.edge_vars.items():
            for i in range(self.num_paths):
                self.model.Add(self.node_to_path[v][i] == self.node_to_path[w][i]).OnlyEnforceIf(x_vw)

    def __add_degree_constraints(self):
        """
        Add an upper limit to the degree of every node.
        """

        for v in self.nodes:
            # "Count" the number of incoming and outgoing edges.
            vin, vout = 0, 0
            """
            its easier to only consider the neighbors of v, cause this is a grid graph
            """
            for w in list(self.graph.neighbors(v)):
                vin += self.edge_vars[w, v]
                vout += self.edge_vars[v, w]

            """
            in start_points, they are ethier the start or end of a path, so they have only one incident edge
            """
            if v in self.start_points:
                self.model.Add(vin + vout == 1)
            else:
                self.model.Add(vin == 1)  # exactly one incoming edge
                self.model.Add(vout == 1)  # exactly one outgoing edge

    def __forbid_bidirectional_edges(self):
        """
        Add the (redundant) constraints x_{v,w} -> !x_{w, v}.
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
        """
        for every 2 nodes in start_points we set the depth to 0, so every path starts independently with this points
        change the choice of start_points may change the resulted path 
        """
        for i in range(len(self.start_points)):
            if i % 2 == 0:
                self.model.Add(self.depth_vars[self.start_points[i]] == 0)

        # If the edge v -> w is selected, d(v) + 1 == d(w) must hold.
        for (v, w), x_vw in self.edge_vars.items():
            """
            force the depth of w to be one greater than the depth of v if the edge v -> w is selected.
            """
            self.model.Add(self.depth_vars[w] == self.depth_vars[v] + 1).OnlyEnforceIf(x_vw)

    def __init__(self, graph, start_points, bottleneck=True):
        self.graph = graph
        self.nodes = list(self.graph.nodes)
        self.edges = list(self.graph.edges)

        self.start_points = start_points

        self.num_nodes = len(self.graph.nodes)
        self.num_paths = len(start_points) // 2

        self.model = cp_model.CpModel()
        self.__make_vars()
        if bottleneck:
            self.__add_bottleneck_constraints()
        self.__add_degree_constraints()
        self.__edge_number_constraint()
        self.__forbid_bidirectional_edges()
        self.__add_depth_constraints()
        self.__path_selection_constraint()

        self.bottleneck_var_value = -1
        self.result = None
        self.status = None
        self.solver = None

    def get_start_points(self):
        return self.start_points

    def get_result(self):
        if self.result is None:
            raise RuntimeError("No solution found yet!")
        return self.result

    def get_instance(self):
        return self.start_points, self.result

    def get_bottleneck(self):
        if self.bottleneck_var_value > 0:
            return self.bottleneck_var_value
        else:
            print("no solution found yet")

    def get_path_depth(self):
        return self.depth_vars.values()

    def get_path_var(self, v):
        for j in range(self.num_paths):
            if self.solver.Value(self.node_to_path[v][j]) == 1:
                # print(v, j)
                return j
        return -1

    def validate(self):
        if len(self.edges) != self.num_nodes - self.num_paths:
            print("The number of edges is not correct!")
            return False
        try:
            self.solve()
        except RuntimeError:
            pass
        if self.status == cp_model.INFEASIBLE:
            print("The model was classified infeasible by the solver!")
            return False
        if self.status != cp_model.OPTIMAL:
            print("Unexpected status after running solver!")
            return False
        return True

    def solve(self):
        """
        Find the optimal solution to the initialized instance.
        Returns the DBST edges as a list of coordinate tuple tuples ((x1,y1),(x2,y2)).
        """
        self.solver = cp_model.CpSolver()
        self.status = self.solver.Solve(self.model)
        if self.status == cp_model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if self.status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")

        edges = [(v, w) for (v, w), x_vw in self.edge_vars.items() if self.solver.Value(x_vw) != 0]

        """
        use nx.connected_components to find the connected components of the graph, which are the paths we want
        it returns a set of nodes, cause it is a set, so we have to resort the nodes according to the depth
        """

        nodes_paths = [sorted(nodes_path, key=lambda x: self.solver.Value(self.depth_vars[x])) for nodes_path in
                       nx.connected_components(nx.Graph(edges))]
        paths = [[(sorted_node_path[i], sorted_node_path[i + 1]) for i in range(len(sorted_node_path) - 1)] for
                 sorted_node_path in nodes_paths]

        self.bottleneck_var_value = self.solver.Value(self.bottleneck_var)
        self.result = paths

        return paths
