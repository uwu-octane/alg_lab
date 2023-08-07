# import the pygame module, so you can use it
import pygame
import thorpy as tp

from Algproject.PM.game.graph import Graph
from Algproject.PM.game.play import Play
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
                # print("RuntimeError")
                start_points = gen_start_points(8, grid)
                continue
        self.game_instance = instance

    def read_game_instance(self):
        data_list = read_json_lines("../instances.jsonl")
        self.game_instance_in_cache = handel_json_data(data_list)

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
        self.g = Graph(self.graph_surface, (5, 5))
        # UI
        self.ui_surface = pygame.Surface((400, HEIGHT))
        self.ui_surface.fill((100, 100, 100))
        tp.init(self.ui_surface, tp.theme_human)

        self.button = tp.Button("Test")
        self.button.center_on(self.ui_surface)
        self.updater = self.button.get_updater()
        self.events = None

        self.clock = pygame.time.Clock()
        self.running = False
        self.track_edge = []
        self.game_instance = []
        self.game_instance_in_cache = []

    def run(self):
        self.running = True
        # main loop
        start_pos = None
        end_pos = None
        while self.running:
            self.clock.tick(60)
            self.events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                # hold left click to draw a line
                self.__handel_left_holding_click(start_pos, end_pos, event)
                """
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # left click
                        start_pos = self.convert_to_game_coordinates(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # left unclick
                        end_pos = self.convert_to_game_coordinates(event.pos)
                        if start_pos and end_pos:
                            print("start_pos: ", start_pos, "end_pos: ", end_pos)
                            self.track_edge.append((start_pos, end_pos))
                            self.g.add_edge(self.track_edge[len(self.track_edge) - 1][0],
                                            self.track_edge[len(self.track_edge) - 1][1])
                """
            self.updater.update(events=self.events, mouse_rel=mouse_rel)

            # Drawing
            self.screen.blit(self.ui_surface, (0, 0))
            self.screen.blit(self.graph_surface, (400, 0))
            self.g.draw()
            pygame.display.flip()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
