import pygame

from Algproject.PM.game.constants import color_list
from Algproject.PM.path_match.util import *
from Algproject.PM.game.tools import *


class Circle:

    def __init__(self, color, pos, radius):
        self.color = color
        self.pos = pos
        self.radius = radius


class Graph:

    def __init__(self, width, height, nodes):
        # graph_surface
        self.graph_surface = pygame.Surface((width, height)).convert_alpha()
        self.graph_surface.fill((255, 255, 255))
        self.width = width
        self.height = height
        self.nodes = nodes

        """
        we shadow every edge in this map, if the edge is shown, the value is 1, otherwise 0
        as a final result we send the positive edges to a solver for validation 
        """
        self.edges_shadow = {}
        self.solution_sign = False  # to decide present solution from user or Solver
        self.__generate_graph()
        self.__shadow_edges()

    def __generate_graph(self):
        self.cell_width = self.width // self.nodes[0]
        self.cell_height = self.height // self.nodes[1]

        self.cells = [[pygame.Rect(i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height)
                       for j in range(self.nodes[1])] for i in range(self.nodes[0])]
        self.circles = [[Circle((0, 0, 0), (i * self.cell_width + self.cell_width / 2,
                                            j * self.cell_height + self.cell_height / 2), 5) for j in
                         range(self.nodes[1])]
                        for i in range(self.nodes[0])]
        self.cells_coor = [(i, j) for j in range(self.nodes[1]) for i in range(self.nodes[0])]

    def draw(self, surface, solver=None):
        self.graph_surface.lock()

        for cell in self.cells:
            for rect in cell:
                pygame.draw.rect(self.graph_surface, (0, 0, 0, 0), rect, 1)

        for cell_coor in self.cells_coor:
            if solver:
                if cell_coor not in solver.get_start_points():
                    cell_coor = self.get_real_cell_coordination(cell_coor)
                    pygame.draw.circle(self.graph_surface, (0, 0, 0), cell_coor, 5)
            else:
                cell_coor = self.get_real_cell_coordination(cell_coor)
                pygame.draw.circle(self.graph_surface, (0, 0, 0), cell_coor, 5)

        if solver:
            for point in solver.get_start_points():
                point_coor = self.get_real_cell_coordination(point)
                point_path_num = solver.get_path_var(point)
                pygame.draw.circle(self.graph_surface, color_list[point_path_num], point_coor, 10)
            if self.solution_sign:
                for path in solver.get_result():
                    for edge in path:
                        self.edges_shadow[edge] = True
                        start = self.get_real_cell_coordination(edge[0])
                        end = self.get_real_cell_coordination(edge[1])
                        edge_path_num = solver.get_path_var(edge[0])
                        pygame.draw.line(self.graph_surface, color_list[edge_path_num], start, end, 4)

        if not self.solution_sign:
            for edge, is_shown in self.edges_shadow.items():
                start = self.get_real_cell_coordination(edge[0])
                end = self.get_real_cell_coordination(edge[1])
                if is_shown:
                    pygame.draw.line(self.graph_surface, (255, 0, 0), start, end, 2)

        self.graph_surface.unlock()
        surface.blit(self.graph_surface, (400, 0))

    def remove_line(self, surface):
        self.graph_surface.fill((255, 255, 255))
        self.draw(surface)

    def get_graph_size(self):
        return self.width, self.height

    def __shadow_edges(self):
        g = gen_grid(self.nodes[0], self.nodes[1])
        edges = list(g.edges())
        bi_edges = [(edge[1], edge[0]) for edge in edges]
        edges = edges + bi_edges
        self.edges_shadow = {edge: False for edge in edges}

    def get_graph_nodes(self):
        return self.nodes

    """this function receives a simple coordination in format (0,1) and return the real coordination which is 
    adjusted with the surface size
    """

    def get_real_cell_coordination(self, coor):
        center_x = coor[0] * self.cell_width + self.cell_width / 2
        center_y = coor[1] * self.cell_height + self.cell_height / 2
        return center_x, center_y

    """
    this function receives a real coordination and return the simple coordination in format (0,1)
    used to work with the event position
    """

    def get_simple_cell_coordination(self, pos):
        x, y = pos[0], pos[1]

        if pos[0] > 0:
            x = pos[0] // self.cell_width
        if pos[1] > 0:
            y = pos[1] // self.cell_height

        return x, y

    # this function is for presenting a original revolution
    def set_solution_sign(self):
        self.solution_sign = True

    def reset_solution_sign(self):
        self.solution_sign = False

    def __are_adjacent(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        # check if the two points are adjacent
        if abs(x1 - x2) + abs(y1 - y2) == 1:
            return True
        else:
            return False

    def connect_edges(self, point_list):
        edges = self.__points_to_edges(point_list)
        for edge in edges:
            self.edges_shadow[edge] = True

    def cancel_edges(self, point_list):
        edges = self.__points_to_edges(point_list)
        for edge in edges:
            self.edges_shadow[edge] = False
            self.edges_shadow[(edge[1], edge[0])] = False

    def set_solver(self, solver):
        self.solver = solver

    def __points_to_edges(self, points):
        edges = []
        for i in range(len(points) - 1):
            if self.__are_adjacent(points[i], points[i + 1]):
                edge = (points[i], points[i + 1])
                edges.append(edge)
        return edges
