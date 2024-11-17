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
        surface.blit(text, (10, 300 + i * 40))

    def get_change_in_resources(self, available_resources):
        """
        This method should return a dictionary with the change in resources that will occur next turn for this event.
        Use this method to affect the resources of the village.
        This is called on every new turn.
        """
        return {}



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
        burnable_buildings = village.buildings.copy()

        # Remove a single builder's hut (to prevent the player from losing the game)
        for building in burnable_buildings:
            if building.name == "buildershut":
                burnable_buildings.remove(building)

        if len(burnable_buildings) == 0:
            self.duration = 0
            return

        self.fire_buildings = random.sample(burnable_buildings, random.randint(1, max(int(len(burnable_buildings) / 2), 1)))
        if len(self.fire_buildings) == 0:
            self.duration = 0
            return

        self.duration = int(len(self.fire_buildings) / 2 + 1)  # Save half the buildings

        super().__init__(village, "Fire!", self.duration, "A fire has broken out in the village, some buildings are burning!")
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

        if len(self.fire_buildings) > 0:
            building = self.fire_buildings.pop()
            self.village.remove_building(building)

    def draw(self, surface, i):
        super().draw(surface, i)
        self.draw_tick += 1
        self.draw_tick %= len(self.fire_images)


        for building in self.fire_buildings:
            surface.blit(self.fire_images[self.draw_tick], (building.x - defines.camera_x + building.rect.width / 2 - VillageFire.width / 2, building.y - defines.camera_y + building.rect.height / 2 - VillageFire.height / 2))


class Blight(RandomEvent):

    def __init__(self, village):
        super().__init__(village, "Blight", 3, "A blight has struck the village, crops are dying!")

    def can_activate(self):
        return self.village.resources["food"] > 0

    def initial_effect(self):
        self.village.resources["food"] = max(0, self.village.resources["food"] - 50)

    def on_new_turn(self):
        super().on_new_turn()
    
    def get_change_in_resources(self, available_resources):
        food_removal = min(30, available_resources["food"])
        return {"food": -food_removal}
    
class Plague(RandomEvent):

    def __init__(self, village):
        super().__init__(village, "Plague", 3, "A plague is spreading amongst your army!")
        self.warrior_loss_per_turn = 1

    def can_activate(self):
        # Can activate if village has population and there isn't already a plague
        return self.village.resources["warriors"] > 0 

    def initial_effect(self):
        # Immediate population loss
        initial_loss = int(min(self.village.resources["warriors"], 5))
        self.village.resources["warriors"] -= initial_loss
        announcement_handler.add_announcement(f"The plague has claimed {initial_loss} warriors!")

    def get_change_in_resources(self, available_resources):
        # No resource changes
        self.removal = int(min(self.warrior_loss_per_turn, available_resources["warriors"]))
        
        return {"warriors": -self.removal}
    
    def on_new_turn(self):
        super().on_new_turn()
        announcement_handler.add_announcement(f"The plague has claimed {self.removal} more warriors!")

    def draw(self, surface, i):
        super().draw(surface, i)
        # Optionally draw plague effects
    
class TradeCaravan(RandomEvent):

    def __init__(self, village):
        super().__init__(village, "Trade Caravan", 1, "A trade caravan has passed by, leaving some goods!")

    def can_activate(self):
        # Can activate if not already active
        no_trade = not any(isinstance(event, TradeCaravan) for event in self.village.random_events.active_events)
        return no_trade
        

    def initial_effect(self):
        received_resources = {
            "food": random.randint(10, 50),
            "wood": random.randint(10, 50),
            "ore": random.randint(10, 50)
        }
        # Add resources to village
        for res, amount in received_resources.items():
            self.village.resources[res] += amount
            announcement_handler.add_announcement(f"You have received {amount} {res} from the trade caravan!")


possible_events = [VillageFire, Blight, TradeCaravan, Plague]