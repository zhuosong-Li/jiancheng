from datetime import datetime

from api_utility import format_date
from app_config import db
from constants import END_OF_PRODUCTION_NUMBER, QUANTTIY_REPORT_REFERENCE
from flask import Blueprint, jsonify, request
from models import *
from sqlalchemy import func, literal

quantity_report_bp = Blueprint("quantity_report_bp", __name__)


def check_report_status(number):
    if number == 0:
        status_name = "未提交"
    elif number == 1:
        status_name = "已提交"
    elif number == 2:
        status_name = "已审批"
    else:
        status_name = "被驳回"
    return status_name


@quantity_report_bp.route("/production/getquantityreporttasks", methods=["GET"])
def get_quantity_report_tasks():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    teams = request.args.get("teams").split(",")
    queries = []
    for team in teams:
        teamId = -1
        if team == "裁断":
            start_date = OrderShoeProductionInfo.cutting_start_date
            end_date = OrderShoeProductionInfo.cutting_end_date
            produced_amount = OrderShoeBatchInfo.cutting_amount
            teamId = 0
        elif team == "针车预备":
            start_date = OrderShoeProductionInfo.pre_sewing_start_date
            end_date = OrderShoeProductionInfo.pre_sewing_end_date
            produced_amount = OrderShoeBatchInfo.pre_sewing_amount
            teamId = 1
        elif team == "针车":
            start_date = OrderShoeProductionInfo.sewing_start_date
            end_date = OrderShoeProductionInfo.sewing_end_date
            produced_amount = OrderShoeBatchInfo.sewing_amount
            teamId = 1
        elif team == "成型":
            start_date = OrderShoeProductionInfo.molding_start_date
            end_date = OrderShoeProductionInfo.molding_end_date
            produced_amount = OrderShoeBatchInfo.molding_amount
            teamId = 2
        else:
            return jsonify({"message": "invalid team name"}), 400
        amount_table = (
            db.session.query(
                OrderShoe.order_shoe_id,
                func.sum(OrderShoeProductionAmount.total_production_amount).label(
                    "total_amount"
                ),
                func.sum(produced_amount).label("produced_amount"),
            )
            .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
            .join(
                OrderShoeBatchInfo,
                OrderShoeBatchInfo.order_shoe_type_id
                == OrderShoeType.order_shoe_type_id,
            )
            .join(
                OrderShoeProductionAmount,
                OrderShoeProductionAmount.order_shoe_batch_info_id
                == OrderShoeBatchInfo.order_shoe_batch_info_id,
            )
            .filter(OrderShoeProductionAmount.production_team == teamId)
            .group_by(OrderShoe.order_shoe_id)
        ).subquery()
        query = (
            db.session.query(
                Order,
                OrderShoe,
                Shoe,
                Customer,
                start_date.label("start_date"),
                end_date.label("end_date"),
                literal(team).label("team"),
                amount_table.c.produced_amount,
                amount_table.c.total_amount,
            )
            .join(OrderShoe, OrderShoe.order_id == Order.order_id)
            .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
            .join(Customer, Customer.customer_id == Order.customer_id)
            .join(
                OrderShoeProductionInfo,
                OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
            )
            .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
            .join(
                OrderShoeBatchInfo,
                OrderShoeBatchInfo.order_shoe_type_id
                == OrderShoeType.order_shoe_type_id,
            )
            .join(
                OrderShoeStatus,
                OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id,
            )
            .join(amount_table, amount_table.c.order_shoe_id == OrderShoe.order_shoe_id)
            .filter(
                OrderShoeStatus.current_status == QUANTTIY_REPORT_REFERENCE[team],
                OrderShoeStatus.current_status_value.in_([0, 1]),
            )
        )
        queries.append(query)
    union_query = queries[0]
    for i in range(1, len(queries)):
        union_query = union_query.union(queries[i])
    if order_rid and order_rid != "":
        union_query = union_query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        union_query = union_query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    count_result = union_query.distinct().count()
    response = union_query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        (
            order,
            order_shoe,
            shoe,
            customer,
            start_date_res,
            end_date_res,
            team,
            produced_amount,
            total_amount,
        ) = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "productionStartDate": start_date_res.strftime("%Y-%m-%d"),
            "productionEndDate": end_date_res.strftime("%Y-%m-%d"),
            "customerName": customer.customer_name,
            "team": team,
            "progress": str(produced_amount) + "/" + str(total_amount),
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@quantity_report_bp.route("/production/createquantityreport", methods=["POST"])
def create_quantity_report():
    data = request.get_json()
    report = QuantityReport(
        order_shoe_id=data["orderShoeId"],
        creation_date=data["creationDate"],
        status=0,
        team=data["team"],
    )
    order_shoe_obj = OrderShoeStatus.query.filter_by(
        order_shoe_id=data["orderShoeId"],
        current_status=QUANTTIY_REPORT_REFERENCE[data["team"]],
    ).first()
    order_shoe_obj.current_status_value = 1
    db.session.add(report)
    db.session.commit()
    return {"reportId": report.report_id}


@quantity_report_bp.route("/production/editquantityreportdetail", methods=["PUT"])
def edit_quantity_report_detail():
    data = request.get_json()
    report_id = data["reportId"]
    detail_arr = data["data"]
    for row in detail_arr:
        item_obj = QuantityReportItem.query.filter_by(
            report_id=report_id, order_shoe_batch_info_id=row["orderShoeBatchInfoId"]
        ).first()
        item_obj.amount = row["amount"]
    db.session.commit()
    return jsonify({"message": "success"})


@quantity_report_bp.route("/production/submitquantityreport", methods=["PATCH"])
def submit_quantity_report():
    data = request.get_json()
    report = QuantityReport.query.get(data["reportId"])
    report.status = 1
    report.submission_date = datetime.now().strftime("%Y-%m-%d")
    db.session.commit()
    return jsonify({"message": "success"})


@quantity_report_bp.route("/production/deletequantityreport", methods=["DELETE"])
def delete_quantity_report():
    report_id = request.args.get("reportId")
    items = QuantityReportItem.query.filter_by(report_id=report_id).all()
    for item in items:
        db.session.delete(item)
    row = QuantityReport.query.get(report_id)
    db.session.delete(row)
    db.session.commit()
    return jsonify({"message": "success"})


@quantity_report_bp.route("/production/getallquantityreports", methods=["GET"])
def get_all_quantity_report():
    order_shoe_id = request.args.get("orderShoeId")
    team = request.args.get("team")
    response = QuantityReport.query.filter_by(
        order_shoe_id=order_shoe_id, team=team
    ).all()
    result = []
    for row in response:
        result.append(
            {
                "reportId": row.report_id,
                "creationDate": format_date(row.creation_date),
                "submissionDate": format_date(row.submission_date),
                "status": check_report_status(row.status),
                "rejectionReason": row.rejection_reason,
            }
        )
    return result


@quantity_report_bp.route("/production/createquantityreportdetail", methods=["POST"])
def create_quantity_report_detail():
    data = request.get_json()
    report_id = data["reportId"]
    order_shoe_id = data["orderShoeId"]
    response = (
        db.session.query(OrderShoeBatchInfo)
        .join(
            OrderShoeType,
            OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id,
        )
        .filter(OrderShoeType.order_shoe_id == order_shoe_id)
        .all()
    )
    result = []
    for row in response:
        item = QuantityReportItem(
            report_id=report_id, order_shoe_batch_info_id=row.order_shoe_batch_info_id
        )
        result.append(item)
    db.session.add_all(result)
    db.session.commit()
    return {"message": "success"}


@quantity_report_bp.route("/production/getquantityreportdetail", methods=["GET"])
def get_quantity_report_detail():
    report_id = request.args.get("reportId")
    # 0: 裁断，1：针车预备，2：针车，3：成型
    team = request.args.get("team", type=int)
    mapping = {0: 0, 1: 1, 2: 1, 3: 2}
    response = (
        db.session.query(
            OrderShoeBatchInfo, OrderShoeProductionAmount, Color, QuantityReportItem
        )
        .join(
            OrderShoeType,
            OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id,
        )
        .join(
            OrderShoeProductionAmount,
            OrderShoeProductionAmount.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
        )
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .join(
            QuantityReportItem,
            QuantityReportItem.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
        )
        .filter(
            QuantityReportItem.report_id == report_id,
            OrderShoeProductionAmount.production_team == mapping[team],
        )
        .all()
    )
    result = []
    for row in response:
        batch_info, production_amount, color, report_item = row
        produced_amount = 0
        if team == 0:
            produced_amount = batch_info.cutting_amount
        elif team == 1:
            produced_amount = batch_info.pre_sewing_amount
        elif team == 2:
            produced_amount = batch_info.sewing_amount
        elif team == 3:
            produced_amount = batch_info.molding_amount
        if production_amount.total_production_amount > 0:
            obj = {
                "orderShoeBatchInfoId": batch_info.order_shoe_batch_info_id,
                "colorName": color.color_name,
                "name": batch_info.name,
                "amount": report_item.amount,
                "totalAmount": production_amount.total_production_amount,
                "producedAmount": produced_amount,
            }
            result.append(obj)
    return result
