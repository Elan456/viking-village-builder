import pygame 
pygame.init()
DISPLAY_WIDTH = pygame.display.Info().current_w
DISPLAY_HEIGHT = pygame.display.Info().current_h

print(DISPLAY_WIDTH, DISPLAY_HEIGHT)  

RIVER_HEIGHT = DISPLAY_WIDTH // 10

GRID_SIZE = 100

camera_x = 0
camera_y = 0

CAMERA_SPEED = 10

RANDOM_EVENT_CHANCE = 0.1

FONT_PATH = "assets/fonts/Oldenburg-Regular.ttf"
FONT = pygame.font.Font("assets/fonts/Oldenburg-Regular.ttf", 64)