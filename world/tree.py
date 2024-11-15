import pygame 
import random 

from config import defines 

class Tree(pygame.sprite.Sprite):
    types = ["birch",
             "oak"]
    
    sprite_sheet = pygame.image.load("assets/nature/Premium_TreesUpdated_No_Outline.png")

    summer_birch = pygame.Surface((64, 112))
    summer_birch.blit(sprite_sheet, (0, 0), (444, 0, 64, 112))

    summer_oak = pygame.Surface((64, 112))
    summer_oak.blit(sprite_sheet, (0, 0), (444, 112, 64, 112))

    def __init__(self, x, y):
        super().__init__()
        self.type = random.choice(Tree.types)
        self.image = Tree.summer_birch if self.type == "birch" else Tree.summer_oak

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    
