import pygame 
from config import defines 
from events.event_handler import EventHandler

lore = """
It’s 100 months before the legendary
Viking leader Sweyn Forkbeard
will launch his audacious invasion of
London in 1013 A.D.

As the chief of a small Norse village,
you’ve been tasked by Sweyn’s war
council to prepare your people to join
the war effort.

The gods have granted you exactly 100
months to grow your village, raise an
army, and amass enough resources to assist
in the conquest.

However, if your forces are insufficient
when Sweyn calls upon you, your alliance
will collapse and your village
will be overrun, erasing your legacy from
the sagas. 
"""

class LoreScroll:
    def __init__(self, event_handler):
        self.event_handler = event_handler
        self.font = pygame.font.Font(defines.FONT_PATH, 64)
        self.speed_up_font = pygame.font.Font(defines.FONT_PATH, 24)
        self.draw_tick = 0
        self.speed = 2
        self.max_draw_tick = 3000
        self.surface = pygame.Surface((defines.DISPLAY_WIDTH, defines.DISPLAY_HEIGHT), pygame.SRCALPHA)

        self.event_handler.register_mouse_click(self.on_click)
        self.got_click = False

    def done(self):
        return self.draw_tick > self.max_draw_tick

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.got_click:
                self.draw_tick = self.max_draw_tick
            self.got_click = True

    def draw(self, surface):
        self.draw_tick += self.speed
        if self.draw_tick > self.max_draw_tick:
            return
        
        dt =  defines.DISPLAY_HEIGHT - self.draw_tick - 50
        final_dt = len(lore.split("\n")) * 70 + dt

        start_fade = 2 * defines.DISPLAY_HEIGHT // 3

        # Less opacity as dt gets closer to 0
        if final_dt > start_fade:
            opacity = 255
        elif 0 < final_dt <= start_fade:
            opacity = int(255 * (final_dt/start_fade))
        else:
            opacity = 0
        # Ensure the opacity is clamped between 0 and 255
        opacity = min(255, max(0, opacity))
        
        # Clear my surface
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(opacity)
        
        for line in lore.split("\n"):
            text = self.font.render(line, True, (255, 255, 255, opacity))
            self.surface.blit(text, (defines.DISPLAY_WIDTH // 2 - text.get_width() // 2, dt))
            dt += 70

        # In the bottom right, indicate that the player can click to speed up the scroll
        text = self.speed_up_font.render("Click twice to skip", True, (255, 255, 255, opacity))
        self.surface.blit(text, (defines.DISPLAY_WIDTH - text.get_width() - 10, defines.DISPLAY_HEIGHT - text.get_height() - 10))

        # Check if the bottom is < 0
        if dt < 0:
            self.draw_tick = self.max_draw_tick

        # Chance the opacity as the bottom get's closer to 0
        
        self.surface.set_alpha(opacity)

        # Draw to the main surface
        surface.blit(self.surface, (0, 0))

        



