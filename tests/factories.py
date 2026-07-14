import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import factory
from patient import Patient


class PatientFactory(factory.Factory):
    class Meta:
        model = Patient

    name = factory.Faker("name")
    age = factory.Faker("random_int", min=1, max=100)
    weight_kg = factory.Faker("pyfloat", min_value=3, max_value=150, right_digits=1, positive=True)
    allergies = factory.List([])