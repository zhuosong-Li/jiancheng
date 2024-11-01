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
                "packagingInfoId":entity.packaging_info_id,
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
                "totalQuantityInRatio": sum([entity.size_34_ratio,entity.size_35_ratio
                ,entity.size_36_ratio,entity.size_37_ratio,entity.size_38_ratio,entity.size_39_ratio,
                entity.size_40_ratio,entity.size_41_ratio,entity.size_42_ratio,entity.size_43_ratio,
                entity.size_44_ratio,entity.size_45_ratio,entity.size_46_ratio])
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
    packaging_info_name = request.json.get("packagingInfoName")
    packaging_info_locale = request.json.get("packagingInfoLocale")
    size_34_ratio = request.json.get("size34Ratio")
    size_35_ratio = request.json.get("size35Ratio")
    size_36_ratio = request.json.get("size36Ratio")
    size_37_ratio = request.json.get("size37Ratio")
    size_38_ratio = request.json.get("size38Ratio")
    size_39_ratio = request.json.get("size39Ratio")
    size_40_ratio = request.json.get("size40Ratio")
    size_41_ratio = request.json.get("size41Ratio")
    size_42_ratio = request.json.get("size42Ratio")
    size_43_ratio = request.json.get("size43Ratio")
    size_44_ratio = request.json.get("size44Ratio")
    size_45_ratio = request.json.get("size45Ratio")
    size_46_ratio = request.json.get("size46Ratio")
    total_quantity_ratio = sum([int(single_ratio) for single_ratio in [size_34_ratio,size_35_ratio
                ,size_36_ratio,size_37_ratio,size_38_ratio,size_39_ratio,
                size_40_ratio,size_41_ratio,size_42_ratio,size_43_ratio,
                size_44_ratio,size_45_ratio,size_46_ratio]])
    try:
        packaging_info_entity = PackagingInfo(
            customer_id=customer_id,
            packaging_info_name = packaging_info_name,
            packaging_info_locale = packaging_info_locale,
            size_34_ratio = size_34_ratio,
            size_35_ratio = size_35_ratio,
            size_36_ratio = size_36_ratio,
            size_37_ratio = size_37_ratio,
            size_38_ratio = size_38_ratio,
            size_39_ratio = size_39_ratio,
            size_40_ratio = size_40_ratio,
            size_41_ratio = size_41_ratio,
            size_42_ratio = size_42_ratio,
            size_43_ratio = size_43_ratio,
            size_44_ratio = size_44_ratio,
            size_45_ratio = size_45_ratio,
            size_46_ratio = size_46_ratio,
            total_quantity_ratio = total_quantity_ratio
        )
        db.session.add(packaging_info_entity)
        db.session.commit()
        return jsonify({"message": "Customer BatchInfo added successfully"})
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

@customer_bp.route("/customer/editbatchinfo", methods=["POST"])
def edit_packaging_info():
    packaging_info_id = request.json.get("packagingInfoId")
    packaging_info_name = request.json.get("packagingInfoName")
    packaging_info_locale = request.json.get("packagingInfoLocale")
    size_34_ratio = request.json.get("size34Ratio")
    size_35_ratio = request.json.get("size35Ratio")
    size_36_ratio = request.json.get("size36Ratio")
    size_37_ratio = request.json.get("size37Ratio")
    size_38_ratio = request.json.get("size38Ratio")
    size_39_ratio = request.json.get("size39Ratio")
    size_40_ratio = request.json.get("size40Ratio")
    size_41_ratio = request.json.get("size41Ratio")
    size_42_ratio = request.json.get("size42Ratio")
    size_43_ratio = request.json.get("size43Ratio")
    size_44_ratio = request.json.get("size44Ratio")
    size_45_ratio = request.json.get("size45Ratio")
    size_46_ratio = request.json.get("size46Ratio")
    total_quantity_ratio = sum([int(single_ratio) for single_ratio in [size_34_ratio,size_35_ratio
                ,size_36_ratio,size_37_ratio,size_38_ratio,size_39_ratio,
                size_40_ratio,size_41_ratio,size_42_ratio,size_43_ratio,
                size_44_ratio,size_45_ratio,size_46_ratio]])
    try:
        entity = PackagingInfo.query.filter_by(packaging_info_id=packaging_info_id).first()
        entity.packaging_info_name = packaging_info_name
        entity.packaging_info_locale = packaging_info_locale
        entity.size_34_ratio = size_34_ratio
        entity.size_35_ratio = size_35_ratio
        entity.size_36_ratio = size_36_ratio
        entity.size_37_ratio = size_37_ratio
        entity.size_38_ratio = size_38_ratio
        entity.size_39_ratio = size_39_ratio
        entity.size_40_ratio = size_40_ratio
        entity.size_41_ratio = size_41_ratio
        entity.size_42_ratio = size_42_ratio
        entity.size_43_ratio = size_43_ratio
        entity.size_44_ratio = size_44_ratio
        entity.size_45_ratio = size_45_ratio
        entity.size_46_ratio = size_46_ratio
        entity.total_quantity_ratio = total_quantity_ratio
        db.session.commit()
        return jsonify({"message": "Customer BatchInfo Updated Successfully"})
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

@customer_bp.route("/customer/deletebatchinfo", methods = ["DELETE"])
def delete_customer_batch():
    try:
        customer_id = request.args.get("customerId")
        packaging_info_id = request.args.get("packagingInfoId")
        batch_info_entity = db.session.query(PackagingInfo).filter(
            PackagingInfo.customer_id == customer_id,
            PackagingInfo.packaging_info_id == packaging_info_id).first()
        if not batch_info_entity:
            return jsonify({"status":"error", "message":"packaging info doesnt exist"})

        db.session.delete(batch_info_entity)
        db.session.commit()
        return jsonify({'status':'success'})

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error:{e}")
        return jsonify({"status":"error", "message" :str(e)}), 500
    finally:
        db.session.close()