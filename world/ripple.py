import pygame 
import random 

from config import defines 

class Ripple:
    def __init__(self):
        self.alpha = 255
        self.radius = 0
        self.max_radius = random.randint(5, 20)

        self.x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
        self.y = random.randint(defines.RIVER_TOP_CELL * defines.GRID_SIZE + self.max_radius, (defines.RIVER_BOTTOM_CELL) * defines.GRID_SIZE - self.max_radius)
    
    def update(self):
        self.radius = min(self.max_radius, self.radius + .1)
        self.alpha = max(0, self.alpha - 2)

    def draw(self, surface: pygame.Surface):
        color = (255, 255, 255, self.alpha)
        ripple_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ripple_surface, color, (self.radius, self.radius), self.radius, 1)
        surface.blit(ripple_surface, (self.x - self.radius - defines.camera_x, self.y - self.radius - defines.camera_y))
