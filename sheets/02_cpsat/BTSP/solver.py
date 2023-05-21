from ortools.sat.python import cp_model
import itertools


def squared_distance(p1, p2):
    """
    Calculate the squared euclidian distance (in order to minimze the use of the sqrt() operation).
    """
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class BTSPSolverCP:
    """ensure the maximum of the cost of the edges in the cycle is minimized."""

    # every edge has a cost.
    def __calculate_distances(self) -> int:
        """
        Precalculate the costs of all edges. The side effect of this method
        is the calculated max_distance, which is necessary in order to specify
        our bottleneck variable's upper bound.
        """
        self.distances = {(i, j): squared_distance(self.points[i], self.points[j])
                          for (i, j) in itertools.permutations(range(len(self.points)), 2)}
        self.max_distance = max(self.distances.values())
        self.min_distance = min(self.distances.values())

    # the maximum of the cost of the edges in the cycle is the bottleneck.

    # the bottleneck must be minimized.

    # the bottleneck must be smaller than or equal to the cost of every edge in the cycle.

    def __make_vars(self):
        """create all involved variables and set the minimization objective."""
        self.edge_vars = {(v, w): self.model.NewBoolVar(f'x_{v},{w}')
                          for v, w in itertools.permutations(range(self.n), 2)}

        self.depth_vars = {v: self.model.NewIntVar(0, self.n - 1, f'd_{v}') for v in range(self.n)}

        """ensure the maximum of the cost of the edges in the cycle is minimized."""
        self.bottleneck_var = self.model.NewIntVarFromDomain(cp_model.Domain.FromValues(list(self.distances.values())),
                                                             'bottleneck_var')
        self.model.Minimize(self.bottleneck_var)

        """give every vertex a variable"""
        self.vertex_vars = {v: self.model.NewBoolVar(f'v_{v}') for v in range(self.n)}

    """find hamiltonian cycle"""

    def __add_hamiltonian_cycle_constraints(self):
        """
        Add the constraints that ensure that the solution is a hamiltonian cycle. Given is a undirected graph G = (V,E)
        """
        # every vertex must be once selected in the cycle
        for v in range(self.n):
            self.model.Add(self.vertex_vars[v] == 1)

        # in cycle there are only n edges
        self.model.Add(sum(self.edge_vars.values()) == self.n)

        # every vertex has exactly one incoming and one outgoing edge
        for v in range(0, self.n):
            # "Count" the number of incoming and outgoing edges.
            vin, vout = 0, 0
            for w in range(0, self.n):
                if v != w:
                    vin += self.edge_vars[w, v]
                    vout += self.edge_vars[v, w]
            self.model.Add(vin == 1)  # exactly one incoming edge
            self.model.Add(vout == 1)  # exactly one coming edge

    def __forbid_bidirectional_edges(self):
        """
        Add the (redundant) constraints x_{v,w} -> !x_{w, v}.
        """
        for v, w in itertools.combinations(range(self.n), 2):
            self.model.AddBoolOr([self.edge_vars[v, w].Not(), self.edge_vars[w, v].Not()])

    def __add_bottleneck_constraints(self):
        """
        Add the constraints to ensure that only edges as cheap or cheaper than
        the bottleneck can be selected (b >= d(v,w) * x_{v,w}).
        """
        for (v, w), x_vw in self.edge_vars.items():
            self.model.Add(self.bottleneck_var >= self.distances[v, w] * x_vw)

    def __add_depth_constraints(self):
        """
        Add the depth constraints x_{v,w} -> d_w = d_v + 1 which guarantee the
        validity of the arborescence.
        hier this constratins works to ensuer no subcrycles in the solution
        """

        # without loss of generality, force one node to be the root.
        self.model.Add(self.depth_vars[0] == 0)

        # If the edge v -> w is selected, d(v) + 1 == d(w) must hold.
        for (v, w), x_vw in self.edge_vars.items():
            """
            force the depth of w to be one greater than the depth of v if the edge v -> w is selected.
            but except the root node, so a cycle could be generated.
            """
            if w == 0:
                continue
            else:
                self.model.Add(self.depth_vars[w] == self.depth_vars[v] + 1).OnlyEnforceIf(x_vw)

    def __add_circle_constraints(self):
        edges = [(key[0], key[1], value) for key, value in self.edge_vars.items()]
        self.model.AddCircuit(edges)

    def __init__(self, points, using_circle_constraints):
        """
        Initialize the model.
        """
        self.points = points
        self.n = len(self.points)
        self.model = cp_model.CpModel()
        self.__calculate_distances()
        self.__make_vars()
        self.__forbid_bidirectional_edges()
        if not using_circle_constraints:
            self.__add_depth_constraints()
        else:
            self.__add_circle_constraints()
        self.__add_bottleneck_constraints()
        self.__add_hamiltonian_cycle_constraints()

    def solve(self):
        """
        Find the optimal solution to the initialized instance.
        Returns the BTSP edges as a list of coordinate tuple tuples ((x1,y1),(x2,y2)).
        """
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")
        return [(self.points[v], self.points[w]) for (v, w), x_vw in self.edge_vars.items() if solver.Value(x_vw) != 0]
