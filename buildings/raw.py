"""
Defines the buildings which simply collect raw resources
"""

import pygame

from buildings.building import Building

class RawBuilding(Building):
    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)

    def _set_production(self, production: dict):
        self.production = production

    def update(self):
        super().update()

        # Production
        for resource, amount in self.production.items():
            self.village.resources[resource] += amount * self.village.production_multipliers[resource]



class GrainField(RawBuilding):
    image_path = "assets/buildings/grain_field.png"

    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)
        
        self._set_image(GrainField.image_path)
        self._set_production({"food": 1})
        self._set_construction_cost({"wood": 10})

        self.name = "Grain Field"

class Mine(RawBuilding):
    image_path = "assets/buildings/mine.png"

    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)

        self._set_image(Mine.image_path)
        self._set_production({"ore": 1})
        self._set_construction_cost({"wood": 10})

        self.name = "Mine"

class LumberMill(RawBuilding):
    image_path = "assets/buildings/lumber_mill.png"
    
    def __init__(self, village, x, y) -> None:
        super().__init__(village, x, y)

        self._set_image(LumberMill.image_path)
        self._set_production({"wood": 1})
        self._set_construction_cost({"wood": 10})

        
