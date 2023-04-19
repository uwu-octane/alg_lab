from util import Node, Edge
from typing import List
import networkx as nx
import gurobipy as gp
import random
from gurobipy import GRB

class SteinerTreeSolver():
    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph.to_directed()
    
    def assert_acyclic_callback(self, where, model, edgevars):
        if where != GRB.Callback.MIPSOL:
            # We are only interested in integral solutions!
            return
        # Get callback solution
        print("INTEGRAL")
        edges, variables = zip(*list(edgevars.items()))
        values = model.cbGetSolution(variables)

        edges = [e for e, val in zip(edges, values) if round(val) == 1]
        tree = self.graph.edge_subgraph(edges)

        for cycle in nx.cycles.simple_cycles(tree):
            cycle_edges = list(zip(cycle, cycle[1:])) + [(cycle[-1], cycle[0])]
            model.cbLazy(sum(edgevars[e] for e in cycle_edges) <= len(cycle_edges) - 1)
            print("Cycle was forbidden!")



    def solve(self, terminals: List[Node]):
        m = gp.Model()
        m.Params.lazyConstraints = 1

        edgevars = {e: m.addVar(vtype = GRB.BINARY) for e in self.graph.edges()}

        # edge can only be used in "one direction"
        for (p, q) in self.graph.edges():
            if p < q:
                m.addConstr(edgevars[(p, q)] + edgevars[(q, p)] <= 1)

        # without loss of generality: choose one of terminals as root node
        root_node = random.choice(terminals)
        print(f"Root node: {root_node}")

        # every terminal must be visited
        for v in terminals:
            incoming_edges = self.graph.in_edges(v)
            num_incoming = sum(edgevars[e] for e in incoming_edges)
            if v == root_node:
                m.addConstr(num_incoming == 0)
            else:
                m.addConstr(num_incoming >= 1)
        
        for v in self.graph.nodes():
            incoming_edges = list(self.graph.in_edges(v))
            num_incoming = sum(edgevars[e] for e in incoming_edges)
            outgoing_edges = list(self.graph.out_edges(v))
            num_outgoing = sum(edgevars[e] for e in outgoing_edges)

            if v == root_node:
                m.addConstr(num_outgoing >= 1)
            else:
                for e in outgoing_edges:
                    # The number of incoming edges must be >= 1 in order to have an outgoing edge.
                    m.addConstr(edgevars[e] <= num_incoming)
        
        total_cost = sum(edgevars[e] * self.graph[e[0]][e[1]]["weight"] for e in self.graph.edges())

        m.setObjective(total_cost, GRB.MINIMIZE)

        callback = lambda model, where: self.assert_acyclic_callback(where, model, edgevars)
        m.optimize(callback)

        # extract solution
        steiner_tree_edges = [e for e, var in edgevars.items() if round(var.X) == 1]

        return self.graph.edge_subgraph(steiner_tree_edges).copy()