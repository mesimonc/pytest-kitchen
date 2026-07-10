import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import Order, InvalidTransitionError
import pytest


def test_valid_transition():
    """Test that a single legal status transition succeeds."""
    order = Order()
    order.transition_to("accepted")
    assert order.status == "accepted"


def test_invalid_transition_raises():
    """Test that an illegal status transition raises InvalidTransitionError."""
    order = Order()
    with pytest.raises(InvalidTransitionError):
        order.transition_to("completed")


@pytest.mark.parametrize("from_status, to_status", [
    ("created", "accepted"),
    ("created", "cancelled"),
    ("accepted", "preparing"),
    ("preparing", "delivering"),
])
def test_valid_transitions_parametrized(from_status, to_status):
    """Test multiple legal transitions in one parametrized test."""
    order = Order()
    order.status = from_status
    order.transition_to(to_status)
    assert order.status == to_status


@pytest.mark.parametrize("from_status, to_status", [
    ("created", "completed"),      # can't skip straight to completed
    ("created", "delivering"),     # can't skip straight to delivering
    ("accepted", "completed"),     # can't skip preparing/delivering
    ("completed", "accepted"),     # completed is a final state
    ("cancelled", "accepted"),     # cancelled is a final state
])
def test_invalid_transitions_parametrized(from_status, to_status):
    """Test multiple illegal transitions all raise InvalidTransitionError."""
    order = Order()
    order.status = from_status
    with pytest.raises(InvalidTransitionError):
        order.transition_to(to_status)