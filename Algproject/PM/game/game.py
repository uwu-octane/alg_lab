# import the pygame module, so you can use it
import pygame, thorpy as tp

import graph

WIDTH = 1200
HEIGHT = 800


def convert_to_game_coordinates(click_pos, graph_size):
    game_x = click_pos[0] - (WIDTH - graph_size[0])
    game_y = click_pos[1] - (HEIGHT - graph_size[1])
    return game_x, game_y


# define a main function
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
    g.draw()
    # UI
    ui_surface = pygame.Surface((400, HEIGHT))
    ui_surface.fill((100, 100, 100))
    tp.init(ui_surface, tp.theme_human)
    button = tp.Button("Nani!!???")
    updater = button.get_updater()

    # Drawing
    screen.blit(ui_surface, (0, 0))
    screen.blit(graph_surface, (400, 0))

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
            """
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_pos = convert_to_game_coordinates(event.pos, g.get_graph_size())
                g.mouse_click(game_pos)
            """
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
                        print("draw")
                        #not working ! ?
                        g.draw_edge(start_pos, end_pos)
                    start_pos = None
                    end_pos = None
        updater.update(events=events, mouse_rel=mouse_rel)
        pygame.display.flip()


if __name__ == "__main__":
    main()
