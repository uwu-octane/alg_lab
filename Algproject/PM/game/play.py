import pygame

from Algproject.PM.game.tools import *

class Play:
    def __int__(self, events):
        self.events = events

    def handle(self, event):
        start_pos = None
        end_pos = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                start_pos = convert_to_game_coordinates(event.pos, self.ui_surface)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # left unclick
                end_pos = convert_to_game_coordinates(event.pos, self.ui_surface)
                if start_pos and end_pos:
                    print("start_pos: ", start_pos, "end_pos: ", end_pos)
                    self.track_edge.append((start_pos, end_pos))
                    self.g.add_edge(self.track_edge[len(self.track_edge) - 1][0],
                                    self.track_edge[len(self.track_edge) - 1][1])
