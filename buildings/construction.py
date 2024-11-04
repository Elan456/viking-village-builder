import pygame 
from config.defines import FONT_PATH
from config import defines 
from buildings.building_info import BldInfo
from utils import utils 
from typing import List
from typing import Dict, List

class Construction:
    """
    Class for keeping track of a building's construction progress.
    """
    def __init__(self, building):
        self.building = building
        self.turns_left = BldInfo.get_construction_time(building.name)
        self.is_being_worked_on = False

        self.font = pygame.font.Font(FONT_PATH, 30)

    def draw(self, surface: pygame.Surface):
        """
        Draws the building with extra details if it is under construction
        """
        construction_surface = pygame.Surface((self.building.rect.width, self.building.rect.height), pygame.SRCALPHA)

        # Draw the building with 50% opacity
        construction_surface.blit(self.building.image, (0, 0))
        construction_surface.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

        # Draw the construction progress (just the number)
        text = self.font.render(str(self.turns_left), True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.building.rect.width // 2, self.building.rect.height // 2))
        construction_surface.blit(text, text_rect)

        # Draw brown rectangle around the building if it's being worked on
        if self.is_being_worked_on:
            pygame.draw.rect(construction_surface, (150, 75, 0), (0, 0, self.building.rect.width, self.building.rect.height), 5)

        # Blit the construction surface to the main surface
        surface.blit(construction_surface, (self.building.x - defines.camera_x, self.building.y - defines.camera_y))

    def on_new_turn(self):
        """
        Called when a new turn occurs
        """
        if self.is_being_worked_on:
            self.turns_left -= 1

    def is_finished(self):
        """
        Returns if the construction is finished
        """
        return self.turns_left <= 0
    
class BuilderManager:
    """
    A class that the village uses to manage the builders
    - Keep the builders assigned to construction jobs 
    - Keep track of the builders' progress
    """

    def __init__(self, village):
        self.village = village
        self.construction_queue: List[Construction] = [] 

    def start_construction(self, building):
        """
        Adds a building to the construction queue
        """
        self.construction_queue.append(Construction(building))
        self.handle_assignments()

    def is_builder_assigned(self, builders, construction: Construction):
        """
        Returns if the builder is already assigned to the construction job
        """
        for builder in builders:
            if builder.construction_target == construction:
                return True
        return False
    
    def handle_assignments(self):
        current_builders = []
        for building in self.village.buildings:
            if building.villager_name == "builder":
                current_builders.append(building.my_villager)

        # Ensure that none of the builders are assigned to a construction job that is already finished
        for builder in current_builders:
            if builder.construction_target is not None and builder.construction_target.is_finished():
                builder.construction_target = None

        # Going in order of the queue, check if a builder is already assigned to it,
        # if not, then assign an avaible builder
        # continue until all builders are assigned
        for construction in self.construction_queue:
            # Check if a builder has it set as it's target
            if not self.is_builder_assigned(current_builders, construction):
                construction.is_being_worked_on = False
                for builder in current_builders:
                    if builder.construction_target is None:
                        builder.construction_target = construction
                        construction.is_being_worked_on = True
                        break


    def on_new_turn(self):
        """
        Recompiles a list of available builders
        Decrements all construction jobs being worked on by one 
        """
        self.handle_assignments()
        for construction in self.construction_queue:
            construction.on_new_turn()

            if construction.is_finished():
                self.village.add_building(construction.building)
                self.handle_assignments()  # Reassign builders

        # Remove all finished constructions
        self.construction_queue = [construction for construction in self.construction_queue if not construction.is_finished()]