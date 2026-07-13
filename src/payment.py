class PaymentProcessor:
    def __init__(self, gateway):
        self.gateway = gateway
        self.processed_payment_ids = set()

    def handle_payment_callback(self, payment_id, amount):
        """
        Handle a payment confirmation callback from the external gateway.
        Must be idempotent: if the same payment_id arrives twice,
        the second call must NOT charge again.
        """
        if payment_id in self.processed_payment_ids:
            return {"status": "already_processed", "payment_id": payment_id}

        result = self.gateway.charge(amount)
        self.processed_payment_ids.add(payment_id)
        return {"status": "charged", "payment_id": payment_id, "result": result}