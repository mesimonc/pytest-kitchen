from locust import HttpUser, task, between


class OrderUser(HttpUser):
    """Simulates a user repeatedly creating orders against the API."""

    wait_time = between(0.1, 0.5)  # simulate a small pause between requests, like a real user

    @task
    def create_order(self):
        self.client.post("/orders", json={"customer_name": "Load Test User"})

    @task
    def get_order(self):
        self.client.get("/orders/1")