from util import Node, Edge
from typing import List
import networkx as nx
import gurobipy as gp
import random
from gurobipy import GRB

class SteinerTreeSolver():

    def __init__(self, graph: nx.Graph) -> None:
        # For an elegant modelation, convert the graph to a directed graph
        self.graph = graph.to_directed()
    
    def assert_acyclic_callback(self, where, model, edgevars):
        """
        This is a callback method, used to lazily add constraints to the model
        during the solving process. This is natively supported by the solver
        GUROBI.

        In the case of this problem, it is possible that the solver generates
        a solution with directed edge cycles. A tree must not contain cycles,
        so whenever a cycle is generated, we add a constraint. This constraint
        simply forces the solver to deselect at least one of the edges in the
        cycle.
        """

        if where != GRB.Callback.MIPSOL:
            # This way, we can check at which state of the solving process the
            # callback was called. For example, it is possible that only a fractional
            # solution is available.
            # We are only interested in integral solutions!
            return

        # Split the key-value items into two lists of edges and variables
        edges, variables = zip(*list(edgevars.items()))
        # Get the current values associated with the variables (list with matching index)
        values = model.cbGetSolution(variables)

        # Zip the edges and the values of their variables back together, construct tree
        # from edges which are "selected" as indicated by their variable having value 1.
        edges = [e for e, val in zip(edges, values) if round(val) == 1]
        tree = self.graph.edge_subgraph(edges)

        # Forbid every (directed) cycle in the solution
        for cycle in nx.cycles.simple_cycles(tree):
            cycle_edges = list(zip(cycle, cycle[1:])) + [(cycle[-1], cycle[0])]
            # This method is used to lazily add a constraint from a callback.
            model.cbLazy(sum(edgevars[e] for e in cycle_edges) <= len(cycle_edges) - 1)
            print("A cycle was forbidden!")


    def solve(self, terminals: List[Node]) -> nx.DiGraph():
        """
        This method finds the cost-minimal Steiner Tree with respect to the given terminals.
        It is returned as a tree graph.
        """

        # Allocate a Gurobi model, enable lazy constraints.
        m = gp.Model()
        m.Params.lazyConstraints = 1

        # Allocate a boolean variable for every directed edge.
        edgevars = {e: m.addVar(vtype = GRB.BINARY) for e in self.graph.edges()}

        # Enforce that every edge can only be used in one direction.
        for (p, q) in self.graph.edges():
            # p < q ensures that this constraint is only added once per pair of connected nodes
            if hash(p) < hash(q):
                m.addConstr(edgevars[(p, q)] + edgevars[(q, p)] <= 1)

        # without loss of generality: choose one of terminals as root node
        root_node = random.choice(terminals)
        print(f"Root node: {root_node}")

        # Enforce that every terminal must be visited, meaning there is one incoming edge (except for root).
        for v in terminals:
            incoming_edges = self.graph.in_edges(v)
            num_incoming = sum(edgevars[e] for e in incoming_edges)
            if v == root_node:
                m.addConstr(num_incoming == 0)
            else:
                m.addConstr(num_incoming == 1)
        
        # Enforce that outgoing edges are only possible when the node is visited (incoming edges are selected)
        for v in self.graph.nodes():
            incoming_edges = list(self.graph.in_edges(v))
            num_incoming = sum(edgevars[e] for e in incoming_edges)
            outgoing_edges = list(self.graph.out_edges(v))
            num_outgoing = sum(edgevars[e] for e in outgoing_edges)

            if v == root_node:
                m.addConstr(num_outgoing >= 1)
            else:
                for e in outgoing_edges:
                    # The number of incoming edges must be >= 1 (= 1) in order to allow an outgoing edge.
                    m.addConstr(edgevars[e] <= num_incoming)
        
        # Build the linear expression that describes the total cost of the Steiner Tree's edges.
        total_cost = sum(edgevars[e] * self.graph[e[0]][e[1]]["weight"] for e in self.graph.edges())
        
        # Set the minimization objective.
        m.setObjective(total_cost, GRB.MINIMIZE)

        # Prepare the callback, optimize the model with enabled callback.
        callback = lambda model, where: self.assert_acyclic_callback(where, model, edgevars)
        m.optimize(callback)

        # Extract and return the solution.
        steiner_tree_edges = [e for e, var in edgevars.items() if round(var.X) == 1]
        return self.graph.edge_subgraph(steiner_tree_edges).copy()