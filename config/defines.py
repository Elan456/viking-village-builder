import pygame 
pygame.init()

SCALE = .8

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

print(DISPLAY_WIDTH, DISPLAY_HEIGHT)  

GRID_SIZE = int(100 * SCALE * .3)

# The world size for building in cells
WORLD_WIDTH = 50
WORLD_HEIGHT = 50

camera_x = 0
camera_y = 0

CAMERA_SPEED = 10

RANDOM_EVENT_CHANCE = 0.1

FONT_PATH = "assets/fonts/Oldenburg-Regular.ttf"
FONT = pygame.font.Font("assets/fonts/Oldenburg-Regular.ttf", 64)