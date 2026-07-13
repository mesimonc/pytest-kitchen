import sys
import os
from unittest.mock import MagicMock
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from payment import PaymentProcessor

@pytest.mark.payment
def test_first_callback_charges_once():
    """Test that the first callback for a payment_id triggers a charge."""
    fake_gateway = MagicMock()
    processor = PaymentProcessor(fake_gateway)

    processor.handle_payment_callback(payment_id="pay_123", amount=50)

    # Fill in the argument the gateway.charge method should have been called with
    fake_gateway.charge.assert_called_once_with(50)

@pytest.mark.payment
def test_duplicate_callback_does_not_charge_twice():
    """Test that a duplicate callback with the same payment_id is idempotent."""
    fake_gateway = MagicMock()
    processor = PaymentProcessor(fake_gateway)

    processor.handle_payment_callback(payment_id="pay_123", amount=50)
    # Simulate the gateway retrying with the exact same payment_id and amount
    processor.handle_payment_callback(payment_id="pay_123", amount=50)

    # Key assertion: even though handle_payment_callback was called twice,
    # gateway.charge should have only been actually invoked once
    assert fake_gateway.charge.call_count == 1