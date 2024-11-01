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

finished_storage_bp = Blueprint("finished_storage_bp", __name__)


@finished_storage_bp.route(
    "/warehouse/warehousemanager/getfinishedinoutoverview", methods=["GET"]
)
def get_finished_in_out_overview():
    """
    op_type:
        0: show all orders,
        1: show active orders
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
            FinishedShoeStorage,
        )
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(
            FinishedShoeStorage,
            FinishedShoeStorage.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .group_by(OrderShoe.order_shoe_id, FinishedShoeStorage.finished_shoe_id)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if op_type != 0:
        query = query.filter(FinishedShoeStorage.finished_status != 2)
    count_result = query.distinct().count()
    response = query.limit(number).offset((page - 1) * number).all()
    result = []
    for row in response:
        (
            order,
            order_shoe,
            shoe,
            total_amount,
            storage_obj,
        ) = row
        if storage_obj.finished_status == 0:
            status_name = "未完成入库"
        elif storage_obj.finished_status == 1:
            status_name = "已完成入库"
        else:
            status_name = "已完成出库"
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "storageId": storage_obj.finished_shoe_id,
            "customerProductName": order_shoe.customer_product_name,
            "inboundAmount": total_amount,
            "currentAmount": storage_obj.finished_amount,
            "statusName": status_name,
            "endDate": order.end_date,
        }
        result.append(obj)
    return {"result": result, "total": count_result}


@finished_storage_bp.route(
    "/warehouse/warehousemanager/inboundfinished", methods=["POST", "PATCH"]
)
def inbound_finished():
    data = request.get_json()
    storage = FinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "failed"}), 400

    storage.finished_amount += int(data["amount"])
    storage.finished_inbound_datetime = data["inboundDate"]

    record = ShoeInboundRecord(
        inbound_amount=data["amount"],
        inbound_datetime=data["inboundDate"],
        finished_shoe_storage_id=storage.finished_shoe_id,
    )
    db.session.add(record)
    db.session.flush()
    rid = (
        "FIR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.shoe_inbound_record_id)
    )
    record.shoe_inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


@finished_storage_bp.route(
    "/warehouse/warehousemanager/outboundfinished", methods=["POST", "PATCH"]
)
def outbound_finished():
    data = request.get_json()
    if data["isOutboundAll"]:
        response = (
            db.session.query(FinishedShoeStorage)
            .join(
                OrderShoe,
                OrderShoe.order_shoe_id == OrderShoe.order_shoe_id,
            )
            .filter(OrderShoe.order_id == data["orderId"])
            .all()
        )
        for row in response:
            storage = row
            _outbound_helper(storage, data)
    else:
        storage = FinishedShoeStorage.query.get(data["storageId"])
        if not storage:
            return jsonify({"message": "failed"}), 400
        _outbound_helper(storage, data)
    db.session.commit()
    return jsonify({"message": "success"})


def _outbound_helper(storage, data):
    record = ShoeOutboundRecord(
        outbound_amount=storage.finished_amount,
        outbound_datetime=data["outboundDate"],
        outbound_address=data["outboundAddress"],
        outbound_type=1,
        finished_shoe_storage_id=storage.finished_shoe_id,
    )
    storage.finished_amount = 0
    storage.finished_status = 2
    db.session.add(record)
    db.session.flush()
    rid = (
        "FOR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.shoe_outbound_record_id)
    )
    record.shoe_outbound_rid = rid


@finished_storage_bp.route(
    "/warehouse/warehousemanager/getfinishedinoutboundrecords", methods=["GET"]
)
def get_finished_in_out_bound_records():
    db.session.query()
    storage_id = request.args.get("storageId")
    inbound_response = ShoeInboundRecord.query.filter(
        ShoeInboundRecord.finished_shoe_storage_id == storage_id
    ).all()
    outbound_response = ShoeOutboundRecord.query.filter(
        ShoeOutboundRecord.finished_shoe_storage_id == storage_id
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


@finished_storage_bp.route(
    "/warehouse/warehousemanager/completeinboundfinished", methods=["PATCH"]
)
def complete_inbound_finished():
    data = request.get_json()
    storage = FinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "order shoe storage not found"}), 400
    storage.finished_status = 1
    db.session.commit()
    return jsonify({"message": "success"})


@finished_storage_bp.route(
    "/warehouse/warehousemanager/completeoutboundfinished", methods=["PATCH"]
)
def complete_outbound_finished():
    data = request.get_json()
    storage = FinishedShoeStorage.query.get(data["storageId"])
    if not storage:
        return jsonify({"message": "order shoe storage not found"}), 400
    storage.finished_status = 2
    db.session.commit()
    return jsonify({"message": "success"})
