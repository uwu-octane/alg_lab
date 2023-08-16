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

        self.tp_button_group1 = tp.Group([self.tp_button_solve, self.tp_button_play], "h")

        self.tp_width = tp.Labelled("Cells Width:", tp.TextInput("", "Type text here"))
        self.tp_height = tp.Labelled("Cells Height:", tp.TextInput("", "Type text here"))
        self.tp_checkbox_random = tp.Labelled("Random pairs?", tp.Checkbox())
        self.tp_checkbox_random.element._at_click = self.__checkbox_random_callback
        self.tp_checkbox_random.element.set_value(True)
        self.tp_amount_pairs = tp.Labelled("Amount of pairs:", tp.TextInput("", "Type text here"))
        self.tp_button_apply = tp.Button("Apply")
        self.tp_button_clear = tp.Button("Clear")
        self.tp_button_group2 = tp.Group([self.tp_button_apply, self.tp_button_clear], "h")

        self.tp_instance_box = tp.TitleBox("Instance Settings", [self.tp_width, self.tp_height, self.tp_checkbox_random, self.tp_amount_pairs, self.tp_button_group2], sort_immediately=True)

        self.tp_ui_box = tp.Box([self.tp_instance_box, self.tp_button_group1])
        self.tp_ui_box.center_on(self.ui_surface)

        self.updater = self.tp_ui_box.get_updater()
        self.events = None

    def __checkbox_random_callback(self):
        if self.tp_checkbox_random.get_value():
            self.tp_amount_pairs.set_locked(True)
        else:
            self.tp_amount_pairs.set_locked(False)


    def handle(self, events, mouse_rel):
        self.updater.update(events=events, mouse_rel=mouse_rel)

    def draw(self, surface):
        surface.blit(self.ui_surface, (0, 0))
