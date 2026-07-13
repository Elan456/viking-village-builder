import pygame
import random

from config import defines

# Reuse small SRCALPHA surfaces by integer radius so draw never allocates.
_RIPPLE_SURFACES: dict[int, pygame.Surface] = {}


def _ripple_surface(radius: int) -> pygame.Surface:
    radius = max(1, int(radius))
    surf = _RIPPLE_SURFACES.get(radius)
    if surf is None:
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, 255), (radius, radius), radius, 1)
        _RIPPLE_SURFACES[radius] = surf
    return surf


class Ripple:
    def __init__(self):
        self.alpha = 255
        self.radius = 0.0
        self.max_radius = random.randint(5, 20)

        self.x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
        self.y = random.randint(
            int(defines.RIVER_TOP_CELL * defines.GRID_SIZE + self.max_radius),
            int(defines.RIVER_BOTTOM_CELL * defines.GRID_SIZE - self.max_radius),
        )

    def update(self):
        self.radius = min(self.max_radius, self.radius + 0.1)
        self.alpha = max(0, self.alpha - 2)

    def draw(self, surface: pygame.Surface):
        r = int(self.radius)
        if r < 1 or self.alpha <= 0:
            return
        ripple_surface = _ripple_surface(r)
        ripple_surface.set_alpha(self.alpha)
        surface.blit(
            ripple_surface,
            (self.x - r - defines.camera_x, self.y - r - defines.camera_y),
        )
