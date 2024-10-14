import pygame
from config.defines import GRID_SIZE
from config import defines 
from villagers.villager import Villager

class Building(pygame.sprite.Sprite):
    """
    Handles the building's rendering after it has been placed on the map.
    Handles updating the building's state, like how much resources it has produced.
    """
    def __init__(self, village, x_cell, y_cell) -> None:
        """
        Initializes the building's position and image.

        :param village: A reference to the village this building belongs to
        :param x: x coordinate of the building (cell)
        :param y: y coordinate of the building (cell)
        """
        super().__init__()
        self.village = village
        self.x_cell = x_cell
        self.y_cell = y_cell
        self.x = x_cell * GRID_SIZE
        self.y = y_cell * GRID_SIZE

        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.name = "Building"
        self.construction_cost = {}

        self.villager_name = None 

        self.my_villager = Villager(self)

    def draw(self, surface: pygame.Surface):
        """
        Draws the building on the screen.

        :param surface: The surface to draw the building on
        """
        # print(camera_x, camera_y)
        surface.blit(self.image, (self.x - defines.camera_x, self.y - defines.camera_y))

        self.my_villager.draw(surface)

    def update(self):
        """
        Updates the building's state. 
        """
        self.my_villager.update()

    def _set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def _set_construction_cost(self, cost: dict):
        self.construction_cost = cost

    def get_cell_width(self):
        return self.rect.width // GRID_SIZE
    
    def get_cell_height(self):
        return self.rect.height // GRID_SIZE
    
    def get_villager_name(self):
        if self.villager_name is None:
            raise NotImplementedError("Villager name not defined")
        
        return self.villager_name

