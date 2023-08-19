import pygame
from Algproject.PM.path_match.util import *
from Algproject.PM.game.constants import color_list


class Circle:

    def __init__(self, color, pos, radius):
        self.color = color
        self.pos = pos
        self.radius = radius


class Graph:

    def __init__(self, width, height, nodes):
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
        self.lines = []
        self.edges = []
        self.cells_coor = [(i, j) for j in range(self.nodes[1]) for i in range(self.nodes[0])]
        self.start_points = []
        self.solution_instance = []

    def draw(self, surface):
        self.graph_surface.lock()
        """
        for i in range(self.nodes[0]):
            for j in range(self.nodes[1]):
                pygame.draw.rect(self.graph_surface, (0, 0, 0), self.cells[i][j], 1)

                pygame.draw.circle(self.graph_surface, self.circles[i][j].color, self.circles[i][j].pos,
                                   self.circles[i][j].radius)
        """
        for cell in self.cells:
            for rect in cell:
                pygame.draw.rect(self.graph_surface, (0, 0, 0), rect, 1)

        for circle in self.circles:
            for c in circle:
                if c not in self.start_points:
                    pygame.draw.circle(self.graph_surface, c.color, c.pos, c.radius)

        if self.start_points:
            i = 1
            j = 0
            for point in self.start_points:
                if j < 15:
                    color = color_list[j]
                else:
                    color = color_list[14]
                if i % 2 == 0:
                    j += 1
                i += 1
                point_coor = self.get_real_cell_coordination(point[0], point[1])
                pygame.draw.circle(self.graph_surface, color, point_coor, 10)

        """
        for cell_coor in self.cells_coor:
            cell_coordination = self.get_real_cell_coordination(cell_coor[0], cell_coor[1])
            pygame.draw.circle(self.graph_surface, (0, 0, 0), cell_coordination, 5)
        """
        if not self.solution_sign:
            for edge, is_shown in self.edges_shadow.items():
                start = self.get_real_cell_coordination(edge[0][0], edge[0][1])
                end = self.get_real_cell_coordination(edge[1][0], edge[1][1])
                if is_shown:
                    pygame.draw.line(self.graph_surface, (255, 0, 0), start, end, 2)
        else:
            i = 0
            for path in self.solution_instance[0][1]:
                if i < 15:
                    color_for_path = color_list[i]
                    i += 1
                else:
                    color_for_path = color_list[14]
                for edge, is_shown in self.edges_shadow.items():
                    if self.is_edge_in_path(edge, path):
                        self.edges_shadow[edge] = True
                        start = self.get_real_cell_coordination(edge[0][0], edge[0][1])
                        end = self.get_real_cell_coordination(edge[1][0], edge[1][1])
                        pygame.draw.line(self.graph_surface, color_for_path, start, end, 4)
        self.graph_surface.unlock()
        surface.blit(self.graph_surface, (400, 0))

    def add_line(self, start, end):
        """
        self.lines.append((self.get_cell_center(start[0], start[1]),
                           self.get_cell_center(end[0], end[1])))
        """

        self.lines.append((start, end))

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

    def get_real_cell_coordination(self, i, j):
        center_x = i * self.cell_width + self.cell_width / 2
        center_y = j * self.cell_height + self.cell_height / 2
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
    def draw_originalpath(self, game_instance):
        # when only one solution in instance.jsonl, just using the "game_instance_in_cache[1]"
        # temp_point = game_instance_in_cache[1].copy()
        self.solution_sign = True
        self.solution_instance = game_instance

    def reset_solution_sign(self):
        self.solution_sign = False

    def is_edge_in_path(self, edge, path):
        sub_segments = [(edge[i], edge[i + 1]) for i in range(len(edge) - 1)]

        for sub_segment in sub_segments:
            found = False
            for segment in path:
                if (sub_segment[0] == segment[0] and sub_segment[1] == segment[1]) or \
                        (sub_segment[0] == segment[1] and sub_segment[1] == segment[0]):
                    found = True
                    break
            if not found:
                return False
        return True

    def are_adjacent(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2

        # 判断两个点是否在横向或纵向上相邻
        if abs(x1 - x2) + abs(y1 - y2) == 1:
            return True
        else:
            return False

    def change_move_edge_in_shadow(self, point_list):
        for i in range(len(point_list) - 1):
            if self.are_adjacent(point_list[i], point_list[i + 1]):
                edge = (point_list[i], point_list[i + 1])
                self.edges_shadow[edge] = True

    def change_move_edge_not_in_shadow(self, point_list):
        for i in range(len(point_list) - 1):
            if self.are_adjacent(point_list[i], point_list[i + 1]):
                edge1 = (point_list[i], point_list[i + 1])
                edge2 = (point_list[i + 1], point_list[i])
                self.edges_shadow[edge1] = False
                self.edges_shadow[edge2] = False
