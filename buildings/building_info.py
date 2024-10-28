import json 

class BldInfo:
    info = json.load(open("buildings/building_defs.json"))

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
