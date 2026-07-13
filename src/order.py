from datetime import datetime, timedelta


class InvalidTransitionError(Exception):
    pass


class Order:
    VALID_TRANSITIONS = {
        "created": ["accepted", "cancelled"],
        "accepted": ["preparing", "cancelled"],
        "preparing": ["delivering"],
        "delivering": ["completed"],
        "completed": [],
        "cancelled": [],
    }

    TIMEOUT_MINUTES = 15

    def __init__(self):
        self.status = "created"
        self.created_at = datetime.now()

    def transition_to(self, new_status):
        if new_status not in self.VALID_TRANSITIONS[self.status]:
            raise InvalidTransitionError(
                f"Cannot transition from '{self.status}' to '{new_status}'"
            )
        self.status = new_status

    def check_timeout(self):
        """
        Automatically cancel the order if it has been sitting in 'created'
        status for longer than TIMEOUT_MINUTES.
        """
        if self.status != "created":
            return

        elapsed = datetime.now() - self.created_at
        if elapsed > timedelta(minutes=self.TIMEOUT_MINUTES):
            self.status = "cancelled"