from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert

from constants import PRODUCTION_REFERENCE
from app_config import db
from models import *
import traceback

price_report_bp = Blueprint("price_report_bp", __name__)


@price_report_bp.route("/production/createpricereport", methods=["POST"])
def create_price_report():
    data = request.get_json()
    reports = []
    try:
        for team in PRODUCTION_REFERENCE[data["line"]]["teams"]:
            reports.append(
                UnitPriceReport(order_shoe_id=data["orderShoeId"], team=team, status=0)
            )
        order_shoe_status = OrderShoeStatus.query.filter_by(
            order_shoe_id=data["orderShoeId"],
            current_status=PRODUCTION_REFERENCE[data["line"]]["status_number"],
        ).first()
        order_shoe_status.current_status_value = 1
        db.session.add_all(reports)
        db.session.commit()
        return jsonify({"message": "success"}), 200
    except Exception:
        traceback.print_exc()
        return jsonify({"message": "error"}), 403


@price_report_bp.route("/production/storepricereportdetail", methods=["POST"])
def store_price_report_detail():
    data = request.get_json()
    report_id = data["reportId"]
    new_data = data["newData"]
    row_id_arr = []
    for row in new_data:
        obj = {
            "report_id": report_id,
            "row_id": row["rowId"],
            "procedure_id": row["procedureId"],
            "price": row["price"],
            "note": row["note"],
        }
        row_id_arr.append(row["rowId"])
        insert_stmt = insert(UnitPriceReportDetail).values(**obj)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            report_id=insert_stmt.inserted.report_id,
            row_id=insert_stmt.inserted.row_id,
            procedure_id=insert_stmt.inserted.procedure_id,
            price=insert_stmt.inserted.price,
            note=insert_stmt.inserted.note,
        )
        db.session.execute(on_duplicate_key_stmt)

    UnitPriceReportDetail.query.filter(
        UnitPriceReportDetail.report_id == report_id,
        ~UnitPriceReportDetail.row_id.in_(row_id_arr),
    ).delete()

    # get order_shoe status
    response = (
        db.session.query(UnitPriceReport, OrderShoeStatus)
        .join(
            OrderShoeStatus,
            UnitPriceReport.order_shoe_id == OrderShoeStatus.order_shoe_id,
        )
        .filter(
            UnitPriceReport.report_id == report_id,
        )
        .all()
    )

    for row in response:
        _, status_obj = row
        status_obj.current_status_value = 1

    db.session.commit()
    return jsonify({"message": "success"})


# @price_report_bp.route("/production/submitpricereport", methods=["POST"])
# def submit_price_report():
#     data = request.get_json()
#     report_id = data["report_id"]
#     if data["team"] not in references:
#         return 405
#     status = references[data["team"]]
#     # get order_shoe status
#     report, status_obj = (
#         db.session.query(UnitPriceReport, OrderShoeStatus)
#         .join(
#             OrderShoeStatus,
#             UnitPriceReport.order_shoe_id == OrderShoeStatus.order_shoe_id,
#         )
#         .filter(
#             OrderShoeStatus.current_status == status,
#             UnitPriceReport.report_id == report_id,
#         )
#         .first()
#     )
#     report.submission_date = data["submission_date"]
#     status_obj.current_status += 1
#     status_obj.current_status_value = 2
#     db.session.commit()
#     return jsonify({"message": "success"})


@price_report_bp.route("/production/getpricereportdetail", methods=["GET"])
def get_price_report_detail():
    report_id = request.args.get("reportId")
    response = (
        db.session.query(UnitPriceReport, UnitPriceReportDetail, ProcedureReference)
        .join(
            UnitPriceReportDetail,
            UnitPriceReport.report_id == UnitPriceReportDetail.report_id,
        )
        .join(
            ProcedureReference,
            UnitPriceReportDetail.procedure_id == ProcedureReference.procedure_id,
        )
        .filter(UnitPriceReport.report_id == report_id)
        .all()
    )
    result = []
    for row in response:
        _, report_detail, procedure_ref = row
        result.append(
            {
                "rowId": report_detail.row_id,
                "procedure": procedure_ref.procedure_name,
                "price": report_detail.price,
                "note": report_detail.note,
            }
        )
    return result


@price_report_bp.route("/production/getpricereportdetailbyordershoeid", methods=["GET"])
def get_price_report_detail_by_order_shoe_id():
    order_shoe_id = request.args.get("orderShoeId")
    team = request.args.get("team")
    response = (
        db.session.query(UnitPriceReport, UnitPriceReportDetail, OrderShoe, ProcedureReference)
        .join(
            UnitPriceReportDetail,
            UnitPriceReport.report_id == UnitPriceReportDetail.report_id,
        ).join(
            OrderShoe,
            UnitPriceReport.order_shoe_id == OrderShoe.order_shoe_id
        ).join(
            ProcedureReference,
            UnitPriceReportDetail.procedure_id == ProcedureReference.procedure_id,
        )
        .filter(OrderShoe.order_shoe_id == order_shoe_id, UnitPriceReport.team == team)
        .all()
    )
    result = []
    for row in response:
        _, report_detail, _, procedure_ref = row
        result.append(
            {
                "rowId": report_detail.row_id,
                "procedure": procedure_ref.procedure_name,
                "price": report_detail.price,
                "note": report_detail.note,
            }
        )
    return result


@price_report_bp.route("/production/getallordershoespricereports", methods=["GET"])
def get_all_order_shoes_price_report():
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
        entity = UnitPriceReport.query.filter_by(
            order_shoe_id=order_shoe.order_shoe_id
        ).first()
        if not entity:
            result[order_shoe.order_shoe_id] = {
                "reportId": "",
                "status": -1,
                "date": None,
            }
        else:
            result[order_shoe.order_shoe_id] = {
                "reportId": entity.report_id,
                "status": entity.status,
                "date": entity.submission_date,
            }
        result[order_shoe.order_shoe_id]["shoeRId"] = shoe.shoe_rid
    return result


@price_report_bp.route("/production/getallprocedures", methods=["GET"])
def get_all_procedures():
    teams = request.args.get("teams")
    teams = teams.split(",")
    response = ProcedureReference.query.filter(ProcedureReference.team.in_(teams)).all()
    result = []
    for row in response:
        result.append(
            {
                "procedureId": row.procedure_id,
                "procedureName": row.procedure_name,
                "price": row.current_price,
                "team": row.team,
            }
        )
    return result
