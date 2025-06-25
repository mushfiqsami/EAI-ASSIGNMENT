
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import models
from xml_utils import validate_xml   
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)  


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


    @app.post("/api/orders")
    def create_order():
        
        if request.content_type.startswith("application/json"):
            data = request.get_json(force=True)
        else:
            
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

   
    @app.post("/api/payments")
    def make_payment():
        
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
        except ValueError as exc:         
            return jsonify(error=str(exc)), 400
        except KeyError:                  
            return jsonify(error="order not found"), 404

        if request.content_type.startswith("application/xml"):
            xml_resp = (
                '<?xml version="1.0"?>\n'
                f'<paymentId>{payment["paymentId"]}</paymentId>'
            )
            return make_response(xml_resp, 201, {"Content-Type": "application/xml"})

        return jsonify(payment), 201

    
    return app



if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
