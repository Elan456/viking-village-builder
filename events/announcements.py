import pygame 


class Announcement:
    def __init__(self, text, options) -> None:
        self.text = text

    def display(self, surface):
        pass 

    def update(self):
        pass 

    def new_turn(self):
        pass

class AnnouncementHandler:
    def __init__(self) -> None:
        self.announcements = []

    def update(self):
        pass 

    def display(self, surface):
        pass 

announcement_handler = AnnouncementHandler()