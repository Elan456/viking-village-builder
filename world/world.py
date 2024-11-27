"""
Handles drawing the background grass, river, and trees
"""

import pygame
import random 
from config import defines 

from world.floater import Floater
from world.ripple import Ripple
from world.tree import Tree 

perlin_image = pygame.image.load("assets/misc/perlin.png")

extra_scale = 1.35

# scale the perlin image
perlin_image = pygame.transform.scale(perlin_image, (defines.WORLD_WIDTH * extra_scale * defines.GRID_SIZE, defines.WORLD_HEIGHT * extra_scale * defines.GRID_SIZE))


def generate_backgrounds():
    """
    For each background color, add noise to give a textured look and save it to a file 
    """
    backgrounds = []
    for color in defines.BACKGROUND_COLORS:
        background = pygame.Surface((defines.WORLD_WIDTH * extra_scale * defines.GRID_SIZE * .5,
                                     defines.WORLD_HEIGHT * extra_scale * defines.GRID_SIZE * .5), pygame.SRCALPHA)

        # If the image already exists with the correct dimensions, load it
        try:
            load_background = pygame.image.load(f"assets/backgrounds/background_{color[0]}_{color[1]}_{color[2]}.jpg")
            # if load_background.get_width() == background.get_width() and load_background.get_height() == background.get_height():
            #     print(f"Loaded background_{color[0]}_{color[1]}_{color[2]}")
            backgrounds.append(load_background)
            continue
        except FileNotFoundError:
            pass

        for x in range(background.get_width()):
            for y in range(background.get_height()):
                noise_1 = perlin_image.get_at((x % perlin_image.get_width(), y % perlin_image.get_height()))
                noise_2 = perlin_image.get_at(((x + 1) % perlin_image.get_width(), (y + 1) % perlin_image.get_height()))
                noise_3 = perlin_image.get_at(((x - 1) % perlin_image.get_width(), (y - 1) % perlin_image.get_height()))

                noise = ((noise_1[0] + noise_2[0] + noise_3[0]) // 3,
                            (noise_1[1] + noise_2[1] + noise_3[1]) // 3,
                            (noise_1[2] + noise_2[2] + noise_3[2]) // 3)
                r, g, b = color
                r += noise[0] * -.25
                g += noise[1] * -.25
                b += noise[2] * -.25
                r = max(0, min(255, r))
                g = max(0, min(255, g))
                b = max(0, min(255, b))
                background.set_at((x, y), (r, g, b, 255))    

        # Save to a file
        pygame.image.save(background, f"assets/backgrounds/background_{color[0]}_{color[1]}_{color[2]}.jpg")

        backgrounds.append(background)

    return backgrounds


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
        self.background_color = (0, 0, 0)
        self.background_surfaces = generate_backgrounds()

        # Scale each one to the full size
        for i, background in enumerate(self.background_surfaces):
            self.background_surfaces[i] = pygame.transform.scale(background, (defines.WORLD_WIDTH * extra_scale * defines.GRID_SIZE,
                                                                            defines.WORLD_HEIGHT * extra_scale * defines.GRID_SIZE))

    def on_new_turn(self):
        # Reset the floaters to make the river look different each time
        # This sells that a big chunk of time passed between turns 
        self.floating_objects = []
        self.spawn_floaters()
        self.cull_trees()

        for tree in self.trees:
            tree.on_new_turn()
        
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
        self.month = (turn % 12) // 2
        self.background_color = defines.BACKGROUND_COLORS[self.month]
      
        # print("drawing background with dimensions", self.background_surfaces[self.month].get_width(), self.background_surfaces[self.month].get_height())
        surface.blit(self.background_surfaces[self.month], (0 - defines.camera_x - defines.WORLD_WIDTH * defines.GRID_SIZE * .25 - 100,
                                                            0 - defines.camera_y - defines.WORLD_HEIGHT * defines.GRID_SIZE * .25 - 100))
        # print("Backsurface colors: ", self.background_surfaces[self.month].get_at((50, 50)))

        # pygame.draw.rect(surface, self.background_color, (0 - defines.camera_x, 0 - defines.camera_y, defines.DISPLAY_WIDTH, defines.DISPLAY_HEIGHT))
        # pygame.draw.circle(surface, (255, 0, 0), (defines.DISPLAY_WIDTH // 2, defines.DISPLAY_HEIGHT // 2), 10)

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