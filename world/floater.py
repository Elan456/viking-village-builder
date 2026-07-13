import pygame
import random

from config import defines


class Floater:
    IMAGE_PATHS = [
        "assets/nature/01_Birch_Branch.png",
        "assets/nature/02_Birch_Branch_Leaf.png",
        "assets/nature/05_Birch_Seed.png",
        "assets/nature/06_Oak_Branch.png",
        "assets/nature/07_Oak_Branch_Leaf.png",
        "assets/nature/10_Oak_Seed.png",
    ]

    SCALED_IMAGES = {}

    def __init__(self):
        self.x = -defines.DISPLAY_WIDTH + random.uniform(-defines.GRID_SIZE, defines.GRID_SIZE)
        self.speed = random.uniform(0.8, 1.3)
        self.age = 0
        self.alpha = 128
        image_name = random.choice(self.IMAGE_PATHS)

        if image_name not in self.SCALED_IMAGES:
            image = pygame.image.load(image_name)
            if "Seed" in image_name:
                image = pygame.transform.scale(image, (20, 20))
            elif "Branch" in image_name:
                image = pygame.transform.scale(image, (40, 40))
            elif "Leaf" in image_name:
                image = pygame.transform.scale(image, (60, 60))
            try:
                image = image.convert_alpha()
            except pygame.error:
                pass
            self.SCALED_IMAGES[image_name] = image

        # Independent alpha per floater without reallocating each frame
        self.image = self.SCALED_IMAGES[image_name].copy()
        self.image.set_alpha(self.alpha)

        river_min_y = defines.RIVER_TOP_CELL * defines.GRID_SIZE
        river_max_y = defines.RIVER_BOTTOM_CELL * defines.GRID_SIZE
        self.y = random.uniform(river_min_y, river_max_y - self.image.get_height())

    def update(self):
        self.x += self.speed
        self.age += 1
        new_alpha = min(255, self.alpha + 5)
        if new_alpha != self.alpha:
            self.alpha = new_alpha
            self.image.set_alpha(self.alpha)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x - defines.camera_x, self.y - defines.camera_y))
