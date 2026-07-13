import pygame
import random

from config import defines


def create_cloud_surface():
    """
    Procedurally generates a single cloud on a surface
    """
    # Smaller than the original 600x600 to cut translucent fill cost
    cloud_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
    cloud_surface.fill((255, 255, 255, 0))

    for _ in range(random.randint(20, 35)):
        oval_width = random.randint(25, 55)
        oval_height = random.randint(max(12, oval_width // 2), min(50, oval_width + 8))
        max_x = max(1, 150 - oval_width)
        max_y = max(1, 150 - oval_height)
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        shadow_x = x + 150 + random.randint(-5, 5)
        shadow_y = y + 150 + random.randint(-5, 5)
        pygame.draw.ellipse(cloud_surface, (0, 0, 0, 50), (shadow_x, shadow_y, oval_width, oval_height))
        pygame.draw.ellipse(cloud_surface, (255, 255, 255, 100), (x, y, oval_width, oval_height))

    return cloud_surface


class Cloud(pygame.sprite.Sprite):
    def __init__(self, cloud_surfaces):
        super().__init__()
        # Own a copy so per-cloud alpha does not mutate shared templates
        self.base_image = random.choice(cloud_surfaces)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
        self.rect.y = random.randint(-defines.DISPLAY_HEIGHT, defines.DISPLAY_HEIGHT)
        self.alpha = 0
        self.image.set_alpha(0)

    def update(self):
        self.rect.x += 1
        if self.rect.x > defines.DISPLAY_WIDTH + defines.GRID_SIZE * 20:
            self.rect.x = random.randint(-defines.DISPLAY_WIDTH, 0)
            self.rect.y = random.randint(-defines.DISPLAY_HEIGHT, defines.DISPLAY_HEIGHT)
            self.alpha = 0

        new_alpha = min(255, self.alpha + random.randint(0, 2))
        if new_alpha != self.alpha:
            self.alpha = new_alpha
            self.image.set_alpha(self.alpha)

    def draw(self, surface):
        if self.alpha <= 0:
            return
        # Skip fully off-screen clouds
        x = self.rect.x - defines.camera_x
        y = self.rect.y - defines.camera_y
        if x + self.rect.width < 0 or y + self.rect.height < 0:
            return
        if x > defines.DISPLAY_WIDTH or y > defines.DISPLAY_HEIGHT:
            return
        surface.blit(self.image, (x, y))


class CloudHandler:

    surfaces = [create_cloud_surface() for _ in range(30)]

    def __init__(self):
        self.clouds = []
        self.on_new_turn()

    def on_new_turn(self):
        self.clouds = []
        for _ in range(6):
            self.clouds.append(Cloud(self.surfaces))

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def draw(self, surface):
        for cloud in self.clouds:
            cloud.draw(surface)
