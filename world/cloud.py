import pygame 
import random

from config import defines 



def create_cloud_surface():
    """
    Procedurally generates a single cloud on a surface
    """
    cloud_surface = pygame.Surface((600, 600), pygame.SRCALPHA)
    cloud_surface.fill((255, 255, 255, 0))

    for i in range(random.randint(20, 50)):
        oval_width = random.randint(50, 100)
        oval_height = random.randint(oval_width // 2, oval_width + 20)
        x = random.randint(oval_width, 300 - oval_width)
        y = random.randint(oval_height, 300 - oval_height)

        shadow_x = x + 300 + random.randint(-5, 5)
        shadow_y = y + 300 + random.randint(-5, 5)
        pygame.draw.ellipse(cloud_surface, (0, 0, 0, 50), (shadow_x, shadow_y, oval_width, oval_height))
        pygame.draw.ellipse(cloud_surface, (255, 255, 255, 100), (x, y, oval_width, oval_height))
        

        

    return cloud_surface

class Cloud(pygame.sprite.Sprite):
        def __init__(self, cloud_surfaces):
            super().__init__()
            self.image = random.choice(cloud_surfaces)
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
            self.rect.y = random.randint(-defines.DISPLAY_HEIGHT, defines.DISPLAY_HEIGHT)
            self.alpha = 0
    
        def update(self):
            self.rect.x += 1
            if self.rect.x > defines.DISPLAY_WIDTH + defines.GRID_SIZE * 20:
                self.rect.x = random.randint(-defines.DISPLAY_WIDTH, 0)
                self.rect.y = random.randint(-defines.DISPLAY_HEIGHT, defines.DISPLAY_HEIGHT)
                self.alpha = 0
            
            self.alpha = min(255, self.alpha + random.randint(0, 2))
            self.image.set_alpha(self.alpha)

        def draw(self, surface):
            surface.blit(self.image, (self.rect.x - defines.camera_x, self.rect.y - defines.camera_y))

class CloudHandler:

    surfaces = [create_cloud_surface() for _ in range(30)]

    def __init__(self):
        self.clouds = []
        self.on_new_turn()

    def on_new_turn(self):
        self.clouds = []
        for _ in range(10):
            self.clouds.append(Cloud(self.surfaces))

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def draw(self, surface):
        for cloud in self.clouds:
            cloud.draw(surface)

