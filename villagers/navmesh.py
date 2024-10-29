import pygame
from config import defines
import random

from pyquadtree import QuadTree

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

    def can_see(self, point1, point2):
        x0, y0 = point1[0], point1[1]
        x1, y1 = point2[0], point2[1]

        for building in self.village.buildings:
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

    def generate_navmesh(self):
        """
        Generates/updates a navigation mesh for the village
        """

        self.nodes = []
        self.nodes_quadtree = QuadTree((0, 0, defines.WORLD_WIDTH * defines.GRID_SIZE, defines.WORLD_HEIGHT * defines.GRID_SIZE))

        # Adds some basic nodes to the navmesh
        for x in range(0, defines.WORLD_WIDTH * defines.GRID_SIZE, defines.GRID_SIZE * 20):
            for y in range(0, defines.WORLD_HEIGHT * defines.GRID_SIZE, defines.GRID_SIZE * 20):
                new_node = Node(x, y)
                self.nodes.append(new_node)
                self.nodes_quadtree.add(new_node, (x, y))

        
        # For every building, add the 4 corners as nodes
        for building in self.village.buildings:
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

        all_bbox = self.nodes_quadtree.get_all_bbox()
        for bbox in all_bbox:
            pygame.draw.rect(surface, (255, 0, 0), (bbox[0] - defines.camera_x, bbox[1] - defines.camera_y, bbox[2] - bbox[0], bbox[3] - bbox[1]), 1)
            
        for node in self.nodes:
            pygame.draw.circle(surface, (0, 0, 255), (node.x - defines.camera_x, node.y - defines.camera_y), 5)
            for neighbor in node.neighbors:
                pygame.draw.line(surface, (0, 0, 255), (node.x - defines.camera_x, node.y - defines.camera_y), (neighbor.node.x - defines.camera_x, neighbor.node.y - defines.camera_y))
