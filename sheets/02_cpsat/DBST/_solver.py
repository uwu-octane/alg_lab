from ortools.sat.python import cp_model
import itertools

class DBSTSolverCP:
    def __squared_distance(self, vi, wi):
        """
        Gegeben zwei Punkt-Indizes, berechne die (ganzzahlige)
        quadrierte Distanz zwischen den Punkten.
        """
        v, w = self.points[vi], self.points[wi]
        return (v[0] - w[0])**2 + (v[1] - w[1])**2
    
    def __compute_distances(self):
        """
        Berechne eine Matrix der Distanzen.
        """
        self.distances = {(v,w): self.__squared_distance(v, w) for v,w in\
                          itertools.product(range(self.n), range(self.n))}
        self.max_distance = max(self.distances.values())
    
    def __make_vars(self):
        """
        Erzeuge die Variablen und setze die Zielfunktion.
        """
        self.edge_vars = {(v,w): self.model.NewBoolVar(f'x_{v},{w}') for v,w in itertools.combinations(range(self.n), 2)}
        self.edge_vars.update({(w,v): self.model.NewBoolVar(f'x_{w},{v}') for v,w in self.edge_vars})
        self.depth_vars = {v: self.model.NewIntVar(0, self.n-1, f'd_{v}') for v in range(self.n)}
        self.bottleneck_var = self.model.NewIntVar(0, self.max_distance, 'b')
        self.model.Minimize(self.bottleneck_var)
    
    def __add_degree_constraints(self):
        """
        Füge die Gradbedingungen hinzu.
        """
        v0out = 0
        for v in range(1, self.n):
            self.model.Add(self.edge_vars[v,0] == 0)  # x_vv0 = 0
            v0out += self.edge_vars[0,v]
        self.model.Add(v0out <= self.max_degree)  # Grad d für v0
        for v in range(1, self.n):
            vin, vout = 0, 0
            for w in range(0, self.n):
                if v != w:
                    vin += self.edge_vars[w,v]
                    vout += self.edge_vars[v,w]
            self.model.Add(vin == 1)  # genau 1 eingehende Kante für v
            self.model.Add(vout <= self.max_degree - 1)  # <= d-1 ausgehende Kanten für v
    
    def __forbid_bidirectional_edges(self):
        """
        Füge die (streng genommen redundanten) Constraints x_{v,w} -> !x_{w, v} hinzu.
        """
        for v,w in itertools.combinations(range(self.n), 2):
            self.model.AddBoolOr([self.edge_vars[v,w].Not(), self.edge_vars[w,v].Not()])
    
    def __add_depth_constraints(self):
        """
        Füge die Tiefenconstraints x_{v,w} -> d_w = d_v + 1 hinzu.
        """
        self.model.Add(self.depth_vars[0] == 0)
        all_edges = 0
        for (v, w), x_vw in self.edge_vars.items():
            self.model.Add(self.depth_vars[w] == self.depth_vars[v] + 1).OnlyEnforceIf(x_vw)
            all_edges += x_vw
        self.model.Add(all_edges == self.n-1)
        
    def __add_bottleneck_constraints(self):
        """
        Füge die Constraints b >= d(v,w) * x_{v,w} hinzu.
        """
        for (v, w), x_vw in self.edge_vars.items():
            self.model.Add(self.bottleneck_var >= self.distances[v,w] * x_vw)
    
    def __init__(self, points, max_degree):
        """
        Erzeuge das Modell.
        :param points: Liste der Punkte (ganzzahlig, in der Ebene, als (x,y)-Tupel).
        :param max_degree: Der höchste zulässige Grad in unserem Spannbaum.
        """
        self.points = points
        self.n = len(self.points)
        self.max_degree = max_degree
        self.model = cp_model.CpModel()
        self.__compute_distances()
        self.__make_vars()
        self.__forbid_bidirectional_edges()
        self.__add_degree_constraints()
        self.__add_depth_constraints()
        self.__add_bottleneck_constraints()
        
    def solve(self):
        """
        Suche die optimale Lösung für das konstruierte Modell und gebe eine Lösung
        (Liste von Kanten als ((x1,y1),(x2,y2))-Tupel) zurück.
        """
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        if status != cp_model.OPTIMAL:
            raise RuntimeError("Unexpected status after running solver!")
        return [(self.points[v], self.points[w]) for (v,w),x_vw in self.edge_vars.items() if solver.Value(x_vw) != 0]