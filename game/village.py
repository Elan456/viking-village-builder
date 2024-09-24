import pygame 
from config.defines import *
import config.defines as defines 
from buildings.building_panel import BuildingPanel
from events.random_event_handler import RandomEventHandler

class Village:
    """
    Handles the village's rendering and updating.
    """
    def __init__(self) -> None:
        self.buildings = []
        self.resources = {"food": 0, "wood": 0, "ore": 0, "people": 0, "weapons": 0}
        self.production_multipliers = {"food": 1, "wood": 1, "ore": 1, "people": 1, "weapons": 1}

        self.river_top = RIVER_HEIGHT
        self.building_panel = BuildingPanel()
        self.random_events = RandomEventHandler(self)
        self.active_effects = []  # Effects which are currently active

    def add_building(self, building):
        self.buildings.append(building)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        for building in self.buildings:
            building.update()

        self.building_panel.update(mouse_pos)

        # Setting the production multipliers to 1 again
        # The random events can then change them 
        self.production_multipliers = {"food": 1, "wood": 1, "ore": 1, "people": 1, "weapons": 1}
        self.random_events.update() 

    def draw_background(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (0, 150, 0), (0 - camera_x, 0 - camera_y, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        # river
        pygame.draw.rect(surface, (0, 0, 255), (0, self.river_top - defines.camera_y, DISPLAY_WIDTH, RIVER_HEIGHT))

        # Draw a grid
        for x in range(0, DISPLAY_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, (0, 0, 0), (x - defines.camera_x, 0 - defines.camera_y), (x - defines.camera_x, DISPLAY_HEIGHT - defines.camera_y))
        for y in range(0, DISPLAY_HEIGHT + GRID_SIZE, GRID_SIZE):
            pygame.draw.line(surface, (0, 0, 0), (0 - defines.camera_x, y - defines.camera_y), (DISPLAY_WIDTH - defines.camera_x, y - defines.camera_y))
    
    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)
        for building in self.buildings:
            building.draw(surface)

        self.building_panel.draw(surface)
        self.random_events.display(surface)