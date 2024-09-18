import pygame 

from config.defines import * 
import config.defines as defines 

class EventHandler:
    def __init__(self) -> None:
        pass 

    def handle(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            return

        # Escape
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            return

        return event
    
    def tick(self, frame_rate):
        # Based on the frame rate, we can adjust the speed of the camera
        # i.e. a lower frame rate means the camera should move in larger steps

        if frame_rate == 0:
            frame_rate = 1
        
        frame_rate_speed_scale = 120 / frame_rate
        self.camera_movements(frame_rate_speed_scale)

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