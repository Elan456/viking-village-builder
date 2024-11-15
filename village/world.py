"""
Handles drawing the background grass, river, and trees
"""

import pygame
import random 
from config import defines 

class Ripple:
    def __init__(self, x, y):
        self.alpha = 255
        self.radius = 0

        self.x = x
        self.y = y
    
    def update(self):
        self.radius = min(5, self.radius + .1)
        self.alpha = max(0, self.alpha - 5)

    def draw(self, surface: pygame.Surface):
        color = (255, 255, 255, self.alpha)
        ripple_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(ripple_surface, color, (self.radius, self.radius), self.radius, 1)
        surface.blit(ripple_surface, (self.x - self.radius - defines.camera_x, self.y - self.radius - defines.camera_y))

class Floater:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.age = 0
        self.alpha = 0

    def update(self):
        self.x += self.speed
        self.age += 1
        self.alpha = min(255, self.alpha + 5)

    def draw(self, surface: pygame.Surface):
        floater_surface = pygame.Surface((10, 5), pygame.SRCALPHA)
        color = (255, 255, 255, self.alpha)
        pygame.draw.ellipse(floater_surface, color, (0, 0, 10, 5))
        surface.blit(floater_surface, (self.x - defines.camera_x, self.y - defines.camera_y))

class World:
    def __init__(self):
        self.river_top_cell = 0
        self.river_width_cells = 3
        self.ripples = []
        self.floating_objects = []

        # Add initial floaters
        for _ in range(10):
            x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
            y = random.randint(self.river_top_cell * defines.GRID_SIZE, (self.river_top_cell + self.river_width_cells) * defines.GRID_SIZE)
            speed = random.uniform(1.3, 1.8)
            self.floating_objects.append(Floater(x, y, speed))

    def update_ripples(self):
        # Add a new ripple randomly
        if random.random() < 0.1:  # Adjust probability to control ripple frequency
            x = random.randint(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
            y = random.randint(self.river_top_cell * defines.GRID_SIZE, (self.river_top_cell + self.river_width_cells) * defines.GRID_SIZE)
            self.ripples.append(Ripple(x, y))

        # Update ripples
        for ripple in self.ripples:
            ripple.update()

        # Remove ripples that are too old
        self.ripples = [ripple for ripple in self.ripples if ripple.alpha > 0]

    def update_floating_objects(self):
        # Add a new floating object randomly
        if random.random() < 0.01:
            x = -defines.DISPLAY_WIDTH + random.uniform(-defines.GRID_SIZE, defines.GRID_SIZE)
            y = random.randint(self.river_top_cell * defines.GRID_SIZE, (self.river_top_cell + self.river_width_cells) * defines.GRID_SIZE)
            speed = random.uniform(1.3, 1.8)
            self.floating_objects.append(Floater(x, y, speed))

        # Update floating objects
        for floater in self.floating_objects:
            floater.update()

        # Remove floating objects with an x value that is too high
        self.floating_objects = [floater for floater in self.floating_objects if floater.x < defines.DISPLAY_WIDTH]

    def draw_river(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            (0, 0, 255),
            (
                0,
                self.river_top_cell * defines.GRID_SIZE - defines.camera_y,
                defines.DISPLAY_WIDTH,
                self.river_width_cells * defines.GRID_SIZE,
            ),
        )

        for ripple in self.ripples:
            ripple.draw(surface)

        for floater in self.floating_objects:
            floater.draw(surface)

    def draw_background(self, surface: pygame.Surface, turn: int):
        month = turn % 12
        num_colors = len(defines.BACKGROUND_COLORS)
        transition_length = 12 // num_colors

        base_index = month // transition_length    # e.g. month 1 --> 0, month 2 --> 0, month 5 --> 1, month 9 --> 2
        next_index = (base_index + 1) % num_colors
        percent_progress_to_next = month / transition_length - base_index

        base_color = defines.BACKGROUND_COLORS[base_index]
        next_color = defines.BACKGROUND_COLORS[next_index]

        color = (
            int(base_color[0] + (next_color[0] - base_color[0]) * percent_progress_to_next),
            int(base_color[1] + (next_color[1] - base_color[1]) * percent_progress_to_next),
            int(base_color[2] + (next_color[2] - base_color[2]) * percent_progress_to_next)
        )


        pygame.draw.rect(surface, color, (0, 0, defines.DISPLAY_WIDTH, defines.DISPLAY_HEIGHT))

        # Draw a grid
        # for x in range(0, defines.WORLD_WIDTH * defines.GRID_SIZE + defines.GRID_SIZE, defines.GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (x - defines.camera_x, 0 - defines.camera_y), (x - defines.camera_x, defines.WORLD_HEIGHT * defines.GRID_SIZE - defines.camera_y))
        # for y in range(0, defines.WORLD_HEIGHT * defines.GRID_SIZE + defines.GRID_SIZE, defines.GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (0 - defines.camera_x, y - defines.camera_y), (defines.WORLD_WIDTH * defines.GRID_SIZE - defines.camera_x, y - defines.camera_y))
    
    def draw(self, surface: pygame.Surface, turn):
        self.draw_background(surface, turn)

        self.update_floating_objects()
        self.update_ripples()
        self.draw_river(surface)