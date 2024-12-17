import traceback
from datetime import datetime, timedelta, date
from app_config import app
from api_utility import format_date, format_line_group, status_converter, to_camel
from app_config import db
from constants import *
from event_processor import EventProcessor
from flask import Blueprint, current_app, jsonify, request, send_file, Response
from models import *
from sqlalchemy import func, or_, cast, Integer, and_, select, asc, desc
from sqlalchemy.dialects.mysql import insert
from constants import OUTSOURCE_STATUS_MAPPING
from general_document.batch_info import generate_excel_file
from business.batch_info_type import get_order_batch_type_helper
import os

production_manager_bp = Blueprint("production_manager_bp", __name__)
PRODUCTION_INFO_ATTRNAMES = OrderShoeProductionInfo.__table__.columns.keys()


def get_order_info_helper(order_id, order_shoe_id):
    query = (
        db.session.query(
            Order,
            Customer,
        )
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(Order.order_id == order_id)
    )
    if order_shoe_id and order_shoe_id != "":
        response = (
            query.add_columns(OrderShoe, Shoe)
            .join(OrderShoe, Order.order_id == OrderShoe.order_id)
            .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
            .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
            .join(Shoe, Shoe.shoe_id == ShoeType.shoe_id)
            .filter(OrderShoe.order_shoe_id == order_shoe_id)
            .first()
        )
        order, customer, order_shoe, shoe = response
        result = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "orderStartDate": format_date(order.start_date),
            "orderEndDate": format_date(order.end_date),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeId": shoe.shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "customerBrand": customer.customer_brand,
        }
    else:
        response = query.first()
        order, customer = response
        result = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "orderStartDate": format_date(order.start_date),
            "orderEndDate": format_date(order.end_date),
            "customerBrand": customer.customer_brand,
        }
    return result


def get_order_shoe_batch_info_helper(order_shoe_id):
    entities = (
        db.session.query(OrderShoeType, OrderShoeBatchInfo, Color)
        .join(
            OrderShoeType,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(OrderShoeType.order_shoe_id == order_shoe_id)
        .all()
    )
    # Dictionary to accumulate total amounts by color
    color_totals = {}

    # First loop to accumulate total amounts for each color
    for entity in entities:
        _, order_shoe_batch_info, color = entity
        if color.color_name not in color_totals:
            color_totals[color.color_name] = 0
        color_totals[color.color_name] += order_shoe_batch_info.total_amount
    # Second loop to build the result list and include the color totals
    result = []
    for entity in entities:
        order_shoe_type, order_shoe_batch_info, color = entity
        obj = {
            "orderShoeTypeId": order_shoe_type.order_shoe_type_id,
            "orderShoeBatchInfoId": order_shoe_batch_info.order_shoe_batch_info_id,
            "batchName": order_shoe_batch_info.name,
            "colorName": color.color_name,
            "pairAmount": order_shoe_batch_info.total_amount,
            "totalAmount": color_totals[
                color.color_name
            ],  # Add total amount for the color
        }
        for i in range(34, 47):
            amount_column_name = f"size_{i}_amount"
            amount = getattr(order_shoe_batch_info, amount_column_name)
            obj[f"size{i}Amount"] = amount
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/getorderamount", methods=["GET"]
)
def get_order_amount():
    order_id = request.args.get("orderId")
    query = (
        db.session.query(
            Order,
            func.sum(OrderShoeBatchInfo.total_amount),
        )
        .join(Customer, Order.customer_id == Customer.customer_id)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id,
        )
        .filter(Order.order_id == order_id)
        .group_by(Order.order_id)
    )
    response = query.first()
    order, total_amount = response
    result = {
        "orderId": order.order_id,
        "orderTotalShoes": total_amount,
    }
    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/getorderinfo", methods=["GET"]
)
def get_order_info():
    order_id = request.args.get("orderId")
    order_shoe_id = request.args.get("orderShoeId")
    result = get_order_info_helper(order_id, order_shoe_id)
    return jsonify(result)


@production_manager_bp.route("/production/getproductioninfo", methods=["GET"])
def get_production_info():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        db.session.query(OrderShoeProductionInfo)
        .filter_by(order_shoe_id=order_shoe_id)
        .first()
    )
    result = {}
    for db_attr in PRODUCTION_INFO_ATTRNAMES:
        attr_value = getattr(response, db_attr)
        if attr_value and isinstance(attr_value, (datetime, date)):
            result[to_camel(db_attr)] = format_date(attr_value)
        else:
            result[to_camel(db_attr)] = attr_value
    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/getinprogressorders", methods=["GET"]
)
def get_in_progress_orders():
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    customer_name = request.args.get("customerName")
    customer_brand = request.args.get("customerBrand")
    query = (
        db.session.query(
            Order,
            Customer,
            func.min(OrderShoeProductionInfo.cutting_start_date),
            func.max(OrderShoeProductionInfo.molding_end_date),
            func.sum(OrderShoeBatchInfo.total_amount),
            func.sum(OrderShoeType.molding_amount),
        )
        .join(Customer, Order.customer_id == Customer.customer_id)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id,
        )
        .join(OrderStatus, OrderStatus.order_id == Order.order_id)
        .group_by(Order.order_id)
        .filter(OrderStatus.order_current_status == 9)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if customer_name and customer_name != "":
        query = query.filter(Customer.customer_name.ilike(f"%{customer_name}%"))
    if customer_brand and customer_brand != "":
        query = query.filter(Customer.customer_brand.ilike(f"%{customer_brand}%"))
    count_result = query.distinct().count()
    response = query.distinct().limit(number).offset((page - 1) * number).all()
    result = []
    for row in response:
        (
            order,
            customer,
            cutting_start_date,
            molding_end_date,
            total_amount,
            finished_amount,
        ) = row
        cutting_start_date = format_date(cutting_start_date)
        molding_end_date = format_date(molding_end_date)
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "customerBrand": customer.customer_brand,
            "startDate": cutting_start_date,
            "endDate": molding_end_date,
            "orderStartDate": format_date(order.start_date),
            "orderEndDate": format_date(order.end_date),
            "orderTotalShoes": total_amount,
            "finishedShoes": finished_amount if finished_amount else 0,
        }
        result.append(obj)
    return {"result": result, "total": count_result}


PROGRESS_STATUS_MAPPING = {
    "未排期": [17],
    "已保存排期": [17],
    "生产前确认": [18],
    "生产中": [23],
    "生产结束": [42],
}


@production_manager_bp.route(
    "/production/productionmanager/getallorderproductionprogress", methods=["GET"]
)
def get_all_order_production_progress():
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    customer_product_name = request.args.get("customerProductName")
    status_node = request.args.get("statusNode")
    start_date_search = request.args.get("orderStartDate")
    end_date_search = request.args.get("orderEndDate")
    customer_name = request.args.get("customerName")
    customer_brand = request.args.get("customerBrand")
    sort_condition = request.args.get("sortCondition")
    # check order status >= 生产流程
    stmt = select(OrderStatus.order_id).where(OrderStatus.order_current_status >= 9)
    order_ids = db.session.execute(stmt).scalars().all()

    # order shoe status
    status_table = (
        db.session.query(
            OrderShoe.order_shoe_id,
            func.group_concat(OrderShoeStatus.current_status).label(
                "current_status_str"
            ),
            func.group_concat(OrderShoeStatus.current_status_value).label(
                "current_status_value_str"
            ),
        )
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .group_by(OrderShoe.order_shoe_id)
    )
    if status_node and status_node != "":
        status_ids = PROGRESS_STATUS_MAPPING[status_node]
        status_table = status_table.filter(
            OrderShoeStatus.current_status.in_(status_ids)
        )
        if status_node == "已保存排期":
            status_table = status_table.filter(
                OrderShoeStatus.current_status_value == 1
            )
    status_table = status_table.subquery()

    # order shoe amount
    order_shoe_info = (
        db.session.query(
            OrderShoe.order_shoe_id,
            func.sum(OrderShoeBatchInfo.total_amount).label("order_shoe_amount"),
        )
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .group_by(OrderShoe.order_shoe_id)
        .subquery()
    )

    team_production_amount = (
        db.session.query(
            OrderShoe.order_shoe_id,
            func.sum(OrderShoeType.cutting_amount).label("total_cutting_amount"),
            func.sum(OrderShoeType.pre_sewing_amount).label("total_pre_sewing_amount"),
            func.sum(OrderShoeType.sewing_amount).label("total_sewing_amount"),
            func.sum(OrderShoeType.molding_amount).label("total_molding_amount"),
        )
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .group_by(OrderShoe.order_shoe_id)
        .subquery()
    )
    query = (
        db.session.query(
            Order,
            Customer,
            OrderShoe,
            Shoe,
            status_table.c.current_status_str,
            status_table.c.current_status_value_str,
            OrderShoeProductionInfo,
            team_production_amount.c.total_cutting_amount,
            team_production_amount.c.total_pre_sewing_amount,
            team_production_amount.c.total_sewing_amount,
            team_production_amount.c.total_molding_amount,
            order_shoe_info.c.order_shoe_amount,
        )
        .join(Customer, Customer.customer_id == Order.customer_id)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .join(status_table, status_table.c.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(
            team_production_amount,
            team_production_amount.c.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(
            order_shoe_info, order_shoe_info.c.order_shoe_id == OrderShoe.order_shoe_id
        )
        .filter(Order.order_id.in_(order_ids))
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if customer_product_name and customer_product_name != "":
        query = query.filter(
            OrderShoe.customer_product_name.ilike(f"%{customer_product_name}%")
        )
    if start_date_search and end_date_search:
        try:
            datetime.strptime(start_date_search, "%Y-%m-%d")
            datetime.strptime(end_date_search, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "invalid date range"}), 400
        query = query.filter(
            or_(
                and_(
                    Order.start_date >= start_date_search,
                    Order.end_date <= end_date_search,
                ),
                and_(
                    Order.start_date <= end_date_search,
                    Order.start_date >= start_date_search,
                ),
                and_(
                    Order.end_date >= start_date_search,
                    Order.end_date <= end_date_search,
                ),
                and_(
                    Order.start_date <= start_date_search,
                    Order.end_date >= end_date_search,
                ),
            ),
        )
    if customer_name and customer_name != "":
        query = query.filter(Customer.customer_name.ilike(f"%{customer_name}%"))
    if customer_brand and customer_brand != "":
        query = query.filter(Customer.customer_brand.ilike(f"%{customer_brand}%"))
    # sort condition
    if sort_condition == "最新":
        query = query.order_by(desc(Order.start_date))
    elif sort_condition == "最旧":
        query = query.order_by(asc(Order.start_date))
    elif sort_condition == "周期最长":
        query = query.order_by(desc(Order.end_date - Order.start_date))
    elif sort_condition == "数量最多":
        query = query.order_by(desc(order_shoe_info.c.order_shoe_amount))
    else:
        query = query.order_by(asc(Order.end_date))
    count_result = query.distinct().count()
    response = query.distinct().limit(number).offset((page - 1) * number).all()
    res = []
    order_shoe_data = {}
    for row in response:
        (
            order,
            customer,
            order_shoe,
            shoe,
            current_status_str,
            current_status_value_str,
            production_info,
            total_cutting_amount,
            total_pre_sewing_amount,
            total_sewing_amount,
            total_molding_amount,
            order_shoe_amount,
        ) = row
        status_arr = [int(item) for item in current_status_str.split(",")]
        status_value_arr = [int(item) for item in current_status_value_str.split(",")]
        status = status_converter(status_arr, status_value_arr)
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "customerBrand": customer.customer_brand,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "orderStartDate": format_date(order.start_date),
            "orderEndDate": format_date(order.end_date),
            "processSheetUploadStatus": order_shoe.process_sheet_upload_status,
            "status": status,
            "technicalRemark": order_shoe.business_technical_remark,
            "materialRemark": order_shoe.business_material_remark,
            "cuttingStartDate": format_date(production_info.cutting_start_date),
            "cuttingEndDate": format_date(production_info.cutting_end_date),
            "preSewingStartDate": format_date(production_info.pre_sewing_start_date),
            "preSewingEndDate": format_date(production_info.pre_sewing_end_date),
            "sewingStartDate": format_date(production_info.sewing_start_date),
            "sewingEndDate": format_date(production_info.sewing_end_date),
            "moldingStartDate": format_date(production_info.molding_start_date),
            "moldingEndDate": format_date(production_info.molding_end_date),
            "orderShoeTypeInfo": [],
            "totalCuttingAmount": total_cutting_amount,
            "totalPreSewingAmount": total_pre_sewing_amount,
            "totalSewingAmount": total_sewing_amount,
            "totalMoldingAmount": total_molding_amount,
            "orderShoeTotal": order_shoe_amount,
            "isMaterialArrived": production_info.is_material_arrived,
        }
        res.append(obj)

    for order_shoe_data in res:
        order_shoe_type_info = (
            db.session.query(
                OrderShoeType, Color, func.sum(OrderShoeBatchInfo.total_amount)
            )
            .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
            .join(Color, Color.color_id == ShoeType.color_id)
            .join(
                OrderShoeBatchInfo,
                OrderShoeBatchInfo.order_shoe_type_id
                == OrderShoeType.order_shoe_type_id,
            )
            .filter(OrderShoeType.order_shoe_id == order_shoe_data["orderShoeId"])
            .group_by(OrderShoeType.order_shoe_type_id)
            .all()
        )
        for order_shoe_type, color, color_amount in order_shoe_type_info:
            order_shoe_data["orderShoeTypeInfo"].append(
                {
                    "colorName": color.color_name,
                    "colorAmount": color_amount,
                    "cuttingAmount": order_shoe_type.cutting_amount,
                    "preSewingAmount": order_shoe_type.pre_sewing_amount,
                    "sewingAmount": order_shoe_type.sewing_amount,
                    "moldingAmount": order_shoe_type.molding_amount,
                }
            )
    return {"result": res, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getproductiondepartments", methods=["GET"]
)
def get_production_departments():
    return jsonify(["裁断", "针车", "成型"])


@production_manager_bp.route("/production/getallordershoeinfo", methods=["GET"])
def get_all_order_shoe_info():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    query = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderStatus, Order.order_id == OrderStatus.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(OrderStatus.order_current_status >= IN_PRODUCTION_ORDER_NUMBER)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    count_result = query.distinct().count()
    response = query.distinct().limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, shoe = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderStartDate": format_date(order.start_date),
            "orderEndDate": format_date(order.end_date),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/getordershoebatchinfoforproduction", methods=["GET"]
)
def get_order_shoe_batch_info_for_production():
    order_shoe_id = request.args.get("orderShoeId")
    node_name = request.args.get("nodeName")
    response = (
        db.session.query(Color, OrderShoeBatchInfo)
        .join(
            OrderShoeType,
            OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id,
        )
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(OrderShoeType.order_shoe_id == order_shoe_id)
        .all()
    )
    result = []
    for row in response:
        color, batch_info = row
        amount = 0
        # 分状态
        if node_name == "裁断开始" or node_name == "裁断结束":
            amount = batch_info.cutting_amount
        elif node_name == "针车预备开始":
            amount = batch_info.pre_sewing_amount
        elif node_name == "针车开始" or node_name == "针车结束":
            amount = batch_info.sewing_amount
        elif (
            node_name == "成型开始"
            or node_name == "成型结束"
            or node_name == "生产结束"
        ):
            amount = batch_info.molding_amount
        obj = {
            "color": color.color_name,
            "batchInfoName": batch_info.name,
            "totalAmount": batch_info.total_amount,
            "finishedAmount": amount,
        }
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/checkdateproductionstatus", methods=["GET"]
)
def check_date_production_status():
    start_date_str = request.args.get("startDate")
    end_date_str = request.args.get("endDate")
    team = request.args.get("team")
    if not start_date_str or not end_date_str:
        return jsonify({"message": "未选择日期"}), 400
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if team == "cutting":
        search_start_date = "cutting_start_date"
        search_end_date = "cutting_end_date"
        teamId = 0
    elif team == "preSewing":
        search_start_date = "pre_sewing_start_date"
        search_end_date = "pre_sewing_end_date"
        teamId = 1
    elif team == "sewing":
        search_start_date = "sewing_start_date"
        search_end_date = "sewing_end_date"
        teamId = 1
    elif team == "molding":
        search_start_date = "molding_start_date"
        search_end_date = "molding_end_date"
        teamId = 2
    else:
        return jsonify({"message": "invalid team name"}), 400

    sub_table = (
        db.session.query(
            OrderShoe,
            OrderShoeType,
            func.sum(OrderShoeProductionAmount.total_production_amount).label(
                "total_amount"
            ),
        )
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeProductionAmount,
            OrderShoeProductionAmount.order_shoe_type_id
            == OrderShoeType.order_shoe_type_id,
        )
        .filter(OrderShoeProductionAmount.production_team == teamId)
        .group_by(OrderShoe.order_shoe_id, OrderShoeType.order_shoe_type_id)
        .subquery()
    )

    response = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            OrderShoeProductionInfo,
            func.sum(sub_table.c.total_amount).label("total_amount"),
        )
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(sub_table, sub_table.c.order_shoe_id == OrderShoe.order_shoe_id)
        .filter(
            or_(
                getattr(OrderShoeProductionInfo, search_end_date) >= start_date,
                getattr(OrderShoeProductionInfo, search_start_date) <= end_date,
            )
        )
        .group_by(OrderShoe.order_shoe_id, OrderShoeProductionInfo.production_info_id)
        .all()
    )

    delta = timedelta(days=1)
    # Create a date range with all days between start_date and end_date
    all_days = []
    current_date = start_date
    while current_date <= end_date:
        all_days.append(current_date)
        current_date += delta
    order_shoes_delta = {day: [] for day in all_days}
    result = []
    # Loop through each order
    for row in response:
        order, order_shoe, shoe, production_info, total_amount = row
        production_start_date = getattr(production_info, search_start_date)
        production_end_date = getattr(production_info, search_end_date)
        first_day = production_start_date
        if production_start_date <= start_date:
            first_day = start_date

        end_day = production_end_date
        if end_day >= end_date:
            end_day = end_date
        obj = {
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "totalAmount": total_amount,
            "productionStartDate": format_date(production_start_date),
            "productionEndDate": format_date(production_end_date),
        }
        current_date = first_day
        while current_date <= end_day:
            order_shoes_delta[current_date].append(obj)
            current_date += delta

    for day in all_days:
        result.append(
            {
                "date": format_date(day),
                "orderShoeCount": len(order_shoes_delta[day]),
                "detail": order_shoes_delta[day],
            }
        )

    return result


@production_manager_bp.route(
    "/production/productionmanager/getordershoeproductionamount", methods=["GET"]
)
def get_order_shoe_production_amount():
    order_shoe_id = request.args.get("orderShoeId")
    entities = (
        db.session.query(
            OrderShoeType.order_shoe_type_id, OrderShoeProductionAmount, Color
        )
        .join(
            OrderShoeType,
            OrderShoeProductionAmount.order_shoe_type_id
            == OrderShoeType.order_shoe_type_id,
        )
        .join(OrderShoe, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
        .all()
    )
    # Dictionary to accumulate total amounts by color
    color_totals = {}

    # First loop to accumulate total amounts for each color
    for entity in entities:
        _, order_shoe_production_amount, color = entity
        team = order_shoe_production_amount.production_team
        if team not in color_totals:
            color_totals[team] = {}
        if color.color_name not in color_totals[team]:
            color_totals[team][color.color_name] = 0
        if order_shoe_production_amount.total_production_amount:
            color_totals[team][
                color.color_name
            ] += order_shoe_production_amount.total_production_amount
    # Second loop to build the result list and include the color totals
    result = {}
    for entity in entities:
        order_shoe_type_id, order_shoe_production_amount, color = entity
        team = order_shoe_production_amount.production_team
        actual_total_amount = order_shoe_production_amount.total_production_amount
        if team not in result:
            result[team] = []
        if not actual_total_amount:
            actual_total_amount = 0
        obj = {
            "productionAmountId": order_shoe_production_amount.order_shoe_production_amount_id,
            "orderShoeTypeId": order_shoe_type_id,
            "colorName": color.color_name,
            "pairAmount": actual_total_amount,
            "totalAmount": color_totals[team][color.color_name],
            "productionTeam": team,
        }
        for i in range(34, 47):
            amount_column_name = f"size_{i}_production_amount"
            amount = getattr(order_shoe_production_amount, amount_column_name)
            obj[f"size{i}Amount"] = amount
        result[team].append(obj)
    return jsonify(result)


@production_manager_bp.route("/production/getordershoebatchinfo", methods=["GET"])
def get_order_shoe_batch_info():
    order_shoe_id = request.args.get("orderShoeId")
    result = get_order_shoe_batch_info_helper(order_shoe_id)
    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/getordershoetypeamount", methods=["GET"]
)
def get_order_shoe_type_amount():
    order_shoe_id = request.args.get("orderShoeId")
    query = (
        db.session.query(
            OrderShoeType,
            func.sum(OrderShoeBatchInfo.total_amount).label("total_amount"),
            Color,
        )
        .join(
            OrderShoeType,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(OrderShoeType.order_shoe_id == order_shoe_id)
        .group_by(OrderShoeType.order_shoe_type_id)
    )
    for i in range(34, 47):
        column_name = f"size_{i}_amount"
        query = query.add_column(
            cast(func.sum(getattr(OrderShoeBatchInfo, column_name)), Integer).label(
                column_name
            )
        )
    entities = query.all()
    # Second loop to build the result list and include the color totals
    result = []
    for entity in entities:
        obj = {
            "orderShoeTypeId": entity.OrderShoeType.order_shoe_type_id,
            "colorName": entity.Color.color_name,
            "totalAmount": entity.total_amount,
        }
        for i in range(34, 47):
            amount_column_name = f"size_{i}_amount"
            amount = getattr(entity, amount_column_name)
            obj[f"size{i}Amount"] = amount
        result.append(obj)

    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/getallquantityreportsoverview", methods=["GET"]
)
def get_all_quantity_reports_overview():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_date = yesterday.date()
    yesterday_production_table = (
        db.session.query(
            OrderShoe,
            QuantityReport.team,
            func.sum(QuantityReportItem.report_amount).label("amount"),
        )
        .join(QuantityReport, QuantityReport.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            QuantityReportItem,
            QuantityReportItem.quantity_report_id == QuantityReport.report_id,
        )
        .filter(
            QuantityReport.creation_date == yesterday_date,
            QuantityReport.status.in_([1, 2]),
        )
        .group_by(OrderShoe.order_shoe_id, QuantityReport.team)
        .subquery()
    )
    query = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            yesterday_production_table.c.team,
            yesterday_production_table.c.amount,
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .outerjoin(
            yesterday_production_table,
            OrderShoe.order_shoe_id == yesterday_production_table.c.order_shoe_id,
        )
        .filter(
            OrderShoeStatus.current_status.in_([23, 30, 32, 40]),
        )
    )

    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    count_result = query.distinct().count()
    response = query.distinct().limit(page_size).offset((page - 1) * page_size).all()
    result = []
    amount_map = {}
    for row in response:
        order, order_shoe, shoe, team, amount = row
        if order_shoe.order_shoe_id not in amount_map:
            obj = {
                "orderId": order.order_id,
                "orderRId": order.order_rid,
                "orderStartDate": format_date(order.start_date),
                "orderEndDate": format_date(order.end_date),
                "orderShoeId": order_shoe.order_shoe_id,
                "shoeRId": shoe.shoe_rid,
                "customerProductName": order_shoe.customer_product_name,
                "cuttingAmount": 0,
                "preSewingAmount": 0,
                "sewingAmount": 0,
                "moldingAmount": 0,
            }
            amount_map[order_shoe.order_shoe_id] = obj
            result.append(obj)
        if team == "裁断":
            amount_map[order_shoe.order_shoe_id]["cuttingAmount"] = amount
        elif team == "针车预备":
            amount_map[order_shoe.order_shoe_id]["preSewingAmount"] = amount
        elif team == "针车":
            amount_map[order_shoe.order_shoe_id]["sewingAmount"] = amount
        elif team == "成型":
            amount_map[order_shoe.order_shoe_id]["moldingAmount"] = amount
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getsubmittedquantityreports", methods=["GET"]
)
def get_submitted_quantity_reports():
    order_shoe_id = request.args.get("orderShoeId")
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    search_start_date = request.args.get("searchStartDate")
    search_end_date = request.args.get("searchEndDate")
    team = request.args.get("team")
    query = (
        db.session.query(OrderShoeProductionInfo, QuantityReport)
        .join(
            QuantityReport,
            OrderShoeProductionInfo.order_shoe_id == QuantityReport.order_shoe_id,
        )
        .filter(
            OrderShoeProductionInfo.order_shoe_id == order_shoe_id,
        )
        .filter(QuantityReport.status.in_([1, 2, 3]))
    )
    if search_start_date and search_end_date:
        try:
            datetime.strptime(search_start_date, "%Y-%m-%d")
            datetime.strptime(search_end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "invalid date range"}), 400
        query = query.filter(
            QuantityReport.creation_date >= search_start_date,
            QuantityReport.creation_date <= search_end_date,
        )
    if team and team in ["裁断", "针车预备", "针车", "成型"]:
        query = query.filter(QuantityReport.team == team)
    count_result = query.distinct().count()
    response = query.distinct().limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        production_info, report = row
        if report.team == "裁断":
            start_date = production_info.cutting_start_date
            end_date = production_info.cutting_end_date
        elif report.team == "针车预备":
            start_date = production_info.pre_sewing_start_date
            end_date = production_info.pre_sewing_start_date
        elif report.team == "针车":
            start_date = production_info.sewing_start_date
            end_date = production_info.sewing_start_date
        else:
            start_date = production_info.molding_start_date
            end_date = production_info.molding_end_date
        if report.status == 1:
            report_status = "未审批"
        elif report.status == 2:
            report_status = "已审批"
        else:
            report_status = "被驳回"
        obj = {
            "reportId": report.report_id,
            "creationDate": format_date(report.creation_date),
            "submissionDate": format_date(report.submission_date),
            "startDate": format_date(start_date),
            "endDate": format_date(end_date),
            "team": report.team,
            "reportStatus": report_status,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/approvequantityreport", methods=["PATCH"]
)
def approve_quantity_report():
    data = request.get_json()
    report = db.session.query(QuantityReport).get(data["reportId"])
    report.status = 2
    report.rejection_reason = None
    response = (
        db.session.query(func.sum(QuantityReportItem.report_amount), OrderShoeType)
        .join(
            OrderShoeType,
            QuantityReportItem.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .filter(QuantityReportItem.quantity_report_id == data["reportId"])
        .group_by(
            QuantityReportItem.quantity_report_id, QuantityReportItem.order_shoe_type_id
        )
        .all()
    )
    for row in response:
        team_amount, order_shoe_type = row
        if report.team == "裁断":
            order_shoe_type.cutting_amount += team_amount
        elif report.team == "针车预备":
            order_shoe_type.pre_sewing_amount += team_amount
        elif report.team == "针车":
            order_shoe_type.sewing_amount += team_amount
        elif report.team == "成型":
            order_shoe_type.molding_amount += team_amount
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/rejectquantityreport", methods=["PATCH"]
)
def reject_quantity_report():
    data = request.get_json()
    report = db.session.query(QuantityReport).get(data["reportId"])
    report.status = 3
    report.rejection_reason = data["rejectionReason"]
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/getpricereportapprovaloverview", methods=["GET"]
)
def get_price_report_approval_overview():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    team = request.args.get("team")
    query = (
        db.session.query(Order, OrderShoe, Customer, Shoe, OrderShoeStatus)
        .join(
            OrderShoe,
            Order.order_id == OrderShoe.order_id,
        )
        .join(Customer, Order.customer_id == Customer.customer_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .filter(
            OrderShoeStatus.current_status.in_([22, 29, 39]),
            OrderShoeStatus.current_status_value.in_([0, 1]),
        )
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if team and team != "":
        if team == "裁断":
            query = query.filter(OrderShoeStatus.current_status == 22)
        elif team == "针车":
            query = query.filter(OrderShoeStatus.current_status == 29)
        elif team == "成型":
            query = query.filter(OrderShoeStatus.current_status == 39)
        else:
            return jsonify({"message": "invalid team name"}), 400
    count_result = query.distinct().count()
    response = query.distinct().limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, customer, shoe, status_obj = row
        if status_obj.current_status == 22:
            team = "裁断"
        elif status_obj.current_status == 29:
            team = "针车"
        else:
            team = "成型"
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderEndDate": format_date(order.end_date),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerName": customer.customer_name,
            "customerProductName": order_shoe.customer_product_name,
            "team": team,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getallpricereportsforordershoe", methods=["GET"]
)
def get_all_price_reports_for_order_shoe():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        db.session.query(OrderShoeProductionInfo, UnitPriceReport)
        .join(
            UnitPriceReport,
            OrderShoeProductionInfo.order_shoe_id == UnitPriceReport.order_shoe_id,
        )
        .filter(
            OrderShoeProductionInfo.order_shoe_id == order_shoe_id,
            UnitPriceReport.status.in_([1, 2, 3]),
        )
        .all()
    )
    result = []
    for row in response:
        production_info, report = row
        if report.team == "裁断":
            start_date = production_info.cutting_start_date
            end_date = production_info.cutting_end_date
        elif report.team == "针车预备":
            start_date = production_info.pre_sewing_start_date
            end_date = production_info.pre_sewing_start_date
        elif report.team == "针车":
            start_date = production_info.sewing_start_date
            end_date = production_info.sewing_start_date
        else:
            start_date = production_info.molding_start_date
            end_date = production_info.molding_end_date
        if report.status == 1:
            status = "未审批"

        elif report.status == 2:
            status = "已审批"
        else:
            status = "已驳回"
        obj = {
            "productionStartDate": format_date(start_date),
            "productionEndDate": format_date(end_date),
            "reportId": report.report_id,
            "reportStatus": status,
            "team": report.team,
        }
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/approvepricereport", methods=["PATCH"]
)
def approve_price_report():
    data = request.get_json()
    order_shoe_id = data["orderShoeId"]
    report_id = data["reportId"]
    flag = True
    report = db.session.query(UnitPriceReport).get(report_id)
    # if it is sewing or pre-sewing report, check if either one is approved
    if report.team == "针车预备" or report.team == "针车":
        query = db.session.query(UnitPriceReport).filter_by(order_shoe_id=order_shoe_id)
        if report.team == "针车预备":
            report2 = query.filter_by(team="针车").first()
        else:
            report2 = query.filter_by(team="针车预备").first()
        if report2.status != 2:
            flag = False
    # sum up the price
    value = (
        db.session.query(func.sum(UnitPriceReportDetail.price))
        .filter_by(report_id=report_id)
        .group_by(UnitPriceReportDetail.report_id)
        .scalar()
    )
    report.price_sum = value
    report.status = 2
    report.rejection_reason = None
    if flag:
        processor: EventProcessor = current_app.config["event_processor"]
        if report.team == "裁断":
            operation_arr = [82, 83]
        elif report.team == "针车" or report.team == "预备":
            operation_arr = [96, 97]
        elif report.team == "成型":
            operation_arr = [116, 117]
        else:
            return jsonify({"message": "Cannot change current status"}), 403
        try:
            for operation in operation_arr:
                event = Event(
                    staff_id=1,
                    handle_time=datetime.now(),
                    operation_id=operation,
                    event_order_id=data["orderId"],
                    event_order_shoe_id=data["orderShoeId"],
                )
                processor.processEvent(event)
        except Exception as e:
            print(e)
            return jsonify({"message": "failed"}), 400
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/rejectpricereport", methods=["PATCH"]
)
def reject_price_report():
    data = request.get_json()
    report_id_arr = data["reportIdArr"]
    processor: EventProcessor = current_app.config["event_processor"]
    # find order shoe current status
    current_status_str = (
        db.session.query(
            func.group_concat(OrderShoeStatus.current_status).label(
                "current_status_str"
            ),
        )
        .filter_by(order_shoe_id=data["orderShoeId"])
        .group_by(OrderShoeStatus.order_shoe_id)
        .first()
    )
    current_status_arr = current_status_str[0].split(",")
    if "22" in current_status_arr:
        operation = 78
        current_status = 22
    elif "29" in current_status_arr:
        operation = 92
        current_status = 29
    elif "39" in current_status_arr:
        operation = 112
        current_status = 39
    else:
        return jsonify({"message": "Cannot change current status"}), 403
    try:
        for report_id in report_id_arr:
            report = db.session.query(UnitPriceReport).get(report_id)
            report.status = 3
            report.rejection_reason = data["rejectionReason"]
        event = Event(
            staff_id=1,
            handle_time=datetime.now(),
            operation_id=operation,
            event_order_id=data["orderId"],
            event_order_shoe_id=data["orderShoeId"],
        )
        processor.processRejectEvent(event, current_status)
    except Exception as e:
        print(e)
        return jsonify({"message": "failed"}), 400
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route("/production/downloadbatchinfo", methods=["GET"])
def download_batch_info():
    order_id = request.args.get("orderId")
    order_shoe_id = request.args.get("orderShoeId")
    shoe_rid = request.args.get("shoeRId")
    order_rid = request.args.get("orderRId")
    result = {}

    temp1 = get_order_info_helper(order_id, order_shoe_id)
    result["order_rid"] = temp1["orderRId"]
    result["shoe_rid"] = temp1["shoeRId"]
    result["customer_brand"] = temp1["customerBrand"]
    result["customer_product_name"] = temp1["customerProductName"]

    # temp2 = get_order_shoe_batch_info_helper(order_shoe_id)
    # result["batch_info"] = temp2
    
    temp2 = []
    response = (
        db.session.query(
            BatchInfoType,
            PackagingInfo,
            OrderShoeBatchInfo.packaging_info_quantity,
            Color
        )
        .join(
            Order, Order.batch_info_type_id == BatchInfoType.batch_info_type_id
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(OrderShoeBatchInfo, OrderShoeType.order_shoe_type_id == OrderShoeBatchInfo.order_shoe_type_id)
        .join(PackagingInfo, PackagingInfo.packaging_info_id == OrderShoeBatchInfo.packaging_info_id)
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(Order.order_id == order_id, OrderShoe.order_shoe_id == order_shoe_id)
        .all()
    )

    # track which column is all zero
    column_amount_mapping = {}
    for shoe_size in SHOESIZERANGE:
        column_amount_mapping[shoe_size] = False

    for row in response:
        batch_info_type, packaging_info, packaging_info_quantity, color = row
        obj = {
            "total_quantity_ratio": packaging_info.total_quantity_ratio,
            "packaging_info_quantity": packaging_info_quantity,
            "color_name": color.color_name,
            "packaging_info_name": packaging_info.packaging_info_name
        }
        for shoe_size in SHOESIZERANGE:
            number = getattr(packaging_info, f"size_{shoe_size}_ratio")
            if number > 0:
                column_amount_mapping[shoe_size] = True
            obj[f"size_{shoe_size}_ratio"] = number
        temp2.append(obj)
    
    # for row in temp2:
    #     for shoe_size in SHOESIZERANGE:
    #         if column_amount_mapping[shoe_size] == False:
    #             del row[f"size_{shoe_size}_ratio"]
            
    result["batch_info"] = temp2
    result["column_amount_mapping"] = column_amount_mapping

    temp3 = get_order_batch_type_helper(order_id)
    result["shoe_size_names"] = temp3

    template_path = os.path.join("./general_document", "装箱配码模板.xlsx")
    new_file_path = os.path.join("./general_document", "装箱配码.xlsx")
    new_name = f"订单{order_rid}-{shoe_rid}_装箱配码.xlsx"
    generate_excel_file(template_path, new_file_path, result)
    return send_file(new_file_path, as_attachment=True, download_name=new_name)
