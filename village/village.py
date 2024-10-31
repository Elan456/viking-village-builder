import pygame 
from typing import List
from config.defines import DISPLAY_HEIGHT, DISPLAY_WIDTH, GRID_SIZE, camera_x, camera_y, show_navmesh
import config.defines as defines 
from buildings.building_panel import BuildingPanel
from buildings.building import Building
from game.main_panel import MainPanel
from events.random_event_handler import RandomEventHandler
from effects.effect import Effect
from villagers.navmesh import NavMesh
from game.initial_village import add_initial_buildings
from village.wall import Wall
from buildings.construction import Construction

class Village:
    """
    Handles the village's rendering and updating.
    """
    def __init__(self, event_handler) -> None:
        self.event_handler = event_handler

        self.buildings: List[Building] = []
        self.turn = 0
        self.resources = {"food": 100, "wood": 100, "ore": 100, "people": 0, "weapons": 0, "warriors": 0, "ships": 0}
        self.production_multipliers = {"food": 1, "wood": 1, "ore": 1, "people": 1, "weapons": 1, "warriors": 1, "ships": 1}

        self.river_top_cell = 3
        self.river_width_cells = 3

        self.width_cell = defines.WORLD_WIDTH
        self.height_cell = defines.WORLD_HEIGHT

        self.building_panel = BuildingPanel(self)
        self.main_panel = MainPanel(self)
        self.random_events = RandomEventHandler(self)
        self.active_effects: List[Effect] = []  # Effects which are currently active

        self.navmesh = NavMesh(self)

        self.building_demolish_queue = []
        self.building_construction_queue: List[Construction] = []

        self.wall = Wall(self)

        add_initial_buildings(self)

    def on_new_turn(self):
        """
        Called when a new turn occurs
        """
        self.turn += 1 
        # Setting the production multipliers to 1 again
        # The random events can then change them 
        self.production_multipliers = {"food": 1, "wood": 1, "ore": 1, "people": 1, "weapons": 1, "warriors": 1, "ships": 1}
        
        # Apply all active effects to get the new production multipliers
        self.active_effects = [effect for effect in self.active_effects if effect.duration > 0]
        for effect in self.active_effects:
            effect.apply(self)
            # Reduce the duration of all effects
            effect.duration -= 1

        # Call the on_new_turn method of all buildings
        for building in self.buildings:
            building.on_new_turn()

        for construction in self.building_construction_queue:
            construction.on_new_turn()

        self.random_events.on_new_turn()

    def construct_building(self, building: Building):
        """
        Adds a building to the construction queue, while it is being built 
        """
        # Deduct the construction_cost
        for resource, amount in building.construction_cost.items():
            self.resources[resource] -= amount

        self.building_construction_queue.append(Construction(building))

    def add_building(self, building: Building):
        """
        Makes the building part of the village
        Adds the navmesh of the building to the village's navmesh
        """

        self.buildings.append(building)

        # Update the Villager's navmesh
        self.navmesh.generate_navmesh()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        for building in self.buildings:
            building.update()

        self.building_panel.update(mouse_pos)
        self.main_panel.update()
        self.wall.update()



    def draw_background(self, surface: pygame.Surface):
        pygame.draw.rect(surface, defines.GRASS_GREEN, (0 - camera_x, 0 - camera_y, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        # river
        pygame.draw.rect(surface, (0, 0, 255), (0, self.river_top_cell * GRID_SIZE - defines.camera_y, DISPLAY_WIDTH, self.river_width_cells * GRID_SIZE))

        # Draw a grid
        # for x in range(0, defines.WORLD_WIDTH * GRID_SIZE + GRID_SIZE, GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (x - defines.camera_x, 0 - defines.camera_y), (x - defines.camera_x, defines.WORLD_HEIGHT * GRID_SIZE - defines.camera_y))
        # for y in range(0, defines.WORLD_HEIGHT * GRID_SIZE + GRID_SIZE, GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (0 - defines.camera_x, y - defines.camera_y), (defines.WORLD_WIDTH * GRID_SIZE - defines.camera_x, y - defines.camera_y))
    
    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)
        self.wall.draw(surface)
        for building in self.buildings:
            building.draw(surface)

        for building in self.buildings:
            building.my_villager.draw(surface)

        for construction in self.building_construction_queue:
            construction.draw(surface)

        if defines.show_navmesh:    
            self.navmesh.draw(surface)

        self.building_panel.draw(surface)
        self.main_panel.draw(surface)
        self.random_events.display(surface)

        for i in range(len(self.active_effects)):
            self.active_effects[i].draw(surface, i)