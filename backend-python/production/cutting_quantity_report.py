from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert

from app_config import app, db
from models import *

cutting_quantity_report_bp = Blueprint("cutting_quantity_report_bp", __name__)


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/createquantityreport", methods=["POST"]
)
def create_quantity_report():
    data = request.get_json()
    report = CuttingQuantityReport(
        order_shoe_id=data["orderShoeId"], creation_date=data["creationDate"], status=0
    )
    print(data["orderShoeId"])
    order_shoe_obj = OrderShoeStatus.query.filter_by(
        order_shoe_id=data["orderShoeId"], current_status=23
    ).first()
    print(order_shoe_obj)
    order_shoe_obj.current_status_value = 1
    db.session.add(report)
    db.session.commit()
    return {"reportId": report.report_id}


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/editquantityreportdetail", methods=["PUT"]
)
def edit_quantity_report_detail():
    data = request.get_json()
    report_id = data["reportId"]
    detail_arr = data["data"]
    for row in detail_arr:
        item_obj = CuttingQuantityReportItem.query.filter_by(
            report_id=report_id, order_shoe_batch_info_id=row["orderShoeBatchInfoId"]
        ).first()
        item_obj.amount = row["amount"]
    db.session.commit()
    return jsonify({"message": "success"})


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/submitquantityreport", methods=["POST"]
)
def submit_quantity_report():
    data = request.get_json()
    # row = CuttingQuantityReport.query.get(data["report_id"])
    # row.status = 1
    # db.session.commit()
    return jsonify({"message": "success"})


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/getallquantityreports", methods=["GET"]
)
def get_all_quantity_report():
    order_shoe_id = request.args.get("orderShoeId")
    response = CuttingQuantityReport.query.filter_by(order_shoe_id=order_shoe_id).all()
    result = []
    for row in response:
        result.append(
            {
                "reportId": row.report_id,
                "creationDate": row.creation_date.strftime("%Y-%m-%d"),
                "status": row.status,
                "rejectionReason": row.rejection_reason,
            }
        )
    return result


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/createquantityreportdetail", methods=["POST"]
)
def create_quantity_report_detail():
    data = request.get_json()
    print(data)
    report_id = data["reportId"]
    order_shoe_id = data["orderShoeId"]
    response = OrderShoeBatchInfo.query.filter_by(order_shoe_id=order_shoe_id).all()
    result = []
    for row in response:
        item = CuttingQuantityReportItem(
            report_id=report_id, order_shoe_batch_info_id=row.order_shoe_batch_info_id
        )
        result.append(item)
    db.session.add_all(result)
    db.session.commit()
    return {"message": "success"}


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/getquantityreportdetail", methods=["GET"]
)
def get_quantity_report_detail():
    report_id = request.args.get("reportId")
    response = (
        db.session.query(OrderShoeBatchInfo, CuttingQuantityReportItem)
        .join(
            CuttingQuantityReportItem,
            CuttingQuantityReportItem.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
        )
        .filter_by(report_id=report_id)
        .all()
    )
    result = []
    for row in response:
        batch_info, report_item = row
        result.append(
            {
                "orderShoeBatchInfoId": batch_info.order_shoe_batch_info_id,
                "name": batch_info.name,
                "amount": report_item.amount,
                "totalAmount": batch_info.total_amount,
                "cuttingAmount": batch_info.cutting_amount,
            }
        )
    return result


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/getallordershoesquantityreports", methods=["GET"]
)
def get_all_order_shoes_quantity_report():
    order_id = request.args.get("orderId")
    order_shoe_status_val = request.args.get("ordershoestatus", type=int)
    response = (
        db.session.query(Order, OrderShoe, OrderShoeStatus, Shoe)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(
            OrderShoeStatus,
            OrderShoe.order_shoe_id == OrderShoeStatus.order_shoe_id,
        )
        .filter(
            Order.order_id == order_id,
            OrderShoeStatus.current_status == order_shoe_status_val,
        )
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .all()
    )
    result = {}
    for row in response:
        _, order_shoe, _, shoe = row
        result[order_shoe.order_shoe_id] = {"shoeRId": shoe.shoe_rid, "status": ""}
    return result


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/getAllBatchInfo", methods=["GET"]
)
def get_all_batch_info():
    order_shoe_id = request.args.get("orderShoeId")
    response = OrderShoeBatchInfo.query.filter_by(order_shoe_id=order_shoe_id).all()
    result = []
    for row in response:
        result.append(
            {
                "name": row.name,
                "totalAmount": row.total_amount,
                "cuttingAmount": row.cutting_amount,
            }
        )
    return result
