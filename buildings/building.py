import pygame
from config import defines 
from villagers.villager import Villager
from villagers.builder import Builder
from buildings.building_info import BldInfo

class Building(pygame.sprite.Sprite):
    """
    Handles the building's rendering after it has been placed on the map.
    Handles updating the building's state, like how much resources it has produced.
    """
    def __init__(self, village, x_cell, y_cell, name) -> None:
        """
        Initializes the building's position and image.

        :param village: A reference to the village this building belongs to
        :param x: x coordinate of the building (cell)
        :param y: y coordinate of the building (cell)
        """
        super().__init__()
        self.name = name
        self.village = village
        self.x_cell = x_cell
        self.y_cell = y_cell
        self.x = x_cell * defines.GRID_SIZE
        self.y = y_cell * defines.GRID_SIZE
        self.image = pygame.image.load(BldInfo.get_image_path(name))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.rect = self.image.get_rect()
        self.construction_cost = BldInfo.get_construction_cost(name)
        self.construction_time = BldInfo.get_construction_time(name)
        self.production = BldInfo.get_production(name)
        self.cost = BldInfo.get_cost(name)

        self.villager_name = BldInfo.get_villager_name(name)

        self.my_villager = Villager(self) if self.villager_name != "builder" else Builder(self)
        self.disabled = False

    def draw(self, surface: pygame.Surface):
        """
        Draws the building on the screen.

        :param surface: The surface to draw the building on
        """
        # print(camera_x, camera_y)
        surface.blit(self.image, (self.x - defines.camera_x, self.y - defines.camera_y))

        # Draw a grey rectangle if the building is disabled
        if self.disabled:
            pygame.draw.rect(surface, (150, 150, 150), (self.x - defines.camera_x, self.y - defines.camera_y, self.rect.width, self.rect.height), 5)

    def update(self):
        """
        Updates the building's state. 
        """
        self.my_villager.update()

    def get_current_production(self):
        """
        Returns a dictionary of what resources the building can produce next turn
        """
        current_production = {} 
        if not self.disabled:
            if all(self.village.resources[resource] >= amount for resource, amount in self.cost.items()):
                for resource, amount in self.production.items():
                    current_production[resource] = amount * self.village.production_multipliers[resource]

        return current_production

    def on_new_turn(self):
        """
        Called when a new turn occurs
        """

        cp = self.get_current_production()
        if cp: # If we can produce resources
            # Consume resources
            for resource, amount in self.cost.items():
                self.village.resources[resource] -= amount
            # Produce resources
            for resource, amount in cp.items():
                self.village.resources[resource] += amount

    def disable(self):
        """
        Disables the building
        """
        if not self.disabled:
            self.disabled = True

    def enable(self):
        """
        Enables the building
        """
        if self.disabled:
            self.disabled = False

    def demolish(self):
        """
        Adds this building to the demolish queue
        """
        if self not in self.village.building_demolish_queue: 
            self.village.building_demolish_queue.append(self)

    def get_cell_width(self):
        return self.rect.width // defines.GRID_SIZE
    
    def get_cell_height(self):
        return self.rect.height // defines.GRID_SIZE
    
    def get_villager_name(self):
        if self.villager_name is None:
            raise NotImplementedError("Villager name not defined")
        
        return self.villager_name

