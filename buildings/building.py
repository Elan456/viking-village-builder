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
        self.boost = 1, []  # Boost multiplier and nearest boost buildings

        self.deprived_of = []  # List of resources that this building is deprived of

    def draw_outline(self, surface: pygame.Surface):
        """
        Draw a black outline around the building to make it easier when placing new buildings
        """
        pygame.draw.rect(surface, (0, 0, 0), (self.x - defines.camera_x, self.y - defines.camera_y, self.rect.width, self.rect.height), 5)

    def draw(self, surface: pygame.Surface):
        """
        Draws the building on the screen.

        :param surface: The surface to draw the building on
        """
        # Get the background color from the world and make it a bit darker for the pad of the building
        background_color = self.village.world.background_color
        darker_color = tuple([max(0, color - 20) for color in background_color])

        # Get the bound for the ground pad but truncate based if the wall is really close
        x_min = max(self.village.wall.x, self.x - defines.GRID_SIZE)
        y_min = max(self.village.wall.y, self.y - defines.GRID_SIZE)
        # Also watch out for the river
        y_min = max(defines.RIVER_BOTTOM_CELL * GRID_SIZE, y_min)
        x_max = min(self.village.wall.x + self.village.wall.width * GRID_SIZE, self.x + self.rect.width + defines.GRID_SIZE)
        y_max = min(self.village.wall.y + self.village.wall.height * GRID_SIZE, self.y + self.rect.height + defines.GRID_SIZE)

        pygame.draw.rect(surface, darker_color, (x_min - defines.camera_x, y_min - defines.camera_y, x_max - x_min, y_max - y_min))

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

    def get_boosted_production(self):
        """
        Returns the boosted production of the building
        """
        return {resource: amount * self.boost[0] for resource, amount in self.production.items()}

    def get_change_in_resources(self, available_resources):
        """
        Based on the available resources, calculate how the net change in resources will be next turn.
        """
        if self.disabled:
            return {}

        can_produce = all(available_resources[resource] >= amount for resource, amount in self.cost.items())
        
        if not can_produce:
            # Update self.deprived_of
            self.deprived_of = [resource for resource, amount in self.cost.items() if available_resources[resource] < amount]
            return {}
        
        change_in_resources = {}
        for resource in list(self.production.keys()) + list(self.cost.keys()):
            produce = self.production.get(resource, 0) * self.boost[0]
            change_in_resources[resource] = produce - self.cost.get(resource, 0)

        return change_in_resources

    def on_new_turn(self):
        pass

    def on_new_building(self):
        pass 
        self.boost = self.calculate_boost()

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
    
    def calculate_boost(self):
        return Building.calculate_boost_static(self.village, self.name, self.x_cell, self.y_cell)
    
    @staticmethod
    def calculate_boost_static(village, name, x_cell, y_cell):
        """
        Calculate the boost multiplier for this building
        Returns the boost multiplier and the nearest boost buildings (so lines can be drawn to them)

        return: (boost_multiplier: float, nearest_boost_buildings: List[Building])
        """

        boost_buildings = BldInfo.get_boost_buildings(name)
        if len(boost_buildings) == 0:
            return 1, []

        nearest_boost_buildings = []  # Each index corresponds to the index of the boost building in the boost_buildings list

        # Find the nearest of each boost building
        for boost_building in boost_buildings:
            nearest_building = None
            nearest_distance = float("inf")
            for building in village.buildings:
                if building.name == boost_building:
                    # manhattan distance
                    distance = abs(building.x_cell - x_cell) + abs(building.y_cell - y_cell)
                    if distance < nearest_distance:
                        nearest_distance = distance
                        nearest_building = building

            nearest_boost_buildings.append((nearest_building, nearest_distance))

        # Calculate the boost multiplier
        boost_multiplier = 1
        max_individual_boost = 0.4  # Maximum boost from a single building
        max_distance = 30
        for building, distance in nearest_boost_buildings:
            if building is not None and distance <= max_distance:
                proximity_factor = max(0, (max_distance - distance) / max_distance)
                individual_boost = proximity_factor * max_individual_boost
                boost_multiplier += individual_boost

        # Cap the total boost multiplier at 2x
        boost_multiplier = min(boost_multiplier, 2.0)

        # Extract the list of nearest boost buildings
        nearest_buildings_list = [building for building, _ in nearest_boost_buildings if building is not None]

        return boost_multiplier, nearest_buildings_list

