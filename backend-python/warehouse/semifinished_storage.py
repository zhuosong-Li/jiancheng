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
            OrderShoeBatchInfo.total_amount,
            SemifinishedShoeStorage,
        )
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(
            SemifinishedShoeStorage,
            SemifinishedShoeStorage.order_shoe_id == OrderShoe.order_shoe_id,
        )
    )
    if order_rid and order_rid != '':
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != '':
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if op_type != 0:
        query = (
            query.join(
                OrderShoeStatus,
                OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id,
            )
            .filter(
                OrderShoeStatus.current_status.in_([25, 26, 34, 35]),
                OrderShoeStatus.current_status_value.in_([0, 1]),
            )
            .filter(SemifinishedShoeStorage.semifinished_status != 2)
        )

    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
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
    else:
        storage.semifinished_amount += data["amount"]
        storage.semifinished_type = data["type"]
        storage.semifinished_inbound_datetime = data["inboundDate"]
        storage.semifinished_status = 1

    record = ShoeInboundRecord(
        inbound_amount=data["amount"],
        inbound_datetime=data["inboundDate"],
        inbound_type=data["type"],
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

    try:
        if storage.semifinished_object == 0:
            opertion1, operation2 = 88, 89
        else:
            opertion1, operation2 = 106, 107
        processor: EventProcessor = current_app.config["event_processor"]
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=opertion1,
            event_order_id=data["orderId"],
            event_order_shoe_id=data["orderShoeId"],
        )
        result = processor.processEvent(event)
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=operation2,
            event_order_id=data["orderId"],
            event_order_shoe_id=data["orderShoeId"],
        )
        result = processor.processEvent(event)
    except Exception as e:
        print(e)
    if not result:
        return jsonify({"message": "failed"}), 500
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
    if data["outboundType"] == "1":
        record = ShoeOutboundRecord(
            outbound_amount=storage.semifinished_amount,
            outbound_datetime=data["outboundDate"],
            picker=data["picker"],
            outbound_type=data["outboundType"],
            semifinished_shoe_storage_id=storage.semifinished_shoe_id,
        )
    elif data["outboundType"] == "2":
        record = ShoeOutboundRecord(
            outbound_amount=storage.semifinished_amount,
            outbound_datetime=data["outboundDate"],
            outbound_address=data["outboundAddress"],
            outbound_type=data["outboundType"],
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
    storage.semifinished_amount = 0
    storage.semifinished_status = 2
    try:
        processor: EventProcessor = current_app.config["event_processor"]
        for op in [90, 91]:
            event = Event(
                staff_id=1,
                handle_time=datetime.datetime.now(),
                operation_id=op,
                event_order_id=data["orderId"],
                event_order_shoe_id=data["orderShoeId"],
            )
            processor.processEvent(event)
    except Exception as e:
        print(e)
        return jsonify({"message": "failed"}), 500
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
        obj = {"opType": "入库", "date": row.inbound_datetime}
        obj["amount"] = row.inbound_amount
        result.append(obj)

    for row in outbound_response:
        obj = {"opType": "出库", "date": row.outbound_datetime}
        obj["amount"] = row.outbound_amount
        result.append(obj)
    return result
