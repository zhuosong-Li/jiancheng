from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

customer_bp = Blueprint("customer_bp", __name__)

@customer_bp.route("/customer/getallcustomers", methods=["GET"])
def get_all_customers():
    customers = Customer.query.all()
    result = []
    for customer in customers:
        result.append(
            {
                "value": customer.customer_id,
                "label": customer.customer_name,
            }
        )
    return jsonify(result)

@customer_bp.route("/customer/getcustomerdetails", methods=["GET"])
def get_customer_details():
    customers = Customer.query.all()
    result = []
    for customer in customers:
        result.append(
            {
                "customerId": customer.customer_id,
                "customerName": customer.customer_name,
                "customerBrand": customer.customer_brand,
            }
        )
    return jsonify(result)

@customer_bp.route("/customer/addcustomer", methods=["POST"])
def add_customer():
    customer_name = request.json.get("customerName")
    customer_brand = request.json.get("customerBrand")
    try:
        customer = Customer(
            customer_name=customer_name,
            customer_brand=customer_brand,
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({"message": "Customer added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@customer_bp.route("/customer/editcustomer", methods=["POST"])
def edit_customer():
    customer_id = request.json.get("customerId")
    customer_name = request.json.get("customerName")
    customer_brand = request.json.get("customerBrand")
    try:
        customer = Customer.query.filter_by(customer_id=customer_id).first()
        customer.customer_name = customer_name
        customer.customer_brand = customer_brand
        db.session.commit()
        return jsonify({"message": "Customer updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

