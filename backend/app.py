"""
Flask API – TechConnect EAI demo
--------------------------------
POST /api/orders        (JSON or XML) ➜ returns full order (incl. orderId)
GET  /api/orders/<id>               ➜ returns order (404 if not found)
POST /api/payments      (JSON or XML) ➜ returns payment receipt
"""

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import models
from xml_utils import validate_xml   # helper already in backend/xml_utils.py


# -----------------------------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  # allow requests from the simple HTML page & desktop client

    # ------------------------------------------------------------------ #
    # Health / meta
    # ------------------------------------------------------------------ #
    @app.get("/")
    def index():
        return {
            "message": "TechConnect EAI Demo API",
            "endpoints": {
                "ping":     "/ping",
                "orders":   "/api/orders",
                "payments": "/api/payments",
            },
        }

    @app.get("/ping")
    def ping():
        """Simple health-probe used by pytest."""
        return jsonify(status="pong")

    # ------------------------------------------------------------------ #
    # Orders
    # ------------------------------------------------------------------ #
    @app.post("/api/orders")
    def create_order():
        """
        Accepts JSON:
            {
              "customer": "Alice",
              "total": 99.9,
              "currency": "MYR"
            }
        or XML that conforms to schemas/order.xsd.
        Always returns the newly-created order (JSON or XML).
        """
        if request.content_type.startswith("application/json"):
            data = request.get_json(force=True)
        else:
            # XML branch
            xml_root = validate_xml(request.data, "order.xsd")
            data = {
                "customer": xml_root.findtext("customer"),
                "total":    xml_root.findtext("total"),
                "currency": xml_root.findtext("currency"),
            }

        order = models.create_order(
            customer = data["customer"],
            total    = float(data["total"]),
            currency = data.get("currency", "MYR"),
        )

        # Echo back the CREATED order in the same media-type received
        if request.content_type.startswith("application/xml"):
            xml_resp = (
                '<?xml version="1.0"?>\n'
                f'<orderId>{order["orderId"]}</orderId>'
            )
            return make_response(xml_resp, 201, {"Content-Type": "application/xml"})

        return jsonify(order), 201

    @app.get("/api/orders/<order_id>")
    def get_order(order_id: str):
        order = models.get_order(order_id)
        if not order:
            return jsonify(error="order not found"), 404
        return jsonify(order)

    # ------------------------------------------------------------------ #
    # Payments
    # ------------------------------------------------------------------ #
    @app.post("/api/payments")
    def make_payment():
        """
        Accepts JSON:
            {
              "orderId": "<uuid>",
              "amount": 99.9,
              "method": "card"
            }
        or XML conforming to schemas/payment.xsd.
        """
        if request.content_type.startswith("application/json"):
            data = request.get_json(force=True)
        else:
            xml_root = validate_xml(request.data, "payment.xsd")
            data = {
                "orderId": xml_root.findtext("orderId"),
                "amount":  xml_root.findtext("amount"),
                "method":  xml_root.findtext("method") or "card",
            }

        try:
            payment = models.record_payment(
                order_id = data["orderId"],
                amount   = float(data["amount"]),
                method   = data.get("method", "card"),
            )
        except ValueError as exc:         # e.g., amount mismatch
            return jsonify(error=str(exc)), 400
        except KeyError:                  # order not found
            return jsonify(error="order not found"), 404

        if request.content_type.startswith("application/xml"):
            xml_resp = (
                '<?xml version="1.0"?>\n'
                f'<paymentId>{payment["paymentId"]}</paymentId>'
            )
            return make_response(xml_resp, 201, {"Content-Type": "application/xml"})

        return jsonify(payment), 201

    # ------------------------------------------------------------------ #
    return app


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
