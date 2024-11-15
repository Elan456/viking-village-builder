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
        self.speed = random.uniform(.8, 1.3)
        self.age = 0
        self.alpha = 0
        image_name = random.choice(self.IMAGE_PATHS)
        
        # Create a scaled image if it doesn't exist
        if image_name not in self.SCALED_IMAGES:
            image = pygame.image.load(image_name)
            if "Seed" in image_name:
                image = pygame.transform.scale(image, (20, 20))
            elif "Branch" in image_name:
                image = pygame.transform.scale(image, (40, 40))
            elif "Leaf" in image_name:
                image = pygame.transform.scale(image, (60, 60))
            self.SCALED_IMAGES[image_name] = image

        self.image = self.SCALED_IMAGES[image_name]

        # Determine the y value based on the river's position and the floater's image height
        river_min_x = defines.RIVER_TOP_CELL * defines.GRID_SIZE
        river_max_x = (defines.RIVER_BOTTOM_CELL) * defines.GRID_SIZE
        self.y = random.uniform(river_min_x, river_max_x - self.image.get_height())

    def update(self):
        self.x += self.speed
        self.age += 1
        self.alpha = min(255, self.alpha + 5)

    def draw(self, surface: pygame.Surface):
        floater_surface = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)
        floater_surface.blit(self.image, (0, 0))
        floater_surface.set_alpha(self.alpha)
        surface.blit(floater_surface, (self.x - defines.camera_x, self.y - defines.camera_y))
        # print("drawing")