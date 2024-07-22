import constants
from app_config import db
from flask import Blueprint, jsonify, request
from models import OrderShoe, OrderShoeStatus, UnitPriceReport, UnitPriceReportDetail
from sqlalchemy import or_, text

price_report_bp = Blueprint("price_report_bp", __name__)

references = {
    "cutting": constants.CUTTING_PRICE_REPORT_STATUS,
    "sewing": constants.SEWING_PRICE_REPORT_STATUS,
    "molding": constants.MOLDING_PRICE_REPORT_STATUS,
}


@price_report_bp.route("/production/createpricereport", methods=["POST"])
def create_price_report():
    data = request.get_json()
    report = UnitPriceReport(order_shoe_id=data["order_shoe_id"], team=data["team"])
    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "success"})


@price_report_bp.route("/production/storepricereportdetail", methods=["POST"])
def store_price_report_detail():
    data = request.get_json()
    report_id = data["report_id"]
    content = data["content"]
    arr = []
    for row in content:
        row["report_id"] = report_id
        arr.append(UnitPriceReportDetail(**row))
    db.session.add_all(arr)
    db.session.commit()
    return jsonify({"message": "success"})


@price_report_bp.route("/production/editpricereportdetail", methods=["PUT"])
def edit_price_report_detail():
    data = request.get_json()
    row = UnitPriceReportDetail.query.filter_by(
        report_id=data["report_id"], row_id=data["row_id"]
    ).first()
    row.procedure_id = data["procedure_id"]
    db.session.commit()
    return jsonify({"message": "success"})


@price_report_bp.route("/production/submitpricereport", methods=["POST"])
def submit_price_report():
    data = request.get_json()
    report_id = data["report_id"]
    if data["team"] not in references:
        return 405
    status = references[data["team"]]
    # get order_shoe status
    report, status_obj = (
        db.session.query(UnitPriceReport, OrderShoeStatus)
        .join(
            OrderShoeStatus,
            UnitPriceReport.order_shoe_id == OrderShoeStatus.order_shoe_id,
        )
        .filter(
            OrderShoeStatus.current_status == status,
            UnitPriceReport.report_id == report_id,
        )
        .first()
    )
    report.submission_date = data["submission_date"]
    status_obj.current_status += 1
    status_obj.current_status_value = 2
    db.session.commit()
    return jsonify({"message": "success"})


@price_report_bp.route("/production/getpricereport", methods=["GET"])
def get_cutting_price_report():
    team = request.args.get("team")
    if team not in references:
        return 405
    status = references[team]
    res = (
        db.session.query(UnitPriceReport, OrderShoe, OrderShoeStatus)
        .join(OrderShoe, UnitPriceReport.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeStatus,
            OrderShoe.order_shoe_id == OrderShoeStatus.order_shoe_id,
        )
        .filter(
            OrderShoeStatus.current_status == status
        )
        .all()
    )
    for row in res:
        print(row)
    return jsonify({"message": "success"})
