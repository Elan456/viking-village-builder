"""
Defines the wall the surround your village 
This defines how much room you have to build in
The player can increase the size of their building area by upgrading the wall
"""

import pygame
from config.defines import GRID_SIZE
from config import defines 

class Wall(pygame.sprite.Sprite):
    def __init__(self, village) -> None:
        self.village = village

        # All defined in cells 
        self.width = 20
        self.height = 20
        self.x = 0
        self.y = 0

        self.color = (50, 50, 50)
        self.thickness = 8

    def draw(self, surface: pygame.Surface):
        """
        Draws the wall on the screen
        """
        # Draw the wall
        pygame.draw.rect(surface, self.color, (self.x * GRID_SIZE - defines.camera_x - self.thickness,
                                            self.y * GRID_SIZE - defines.camera_y - self.thickness,
                                              self.width * GRID_SIZE + 2 * self.thickness,
                                                self.height * GRID_SIZE + 2 * self.thickness), 8)
        

    def can_upgrade(self):
        """
        Checks if the wall can be upgraded
        """
        return self.village.resources["wood"] >= 100
    
    def upgrade(self):
        """
        Upgrades the wall to increase the size of the village
        """
        self.width += 5
        self.height += 5

    def can_build(self, x, y, width, height):
        """
        Checks if a building can be built at the given position
        by ensuring it is within the wall
        """
        
        # Ensures the building is within the wall
        if x < self.x or y < self.y:
            return False
        if x + width > self.x + self.width or y + height > self.y + self.height:
            return False
        return True 