import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from factories import PatientFactory
import pytest


@pytest.mark.dosage
def test_default_patient_has_no_allergies():
    """Test that a factory-created patient with default values has no allergies."""
    patient = PatientFactory()
    assert patient.has_allergy("penicillin") is False


@pytest.mark.dosage
def test_patient_with_specific_allergy():
    """Test overriding just the allergies field, everything else stays a valid default."""
    patient = PatientFactory(allergies=["penicillin"])
    assert patient.has_allergy("penicillin") is True
    assert isinstance(patient.name, str) and len(patient.name) > 0
    assert 1 <= patient.age <= 100
    assert 3 <= patient.weight_kg <= 150


@pytest.mark.dosage
def test_factory_generates_varied_names():
    """Test that the factory produces different names across multiple calls,
    proving the data is randomly generated rather than hardcoded."""
    patient_1 = PatientFactory()
    patient_2 = PatientFactory()
    assert patient_1.name != patient_2.name