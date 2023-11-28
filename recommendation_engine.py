import itertools
from typing import List
from base_classes import *
import sqlite3


def sample_skis():
    skis = []
    skis.append(Ski("Redster S9", "Atomic", "expert", 1, 150, 58, 0))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 155, 58, 0))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 160, 58, 1))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 165, 58, 2))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 170, 58, 3))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 175, 58, 4))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 180, 58, 5))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 185, 58, 6))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 190, 58, 7))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 195, 58, 8))
    skis.append(Ski("Redster S9", "Atomic", "expert", 3, 200, 58, 9))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 150, 68, 10))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 155, 68, 11))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 160, 68, 12))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 165, 68, 13))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 170, 68, 14))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 175, 68, 15))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 180, 68, 16))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 185, 68, 17))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 190, 68, 18))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 195, 68, 19))
    skis.append(Ski("Attraxion", "Rossignol", "expert", 3, 200, 68, 20))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 150, 64, 21))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 155, 64, 22))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 160, 64, 23))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 165, 64, 24))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 170, 64, 25))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 175, 64, 26))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 180, 64, 27))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 185, 64, 28))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 190, 64, 29))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 195, 64, 30))
    skis.append(Ski("Forza 20D", "Rossignol", "expert", 3, 200, 64, 31))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 150, 62, 32))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 155, 62, 33))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 160, 62, 34))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 165, 62, 35))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 170, 62, 36))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 175, 62, 37))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 180, 62, 38))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 185, 62, 39))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 190, 62, 40))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 195, 62, 41))
    skis.append(Ski("MCK Sport", "Fisher", "expert", 3, 200, 62, 42))
    return skis


def get_skis(sample=False):
    """Returns a list of all skis in the database."""

    if sample:
        return sample_skis()

    conn = sqlite3.connect('ski.db')
    c = conn.cursor()
    c.execute("SELECT * FROM skis")
    tmp = c.fetchall()
    conn.close()
    skis = []
    for ski in tmp:
        skis.append(Ski(ski[1], ski[2], ski[3],
                    ski[4], ski[5], ski[6], ski[7]))
    return skis


class Engine():
    def __init__(self):
        self.skis: List[Ski] = get_skis()
        self.proficiencies = ["beginner", "intermediate", "advanced", "expert"]
        self.stiffness_classes = ["very soft",
                                  "soft", "medium", "stiff", "very stiff"]

    def filter_skis(self, stiffness: List[int], width: List[int], length: List[int], proficiency: List[str]):
        """Returns a list of skis that match the given parameters."""

        # create a list of all possible parameter combinations
        parameter_combinations = list(itertools.product(
            stiffness, width, length, proficiency))
        preliminary_recommendation = []
        # filter skis to match the given parameters
        for ski in self.skis:
            if type(ski.proficiency) == str:
                proficiency = self.proficiencies.index(ski.proficiency)
            else:
                proficiency = ski.proficiency
            if (ski.stiffness, ski.width, ski.length, proficiency) in parameter_combinations:
                preliminary_recommendation.append(ski)
        return preliminary_recommendation

    def generate_recommendation(self, user: User, ski_preference: SkiPreference):
        """Generates a recommendation based on the user's profile and the skis in the database."""

        stiffness_class = ski_preference.stiffness
        width = ski_preference.width
        weight = user.weight
        proficiency = self.proficiencies.index(user.proficiency)

        # Adjust stiffness and width based on user's bmi
        if user.bmi < 18.5:
            width -= 2
            stiffness_class -= 1
        elif user.bmi > 25:
            stiffness_class += 1
        elif user.bmi > 30:
            width += 2
            stiffness_class += 2

        # Adjust stiffness and width based on user's weight
        if weight < 60:
            width -= 1
            stiffness_class -= 1
        elif weight > 100:
            width += 1
            stiffness_class += 1

        # extend the parameters to include adjacent classes
        stiffness_range = [stiffness_class - 1,
                           stiffness_class, stiffness_class + 1]
        width_range = [_ for _ in range(int(width - 5), int(width + 5))]
        length_range = [_ for _ in range(
            int(user.ski_length - 5), int(user.ski_length + 5))]
        # generate a preliminary recommendation
        preliminary_recommendation = []
        while len(preliminary_recommendation) == 0:
            preliminary_recommendation = self.filter_skis(
                stiffness_range, width_range, length_range, [proficiency])
            if len(preliminary_recommendation) == 0:
                proficiency -= 1
                if proficiency < 0:
                    return []

        # sort the preliminary recommendation by similarity to the user's profile
        recommendation = sorted(
            preliminary_recommendation,
            key=lambda ski: abs(ski.stiffness - stiffness_class) + abs(ski.width - width) + abs(ski.length - user.ski_length))
        return recommendation

    def display_recommendation(self, recommendation: List[Ski]):
        """Displays the recommendation in a user-friendly way."""

        for ski in recommendation:
            out_str = ''
            out_str += f"{ski.manufacturer} "
            out_str += f"{ski.name} "
            out_str += f"length: {ski.length}cm "
            out_str += f"width: {ski.width}mm "
            out_str += f"stiffness: {self.stiffness_classes[ski.stiffness - 1]}"
            print(out_str)
