# import the pygame module, so you can use it
import pygame
import random

from Algproject.PM.game.tools import *
from Algproject.PM.game.graph import Graph
from Algproject.PM.game.ui import Ui
import Algproject.PM.game.constants as c

from Algproject.PM.path_match.solver import GameSolver
from Algproject.PM.path_match.util import *


class Game:
    """
    create some game instances
    """

    def __gen_game_instance(self, instance_num, pairs):
        grid = gen_grid(self.g.get_graph_nodes()[0], self.g.get_graph_nodes()[1])
        start_points = gen_start_points(2 * pairs, grid)
        instances = []
        while instance_num > 0:
            try:
                solver = GameSolver(grid, start_points)
                solver.solve()
                instance = solver.get_instance()
                self.bottleneck = solver.get_bottleneck()
                instances.append(instance)
                instance_num -= 1
            except RuntimeError:
                # print("RuntimeError")
                start_points = gen_start_points(2 * pairs, grid)
                continue
        self.game_instance = instances

    def validate(self):
        if self.g.edges_shadow:
            g = nx.Graph()
            edge_copy = set()
            for edge, is_shown in self.g.edges_shadow.items():
                if is_shown:
                    edge_copy.add(edge)
            g.add_edges_from(list(edge_copy))
            cells = self.g.cells_coor
            for cell in cells:
                g.add_node(cell)
            print(self.g.start_points)
            solver = GameSolver(g, self.g.start_points)
            return solver.validate()

    def read_game_instance(self):
        data_list = read_json_lines()
        self.game_instance_in_cache = handel_json_data(data_list)

    """
    Callback function for the Clear button. Clears all settings made so far
    """

    def ui_clear_button_callback(self):
        # TODO: Clear UI element's content, only bottleneck cannot be cleared
        self.ui.clear_all()
        self.g.graph_surface.fill((255, 255, 255))
        for edge in self.g.edges_shadow:
            if self.g.edges_shadow[edge]:
                self.g.edges_shadow[edge] = False

    """
    Callback function for the Apply button. Generate Instance when button is clicked
    """

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
                self.pairs = self.ui.tp_amount_pairs.element.get_value()
                max_pairs = (widht * height) // 2
                if self.pairs == "":
                    self.pairs = random.randint(1, (widht * height) // 2)
                else:
                    if int(self.pairs) > max_pairs:
                        self.pairs = max_pairs
                    else:
                        self.pairs = int(self.pairs)
                        # TODO: Sometimes an error occurs (probably when an instance is unsolvable, we need a solution to display such a case)
                        self.__gen_game_instance(1, self.pairs)
                        self.g.start_points = self.game_instance[0][0]
                        self.g.draw(self.screen)

    def ui_check_button_callback(self):
        if self.game_instance:
            if self.validate():
                print("Valid")
            else:
                print("Invalid")

    def ui_solve_button_callback(self):
        if self.game_instance is None:
            self.ui_apply_button_callback()

        self.g.draw_originalpath(self.game_instance)
        bottleneck = str(self.bottleneck)
        self.ui.tp_bottleneck.set_value(bottleneck)

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
        self.ui.tp_button_clear._at_click = self.ui_clear_button_callback
        self.ui.tp_button_check._at_click = self.ui_check_button_callback
        self.ui.tp_button_solve._at_click = self.ui_solve_button_callback
        self.clock = pygame.time.Clock()
        self.running = False
        self.game_instance = None
        self.game_instance_in_cache = []
        # self.read_game_instance()

        self.events = None
        self.mouse_rel = None

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        # main loop
        start_node = None
        end_node = None
        while self.running:
            self.clock.tick(60)
            self.events = pygame.event.get()
            self.mouse_rel = pygame.mouse.get_rel()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:
                        click_pos = convert_to_game_coordinates(event.pos, self.g.graph_surface)
                        click_pos = self.g.get_simple_cell_coordination(click_pos)
                        if check_is_in_cell(click_pos, self.g.cells_coor):
                            start_node = click_pos
                            print(start_node)
                        pygame.display.update()
                elif event.type == pygame.MOUSEBUTTONUP:
                    click_pos = convert_to_game_coordinates(event.pos, self.g.graph_surface)
                    click_pos = self.g.get_simple_cell_coordination(click_pos)

                    if check_is_in_cell(click_pos, self.g.cells_coor):
                        end_node = click_pos
                        print(end_node)
                        edge = (start_node, end_node)
                        if safe_edge(edge, self.g.edges_shadow):
                            if event.button == 1:
                                self.g.edges_shadow[edge] = 1
                                pygame.display.update()
                                """
                                right mouse click to cancel the edge
                                """
                            if event.button == 3:
                                self.g.edges_shadow[edge] = 0
                                self.g.edges_shadow[(end_node, start_node)] = 0
                                self.g.remove_line(self.screen)
                                pygame.display.update()
            # UI
            self.ui.handle(self.events, self.mouse_rel)

            # Drawing
            self.screen.fill((255, 255, 255))
            self.ui.draw(self.screen)
            self.g.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
