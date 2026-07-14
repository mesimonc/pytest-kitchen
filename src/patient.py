class Patient:
    def __init__(self, name, age, weight_kg, allergies=None):
        self.name = name
        self.age = age
        self.weight_kg = weight_kg
        self.allergies = allergies or []

    def has_allergy(self, drug_name):
        return drug_name in self.allergies