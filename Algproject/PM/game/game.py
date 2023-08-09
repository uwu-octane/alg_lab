# import the pygame module, so you can use it
import pygame

from Algproject.PM.game.graph import Graph
from Algproject.PM.game.ui import Ui
import Algproject.PM.game.constants as c

from Algproject.PM.path_match.solver import GameSolver
from Algproject.PM.path_match.util import *

class Game:
    """
    create some game instances
    """

    def __gen_game_instance(self, instance_num):
        grid = gen_grid(self.g.get_graph_nodes()[0], self.g.get_graph_nodes()[1])
        start_points = gen_start_points(8, grid)
        instances = []
        while instance_num > 0:
            try:
                solver = GameSolver(grid, start_points)
                paths = solver.solve()
                instance = solver.get_instance()
                instances.append(instance)
                instance_num -= 1
            except RuntimeError:
                # print("RuntimeError")
                start_points = gen_start_points(8, grid)
                continue
        self.game_instance = instances

    def read_game_instance(self):
        data_list = read_json_lines()
        self.game_instance_in_cache = handel_json_data(data_list)

    def __init__(self):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        pygame.display.set_caption("minimal program")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

        # Graph
        self.g = Graph(800, c.HEIGHT, (5, 10))

        # UI 
        self.ui = Ui(400, c.HEIGHT)

        self.clock = pygame.time.Clock()
        self.running = False
        self.track_edge = []
        self.game_instance = []
        self.game_instance_in_cache = []
        self.read_game_instance()

    def run(self):
        self.running = True
        self.g.draw_originalpath(self.game_instance_in_cache)
        # main loop
        while self.running:
            self.clock.tick(60)
            self.events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                self.ui.handle(event)

            self.ui.update(mouse_rel)

            # Drawing
            self.ui.draw(self.screen)
            self.g.draw(self.screen)
            pygame.display.flip()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()

    game.run()
    #print(get_src_dir())
    #print(get_root_dir())
