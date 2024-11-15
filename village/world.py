"""
Handles drawing the background grass, river, and trees
"""

import pygame
from config import defines 

class World:
    def __init__(self):
        self.river_top_cell = 0
        self.river_width_cells = 3

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
        # river
        pygame.draw.rect(surface, (0, 0, 255), (0, self.river_top_cell * defines.GRID_SIZE - defines.camera_y, defines.DISPLAY_WIDTH, self.river_width_cells * defines.GRID_SIZE))

        # Draw a grid
        # for x in range(0, defines.WORLD_WIDTH * defines.GRID_SIZE + defines.GRID_SIZE, defines.GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (x - defines.camera_x, 0 - defines.camera_y), (x - defines.camera_x, defines.WORLD_HEIGHT * defines.GRID_SIZE - defines.camera_y))
        # for y in range(0, defines.WORLD_HEIGHT * defines.GRID_SIZE + defines.GRID_SIZE, defines.GRID_SIZE):
        #     pygame.draw.line(surface, (0, 0, 0), (0 - defines.camera_x, y - defines.camera_y), (defines.WORLD_WIDTH * defines.GRID_SIZE - defines.camera_x, y - defines.camera_y))
    
    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)