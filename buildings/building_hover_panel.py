"""
Defines the panel that shows when the user hovers over a building
"""
import pygame 

from utils.button import Button
from utils.style_button import StyleButton
from assets.ui.button_mapping import RED_EXIT, GREEN_PLAY, RED_PAUSE, BLUE_PLAY
from config.defines import FONT_PATH
from config import defines 
from game.resources import get_icon
from config.defines import DISPLAY_HEIGHT, DISPLAY_WIDTH
from buildings.building_info import BldInfo


class BuildingHoverPanel:
    def __init__(self, village) -> None:
        self.village = village

        self.small_font = pygame.font.Font(FONT_PATH, 12)

        self.button_size = defines.GRID_SIZE * 2

        self.disable_button = StyleButton(0, 0, self.button_size, self.button_size, RED_PAUSE, None, hover_text="Disable")
        self.enable_button = StyleButton(0, 0, self.button_size, self.button_size, BLUE_PLAY, None, hover_text="Enable")
        self.demolish_button = StyleButton(0, 0, self.button_size, self.button_size, RED_EXIT, None, hover_text="Demolish")

        self.font = pygame.font.Font(FONT_PATH, 16)
        

        self.panel_width = 340
        self.panel_height = 140
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

        if not in_shop:
            br_x = self.real_building.x + self.real_building.rect.width
            br_y = self.real_building.y + self.real_building.rect.height

            if self.real_building.disabled:
                self.enable_button.move(br_x - self.button_size, br_y - self.button_size)
                self.enable_button.draw(surface, defines.camera_x, defines.camera_y)
            else:
                self.disable_button.move(br_x - self.button_size, br_y - self.button_size)
                self.disable_button.draw(surface, defines.camera_x, defines.camera_y)
            self.demolish_button.move(br_x - self.button_size * 2, br_y - self.button_size)
            self.demolish_button.draw(surface, defines.camera_x, defines.camera_y)
            
        # Draw the panel box relative to the mouse position
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        y -= self.panel_height
        x -= self.panel_width
        x = max(x, 0)
        y = max(y, 0)
        x = min(x, DISPLAY_WIDTH - self.panel_width)
        y = min(y, DISPLAY_HEIGHT - self.panel_height)

        if not in_shop:
            boost, boost_buildings = self.real_building.calculate_boost()

            # Draw lines to the buildings that are boosting this building
            for i, bb in enumerate(boost_buildings):
                pygame.draw.line(surface, (0, 0, 255), (x + self.panel_width - 10, y + self.panel_height - 10), (bb.x - defines.camera_x + bb.rect.width // 2, bb.y - defines.camera_y + bb.rect.height // 2), 5)


        surface.blit(self.panel_box, (x, y))

        name_text = self.font.render(BldInfo.get_name(building), True, (0, 0, 0))
        surface.blit(name_text, (x + 10, y + 10))

        description_text = self.font.render(BldInfo.get_description(building), True, (0, 0, 0))
        surface.blit(description_text, (x + 10, y + 30))

        # Column text
        columns_text = self.small_font.render("Build Cost | Production | Consumption", True, (0, 0, 0))
        surface.blit(columns_text, (x + 10, y + 50))

        # Construction cost
        self.draw_resource_dict(surface, x + 5, y + 70, BldInfo.get_construction_cost(building),
                                bottom_text=f"{BldInfo.get_construction_time(building)} Turns")

        # Resource production
        if not in_shop:
            production = self.real_building.get_boosted_production()
        else:
            production = BldInfo.get_production(building)
        self.draw_resource_dict(surface, x + 100, y + 70, production)

        # Resource consumption
        if BldInfo.get_cost(building):
            self.draw_resource_dict(surface, x + 200, y + 70, BldInfo.get_cost(building))

        if not in_shop:
            boost_text = self.font.render(f"Boost: {round(boost,2)}x", True, (0, 0, 0))
            surface.blit(boost_text, (x + self.panel_width - boost_text.get_width() - 10, y + self.panel_height - boost_text.get_height() - 10))

        if self.village.building_panel.help:
            # Add some explanation text off to the side
            help_text = [
                "This panel shows the details of the",
                "building you are hovering over.",
                "You can disable, enable, or demolish",
                "the building. The blue lines show which ",
                "buildings are boosting this building.",
                "Disable a building to conserve the resource",
                "it consumes, so you can use it elsewhere.",
                "Demolish a building to make space for another", 
                "when wall upgrades get expensive."
            ]

            # Draw a background for the help text
            box_height = (len(help_text) + 1) * (defines.HELP_FONT.get_height() + 3)
            box_width = max([defines.HELP_FONT.size(line)[0] for line in help_text]) + 10

            help_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            help_box.fill((0, 0, 0, 180))
            surface.blit(help_box, (x - box_width // 3, y + self.panel_height))

            for i, line in enumerate(help_text):
                text = defines.HELP_FONT.render(line, True, defines.HELP_COLOR)
                surface.blit(text, (x - box_width // 3, y + self.panel_height + i*(text.get_height() + 3)))


        

    def draw_resource_dict(self, surface, x, y, cost: dict, bottom_text=None):
        """
        Draws the construction cost on the screen
        
        icon: amount
        bottom_text: text to display at the bottom of the resource list
        """
        for i, resource in enumerate(cost.keys()):
            icon = get_icon(resource)
            surface.blit(icon, (x, y + i*20))
            resource_text = self.font.render(f"{round(cost[resource], 2)}", True, (0, 0, 0))
            surface.blit(resource_text, (x + 24, y + i*20))

        if bottom_text:
            bottom_text = self.font.render(bottom_text, True, (0, 0, 0))
            surface.blit(bottom_text, (x, y + 22 * len(cost.keys())))


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
