import threading


class Inventory:
    def __init__(self, stock):
        self.stock = stock
        self._lock = threading.Lock()

    def purchase(self, quantity=1):
        with self._lock:
            if self.stock < quantity:
                raise ValueError("Not enough stock")
            current = self.stock
            self.stock = current - quantity
            return True