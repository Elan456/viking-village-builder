"""
Renders and handles the building panel where buildings can be selected, dragged and placed on the map.
Shows the price of the building and what it produces when hovering over it.
"""

import pygame
from typing import List, Tuple
from config.defines import GRID_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT
from config import defines 
from buildings.craft import Blacksmith, Barrack, Shipwright
from buildings.raw import GrainField, LumberMill, Mine
from buildings.building import Building
from buildings.building_hover_panel import BuildingHoverPanel
from events.announcements import announcement_handler

ALL_BUILDINGS: List[Building] = [GrainField, Mine, LumberMill, Blacksmith, Shipwright, Barrack]

class BuildingPanel:
    def __init__(self, village) -> None:
        self.village = village
        self.buildings: List[Tuple[Building, pygame.Surface, pygame.Surface]] = []
        self.hovered_building: int = None  # Index of the hovered building
        
        self.selected_building: int = None  # Index of the selected building
        self.selected_can_be_placed = False
        self.selected_can_be_placed_msg = ""
        self.selected_cell_x = 0
        self.selected_cell_y = 0
        self.selected_width_cell = 0
        self.selected_height_cell = 0

        self.width = GRID_SIZE * 4
        

        self.x = DISPLAY_WIDTH - self.width
        self.y = GRID_SIZE * 2
        self.height = DISPLAY_HEIGHT - self.y

        self.font = pygame.font.Font(None, 36)

        self.load_buildings()

        self.building_hover_panel = BuildingHoverPanel()

    def load_buildings(self):
        # Populate buildings with (building, image) tuples
        for building in ALL_BUILDINGS:
            image = pygame.image.load(building.image_path)


            scale = 2*GRID_SIZE / image.get_height()
            image = pygame.transform.scale(image, (int(image.get_width() * scale), image.get_height() * scale))
            highlighted_image = image.copy()
            pygame.draw.rect(highlighted_image, (0, 255, 0), (0, 0, image.get_width(), image.get_height()), 5)

            self.buildings.append((building(None, 0, 0), image, highlighted_image))

    def check_selected_can_be_placed(self):
        """
        Runs all the checks to see if the selected building can be placed
        1. Check if the building is colliding with another building
        2. Check if the building is colliding with the river
        3. Check if the building is colliding with the edge of the map
        4. Check if there are enough resources
        """

        # Check if the building is colliding with another building
        if self.other_building_collision(self.selected_cell_x, self.selected_cell_y, self.selected_width_cell, self.selected_height_cell):
            return False, "Building is colliding with another building"

        # Check if the building is colliding with the river
        if self.river_collision(self.selected_cell_x, self.selected_cell_y, self.selected_width_cell, self.selected_height_cell):
            return False, "Building is colliding with the river"

        # Check if the building is colliding with the edge of the map
        if self.selected_cell_x < 0 or self.selected_cell_x + self.selected_width_cell > self.village.width_cell or self.selected_cell_y < 0 or self.selected_cell_y + self.selected_height_cell > self.village.height_cell:
            return False, "Building is colliding with the edge of the map"

        # Check if there are enough resources
        building = ALL_BUILDINGS[self.selected_building](self.village, self.selected_cell_x, self.selected_cell_y)
        for resource, amount in building.construction_cost.items():
            if self.village.resources[resource] < amount:
                return False, f"Not enough {resource}"

        return True, "Building can be placed"


    def update(self, mouse_pos: tuple):
        # Check if the mouse is over a building
        for i, (building, image, highlighted_image) in enumerate(self.buildings):
            if self.x < mouse_pos[0] < self.x + self.width and self.y + i * GRID_SIZE * 3 < mouse_pos[1] < self.y + (i + 1) * GRID_SIZE * 3:
                self.hovered_building = i
                break
        else:
            self.hovered_building = None

        # If mouse is down, then set the selected buildign to the hovered building
        if pygame.mouse.get_pressed()[0]: 
            if self.hovered_building is not None:
                self.selected_building = self.hovered_building
        else:
            if self.selected_building is not None:
                # If the mouse is up, then place the building
                if self.selected_can_be_placed:
                    self.village.add_building(ALL_BUILDINGS[self.selected_building](self.village, self.selected_cell_x, self.selected_cell_y))
                else:
                    announcement_handler.add_announcement(self.selected_can_be_placed_msg)
            self.selected_building = None

        if self.selected_building is not None:
            # Getting the dimensions of the building
            image = self.buildings[self.selected_building][1]

            # Width and height from the image // GRID_SIZE
            self.selected_width_cell = self.buildings[self.selected_building][0].get_cell_width()
            self.selected_height_cell = self.buildings[self.selected_building][0].get_cell_height()

            # Get the mouse position
            x, y = pygame.mouse.get_pos()

            # True x and y based on the camera position
            x = x + defines.camera_x - image.get_width() // 2
            y = y + defines.camera_y - image.get_height() // 2

            # Get the top left corner of the building
            self.selected_cell_x = round(x / GRID_SIZE) - 1
            self.selected_cell_y = round(y / GRID_SIZE) - 1

            # Check if the building can be placed
            self.selected_can_be_placed, self.selected_can_be_placed_msg = self.check_selected_can_be_placed()
               

    def other_building_collision(self, selected_x, selected_y, selected_width_cell, selected_height_cell):
        """
        Based on where you want to put the selected building, return true or false if it overlaps with an existing building.
        :param selected_x: x coordinate of the selected building's cell top left
        :param selected_y: y coordinate of the selected building's cell top left
        :param selected_width_cell: width of the selected building in cells
        :param selected_height_cell: height of the selected building in cells
        """

        for building in self.village.buildings:
            if building is self:
                continue

            # Check if the selected building overlaps with the building or is too close to allow for a path
            if (selected_x < building.x_cell + building.get_cell_width() + 1 and
                selected_x + selected_width_cell > building.x_cell - 1 and
                selected_y < building.y_cell + building.get_cell_height() + 1 and
                selected_y + selected_height_cell > building.y_cell - 1):
                return True
        
        return False
    
    def river_collision(self, selected_x, selected_y, selected_width_cell, selected_height_cell):
        """
        Based on where you want to put the selected building, return true or false if it overlaps with a river.
        :param selected_x: x coordinate of the selected building's cell top left
        :param selected_y: y coordinate of the selected building's cell top left
        :param selected_width_cell: width of the selected building in cells
        :param selected_height_cell: height of the selected building in cells
        """

        river_min_y_cell = self.village.river_top_cell
        river_max_y_cell = river_min_y_cell + self.village.river_width_cells

        # If the y of the building overlaps with the river, then return true
        if (selected_y < river_max_y_cell and
            selected_y + selected_height_cell > river_min_y_cell):
            return True

    
    def draw(self, surface: pygame.Surface):
        # Draw onto the main surface, a green or red outline of where the building will be placed
        if self.selected_building is not None:

            color = (0, 255, 0) if self.selected_can_be_placed else (255, 0, 0)

            # Draw the building
            pygame.draw.rect(surface, color,
                              (self.selected_cell_x * GRID_SIZE - defines.camera_x, self.selected_cell_y * GRID_SIZE - defines.camera_y,
                                self.selected_width_cell * GRID_SIZE, self.selected_height_cell * GRID_SIZE), 5)


        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the background
        pygame.draw.rect(temp_surface, (0, 100, 0, 200), (0, 0, self.width, self.height))

        # Draw each building, one after the other vertically
        
        for i, building in enumerate(self.buildings):
            # Get x for centering it
            x = (self.width - building[1].get_width()) // 2
            # Check if hovered
            if self.hovered_building == i:
                temp_surface.blit(building[2], (x, i * GRID_SIZE * 3))
            else:
                temp_surface.blit(building[1], (x, i * GRID_SIZE * 3))

        surface.blit(temp_surface, (self.x, self.y))

        # Draw the selected building centered on the mouse
        if self.selected_building is not None:
            _, image, _ = self.buildings[self.selected_building]
            x, y = pygame.mouse.get_pos()
            x -= image.get_width() // 2
            y -= image.get_height() // 2
            surface.blit(image, (x, y))

        # If a building is being hovered on, then draw the hover panel
        if self.hovered_building is not None:
            building = self.buildings[self.hovered_building][0]
            self.building_hover_panel.draw(surface, building, in_shop=True)