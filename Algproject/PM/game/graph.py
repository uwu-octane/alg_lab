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

        self.cells = [[pygame.Rect(i*self.cell_width,j*self.cell_height,self.cell_width,self.cell_height) 
                        for j in range(self.nodes[1])] for i in range(self.nodes[0])]

    def draw(self):
        for i in range(self.nodes[0]):
            for j in range(self.nodes[1]):
                pygame.draw.rect(self.surface,(0,0,0),self.cells[i][j],1)
                pygame.draw.circle(self.surface,(0,0,0),(i*self.cell_width+self.cell_width/2,
                                                         j*self.cell_height+self.cell_height/2),5)
