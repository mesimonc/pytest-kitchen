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

    def __init__(self):
        self.status = "created"

    def transition_to(self, new_status):
        if new_status not in self.VALID_TRANSITIONS[self.status]:
            raise InvalidTransitionError(
                f"Cannot transition from {self.status} to {new_status}"
            )
        self.status = new_status