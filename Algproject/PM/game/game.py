# import the pygame module, so you can use it
import pygame
import thorpy as tp

from Algproject.PM.game.graph import Graph
from Algproject.PM.path_match.solver import GameSolver
from Algproject.PM.path_match.util import *

WIDTH = 1200
HEIGHT = 800


class Game:
    """
    this function is to adjust the click positions, because the graph is not in the left top corner of the window,
    but the game position is based on the left top corner of the window
    """
    def convert_to_game_coordinates(self, click_pos):
        game_x = click_pos[0] - (WIDTH - self.g.get_graph_size()[0])
        game_y = click_pos[1] - (HEIGHT - self.g.get_graph_size()[1])
        return game_x, game_y

    """
    create some game instances
    """
    def __gen_game_instance(self, instance_num):
        grid = gen_grid(self.g.get_graph_nodes()[0], self.g.get_graph_nodes()[1])
        start_points = gen_start_points(8, grid)
        instance = []
        while instance_num > 0:
            try:
                solver = GameSolver(grid, start_points[1])
                edges, paths = solver.solve()
                instance.append((start_points[1], edges, paths))
                instance_num -= 1
            except RuntimeError:
                #print("RuntimeError")
                start_points = gen_start_points(8, grid)
                continue
        return instance

    def __init__(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        pygame.display.set_caption("minimal program")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # Graph
        self.graph_surface = pygame.Surface((800, HEIGHT))
        self.graph_surface.fill((255, 255, 255))
        self.g = Graph(self.graph_surface, (10, 10))
        # UI
        self.ui_surface = pygame.Surface((400, HEIGHT))
        self.ui_surface.fill((100, 100, 100))
        tp.init(self.ui_surface, tp.theme_human)

        self.button = tp.Button("Test")
        self.button.center_on(self.ui_surface)
        self.updater = self.button.get_updater()

        self.clock = pygame.time.Clock()
        self.track_edge = []
        self.game_instance = self.__gen_game_instance(10)

    def run(self):
        running = True
        # main loop
        start_pos = None
        end_pos = None
        while running:
            self.clock.tick(60)
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                # hold left click to draw a line
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        start_pos = self.convert_to_game_coordinates(event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # left unclick
                        end_pos = self.convert_to_game_coordinates(event.pos)
                        if start_pos and end_pos:
                            print("start_pos: ", start_pos, "end_pos: ", end_pos)
                            self.track_edge.append((start_pos, end_pos))
                            self.g.add_edge(self.track_edge[len(self.track_edge) - 1][0],
                                            self.track_edge[len(self.track_edge) - 1][1])

            self.updater.update(events=events, mouse_rel=mouse_rel)

            # Drawing
            self.screen.blit(self.ui_surface, (0, 0))
            self.screen.blit(self.graph_surface, (400, 0))
            self.g.draw()
            pygame.display.flip()
            pygame.display.update()


# define a main function
"""
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Graph
    graph_surface = pygame.Surface((800, HEIGHT))
    graph_surface.fill((255, 255, 255))
    g = graph.Graph(graph_surface, (10, 10))
    # UI
    ui_surface = pygame.Surface((400, HEIGHT))
    ui_surface.fill((100, 100, 100))
    tp.init(ui_surface, tp.theme_human)
    button = tp.Button("Test")
    button.center_on(ui_surface)
    updater = button.get_updater()

    running = True
    clock = pygame.time.Clock()
    start_pos = None
    end_pos = None
    # main loop
    while running:
        clock.tick(60)
        events = pygame.event.get()
        mouse_rel = pygame.mouse.get_rel()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_pos = convert_to_game_coordinates(event.pos, g.get_graph_size())
                g.mouse_click(game_pos)
            
            # hold left click to draw a line

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    start_pos = convert_to_game_coordinates(event.pos, g.get_graph_size())
                    g.mouse_click(start_pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left unclick
                    end_pos = convert_to_game_coordinates(event.pos, g.get_graph_size())
                    g.mouse_click(end_pos)
                    if start_pos and end_pos:
                        g.add_edge(start_pos, end_pos)
                    start_pos = None
                    end_pos = None

        updater.update(events=events, mouse_rel=mouse_rel)

        # Drawing
        screen.blit(ui_surface, (0, 0))
        screen.blit(graph_surface, (400, 0))
        g.draw()
        pygame.display.flip()
        pygame.display.update()
"""

if __name__ == "__main__":
    game = Game()
    print(game.game_instance)
    game.run()
