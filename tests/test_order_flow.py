import requests, pytest

API = "http://localhost:5000"

@pytest.fixture(scope="module")
def order_id():
    payload = {"customer": "pytest", "total": 50.0, "currency": "MYR"}
    r = requests.post(API + "/api/orders", json=payload, timeout=3)
    assert r.status_code == 201
    return r.json()["orderId"]

def test_pay_and_status(order_id):
    pay = {"orderId": order_id, "amount": 50.0, "method": "card"}
    r = requests.post(API + "/api/payments", json=pay, timeout=3)
    assert r.status_code == 201

    r = requests.get(API + f"/api/orders/{order_id}", timeout=3)
    assert r.json()["status"] == "PAID"
