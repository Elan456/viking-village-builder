import random 
import pygame 

from config.defines import FONT_PATH, GRID_SIZE
from config import defines 
from events.announcements import announcement_handler

class RandomEvent:
    """
    A random event can happen every time the player starts a new turn.
    
    Because it has a reference to the village object, it can do basically anything.
    """

    def __init__(self, village, name, duration, description):
        self.village = village
        self.name = name
        self.duration = duration
        self.description = description

        self.font = pygame.font.Font(FONT_PATH, 32)

        if self.can_activate():
            self.initial_effect()
            announcement_handler.add_announcement(f"{description}")
        
        else:
            self.duration = 0

    def can_activate(self):
        """
        This method should return True if the event can be activated, False otherwise.
        """
        return True
        
    def initial_effect(self):
        """
        This is the first effect that happens when the event is triggered.
        """
        raise NotImplementedError("The developer needs to implement the initial_effect method")

    def on_new_turn(self):
        """
        This is the effect that happens every time the player starts a new turn.
        """
        self.duration -= 1

    def draw(self, surface, i):
        """
        This is the method that draws the event to the screen.
        """
        # Draw the name and duration left in the top left corner
        text = self.font.render(f"{self.name} - {self.duration} turns left", True, (255, 255, 255))
        surface.blit(text, (10, 300 + i * 20))



class VillageFire(RandomEvent):

    fire_images = []
    fire_sheet = pygame.image.load("assets/random_events/Fire_Spreadsheet.png")
    for x in range(2):
        for y in range(2):
            img = fire_sheet.subsurface((x * 512, y * 512, 512, 512))
            # Scale to 2x2 gridsize
            img = pygame.transform.scale(img, (GRID_SIZE * 4, GRID_SIZE * 4))
            fire_images.append(img)
    
    width = fire_images[0].get_width()
    height = fire_images[0].get_height()


    def __init__(self, village):
        super().__init__(village, "Fire!", 2, "A fire has broken out in the village, some buildings are burning!")

        burnable_buildings = [building for building in village.buildings if building.name != "buildershut"]

        if len(burnable_buildings) == 0:
            self.duration = 0
            return

        self.fire_buildings = random.sample(burnable_buildings, random.randint(1, min(3, len(burnable_buildings))))

        self.draw_tick = 0

    def can_activate(self):
        # Make sure there are buildings that can burn and that a fire isn't currently active
        has_targets = len([building for building in self.village.buildings if building.name != "buildershut"]) > 0
        no_fire = not any(isinstance(event, VillageFire) for event in self.village.random_events.active_events)

        return has_targets and no_fire


    def initial_effect(self):
        pass 
        

    def on_new_turn(self):
        super().on_new_turn()

        if len(self.fire_buildings) > 0 and self.duration < 3:
            building = self.fire_buildings.pop()
            self.village.remove_building(building)

    def draw(self, surface, i):
        super().draw(surface, i)
        self.draw_tick += 1
        self.draw_tick %= len(self.fire_images)


        for building in self.fire_buildings:
            surface.blit(self.fire_images[self.draw_tick], (building.x - defines.camera_x + building.rect.width / 2 - VillageFire.width / 2, building.y - defines.camera_y + building.rect.height / 2 - VillageFire.height / 2))

possible_events = [VillageFire]