resource_to_icon = {
    "wood": "assets/resources/wood.png",
    "ore": "assets/resources/ore.png",
    "food": "assets/resources/food.png",
    "people": "assets/resources/people.png",
    "weapons": "assets/resources/weapons.png",
    "boats": "assets/resources/boats.png",
    "gold": "assets/resources/gold.png",
}


def get_icon(resource_name: str):
    return resource_to_icon[resource_name]

