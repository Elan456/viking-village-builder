import pygame 

from utils.button import Button 

class StyleButton(Button):
    sprite_sheet = pygame.image.load("assets/ui/button.png")

    def __init__(self, x, y,
                 width, height,
                 button_select,
                 action):
        
        """
        Button select is a tuple of (col, row) in the sprite sheet
        """
        
        self.width = width 
        self.height = height
        self.button_select_col, self.button_select_row = button_select

        self.action = action

        self.image = pygame.Surface((16, 16))
        self.image.blit(StyleButton.sprite_sheet, (0, 0), (self.button_select_col * 16,
                                                           self.button_select_row * 16, 16, 16))
        
        self.hovered_image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.hovered_image.blit(StyleButton.sprite_sheet, (0, 0), (self.button_select_col * 16,
                                                                   self.button_select_row * 16, 16, 16))
        # Make the hovered image a bit brighter
        self.hovered_image.fill((40, 40, 40, 0), None, pygame.BLEND_RGBA_ADD)

        # Scale image to size
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hovered_image = pygame.transform.scale(self.hovered_image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.clicked = False 
    
    def draw(self, surface):
        surface.blit(self.hovered_image if self.is_hovered(pygame.mouse.get_pos()) else self.image, self.rect)



