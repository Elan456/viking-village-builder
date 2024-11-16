import pygame 
from config.defines import GRID_SIZE
from config import defines 


class DirtPath:
    def __init__(self, village):
        self.village = village
        self.surface = pygame.Surface((village.wall.width * GRID_SIZE, village.wall.height * GRID_SIZE), pygame.SRCALPHA)

    def on_navmesh_change(self, nodes_to_neighbors):
        """
        When the navmesh changes, give me a dictionary of nodes to neighbors and I will draw the dirt path between them
        """

        # Walking location conversion (Do this in reverse)
        # xmin = building.x - defines.GRID_SIZE + 2
        # xmax = building.x + building.rect.width - 2
        # ymin = building.y - defines.GRID_SIZE * 2 + 2
        # ymax = building.y + building.rect.height - 2 - defines.GRID_SIZE

        self.surface.fill((0, 0, 0, 0))
        for node, neighbors in nodes_to_neighbors.items():
            for neighbor in neighbors:
                pygame.draw.line(self.surface, (100, 100, 100),
                                  (node.x + defines.GRID_SIZE, node.y + defines.GRID_SIZE * 2), (neighbor.node.x + defines.GRID_SIZE, neighbor.node.y + defines.GRID_SIZE * 2),
                                    8)

    def draw(self, surface):
        """
        Draws the dirt path on the screen
        """
        surface.blit(self.surface, (self.village.wall.x * GRID_SIZE - defines.camera_x, self.village.wall.y * GRID_SIZE - defines.camera_y))
