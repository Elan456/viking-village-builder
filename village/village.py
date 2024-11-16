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
from buildings.construction import Construction, BuilderManager
from world.world import World 
from villagers.dirt_path import DirtPath

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

        self.width_cell = defines.WORLD_WIDTH
        self.height_cell = defines.WORLD_HEIGHT

        self.building_panel = BuildingPanel(self)
        self.main_panel = MainPanel(self)
        self.random_events = RandomEventHandler(self)
        self.active_effects: List[Effect] = []  # Effects which are currently active
        self.wall = Wall(self)
        self.dirt_path = DirtPath(self)

        self.navmesh = NavMesh(self)

        self.building_demolish_queue = []
        self.world = World(self)

        self.builder_manager = BuilderManager(self)

        add_initial_buildings(self)

        self.event_handler.register_event(pygame.KEYDOWN, pygame.K_c, self.cheat_resources)

    def cheat_resources(self):
        """
        Adds a lot of resources to the village
        """
        self.resources["food"] += 1000
        self.resources["wood"] += 1000
        self.resources["ore"] += 1000
        self.resources["people"] += 1000

    
    def calculate_turn_change_resources(self) -> dict:
        """
        Goes through each building and calculates the resources it produces and consumes
        """
        change_in_resources = {}
        for building in self.buildings:
            for resource, amount in building.get_change_in_resources(self.resources).items():
                change_in_resources[resource] = change_in_resources.get(resource, 0) + amount

        return change_in_resources
        

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

        # Calculate the change in resources
        change_in_resources = self.calculate_turn_change_resources()

        # Apply the change in resources
        for resource, amount in change_in_resources.items():
            self.resources[resource] += amount

        self.builder_manager.on_new_turn()

        self.random_events.on_new_turn()

        self.world.on_new_turn()

        # Update all the villagers 100 times, to show a lot of time has passed
        for _ in range(200):
            for building in self.buildings:
                building.my_villager.update()

    def construct_building(self, building: Building):
        """
        Adds a building to the construction queue, while it is being built 
        """
        # Deduct the construction_cost
        for resource, amount in building.construction_cost.items():
            self.resources[resource] -= amount

        self.builder_manager.start_construction(building)
        self.navmesh.generate_navmesh()

    def add_building(self, building: Building):
        """
        Makes the building part of the village
        Adds the navmesh of the building to the village's navmesh
        """

        self.buildings.append(building)

        # Update the Villager's navmesh
        self.navmesh.generate_navmesh()

    def remove_building(self, building: Building):
        """
        Removes a building from the village
        """
        self.buildings.remove(building)

        # Update the Villager's navmesh
        self.navmesh.generate_navmesh()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        for building in self.buildings:
            building.update()

        self.building_panel.update(mouse_pos)
        self.main_panel.update()
        self.wall.update()


    def draw(self, surface: pygame.Surface):
        self.world.draw(surface, self.turn)
        # self.dirt_path.draw(surface)
        self.wall.draw(surface)
        for building in self.buildings:
            building.draw(surface)

        for building in self.buildings:
            building.my_villager.draw(surface)

        for construction in self.builder_manager.construction_queue:
            construction.draw(surface)

        if defines.show_navmesh:    
            self.navmesh.draw(surface)

        self.wall.upgrade_button.draw(surface)
        self.building_panel.draw(surface)
        self.main_panel.draw(surface)
        self.random_events.display(surface)

        for i in range(len(self.active_effects)):
            self.active_effects[i].draw(surface, i)