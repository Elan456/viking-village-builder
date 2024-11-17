import pygame 
import random 

from utils.button import Button 
from config.defines import * 
from events.random_event import possible_events

class RandomEventHandler:
    """
    Handles all of the random events which can occur between turns 
    For an event, a box will appear in the center of the screen with text and two buttons
    The player can choose between the two options

    Usually, the event will give or take away resources with an option to take more or less risk 
    """

    def __init__(self, village) -> None:
        
        self.village = village
        self.showing_event = False 
        self.font = pygame.font.Font(None, 64)
        self.active_events = []


    ####### 
    # Display and update are for the event box 
    #######
    def update(self):
        pass 

    def draw(self, surface):
        for i, event in enumerate(self.active_events):
            event.draw(surface, i)

    def on_new_turn(self):
        # on new turn for each event
        for event in self.active_events:
            event.on_new_turn()

        # When a new turn occurs, there is a chance for a random event to occur
        if random.random() < 0.1:
            event = random.choice(possible_events)(self.village)
            self.active_events.append(event)


        

        # Remove events that have expired
        self.active_events = [event for event in self.active_events if event.duration > 0]