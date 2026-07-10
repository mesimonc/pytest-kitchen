import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import Order, InvalidTransitionError
import pytest


def test_valid_transition():
    order = Order()
    order.transition_to("accepted")
    assert order.status == "accepted"


def test_invalid_transition_raises():
    order = Order()
    with pytest.raises(InvalidTransitionError):
        order.transition_to("completed")