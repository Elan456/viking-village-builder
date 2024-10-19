"""
The main panel lives on the bottom of the screen and gives the player a button to got to the next turn
"""

import pygame
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT, FONT_PATH
from utils.button import Button
from .resources import get_icon
from .resources import resource_to_icon

class MainPanel:
    def __init__(self, village) -> None:
        self.village = village
        self.next_turn_button = Button(0, DISPLAY_HEIGHT - 100, 200, 100, "Next Turn",
                                        (0, 255, 0), (0, 0, 0),
                                          FONT, self.next_turn)
        
        self.turn_font = pygame.font.Font(FONT_PATH, 24)
        self.resource_font = pygame.font.Font(FONT_PATH, 16)

        self.resource_box_width = 100
        self.resource_box_height = 100
        self.resource_box = pygame.Surface((self.resource_box_width, self.resource_box_height), pygame.SRCALPHA)
        self.resource_box.fill((150, 150, 150, 180))
    
        
    def update(self):
        self.next_turn_button.update()

    def draw(self, surface):
        # alpha
        surface.convert_alpha()
        self.next_turn_button.draw(surface)

        current_turn_text = self.turn_font.render(f"Turn: {self.village.turn}", True, (0, 0, 0))
        surface.blit(current_turn_text, (220, DISPLAY_HEIGHT - 100))

        
        surface.blit(self.resource_box, (DISPLAY_WIDTH//2-self.resource_box_width//2, 0))

        for i, resource in enumerate(resource_to_icon.keys()):
            icon = get_icon(resource)
            surface.blit(icon, (DISPLAY_WIDTH//2-self.resource_box_width//2, 0 + i*20))
            resource_text = self.resource_font.render(f"{self.village.resources[resource]}", True, (0, 0, 0))
            surface.blit(resource_text, (DISPLAY_WIDTH//2-self.resource_box_width//2 + 50, 0 + i*20))

    def next_turn(self):
        self.village.on_new_turn()