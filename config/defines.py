import pygame 
import platform 
import os

pygame.init()

SCALE = .8

SPRING_GREEN = (0, 150, 0)
SUMMER_GREEN = (0, 200, 0)
FALL_GREEN = (0, 100, 0)
FALL_BROWN = (100, 50, 25)
WINTER_GREEN = (0, 100, 0)
WINTER_WHITE = (255, 255, 255)

BACKGROUND_COLORS = [SPRING_GREEN, SUMMER_GREEN, FALL_GREEN, FALL_BROWN, WINTER_GREEN, WINTER_WHITE]

os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0,0)

if platform.system() == "Windows":
    DISPLAY_WIDTH = pygame.display.Info().current_w
    DISPLAY_HEIGHT = pygame.display.Info().current_h
    FULL_SCREEN = False
else:
    os.environ['SDL_VIDEO_X11_DPI_AWARE'] = "1"  # Enable DPI scaling
    DISPLAY_WIDTH = 1800
    DISPLAY_HEIGHT = 900
    FULL_SCREEN = False

RIVER_TOP_CELL = 0
RIVER_BOTTOM_CELL = 3

GRID_SIZE = int(100 * SCALE * .3)

# The world size for building in cells
WORLD_WIDTH = 120
WORLD_HEIGHT = 80

camera_x = 0
camera_y = 0

CAMERA_SPEED = 10

RANDOM_EVENT_CHANCE = 0.1

FONT_PATH = "assets/fonts/Oldenburg-Regular.ttf"
FONT = pygame.font.Font("assets/fonts/Oldenburg-Regular.ttf", 64)

show_navmesh = False

WIN_CONDITION = {
    "warriors": 250,
    "ships": 10,
}