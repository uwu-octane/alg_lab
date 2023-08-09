import pygame
import thorpy as tp

from Algproject.PM.game.tools import *

class Ui:
    def __init__(self, width, height):
        # UI
        self.ui_surface = pygame.Surface((width, height))
        self.ui_surface.fill((100, 100, 100))
        tp.init(self.ui_surface, tp.theme_human)

        self.button = tp.Button("Test")
        self.button.center_on(self.ui_surface)
        self.updater = self.button.get_updater()
        self.events = None

    def update(self, mouse_rel):
        self.updater.update(events=self.events, mouse_rel=mouse_rel)

    def handle(self, event):
        None

    def draw(self, surface):
        surface.blit(self.ui_surface, (0, 0))
