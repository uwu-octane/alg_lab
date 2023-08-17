import pygame
from Algproject.PM.path_match.util import *


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
            for point in self.start_points:
                point_coor = self.get_real_cell_coordination(point[0], point[1])
                pygame.draw.circle(self.graph_surface, 'skyblue', point_coor, 5)
        """
        for cell_coor in self.cells_coor:
            cell_coordination = self.get_real_cell_coordination(cell_coor[0], cell_coor[1])
            pygame.draw.circle(self.graph_surface, (0, 0, 0), cell_coordination, 5)
        """
        for edge, is_shown in self.edges_shadow.items():
            start = self.get_real_cell_coordination(edge[0][0], edge[0][1])
            end = self.get_real_cell_coordination(edge[1][0], edge[1][1])
            if is_shown:
                pygame.draw.line(self.graph_surface, (255, 0, 0), start, end, 2)
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
        # edges = [(self.get_cell_center(edge[0][0],edge[0][1]), self.get_cell_center(edge[1][0], edge[1][1])) for edge in edges]
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
        temp_point = game_instance[0][0].copy()
        for point in temp_point:
            for path in game_instance[0][1]:
                color = generate_random_rgb_from_hex()
                (r, g, b) = hex_to_rgb(color)
                temp = path.copy()
                for edge in temp:
                    if point == edge[0] or point == edge[1]:
                        pygame.draw.line(self.graph_surface, (r, g, b),
                                         (self.get_real_cell_coordination(edge[0][0], edge[0][1])),
                                         self.get_real_cell_coordination(edge[1][0], edge[1][1]), 3)

                        temp_point.remove(point)
                        if edge[0] in temp_point:
                            temp_point.remove(edge[0])
                        if edge[1] in temp_point:
                            temp_point.remove(edge[0])
                        temp.remove(edge)

                    while len(temp) > 0:
                        pygame.draw.line(self.graph_surface, (r, g, b),
                                         (self.get_real_cell_coordination(temp[0][0][0], temp[0][0][1])),
                                         self.get_real_cell_coordination(temp[0][1][0], temp[0][1][1]), 3)
                        if temp[0][0] in temp_point:
                            temp_point.remove(temp[0][0])
                        if temp[0][1] in temp_point:
                            temp_point.remove(temp[0][1])
                        temp.pop(0)