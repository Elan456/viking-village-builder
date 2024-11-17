import json 
import pygame 
from config.defines import GRID_SIZE

def load_images():
    """
    Load each image from it's path and then scale it to the correct size based on the json file
    """
     
    images = {}
    with open("buildings/building_defs.json") as f:
        data = json.load(f)
        for building in data:
            image = pygame.image.load(f"assets/buildings/{building}.png")
            image = pygame.transform.scale(image, (GRID_SIZE * data[building]["width"], GRID_SIZE * data[building]["height"]))
            images[building] = image
    return images

class BldInfo:
    info = json.load(open("buildings/building_defs.json"))
    images = load_images()

    @staticmethod
    def get_all_keys():
        return list(BldInfo.info.keys())
    
    @staticmethod
    def get_name(name):
        return BldInfo.get_info(name).get("name", None)
    
    @staticmethod
    def get_info(name):
        return BldInfo.info[name]
    
    @staticmethod
    def get_width(name):
        return BldInfo.get_info(name).get("width", 1)
    
    @staticmethod   
    def get_height(name):
        return BldInfo.get_info(name).get("height", 1)
    
    @staticmethod
    def get_image_path(name):
        return f"assets/buildings/{name}.png"
    
    @staticmethod
    def get_construction_time(name):
        return BldInfo.get_info(name).get("construction_time", 0)
    
    @staticmethod
    def get_construction_cost(name):
        return BldInfo.get_info(name).get("construction", {})
    
    @staticmethod
    def get_production(name):
        return BldInfo.get_info(name).get("production", {})
    
    @staticmethod
    def get_cost(name):
        return BldInfo.get_info(name).get("cost", {})
    
    @staticmethod
    def get_villager_name(name):
        return BldInfo.get_info(name).get("villager_name", None)
    
    @staticmethod
    def get_boost_buildings(name):
        return BldInfo.get_info(name).get("boost_buildings", [])
