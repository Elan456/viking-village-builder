import pygame
from config.defines import *

class Building(pygame.sprite.Sprite):
    """
    Handles the building's rendering after it has been placed on the map.
    Handles updating the building's state, like how much resources it has produced.
    """
    def __init__(self, village, x, y) -> None:
        """
        Initializes the building's position and image.

        :param village: A reference to the village this building belongs to
        :param x: x coordinate of the building
        :param y: y coordinate of the building
        """
        super().__init__()
        self.village = village
        self.x = x
        self.y = y

        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.name = "Building"
        self.construction_cost = {}

    def draw(self, surface: pygame.Surface):
        """
        Draws the building on the screen.

        :param surface: The surface to draw the building on
        """
        surface.blit(self.image, (self.x - camera_x, self.y - camera_y))

    def _set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def _set_construction_cost(self, cost: dict):
        self.construction_cost = cost

