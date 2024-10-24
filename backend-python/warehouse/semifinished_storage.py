import datetime
from decimal import Decimal

from app_config import db
from constants import (
    END_OF_PRODUCTION_NUMBER,
    IN_PRODUCTION_ORDER_NUMBER,
    PRODUCTION_LINE_REFERENCE,
    SHOESIZEINFO,
)
from event_processor import EventProcessor
from flask import Blueprint, current_app, jsonify, request
from models import *
from sqlalchemy import func, or_, and_

semifinished_storage_bp = Blueprint("semifinished_storage_bp", __name__)


@semifinished_storage_bp.route(
    "/warehouse/warehousemanager/getsemifinishedinoutoverview", methods=["GET"]
)
def get_semifinished_in_out_overview():
    """
    op_type: 0 means show all orders, 1 means show active orders
    """
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    op_type = request.args.get("opType", default=0, type=int)

    query = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            func.sum(OrderShoeBatchInfo.total_amount).label("total_amount"),
            SemifinishedShoeStorage,
        )
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(
            SemifinishedShoeStorage,
            SemifinishedShoeStorage.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .group_by(OrderShoe.order_shoe_id, SemifinishedShoeStorage.semifinished_shoe_id)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if op_type != 0:
        query = query.filter(SemifinishedShoeStorage.semifinished_status != 2)
    count_result = query.distinct().count()
    response = query.limit(number).offset((page - 1) * number).all()
    result = []
    for row in response:
        (order, order_shoe, shoe, total_amount, storage_obj) = row
        if storage_obj.semifinished_status == 0:
            status_name = "未完成入库"
        elif storage_obj.semifinished_status == 1:
            status_name = "已完成入库"
        else:
            status_name = "已完成出库"
        if storage_obj.semifinished_object == 0:
            object = "裁断后材料"
        else:
            object = "鞋包"
        if storage_obj.semifinished_type == 0:
            storage_type = '自产'
        else:
            storage_type = '外包'
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "storageId": storage_obj.semifinished_shoe_id,
            "customerProductName": order_shoe.customer_product_name,
            "inboundAmount": total_amount,
            "currentAmount": storage_obj.semifinished_amount,
            "object": object,
            "storageType": storage_type,
            "statusName": status_name,
        }
        result.append(obj)
    return {"result": result, "total": count_result}


@semifinished_storage_bp.route(
    "/warehouse/warehousemanager/inboundsemifinished", methods=["POST", "PATCH"]
)
def inbound_semifinished():
    data = request.get_json()
    storage = SemifinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "failed"}), 400

    storage.semifinished_amount += int(data["amount"])
    storage.semifinished_inbound_datetime = data["inboundDate"]

    record = ShoeInboundRecord(
        inbound_amount=data["amount"],
        inbound_datetime=data["inboundDate"],
        semifinished_shoe_storage_id=data["storageId"],
    )
    db.session.add(record)
    db.session.flush()
    rid = (
        "SIR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.shoe_inbound_record_id)
    )
    record.shoe_inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


@semifinished_storage_bp.route(
    "/warehouse/warehousemanager/finishinoutbound", methods=["PATCH"]
)
def finish_inoutbound():
    data = request.get_json()
    storage = SemifinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "order shoe storage not found"}), 400
    storage.semifinished_status = 2
    db.session.commit()
    return jsonify({"message": "success"})

@semifinished_storage_bp.route(
    "/warehouse/warehousemanager/outboundsemifinished", methods=["POST", "PATCH"]
)
def outbound_semifinished():
    data = request.get_json()
    storage = SemifinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "failed"}), 400
    if storage.semifinished_type == 0:
        record = ShoeOutboundRecord(
            outbound_amount=int(data["outboundAmount"]),
            outbound_datetime=data["outboundDate"],
            picker=data["picker"],
            outbound_type=storage.semifinished_type,
            semifinished_shoe_storage_id=storage.semifinished_shoe_id,
        )
    elif storage.semifinished_type == 1:
        record = ShoeOutboundRecord(
            outbound_amount=int(data["outboundAmount"]),
            outbound_datetime=data["outboundDate"],
            outbound_address=data["outboundAddress"],
            outbound_type=storage.semifinished_type,
            semifinished_shoe_storage_id=storage.semifinished_shoe_id,
        )
    else:
        return jsonify({"message": "failed"}), 400

    db.session.add(record)
    db.session.flush()
    rid = (
        "SOR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.shoe_outbound_record_id)
    )
    record.shoe_outbound_rid = rid
    storage.semifinished_amount -= int(data["outboundAmount"])
    db.session.commit()
    return jsonify({"message": "success"})


@semifinished_storage_bp.route(
    "/warehouse/warehousemanager/getsemifinishedinoutboundrecords", methods=["GET"]
)
def get_semifinished_in_out_bound_records():
    db.session.query()
    storage_id = request.args.get("storageId")
    inbound_response = ShoeInboundRecord.query.filter(
        ShoeInboundRecord.semifinished_shoe_storage_id == storage_id
    ).all()
    outbound_response = ShoeOutboundRecord.query.filter(
        ShoeOutboundRecord.semifinished_shoe_storage_id == storage_id
    ).all()

    result = []
    for row in inbound_response:
        obj = {
            "opType": "入库",
            "date": row.inbound_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        obj["amount"] = row.inbound_amount
        result.append(obj)

    for row in outbound_response:
        obj = {
            "opType": "出库",
            "date": row.outbound_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        obj["amount"] = row.outbound_amount
        result.append(obj)
    return result
