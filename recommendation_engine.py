import itertools
from typing import List
from base_classes import *
import sqlite3
import numpy as np


def get_skis():
    """Returns a list of all skis in the database."""

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

    def filter_skis(self, stiffness: List[int], width: List[int], length: List[int], proficiency: List[str]):
        """Returns a list of skis that match the given parameters."""

        # create a list of all possible parameter combinations
        parameter_combinations = np.array(itertools.product(
            stiffness, width, length, proficiency))
        preliminary_recommendation = []
        # filter skis to match the given parameters
        for ski in self.skis:
            if [ski.stiffness, ski.width, ski.length, ski.proficiency] in parameter_combinations:
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
            width -= 1
            stiffness_class -= 1
        elif user.bmi > 25:
            width += 1
            stiffness_class += 1
        elif user.bmi > 30:
            width += 2
            stiffness_class += 2

        # Adjust stiffness and width based on user's weight
        if weight < 50:
            width -= 1
            stiffness_class -= 1
        elif weight > 100:
            width += 1
            stiffness_class += 1

        # extend the parameters to include adjacent classes
        stiffness = [stiffness_class - 1, stiffness_class, stiffness_class + 1]
        width = [width - 1, width, width + 1]
        length = [
            ski_len for ski_len in range(int(user.ski_length - 3), int(user.ski_length + 3))
        ]
        # generate a preliminary recommendation
        preliminary_recommendation = []
        while len(preliminary_recommendation) == 0:
            preliminary_recommendation = self.filter_skis(
                stiffness, width, length, [proficiency])
            length = [
                ski_len for ski_len in range(int(user.ski_length - 5), int(user.ski_length + 5))
            ]
            if len(preliminary_recommendation) == 0:
                proficiency -= 1
                if proficiency < 0:
                    return []

        # sort the preliminary recommendation by similarity to the user's profile
        recommendation = sorted(
            preliminary_recommendation,
            key=lambda ski: abs(ski.stiffness - stiffness_class) + abs(ski.width - width) + abs(ski.length - user.ski_length))
        return recommendation