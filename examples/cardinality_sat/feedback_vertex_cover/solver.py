from pysat.solvers import Solver as SATSolver
from typing import List, Set, Tuple, Iterable, Dict, Any, Optional
import networkx as nx
import itertools
import math

from util import find_cycle, Node, Edge
from greedy import greedy_fvs


class FeedbackVertexSetSolverSAT():
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph
        # a cycle basis can be calculated in polynomial time and contains cycles that can be "combined" to construct
        # any possible cycle in the graph. This list does not contain all cycles, but represents most of them, with high chance.
        # New cycles that have not been found before are added lazily later on.
        self.cycles = nx.cycle_basis(self.graph)
        print(f"Number of cycles in cycle basis: {len(self.cycles)}")
        # dictionary for the variables in the SAT formula 
        self.node_variables: Dict[Node, int] = dict()
    
    def get_node_var(self, v: Node):
        """
        This method associates each vertex in the graph with an integer between 1 and |V|.
        These numbers represent the boolean variables in the clauses of the SAT problem.
        Using this method also potentially reduces the size of the resulting SAT problem, as only variables for vertices
        appearing in any cycle are generated. We may call this "lazy variable generation"
        """
        if not v in self.node_variables:
            self.node_variables[v] = len(self.node_variables) + 1
        return self.node_variables[v]
    
    def decide(self, k: int):
        """
        Decide, whether a feedback vertex set of (at most) k vertices exists.
        If one exists, it is returned as a set of vertices. Otherwise, 'None' is returned.

        This is done by modeling and solving an equivalent Cardinality-SAT instance.

        The constraints are as follows:
            - For every cycle, force at least one of the vertices to be "selected".
                - Note: Finding all (even simple) cycles in an undirected graph requires exponential time (otherwise, solving Hamiltonian Cycle and TSP would be easy), so we lazily introduce this constraint whenever a cycle remains after solving the problem.
            - Using a cardinality constraint, we allow at most k vertices to be "selected".
        """

        # Initialize our Cardinality-SAT solver
        solver = SATSolver("MiniCard")

        def constrain_cycle(cycle: List[Node]):
            """
            Force the inclusion of at least one vertex in the cycle into the FVS.
            """
            # fetch the variables associated with the vertices in the cycle
            cycle_vertex_vars = [self.get_node_var(v) for v in cycle]
            # force at least one of them to be selected
            solver.add_clause(cycle_vertex_vars)
        
        def limit_positive_variables():
            """
            Limit number of "selected" vertices to at most k.
            """
            all_node_vars = list(self.node_variables.values())
            solver.add_atmost(all_node_vars, k)
        
        # Initial constraints
        for cycle in self.cycles:
            constrain_cycle(cycle)
        limit_positive_variables()
        
        # as long as the SAT solver returns "satisfiable"
        while solver.solve():
            # retrieve the solution from the solver. This solution contains a positive number for every positively assigned variable and a negative number for every negatively assigned one
            solution = set(solver.get_model())
            feedback_nodes = set(p for (p, var) in self.node_variables.items() if var in solution)
            subgraph = self.graph.copy()
            subgraph.remove_nodes_from(feedback_nodes)
            cycle = find_cycle(subgraph)
            if cycle:
                # Lazily add constraint to "forbid" the found cycle, solve again.
                # This is not as inefficient as you might think; The solver is able to (more or less) continue from where it stopped. In addition, fewer constraints usually result in much easier models and are solved way faster than "complete" models, in our case with an exponential number of constraints (for each existing cycle).
                self.cycles.append(cycle)
                num_vars_before_new_constraint = len(self.node_variables)
                constrain_cycle(cycle)
                if len(self.node_variables) != num_vars_before_new_constraint:
                    limit_positive_variables()
                continue
            else:
                # The remaining graph contains no cycles. A valid solution was found!
                print(f"k = {k}: SAT")
                return feedback_nodes
        else:
            # The SAT-solver proved the formula to be infeasible. This proves that there exists no FVS of size k.
            print(f"k = {k}: UNSAT")
            return None
    
    def find_optimum(self):
        """
        Finds the smallest FVS on the given graph.
        """

        # calculate a greedy FVS in order to obtain an upper bound to the minimum FVS
        best_solution = greedy_fvs(self.graph)
        k = len(best_solution)
        print(f"A greedy solution of size {k} was found!")

        ub = k # the lowest number of vertices that are proven to build a FVS
        lb = 0 # the lowest number of vertices that might still build a FVS (not proven wrong)

        while lb < ub:
            k = (lb + ub) // 2 # integer division (discards floating point decimals)
            k_limited_fvs = self.decide(k)

            if k_limited_fvs is not None:
                # A valid, better solution was found!
                best_solution = k_limited_fvs
                ub = len(k_limited_fvs)
                print(f"A solution of size {k} was found by the solver!")
            else:
                # k-FVS was proven impossible by the solver
                lb = k + 1
            
        print(f"The solution of size {len(best_solution)} was proven to be optimal!")
        return best_solution
