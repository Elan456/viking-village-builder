"""
Handles drawing the background grass, river, and trees
"""

import pygame
import random 
from config import defines 

from world.floater import Floater
from world.ripple import Ripple
from world.tree import Tree 


class World:
    def __init__(self, village):
        self.village = village 
        self.ripples = []
        self.floating_objects = []

        # Add initial floaters
        for _ in range(10):
            f = Floater()
            f.x = random.uniform(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
            self.floating_objects.append(f)

    def update_ripples(self):
        # Add a new ripple randomly
        if random.random() < 0.1:  # Adjust probability to control ripple frequency
            self.ripples.append(Ripple())

        # Update ripples
        for ripple in self.ripples:
            ripple.update()

        # Remove ripples that are too old
        self.ripples = [ripple for ripple in self.ripples if ripple.alpha > 0]

    def update_floating_objects(self):
        # Add a new floating object randomly
        if random.random() < 0.005:
            self.floating_objects.append(Floater())

        # Update floating objects
        for floater in self.floating_objects:
            floater.update()

        # Remove floating objects with an x value that is too high
        self.floating_objects = [floater for floater in self.floating_objects if floater.x < defines.DISPLAY_WIDTH]

    def draw_river(self, surface: pygame.Surface):
        river_width_cells = defines.RIVER_BOTTOM_CELL - defines.RIVER_TOP_CELL
        pygame.draw.rect(
            surface,
            (0, 0, 255),
            (
                0,
                defines.RIVER_TOP_CELL * defines.GRID_SIZE - defines.camera_y,
                defines.DISPLAY_WIDTH,
                river_width_cells * defines.GRID_SIZE,
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

    def draw(self, surface: pygame.Surface, turn):
        self.draw_background(surface, turn)

        self.update_floating_objects()
        self.update_ripples()
        self.draw_river(surface)