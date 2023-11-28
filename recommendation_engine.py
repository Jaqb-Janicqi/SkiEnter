import itertools
from typing import List
from base_classes import *
import sqlite3


def sample_skis():
    brand_ski_tuples = [
        ("Atomic", "Redster S9"),
        ("Rossignol", "Attraxion"),
        ("Rossignol", "Forza 20D"),
        ("Fisher", "MCK Sport"),
        ("Fisher", "MCK Casual")
    ]
    stiffness = [1, 2, 3, 4, 5]
    width = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
    length = [150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200]
    proficiency = ["beginner", "intermediate", "advanced", "expert"]
    parameter_combinations = list(itertools.product(
        stiffness, width, length, proficiency))
    skis = []
    for brand, name in brand_ski_tuples:
        for stiffness, width, length, proficiency in parameter_combinations:
            skis.append(Ski(name, brand, proficiency,
                            stiffness, length, width, 0))
    # clear all skis from the database
    conn = sqlite3.connect('SkiEnter_database.db')
    c = conn.cursor()
    c.execute(
        """
        DELETE * FROM skis;
        """
    )
    conn.commit()

    # add all skis to the database
    for ski in skis:
        c.execute(
            """
            INSERT INTO skis (name, manufacturer, proficiency, stiffness, length, width)
            VALUES (?, ?, ?, ?, ?, ?);
            """,
            (ski.name, ski.manufacturer, ski.proficiency,
             ski.stiffness, ski.length, ski.width)
        )
    conn.commit()

    c.execute(
        """ 
        select count(*) from skis;
        """
    )
    print(c.fetchall())
    return skis


def get_skis():
    """Returns a list of all skis in the database."""

    conn = sqlite3.connect('SkiEnter_database.db')
    c = conn.cursor()
    c.execute(
        """
        SELECT DISTINCT name, manufacturer, proficiency, stiffness, length, width, ski_number FROM Skis
        JOIN Skis_item as item ON item.ski_ID = Skis.ski_number
        WHERE is_available = 1;
        """
    )
    tmp = c.fetchall()
    conn.close()
    skis = []
    for ski in tmp:
        skis.append(Ski(ski[0], ski[1], ski[2],
                    ski[3], ski[4], ski[5], ski[6]))
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
        width_range = [_ for _ in range(int(width - 10), int(width + 10))]
        length_range = [_ for _ in range(
            int(user.ski_length - 10), int(user.ski_length + 10))]
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


if __name__ == "__main__":
    engine = Engine()
    user = User("John", "Doe", 25, " ", " ", 80, 180, "advanced")
    ski_preference = SkiPreference(user, 3, 90)
    recommendation = engine.generate_recommendation(user, ski_preference)
    engine.display_recommendation(recommendation)
