import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import InvalidTransitionError
import pytest


def test_valid_transition(new_order):
    """Test that a single legal status transition succeeds."""
    new_order.transition_to("accepted")
    assert new_order.status == "accepted"


def test_invalid_transition_raises(new_order):
    """Test that an illegal status transition raises InvalidTransitionError."""
    with pytest.raises(InvalidTransitionError):
        new_order.transition_to("completed")


@pytest.mark.parametrize("from_status, to_status", [
    ("created", "accepted"),
    ("created", "cancelled"),
    ("accepted", "preparing"),
    ("preparing", "delivering"),
])
def test_valid_transitions_parametrized(from_status, to_status, new_order):
    """Test multiple legal transitions in one parametrized test."""
    new_order.status = from_status
    new_order.transition_to(to_status)
    assert new_order.status == to_status


@pytest.mark.parametrize("from_status, to_status", [
    ("created", "completed"),
    ("created", "delivering"),
    ("accepted", "completed"),
    ("completed", "accepted"),
    ("cancelled", "accepted"),
])
def test_invalid_transitions_parametrized(from_status, to_status, new_order):
    """Test multiple illegal transitions all raise InvalidTransitionError."""
    new_order.status = from_status
    with pytest.raises(InvalidTransitionError):
        new_order.transition_to(to_status)