import pygame 

from villagers.villager import Villager 
from buildings.construction import Construction

class Builder(Villager):
    def __init__(self, my_building):
        super().__init__(my_building)
        self.construction_target: Construction = None

    def choose_destination(self):
        if self.construction_target is not None:
            return self.get_random_building_edge(self.construction_target.building)
        else:
            return self.get_random_building_edge(self.building)