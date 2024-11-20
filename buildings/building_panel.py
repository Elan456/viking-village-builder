"""
Renders and handles the building panel where buildings can be selected, dragged and placed on the map.
Shows the price of the building and what it produces when hovering over it.
"""

import pygame
from typing import List, Tuple
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT
from config import defines 
from buildings.building_info import BldInfo
from buildings.building import Building
from buildings.building_hover_panel import BuildingHoverPanel
from events.announcements import announcement_handler

ALL_BUILDINGS: List[str] = BldInfo.get_all_keys()

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
        self.selected_boost = None

        self.width = defines.GRID_SIZE * 4
        

        self.x = DISPLAY_WIDTH - self.width

        self.y = defines.GRID_SIZE * 2
        self.height = DISPLAY_HEIGHT - self.y

        self.font = pygame.font.Font(defines.FONT_PATH, 36)

        self.load_buildings()

        self.building_hover_panel = BuildingHoverPanel(self.village) 
        self.mouse_pos = (0, 0)

        # Ensures that the a building is selected only when the mouse clicks
        self.village.event_handler.register_mouse_click(self.on_mouse_click)

    def load_buildings(self):
        # Populate buildings with (building, image) tuples
        for building in ALL_BUILDINGS:
            image = pygame.image.load(BldInfo.get_icon_path(building))


            scale = 3*defines.GRID_SIZE / image.get_height()
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            highlighted_image = image.copy()
            pygame.draw.rect(highlighted_image, (0, 255, 0), (0, 0, image.get_width(), image.get_height()), 5)

            # Can't afford image
            not_afford_image = image.copy()
            pygame.draw.rect(not_afford_image, (100, 0, 0), (0, 0, image.get_width(), image.get_height()), 5)


            self.buildings.append((building, image, highlighted_image, not_afford_image))

    def is_enough_resources(self, building: str):
        """
        Check if there are enough resources to build the building
        """
        for resource, amount in BldInfo.get_construction_cost(building).items():
            if self.village.resources[resource] < amount:
                return False
        return True

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
        #  if self.selected_cell_x < 0 or self.selected_cell_x + self.selected_width_cell > self.village.width_cell or self.selected_cell_y < 0 or self.selected_cell_y + self.selected_height_cell > self.village.height_cell:
         #   return False, "Building is colliding with the edge of the map"

        # Check if the building collides with the wall
        if not self.village.wall.can_build(self.selected_cell_x, self.selected_cell_y, self.selected_width_cell, self.selected_height_cell):
            return False, "Building is outside the wall"

        if ALL_BUILDINGS[self.selected_building] == "shipyard" and not self.check_along_river(self.selected_cell_x, self.selected_cell_y, self.selected_width_cell, self.selected_height_cell):
            return False, "Shipyard must be placed along the river"
        
        # Check if there are enough resources
        building = ALL_BUILDINGS[self.selected_building]
        if not self.is_enough_resources(building):
            return False, "Not enough resources to build the building"

        return True, "Building can be placed"
    

    def on_mouse_click(self, event):
        """
        Called whenever a mouse down event is detected.
        """
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Based on the location of the mouse try to set a building as selected
            if self.hovered_building is not None:
                self.selected_building = self.hovered_building

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # If the mouse is up, then place the building
            if self.selected_building is not None:
                if self.selected_can_be_placed:
                    self.village.construct_building(Building(self.village, self.selected_cell_x, self.selected_cell_y, ALL_BUILDINGS[self.selected_building]))
                else:
                    announcement_handler.add_announcement(self.selected_can_be_placed_msg)
            self.selected_building = None


    def update(self, mouse_pos: tuple):
        self.mouse_pos = mouse_pos

        self.building_hover_panel.update()

        # Check if the mouse is over a building
        for i, (building, image, highlighted_image, _) in enumerate(self.buildings):
            if self.x < mouse_pos[0] < self.x + self.width and self.y + i * defines.GRID_SIZE * 4 < mouse_pos[1] < self.y + (i + 1) * defines.GRID_SIZE * 4:
                self.hovered_building = i
                break
        else:
            self.hovered_building = None

        if self.selected_building is not None:
            # Getting the dimensions of the building
            image = self.buildings[self.selected_building][1]

            # Width and height from the image // GRID_SIZE
            self.selected_width_cell = BldInfo.get_width(self.buildings[self.selected_building][0])
            self.selected_height_cell = BldInfo.get_height(self.buildings[self.selected_building][0])

            # Get the mouse position
            x, y = pygame.mouse.get_pos()

            # True x and y based on the camera position
            x = x + defines.camera_x - image.get_width() // 2
            y = y + defines.camera_y - image.get_height() // 2

            # Get the top left corner of the building
            self.selected_cell_x = round(x / defines.GRID_SIZE) - 1
            self.selected_cell_y = round(y / defines.GRID_SIZE) - 1

            # Check if the building can be placed
            self.selected_can_be_placed, self.selected_can_be_placed_msg = self.check_selected_can_be_placed()

            # Calculate the boost of the building
            self.selected_boost = Building.calculate_boost_static(self.village, self.buildings[self.selected_building][0], self.selected_cell_x, self.selected_cell_y)
               

    def other_building_collision(self, selected_x, selected_y, selected_width_cell, selected_height_cell):
        """
        Based on where you want to put the selected building, return true or false if it overlaps with an existing building.
        :param selected_x: x coordinate of the selected building's cell top left
        :param selected_y: y coordinate of the selected building's cell top left
        :param selected_width_cell: width of the selected building in cells
        :param selected_height_cell: height of the selected building in cells
        """

        for building in self.village.buildings + [c.building for c in self.village.builder_manager.construction_queue]:
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

        river_min_y_cell = defines.RIVER_TOP_CELL
        river_max_y_cell = defines.RIVER_BOTTOM_CELL

        # If the y of the building overlaps with the river, then return true
        if (selected_y < river_max_y_cell and
            selected_y + selected_height_cell > river_min_y_cell):
            return True

    def check_along_river(self, selected_x, selected_y, selected_width_cell, selected_height_cell):
        """
        Returns true if the building is along the river i.e. the building is touching the river.
        """

        river_min_y_cell = defines.RIVER_TOP_CELL
        river_max_y_cell = defines.RIVER_BOTTOM_CELL

        # If the building is touching the river, then return true
        if (selected_y == river_max_y_cell or
            selected_y + selected_height_cell == river_min_y_cell):
            return True

        return False

    
    def draw(self, surface: pygame.Surface):
        # Draw onto the main surface, a green or red outline of where the building will be placed
        if self.selected_building is not None:

            self.village.world.draw_grid(surface)
            for building in self.village.buildings:
                building.draw_outline(surface)

            color = (0, 255, 0) if self.selected_can_be_placed else (255, 0, 0)

            # Draw the building
            pygame.draw.rect(surface, color,
                              (self.selected_cell_x * defines.GRID_SIZE - defines.camera_x, self.selected_cell_y * defines.GRID_SIZE - defines.camera_y,
                                self.selected_width_cell * defines.GRID_SIZE, self.selected_height_cell * defines.GRID_SIZE), 5)


        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the background
        pygame.draw.rect(temp_surface, (50, 50, 50, 200), (0, 0, self.width, self.height))

        # Draw each building, one after the other vertically
        
        for i, building in enumerate(self.buildings):
            # Get x for centering it
            x = (self.width - building[1].get_width()) // 2
            # Check if hovered
            if self.hovered_building == i:
                temp_surface.blit(building[2], (x, i * defines.GRID_SIZE * 4))
            else:
                if not self.is_enough_resources(building[0]):
                    temp_surface.blit(building[3], (x, i * defines.GRID_SIZE * 4))
                else:
                    temp_surface.blit(building[1], (x, i * defines.GRID_SIZE * 4))

        surface.blit(temp_surface, (self.x, self.y))

        # Draw the selected building centered on the mouse
        if self.selected_building is not None:
            _, image, _, _ = self.buildings[self.selected_building]
            x, y = pygame.mouse.get_pos()
            x -= image.get_width() // 2
            y -= image.get_height() // 2
            surface.blit(image, (x, y))

            # Draw the boost of the building
            if self.selected_boost is not None and len(self.selected_boost[1]) > 0:
                boost, boost_builings = self.selected_boost
                for i, building in enumerate(boost_builings):
                    # Draw a blue line to the building
                    pygame.draw.line(surface, (0, 0, 255), (x + image.get_width() // 2, y + image.get_height() + 30), (building.x_cell * defines.GRID_SIZE - defines.camera_x + building.get_cell_width() * defines.GRID_SIZE // 2, building.y_cell * defines.GRID_SIZE - defines.camera_y + building.get_cell_height() * defines.GRID_SIZE // 2), 5)


                # Rectangle behind to improve contrast
                boost_text_width = 220
                boost_text_surface = pygame.Surface((boost_text_width, 50), pygame.SRCALPHA)
                pygame.draw.rect(boost_text_surface, (255, 255, 255, 100), (0, 0, boost_text_width, 50))
                boost_text = self.font.render(f"Boost: {boost:.2f}", True, (0, 50, 200))
                boost_text_surface.blit(boost_text, (10, 10))
                surface.blit(boost_text_surface, (x + image.get_width() // 2 - 100, y + image.get_height() + 30))

                
        # If a building is being hovered on, then draw the hover panel
        if self.hovered_building is not None:
            building = self.buildings[self.hovered_building][0]
            self.building_hover_panel.draw(surface, building)
        else:
            self.building_hover_panel.draw(surface)