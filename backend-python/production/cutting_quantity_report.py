from flask import Blueprint, jsonify, request
from sqlalchemy import or_, text

from app_config import app, db
from models import *

cutting_quantity_report_bp = Blueprint("cutting_quantity_report_bp", __name__)


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/createquantityreport", methods=["POST"]
)
def create_quantity_report():
    data = request.get_json()
    report = CuttingQuantityReport(
        order_shoe_id=data["orderShoeId"],
        creation_date=data["creationDate"],
        status=0
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "success"})


@cutting_quantity_report_bp.route(
    "/production/fabriccutting/editquantityreportdetail", methods=["PUT"]
)
def edit_quantity_report_detail():
    data = request.get_json()
    arr = [CuttingQuantityReportItem(**obj) for obj in data]
    # db.session.add_all(arr)
    # db.session.commit()
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
    "/production/fabriccutting/getallquantityreport", methods=["GET"]
)
def get_all_quantity_report():
    order_shoe_id = request.args.get("orderShoeId")
    response = CuttingQuantityReport.query.filter_by(
        order_shoe_id=order_shoe_id
    ).all()
    result = []
    for row in response:
        result.append({
            "reportId": row.report_id,
            "creationDate": row.creation_date.strftime("%Y-%m-%d"),
            "status": row.status,
            "rejectionReason": row.rejection_reason
        })
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
