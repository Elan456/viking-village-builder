import pygame 
import random 

from config import defines 
from config.defines import GRID_SIZE

sprite_sheet = pygame.image.load("assets/nature/Premium_TreesUpdated_No_Outline.png")

def load_tree_images(start_x, start_y):
    age_1 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_1.blit(sprite_sheet, (16, 86), (start_x + 32 * 0, start_y + 86, 32, 32))

    age_2 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_2.blit(sprite_sheet, (16, 0), (start_x + 32 * 1, start_y, 32, 112))

    age_3 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_3.blit(sprite_sheet, (16, 0), (start_x + 32 * 2, start_y, 32, 112))

    age_4 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_4.blit(sprite_sheet, (16, 0), (start_x + 32 * 3, start_y, 32, 112))

    age_5 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_5.blit(sprite_sheet, (0, 0), (start_x + 32 * 4, start_y, 64, 112))

    age_6 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_6.blit(sprite_sheet, (0, 0), (start_x + 32 * 6, start_y, 64, 112))

    age_7 = pygame.Surface((64, 112), pygame.SRCALPHA)
    age_7.blit(sprite_sheet, (16, 75), (256, start_y + 42, 32, 32))

    return [age_1, age_2, age_3, age_4, age_5, age_6, age_6, age_7]

class Tree(pygame.sprite.Sprite):

    winter_birch_ages = load_tree_images(0, 0)
    summer_birch_ages = load_tree_images(256, 0)

    winter_oak_ages = load_tree_images(0, 112)
    summer_oak_ages = load_tree_images(256, 112)

    oak_set = [summer_oak_ages, winter_oak_ages]
    birch_set = [summer_birch_ages, winter_birch_ages]

    def __init__(self, village):
        super().__init__()
        self.village = village
        self.image_sets = Tree.birch_set if random.randint(0, 1) == 0 else Tree.oak_set

        self.age = random.uniform(0, len(self.image_sets[0]) - 1)
        self.image = None 
        self.on_new_turn()
        
        self.relocate()


    def relocate(self):
        self.goto_random_location()
        while self.check_on_river() or self.check_within_wall():
            self.goto_random_location()
            

    def goto_random_location(self):
        self.x = random.randint(int(-defines.WORLD_WIDTH * GRID_SIZE * .25), int(defines.WORLD_WIDTH * GRID_SIZE))
        self.y = random.randint(int(-defines.WORLD_HEIGHT * GRID_SIZE * .25), int(defines.WORLD_HEIGHT * GRID_SIZE))

    def check_on_river(self):
        bottom_y = self.y + self.rect.height - 20
        if bottom_y > defines.RIVER_TOP_CELL * GRID_SIZE and bottom_y < defines.RIVER_BOTTOM_CELL * GRID_SIZE:
            return True

    def check_within_wall(self):
        wall_min_x = self.village.wall.x
        wall_max_x = self.village.wall.x + self.village.wall.width * GRID_SIZE
        wall_min_y = self.village.wall.y
        wall_max_y = self.village.wall.y + self.village.wall.height * GRID_SIZE

        wall_rect = pygame.Rect(wall_min_x, wall_min_y, wall_max_x - wall_min_x, wall_max_y - wall_min_y)
        tree_rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)

        return wall_rect.colliderect(tree_rect)

    def on_new_turn(self):  
        self.age += .05
        if self.age >= len(self.image_sets[0]):
            self.age = 0
            self.relocate()

        month = (self.village.turn % 12) // 2

        

        season = "summer" if month in [0, 1, 2] else "winter"

        if season == "summer":
            self.image = self.image_sets[0][int(self.age)]
        else:
            self.image = self.image_sets[1][int(self.age)]

        self.rect = self.image.get_rect()


    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x - defines.camera_x, self.y - defines.camera_y))

    
