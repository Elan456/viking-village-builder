import pygame
import random
from config import defines
from .navmesh import Node
import json
from utils.utils import long_text, longTextnewLines

ALL_VILLAGERS = ["farmer", "miner", "lumberjack", "blacksmith", "shipwright", "builder", "hersir"]


class Villager(pygame.sprite.Sprite):

    blurts = json.load(open("villagers/blurts.json", "r"))
    blurt_font = pygame.font.Font(defines.FONT_PATH, 10)

    idle_ss = {name: pygame.image.load(f"assets/villagers/{name}/idle.png") for name in ALL_VILLAGERS}
    walk_ss = {name: pygame.image.load(f"assets/villagers/{name}/walk.png") for name in ALL_VILLAGERS}

    frame_width = defines.GRID_SIZE * 2
    frame_height = defines.GRID_SIZE * 2

    # Scale all the images by 2x
    for name in ALL_VILLAGERS:
        idle_ss[name] = pygame.transform.scale(idle_ss[name], (frame_width * 4, frame_height))
        walk_ss[name] = pygame.transform.scale(walk_ss[name], (frame_width * 6, frame_height))

    # name -> action -> facing(0/1) -> list of frame surfaces
    frames = None

    @classmethod
    def prepare_frames(cls):
        """Slice and flip animation frames once (call after display convert)."""
        cls.frames = {}
        for name in ALL_VILLAGERS:
            idle_sheet = cls.idle_ss[name].convert_alpha()
            walk_sheet = cls.walk_ss[name].convert_alpha()
            cls.idle_ss[name] = idle_sheet
            cls.walk_ss[name] = walk_sheet

            idle_right = []
            for i in range(4):
                frame = idle_sheet.subsurface(
                    (i * cls.frame_width, 0, cls.frame_width, cls.frame_height)
                ).copy()
                idle_right.append(frame)
            idle_left = [pygame.transform.flip(f, True, False) for f in idle_right]

            walk_right = []
            for i in range(6):
                frame = walk_sheet.subsurface(
                    (i * cls.frame_width, 0, cls.frame_width, cls.frame_height)
                ).copy()
                walk_right.append(frame)
            walk_left = [pygame.transform.flip(f, True, False) for f in walk_right]

            cls.frames[name] = {
                "idle": (idle_right, idle_left),
                "walk": (walk_right, walk_left),
            }

    def __init__(self, my_building) -> None:
        super().__init__()
        self.building = my_building
        self.village = self.building.village

        self.x = self.building.x
        self.y = self.building.y

        self.name = None

        self.current_action = "idle"  # idle, walk
        self.walk_time = 600  # How long to spend walking (frames)
        self.idle_time = 100
        self.current_time = 0  # Counts down to zero and then switches actions
        self.frame_tick = 0

        self.blurt_tick = random.randint(500, 2000)
        self.blurt_message = None

        self.destination = None
        self.facing = 0  # 0 = right, 1 = left

        self.current_destination_index = 0
        self.path = []  # Sequence of points to walk to

        self.speed = 1
        self.lost = False

        self._blank = pygame.Surface((Villager.frame_width, Villager.frame_height), pygame.SRCALPHA)

    def handle_blurt(self):
        self.blurt_tick -= 1
        if self.blurt_tick == 0:
            self.blurt_message = random.choice(Villager.blurts[self.name])
            self.blurt_message = longTextnewLines(self.blurt_message, 20)

        if self.blurt_tick < -100:
            self.blurt_tick = random.randint(500, 2000)

    def draw_blurt(self, surface):
        if self.blurt_message is not None:
            long_text(
                surface,
                (self.x - defines.camera_x, self.y - 20 - defines.camera_y),
                self.blurt_message,
                (0, 0, 0),
                self.blurt_font,
                20,
                align="center",
                rect_color=(128, 128, 128, 255),
                border_color=(0, 0, 0, 255),
            )

    def get_image(self):
        if self.name is None or Villager.frames is None:
            return self._blank
        action = self.current_action if self.current_action in ("idle", "walk") else "idle"
        facing_frames = Villager.frames[self.name][action][self.facing]
        n = len(facing_frames)
        idx = int(self.frame_tick) % n
        return facing_frames[idx]

    def start_walking(self):
        self.current_action = "walk"
        if self.destination is None:
            self.destination = self.choose_destination()
            self.path = self.village.navmesh.find_path_a_star((self.x, self.y), self.destination)
            if self.path is None:
                self.lost = True
                self.current_action = "idle"
                self.current_time = self.idle_time
                self.destination = None
                return
            self.path.append(Node(self.destination[0], self.destination[1]))
        self.lost = False
        if self.path is None:
            self.lost = True
            self.current_action = "idle"
            self.current_time = self.idle_time
            self.destination = None

    def update(self):
        if self.name is None:
            self.name = self.building.get_villager_name()

        self.handle_blurt()

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
            # Move towards the next point in the path
            dx = self.path[0].x - self.x
            dy = self.path[0].y - self.y
            if dx < 0:
                self.facing = 1
            else:
                self.facing = 0
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < 2:
                self.path.pop(0)
                if len(self.path) == 0:
                    self.current_action = "idle"
                    self.current_time = self.idle_time
                    self.destination = None
            else:
                dx /= dist
                dy /= dist
                self.x += dx * self.speed
                self.y += dy * self.speed

    def draw_path(self, surface):
        if self.path is None:
            return

        path = [Node(self.x, self.y)] + self.path
        for i in range(len(path) - 1):
            pygame.draw.line(
                surface,
                (255, 0, 0),
                (path[i].x - defines.camera_x, path[i].y - defines.camera_y),
                (path[i + 1].x - defines.camera_x, path[i + 1].y - defines.camera_y),
                8,
            )

        if self.destination is not None:
            pygame.draw.circle(
                surface,
                (255, 0, 0),
                (self.destination[0] - defines.camera_x, self.destination[1] - defines.camera_y),
                20,
                2,
            )

    def draw(self, surface):
        surface.blit(self.get_image(), (self.x - defines.camera_x, self.y - defines.camera_y))

        if self.lost:
            pygame.draw.line(
                surface,
                (255, 0, 0),
                (self.x - 10 - defines.camera_x, self.y - 10 - defines.camera_y),
                (self.x + 10 - defines.camera_x, self.y + 10 - defines.camera_y),
                3,
            )

        if self.blurt_tick < 0:
            self.draw_blurt(surface)

    def get_random_building_edge(self, building):
        x = random.choice([-1, building.get_cell_width()]) * defines.GRID_SIZE
        y = random.choice([-1, building.get_cell_height() - 1]) * defines.GRID_SIZE
        x += building.x
        y += building.y
        return x, y

    def get_random_building_by_type(self, building_type):
        random_order = self.village.buildings.copy()
        random.shuffle(random_order)
        for building in random_order:
            if building.name == building_type:
                return building
        return None

    def choose_destination(self):
        self.current_destination_index += 1
        if self.name == "farmer":
            return self.get_random_building_edge(self.building)

        elif self.name == "miner":
            self.current_destination_index %= 2
            if self.current_destination_index == 0:
                return self.get_random_building_edge(self.building)
            elif self.current_destination_index == 1:
                return 0, defines.WORLD_HEIGHT * defines.GRID_SIZE

        elif self.name == "lumberjack":
            self.current_destination_index %= 2
            if self.current_destination_index == 0:
                return self.get_random_building_edge(self.building)
            elif self.current_destination_index == 1:
                tree = self.village.world.get_random_mature_tree()
                if tree is None:
                    return self.get_random_building_edge(self.building)
                return tree.x + 32, tree.y + 112

        elif self.name == "blacksmith":
            self.current_destination_index %= 3
            if self.current_destination_index == 0:
                return self.get_random_building_edge(self.building)
            elif self.current_destination_index == 1:
                lumbermill = self.get_random_building_by_type("lumbermill")
                if lumbermill is None:
                    return self.get_random_building_edge(self.building)
                return self.get_random_building_edge(lumbermill)
            elif self.current_destination_index == 2:
                mine = self.get_random_building_by_type("mine")
                if mine is None:
                    return self.get_random_building_edge(self.building)
                return self.get_random_building_edge(mine)

        elif self.name == "shipwright":
            self.current_destination_index %= 3
            if self.current_destination_index == 0:
                return self.get_random_building_edge(self.building)
            elif self.current_destination_index == 1:
                lumbermill = self.get_random_building_by_type("lumbermill")
                if lumbermill is None:
                    return self.get_random_building_edge(self.building)
                return self.get_random_building_edge(lumbermill)
            elif self.current_destination_index == 2:
                return defines.WORLD_WIDTH / 2 * defines.GRID_SIZE, defines.GRID_SIZE * 4

        else:
            self.current_destination_index %= 1
            return self.get_random_building_edge(self.building)
