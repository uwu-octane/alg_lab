import Algproject.PM.game.constants as c

"""
this function is to adjust the click positions, because the graph is not in the left top corner of the window,
but the game position is based on the left top corner of the window
"""

def convert_to_game_coordinates(click_pos, surface):
    game_x = click_pos[0] - (c.WIDTH - surface.get_width())
    game_y = click_pos[1] - (c.HEIGHT - surface.get_height())
    return game_x, game_y

