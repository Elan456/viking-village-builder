import pygame
from config.defines import FONT_PATH, DISPLAY_WIDTH, DISPLAY_HEIGHT


class Announcement:

    font = pygame.font.Font(FONT_PATH, 128)

    def __init__(self, text) -> None:
        self.text = text
        self.fade_in_duration = 50  # Duration of fade-in (ticks)
        self.fade_out_duration = 500  # Duration of fade-out (ticks)
        self.max_tick = self.fade_in_duration + self.fade_out_duration
        self.tick = self.max_tick  # Start with the full tick for both phases

    def draw(self, surface, i):
        # Determine the opacity based on the current tick value
        if self.tick > self.fade_out_duration:
            # Fade-in phase: tick goes from fade_in_duration to max_tick
            fade_factor = (self.max_tick - self.tick) / self.fade_in_duration
        else:
            # Fade-out phase: tick goes from fade_out_duration to 0
            fade_factor = self.tick / self.fade_out_duration

        # Calculate opacity (0-255)
        opacity = int(255 * fade_factor)

        # Render the text without color, just using grayscale or original color
        text = Announcement.font.render(self.text, True, (255, 255, 255))  # Render with solid white

        # Create a surface to control opacity
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.fill((255, 255, 255, 0))  # Transparent surface

        # Blit the text onto the transparent surface
        text_surface.blit(text, (0, 0))

        # Set the opacity (alpha) of the text surface
        text_surface.set_alpha(opacity)

        # Blit the text surface onto the main surface
        surface.blit(text_surface, (DISPLAY_WIDTH // 2 - text.get_width() // 2, DISPLAY_HEIGHT // 2 - text.get_height() // 2 + i * 120))

    def update(self):
        # Decrease the tick over time, capping it at 0
        if self.tick > 0:
            self.tick -= 1


class AnnouncementHandler:
    """
    Handles displaying and updating announcements. Any other class can add an announcement to the handler.
    """
    def __init__(self) -> None:
        self.announcements = []

    def add_announcement(self, text: str):
        self.announcements.insert(0, Announcement(text))

    def update(self):
        # Filter out the announcements with a tick < 0
        self.announcements = [announcement for announcement in self.announcements if announcement.tick > 0]
        for announcement in self.announcements:
            announcement.update()

    def display(self, surface):
        for i, announcement in enumerate(self.announcements):
            announcement.draw(surface, i)


# Statically defined, singleton AnnouncementHandler
announcement_handler = AnnouncementHandler()
