

class Effect:
    """
    An effect which can be applied to the village 
    """
    def __init__(self, name, duration, func) -> None:
        """
        :param name: The name of the effect
        :param duration: The duration of the effect in turns
        :param func: The function which will be called when the effect is applied
        """
        self.name = name 
        self.duration = duration 
        self.func = func 

    def apply(self, village):
        self.func(village)

class RandomEvent:
    """
    A random event has an initial effect, and then two options, each with their own effect
    """
    def __init__(self, name:str) -> None:
        self.name = name
        self.weight = 1  # A higher weight means a higher chance of occurring
        self.description = ""
        self.initial_effect: Effect = None
        
        self.opt_1_effect: Effect = None
        self.opt_1_effect: Effect = None

        self.opt_1_label = ""
        self.opt_2_label = ""

    def set_description(self, description:str):
        self.set_description = description
        return self 
    
    def set_initial_effect(self, effect:Effect):
        self.initial_effect = effect
        return self
    
    def set_opt_1_effect(self, effect:Effect):
        self.opt_1_effect = effect
        return self
    
    def set_opt_2_effect(self, effect:Effect):
        self.opt_2_effect = effect
        return self
    
    def set_opt_1_label(self, label:str):
        self.opt_1_label = label
        return self
    
    def set_opt_2_label(self, label:str):
        self.opt_2_label = label
        return self
    

random_events = [

]