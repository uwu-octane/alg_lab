import pygame
import thorpy as tp


class Ui:
    def __init__(self, width, height):
        # UI
        self.ui_surface = pygame.Surface((width, height))
        self.ui_surface.fill((100, 100, 100))
        tp.init(self.ui_surface, tp.theme_human)

        self.tp_button_solve = tp.Button("Solve")
        self.tp_width_input = tp.TextInput("", "Type text here")
        self.tp_width = tp.Labelled("Cells Width:", self.tp_width_input)
        self.tp_height_input = tp.TextInput("", "Type text here")
        self.tp_height = tp.Labelled("Cells Height:", self.tp_height_input)
        self.tp_amount_pairs_input = tp.TextInput("", "Type text here")
        self.tp_amount_pairs = tp.Labelled("Amount of pairs:", self.tp_amount_pairs_input)
        self.tp_checkbox_bottleneck = tp.Labelled("Bottleneck?", tp.Checkbox())
        self.tp_checkbox_bottleneck.element._at_click = self.__checkbox_bottleneck_callback
        self.tp_checkbox_bottleneck.element.set_value(True)
        self.tp_bottleneck_input = tp.TextInput("      ")
        self.tp_bottleneck = tp.Labelled("Bottleneck:", self.tp_bottleneck_input)
        self.tp_valid_input = tp.TextInput("      ")
        self.tp_valid = tp.Labelled("Valid:", self.tp_valid_input)
        self.tp_button_apply = tp.Button("Apply")
        self.tp_button_clear = tp.Button("Clear")
        self.tp_button_check = tp.Button("Check")
        self.tp_button_group = tp.Group(
            [self.tp_button_apply, self.tp_button_clear, self.tp_button_solve, self.tp_button_check], "h")

        self.tp_instance_box = tp.TitleBox("Instance Settings", [self.tp_width, self.tp_height, self.tp_amount_pairs,
                                                                 self.tp_checkbox_bottleneck], sort_immediately=True)

        self.tp_solution_box = tp.TitleBox("Solution", [self.tp_bottleneck, self.tp_valid], sort_immediately=True)

        self.tp_ui_box = tp.Box([self.tp_instance_box, self.tp_solution_box, self.tp_button_group])
        self.tp_ui_box.center_on(self.ui_surface)

        self.updater = self.tp_ui_box.get_updater()
        self.events = None

    def __checkbox_bottleneck_callback(self):
        if self.tp_checkbox_bottleneck.get_value():
            self.tp_bottleneck.set_locked(True)
        else:
            self.tp_bottleneck.set_locked(False)

    def handle(self, events, mouse_rel):
        self.updater.update(events=events, mouse_rel=mouse_rel)

    def draw(self, surface):
        surface.blit(self.ui_surface, (0, 0))

    def clear_all(self):
        # self.tp_width.set_value("")
        self.tp_width_input.value = ""
        self.tp_height_input.value = ""
        self.tp_amount_pairs_input.value = ""
        self.tp_bottleneck.set_value("")
        self.tp_valid_input.set_value("")

    # to make an alert(pop-up windows)
    def show_alert(self, valid=0):
        if valid == 0:
            self.alert = tp.Alert("RESULT", "Invalid")
        else:
            self.alert = tp.Alert("RESULT", "Valid")
        self.alert.set_size((200, 200))
        self.alert.set_bck_color((150, 150, 150))
        self.alert.launch_nonblocking()

