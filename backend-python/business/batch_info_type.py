from flask import Blueprint, jsonify, request
from models import *
from api_utility import to_camel, to_snake


from app_config import app, db

batch_type_bp = Blueprint("batch_type_bp", __name__)
TABLE_ATTRNAMES = BatchInfoType.__table__.columns.keys()


def get_order_batch_type_helper(order_id):
    # get batch info type (US, EU)
    shoe_size_locale = (
        db.session.query(BatchInfoType)
        .join(Order, BatchInfoType.batch_info_type_id == Order.batch_info_type_id)
        .filter(Order.order_id == order_id)
        .first()
    )
    result = []
    for i in range(34, 47):
        locale = getattr(shoe_size_locale, f"size_{i}_name")
        type_name = getattr(shoe_size_locale, f"batch_info_type_name")
        if locale:
            obj = {"prop": f"size{i}Amount", "label": locale, "type": type_name}
            result.append(obj)
        if locale == None:
            break
    return result


@batch_type_bp.route("/batchtype/getallbatchtypes", methods=["GET"])
def get_all_batch_types():
    entities = db.session.query(BatchInfoType).all()
    response_list = []
    attr_names = TABLE_ATTRNAMES

    for entity in entities:
        result = {}
        for db_attr in attr_names:
            if getattr(entity, db_attr) == "":
                result[to_camel(db_attr)] = None
            else:
                result[to_camel(db_attr)] = getattr(entity, db_attr,None)
        response_list.append(result)
    return jsonify({"batchDataTypes": response_list}), 200


@batch_type_bp.route("/batchtype/getorderbatchtype", methods=["GET"])
def get_order_batch_type():
    order_id = request.args.get("orderId")
    result = get_order_batch_type_helper(order_id)
    return result
@batch_type_bp.route("/batchtype/addbatchtype", methods=["POST"])
def add_batch_type():
    batch_info_type_name = request.args.get("batchInfoTypeName")
    db_entity = BatchInfoType()
    for attr in TABLE_ATTRNAMES:
        print(attr, request.json.get(to_camel(attr)))
        setattr(db_entity, attr, request.json.get(to_camel(attr)))
        db_entity.batch_info_type_id = None
    db.session.add(db_entity)
    db.session.commit() 
    # for attr in TABLE_ATTRNAMES:
        
    return jsonify({"message":"123"}), 200


@batch_type_bp.route("/batchtype/deletebatchtype", methods=["DELETE"])
def delete_batch_type():
    batch_type_id = request.args.get("batchTypeId")
    db.session.execute(db.delete(BatchInfoType).filter_by(batch_info_type_id = batch_type_id))
    db.session.commit()
    return jsonify({"msg":"deleted"}), 200