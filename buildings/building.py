import pygame
from config import defines 
from villagers.villager import Villager
from villagers.builder import Builder
from buildings.building_info import BldInfo
from events.announcements import announcement_handler
from config.defines import GRID_SIZE


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
        self.image = BldInfo.images[name]
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
        self.being_demolished = False

    def draw_outline(self, surface: pygame.Surface):
        """
        Draw a black outline around the building to make it easier when placing new buildings
        """
        pygame.draw.rect(surface, (0, 0, 0), (self.x - defines.camera_x, self.y - defines.camera_y, self.rect.width, self.rect.height), 1)

    def draw(self, surface: pygame.Surface):
        """
        Draws the building on the screen.

        :param surface: The surface to draw the building on
        """
        # Draw a brown path on the ground around the building
        # pygame.draw.rect(surface, (227, 186, 116), (self.x - defines.camera_x - GRID_SIZE, self.y - defines.camera_y - GRID_SIZE, self.rect.width + GRID_SIZE * 2, self.rect.height + GRID_SIZE * 2), GRID_SIZE)

        # print(camera_x, camera_y)
        if not self.being_demolished:
            surface.blit(self.image, (self.x - defines.camera_x, self.y - defines.camera_y))

        # Draw a grey rectangle if the building is disabled
        if self.disabled:
            pygame.draw.rect(surface, (150, 150, 150), (self.x - defines.camera_x, self.y - defines.camera_y, self.rect.width, self.rect.height), 5)

    def update(self):
        """
        Updates the building's state. 
        """
        self.my_villager.update()

    def get_change_in_resources(self, available_resources):
        """
        Based on the available resources, calculate how the net change in resources will be next turn.
        """
        if self.disabled:
            return {}

        can_produce = all(available_resources[resource] >= amount for resource, amount in self.cost.items())
        
        if not can_produce:
            return {}
        
        change_in_resources = {}
        for resource in list(self.production.keys()) + list(self.cost.keys()):
            change_in_resources[resource] = self.production.get(resource, 0) - self.cost.get(resource, 0)

        return change_in_resources

    def on_new_turn(self):
        """
        Called when a new turn occurs
        """ 
        pass 

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
        if not self.being_demolished:
            self.being_demolished = True
            self.village.builder_manager.start_demolition(self)
        else:
            # Cancel the demolition
            self.being_demolished = False
            self.village.builder_manager.cancel(self)
            announcement_handler.add_announcement("Demolition cancelled")
            


    def get_cell_width(self):
        return self.rect.width // defines.GRID_SIZE
    
    def get_cell_height(self):
        return self.rect.height // defines.GRID_SIZE
    
    def get_villager_name(self):
        if self.villager_name is None:
            raise NotImplementedError("Villager name not defined")
        
        return self.villager_name

