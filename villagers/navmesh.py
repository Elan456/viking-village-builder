import pygame
from config import defines
from config.defines import GRID_SIZE
import random

from pyquadtree import QuadTree
import copy


class CollisionRect:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

class Neighbor:
    def __init__(self, node, cost):
        self.node = node
        self.cost = cost

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbor(self, node, cost):
        self.neighbors.append(Neighbor(node, cost))

class NavMesh:

    def __init__(self, village):
        self.village = village
        self.nodes = None

        # Quadtree that holds all the buildings for can_see
        self.building_quadtree = None 

    def can_see(self, point1, point2):
        x0, y0 = point1[0], point1[1]
        x1, y1 = point2[0], point2[1]

        buildings_to_check = self.building_quadtree.query((min(x0, x1) - 2 * GRID_SIZE,
                                                           min(y0, y1) -  2 * GRID_SIZE,
                                                           max(x0, x1) +  2 * GRID_SIZE,
                                                           max(y0, y1) +  2 * GRID_SIZE))
        # Add in the 5 nearest buildings to the query
        # buildings_to_check = self.building_quadtree.nearest_neighbors(point1, number_of_neighbors=5)
        # buildings_to_check += self.building_quadtree.nearest_neighbors(point2, number_of_neighbors=5)

        buildings_to_check = [e.item[0] for e in buildings_to_check]

        buildings_to_check = list(set(buildings_to_check))

        for building in buildings_to_check + self.village.wall.get_collision_rects():
            # print(building.x, building.y, building.rect.width, building.rect.height, type(building))
            xmin = building.x - defines.GRID_SIZE + 2
            xmax = building.x + building.rect.width - 2
            ymin = building.y - defines.GRID_SIZE * 2 + 2
            ymax = building.y + building.rect.height - 2 - defines.GRID_SIZE

            if self.liang_barsky(x0, y0, x1, y1, xmin, xmax, ymin, ymax):
                return False  # Line of sight is blocked by this building

        return True  # No buildings block the line of sight

    def liang_barsky(self, x0, y0, x1, y1, xmin, xmax, ymin, ymax):
        """
        Checks if a line segment intersects a rectangle
        """
        dx = x1 - x0
        dy = y1 - y0
        p = [-dx, dx, -dy, dy]
        q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]
        u1, u2 = 0.0, 1.0

        for pi, qi in zip(p, q):
            if pi == 0:
                if qi < 0:
                    return False  # Line is parallel and outside the rectangle
                else:
                    continue  # Line is parallel and inside the rectangle
            u = qi / pi
            if pi < 0:
                if u > u2:
                    return False  # Line is outside the rectangle
                if u > u1:
                    u1 = u
            else:
                if u < u1:
                    return False  # Line is outside the rectangle
                if u < u2:
                    u2 = u

        return True  # Line segment intersects the rectangle

    def generate_building_quadtree(self):
        """
        Generates a quadtree which holds all the buildings for
        quick lookup for can_see 
        """
        self.building_quadtree = QuadTree((-defines.WORLD_WIDTH * .25 * defines.GRID_SIZE,
                                           -defines.WORLD_HEIGHT * .25 * defines.GRID_SIZE,
                                           defines.WORLD_WIDTH * defines.GRID_SIZE, defines.WORLD_HEIGHT * defines.GRID_SIZE))

        for building in self.village.buildings + [c.building for c in self.village.builder_manager.construction_queue]:
            # Add each corner of the building to the quadtree
            # Turning each building a tuple because the quadtree can't store duplicates
            self.building_quadtree.add((building, 1), (building.x - GRID_SIZE, building.y - GRID_SIZE))
            self.building_quadtree.add((building, 2), (building.x + building.rect.width + GRID_SIZE, building.y - GRID_SIZE))
            self.building_quadtree.add((building, 3), (building.x - GRID_SIZE, building.y + building.rect.height + GRID_SIZE))
            self.building_quadtree.add((building, 4), (building.x + building.rect.width + GRID_SIZE, building.y + building.rect.height + GRID_SIZE))

            # Add points in the middle
            self.building_quadtree.add((building, 5), (building.x + building.rect.width // 2, building.y - GRID_SIZE))
            self.building_quadtree.add((building, 6), (building.x + building.rect.width // 2, building.y + building.rect.height + GRID_SIZE))
            self.building_quadtree.add((building, 7), (building.x - GRID_SIZE, building.y + building.rect.height // 2))
            self.building_quadtree.add((building, 8), (building.x + building.rect.width + GRID_SIZE, building.y + building.rect.height // 2))


    def generate_navmesh(self):
        """
        Generates/updates a navigation mesh for the village
        """

        self.generate_building_quadtree()

        self.nodes = []
        self.nodes_quadtree = QuadTree((-defines.WORLD_WIDTH * .25 * defines.GRID_SIZE,
                                         -defines.WORLD_HEIGHT * .25 * defines.GRID_SIZE,
                                         defines.WORLD_WIDTH * defines.GRID_SIZE, defines.WORLD_HEIGHT * defines.GRID_SIZE))

        # Adds some basic nodes to the navmesh
        for x in range(int(-defines.WORLD_WIDTH * defines.GRID_SIZE * .25),
                        defines.WORLD_WIDTH * defines.GRID_SIZE, defines.GRID_SIZE * 15):
            for y in range(int(-defines.WORLD_HEIGHT * defines.GRID_SIZE * .25),
                            defines.WORLD_HEIGHT * defines.GRID_SIZE, defines.GRID_SIZE * 15):
                new_node = Node(x, y)
                self.nodes.append(new_node)
                self.nodes_quadtree.add(new_node, (x, y))

        # Add the wall nodes
        for node in self.village.wall.outer_corner_nodes:
            n = copy.deepcopy(node)
            self.nodes.append(n)
            self.nodes_quadtree.add(n, (n.x, n.y))
        wall_node = copy.deepcopy(self.village.wall.hole_node)
        self.nodes.append(wall_node)
        self.nodes_quadtree.add(wall_node, (wall_node.x, wall_node.y))

        
        # For every building, add the 4 corners as nodes
        for building in self.village.buildings + [c.building for c in self.village.builder_manager.construction_queue]:
            x, y = building.x, building.y
            n1 = Node(x - 1 - defines.GRID_SIZE, y - 1 - defines.GRID_SIZE * 2)
            n2 = Node(x + building.rect.width + 1, y - 1 - defines.GRID_SIZE * 2)
            n3 = Node(x - 1 - defines.GRID_SIZE, y + building.rect.height + 1 - defines.GRID_SIZE)
            n4 = Node(x + building.rect.width + 1, y + building.rect.height + 1 - defines.GRID_SIZE)
            for n in [n1, n2, n3, n4]:
                self.nodes_quadtree.add(n, (n.x, n.y))
                self.nodes.append(n)

        # For every node, add all the nodes it can see as neighbors
        total_neighbors = 0
        for i, node in enumerate(self.nodes):
            for other_element in self.nodes_quadtree.nearest_neighbors((node.x, node.y), number_of_neighbors=10):
                other_node = other_element.item
                other_point = other_element.point
                if node == other_node:
                    continue
                distance_sq = (node.x - other_point[0]) ** 2 + (node.y - other_point[1]) ** 2
                if self.can_see((node.x, node.y), other_point):
                    other_node_index = self.nodes.index(other_node)
                    distance = distance_sq ** 0.5

                    # Ensuring all neighbors are recriprocal
                    self.nodes[i].add_neighbor(self.nodes[other_node_index], distance)
                    self.nodes[other_node_index].add_neighbor(self.nodes[i], distance)
                    total_neighbors += 1

        # If a node has no neighbors, remove it
        nodes_to_remove = [node for node in self.nodes if len(node.neighbors) == 0]
        for node in nodes_to_remove:
            self.nodes.remove(node)
            self.nodes_quadtree.delete(node)

        self.village.dirt_path.on_navmesh_change({node: node.neighbors for node in self.nodes})

    def find_path_a_star(self, start_pnt, end_pnt):
        """
        Finds a path from start to end using the A* algorithm
        """

        # Find the nodes closest to the start and end points that can be seen
        start = self.nodes_quadtree.nearest_neighbors(start_pnt, number_of_neighbors=1)[0].item
        end = self.nodes_quadtree.nearest_neighbors(end_pnt, number_of_neighbors=1)[0].item

        open_list = [start]
        closed_list = []
        came_from = {start: None}  # Dictionary to store the parent of each node
        g_score = {node: float('inf') for node in self.nodes}  # Dictionary to store the cost of the cheapest path from start to node
        g_score[start] = 0
        h_score = {node: ((node.x - end.x) ** 2 + (node.y - end.y) ** 2) ** 0.5 for node in self.nodes}  # Dictionary to store the heuristic cost from node to end

        while open_list:
            current = min(open_list, key=lambda node: g_score[node] + h_score[node])
            if current == end:  # Path found

                # Build the path using the came_from dictionary
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path = path[::-1]
                # Add the true end point to the path
                path.append(Node(end_pnt[0], end_pnt[1]))
                
                # Add the true start point to the path
                path.insert(0, Node(start_pnt[0], start_pnt[1]))
                return path

            open_list.remove(current)
            closed_list.append(current)

            for neighbor in current.neighbors:
                if neighbor.node in closed_list:
                    continue
                tentative_g_score = g_score[current] + neighbor.cost  # Get the potential g_score for this node
                if neighbor.node not in open_list:  # If the neighbor is not in the open list, add it
                    open_list.append(neighbor.node)
                elif tentative_g_score >= g_score[neighbor.node]:  # Don't use the g_score if it's worse than the current one
                    continue
                
                # If the g_score is better, than update the came_from and g_score dictionaries
                came_from[neighbor.node] = current
                g_score[neighbor.node] = tentative_g_score

        return None  # No path found

    def draw(self, surface):
        """
        Draws the navigation mesh on the screen
        """
        if self.nodes is None:
            return

        # all_bbox = self.nodes_quadtree.get_all_bbox()
        all_bbox = self.building_quadtree.get_all_bbox()
        for bbox in all_bbox:
            pygame.draw.rect(surface, (255, 0, 0), (bbox[0] - defines.camera_x, bbox[1] - defines.camera_y, bbox[2] - bbox[0], bbox[3] - bbox[1]), 2)

        # Draw the villager routes
        for node in self.nodes:
            for neighbor in node.neighbors:
                pygame.draw.line(surface, (0, 255, 0), (node.x - defines.camera_x, node.y - defines.camera_y), (neighbor.node.x - defines.camera_x, neighbor.node.y - defines.camera_y))
            pygame.draw.circle(surface, (0, 255, 0), (node.x - defines.camera_x, node.y - defines.camera_y), 5)
        # Draw the building corners  
        for point in [v.point for v in self.building_quadtree.get_all_elements()]:
            node = Node(point[0], point[1])
            pygame.draw.circle(surface, (0, 255, 255), (node.x - defines.camera_x, node.y - defines.camera_y), 5)
            for neighbor in node.neighbors:
                pygame.draw.line(surface, (0, 0, 255), (node.x - defines.camera_x, node.y - defines.camera_y), (neighbor.node.x - defines.camera_x, neighbor.node.y - defines.camera_y))
