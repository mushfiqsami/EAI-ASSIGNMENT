import requests
API = "http://localhost:5000"

def test_ping():
    r = requests.get(API + "/ping", timeout=2)
    assert r.status_code == 200
    assert r.json() == {"status": "pong"}
