from .util import all_edges_sorted, squared_distance
import math

class GreedyDBST:
    """
    Solve DBST using a greedy heuristic, similar to Kruskal's algorithm for MST.
    Sort all edges of the graph, iteratively pick the shortest viable edge
    (That does not create a cycle or violates the degree constraint of a node)
    and add it to the tree, until all nodes are connected (n-1 edges needed).
    The connected components are managed in a 'disjoint-set' or 'union-find'
    datastructure, which is used to efficiently check whether two vertices are
    partof the same component (adding an edge would create a cycle).
    """
    def __init__(self, points, degree):
        self.points = points
        self.all_edges = all_edges_sorted(points)
        self._component_of = {v: v for v in points}
        self.degree = degree
        
    def __component_root(self, v):
        cof = self._component_of[v]
        if cof != v:
            cof = self.__component_root(cof)
            self._component_of[v] = cof
        return cof
        
    def __merge_if_not_same_component(self, v, w):
        cv = self.__component_root(v)
        cw = self.__component_root(w)
        if cv != cw:
            self._component_of[cw] = cv
            return True
        return False
    
    def solve(self):
        edges = []
        degree = {v: 0 for v in self.points}
        n = len(self.points)
        m = 0
        for v,w in self.all_edges:
            if degree[v] < self.degree and degree[w] < self.degree:
                if self.__merge_if_not_same_component(v,w):
                    edges.append((v,w))
                    degree[v] += 1
                    degree[w] += 1
                    m += 1
                    if m == n-1:
                        self.max_sq_length = squared_distance(v,w)
                        print(f"Greedy bottleneck: {math.dist(v,w)}")
                        break
        return edges