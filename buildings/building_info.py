import json 
import pygame 
import pygame.gfxdraw
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

def load_icons():
    """
    Load each image from it's path and then scale it to the correct size based on the json file
    """
     
    images = {}
    with open("buildings/building_defs.json") as f:
        data = json.load(f)
        for building in data:
            image = pygame.image.load(data[building]['icon_path'])
            image = pygame.transform.scale(image, (2 * GRID_SIZE, 2 * GRID_SIZE))
            circle = pygame.Surface((2.8 * GRID_SIZE, 2.8 * GRID_SIZE), pygame.SRCALPHA)
            circle_radius = int(GRID_SIZE * 1.25)
            
            
            pygame.gfxdraw.aacircle(circle, circle_radius, circle_radius, int(circle_radius * .9), (0, 0, 0, 255))
            pygame.gfxdraw.aacircle(circle, circle_radius, circle_radius, circle_radius, (0, 0, 0, 255))
            pygame.gfxdraw.filled_circle(circle, circle_radius, circle_radius, circle_radius, (0, 0, 0, 255))
            pygame.gfxdraw.filled_circle(circle, circle_radius, circle_radius, int(circle_radius * .9), (0, 0, 0, 128))
            
        
            
            circle.blit(image, (0.25 * GRID_SIZE, 0.25 * GRID_SIZE))
            images[building] = circle
    return images

class BldInfo:
    info = json.load(open("buildings/building_defs.json"))
    images = load_images()
    icons = load_icons()

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
    def get_description(name):
        return BldInfo.get_info(name).get("description", "")
    
    @staticmethod
    def get_boost_buildings(name):
        return BldInfo.get_info(name).get("boost_buildings", [])
    
    @staticmethod 
    def get_icon_path(name):
        return BldInfo.get_info(name).get("icon_path", None)
