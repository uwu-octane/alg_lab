import traceback

from ortools.sat.python import cp_model
import itertools

import networkx as nx
import random
import matplotlib
import matplotlib.pyplot as plt
import signal


def squared_distance(p1, p2):
    """
    Calculate the squared euclidian distance (in order to minimze the use of the sqrt() operation).
    """
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


class BTSPSolverCP:
    def __calculate_distances(self) -> int:
        """
        Precalculate the costs of all edges. The side effect of this method
        is the calculated max_distance, which is necessary in order to specify
        our bottleneck variable's upper bound.
        """
        self.distances = {(i, j): squared_distance(self.points[i], self.points[j])
                          for (i, j) in itertools.permutations(range(len(self.points)), 2)}
        self.max_distance = max(self.distances.values())

    def __make_vars(self):
        """
        Create all involved variables and set the minimization objective.
        """
        self.edge_vars = {(v, w): self.model.NewBoolVar(f'x_{v},{w}')
                          for v, w in itertools.permutations(range(self.n), 2)}
        self.bottleneck_var = self.model.NewIntVar(0, self.max_distance, 'b')
        self.model.Minimize(self.bottleneck_var)

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

    def __add_degree_constraints(self):
        """
        Add an upper limit to the degree of every node.
        """
        # Handle all other nodes.
        for v in range(1, self.n):
            # "Count" the number of incoming and outgoing edges.
            vin, vout = 0, 0
            for w in range(0, self.n):
                if v != w:
                    vin += self.edge_vars[w, v]
                    vout += self.edge_vars[v, w]
            self.model.Add(vin == 1)  # exactly one incoming edge
            self.model.Add(vout == 1)  # exactly one outgoing edge

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

    def __init__(self, points):
        """
        Initialize the model.
        """
        self.points = points
        self.n = len(self.points)
        self.model = cp_model.CpModel()
        self.__calculate_distances()
        self.__make_vars()
        self.__add_bottleneck_constraints()
        arcs = list()
        for (v, w), x_vw in self.edge_vars.items():
            arc = (v, w, x_vw)
            arcs.append(arc)

        self.model.AddCircuit(arcs)

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
        return [(self.points[v], self.points[w]) for (v, w), x_vw in self.edge_vars.items() if solver.Value(x_vw) != 0]


def random_points(n, w=10_000, h=10_000):
    """
    Generate a list of n randomly placed points on the w x h grid.
    """
    return [(random.randint(0, w), random.randint(0, h)) for _ in range(n)]


def draw_btsp_edges(edges):
    """
    Draw the edges of a DBST. The bottleneck edge(s) automatically get highlighted.
    """
    points = set([e[0] for e in edges] + [e[1] for e in edges])
    draw_graph = nx.empty_graph()
    draw_graph.add_nodes_from(points)
    draw_graph.add_edges_from(edges)
    g_edges = draw_graph.edges()
    max_length = max((squared_distance(*e) for e in g_edges))
    color = [('red' if squared_distance(*e) == max_length else 'black') for e in g_edges]
    width = [(1.0 if squared_distance(*e) == max_length else 0.5) for e in g_edges]
    plt.clf()
    fig, ax = plt.gcf(), plt.gca()
    fig.set_size_inches(8, 8)
    ax.set_aspect(1.0)  # 1:1 aspect ratio
    nx.draw_networkx(draw_graph, pos={p: p for p in points}, node_size=8,
                     with_labels=False, edgelist=g_edges, edge_color=color, width=width, ax=ax)
    plt.show()


if __name__ == '__main__':
    import time
    random.seed(1234567)  # remove if you want random instances
    signal.signal(signal.SIGALRM, lambda signum,
                                         frame: print('\nYour time got over'))

    signal.alarm(60)
    start = time.time()
    try:
        for i in range(100):
            num_of_points = random.randint(10, 100)
            print(f'Iteration: {i}, points: {num_of_points}')
            BTSPSolverCP(random_points(num_of_points))
    except Exception as e:
        print(e)
    signal.alarm(0)
    print(f'TIme taken: {round(time.time() - start, 4)}')
