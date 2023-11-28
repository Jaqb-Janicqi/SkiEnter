class User():
    def __init__(self, name, surname, age, email, password, weight, height, proficiency):
        self.name = name
        self.surname = surname
        self.age = age
        self.email = email
        self.password = password
        self.weight = weight
        self.height = height
        self.proficiency = proficiency

    @property
    def bmi(self):
        return self.weight / (self.height / 100) ** 2

    @property
    def ski_length(self):
        return self.height * 0.95


class SkiPreference():
    def __init__(self, user, stiffness, width):
        self.user = user
        self.stiffness = stiffness
        self.width = width


class Ski():
    def __init__(self, name, manufacturer, proficiency, stiffness, length, width, ski_number):
        self.name = name
        self.manufacturer = manufacturer
        self.proficiency = proficiency
        self.stiffness = stiffness
        self.length = length
        self.width = width
        self.ski_number = ski_number
