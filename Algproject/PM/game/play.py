import pygame

from Algproject.PM.game.tools import *


class Play:
    def __int__(self, game):
        self.game = game

    def handle(self, game):
        start_pos = None
        end_pos = None
        events = game.events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    start_pos = convert_to_game_coordinates(event.pos, game.ui_surface)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left unclick
                    end_pos = convert_to_game_coordinates(event.pos, game.ui_surface)
                    if start_pos and end_pos:
                        print("start_pos: ", start_pos, "end_pos: ", end_pos)
                        game.track_edge.append((start_pos, end_pos))
                        game.g.add_edge(game.track_edge[len(game.track_edge) - 1][0],
                                        game.track_edge[len(game.track_edge) - 1][1])
"""
  for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click_pos = convert_to_game_coordinates(event.pos, self.g.graph_surface)
                        click_pos = self.g.get_cell_coordination(click_pos)
                        if check_is_in_cell(click_pos, self.g.cells_coor):
                            start_node = click_pos
                            print(start_node)
                        pygame.display.update()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        click_pos = convert_to_game_coordinates(event.pos, self.g.graph_surface)
                        click_pos = self.g.get_cell_coordination(click_pos)
                        start_node = start_node
                        if check_is_in_cell(click_pos, self.g.cells_coor):
                            end_node = click_pos
                            print(end_node)
                            if not safe_edge((start_node, end_node), self.g.edges_shadow):
                                print(start_node, end_node)
                                print("not safe")
                            else:
                                print("safe")
                                print(start_node, end_node)

                        pygame.display.update()
            for edge, is_shown in self.g.edges_shadow.items():
                if is_shown == 1:
                    
                    self.g.add_line(edge[0], edge[1])
                    #pygame.display.update()
"""