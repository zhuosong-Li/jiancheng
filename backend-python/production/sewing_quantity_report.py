from app_config import app, db
from flask import Blueprint, jsonify, request
from models import SewingQuantityReport, SewingQuantityReportItem
from sqlalchemy import or_, text

sewing_quantity_report_bp = Blueprint("sewing_quantity_report_bp", __name__)


@sewing_quantity_report_bp.route(
    "/production/fabriccutting/createquantityreport", methods=["POST"]
)
def create_price_report():
    data = request.get_json()
    report = SewingQuantityReport(
        order_shoe_id=data["order_shoe_id"],
        creation_date=data["creation_date"],
        status=0,
        team=data["team"],
    )
    # db.session.add(report)
    # db.session.commit()
    return jsonify({"message": "success"})


@sewing_quantity_report_bp.route(
    "/production/fabriccutting/editquantityreportdetail", methods=["PUT"]
)
def edit_quantity_report_detail():
    data = request.get_json()
    arr = [SewingQuantityReportItem(**obj) for obj in data]
    # db.session.add_all(arr)
    # db.session.commit()
    return jsonify({"message": "success"})


@sewing_quantity_report_bp.route(
    "/production/fabriccutting/submitquantityreport", methods=["POST"]
)
def submit_quantity_report():
    data = request.get_json()
    # row = SewingQuantityReport.query.get(data["report_id"])
    # row.status = 1
    # db.session.commit()
    return jsonify({"message": "success"})


@sewing_quantity_report_bp.route(
    "/production/fabriccutting/getallquantityreport", methods=["GET"]
)
def get_all_quantity_report():
    data = request.get_json()
    row = SewingQuantityReport.query.filter_by(
        order_shoe_id=data["order_shoe_id"]
    ).all()
    return jsonify({"message": "success"})
