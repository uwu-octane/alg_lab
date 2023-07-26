# import the pygame module, so you can use it
import pygame, thorpy as tp

import graph

WIDTH = 1200
HEIGHT = 800
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("minimal program")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # Graph
    graph_surface = pygame.Surface((800,HEIGHT))
    graph_surface.fill((255,255,255))
    g = graph.Graph(graph_surface,(10,10))
    g.draw()

    # UI
    ui_surface = pygame.Surface((400,HEIGHT))
    ui_surface.fill((100,100,100))
    tp.init(ui_surface,tp.theme_human)
    button = tp.Button("Nani!!???")
    updater = button.get_updater()

    # Drawing
    screen.blit(ui_surface,(0,0))
    screen.blit(graph_surface,(400,0))
     
    running = True
    clock = pygame.time.Clock()
     
    # main loop
    while running:
        clock.tick(60)
        events = pygame.event.get()
        mouse_rel = pygame.mouse.get_rel()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        updater.update(events=events, mouse_rel=mouse_rel)
        pygame.display.flip()
     
if __name__=="__main__":
    main()
