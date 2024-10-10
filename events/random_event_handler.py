import pygame 
import random 

from utils.button import Button 
from config.defines import * 
from events.random_event import RandomEvent, Effect, random_events

class RandomEventHandler:
    """
    Handles all of the random events which can occur between turns 
    For an event, a box will appear in the center of the screen with text and two buttons
    The player can choose between the two options

    Usually, the event will give or take away resources with an option to take more or less risk 
    """

    def __init__(self, village) -> None:
        
        self.showing_event = False 
        self.font = pygame.font.Font(None, 64)


    ####### 
    # Display and update are for the event box 
    #######
    def update(self):
        pass 

    def display(self, surface):
        pass 
        # # In the top left corner of the screen, display all the current active effects
        # for i, effect in enumerate(self.effects):
        #     text = self.font.render(effect.name + " " + str(effect.duration) + " turns left", True, (0, 0, 0))
        #     surface.blit(text, (10, 10 + i * 60))

    def on_new_turn(self):
        # When a new turn occurs, there is a chance for a random event to occur
        if random.random() < RANDOM_EVENT_CHANCE:
            self.showing_event = True