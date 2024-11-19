"""
The main panel lives on the bottom of the screen and gives the player a button to got to the next turn
"""

import pygame
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, FONT_PATH, WIN_CONDITION
from utils.button import Button
from utils.style_button import StyleButton
from assets.ui.button_mapping import GREEN_NEXT
from .resources import get_icon
from .resources import resource_to_icon

class MainPanel:
    def __init__(self, village) -> None:
        self.village = village
        self.next_turn_font = pygame.font.Font(FONT_PATH, 24)
        self.next_turn_button = StyleButton(50, DISPLAY_HEIGHT - 150, 100, 100, GREEN_NEXT, self.next_turn,
                                            hover_text="Next Turn" )
        
        self.turn_font = pygame.font.Font(FONT_PATH, 24)
        self.resource_font = pygame.font.Font(FONT_PATH, 16)

        self.resource_box_x = 0
        self.resource_box_y = 0
        self.resource_box_width = 400
        self.resource_box_height = self.village.resources.keys().__len__() * (self.resource_font.get_height() + 3)
        self.resource_box = pygame.Surface((self.resource_box_width, self.resource_box_height), pygame.SRCALPHA)
        self.resource_box.fill((150, 150, 150, 150))
    
        
    def update(self):
        self.next_turn_button.update()

    def draw(self, surface):
        # alpha
        surface.convert_alpha()

        background = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.rect(background, (255, 255, 255, 100), (0, 0, 200, 200))
        surface.blit(background, (0, DISPLAY_HEIGHT - 200))

        self.next_turn_button.draw(surface)

        current_turn_text = self.turn_font.render(f"{100 - self.village.turn} turns left", True, (0, 0, 0))
        surface.blit(current_turn_text, (10, DISPLAY_HEIGHT - 190))

        
        surface.blit(self.resource_box, (self.resource_box_x, self.resource_box_y))

        v_spacing = 25

        resources_change = self.village.calculate_turn_change_resources()

        turns_left = 100 - self.village.turn

        # Projected final resources
        final_resources = self.village.resources.copy()
        for resource, change in resources_change.items():
            final_resources[resource] += change * turns_left


        for i, resource in enumerate(resource_to_icon.keys()):
            icon = get_icon(resource)
            surface.blit(icon, (self.resource_box_x, 0 + i*v_spacing))
            
            delta = round(resources_change.get(resource, 0),2)
            if delta > 0:
                delta = "+ " + str(delta)
            elif delta == 0:
                delta = ""
            else:
                delta = f"- {abs(delta)}"
            resource_string = f"{round(self.village.resources[resource],2)} {delta}"

            multiplication_value = round(self.village.production_multipliers[resource],2)

            resource_string += f" x {multiplication_value:.2f}" if multiplication_value != 1 else ""

            resource_text = self.resource_font.render(resource_string, True, (0, 0, 0))
            surface.blit(resource_text, (self.resource_box_x + 30, 0 + i*v_spacing))

            # If the resource is in the win condition, show the win condition and the current projection
            if resource in WIN_CONDITION:
                win_condition = int(WIN_CONDITION[resource])
                projected_value = int(final_resources[resource])
                win_condition_text = self.resource_font.render(f"Projection: {projected_value}/{win_condition}", True, (0, 0, 0))
                surface.blit(win_condition_text, (self.resource_box_x + 180, 0 + i*v_spacing))

    def next_turn(self):
        self.village.on_new_turn()