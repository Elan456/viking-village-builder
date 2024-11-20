import pygame 
from config.defines import FONT_PATH
from utils.button import Button 

class StyleButton(Button):
    sprite_sheet = pygame.image.load("assets/ui/button.png")

    def __init__(self, x, y,
                 width, height,
                 button_select,
                 action, hover_text=None):
        
        """
        Button select is a tuple of (col, row) in the sprite sheet
        """
        
        self.width = width 
        self.height = height
        self.button_select_col, self.button_select_row = button_select

        self.hover_text = hover_text

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
        
        if self.hover_text:
            self.hover_text = pygame.font.Font(FONT_PATH, 24).render(self.hover_text, True, (0, 0, 0))
    
    def draw(self, surface, cam_x=0, cam_y=0):
        is_hovered = self.is_hovered(pygame.mouse.get_pos(), cam_x=cam_x, cam_y=cam_y)
        surface.blit(self.hovered_image if is_hovered else self.image, (self.rect.x - cam_x, self.rect.y - cam_y))

        # Write the hover text directly under the button (centered)
        if is_hovered and self.hover_text:
            text_surface = pygame.Surface((self.hover_text.get_width() + 20, self.hover_text.get_height() + 10), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, 200))
            surface.blit(text_surface, (self.rect.x + self.width // 2 - text_surface.get_width() // 2 - cam_x, self.rect.y + self.height - cam_y))
            surface.blit(self.hover_text, (self.rect.x + self.width // 2 - self.hover_text.get_width() // 2 - cam_x, self.rect.y + self.height + 5 - cam_y))



