import random 
from events.announcements import announcement_handler
from config.defines import FONT

class Effect:
    """
    An effect which can be applied to the village 
    """
    def __init__(self, name, duration,
                 min_scale=1, max_scale=1,
                 resource_count_name=None, resource_prod_name=None,
                 magnitude=1, removes_effect=None, removes_effect_chance=1) -> None:
        """
        :param name: The name of the effect
        :param duration: The duration of the effect in turns
        :param min_scale: The minimum scale of the magnitude
        :param max_scale: The maximum scale of the magnitude
        :param resource_count_name: The name of the resource count to modify
        :param resource_prod_name: The name of the resource production rate to modify
        :param magnitude: The magnitude of the effect, will be multiplied by a random number between min_scale and max_scale
        :param removes_effect: The name of the effect which will be removed when this effect is applied
        :param removes_effect_chance: The chance of removing the effect 0-1
        """

        self.name = name 
        self.duration = duration 
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.resource_count_name = resource_count_name
        self.resource_prod_name = resource_prod_name
        self.removes_effect = removes_effect
        self.removes_effect_chance = removes_effect_chance

        assert self.min_scale <= self.max_scale
        self.magnitude = random.uniform(self.min_scale, self.max_scale) * magnitude
        self.magnitude = round(self.magnitude, 1)
        
        # You can't modify both the count and the production rate
        assert self.resource_count_name is not None or self.resource_prod_name is not None

        self.application_count = 0

    
    def apply(self, village):
        """
        Apply the effect to the village
        """
        if self.application_count == 0:
            # Try to remove the removes_effect
            if self.removes_effect is not None and self.removes_effect in village.active_effects:
                if random.random() < self.removes_effect_chance:
                    village.active_effects.remove(self.removes_effect)
                    announcement_handler.add_announcement(f"{self.removes_effect} has been removed by {self.name}")

        if self.resource_count_name is not None:
            village.resources[self.resource_count_name] += self.magnitude
        if self.resource_prod_name is not None:
            village.production_multipliers[self.resource_prod_name] = self.magnitude

    def draw(self, surface, i): 
        """
        Draw the effect and how many turns are left in the top-left corner of the screen
        :param surface: The surface to draw on
        :param i: The index of the effect in the list (for vertical spacing)
        """

        text = f"{self.name} {self.duration} turns left"
        text = FONT.render(text, True, (0, 0, 0))
        surface.blit(text, (10, 10 + i * 60))

    def __str__(self) -> str:
        """
        Gives a description of the effect
        """
        if self.resource_count_name is not None:
            symbol = "+" if self.magnitude > 0 else ""
            return f"{self.name}: {self.resource_count_name} {symbol}{self.magnitude} for {self.duration} turns"
        if self.resource_prod_name is not None:
            return f"{self.name}: {self.resource_prod_name} x{self.magnitude} for {self.duration} turns"