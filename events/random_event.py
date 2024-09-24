from effects.effect import Effect


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
        self.opt_2_effect: Effect = None

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
    RandomEvent("A blight has struck the village's crops")
    .set_description("The crops have been infected with a blight, reducing food production")
    .set_initial_effect(Effect("Blight", 3, resource_prod_name="food", magnitude=0.5))
    .set_opt_1_effect(Effect("Crop Burning", 3, resource_prod_name="food", magnitude=0, removes_effect="Blight", removes_effect_chance=0.8))
    .set_opt_1_label("Burn the crops")
    .set_opt_2_label("Wait the blight out")
]