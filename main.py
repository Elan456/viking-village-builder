import pygame 

from game.village import Village
from events.event_handler import EventHandler
from config.defines import *
import assets.buildings.generate_placeholders
from events.announcements import announcement_handler

pygame.init()
pygame.font.init()

class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        # Enable alpha channel for transparency
        self.screen.set_alpha(None)
        self.village = Village()
        self.event_handler = EventHandler()
        self.clock = pygame.time.Clock()

    def start(self):
        while True:
            frame_rate = self.clock.get_fps()
            if self.event_handler.tick(frame_rate) == None:
                break

            self.village.update()
            self.village.draw(self.screen)

            announcement_handler.update()
            announcement_handler.display(self.screen)

            pygame.display.flip()
            self.clock.tick(30)
            pygame.display.set_caption(f"FPS: {frame_rate}")



if __name__ == "__main__":
    Game().start()