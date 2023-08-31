# import the pygame module, so you can use it
import pygame

from Algproject.PM.game.graph import Graph
from Algproject.PM.game.tools import *
from Algproject.PM.game.ui import Ui
from Algproject.PM.path_match.solver import GameSolver
from Algproject.PM.path_match.util import *


class Game:
    """
    This method generates solvable instances
    """

    def __gen_game_instance(self, pairs, bottleneck):
        grid = gen_grid(self.g.get_graph_nodes()[0], self.g.get_graph_nodes()[1])
        start_points = gen_start_points(2 * pairs, grid)

        # Try to generate a solvable instance.
        while True:
            try:
                self.solver = GameSolver(grid, start_points, bottleneck)
                self.solver.solve()
                self.bottleneck = self.solver.get_bottleneck()
                break
            except RuntimeError:
                start_points = gen_start_points(2 * pairs, grid)
                continue
        self.game_instance = self.solver.get_instance()

    """
    This method generates a graph from the existing solution and tries to solve it
    """

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
            solver = GameSolver(g, self.solver.get_start_points(), self.ui.tp_checkbox_bottleneck.get_value())
            return solver.validate()

    """
    Read game instance from json file
    """

    def __read_game_instance(self):
        data_list = read_json_lines()
        if data_list:
            game_instance_in_cache = handel_json_data(data_list)
            self.game_instance_in_cache = self.__instance_iterator(game_instance_in_cache)

    """
    Callback function for the Clear button. Clears all settings made so far
    """

    def ui_clear_button_callback(self):
        self.ui.clear_all()
        self.g.reset_solution_sign()
        self.g.start_points = []
        self.g.solver = None
        self.game_instance = None
        self.g.graph_surface.fill((255, 255, 255))
        self.game_instance_enterd = False
        for edge in self.g.edges_shadow:
            if self.g.edges_shadow[edge]:
                self.g.edges_shadow[edge] = False

    """
    Callback function for the Apply button. Generate Instance when button is clicked
    """

    def ui_apply_button_callback(self):
        width = self.ui.tp_width.get_value()
        height = self.ui.tp_height.get_value()

        # Check if entered text is not none
        if width != "" and height != "":
            width = int(width)
            height = int(height)

            # Adjust graph size to entred width and height
            self.g = Graph(800, c.HEIGHT, (width, height))

            # Check if pair textbox was set. If no, gereate a random amount of pairs
            self.pairs = self.ui.tp_amount_pairs.element.get_value()
            max_pairs = (width * height) // 2
            if self.pairs == "":
                self.pairs = random.randint(1, max_pairs)
            else:
                if int(self.pairs) > max_pairs:
                    self.pairs = max_pairs
                else:
                    self.pairs = int(self.pairs)
                    self.__gen_game_instance(self.pairs, self.ui.tp_checkbox_bottleneck.get_value())
                    store_in_json(self.game_instance[0], self.game_instance[1])
                    self.__read_game_instance()
                    self.g.draw(self.screen, self.solver)
                    self.game_instance_enterd = True

    """
    Callback function for the check button.
    """

    def ui_check_button_callback(self):
        if self.game_instance and self.game_instance_enterd:
            if self.validate():
                self.ui.show_alert(1)
                self.ui.tp_valid_input.set_value("Yes")
                self.ui.tp_bottleneck.set_value(str(self.bottleneck))
            else:
                self.ui.show_alert(0)
                self.ui.tp_valid_input.set_value("No")

    """
    Callback function for the solve button. When clicked, show the calculated solution
    """

    def ui_solve_button_callback(self):
        if self.game_instance_enterd:
            self.g.set_solution_sign()
            self.g.draw(self.screen, self.solver)
            bottleneck = str(self.bottleneck)
            self.ui.tp_bottleneck.set_value(bottleneck)

    """
    Callback function for the read button. When clicked, read an abitrary json file
    """

    def ui_read_button_callback(self):
        try:
            current_instance = next(self.game_instance_in_cache)
            g = nx.Graph()
            edges = []
            for path in current_instance[1]:
                edges.extend(path)
            g.add_edges_from(edges)
            nodes = list(g.nodes())
            width = max([node[0] for node in nodes]) + 1
            height = max([node[1] for node in nodes]) + 1
            self.solver = GameSolver(g, current_instance[0], self.ui.tp_checkbox_bottleneck.get_value())
            self.solver.solve()
            self.bottleneck = self.solver.get_bottleneck()
            self.g = Graph(800, c.HEIGHT, (width, height))
            self.game_instance = self.solver.get_instance()
            self.g.draw(self.screen, self.solver)
            self.game_instance_enterd = True
        except StopIteration:
            pass

    def __instance_iterator(self, game_instance_in_cache):
        for item in game_instance_in_cache:
            yield item

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
        self.ui.tp_button_read._at_click = self.ui_read_button_callback
        self.clock = pygame.time.Clock()
        self.running = False
        self.mouse_clicked = False
        self.left_or_right_click = False
        """
        this array is to maintain the mouse motion when the user is drawing a path
        """
        self.tracking_mouse_motion = []
        """
        any instance is always in form (start_points, path)
        where start_points is a list of points (x, y) and path is a list of paths [path1, path2, ...]
        every path is a list of edges [((x1, y1), (x2, y2)), ...]
        """
        self.game_instance = None
        self.game_instance_in_cache = []
        self.game_instance_enterd = False  # Has the use enterend instance settings?
        self.solver = None
        self.__read_game_instance()

        self.events = None
        self.mouse_rel = None

    def run(self):
        clock = pygame.time.Clock()
        self.running = True
        # main loop
        while self.running:
            self.clock.tick(60)
            self.events = pygame.event.get()
            self.mouse_rel = pygame.mouse.get_rel()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                    """
                    hold left mouse button to draw edges
                    hold right mouse button to cancel edges
                    """
                elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click
                    # event.button == 1 -> left mouse button
                    # event.button == 3 -> right mouse button
                    # during mouse motion the event.type is not stored, so we use mouse_click to enable a flag
                    self.mouse_clicked = True
                    if event.button == 1:
                        self.left_or_right_click = True
                    if event.button == 3:
                        self.left_or_right_click = False

                elif event.type == pygame.MOUSEBUTTONUP:  # mouse click release
                    """
                    when button up is caught, we reset the tacking information and mouse_clicked flag
                    """
                    self.mouse_clicked = False
                    self.tracking_mouse_motion = []

                elif event.type == pygame.MOUSEMOTION:
                    if self.mouse_clicked:
                        move_point = convert_to_game_coordinates(event.pos, self.g.graph_surface)
                        move_point = self.g.get_simple_cell_coordination(move_point)

                        if move_point not in self.tracking_mouse_motion:
                            self.tracking_mouse_motion.append(move_point)

                        if self.left_or_right_click:
                            self.g.connect_edges(self.tracking_mouse_motion)
                        else:
                            self.g.cancel_edges(self.tracking_mouse_motion)
                            self.g.remove_line(self.screen)

            # UI
            self.ui.handle(self.events, self.mouse_rel)

            # Drawing
            self.screen.fill((255, 255, 255))
            self.ui.draw(self.screen)
            if self.solver:
                self.g.draw(self.screen, self.solver)
            else:
                self.g.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
