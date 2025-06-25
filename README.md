## Quick start

```bash
git clone https://github.com/YourUser/techconnect-eai-demo.git
cd techconnect-eai-demo
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py   # API now on localhost:5000


# TechConnect EAI Demo

Lightweight demonstration of the Enterprise Application Integration (EAI) slice
described in the CIT6324 project report.  
This repo will contain:

* **backend** – Python 3.10 + Flask REST API (XML & JSON)
* **web**     – Static HTML + JavaScript UI
* **desktop** – Python desktop client (Tkinter)

## Quick start (backend)

```bash
git clone https://github.com/<YOUR-USER>/techconnect-eai-demo.git
cd techconnect-eai-demo

# Optional virtualenv
python -m venv venv && source venv/bin/activate

pip install -r backend/requirements.txt
python backend/app.py


### Day-2 demo

```bash
# Start API
python backend/app.py

# Create order (JSON)
curl -X POST -H "Content-Type: application/json" \
     -d @samples/order.json http://localhost:5000/api/orders

# Create order (XML)
curl -X POST -H "Content-Type: application/xml" \
     --data-binary @samples/order.xml http://localhost:5000/api/orders

# Record payment
curl -X POST -H "Content-Type: application/json" \
     -d '{"orderId":"<uuid>", "amount":199.99, "method":"card"}' \
     http://localhost:5000/api/payments

## Front-end demos (Day-3)

### Website
```bash
# backend running on port 5000
start "" web/index.html   # Windows


---

## Quick test checklist

1. **Backend running** (`python backend/app.py`)  
2. **Website** – open `web/index.html`, create order, check order-ID prints.  
3. **Desktop** – run `python desktop/gui.py`, paste order-ID, click *Make Payment*, then *Check Status* (status should change to `PAID`).  
4. Everything works → Day-3 complete.

Please copy the files, install **requests**, and run the quick tests.  
When both front-ends work, tell me **“website & desktop work”** and we’ll move to final polish (README badges, screenshots/GIF, Appendix snippet) tomorrow.

---

## Screenshots

| Website | Desktop |
|---------|---------|
| ![Web demo](docs/web_demo.png) | ![Desktop demo](docs/desktop_demo.png) |

## One-liner quick-start

```bash
git clone https://github.com/your-username/techconnect-eai-demo.git
cd techconnect-eai-demo
python -m venv venv && venv\Scripts\activate        # Unix: source venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py                               # open http://localhost:5000/ping
start "" web/index.html                             # Windows; open in browser
python desktop/gui.py                               # desktop client
