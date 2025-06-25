"""
Very small in-memory DAO for demo purposes only.
In production you would replace these with database calls.
"""

from uuid import uuid4
from datetime import datetime, timezone

# orderId ➜ record dict
_DB: dict[str, dict] = {}


def create_order(customer: str, total: float, currency: str = "MYR") -> dict:
    order_id = str(uuid4())
    record = {
        "orderId": order_id,
        "customer": customer,
        "total": total,
        "currency": currency,
        "status": "CREATED",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    _DB[order_id] = record
    return record


def get_order(order_id: str) -> dict | None:
    return _DB.get(order_id)


def pay_order(order_id: str, amount: float, method: str) -> dict:
    order = _DB.get(order_id)
    if not order:
        raise KeyError("order not found")
    if amount != order["total"]:
        raise ValueError("amount mismatch")
    order["status"] = "PAID"
    order["paymentMethod"] = method
    order["paidAt"] = datetime.now(timezone.utc).isoformat()
    return order

# ------------------------------------------------------------------ #
# compatibility alias for app.py
def record_payment(order_id: str, amount: float, method: str) -> dict:
    """app.py expects record_payment; re-use pay_order implementation."""
    return pay_order(order_id, amount, method)
