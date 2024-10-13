import pygame 

from config.defines import FONT_PATH

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
        self.hover_color = (min(color[0] + 100, 255), min(color[1] + 100, 255), min(color[2] + 100, 255))
        self.text_color = text_color 
        self.font = pygame.font.Font(FONT_PATH, 24)
        self.action = action 

        self.rect = pygame.Rect(x, y, width, height)
        self.text = self.font.render(text, True, text_color)

        # To count as a click, the user must click and release the mouse on the button
        self.clicked = False

    def change_color(self, color):
        self.color = color

    def change_text(self, text):
        self.text = text

    def update(self):
        """
        Checks if the button is clicked on and then triggers the action
        """

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        if self.is_hovered(mouse_pos):
            if not mouse_down and self.clicked:
                self.action()
                self.clicked = False
            elif mouse_down:
                self.clicked = True
        else:
            self.clicked = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(self.text, (self.x + self.width / 2 - self.text.get_width() / 2, self.y + self.height / 2 - self.text.get_height() / 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)