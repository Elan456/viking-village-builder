import pygame 
import random
from config import defines 

ALL_VILLAGERS = ["farmer", "miner", "lumberjack", "blacksmith", "shipwright", "builder", "hersir"]

class Villager(pygame.sprite.Sprite):

    idle_ss = {name: pygame.image.load(f"assets/villagers/{name}/idle.png") for name in ALL_VILLAGERS}
    walk_ss = {name: pygame.image.load(f"assets/villagers/{name}/walk.png") for name in ALL_VILLAGERS}

    def __init__(self, my_building) -> None:
        super().__init__()
        self.building = my_building
        self.village = self.building.village

        self.x = self.building.x
        self.y = self.building.y

        self.name = None

        self.current_action = "idle"  # idle, walk
        self.walk_time = 600  # How long to spend walking (frames)
        self.idle_time = 0
        self.current_time = 0 # Counts down to zero and then switches actions
        self.frame_tick = 0

        self.destination = None

    def get_image(self):
        if self.name is None:
            return pygame.Surface((48, 48))
        if self.current_action == "idle":
            base_image = Villager.idle_ss[self.name]
            x = (int(self.frame_tick) % 4) * 48
            y = 0
            return base_image.subsurface((x, y, 48, 48))

        elif self.current_action == "walk":
            # (50x50) with 6 frames
            base_image = Villager.walk_ss[self.name]
            x = (int(self.frame_tick) % 6) * 48
            y = 0
            return base_image.subsurface((x, y, 48, 48))
        
    def start_walking(self):
        self.current_action = "walk"
        self.destination = (self.x + random.randint(-100, 100), self.y + random.randint(-100, 100))
        
    def update(self):
        if self.name is None:
            self.name = self.building.get_villager_name()

        self.frame_tick += 0.1
        self.current_time -= 1

        if self.current_time < 0:
            if self.current_action == "idle":
                self.current_action = "walk"
                self.current_time = self.walk_time + random.randint(-100, 100)
                self.start_walking()
            else:
                self.current_action = "idle"
                self.current_time = self.idle_time

        if self.current_action == "walk":
            if self.destination is None:
                self.start_walking()
            # Move towards the destination
            dx = self.destination[0] - self.x
            dy = self.destination[1] - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < 2:
                self.current_action = "idle"
                self.current_time = self.idle_time
            else:
                if dx != 0:
                    self.x += dx / abs(dx)
                if dy != 0:
                    self.y += dy / abs(dy)

    def draw(self, surface):
        surface.blit(self.get_image(), (self.x - defines.camera_x, self.y - defines.camera_y))
