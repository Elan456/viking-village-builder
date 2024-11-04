"""
Defines the panel that shows when the user hovers over a building
"""
import pygame 

from .building import Building
from utils.button import Button
from config.defines import FONT_PATH
from config import defines 
from game.resources import get_icon
from config.defines import DISPLAY_HEIGHT, DISPLAY_WIDTH
from buildings.building_info import BldInfo


class BuildingHoverPanel:
    def __init__(self, village) -> None:
        self.village = village

        self.small_font = pygame.font.Font(FONT_PATH, 12)
        self.disable_button = Button(0, 0, defines.GRID_SIZE * 3, defines.GRID_SIZE, "Disable", (255, 0, 0), (0, 0, 0), self.small_font, None)
        self.enable_button = Button(0, 0, defines.GRID_SIZE * 3, defines.GRID_SIZE, "Enable", (0, 255, 255), (0, 0, 0), self.small_font, None)
        self.demolish_button = Button(0, 0, defines.GRID_SIZE * 3, defines.GRID_SIZE, "Demolish", (255, 0, 0), (0, 0, 0), self.small_font, None)

        self.font = pygame.font.Font(FONT_PATH, 16)
        

        self.panel_width = 260
        self.panel_height = 110
        self.panel_box = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        self.panel_box.fill((0, 150, 255, 180))

        self.real_building = None  # The real building that we are hovering over

    def draw(self, surface, shop_building=None):
        """
        Draws the panel on the screen
        """

        if shop_building is not None:
            building = shop_building
            in_shop = True
        else:
            if self.real_building is None:
                return
            building = self.real_building.name
            in_shop = False

        
        # Draw the panel box relative to the mouse position
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        y -= self.panel_height
        x -= self.panel_width
        x = max(x, 0)
        y = max(y, 0)
        x = min(x, DISPLAY_WIDTH - self.panel_width)
        y = min(y, DISPLAY_HEIGHT - self.panel_height)
        surface.blit(self.panel_box, (x, y))

        name_text = self.font.render(BldInfo.get_name(building), True, (0, 0, 0))
        surface.blit(name_text, (x + 10, y + 10))

        # Column text
        columns_text = self.small_font.render("Build Cost | Production | Consumption", True, (0, 0, 0))
        surface.blit(columns_text, (x + 10, y + 30))

        # Construction cost
        self.draw_resource_dict(surface, x + 5, y + 50, BldInfo.get_construction_cost(building),
                                bottom_text=f"{BldInfo.get_construction_time(building)} Turns")

        # Resource production
        self.draw_resource_dict(surface, x + 100, y + 50, BldInfo.get_production(building))

        # Resource consumption
        if BldInfo.get_cost(building):
            self.draw_resource_dict(surface, x + 200, y + 50, BldInfo.get_cost(building))

        if not in_shop:
            if self.real_building.disabled:
                self.enable_button.move(self.real_building.x, self.real_building.y)
                self.enable_button.draw(surface, defines.camera_x, defines.camera_y)
            else:
                self.disable_button.move(self.real_building.x, self.real_building.y)
                self.disable_button.draw(surface, defines.camera_x, defines.camera_y)
            self.demolish_button.move(self.real_building.x, self.real_building.y + defines.GRID_SIZE)
            self.demolish_button.draw(surface, defines.camera_x, defines.camera_y)

    def draw_resource_dict(self, surface, x, y, cost: dict, bottom_text=None):
        """
        Draws the construction cost on the screen
        
        icon: amount
        bottom_text: text to display at the bottom of the resource list
        """
        for i, resource in enumerate(cost.keys()):
            icon = get_icon(resource)
            surface.blit(icon, (x, y + i*20))
            resource_text = self.font.render(f"{cost[resource]}", True, (0, 0, 0))
            surface.blit(resource_text, (x + 24, y + i*20))

        if bottom_text:
            bottom_text = self.font.render(bottom_text, True, (0, 0, 0))
            surface.blit(bottom_text, (x, y + 20 * len(cost.keys())))


    def update(self):
        self.real_building = None
        # Check if we are hovering over a building
        for building in self.village.buildings:
            # Get true_rect adjusted for camera
            true_rect = [building.x - defines.camera_x, building.y - defines.camera_y, building.rect.width, building.rect.height]
            if pygame.Rect(true_rect).collidepoint(pygame.mouse.get_pos()):
                self.real_building = building
                break

        if self.real_building:
            if self.real_building.disabled:
                self.enable_button.update(defines.camera_x, defines.camera_y)
                self.enable_button.set_action(self.real_building.enable)
            else:
                self.disable_button.update(defines.camera_x, defines.camera_y)
                self.disable_button.set_action(self.real_building.disable)
            self.demolish_button.update(defines.camera_x, defines.camera_y)
            self.demolish_button.set_action(self.real_building.demolish)
