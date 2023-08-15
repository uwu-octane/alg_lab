import Algproject.PM.game.constants as c
from Algproject.PM.game import graph

"""
this function is to adjust the click positions, because the graph is not in the left top corner of the window,
but the game position is based on the left top corner of the window
"""


# graph_surface
def convert_to_game_coordinates(click_pos, surface):
    game_x = click_pos[0] - (c.WIDTH - surface.get_width())
    game_y = click_pos[1] - (c.HEIGHT - surface.get_height())
    return game_x, game_y


def check_is_in_cell(converted_click_pos, cells_coor):
    if converted_click_pos in cells_coor:
        return True
    return False


def safe_edge(edge, edges_shadow):
    if edge:
        if edge[0] == edge[1]:
            return False
        if edge in edges_shadow:
            return True
    return False
