"""
Defines the panel that shows when the user hovers over a building
"""
import pygame 

from .building import Building
from .craft import CraftBuilding
from .raw import RawBuilding
from utils.button import Button
from config.defines import FONT_PATH
from game.resources import get_icon
from config.defines import DISPLAY_HEIGHT, DISPLAY_WIDTH


class BuildingHoverPanel:
    def __init__(self) -> None:
        self.disable_button = Button(0, 0, 50, 50, "X", (255, 0, 0), (0, 0, 0), None, None)
        self.demolish_button = Button(0, 0, 50, 50, "Demolish", (255, 0, 0), (0, 0, 0), None, None)

        self.font = pygame.font.Font(FONT_PATH, 16)
        self.small_font = pygame.font.Font(FONT_PATH, 12)

        self.panel_width = 260
        self.panel_height = 200
        self.panel_box = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)
        self.panel_box.fill((0, 150, 255, 180))

    def draw(self, surface, building: Building, in_shop=False):
        """
        Draws the panel on the screen
        """
        mouse_pos = pygame.mouse.get_pos()

        # Draw the panel box relative to the mouse position
        x, y = mouse_pos
        y -= self.panel_height
        x -= self.panel_width
        x = max(x, 0)
        y = max(y, 0)
        x = min(x, DISPLAY_WIDTH - self.panel_width)
        y = min(y, DISPLAY_HEIGHT - self.panel_height)
        surface.blit(self.panel_box, (x, y))

        # Building name
        name_text = self.font.render(building.name, True, (0, 0, 0))
        surface.blit(name_text, (x + 10, y + 10))

        # Column text
        columns_text = self.small_font.render("Build Cost | Production | Consumption", True, (0, 0, 0))
        surface.blit(columns_text, (x + 10, y + 30))

        # Construction cost
        self.draw_resource_dict(surface, x + 5, y + 50, building.construction_cost)

        # Resource production
        self.draw_resource_dict(surface, x + 100, y + 50, building.production)

        # Resource consumption
        if isinstance(building, CraftBuilding):
            self.draw_resource_dict(surface, x + 200, y + 50, building.cost)

        if not in_shop:
            self.disable_button.rect.topleft = (building.x + 50, building.y)
            self.disable_button.draw(surface)
            self.demolish_button.rect.topleft = (building.x + 50, building.y)
            self.demolish_button.draw(surface)

    def draw_resource_dict(self, surface, x, y, cost: dict):
        """
        Draws the construction cost on the screen
        
        icon: amount
        """
        for i, resource in enumerate(cost.keys()):
            icon = get_icon(resource)
            surface.blit(icon, (x, y + i*20))
            resource_text = self.font.render(f"{cost[resource]}", True, (0, 0, 0))
            surface.blit(resource_text, (x + 24, y + i*20))


    def update(self):
        pass
