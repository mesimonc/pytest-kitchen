import sys
import os
from hypothesis import given, strategies as st

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

@pytest.mark.dosage
@pytest.mark.skip(reason="Extreme low-weight neonatal dosing not yet supported")
def test_dosage_for_extremely_low_weight_neonate():
    """Test dosage calculation for neonates under 1kg (not yet implemented)."""
    result = calc_dosage(weight_kg=0.5, mg_per_kg=2, max_safe_mg=1)
    assert result == 1


@pytest.mark.dosage
@pytest.mark.xfail(reason="Known floating point precision issue with repeated small additions")
def test_dosage_floating_point_precision_known_bug():
    """Test that reveals a known floating-point precision bug with tiny weights."""
    weight = 0.1 + 0.1 + 0.1  # classic float precision trap: not exactly 0.3
    result = calc_dosage(weight_kg=weight, mg_per_kg=1, max_safe_mg=100)
    assert result == 0.3

@pytest.mark.dosage
@given(
    weight_kg=st.floats(min_value=0.1, max_value=500, allow_nan=False),
    mg_per_kg=st.floats(min_value=0.1, max_value=50, allow_nan=False),
)
def test_dosage_is_always_positive_for_valid_weight(weight_kg, mg_per_kg):
    """Property: for any valid positive weight and mg_per_kg,
    the calculated dosage (before hitting max_safe_mg) should always be positive."""
    max_safe_mg = weight_kg * mg_per_kg + 1  # deliberately set high enough to avoid DosageError
    result = calc_dosage(weight_kg=weight_kg, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    assert result > 0


@pytest.mark.dosage
@given(
    weight_kg=st.floats(min_value=0.1, max_value=500, allow_nan=False),
    mg_per_kg=st.floats(min_value=0.1, max_value=50, allow_nan=False),
)
def test_dosage_scales_linearly_with_weight(weight_kg, mg_per_kg):
    """Property: doubling the weight should exactly double the dosage.
    (This assumption is naive and will likely be broken by hypothesis.)"""
    max_safe_mg = weight_kg * mg_per_kg * 3  # generous ceiling
    dosage_1x = calc_dosage(weight_kg=weight_kg, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    dosage_2x = calc_dosage(weight_kg=weight_kg * 2, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    assert dosage_2x == dosage_1x * 2


@pytest.mark.dosage
@given(
    weight_kg=st.floats(min_value=0.1, max_value=500, allow_nan=False),
    mg_per_kg=st.floats(min_value=0.1, max_value=50, allow_nan=False),
)
def test_dosage_is_additive_across_split_weight(weight_kg, mg_per_kg):
    """Property: splitting the weight into two halves and summing their
    dosages should equal the dosage for the full weight.
    (Naive assumption, likely broken by floating point rounding.)"""
    max_safe_mg = weight_kg * mg_per_kg * 3
    half = weight_kg / 2
    dosage_half_1 = calc_dosage(weight_kg=half, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    dosage_half_2 = calc_dosage(weight_kg=weight_kg - half, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    dosage_full = calc_dosage(weight_kg=weight_kg, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    assert dosage_half_1 + dosage_half_2 == dosage_full


@pytest.mark.dosage
@given(
    weight_kg=st.floats(min_value=0.3, max_value=500, allow_nan=False),
    mg_per_kg=st.floats(min_value=0.1, max_value=50, allow_nan=False),
)
def test_dosage_is_additive_across_thirds(weight_kg, mg_per_kg):
    """Property: splitting weight into three equal thirds and summing their
    dosages should equal the dosage for the full weight.
    (Naive assumption — division by 3 in binary floating point is imprecise.)"""
    max_safe_mg = weight_kg * mg_per_kg * 4
    third = weight_kg / 3
    dosage_third = calc_dosage(weight_kg=third, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    dosage_full = calc_dosage(weight_kg=weight_kg, mg_per_kg=mg_per_kg, max_safe_mg=max_safe_mg)
    assert abs(dosage_third * 3 - dosage_full) < 1e-9