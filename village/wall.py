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
from utils.button import Button 
from game.resources import get_icon
from events.announcements import announcement_handler

class Wall(pygame.sprite.Sprite):
    def __init__(self, village) -> None:
        self.village = village

        # All defined in cells 
        self.width = 40
        self.height = 35
        self.x = 0
        self.y = 0

        self.color = (50, 50, 50)
        self.thickness = 8
        self.hole_size = 4   # In cells

        ### 
        # Setup collision rects 
        ### 
        self.calculate_walls()

        
        self.upgrade_button_font = pygame.font.Font(defines.FONT_PATH, 20)
        self.upgrade_button = Button(self.x ,
                                     self.y * GRID_SIZE + self.height * GRID_SIZE + 10,
                                     180, 30, "Upgrade Wall", (100, 100, 100), (0, 0, 0), self.upgrade_button_font, self.try_upgrade)
        
        self.upgrade_cost = {
            "wood": 200,
            "ore": 150
        }

        self.wall_cost_multiplier = 3

    def draw(self, surface: pygame.Surface):
        """
        Draws the wall on the screen
        """
        
        for wall in self.walls:
            pygame.draw.rect(surface, self.color, (wall.x - defines.camera_x, wall.y - defines.camera_y, wall.width, wall.height))

        # Draw next to the button the icons and amount of resources needed to upgrade the wall
        for i, (resource, amount) in enumerate(self.upgrade_cost.items()):
            icon = get_icon(resource)
            icon = pygame.transform.scale(icon, (20, 20))
            surface.blit(icon, (self.upgrade_button.x + self.upgrade_button.width + i * 100, self.upgrade_button.y + 5))
            text = self.upgrade_button_font.render(str(amount), True, (0, 0, 0))
            surface.blit(text, (self.upgrade_button.x + self.upgrade_button.width + 20 + i * 100, self.upgrade_button.y + 5))

    def update(self):
        """
        Updates the wall
        """
        self.upgrade_button.update()
        self.upgrade_button.move(
            -defines.camera_x - self.thickness, -defines.camera_y - self.upgrade_button.height - self.thickness
        )

    def calculate_walls(self):
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



    def get_collision_rects(self):
        """
        Returns 5 collision rectangles to represent the wall
        left wall, top wall, right wall, left-side bottom wall, right-side bottom wall
        """
        return self.walls
    
    def try_upgrade(self):
        """
        Tries to upgrade the wall
        """
        if self.can_upgrade():
            self.upgrade()
        else:
            announcement_handler.add_announcement("Not enough resources to upgrade the wall")

    def can_upgrade(self):
        """
        Checks if the wall can be upgraded
        """
        for item in self.upgrade_cost.keys():
            if self.village.resources[item] < self.upgrade_cost[item]:
                return False
        return True
    
    def upgrade(self):
        """
        Upgrades the wall to increase the size of the village
        """
        self.width += 8
        self.height += 5
        self.calculate_walls()

        for item in self.upgrade_cost.keys():
            self.village.resources[item] -= self.upgrade_cost[item]
            self.upgrade_cost[item] *= self.wall_cost_multiplier
            self.upgrade_cost[item] = int(self.upgrade_cost[item])

        self.village.navmesh.generate_navmesh()
        self.village.world.on_wall_upgrade()

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