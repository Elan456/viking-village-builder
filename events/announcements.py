import pygame
from config.defines import FONT_PATH, DISPLAY_WIDTH, DISPLAY_HEIGHT


class Announcement:

    font = pygame.font.Font(FONT_PATH, 32)

    def __init__(self, text) -> None:
        self.text = text
        self.fade_in_duration = 20  # Duration of fade-in (ticks)
        self.fade_out_duration = 200  # Duration of fade-out (ticks)
        self.max_tick = self.fade_in_duration + self.fade_out_duration
        self.tick = self.max_tick  # Start with the full tick for both phases

        # Pre-render text and backing once
        text_surf = Announcement.font.render(self.text, True, (255, 255, 255))
        self._base = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        self._base.fill((0, 0, 0, 200))
        self._base.blit(text_surf, (0, 0))
        self._text_width = text_surf.get_width()
        self._text_height = text_surf.get_height()
        self._last_opacity = None

    def draw(self, surface, i):
        if self.tick > self.fade_out_duration:
            fade_factor = (self.max_tick - self.tick) / self.fade_in_duration
        else:
            fade_factor = self.tick / self.fade_out_duration

        opacity = int(255 * fade_factor)
        if opacity != self._last_opacity:
            self._last_opacity = opacity
            self._base.set_alpha(opacity)

        surface.blit(
            self._base,
            (
                DISPLAY_WIDTH // 2 - self._text_width // 2,
                DISPLAY_HEIGHT // 2
                - self._text_height // 2
                + i * (self._text_height + 10)
                + 100,
            ),
        )

    def update(self):
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
        self.announcements = [announcement for announcement in self.announcements if announcement.tick > 0]
        for announcement in self.announcements:
            announcement.update()

    def display(self, surface):
        for i, announcement in enumerate(self.announcements):
            announcement.draw(surface, i)


# Statically defined, singleton AnnouncementHandler
announcement_handler = AnnouncementHandler()
