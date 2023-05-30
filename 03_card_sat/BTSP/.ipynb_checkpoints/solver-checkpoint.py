from pysat.solvers import Solver
import networkx as nx
import math

from util import Node, Edge, Iterable, List, Set, Optional, all_edges_sorted

class BTSPSolverSAT:
    def __make_edge_variables(self):
        """
        Create mappings from edges to corresponding variables and back.
        """

        # Map every undirected edge to an integer >= 1. This integer is both
        # used for encoding SAT clauses and for fetching the index/position
        # in the sorted edges (+1). The latter is important when handling the
        # bottleneck
        self.edge_to_var = {edge: i for i, edge in enumerate(self.all_edges, start=1)}

        # other way around
        self.var_to_edge = {v: e for e, v in self.edge_to_var.items()}

        # as edges are undirected, the swapped version of the edge should point to the same variable
        self.edge_to_var.update({(w,v): i for (v,w), i in self.edge_to_var.items()})
        
    def __add_degree_constraints(self):
        """
        Add constraints that assure 1 <= |N(v)| <= d for all v in V.
        """
        for v in self.graph.nodes:
            edge_vars = [self.edge_to_var[v,w] for w in self.graph.neighbors(v)]
            self.solver.add_clause(edge_vars)  # at least one edge must be selected
            self.solver.add_atmost(edge_vars, self.degree)  # at most d can be selected
    
    def __add_edge_count_constraint(self):
        """
        Add constraint that exactly n edges are selected.
        """
        positive_edges = [self.edge_to_var[e] for e in self.all_edges]
        negative_edges = [-v for v in positive_edges]
        n = len(self.points)
        self.solver.add_atmost(positive_edges, n)  # at most n edges
        self.solver.add_atmost(negative_edges, len(self.all_edges) - n)  # at most |E| - n non-edges
    
    def __init__(self, points: Iterable[Node], degree: int, solver: str = "Gluecard4", solution: List[Edge] = None):
        """
        Initialize the solver.
        :param points: The set of points as (x,y)-tuples.
        :param degree: The maximum degree of a node.
        :param solution: Optional parameter. Either 'None' or a valid starting solutin (as list of edges).
        """
        self.points = set(points)
        self.degree = degree
        self.all_edges = all_edges_sorted(points)
        self.graph = nx.Graph(self.all_edges)
        self.best_solution = solution
        self.solver = Solver(solver, with_proof=False, use_timer=True)
        self.__make_edge_variables()
        self.__add_degree_constraints()
        self.__add_edge_count_constraint()

    def __del__(self):
        """
        The solvers from python-sat need a special cleanup,
        which is not necessary for normal Python code.
        There seem to occur resource leaks when you leave this out,
        so it should be sufficient to let the solvers clean up at the garbage collection.
        """
        self.solver.delete()

    def __threshold_assumptions(self, threshold: int):
        """
        Create list of assumptions, which deactivate all edges longer than the
        edge at a given threshold index.
        """
        return [-self.edge_to_var[e] for e in self.all_edges[threshold+1:]]
    
    def __handle_components(self, components):
        """
        Add 'lazy constraints' for solutions which feature more than one connected component.
        This forces the solver to select at least one edge that leaves the component
        for every component in the graph.
        """
        for component in components:
            crossing_edges = []
            vset = set(component)
            for v in component:
                for w in self.points - vset:
                    crossing_edges.append(self.edge_to_var[v, w])
            self.solver.add_clause(crossing_edges)

    def __solve_with_threshold(self, threshold: int) -> Optional[int]:
        """
        Solves the decision problem:
        'Does there exist a spanning tree with degree constraint self.degree,
        such that no edge in the tree is longer than the edge at self.all_edges[threshold]'?

        This method returns 'None' if no valid solution is found.
        Otherwise, the highest utilized edge index is returned.
        """

        # Create so called 'assumptions', which force the solver to deactivate all
        # edges longer than the given threshold index edge.
        assumptions = self.__threshold_assumptions(threshold)
        while True:
            if not self.solver.solve(assumptions=assumptions):
                print(f"The bottleneck {math.dist(*self.all_edges[threshold])} is infeasible!")
                return None
            edges = self.__model_to_solution()
            #draw_edges(edges)
            #plt.show()
            edge_set = set(edges)
            g = self.graph.edge_subgraph(edges)
            components = list(nx.connected_components(g))
            if len(components) > 1:
                self.__handle_components(components)
            else:
                threshold = self.__max_index(edges)
                print(f"New best bottleneck: {math.dist(*self.all_edges[threshold])}!")
                self.best_solution = edges
                return threshold
    
    def __model_to_solution(self) -> List[Edge]:
        """
        Turn a valid SAT-assignment (solution) to a list of edges.
        """
        model = self.solver.get_model()
        return [self.var_to_edge[lit] for lit in model if lit > 0]
    
    def __index_of_solution_with_threshold(self, threshold: int) -> Optional[int]:
        """
        Return the index of the longest used edge in the solution.
        If the solution is invalid (graph unconnected), 'None' is returned.
        """
        g = self.graph.edge_subgraph(self.all_edges[:threshold + 1])
        if not nx.is_connected(g):
            print(f"The bottleneck {math.dist(*self.all_edges[threshold])} created an unconnected graph!")
            return None
        return self.__solve_with_threshold(threshold)

    def __max_index(self, solution: List[Edge]):
        """
        Return the index of the longest edge in a given solution.
        """
        return max((self.edge_to_var[e] - 1 for e in solution))
    
    def linear_search_ascending(self):
        """
        Linear search for the shortest bottleneck edge under degree constraint self.degree in ascending order
        """
        start = 0 # Starting edge index
        if self.best_solution is not None:
            start = self.__max_index(self.best_solution)
        for index, edge in enumerate(self.all_edges[start:]):
            self.__index_of_solution_with_threshold(index)
            
    def linear_search_descending(self):
        """
        Linear search for the shortest bottleneck edge under degree constraint self.degree in descending order
        """
        start = 0 # Starting edge index
        if self.best_solution is not None:
            start = self.__max_index(self.best_solution)
        for index, edge in enumerate(reversed(self.all_edges[start:])):
            self.__index_of_solution_with_threshold(index)

    def binary_search(self):
        """
        Binary search for the shortest bottleneck edge under degree constraint self.degree
        """
        lb = len(self.points) - 2  # The largest index that we know of to be essential
        ub = len(self.all_edges) - 1  # The smallest valid bottleneck we found
        if self.best_solution is not None:
            ub = self.__max_index(self.best_solution)
        while lb < ub - 1:
            mid = (lb + ub) // 2  # Integer division in Python: //
            actual_index = self.__index_of_solution_with_threshold(mid)
            if actual_index:
                ub = actual_index
            else:
                lb = mid
    
    def solve(self, method: int):
        if method == 0:
            self.binary_search()
        elif method == 1:
            self.linear_search_descending()
        elif method == 2:
            self.linear_search_ascending()
        else:
            print("method invalid")
            return None
        
        return self.best_solution, self.solver.time_accum()