import gurobipy as gp
from gurobipy import GRB

import networkx as nx
from typing import Any, List, Set, Tuple, Dict
import matplotlib.pyplot as plt

Node = Any
Edge = Tuple[Node, Node]

class MultiSourceSinkMaxFlow():
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.sources = set()
        self.sinks = set()
    
    def add_node(self, node: Node):
        self.graph.add_node(node)

    def add_source(self, node: Node):
        self.add_node(node)
        self.sources.add(node)
    
    def add_sink(self, node: Node):
        self.add_node(node)
        self.sinks.add(node)
    
    def add_edge(self, node1: Node, node2: Node, capacity: float):
        assert not self.graph.has_edge(node1, node2)
        self.graph.add_edge(node1, node2, capacity=capacity)
    
    def optimize(self):
        m = gp.Model()

        edge_utilization_vars = {
            (p, q): m.addVar(lb=0.0, ub=self.graph[p][q]["capacity"], vtype=GRB.CONTINUOUS) for (p, q) in self.graph.edges()
        }

        target_term = 0.0

        for v in self.graph.nodes():
            if v in self.sources:
                continue
            elif v in self.sinks:
                incoming_edges = self.graph.in_edges(v, data=False)
                incoming_flow = sum(edge_utilization_vars[e] for e in incoming_edges)
                target_term += incoming_flow
                continue
                
            incoming_edges = self.graph.in_edges(v, data=False)
            outgoing_edges = self.graph.out_edges(v, data=False)
            in_sum = sum(edge_utilization_vars[e] for e in incoming_edges)
            out_sum = sum(edge_utilization_vars[e] for e in outgoing_edges)

            m.addConstr(in_sum == out_sum)
        
        m.setObjective(target_term, GRB.MAXIMIZE)
        m.optimize()

        utilizations = {e: var.X for e, var in edge_utilization_vars.items()}
        return utilizations

    
    def draw(self, utilizations: Dict[Edge, float]):

        fig = plt.figure()
        fig.set_size_inches(12, 12)

        edge_labels = {
            e: f"{round(util, 2)} / {round(self.graph[e[0]][e[1]]['capacity'], 2)}" for e, util in utilizations.items()
        }
        layout = nx.layout.planar_layout(self.graph)

        nx.draw_networkx(
            self.graph, 
            labels={n: str(n) for n in self.graph.nodes()}, 
            pos=layout,
            node_color=["orange" if n in self.sinks else ("green" if n in self.sources else "grey") for n in self.graph.nodes()]
        )
        nx.draw_networkx_edge_labels(self.graph, pos=layout, edge_labels=edge_labels, font_size=10)
        plt.show()
