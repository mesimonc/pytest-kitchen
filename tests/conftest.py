import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from order import Order
import pytest


@pytest.fixture
def new_order():
    """Provide a fresh Order instance in the default 'created' state."""
    return Order()