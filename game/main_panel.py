"""
The main panel lives on the bottom of the screen and gives the player a button to got to the next turn
"""

import pygame
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT, FONT
from utils.button import Button

class MainPanel:
    def __init__(self, village) -> None:
        self.village = village
        self.next_turn_button = Button(DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100, 200, 100, "Next Turn",
                                        (0, 255, 0), (0, 0, 0),
                                          FONT, self.next_turn)
        
    def update(self):
        self.next_turn_button.update()

    def draw(self, surface):
        self.next_turn_button.draw(surface)

    def next_turn(self):
        self.village.on_new_turn()