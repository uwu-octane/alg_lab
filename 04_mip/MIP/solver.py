import gurobipy as grb
import itertools
import networkx as nx
from networkx.classes.graphviews import subgraph_view
import math


class DBSTSolverIP:
    def __make_vars(self):
        # Create binary variables for every *undirected* edge
        self.bnvars = {e: self.model_bottleneck.addVar(lb=0, ub=1, vtype=grb.GRB.BINARY) for e in self.all_edges}
        # Create a fractional variable (vtype=grb.GRB.CONTINUOUS) for the bottleneck length
        self.l = self.model_bottleneck.addVar(lb=0, ub=math.dist(*self.all_edges[-1]), vtype=grb.GRB.CONTINUOUS)

    def __add_degree_bounds(self, model, varmap: dict):
        """
        Enforce the degree constraint.
        This implementation accepts a dictionary for the edge variables,
        which is useful for use in multiple models.
        """
        for v in self.points:
            edgevars = 0
            for e in self.edges_of[v]:
                if e in varmap:
                    edgevars += varmap[e]
            model.addConstr(edgevars >= 1)
            model.addConstr(edgevars <= self.degree)

    def __add_total_edges(self, model, varmap: dict):
        """
        Enforce the constraint sum(x_e) = n-1
        """
        model.addConstr(sum(varmap.values()) == len(self.points) - 1)

    def __make_edges(self):
        edges_of = {p: list() for p in self.points}
        for e in self.all_edges:
            edges_of[e[0]].append(e)
            edges_of[e[1]].append(e)
        return edges_of

    def __add_bottleneck_constraints(self):
        """
        Enforce the bottleneck constraints.
        """
        for e, x_e in self.bnvars.items():
            self.model_bottleneck.addConstr(self.l >= math.dist(*e) * x_e)

    def __get_integral_solution(self, model, varmap: dict) -> nx.Graph:
        """
        Constructs a graph from the current solution of the given model.
        To be used inside of a callback.
        """
        variables = [x_e for e, x_e in varmap.items()]
        values = model.cbGetSolution(variables)
        graph = nx.empty_graph()
        graph.add_nodes_from(self.points)
        for i, (e, x_e) in enumerate(varmap.items()):
            # x_e has value v in the current solution
            v = values[i]
            if v >= 0.5:  # the values are not always 0 or 1 due to numerical errors
                graph.add_edge(e[0], e[1])
        return graph

    def __forbid_component(self, model, varmap: dict, component):
        """
        Forbid the occurence of multiple, disconnected components, by enforcing
        leaving edges for all occuring components.
        """
        crossing_edges = 0
        for v in component:
            for e in self.edges_of[v]:
                if e in varmap:
                    target = e[0] if e[0] != v else e[1]
                    if target not in component:
                        crossing_edges += varmap[e]
        # The constraint is added using "cbLazy" instaed of "addConstr" in a callback.
        model.cbLazy(crossing_edges >= 1)

    def __callback_integral(self, model, varmap):
        # Check whether the solution is connected
        graph = self.__get_integral_solution(model, varmap)
        components = list(nx.connected_components(graph))

        if len(components) == 1:
            # Graph is connected. Do nothing!
            return
        else:
            # Make components connected.
            for component in components:
                self.__forbid_component(model, varmap, component)

    def __callback_fractional(self, model, varmap):
        # Nothing has to be done in here.
        # Some more advanced techniques can be used to add helpful constraints
        # just from looking at a fractional solution, but this exceeds the scope
        # of this course. It can still be interesting to analyze fractional solutions
        # that the solver comes up with.
        pass

    def callback(self, where, model, varmap):
        if where == grb.GRB.Callback.MIPSOL:
            # we have an integral solution (potentially valid solution)
            self.__callback_integral(model, varmap)
        elif where == grb.GRB.Callback.MIPNODE and \
                model.cbGet(grb.GRB.Callback.MIPNODE_STATUS) == grb.GRB.OPTIMAL:
            # we have a fractional solution
            # (intermediate solution with fractional values for all booleans)
            self.__callback_fractional(model, varmap)

    def __init__(self, points, edges, degree):
        self.points = points
        self.all_edges = edges
        self.degree = degree
        self.edges_of = self.__make_edges()
        self.model_bottleneck = grb.Model()  # "First stage" model for finding the bottleneck edge
        self.model_minsum = grb.Model()  # "Second stage" model for finding the cost-minimal DBST with fixed bottleneck.
        self.remaining_edges = None
        self.msvars = None
        self.__make_vars()
        self.__add_degree_bounds(self.model_bottleneck, self.bnvars)
        self.__add_total_edges(self.model_bottleneck, self.bnvars)
        self.__add_bottleneck_constraints()
        # Give the solver a heads up that lazy constraints will be utilized
        self.model_bottleneck.Params.lazyConstraints = 1
        # Set the first objective
        self.model_bottleneck.setObjective(self.l, grb.GRB.MINIMIZE)

    def __init_minsum_model(self):
        """
        Set up variables, constraints and objective function for the
        second stage model.
        """
        # Create binary variables (vtype=grb.GRB.BINARY) for all edges
        self.msvars = {e: self.model_minsum.addVar(lb=0, ub=1, vtype=grb.GRB.BINARY)
                       for e in self.remaining_edges}
        self.__add_degree_bounds(self.model_minsum, self.msvars)
        self.__add_total_edges(self.model_minsum, self.msvars)
        self.model_minsum.Params.lazyConstraints = 1
        obj = sum((math.dist(*e) * x_e for e, x_e in self.msvars.items()))
        self.model_minsum.setObjective(obj, grb.GRB.MINIMIZE)

    def __solve_bottleneck(self):
        # Find the optimal bottleneck (first stage)
        cb_bn = lambda model, where: self.callback(where, model, self.bnvars)
        self.model_bottleneck.optimize(cb_bn)
        if self.model_bottleneck.status != grb.GRB.OPTIMAL:
            raise RuntimeError("Unexpected status after optimization!")
        bottleneck = self.model_bottleneck.objVal
        print(f"[DBST SOLVER]: Found the optimal bottleneck! Bottleneck length is {bottleneck}")
        self.remaining_edges = [e for e in self.all_edges if math.dist(*e) <= bottleneck]
        return [e for e, x_e in self.bnvars.items() if x_e.x >= 0.5]

    def __solve_minsum(self):
        # Find the optimal tree (second stage)
        self.__init_minsum_model()
        cb_ms = lambda model, where: self.callback(where, model, self.msvars)
        self.model_minsum.optimize(cb_ms)
        if self.model_bottleneck.status != grb.GRB.OPTIMAL:
            raise RuntimeError("Unexpected status after optimization!")
        # Return all edges with value >= 0.5 (numerical reasons)
        print(f"[DBST SOLVER]: Found the optimal tree! Total cost: {self.model_minsum.objVal}")
        return [e for e, x_e in self.msvars.items() if x_e.x >= 0.5]

    def solve(self, minsum: bool = False):
        dbst_edges = self.__solve_bottleneck()
        if not minsum:
            return dbst_edges
        else:
            return self.__solve_minsum()
