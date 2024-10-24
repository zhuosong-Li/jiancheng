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

@customer_bp.route("/customer/getcustomerbatchinfo", methods=["GET"])
def get_customer_batch_info():
    customer_id = request.args.get("customerid")
    entities = (db.session.query(PackagingInfo)
                .filter(PackagingInfo.customer_id == customer_id)
                .all())
    result = []
    for entity in entities:
        result.append(
            {
                "packagingInfoName":entity.packaging_info_name,
                "packagingInfoLocale":entity.packaging_info_locale,
                "size34Ratio":entity.size_34_ratio,
                "size35Ratio":entity.size_35_ratio,
                "size36Ratio":entity.size_36_ratio,
                "size37Ratio":entity.size_37_ratio,
                "size38Ratio":entity.size_38_ratio,
                "size39Ratio":entity.size_39_ratio,
                "size40Ratio":entity.size_40_ratio,
                "size41Ratio":entity.size_41_ratio,
                "size42Ratio":entity.size_42_ratio,
                "size43Ratio":entity.size_43_ratio,
                "size44Ratio":entity.size_44_ratio,
                "size45Ratio":entity.size_45_ratio,
                "size46Ratio":entity.size_46_ratio,
            }
        )
    print(result)
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
    
@customer_bp.route("/customer/addcustomerbatchinfo", methods=["POST"])
def add_customer_batch_info():
    customer_id = request.json.get("customerId")
    packaging_info_name = request.json.get("batchName")
    packaging_info_locale = request.json.get("batchLocale")
    size_34_ratio = request.json.get("batchQuantity34")
    size_35_ratio = request.json.get("batchQuantity35")
    size_36_ratio = request.json.get("batchQuantity36")
    size_37_ratio = request.json.get("batchQuantity37")
    size_38_ratio = request.json.get("batchQuantity38")
    size_39_ratio = request.json.get("batchQuantity39")
    size_40_ratio = request.json.get("batchQuantity40")
    size_41_ratio = request.json.get("batchQuantity41")
    size_42_ratio = request.json.get("batchQuantity42")
    size_43_ratio = request.json.get("batchQuantity43")
    size_44_ratio = request.json.get("batchQuantity44")
    size_45_ratio = request.json.get("batchQuantity45")
    size_46_ratio = request.json.get("batchQuantity46")
    try:
        packaging_info_entity = PackagingInfo(
            customer_id=customer_id,
            packaging_info_name = packaging_info_name,
            packaging_info_locale = packaging_info_locale,
            size_34_ratio= size_34_ratio,
            size_35_ratio= size_35_ratio,
            size_36_ratio= size_36_ratio,
            size_37_ratio= size_37_ratio,
            size_38_ratio= size_38_ratio,
            size_39_ratio= size_39_ratio,
            size_40_ratio= size_40_ratio,
            size_41_ratio= size_41_ratio,
            size_42_ratio= size_42_ratio,
            size_43_ratio= size_43_ratio,
            size_44_ratio= size_44_ratio,
            size_45_ratio= size_45_ratio,
            size_46_ratio= size_46_ratio
        )
        print(packaging_info_entity)
        db.session.add(packaging_info_entity)
        db.session.commit()
        return jsonify({"message": "Customer BatchInfo added successfully"})
    except Exception as e:
        print(str(e))
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

