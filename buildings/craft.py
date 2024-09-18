"""
Defines the buildings which craft items from resources
"""

import pygame
from buildings.building import Building

class CraftBuilding(Building):
    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)
        self.production = {}
        self.cost = {}

    def _set_production(self, production: dict):
        self.production = production

    def _set_cost(self, cost: dict):
        self.cost = cost

    def update(self):
        super().update()

        # If the village has the available resources to craft the item
        # then craft it 
        if all(self.village.resources[resource] >= amount for resource, amount in self.cost.items()):
            for resource, amount in self.cost.items():
                self.village.resources[resource] -= amount
            for resource, amount in self.production.items():
                self.village.resources[resource] += amount

class BlackSmith(CraftBuilding):
    image_path = "assets/buildings/blacksmith.png"

    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)

        self._set_image(BlackSmith.image_path)
        self._set_production({"weapons": 1})
        self._set_cost({"wood": 10, "ore": 5})

        self.name = "Blacksmith"