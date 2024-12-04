import pygame 

from config.defines import CAMERA_SPEED
import config.defines as defines 
from events.announcements import announcement_handler

class EventHandler:
    """
    General event handler, i.e. keyboard and mouse events 
    """
    def __init__(self) -> None:
        self.mouse_click_funcs = []
        self.event_funcs = []  # event to function mapping

    def register_mouse_click(self, func):
        """
        When main mouse clicks, call this function
        """
        self.mouse_click_funcs.append(func)

    def register_event(self, event_type, event_key, func):
        """
        Register a function to be called when a certain event occurs
        """
        self.event_funcs.append((event_type, event_key, func))

    def register_help(self, func):
        """
        This func will be called every time the player presses 'h'  
        """
        self.register_event(pygame.KEYDOWN, pygame.K_h, func)

    def handle(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            return

        # Escape
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            return
        
        # Have the spacebar trigger a "hello there" announcement
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            announcement_handler.add_announcement("Hello there!")

        # Pressing 'n' should set the show navmesh config in the config defines toggle
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            defines.show_navmesh = not defines.show_navmesh

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            for func in self.mouse_click_funcs:
                func(event)

        # Event functions
        for event_type, event_key, func in self.event_funcs:
            if event.type == event_type and event.key == event_key:
                func()

        return event
    
    def tick(self, frame_rate):
        # Based on the frame rate, we can adjust the speed of the camera
        # i.e. a lower frame rate means the camera should move in larger steps

        if frame_rate == 0:
            frame_rate = 1
        
        frame_rate_speed_scale = 120 / frame_rate
        self.camera_movements(frame_rate_speed_scale)
        self.camera_mouse_pan()

        for event in pygame.event.get():
            event = self.handle(event)
            if event == None:
                return
        
        return True
            
    
    def camera_movements(self, frame_rate_speed_scale):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            defines.camera_x -= CAMERA_SPEED * frame_rate_speed_scale
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            defines.camera_x += CAMERA_SPEED * frame_rate_speed_scale
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            defines.camera_y -= CAMERA_SPEED * frame_rate_speed_scale
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            defines.camera_y += CAMERA_SPEED * frame_rate_speed_scale

        # Enforce camera bounds
        if defines.camera_x < defines.WORLD_WIDTH * -defines.GRID_SIZE * .25 - 100:
            defines.camera_x = defines.WORLD_WIDTH * -defines.GRID_SIZE * .25 - 100
        if defines.camera_y < defines.WORLD_HEIGHT * -defines.GRID_SIZE * .25 - 100:
            defines.camera_y = defines.WORLD_HEIGHT * -defines.GRID_SIZE * .25 - 100

        if defines.camera_x > defines.WORLD_WIDTH * defines.GRID_SIZE - defines.DISPLAY_WIDTH + 100:
            defines.camera_x = defines.WORLD_WIDTH * defines.GRID_SIZE - defines.DISPLAY_WIDTH + 100
        if defines.camera_y > defines.WORLD_HEIGHT * defines.GRID_SIZE - defines.DISPLAY_HEIGHT + 100:
            defines.camera_y = defines.WORLD_HEIGHT * defines.GRID_SIZE - defines.DISPLAY_HEIGHT + 100

    def camera_mouse_pan(self):
        x, y = pygame.mouse.get_rel()
        if pygame.mouse.get_pressed()[1]:
            defines.camera_x -= x
            defines.camera_y -= y