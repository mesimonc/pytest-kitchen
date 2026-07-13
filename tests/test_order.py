import sys
import os
from freezegun import freeze_time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import InvalidTransitionError
import pytest

@pytest.mark.order
def test_valid_transition(new_order):
    """Test that a single legal status transition succeeds."""
    new_order.transition_to("accepted")
    assert new_order.status == "accepted"

@pytest.mark.order
def test_invalid_transition_raises(new_order):
    """Test that an illegal status transition raises InvalidTransitionError."""
    with pytest.raises(InvalidTransitionError):
        new_order.transition_to("completed")

@pytest.mark.order
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

@pytest.mark.order
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

@pytest.mark.order
def test_order_not_timed_out_before_15_minutes(new_order):
    """Test that an order is NOT cancelled if less than 15 minutes have passed."""
    with freeze_time(datetime.now() + timedelta(minutes=10)):
        new_order.check_timeout()
    assert new_order.status == "created"
@pytest.mark.order
def test_order_timed_out_after_15_minutes(new_order):
    """Test that an order is cancelled if more than 15 minutes have passed."""
    with freeze_time(datetime.now() + timedelta(minutes=16)):
        new_order.check_timeout()
    assert new_order.status == "cancelled"

@pytest.mark.order
def test_check_timeout_does_nothing_if_not_created(new_order):
    """Test that check_timeout has no effect once the order has left 'created' status."""
    new_order.transition_to("accepted")

    with freeze_time(datetime.now() + timedelta(minutes=999)):
        new_order.check_timeout()

    assert new_order.status == "accepted"