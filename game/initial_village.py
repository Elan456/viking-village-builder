from buildings.building import Building
from buildings.building_info import BldInfo
from config.defines import GRID_SIZE

"""
Spawns the initial village buildings
"""

def add_initial_buildings(village):
    origin_x = 0
    origin_y = 10

    lumbermill_width = BldInfo.get_width("lumbermill")

    village.add_building(Building(village, origin_x, origin_y, "lumbermill"))
    # village.add_building(Building(village,
    #                                 origin_x + BldInfo.get_width("lumbermill") + 1, origin_y, "lumbermill"))

    village.add_building(Building(village, origin_x + lumbermill_width + 1, origin_y, "mine"))
    village.add_building(Building(village, origin_x + lumbermill_width + 1, origin_y + BldInfo.get_height("mine") + 1, "grainfield"))

    # Add a buildershut
    village.add_building(Building(village, origin_x + lumbermill_width + 1, origin_y + BldInfo.get_height("mine") + 1 + BldInfo.get_height("grainfield"), "buildershut"))