from ortools.sat.python import cp_model

import matplotlib.pyplot as plt
import networkx as nx
import itertools


def draw_edges(edges):
    """
    Draw the edges of a DBST. The bottleneck edge(s) automatically get highlighted.
    """
    points = set([e[0] for e in edges] + [e[1] for e in edges])
    draw_graph = nx.empty_graph()
    draw_graph.add_nodes_from(points)
    draw_graph.add_edges_from(edges)
    g_edges = draw_graph.edges()
    plt.clf()
    fig, ax = plt.gcf(), plt.gca()
    fig.set_size_inches(8,8)
    ax.set_aspect(1.0)  # 1:1 aspect ratio
    nx.draw_networkx(draw_graph, pos={p: p for p in points}, node_size=8,
                     with_labels=False, edgelist=g_edges, ax=ax)
    plt.show()


class GameSolver:

    def __make_vars(self):
        # graph.nodes
        self.node_vars = {n: tuple(self.model.NewBoolVar(f'{n}_{i}') for i in range(self.num_of_paths)) for n in
                          list(self.graph.nodes)}
        self.edge_vars = {e: tuple(self.model.NewBoolVar(f'{e}_{i}') for i in range(self.num_of_paths)) for e in
                          list(self.graph.edges)}
        self.depth_vars = {v: self.model.NewIntVar(0, len(self.graph.nodes) - 1, f'd_{v}') for v in range(self.num_nodes)}

        # Start points which have to be connected
        for i in range(self.num_of_paths):
            n1, n2 = start[i]
            self.model.Add(self.node_vars[n1][i] == 1)
            self.model.Add(self.node_vars[n2][i] == 1)

    def __single_selection_constraint(self):
        """ 
        Enforce that each node has be used once
        """
        for v in nx.nodes(self.graph):
            self.model.Add(sum(self.node_vars[v]) == 1)

        """
        Enforce that each edge can only be used once
        """
        for e in nx.edges(self.graph):
            self.model.Add(sum(self.edge_vars[e]) <= 1)

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

    def __forbid_bidirectional_edges(self):
        """
        Add the (redundant) constraints x_{v,w} -> !x_{w, v}.
        """
        for v, w in itertools.combinations(self.graph.edges, 2):
            # if the two edges are "reverse" from each other
            if v[0] == w[1] or v[1] == w[0]:
                for path in range(self.num_of_paths):
                    self.model.AddBoolOr([self.edge_vars[v][path].Not(), self.edge_vars[w][path].Not()])

    def __add_depth_constraints(self):
        """
        Add the depth constraints x_{v,w} -> d_w = d_v + 1 which guarantee the
        validity of the arborescence.
        """
        # without loss of generality, force one node to be the root.
        self.model.Add(self.depth_vars[0] == 0)
        # Todo:
        # spanning tree has exactly n-1 edges.
        self.model.Add(sum() == self.num_nodes - 1)
        # Todo:
        # If the edge v -> w is selected, d(v) + 1 == d(w) must hold.
        for (v, w), x_vw in self.edge_vars.items():
            self.model.Add(self.depth_vars[w] == self.depth_vars[v] + 1).OnlyEnforceIf(x_vw)

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start
        self.num_nodes = len(self.graph.nodes)
        self.num_of_paths = len(start)
        self.model = cp_model.CpModel()
        self.__make_vars()
        self.__single_selection_constraint()
        self.__connectivity_constraint()
        self.__degree_constraint()
        self.__forbid_bidirectional_edges()

    def solve(self):
        _solver = cp_model.CpSolver()
        status = _solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            raise RuntimeError("The model was classified infeasible by the solver!")
        if status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")

        for v, v_p in self.node_vars.items():
            print(f'Node {v}')
            for i, p in enumerate(v_p):
                print(f'Value for path_{i}: {_solver.Value(p)}')
        return [_solver.Value(*b) for n, b in self.node_vars.items()], [e for e in self.graph.edges if _solver.Value(self.edge_vars[e][0]) == 1]


G = nx.grid_2d_graph(2, 4).to_directed()
pos = {p: p for p in G.nodes}
nx.draw_networkx(G, pos=pos)
# plt.show()
# print(list(G.nodes))
start = [(list(G)[0], list(G)[4])]
# print(start)
solver = GameSolver(G, start)
nodes, edges = solver.solve()
print(edges)
draw_edges(edges)
