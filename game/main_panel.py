"""
The main panel lives on the bottom of the screen and gives the player a button to got to the next turn
"""

import pygame
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT_PATH, WIN_CONDITION
from config import defines
from utils.style_button import StyleButton
from assets.ui.button_mapping import GREEN_NEXT
from .resources import get_icon
from .resources import resource_to_icon
import math

class MainPanel:
    def __init__(self, village) -> None:
        self.village = village
        self.next_turn_font = pygame.font.Font(FONT_PATH, 24)
        self.next_turn_button = StyleButton(50, DISPLAY_HEIGHT - 150, 100, 100, GREEN_NEXT, self.next_turn,
                                            hover_text="Next Turn" )

        self.turn_font = pygame.font.Font(FONT_PATH, 24)
        self.resource_font = pygame.font.Font(FONT_PATH, 24)

        self.help = False
        self.village.event_handler.register_help(lambda: setattr(self, "help", not self.help))

        self.resource_box_x = 25
        self.resource_box_y = 0
        self.resource_box_width = 550
        self.resource_box_height = self.village.resources.keys().__len__() * (self.resource_font.get_height())
        self.resource_box = pygame.Surface((self.resource_box_width, self.resource_box_height), pygame.SRCALPHA)
        self.resource_box.fill((150, 150, 150, 200))
        self.draw_tick = 0

        # Static panels — never reallocate per frame
        self.turn_button_bg = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.rect(self.turn_button_bg, (255, 255, 255, 100), (0, 0, 200, 200))

        self.help_hint = defines.HELP_FONT.render("Press H for help", True, defines.HELP_COLOR)
        self._help_next_turn_lines = [
            defines.HELP_FONT.render(line, True, defines.HELP_COLOR)
            for line in (
                "This shows the number of turns left until the end of the game.",
                "Click the button to advance to the next turn,",
                "which triggers the production of resource and construction of buildings.",
            )
        ]
        self._help_resource_lines = [
            defines.HELP_FONT.render(line, True, defines.HELP_COLOR)
            for line in (
                "This is the main resource panel.",
                "It shows the change in resources for the next turn.",
                "Based on the current production rate, it predicts your final soldier and ship counts.",
                "You need 250 soldiers and 10 ships on the final turn to win.",
            )
        ]

        # Resource HUD cache — rebuilt only when underlying data changes
        self._hud_cache = None
        self._hud_cache_key = None
        self._turns_left_text = None
        self._turns_left_value = None

    def update(self):
        self.next_turn_button.update()

    def _resource_cache_key(self):
        # Cheap key: only recompute production when this changes
        return (
            self.village.turn,
            tuple(
                (
                    resource,
                    round(self.village.resources[resource], 2),
                    round(self.village.production_multipliers[resource], 2),
                )
                for resource in resource_to_icon.keys()
            ),
            tuple(
                (b.name, b.disabled, b.being_demolished, round(b.boost[0], 3))
                for b in self.village.buildings
            ),
        )

    def _rebuild_hud_cache(self):
        resources_change = self.village.calculate_turn_change_resources()
        deprived_of = set()
        for building in self.village.buildings:
            deprived_of.update(building.deprived_of)

        cache = pygame.Surface(
            (self.resource_box_width, self.resource_box_height), pygame.SRCALPHA
        )
        cache.blit(self.resource_box, (0, 0))
        pygame.draw.rect(
            cache, (0, 0, 0), (0, 0, self.resource_box_width, self.resource_box_height), 2
        )

        v_spacing = 25
        turns_left = 100 - self.village.turn
        final_resources = self.village.resources.copy()
        for resource, change in resources_change.items():
            final_resources[resource] += change * turns_left

        for i, resource in enumerate(resource_to_icon.keys()):
            icon = get_icon(resource)
            cache.blit(icon, (10, 10 + i * v_spacing))

            delta = round(resources_change.get(resource, 0), 2)
            if delta > 0:
                delta_str = "+ " + str(delta)
            elif delta == 0:
                delta_str = ""
            else:
                delta_str = f"- {abs(delta)}"
            resource_string = f"{round(self.village.resources[resource], 2)} {delta_str}"

            multiplication_value = round(self.village.production_multipliers[resource], 2)
            if multiplication_value != 1:
                resource_string += f" x {multiplication_value:.2f}"

            resource_color = (100, 0, 0) if resource in deprived_of else (0, 0, 0)
            resource_text = self.resource_font.render(resource_string, True, resource_color)
            cache.blit(resource_text, (50, 10 + i * v_spacing))

            if resource in WIN_CONDITION:
                win_condition = int(WIN_CONDITION[resource])
                projected_value = int(final_resources[resource])
                win_condition_color = (
                    (0, 0, 0) if projected_value >= win_condition else (100, 0, 0)
                )
                win_condition_text = self.resource_font.render(
                    f"Projection: {projected_value}/{win_condition}",
                    True,
                    win_condition_color,
                )
                cache.blit(
                    win_condition_text,
                    (resource_text.get_width() + 80, 10 + i * v_spacing),
                )

        self._hud_cache = cache

    def draw(self, surface):
        self.draw_tick += 1
        self.draw_tick %= 10000

        surface.blit(self.turn_button_bg, (0, DISPLAY_HEIGHT - 200))
        self.next_turn_button.draw(surface)

        turns_left = 100 - self.village.turn
        if turns_left != self._turns_left_value:
            self._turns_left_value = turns_left
            self._turns_left_text = self.turn_font.render(
                f"{turns_left} turns left", True, (0, 0, 0)
            )
        surface.blit(self._turns_left_text, (10, DISPLAY_HEIGHT - 190))

        if self.help:
            for i, text in enumerate(self._help_next_turn_lines):
                surface.blit(text, (200, DISPLAY_HEIGHT - 150 + i * (text.get_height() + 3)))
            pygame.draw.rect(surface, defines.HELP_COLOR, (50, DISPLAY_HEIGHT - 150, 100, 100), 2)

        cache_key = self._resource_cache_key()
        if cache_key != self._hud_cache_key:
            self._hud_cache_key = cache_key
            self._rebuild_hud_cache()

        surface.blit(self._hud_cache, (self.resource_box_x, self.resource_box_y))

        if self.help:
            for i, text in enumerate(self._help_resource_lines):
                surface.blit(
                    text,
                    (
                        self.resource_box_x,
                        self.resource_box_y
                        + self.resource_box_height
                        + 10
                        + i * (text.get_height() + 3),
                    ),
                )
            pygame.draw.rect(
                surface,
                defines.HELP_COLOR,
                (
                    self.resource_box_x,
                    self.resource_box_y,
                    self.resource_box_width,
                    self.resource_box_height,
                ),
                2,
            )

        offset = math.sin(self.draw_tick / (2 * math.pi)) * 10
        surface.blit(
            self.help_hint,
            (
                DISPLAY_WIDTH - self.help_hint.get_width() * 2,
                DISPLAY_HEIGHT - self.help_hint.get_height() - 10 + offset,
            ),
        )

    def next_turn(self):
        self.village.on_new_turn()
