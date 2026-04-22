class Cat:
    """This class represents a cat"""

    hunger = 0
    social_battery = 0
    feeling_loved = 0
    tiredness = 0


    def __init__(self,):
        self.hunger = 0
        self.social_battery = 0
        self.feeling_loved = 0
        self.tiredness = 0

    def mood_prompt(self,) -> str:
        """
        This method is called when a question is asked to prompt the mood the cat should reply in.

        :return:
        """
        mood_prompt = ""
        if self.hunger < 5:
            mood_prompt += "Answer as if the cat is super hungry and only thinks about food."
        if self.hunger >5:
            mood_prompt += "Answer as if the cat just ate and would like to digest the meal a bit."
        return mood_prompt





