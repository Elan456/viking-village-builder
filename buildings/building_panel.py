"""
Renders and handles the building panel where buildings can be selected, dragged and placed on the map.
Shows the price of the building and what it produces when hovering over it.
"""

import pygame
from config.defines import *
from buildings.craft import BlackSmith
from buildings.raw import GrainField, LumberMill, Mine

ALL_BUILDINGS = [GrainField, Mine, LumberMill, BlackSmith]

class BuildingPanel:
    def __init__(self) -> None:
        self.buildings = []
        self.selected_building = None
        self.hovered_building = None

        self.width = GRID_SIZE * 4
        

        self.x = DISPLAY_WIDTH - self.width
        self.y = GRID_SIZE * 2
        self.height = DISPLAY_HEIGHT - self.y

        self.font = pygame.font.Font(None, 36)

        self.load_buildings()

    def load_buildings(self):
        # Populate buildings with (building, image) tuples
        for building in ALL_BUILDINGS:
            image = pygame.image.load(building.image_path)


            scale = 2*GRID_SIZE / image.get_height()
            image = pygame.transform.scale(image, (int(image.get_width() * scale), image.get_height() * scale))
            highlighted_image = image.copy()
            pygame.draw.rect(highlighted_image, (0, 255, 0), (0, 0, image.get_width(), image.get_height()), 5)

            self.buildings.append((building, image, highlighted_image))


    def update(self, mouse_pos: tuple):
        # Check if the mouse is over a building
        for i, (building, image, highlighted_image) in enumerate(self.buildings):
            if self.x < mouse_pos[0] < self.x + self.width and self.y + i * GRID_SIZE * 3 < mouse_pos[1] < self.y + (i + 1) * GRID_SIZE * 3:
                self.hovered_building = building
                break
        else:
            self.hovered_building = None
    
    def draw(self, surface: pygame.Surface):
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the background
        pygame.draw.rect(temp_surface, (0, 100, 0, 200), (0, 0, self.width, self.height))

        # Draw each building, one after the other vertically
        
        for i, building in enumerate(self.buildings):
            # Get x for centering it
            x = (self.width - building[1].get_width()) // 2
            # Check if hovered
            if self.hovered_building == building[0]:
                temp_surface.blit(building[2], (x, i * GRID_SIZE * 3))
            else:
                temp_surface.blit(building[1], (x, i * GRID_SIZE * 3))

        surface.blit(temp_surface, (self.x, self.y))
