import pygame 
pygame.init()

SCALE = .8

SPRING_GREEN = (0, 150, 0)
SUMMER_GREEN = (0, 200, 0)
FALL_GREEN = (0, 100, 0)
FALL_BROWN = (100, 50, 25)
WINTER_GREEN = (0, 100, 0)
WINTER_WHITE = (255, 255, 255)

BACKGROUND_COLORS = [SPRING_GREEN, SUMMER_GREEN, FALL_GREEN, FALL_BROWN, WINTER_GREEN, WINTER_WHITE]

DISPLAY_WIDTH = pygame.display.Info().current_w
DISPLAY_HEIGHT = pygame.display.Info().current_h

print(DISPLAY_WIDTH, DISPLAY_HEIGHT)  
print(f"Aspect ratio: {DISPLAY_WIDTH / DISPLAY_HEIGHT}")

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

show_navmesh = False