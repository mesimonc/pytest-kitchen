import sys
import os
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from inventory import Inventory


def test_concurrent_purchases_can_oversell_without_lock():
    """Demonstrate a real race condition: two threads buying the last item
    concurrently can BOTH succeed, oversell ing the single unit of stock."""
    inventory = Inventory(stock=1)
    results = []

    def try_purchase():
        try:
            inventory.purchase(1)
            results.append("success")
        except ValueError:
            results.append("failed")

    thread_1 = threading.Thread(target=try_purchase)
    thread_2 = threading.Thread(target=try_purchase)

    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()

    success_count = results.count("success")
    assert success_count == 1, (
        f"Expected exactly 1 successful purchase, but got {success_count} "
        f"(final stock={inventory.stock}) — this demonstrates a race condition"
    )