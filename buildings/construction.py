import pygame 
from config.defines import FONT_PATH
from config import defines 
from buildings.building_info import BldInfo

class Construction:
    """
    Class for keeping track of a building's construction progress.
    """
    def __init__(self, building):
        self.building = building
        self.turns_left = BldInfo.get_construction_time(building.name)
        self.is_being_worked_on = False

        self.font = pygame.font.Font(FONT_PATH, 20)

    def draw(self, surface: pygame.Surface):
        """
        Draws the building with extra details if it is under construction
        """
        construction_surface = pygame.Surface((self.building.rect.width, self.building.rect.height), pygame.SRCALPHA)

        # Draw the building with 50% opacity
        construction_surface.blit(self.building.image, (0, 0))
        construction_surface.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

        # Draw the construction progress
        progress_text = self.font.render(f"{self.turns_left} turns left", True, (0, 0, 0))
        construction_surface.blit(progress_text, (0, 0))

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