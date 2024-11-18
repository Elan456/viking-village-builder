import pygame 
from utils.style_button import StyleButton
from config.defines import FONT_PATH
from assets.ui.button_mapping import GREEN_PLAY, RED_EXIT


start_screen_image = pygame.image.load("assets/backgrounds/start_screen.png")

class StartMenu:
    def __init__(self):
        self.font = pygame.font.Font(FONT_PATH, 48)
        self.screen = pygame.display.set_mode((800, 600))
        # Scale image to size 
        self.image = pygame.transform.scale(start_screen_image, (800, 600))
        self.play_button = StyleButton(275, 400, 100, 100, GREEN_PLAY, self.start_game)
        self.exit_button = StyleButton(425, 400, 100, 100, RED_EXIT, self.exit_game)
        self.running = True 

        self.title_line_1 = self.font.render("Invasion of London", True, (0, 0, 0))
        self.title_line_2 = self.font.render("Forkbeard's Call", True, (0, 0, 0))
        self.title = [self.title_line_1, self.title_line_2]

        pygame.display.set_caption("Invasion of London: Forkbeard's Call")
    
    def start(self):
        while self.running:
            self.screen.blit(self.image, (0, 0))
            self.play_button.update()
            self.exit_button.update()
            self.play_button.draw(self.screen)
            self.exit_button.draw(self.screen)

            for i, title in enumerate(self.title):
                # Center the title
                self.screen.blit(title, (400 - title.get_width() // 2, 70 + i * title.get_height() + 20))


            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    # escape key on keyboard
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game()

    def start_game(self):
        self.running = False 

    def exit_game(self):
        pygame.quit()
        quit()

