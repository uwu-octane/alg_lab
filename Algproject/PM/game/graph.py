import pygame
from Algproject.PM.path_match.util import generate_random_rgb_from_hex, hex_to_rgb

class Circle:

    def __init__(self, color, pos, radius):
        self.color = color
        self.pos = pos
        self.radius = radius

class Graph:

    def __init__(self, width, height, nodes):
        self.graph_surface = pygame.Surface((width, height))
        self.graph_surface.fill((255, 255, 255))
        self.width = width
        self.height = height
        self.nodes = nodes
        self.__generate_graph()

    def __generate_graph(self):
        self.cell_width = self.width // self.nodes[0]
        self.cell_height = self.height // self.nodes[1]

        self.cells = [[pygame.Rect(i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height)
                       for j in range(self.nodes[1])] for i in range(self.nodes[0])]
        self.circles = [[ Circle((0, 0, 0), (i * self.cell_width + self.cell_width / 2,
                        j * self.cell_height + self.cell_height / 2), 5) for j in range(self.nodes[1])] 
                        for i in range(self.nodes[0])]
        self.lines = []
        self.start_points = []

    def draw(self, surface):
        self.graph_surface.lock()
        for i in range(self.nodes[0]):
            for j in range(self.nodes[1]):
                pygame.draw.rect(self.graph_surface, (0, 0, 0), self.cells[i][j], 1)
                pygame.draw.circle(self.graph_surface, self.circles[i][j].color, self.circles[i][j].pos, self.circles[i][j].radius)

        for l in self.lines:
            start = self.get_cell_coordination(l[0])
            end = self.get_cell_coordination(l[1])
            pygame.draw.line(self.graph_surface, (255, 0, 0), (start, end), 2)
        self.graph_surface.unlock()
        surface.blit(self.graph_surface, (400, 0))

    def add_line(self, start, end):
        self.lines.append((self.get_cell_center(start[0], start[1]),
                              self.get_cell_center(end[0], end[1])))

    def get_graph_size(self):
        return self.width, self.height

    def get_graph_nodes(self):
        return self.nodes

    def get_cell_center(self, i, j):
        center_x = i * self.cell_width + self.cell_width / 2
        center_y = j * self.cell_height + self.cell_height / 2
        return center_x, center_y

    def get_cell_coordination(self, pos):
        x, y = pos[0], pos[1]

        if pos[0] > 0:
            x = pos[0] // self.cell_width
        if pos[1] > 0:
            y = pos[1] // self.cell_height

        return x, y

    def add_start_point(self, start, end, color):
        self.start_points.append((start, end))
        self.circles[start[0]][start[1]].color = color
        self.circles[end[0]][end[1]].color = color

    def mouse_click(self, pos):
        for cell in self.cells:
            for rect in cell:
                if rect.collidepoint(pos):
                    print(self.get_cell_coordination((rect.x, rect.y)))

    def print_all_cell(self):
        for cell in self.cells:
            for rect in cell:
                print(rect.x, rect.y)

    # this function is for presenting a original revolution
    def draw_originalpath(self, game_instance_in_cache):
        # when only one resolution in instance.jsonl, just using the "game_instance_in_cache[1]"
        # temp_point = game_instance_in_cache[1].copy()
        temp_point = game_instance_in_cache[0][0].copy()
        for point in temp_point:
            for path in game_instance_in_cache[0][1]:
                color = generate_random_rgb_from_hex()
                (r, g, b) = hex_to_rgb(color)
                temp = path.copy()
                for edge in temp:
                    if point == edge[0] or point == edge[1]:
                        pygame.draw.line(self.graph_surface, (r, g, b), (self.get_cell_center(edge[0][0], edge[0][1])),
                                         self.get_cell_center(edge[1][0], edge[1][1]), 3)

                        temp_point.remove(point)
                        if edge[0] in temp_point:
                            temp_point.remove(edge[0])
                        if edge[1] in temp_point:
                            temp_point.remove(edge[0])
                        temp.remove(edge)

                    while len(temp) > 0:
                        pygame.draw.line(self.graph_surface, (r, g, b),
                                         (self.get_cell_center(temp[0][0][0], temp[0][0][1])),
                                         self.get_cell_center(temp[0][1][0], temp[0][1][1]), 3)
                        if temp[0][0] in temp_point:
                            temp_point.remove(temp[0][0])
                        if temp[0][1] in temp_point:
                            temp_point.remove(temp[0][1])
                        temp.pop(0)
