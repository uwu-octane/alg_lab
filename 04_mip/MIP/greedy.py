from random import random, choice
from typing import Set, List

from .util import all_edges_sorted, Node, squared_distance, Edge
import math


class Greedy_Btsp:
    def __init__(self, points):
        self.points = points
        self.all_edges = all_edges_sorted(points)
        self._component_of = {v: v for v in points}
        self.degree = 2

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
        bottleneck = 0
        n = len(self.points)
        m = 0
        for v, w in self.all_edges:
            if degree[v] < self.degree and degree[w] < self.degree:
                if self.__merge_if_not_same_component(v, w):
                    edges.append((v, w))
                    degree[v] += 1
                    degree[w] += 1
                    m += 1
                    if m == n - 1:
                        bottleneck = math.dist(v, w)
                        print(f"Greedy bottleneck: {bottleneck}")
                        break
        for v, w in self.all_edges:
            if degree[v] < self.degree and degree[w] < self.degree:
                edges.append((v, w))
        return [1 if x in edges else 0 for x in self.all_edges], bottleneck

