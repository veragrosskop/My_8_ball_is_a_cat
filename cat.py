from enum import Enum
from typing import Dict, List
from time import time


class Mood(Enum):
    best = "happy"
    normal = "good"
    worst = "very grumpy"
    hungry = "hungry"
    tired = "sleepy"
    antisocial = "antisocial"
    lonely = "lonely"

class Cat:
    """This class represents a cat"""

    hunger = 0
    social_fatigue = 0
    loneliness = 0
    sleepy = 0
    mood = [Mood.normal]
    last_update = None

    def __init__(self,):
        self.hunger = 2
        self.social_fatigue = 5
        self.loneliness = 0
        self.sleepy = 0
        self.update_mood()

    def clamp(self):
        """
        Clamps all state attributes to the min and max value.
        :return:
        """
        minimum = 0
        maximum = 100
        self.hunger = max(minimum, min(maximum, self.hunger))
        self.loneliness = max(minimum, min(maximum, self.loneliness))
        self.social_fatigue = max(minimum, min(maximum, self.social_fatigue))
        self.sleepy = max(minimum, min(maximum, self.sleepy))

    def get_mood_instructions(self,) -> str:
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

    def handle_pet(self):
        """
        Handles a pet event. Increases the loved feeling and reduces the social battery.
        """
        self.loneliness -= 2
        self.social_fatigue += 1
        self.clamp()
        self.update_mood()

    def handle_feed(self):
        """
        Handles a feed event.
        Decreases the hunger.
        """

        self.hunger -= 1
        self.clamp()
        self.update_mood()

    def update_mood(self):
        """
        Updates the mood based on the state of the cat.

        """
        self.mood = []
        if self.hunger > 5:
            self.mood.append(Mood.hungry)
        if self.social_fatigue <= 3:
            self.mood.append(Mood.antisocial)
        if self.loneliness <= 5:
            self.mood.append(Mood.lonely)
        if self.sleepy <= 3:
            self.mood.append(Mood.tired)
        if all(mood < 3 for mood in(self.hunger, self.sleepy, self.loneliness, self.social_fatigue)):
            self.mood.append(Mood.best)
        if all(mood > 8 for mood in (self.hunger, self.sleepy, self.loneliness, self.social_fatigue)):
            self.mood.append(Mood.worst)
        if not self.mood:
            self.mood.append(Mood.normal)


    def update(self):
        now = time()

        if self.last_update is None:
            self.last_update = now
            return

        elapsed = now - self.last_update

        self.hunger += elapsed * 0.02
        self.loneliness += elapsed * 0.015
        self.sleepy += elapsed * 0.02
        self.social_fatigue -= elapsed * 0.015
        self.update_mood()

        self.last_update = now

    def get_dict_state(self) -> Dict[str, str | List[str]]:
        """
        Writes all the state variables to a dictionary.

        :return:
        """

        state = {
            "hunger": self.hunger,
             "sleepy": self.sleepy,
             "loneliness": self.loneliness,
             "social_fatigue": self.social_fatigue,
             "last_update": self.last_update,
             "mood": [m.value for m in self.mood]
        }

        return state








