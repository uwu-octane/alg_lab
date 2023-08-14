import pygame
import thorpy as tp

from Algproject.PM.game.tools import *

class Ui:
    def __init__(self, width, height):
        # UI
        self.ui_surface = pygame.Surface((width, height))
        self.ui_surface.fill((100, 100, 100))
        tp.init(self.ui_surface, tp.theme_human)

        self.tp_button_solve = tp.Button("Solve")
        self.tp_button_play = tp.Button("Play")

        self.tp_button_group = tp.Group([self.tp_button_solve, self.tp_button_play])

        self.tp_width = tp.Labelled("Cells Width:", tp.TextInput("", "Type text here"))
        self.tp_height = tp.Labelled("Cells Height:", tp.TextInput("", "Type text here"))
        self.tp_checkbox_random = tp.Labelled("Random Start Points?", tp.Checkbox())
        self.tp_button_apply = tp.Button("Apply")

        self.tp_size_box = tp.TitleBox("Instance Settings", [self.tp_width, self.tp_height, self.tp_checkbox_random, self.tp_button_apply], sort_immediately=True)

        self.tp_ui_box = tp.Box([self.tp_size_box, self.tp_button_group])
        self.tp_ui_box.center_on(self.ui_surface)

        self.updater = self.tp_ui_box.get_updater()
        self.events = None

    def handle(self, events, mouse_rel):
        self.updater.update(events=events, mouse_rel=mouse_rel)

    def draw(self, surface):
        surface.blit(self.ui_surface, (0, 0))
