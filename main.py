import pygame 

from village.village import Village
from events.event_handler import EventHandler
from config.defines import DISPLAY_WIDTH, DISPLAY_HEIGHT, FULL_SCREEN
from events.announcements import announcement_handler
from game.start_menu import StartMenu
from game.lore_scroll import LoreScroll
from config.defines import FONT_PATH

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Invasion of London: Forkbeard's Call")
pygame.display.set_icon(pygame.image.load("assets/resources/axe.png"))

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN if FULL_SCREEN else 0)
        # Enable alpha channel for transparency
        self.screen.set_alpha(None)
        self.event_handler = EventHandler()
        self.village = Village(self.event_handler)
        self.lore_scroll = LoreScroll(self.event_handler)
        self.clock = pygame.time.Clock()

        self.fps_font = pygame.font.Font(FONT_PATH, 12)

    def start(self):
        while True:
            frame_rate = self.clock.get_fps()
            if self.event_handler.tick(frame_rate) == None:
                break

            self.village.update()
            self.village.draw(self.screen)
            self.lore_scroll.draw(self.screen)

            announcement_handler.update()
            announcement_handler.display(self.screen)

            fps_text = self.fps_font.render(f"{frame_rate:.1f} FPS", True, (0, 0, 0))
            self.screen.blit(fps_text, (DISPLAY_WIDTH - fps_text.get_width() - 5, 5))


            pygame.display.flip()
            self.clock.tick(30)



if __name__ == "__main__":
    StartMenu().start()
    Game().start()