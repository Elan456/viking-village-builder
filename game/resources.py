import pygame 

resource_to_icon = {
    "wood": "assets/resources/wood.png",
    "ore": "assets/resources/ore.png",
    "food": "assets/resources/food.png",
    "weapons": "assets/resources/axe.png",
    "warriors": "assets/resources/warrior.png",
    "ships": "assets/resources/ship.png",
}

# Load all the resources and replace the dict with the properly scaled images
for resource_name, resource_path in resource_to_icon.items():
    image = pygame.image.load(resource_path)
    image = pygame.transform.scale(image, (24, 24))
    resource_to_icon[resource_name] = image


def get_icon(resource_name: str):
    return resource_to_icon[resource_name]