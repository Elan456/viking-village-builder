import pygame 

class Button:
    """
    A button which can be clicked on 
    """

    if not pygame.font.get_init():
        pygame.font.init()

    def __init__(self, x, y, width, height, text, color, text_color, font, action) -> None:
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        self.text = text 
        self.color = color 
        self.text_color = text_color 
        self.font = font 
        self.action = action 

        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 32)
        self.text = self.font.render(text, True, text_color)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text, (self.x + self.width / 2 - self.text.get_width() / 2, self.y + self.height / 2 - self.text.get_height() / 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)