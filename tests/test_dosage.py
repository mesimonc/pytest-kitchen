import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dosage import calc_dosage, DosageError
import pytest

@pytest.mark.dosage
def test_normal_dosage_within_safe_range():
    """Test that a dosage within the safe range returns the correct value."""
    result = calc_dosage(weight_kg=10, mg_per_kg=5, max_safe_mg=100)
    assert result == 50

@pytest.mark.dosage
def test_dosage_exceeds_max_raises_dosage_error():
    """Test that a dosage over the safe max raises DosageError."""
    with pytest.raises(DosageError):
        calc_dosage(weight_kg=30, mg_per_kg=5, max_safe_mg=100)

@pytest.mark.dosage
def test_dosage_exactly_at_max_does_not_raise():
    """Boundary test: dosage exactly equal to max_safe_mg should NOT raise,
    because the check in calc_dosage uses '>' not '>='."""
    result = calc_dosage(weight_kg=20, mg_per_kg=5, max_safe_mg=100)
    assert result == 100

@pytest.mark.dosage
@pytest.mark.parametrize("weight_kg", [0, -5, -0.1])
def test_invalid_weight_raises_value_error(weight_kg):
    """Test that zero or negative weight raises ValueError."""
    with pytest.raises(ValueError):
        calc_dosage(weight_kg=weight_kg, mg_per_kg=5, max_safe_mg=100)

@pytest.mark.dosage
def test_dosage_just_one_unit_over_max_raises():
    """Boundary test: dosage exceeding max by the smallest margin still raises."""
    with pytest.raises(DosageError):
        calc_dosage(weight_kg=20.02, mg_per_kg=5, max_safe_mg=100)