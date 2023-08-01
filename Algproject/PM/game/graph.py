import pygame


class Graph:

    def __init__(self, surface, nodes):
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.surface = surface
        self.nodes = nodes
        self.__generate_graph()

    def __generate_graph(self):
        self.cell_width = self.width // self.nodes[0]
        self.cell_height = self.height // self.nodes[1]

        self.cells = [[pygame.Rect(i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height)
                       for j in range(self.nodes[1])] for i in range(self.nodes[0])]
        self.edges = []

    def draw(self):
        self.surface.lock()
        for i in range(self.nodes[0]):
            for j in range(self.nodes[1]):
                pygame.draw.rect(self.surface, (0, 0, 0), self.cells[i][j], 1)
                pygame.draw.circle(self.surface, (0, 0, 0), (i * self.cell_width + self.cell_width / 2,
                                                             j * self.cell_height + self.cell_height / 2), 5)
        for e in self.edges:
            start = self.get_cell_coordination(e[0])
            end = self.get_cell_coordination(e[1])
            pygame.draw.line(self.surface, (255, 0, 0), (self.get_cell_center(start[0], start[1])),
                              self.get_cell_center(end[0], end[1]), 2)
        self.surface.unlock()

    def add_edge(self, start, end):
        self.edges.append((start, end))

    def get_graph_size(self):
        return self.width, self.height

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

    def mouse_click(self, pos):
        for cell in self.cells:
            for rect in cell:
                if rect.collidepoint(pos):
                    print(self.get_cell_coordination((rect.x, rect.y)))

    def print_all_cell(self):
        for cell in self.cells:
            for rect in cell:
                print(rect.x, rect.y)
