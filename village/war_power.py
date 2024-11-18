import pygame 
from config import defines
from config.defines import GRID_SIZE, FONT_PATH
import math 
import random

def load_warrior_images():
    viking_sheet = pygame.image.load("assets/warrior/Viking-Sheet.png")
    warrior_images = []
    for i in range(8):
        image = pygame.surface.Surface((48, 48), pygame.SRCALPHA)
        image.blit(viking_sheet, (0, 0), (32 + i * 115, 25, 48, 48))
        image = pygame.transform.scale(image, (GRID_SIZE * 1.5, GRID_SIZE * 1.5))
        warrior_images.append(image)

    return warrior_images


class WarPower:
    """
    Handles drawing and updating the boats and soldiers in the river
    """
    
    ship_image = pygame.image.load("assets/warrior/ship.png")
    ship_image = pygame.transform.scale(ship_image, (GRID_SIZE * 3, GRID_SIZE * 3))

    viking_sheet = pygame.image.load("assets/warrior/Viking-Sheet.png")

    warrior_images = load_warrior_images()
    warrior_image_width = warrior_images[0].get_width()

    warrior_spacing = warrior_image_width * .7

    SWAY_DURATION = 40
    SWAY_MAGNITUDE = 30

    def __init__(self, village):
        self.village = village

        self.draw_tick = 0

        # Tick offsets
        self.tick_offsets = [random.randint(0, 100) for _ in range(300)]

        self.font = pygame.font.Font(FONT_PATH, 48)

    @staticmethod
    def sway_function(x):
        return WarPower.SWAY_MAGNITUDE * (1 + math.sin(x / WarPower.SWAY_DURATION))
    
    def draw(self, surface):
        self.draw_tick += 1
        self.draw_tick %= int(WarPower.SWAY_DURATION * math.pi * 2)

        start_x = self.village.wall.x + GRID_SIZE
        start_y = defines.RIVER_TOP_CELL * GRID_SIZE

        boat_spacing = GRID_SIZE * 3

        num_boats = int(self.village.resources["ships"])
        num_soldiers = int(self.village.resources["warriors"])

        for i in range(num_boats):
            sway = WarPower.sway_function(self.draw_tick + i * 10)
            surface.blit(WarPower.ship_image, (start_x - defines.camera_x + i * boat_spacing + sway, start_y - defines.camera_y))

        max_num_soldiers_width = int((self.village.wall.width * GRID_SIZE) / (WarPower.warrior_spacing) - 2)
        max_num_soldiers_width = 50

        start_y = self.village.wall.y - GRID_SIZE * 5
        # To center
        army_width = max_num_soldiers_width * WarPower.warrior_spacing

        start_x = self.village.wall.x + (self.village.wall.width * GRID_SIZE - army_width) / 2

        # Draw a box outline showing where the soldiers will be drawn
        pygame.draw.rect(surface, (100, 100, 100), (start_x - defines.camera_x, start_y - defines.camera_y + GRID_SIZE - GRID_SIZE * (250 // max_num_soldiers_width), max_num_soldiers_width * WarPower.warrior_spacing,
                                            GRID_SIZE * (250 // max_num_soldiers_width + 1)), 3)

        # Draw the soldiers in neat rows along the bottom of the river
        for i in range(num_soldiers):
            rank = i // max_num_soldiers_width
            x = start_x + (i % max_num_soldiers_width) * WarPower.warrior_spacing
            y = start_y + (GRID_SIZE * 1) - GRID_SIZE * 1.0 * (1 + rank)

            my_tick = (self.draw_tick + self.tick_offsets[i % 300]) // 8
            surface.blit(WarPower.warrior_images[my_tick % 8], (x - defines.camera_x, y - defines.camera_y))

        if self.village.turn >= 100:
            self.draw_end_game(surface)

    def draw_end_game(self, surface):
        end_game_surface = pygame.Surface((defines.DISPLAY_WIDTH, defines.DISPLAY_HEIGHT), pygame.SRCALPHA)
        end_game_surface.fill((255, 255, 255, 50))
        surface.blit(end_game_surface, (0, 0))

        won = self.village.resources["warriors"] >= 250 and self.village.resources["ships"] >= 10
        if won:
            text = "You have won!"
        else:
            text = "You have lost!"

        text = self.font.render(text, True, (0, 0, 0))
        surface.blit(text, (defines.DISPLAY_WIDTH // 2 - text.get_width() // 2, defines.DISPLAY_HEIGHT // 2 - text.get_height() // 2 - 100))
        warrior_count = int(self.village.resources["warriors"])
        ship_count = int(self.village.resources["ships"])
        stats = {
            "Warriors": f"{warrior_count}/250",
            "Ships": f"{ship_count}/10",
            "Buildings": len(self.village.buildings),
        }

        for i, (key, value) in enumerate(stats.items()):
            text = self.font.render(f"{key}: {value}", True, (0, 0, 0))
            surface.blit(text, (defines.DISPLAY_WIDTH // 2 - text.get_width() // 2, defines.DISPLAY_HEIGHT // 2 - text.get_height() // 2 + (i + 1) * 70))