"""
Defines the wall the surround your village 
This defines how much room you have to build in
The player can increase the size of their building area by upgrading the wall
"""

import pygame
from config.defines import GRID_SIZE
from config import defines 
from villagers.navmesh import CollisionRect
from villagers.navmesh import Node

class Wall(pygame.sprite.Sprite):
    def __init__(self, village) -> None:
        self.village = village

        # All defined in cells 
        self.width = 20
        self.height = 20
        self.x = 0
        self.y = 0

        self.color = (50, 50, 50)
        self.thickness = 8
        self.hole_size = 4   # In cells

        ### 
        # Setup collision rects 
        ### 

        self.left_wall = CollisionRect(self.x * GRID_SIZE - self.thickness,
                                  self.y * GRID_SIZE - self.thickness,
                                  self.thickness, self.height * GRID_SIZE + 2 * self.thickness)
        self.top_wall = CollisionRect(self.x * GRID_SIZE - self.thickness,
                                    self.y * GRID_SIZE - self.thickness,
                                    self.width * GRID_SIZE + 2 * self.thickness, self.thickness)
        self.right_wall = CollisionRect(self.x * GRID_SIZE + self.width * GRID_SIZE,
                                    self.y * GRID_SIZE - self.thickness,
                                    self.thickness, self.height * GRID_SIZE + 2 * self.thickness)
        self.left_bottom_wall = CollisionRect(self.x * GRID_SIZE - self.thickness,
                                        self.y * GRID_SIZE + self.height * GRID_SIZE,
                                        self.width * GRID_SIZE / 2 - (self.hole_size * GRID_SIZE * 0.5), self.thickness)
        self.right_bottom_wall = CollisionRect(self.x * GRID_SIZE + self.width * GRID_SIZE / 2 + (self.hole_size * GRID_SIZE * 0.5),
                                        self.y * GRID_SIZE + self.height * GRID_SIZE,
                                        self.width / 2 * GRID_SIZE - self.hole_size / 2 * GRID_SIZE, self.thickness)

        self.walls = [self.left_wall, self.top_wall, self.right_wall, self.left_bottom_wall, self.right_bottom_wall]
        # Put a single node in the center of the wall
        self.hole_node = Node(int(self.x * GRID_SIZE + self.width // 2 * GRID_SIZE),
                              int(self.y * GRID_SIZE + self.height * GRID_SIZE))
        
        self.outer_corner_nodes = [Node(self.x * GRID_SIZE - self.thickness - 5, self.y * GRID_SIZE - self.thickness - 5),
                                      Node(self.x * GRID_SIZE + self.width * GRID_SIZE + self.thickness + 5, self.y * GRID_SIZE - self.thickness - 5),
                                      Node(self.x * GRID_SIZE - self.thickness - 5, self.y * GRID_SIZE + self.height * GRID_SIZE + self.thickness + 5),
                                      Node(self.x * GRID_SIZE + self.width * GRID_SIZE + self.thickness + 5, self.y * GRID_SIZE + self.height * GRID_SIZE + self.thickness + 5)]


    def draw(self, surface: pygame.Surface):
        """
        Draws the wall on the screen
        """
        
        for wall in self.walls:
            pygame.draw.rect(surface, self.color, (wall.x - defines.camera_x, wall.y - defines.camera_y, wall.width, wall.height))


    def get_collision_rects(self):
        """
        Returns 5 collision rectangles to represent the wall
        left wall, top wall, right wall, left-side bottom wall, right-side bottom wall
        """
        return self.walls

    def can_upgrade(self):
        """
        Checks if the wall can be upgraded
        """
        return self.village.resources["wood"] >= 100
    
    def upgrade(self):
        """
        Upgrades the wall to increase the size of the village
        """
        self.width += 5
        self.height += 5

    def can_build(self, x, y, width, height):
        """
        Checks if a building can be built at the given position
        by ensuring it is within the wall
        """
        
        # Ensures the building is within the wall
        if x < self.x or y < self.y:
            return False
        if x + width > self.x + self.width or y + height > self.y + self.height:
            return False
        return True 