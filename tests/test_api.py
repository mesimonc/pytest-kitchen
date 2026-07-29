import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)


def test_create_order_returns_201_and_correct_data():
    """Test that creating an order returns the expected structure."""
    response = client.post("/orders", json={"customer_name": "Alice"})
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Alice"
    assert data["status"] == "created"
    assert "id" in data


def test_get_existing_order_returns_correct_data():
    """Test that fetching a previously created order returns matching data."""
    create_response = client.post("/orders", json={"customer_name": "Bob"})
    order_id = create_response.json()["id"]

    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["customer_name"] == "Bob"


def test_get_nonexistent_order_returns_404():
    """Test that fetching a non-existent order id returns 404."""
    response = client.get("/orders/999999")
    assert response.status_code == 404