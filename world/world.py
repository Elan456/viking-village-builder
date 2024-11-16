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
        self.trees = []
        self.month = 0

        # Add initial floaters
        self.spawn_floaters()

        self.spawn_trees()

    def on_new_turn(self):
        # Reset the floaters to make the river look different each time
        # This sells that a big chunk of time passed between turns 
        self.floating_objects = []
        self.spawn_floaters()
        self.cull_trees()

        for tree in self.trees:
            tree.on_new_turn(self.month)
        
        # Re-sort the trees so that they are drawn in the correct order
        # Because the trees move after they die
        self.trees.sort(key=lambda tree: tree.y)

    def on_wall_upgrade(self):
        # Cut down trees that are now within the wall
        self.cull_trees()

    def spawn_floaters(self):
        for _ in range(10):
            f = Floater()
            f.x = random.uniform(-defines.DISPLAY_WIDTH, defines.DISPLAY_WIDTH)
            self.floating_objects.append(f)

    def spawn_trees(self):
        for _ in range(200):
            t = Tree(self.village)
            self.trees.append(t)

        self.cull_trees()
        # Z-order the trees so that they are drawn in the correct order
        self.trees.sort(key=lambda tree: tree.y)

    def cull_trees(self):
        # Removes trees if they are within the wall
        self.trees = [tree for tree in self.trees if not tree.check_within_wall()]

    def get_random_mature_tree(self):
        mature_trees = [tree for tree in self.trees if tree.age > 6 and tree.age < 7]
        if len(mature_trees) == 0:
            return None
        return random.choice(mature_trees)

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
        self.month = turn % 12
        num_colors = len(defines.BACKGROUND_COLORS)
        transition_length = 12 // num_colors

        base_index = self.month // transition_length    # e.g. month 1 --> 0, month 2 --> 0, month 5 --> 1, month 9 --> 2
        next_index = (base_index + 1) % num_colors
        percent_progress_to_next = self.month / transition_length - base_index

        base_color = defines.BACKGROUND_COLORS[base_index]
        next_color = defines.BACKGROUND_COLORS[next_index]

        color = (
            int(base_color[0] + (next_color[0] - base_color[0]) * percent_progress_to_next),
            int(base_color[1] + (next_color[1] - base_color[1]) * percent_progress_to_next),
            int(base_color[2] + (next_color[2] - base_color[2]) * percent_progress_to_next)
        )


        pygame.draw.rect(surface, color, (0, 0, defines.DISPLAY_WIDTH, defines.DISPLAY_HEIGHT))

    def draw_grid(self, surface: pygame.Surface):
        min_x = self.village.wall.x 
        min_y = self.village.wall.y
        max_x = self.village.wall.x + self.village.wall.width * defines.GRID_SIZE 
        max_y = self.village.wall.y + self.village.wall.height * defines.GRID_SIZE 

        for x in range(min_x, max_x, defines.GRID_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (x - defines.camera_x, min_y - defines.camera_y), (x - defines.camera_x, max_y - defines.camera_y))
        for y in range(min_y, max_y + defines.GRID_SIZE, defines.GRID_SIZE):
            pygame.draw.line(surface, (100, 100, 100), (min_x - defines.camera_x, y - defines.camera_y), (max_x - defines.camera_x, y - defines.camera_y))

    def draw(self, surface: pygame.Surface, turn):
        self.draw_background(surface, turn)

        self.update_floating_objects()
        self.update_ripples()
        self.draw_river(surface)
        for tree in self.trees:
            tree.draw(surface)