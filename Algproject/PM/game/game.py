# import the pygame module, so you can use it
import pygame
import random

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
                # paths = solver.solve()
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

    def ui_apply_button_callback(self):
        widht = self.ui.tp_width.get_value()
        height = self.ui.tp_height.get_value()

        # Check if entered text is not none
        if widht != "" and height != "":
            widht = int(widht)
            height = int(height)

            # Adjust graph size
            self.g = Graph(800, c.HEIGHT, (widht, height))

            # Generate random start points if desired
            random_points = self.ui.tp_checkbox_random.get_value()
            if random_points:

                # Check if pair textbox was set
                pairs = self.ui.tp_amount_pairs.element.get_value()
                max_pairs = (widht*height)//2
                if pairs == "":
                    pairs = random.randint(1, (widht*height)//2)
                else:
                    if int(pairs) > max_pairs:
                        pairs = max_pairs
                    else:
                        pairs = int(pairs)

                # Generate pairs with color, start_points and end_points
                colors = [random.sample(range(200*i//pairs, 200), 3) for i in range(pairs)]
                population = [(x, y) for x in range(widht) for y in range(height)] 
                start_points = random.sample(population, pairs)
                end_points = random.sample(set(population)-set(start_points), pairs)

                for i in range(pairs):
                    color = colors[i]
                    start = (start_points[i][0], start_points[i][1])
                    end = (end_points[i][0], end_points[i][1])
                    self.g.add_start_point(start, end, color)

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
        self.ui.tp_button_apply._at_click = self.ui_apply_button_callback

        self.clock = pygame.time.Clock()
        self.running = False
        self.track_edge = []
        self.game_instance = []
        self.game_instance_in_cache = []
        self.read_game_instance()

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        # self.g.draw_originalpath(self.game_instance_in_cache)
        # main loop
        while self.running:
            self.clock.tick(60)
            self.events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

            # UI
            self.ui.handle(self.events, mouse_rel)

            # Drawing
            self.screen.fill((255, 255, 255))
            self.ui.draw(self.screen)
            self.g.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    game = Game()

    game.run()
    # print(get_src_dir())
    # print(get_root_dir())
