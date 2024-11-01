import traceback
from datetime import datetime, timedelta

from api_utility import format_date, format_line_group
from app_config import db
from constants import *
from event_processor import EventProcessor
from flask import Blueprint, current_app, jsonify, request
from models import *
from sqlalchemy import func, or_
from sqlalchemy.dialects.mysql import insert
from constants import OUTSOURCE_STATUS_MAPPING

production_manager_bp = Blueprint("production_manager_bp", __name__)


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
    query = (
        db.session.query(
            Order,
            Customer,
        )
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(Order.order_id == order_id)
    )
    if order_shoe_id and order_shoe_id != "":
        response = query.add_columns(OrderShoe, Shoe).join(
            OrderShoe, Order.order_id == OrderShoe.order_id
        ).join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        ).join(
            OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id
        ).join(
            ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id
        ).join(
            Shoe, Shoe.shoe_id == ShoeType.shoe_id
        ).filter(
            OrderShoe.order_shoe_id == order_shoe_id
        ).first()
        order, customer, order_shoe, shoe = response
        result = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "orderStartDate": order.start_date.strftime("%Y-%m-%d"),
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name
        }
    else:
        response = query.first()
        order, customer = response
        result = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "orderStartDate": order.start_date.strftime("%Y-%m-%d"),
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
        }
    return jsonify(result)

@production_manager_bp.route(
    "/production/productionmanager/getinprogressorders", methods=["GET"]
)
def get_in_progress_orders():
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    query = (
        db.session.query(
            Order,
            Customer,
            func.min(OrderShoeProductionInfo.cutting_start_date),
            func.max(OrderShoeProductionInfo.molding_end_date),
            func.sum(OrderShoeBatchInfo.total_amount),
            func.sum(OrderShoeBatchInfo.molding_amount),
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
    count_result = query.distinct().count()
    response = query.limit(number).offset((page - 1) * number).all()
    result = []
    for row in response:
        (
            order,
            customer,
            cutting_start_date,
            molding_end_date,
            total_amount,
            molding_amount,
        ) = row
        cutting_start_date = format_date(cutting_start_date)
        molding_end_date = format_date(molding_end_date)
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "startDate": cutting_start_date,
            "endDate": molding_end_date,
            "orderStartDate": order.start_date.strftime("%Y-%m-%d"),
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
            "orderTotalShoes": total_amount,
            "finishedShoes": molding_amount,
        }
        result.append(obj)
    return {"result": result, "total": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getproductionlines", methods=["GET"]
)
def get_production_lines():
    return jsonify(PRODUCTION_LINES)


@production_manager_bp.route(
    "/production/productionmanager/getordershoescheduleinfo", methods=["GET"]
)
def get_order_shoe_schedule_info():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        db.session.query(
            OrderShoeProductionInfo,
        )
        .filter(OrderShoeProductionInfo.order_shoe_id == order_shoe_id)
        .first()
    )
    cutting_start_date = format_date(response.cutting_start_date)
    cutting_end_date = format_date(response.cutting_end_date)
    pre_sewing_start_date = format_date(response.pre_sewing_start_date)
    pre_sewing_end_date = format_date(response.pre_sewing_end_date)
    sewing_start_date = format_date(response.sewing_start_date)
    sewing_end_date = format_date(response.sewing_end_date)
    molding_start_date = format_date(response.molding_start_date)
    molding_end_date = format_date(response.molding_end_date)
    cutting_line_group = format_line_group(response.cutting_line_group)
    pre_sewing_line_group = format_line_group(response.pre_sewing_line_group)
    sewing_line_group = format_line_group(response.sewing_line_group)
    molding_line_group = format_line_group(response.molding_line_group)
    result = {
        "cuttingLineNumbers": cutting_line_group,
        "preSewingLineNumbers": pre_sewing_line_group,
        "sewingLineNumbers": sewing_line_group,
        "moldingLineNumbers": molding_line_group,
        "cuttingStartDate": cutting_start_date,
        "cuttingEndDate": cutting_end_date,
        "preSewingStartDate": pre_sewing_start_date,
        "preSewingEndDate": pre_sewing_end_date,
        "sewingStartDate": sewing_start_date,
        "sewingEndDate": sewing_end_date,
        "moldingStartDate": molding_start_date,
        "moldingEndDate": molding_end_date,
        "isCuttingOutsourced": response.is_cutting_outsourced,
        "isSewingOutsourced": response.is_sewing_outsourced,
        "isMoldingOutsourced": response.is_molding_outsourced,
    }
    return result


# @production_manager_bp.route(
#     "/production/productionmanager/getproductioninfo", methods=["GET"]
# )
# def get_production_info():
#     # 参考scheduleView.vue 441行
#     team = request.args.get("team")
#     # 成型号
#     number = request.args.get("number")
#     if team == "cutting":
#         status = 23
#         line_usage = OrderShoeProductionInfo.cutting_line_group
#         start_date = OrderShoeProductionInfo.cutting_start_date
#         end_date = OrderShoeProductionInfo.cutting_end_date
#     elif team == "preSewing":
#         status = 29
#         line_usage = OrderShoeProductionInfo.pre_sewing_line_group
#         start_date = OrderShoeProductionInfo.pre_sewing_start_date
#         end_date = OrderShoeProductionInfo.pre_sewing_end_date
#     elif team == "sewing":
#         status = 31
#         line_usage = OrderShoeProductionInfo.sewing_line_group
#         start_date = OrderShoeProductionInfo.sewing_start_date
#         end_date = OrderShoeProductionInfo.sewing_end_date
#     elif team == "molding":
#         status = 39
#         line_usage = OrderShoeProductionInfo.molding_line_group
#         start_date = OrderShoeProductionInfo.molding_start_date
#         end_date = OrderShoeProductionInfo.molding_end_date
#     else:
#         return {"message": "failed"}, 400
#     response = (
#         db.session.query(
#             Order,
#             Shoe,
#             func.sum(OrderShoeBatchInfo.total_amount),
#             line_usage,
#             start_date,
#             end_date,
#         )
#         .join(OrderShoe, OrderShoe.order_id == Order.order_id)
#         .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
#         .join(
#             OrderShoeBatchInfo,
#             OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
#         )
#         .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
#         .join(
#             OrderShoeProductionInfo,
#             OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
#         )
#         .filter(OrderShoeStatus.current_status == status)
#         .group_by(Order.order_id, OrderShoe.order_shoe_id)
#         .all()
#     )

#     result = []
#     for row in response:
#         (
#             order,
#             shoe,
#             total_amount,
#             line_usage_info,
#             start_date_val,
#             end_date_val,
#         ) = row
#         val = len(line_usage_info.split(","))
#         obj = {
#             "startDate": start_date_val,
#             "endDate": end_date_val,
#             "orderId": order.order_id,
#             "orderRId": order.order_rid,
#             "shoeRId": shoe.shoe_rid,
#             "number": total_amount,
#             "lineUsage": val,
#         }
#         result.append(obj)
#     return result


def is_valid_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return None


@production_manager_bp.route(
    "/production/productionmanager/editproductionschedule", methods=["PATCH"]
)
def edit_production_schedule():
    data = request.get_json()
    entity = OrderShoeProductionInfo.query.filter(
        OrderShoeProductionInfo.order_shoe_id == data["orderShoeId"]
    ).first()
    entity.cutting_line_group = data["cuttingInfo"]["lineValue"]
    entity.is_cutting_outsourced = data["cuttingInfo"]["isOutsourced"]

    if is_valid_date(data["cuttingInfo"]["startDate"]):
        entity.cutting_start_date = data["cuttingInfo"]["startDate"]

    if is_valid_date(data["cuttingInfo"]["endDate"]):
        entity.cutting_end_date = data["cuttingInfo"]["endDate"]

    entity.pre_sewing_line_group = data["sewingInfo"]["lineValue"]

    if is_valid_date(data["sewingInfo"]["startDate"]):
        entity.pre_sewing_start_date = data["sewingInfo"]["startDate"]

    if is_valid_date(data["sewingInfo"]["endDate"]):
        entity.pre_sewing_end_date = data["sewingInfo"]["endDate"]

    entity.sewing_line_group = data["sewingInfo"]["lineValue"]
    entity.is_sewing_outsourced = data["sewingInfo"]["isOutsourced"]

    if is_valid_date(data["sewingInfo"]["startDate"]):
        entity.sewing_start_date = data["sewingInfo"]["startDate"]

    if is_valid_date(data["sewingInfo"]["endDate"]):
        entity.sewing_end_date = data["sewingInfo"]["endDate"]

    entity.molding_line_group = data["moldingInfo"]["lineValue"]
    entity.is_molding_outsourced = data["moldingInfo"]["isOutsourced"]

    if is_valid_date(data["moldingInfo"]["startDate"]):
        entity.molding_start_date = data["moldingInfo"]["startDate"]

    if is_valid_date(data["moldingInfo"]["endDate"]):
        entity.molding_end_date = data["moldingInfo"]["endDate"]
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/startproduction", methods=["PATCH"]
)
def start_production():
    data = request.get_json()
    # pass to event processor
    processor: EventProcessor = current_app.config["event_processor"]
    try:
        for operation in [72, 73]:
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
    return jsonify({"message": "success"}), 200


@production_manager_bp.route(
    "/production/productionmanager/getorderproductiondetail", methods=["GET"]
)
def get_order_production_detail():
    order_id = request.args.get("orderId")
    response = (
        db.session.query(
            OrderShoe,
            Shoe,
            func.group_concat(OrderShoeStatus.current_status).label(
                "current_status_str"
            ),
            func.group_concat(OrderShoeStatus.current_status_value).label(
                "current_status_value_str"
            ),
        )
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .filter(OrderShoe.order_id == order_id)
        .group_by(OrderShoe.order_shoe_id)
        .all()
    )
    result = []
    for row in response:
        order_shoe, shoe, current_status_str, current_status_value_str = row
        current_status_arr = current_status_str.split(",")
        current_status_value_arr = current_status_value_str.split(",")
        if "0" in current_status_arr:
            status = "创建投产指令单中"
        elif "17" in current_status_arr:
            if current_status_value_arr[current_status_arr.index("17")] == "2":
                status = "已排产，技术部调板未下发"
            else:
                status = "未排产"
        elif "18" in current_status_arr:
            status = "技术部调板已下发，等待确认开始生产"
        elif "42" in current_status_arr:
            status = "生产完毕"
        else:
            status = "正在生产"
        obj = {
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "totalShoes": 0,
            "detail": [],
            "status": status,
        }
        detail_response = (
            db.session.query(ShoeType, OrderShoeBatchInfo, Color)
            .join(OrderShoeType, OrderShoeType.shoe_type_id == ShoeType.shoe_type_id)
            .join(
                OrderShoeBatchInfo,
                OrderShoeBatchInfo.order_shoe_type_id
                == OrderShoeType.order_shoe_type_id,
            )
            .join(Color, Color.color_id == ShoeType.color_id)
            .filter(OrderShoeType.order_shoe_id == order_shoe.order_shoe_id)
            .all()
        )
        for detail_row in detail_response:
            shoe_type, batch_info, color = detail_row
            obj["totalShoes"] += batch_info.total_amount
            obj["detail"].append(
                {
                    "batchInfoName": batch_info.name,
                    "colorName": color.color_name,
                    "batchAmount": batch_info.total_amount,
                    "cuttingAmount": batch_info.cutting_amount,
                    "preSewingAmount": batch_info.pre_sewing_amount,
                    "sewingAmount": batch_info.sewing_amount,
                    "moldingAmount": batch_info.molding_amount,
                    "imageurl": shoe_type.shoe_image_url,
                }
            )
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/getproductiondepartments", methods=["GET"]
)
def get_production_departments():
    return jsonify(["裁断", "针车", "成型"])


@production_manager_bp.route(
    "/production/productionmanager/getlogisticsoverview", methods=["GET"]
)
def get_logistics_overview():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    query = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderStatus, Order.order_id == OrderStatus.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(OrderStatus.order_current_status == IN_PRODUCTION_ORDER_NUMBER)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    count_result = query.distinct().count()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, shoe = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getfinishednodes", methods=["GET"]
)
def get_finished_nodes():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    status_point = request.args.get("nodeName")
    query = (
        db.session.query(Order, OrderShoe, Shoe, OrderShoeStatusReference)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderStatus, Order.order_id == OrderStatus.order_id)
        .join(
            OrderShoeStatusReference,
            OrderShoeStatusReference.status_id == OrderShoeStatus.current_status,
        )
        .filter(OrderStatus.order_current_status == 9)
        .filter(OrderShoeStatus.current_status_value.in_([0, 1]))
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    if status_point and ORDER_SHOE_STATUS_REFERENCE[status_point]:
        query = query.filter(
            OrderShoeStatus.current_status == ORDER_SHOE_STATUS_REFERENCE[status_point]
        )
    else:
        query = query.filter(
            OrderShoeStatus.current_status.in_([18, 23, 24, 30, 31, 32, 33, 40, 41, 42])
        )
    count_result = query.distinct().count()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, shoe, reference = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "nodeName": reference.status_name,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getordershoebatchinfoforproduction", methods=["GET"]
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
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    if team == "裁断":
        search_start_date = "cutting_start_date"
        search_end_date = "cutting_end_date"
    elif team == "针车预备":
        search_start_date = "pre_sewing_start_date"
        search_end_date = "pre_sewing_end_date"
    elif team == "针车":
        search_start_date = "sewing_start_date"
        search_end_date = "sewing_end_date"
    elif team == "成型":
        search_start_date = "molding_start_date"
        search_end_date = "molding_end_date"
    else:
        return jsonify({"message": "invalid team name"}), 400

    sub_table = (
        db.session.query(
            OrderShoe,
            OrderShoeType,
            func.sum(OrderShoeBatchInfo.total_amount).label("total_amount"),
        )
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
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
            "productionStartDate": production_start_date.strftime("%Y-%m-%d"),
            "productionEndDate": production_end_date.strftime("%Y-%m-%d"),
        }
        current_date = first_day
        while current_date <= end_day:
            order_shoes_delta[current_date].append(obj)
            current_date += delta

    for day in all_days:
        result.append(
            {
                "date": day.strftime("%Y-%m-%d"),
                "orderShoeCount": len(order_shoes_delta[day]),
                "detail": order_shoes_delta[day],
            }
        )

    return result


@production_manager_bp.route(
    "/production/productionmanager/getordershoestatus", methods=["GET"]
)
def get_order_shoe_status():
    order_shoe_id = request.args.get("orderShoeId")
    order_shoe_status = (
        db.session.query(func.group_concat(OrderShoeStatus.current_status))
        .filter(OrderShoeStatus.order_shoe_id == order_shoe_id)
        .first()
    )
    arr = order_shoe_status[0].split(",")
    return arr


@production_manager_bp.route(
    "/production/productionmanager/editordershoestatus", methods=["PATCH"]
)
def edit_order_shoe_status():
    data = request.get_json()
    order_shoe_id = data["orderShoeId"]
    arr = []
    order_shoe_status, status_value = (
        db.session.query(
            func.group_concat(OrderShoeStatus.current_status),
            func.group_concat(OrderShoeStatus.current_status_value),
        )
        .filter(OrderShoeStatus.order_shoe_id == order_shoe_id)
        .first()
    )
    status_arr: list = order_shoe_status.split(",")
    status_value_arr: list = status_value.split(",")

    # 相关外包完成才能推进生产线完成
    outsource_info = (
        db.session.query(OutsourceInfo).filter_by(order_shoe_id=order_shoe_id).all()
    )
    for info in outsource_info:
        if (
            (
                "24" in status_arr
                and info.outsource_type[-1] == "0"
                and info.outsource_status != 7
            )
            or (
                "33" in status_arr
                and info.outsource_type[-1] == "1"
                and info.outsource_status != 7
            )
            or (
                "41" in status_arr
                and info.outsource_type[-1] == "2"
                and info.outsource_status != 7
            )
        ):
            return jsonify({"message": "外包尚未完成"}), 400

    # 半成品或成品入库完成才能推进生产线完成
    storage_status = None
    if "24" in status_arr:
        storage_status = (
            db.session.query(
                SemifinishedShoeStorage.semifinished_status.label("storage_status")
            )
            .filter_by(order_shoe_id=order_shoe_id, semifinished_object=0)
            .scalar()
        )
    elif "33" in status_arr:
        storage_status = (
            db.session.query(
                SemifinishedShoeStorage.semifinished_status.label("storage_status")
            )
            .filter_by(order_shoe_id=order_shoe_id, semifinished_object=1)
            .scalar()
        )
    elif "41" in status_arr:
        storage_status = (
            db.session.query(
                FinishedShoeStorage.finished_status.label("storage_status")
            )
            .filter_by(order_shoe_id=order_shoe_id)
            .scalar()
        )
    if storage_status and storage_status != 1:
        return jsonify({"message": "制品尚未入库"}), 400

    team = -1
    if "18" in status_arr:
        team = 0
        arr.append(
            SemifinishedShoeStorage(
                order_shoe_id=order_shoe_id,
                semifinished_status=0,
                semifinished_object=0,
            )
        )
    elif "24" in status_arr:
        team = 1
        arr.append(
            SemifinishedShoeStorage(
                order_shoe_id=order_shoe_id,
                semifinished_status=0,
                semifinished_object=1,
            )
        )
    elif "33" in status_arr:
        team = 2
        arr.append(
            FinishedShoeStorage(
                order_shoe_id=order_shoe_id,
                finished_status=0,
            )
        )
    if team > -1:
        # 如果没有自产，直接跳至工组结束
        production_amount = (
            db.session.query(
                func.sum(OrderShoeProductionAmount.total_production_amount)
            )
            .join(
                OrderShoeBatchInfo,
                OrderShoeBatchInfo.order_shoe_batch_info_id
                == OrderShoeProductionAmount.order_shoe_batch_info_id,
            )
            .join(
                OrderShoeType,
                OrderShoeBatchInfo.order_shoe_type_id
                == OrderShoeType.order_shoe_type_id,
            )
            .join(OrderShoe, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
            .filter(
                OrderShoe.order_shoe_id == order_shoe_id,
                OrderShoeProductionAmount.production_team == team,
            )
            .group_by(
                OrderShoe.order_shoe_id, OrderShoeProductionAmount.production_team
            )
            .scalar()
        )
        if production_amount == 0:
            current_status_id = -1
            next_status_id = -1
            if "18" in status_arr:
                current_status_id = 18
                next_status_id = 24
            elif "24" in status_arr:
                current_status_id = 24
                next_status_id = 33
            elif "33" in status_arr:
                current_status_id = 33
                next_status_id = 41
            else:
                return (
                    jsonify({"message": "Invalid status"}),
                    400,
                )
            status_obj = (
                db.session.query(OrderShoeStatus)
                .filter_by(
                    order_shoe_id=order_shoe_id, current_status=current_status_id
                )
                .first()
            )
            status_obj.current_status = next_status_id
            status_obj.current_status_value = 0
            db.session.add_all(arr)
            db.session.commit()
            return jsonify({"message": "跳至下一生产线结束"}), 200
    production_nodes = ["18", "23", "24", "30", "31", "32", "33", "40", "41", "42"]
    matching_status = next((num for num in status_arr if num in production_nodes), None)
    if not matching_status:
        return (
            jsonify({"message": "You cannot progress the production in this state"}),
            400,
        )
    # 生产线开始要等工价审批完才能结束
    if "23" in status_arr and (
        "22" not in status_arr or (status_value_arr[status_arr.index("22")] != "2")
    ):
        return jsonify({"message": "裁断工价单尚未审批"}), 400
    if "32" in status_arr and (
        "29" not in status_arr or (status_value_arr[status_arr.index("29")] != "2")
    ):
        return jsonify({"message": "针车工价单尚未审批"}), 400
    if "40" in status_arr and (
        "39" not in status_arr or (status_value_arr[status_arr.index("39")] != "2")
    ):
        return jsonify({"message": "成型工价单尚未审批"}), 400
    if "18" in status_arr:
        report1 = UnitPriceReport(order_shoe_id=order_shoe_id, team="裁断", status=0)
        arr.append(report1)
    elif "24" in status_arr:
        report1 = UnitPriceReport(
            order_shoe_id=order_shoe_id, team="针车预备", status=0
        )
        report2 = UnitPriceReport(order_shoe_id=order_shoe_id, team="针车", status=0)
        arr.append(report1)
        arr.append(report2)
    elif "33" in status_arr:
        report = UnitPriceReport(order_shoe_id=order_shoe_id, team="成型", status=0)
        arr.append(report)
    try:
        processor: EventProcessor = current_app.config["event_processor"]
        # find operation id
        operations = (
            db.session.query(Operation)
            .filter_by(operation_type=2, operation_modified_status=int(matching_status))
            .all()
        )
        operation_ids = [row.operation_id for row in operations]
        for op in operation_ids:
            event = Event(
                staff_id=1,
                handle_time=datetime.now(),
                operation_id=op,
                event_order_id=data["orderId"],
                event_order_shoe_id=order_shoe_id,
            )
            processor.processEvent(event)
    except Exception as e:
        print(e)
        return jsonify({"message": "failed"}), 400
    db.session.add_all(arr)
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/getorderoutsourceoverview", methods=["GET"]
)
def get_order_outsource_overview():
    page = request.args.get("page", type=int)
    page_size = request.args.get("pageSize", type=int)
    order_rid = request.args.get("orderRId")
    shoe_rid = request.args.get("shoeRId")
    query = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            Customer,
            OrderShoeProductionInfo.is_cutting_outsourced,
            OrderShoeProductionInfo.is_sewing_outsourced,
            OrderShoeProductionInfo.is_molding_outsourced,
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderStatus, OrderStatus.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(Customer, Customer.customer_id == Order.customer_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .filter(OrderStatus.order_current_status == IN_PRODUCTION_ORDER_NUMBER)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"%{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"%{shoe_rid}%"))
    count_result = query.distinct().count()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        (
            order,
            order_shoe,
            shoe,
            customer,
            is_cutting_outsourced,
            is_sewing_outsourced,
            is_molding_outsourced,
        ) = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "orderEndDate": format_date(order.end_date),
            "isCuttingOutsourced": is_cutting_outsourced,
            "isSewingOutsourced": is_sewing_outsourced,
            "isMoldingOutsourced": is_molding_outsourced,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getordershoebatchestimatedamount", methods=["GET"]
)
def get_order_shoe_batch_estimated_amount():
    order_shoe_id = request.args.get("orderShoeId")
    entities = (
        db.session.query(OrderShoeBatchInfo, OrderShoeProductionAmount, Color)
        .join(
            OrderShoeType,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(
            OrderShoeProductionAmount,
            OrderShoeProductionAmount.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
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
        order_shoe_batch_info, order_shoe_production_amount, color = entity
        team = order_shoe_production_amount.production_team
        if team not in color_totals:
            color_totals[team] = {}
        else:
            if color.color_name not in color_totals[team]:
                color_totals[team][color.color_name] = 0
            if order_shoe_production_amount.total_production_amount:
                color_totals[team][
                    color.color_name
                ] += order_shoe_production_amount.total_production_amount
    # Second loop to build the result list and include the color totals
    result = {}
    for entity in entities:
        order_shoe_batch_info, order_shoe_production_amount, color = entity
        team = order_shoe_production_amount.production_team
        actual_total_amount = order_shoe_production_amount.total_production_amount
        if team not in result:
            result[team] = []
        if not actual_total_amount:
            actual_total_amount = 0
        result[team].append(
            {
                "productionAmountId": order_shoe_production_amount.order_shoe_production_amount_id,
                "orderShoeBatchInfoId": order_shoe_batch_info.order_shoe_batch_info_id,
                "batchName": order_shoe_batch_info.name,
                "size34": order_shoe_production_amount.size_34_production_amount,
                "size35": order_shoe_production_amount.size_35_production_amount,
                "size36": order_shoe_production_amount.size_36_production_amount,
                "size37": order_shoe_production_amount.size_37_production_amount,
                "size38": order_shoe_production_amount.size_38_production_amount,
                "size39": order_shoe_production_amount.size_39_production_amount,
                "size40": order_shoe_production_amount.size_40_production_amount,
                "size41": order_shoe_production_amount.size_41_production_amount,
                "size42": order_shoe_production_amount.size_42_production_amount,
                "size43": order_shoe_production_amount.size_43_production_amount,
                "size44": order_shoe_production_amount.size_44_production_amount,
                "size45": order_shoe_production_amount.size_45_production_amount,
                "size46": order_shoe_production_amount.size_46_production_amount,
                "colorName": color.color_name,
                "pairAmount": actual_total_amount,
                "totalAmount": color_totals[team][color.color_name],
                "productionTeam": team,
            }
        )
    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/getordershoebatchinfo", methods=["GET"]
)
def get_order_shoe_batch_info():
    order_shoe_id = request.args.get("orderShoeId")
    entities = (
        db.session.query(OrderShoeBatchInfo, Color)
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
        order_shoe_batch_info, color = entity
        if color.color_name not in color_totals:
            color_totals[color.color_name] = 0
        color_totals[color.color_name] += order_shoe_batch_info.total_amount
    # Second loop to build the result list and include the color totals
    result = []
    for entity in entities:
        order_shoe_batch_info, color = entity
        result.append(
            {
                "orderShoeBatchInfoId": order_shoe_batch_info.order_shoe_batch_info_id,
                "batchName": order_shoe_batch_info.name,
                "size34": order_shoe_batch_info.size_34_amount,
                "size35": order_shoe_batch_info.size_35_amount,
                "size36": order_shoe_batch_info.size_36_amount,
                "size37": order_shoe_batch_info.size_37_amount,
                "size38": order_shoe_batch_info.size_38_amount,
                "size39": order_shoe_batch_info.size_39_amount,
                "size40": order_shoe_batch_info.size_40_amount,
                "size41": order_shoe_batch_info.size_41_amount,
                "size42": order_shoe_batch_info.size_42_amount,
                "size43": order_shoe_batch_info.size_43_amount,
                "size44": order_shoe_batch_info.size_44_amount,
                "size45": order_shoe_batch_info.size_45_amount,
                "size46": order_shoe_batch_info.size_46_amount,
                "colorName": color.color_name,
                "pairAmount": order_shoe_batch_info.total_amount,
                "totalAmount": color_totals[
                    color.color_name
                ],  # Add total amount for the color
            }
        )
    return jsonify(result)


@production_manager_bp.route(
    "/production/productionmanager/saveproductionamount", methods=["PATCH"]
)
def save_production_amount():
    data = request.get_json()
    for row in data:
        obj = {}
        # set production_amount_id
        if "productionAmountId" in row:
            obj["order_shoe_production_amount_id"] = row["productionAmountId"]
        obj["total_production_amount"] = 0
        obj["order_shoe_batch_info_id"] = row["orderShoeBatchInfoId"]
        obj["production_team"] = row["productionTeam"]
        for i in range(34, 47):
            obj[f"size_{i}_production_amount"] = 0
            if f"size{i}" in row:
                if not row[f"size{i}"]:
                    row[f"size{i}"] = 0
                obj[f"size_{i}_production_amount"] = int(row[f"size{i}"])
                obj["total_production_amount"] += int(row[f"size{i}"])
        stmt = insert(OrderShoeProductionAmount).values(**obj)
        stmt = stmt.on_duplicate_key_update(**obj)
        db.session.execute(stmt)
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/getordershoeoutsourceinfo", methods=["GET"]
)
def get_order_shoe_outsource_info():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        (
            db.session.query(OutsourceInfo, OutsourceFactory)
            .join(OrderShoe, OrderShoe.order_shoe_id == OutsourceInfo.order_shoe_id)
            .join(
                OutsourceFactory,
                OutsourceFactory.factory_id == OutsourceInfo.factory_id,
            )
        )
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
        .all()
    )
    result = []
    for row in response:
        outsource_info, factory = row
        temp = []
        for number in outsource_info.outsource_type.split(","):
            if number == "0":
                temp.append("裁断")
            elif number == "1":
                temp.append("针车")
            elif number == "2":
                temp.append("成型")
        obj = {
            "outsourceInfoId": outsource_info.outsource_info_id,
            "outsourceType": temp,
            "outsourceFactory": {
                "id": factory.factory_id,
                "value": factory.factory_name,
            },
            "outsourceAmount": outsource_info.outsource_amount,
            "outsourceStartDate": outsource_info.outsource_start_date.strftime(
                "%Y-%m-%d"
            ),
            "outsourceEndDate": outsource_info.outsource_end_date.strftime("%Y-%m-%d"),
            "outsourceStatus": outsource_info.outsource_status,
            "deadlineDate": outsource_info.deadline_date.strftime("%Y-%m-%d"),
            "semifinishedRequired": outsource_info.semifinished_required,
            "materialEstimatedOutboundDate": outsource_info.material_estimated_outbound_date.strftime(
                "%Y-%m-%d"
            ),
        }
        if outsource_info.semifinished_estimated_outbound_date:
            obj["semifinishedEstimatedOutboundDate"] = (
                outsource_info.semifinished_estimated_outbound_date.strftime("%Y-%m-%d")
            )
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/getoutsourcebatchinfo", methods=["GET"]
)
def get_outsource_batch_info():
    order_shoe_id = request.args.get("orderShoeId")
    outsource_info_id = request.args.get("outsourceInfoId")
    entities = (
        db.session.query(OrderShoeBatchInfo, OutsourceBatchInfo, Color)
        .join(
            OutsourceBatchInfo,
            OutsourceBatchInfo.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
        )
        .join(
            OrderShoeType,
            OrderShoeBatchInfo.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, Color.color_id == ShoeType.color_id)
        .filter(
            OrderShoeType.order_shoe_id == order_shoe_id,
            OutsourceBatchInfo.outsource_info_id == outsource_info_id,
        )
        .all()
    )
    # Dictionary to accumulate total amounts by color
    color_totals = {}

    # First loop to accumulate total amounts for each color
    for entity in entities:
        order_shoe_batch_info, outsource_batch_info, color = entity
        if color.color_name not in color_totals:
            color_totals[color.color_name] = 0
        color_totals[color.color_name] += outsource_batch_info.batch_outsource_amount
    # Second loop to build the result list and include the color totals
    result = []
    for entity in entities:
        order_shoe_batch_info, outsource_batch_info, color = entity
        result.append(
            {
                "outsourceBatchInfoId": outsource_batch_info.outsource_batch_info_id,
                "orderShoeBatchInfoId": order_shoe_batch_info.order_shoe_batch_info_id,
                "batchName": order_shoe_batch_info.name,
                "size34": outsource_batch_info.size_34_outsource_amount,
                "size35": outsource_batch_info.size_35_outsource_amount,
                "size36": outsource_batch_info.size_36_outsource_amount,
                "size37": outsource_batch_info.size_37_outsource_amount,
                "size38": outsource_batch_info.size_38_outsource_amount,
                "size39": outsource_batch_info.size_39_outsource_amount,
                "size40": outsource_batch_info.size_40_outsource_amount,
                "size41": outsource_batch_info.size_41_outsource_amount,
                "size42": outsource_batch_info.size_42_outsource_amount,
                "size43": outsource_batch_info.size_43_outsource_amount,
                "size44": outsource_batch_info.size_44_outsource_amount,
                "size45": outsource_batch_info.size_45_outsource_amount,
                "size46": outsource_batch_info.size_46_outsource_amount,
                "colorName": color.color_name,
                "pairAmount": outsource_batch_info.batch_outsource_amount,
                "totalAmount": color_totals[
                    color.color_name
                ],  # Add total amount for the color
            }
        )
    return result


@production_manager_bp.route(
    "/production/productionmanager/storeoutsourceforordershoe", methods=["PUT"]
)
def store_outsource_for_order_shoe():
    outsource_input = request.get_json()
    departments = ""
    for line in outsource_input["type"]:
        if line == "裁断":
            departments += "0,"
        elif line == "针车":
            departments += "1,"
        elif line == "成型":
            departments += "2,"
        else:
            return jsonify({"message": "failed"}), 400
    departments = departments[:-1]
    obj = {
        "outsource_type": departments,
        "factory_id": outsource_input["factoryId"],
        "outsource_start_date": outsource_input["outsourceStartDate"],
        "outsource_end_date": outsource_input["outsourceEndDate"],
        "deadline_date": outsource_input["deadlineDate"],
        "material_estimated_outbound_date": outsource_input[
            "materialEstimatedOutboundDate"
        ],
        "outsource_amount": 0,
        "outsource_status": 0,
        "order_shoe_id": outsource_input["orderShoeId"],
    }
    obj["semifinished_required"] = outsource_input["semifinishedRequired"]
    if obj["semifinished_required"]:
        obj["semifinished_estimated_outbound_date"] = outsource_input[
            "semifinishedEstimatedOutboundDate"
        ]
    else:
        obj["semifinished_estimated_outbound_date"] = None
    info_obj = None
    outsource_info_id = -1
    if "outsourceInfoId" in outsource_input:
        obj["outsource_info_id"] = outsource_input["outsourceInfoId"]
        outsource_info_id = outsource_input["outsourceInfoId"]
        stmt = insert(OutsourceInfo).values(**obj)
        stmt = stmt.on_duplicate_key_update(**obj)
        db.session.execute(stmt)
    else:
        info_obj = OutsourceInfo(**obj)
        db.session.add(info_obj)
        db.session.flush()
        outsource_info_id = info_obj.outsource_info_id
    # set production info
    production_obj = OrderShoeProductionInfo.query.filter_by(
        order_shoe_id=outsource_input["orderShoeId"]
    ).first()
    for line in outsource_input["type"]:
        if line == "裁断":
            production_obj.is_cutting_outsourced = True
        elif line == "针车":
            production_obj.is_sewing_outsourced = True
        elif line == "成型":
            production_obj.is_molding_outsourced = True

    total_outsource_amount = 0
    for row in outsource_input["outsourceAmount"]:
        outsource_obj = {}

        # set outsource_batch_info_id
        if "outsourceBatchInfoId" in row:
            outsource_obj["outsource_batch_info_id"] = row["outsourceBatchInfoId"]
        outsource_obj["batch_outsource_amount"] = 0
        for i in range(34, 47):
            outsource_obj[f"size_{i}_outsource_amount"] = 0
            if f"size{i}Val" in row:
                outsource_obj[f"size_{i}_outsource_amount"] = int(row[f"size{i}Val"])
                outsource_obj["batch_outsource_amount"] += int(row[f"size{i}Val"])

        # set outsource_info_id
        outsource_obj["outsource_info_id"] = outsource_info_id

        # ser order_shoe_batch_info_id
        outsource_obj["order_shoe_batch_info_id"] = row["orderShoeBatchInfoId"]

        stmt = insert(OutsourceBatchInfo).values(**outsource_obj)
        stmt = stmt.on_duplicate_key_update(**outsource_obj)
        db.session.execute(stmt)
        total_outsource_amount += outsource_obj["batch_outsource_amount"]

    # set amount
    outsource_info = db.session.query(OutsourceInfo).get(outsource_info_id)
    outsource_info.outsource_amount = total_outsource_amount
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/deleteoutsourceinfo", methods=["DELETE"]
)
def delete_outsource_info():
    order_shoe_id = request.args.get("orderShoeId")
    outsource_info_id = request.args.get("outsourceInfoId")
    outsource_info = (
        db.session.query(OutsourceInfo)
        .filter(OutsourceInfo.outsource_info_id == outsource_info_id)
        .first()
    )
    # set production info
    production_obj = OrderShoeProductionInfo.query.filter_by(
        order_shoe_id=order_shoe_id
    ).first()
    for line in outsource_info.outsource_type.split(","):
        if line == "0":
            production_obj.is_cutting_outsourced = False
        elif line == "1":
            production_obj.is_sewing_outsourced = False
        elif line == "2":
            production_obj.is_molding_outsourced = False

    db.session.delete(outsource_info)
    db.session.query(OutsourceBatchInfo).filter(
        OutsourceBatchInfo.outsource_info_id == outsource_info_id
    ).delete()
    db.session.commit()
    return jsonify({"message": "succuess"})


@production_manager_bp.route(
    "/production/productionmanager/submitoutsourceinfo", methods=["PATCH"]
)
def submit_outsource_info():
    data = request.get_json()
    # set approval status to 1
    info_id = data["outsourceInfoId"]
    response = (
        db.session.query(OutsourceInfo)
        .filter(OutsourceInfo.outsource_info_id == info_id)
        .first()
    )
    response.outsource_status = 1
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/editoutsourcestatus", methods=["PATCH"]
)
def edit_outsource_status():
    data = request.get_json()
    outsource_info_id = data["outsourceInfoId"]
    outsource_obj = db.session.query(OutsourceInfo).get(outsource_info_id)
    outsource_obj.outsource_status = data["outsourceStatus"]
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/getoutsourcesemifinishedshipping", methods=["GET"]
)
def get_outsource_semifinished_shipping():
    outsource_info_id = request.args.get("outsourceInfoId")
    response = (
        db.session.query(OutsourceInfo, SemifinishedShoeStorage, ShoeOutboundRecord)
        .join(
            SemifinishedShoeStorage,
            SemifinishedShoeStorage.order_shoe_id == OutsourceInfo.order_shoe_id,
        )
        .join(
            ShoeOutboundRecord,
            ShoeOutboundRecord.semifinished_shoe_storage_id
            == SemifinishedShoeStorage.semifinished_shoe_id,
        )
        .filter(
            OutsourceInfo.outsource_info_id == outsource_info_id,
        )
        .all()
    )
    result = []
    for row in response:
        outsource_info, shoe_storage, record = row
        obj = {
            "semifinishedObject": shoe_storage.semifinished_object,
            "semifinishedAmount": shoe_storage.semifinished_amount,
            "semifinishedStatus": shoe_storage.semifinished_status,
            "semifinishedEstimatedOutboundDate": outsource_info.semifinished_estimated_outbound_date,
            "outboundDatetime": record.outbound_datetime,
        }
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/getoutsourcematerialshipping", methods=["GET"]
)
def get_outsource_material_shipping():
    outsource_info_id = request.args.get("outsourceInfoId")
    # 发货数量：material_storage.current_amount
    query1 = (
        db.session.query(
            OutsourceInfo,
            MaterialStorage.material_outsource_status,
            MaterialStorage.current_amount,
            Material,
            MaterialType,
            OutboundRecord,
            Color,
        )
        .join(OrderShoe, OutsourceInfo.order_shoe_id == OrderShoe.order_shoe_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            MaterialStorage,
            MaterialStorage.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(
            Material,
            Material.material_id == MaterialStorage.material_id,
        )
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(
            OutboundRecord,
            OutboundRecord.material_storage_id == MaterialStorage.material_storage_id,
        )
        .join(Color, Color.color_id == MaterialStorage.material_storage_color)
        .filter(
            OutsourceInfo.outsource_info_id == outsource_info_id,
        )
    )
    query2 = (
        db.session.query(
            OutsourceInfo,
            SizeMaterialStorage.material_outsource_status,
            SizeMaterialStorage.total_current_amount.label("current_amount"),
            Material,
            MaterialType,
            OutboundRecord,
            Color,
        )
        .join(OrderShoe, OutsourceInfo.order_shoe_id == OrderShoe.order_shoe_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            SizeMaterialStorage,
            SizeMaterialStorage.order_shoe_type_id == OrderShoeType.order_shoe_type_id,
        )
        .join(
            Material,
            Material.material_id == SizeMaterialStorage.material_id,
        )
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(
            OutboundRecord,
            OutboundRecord.size_material_storage_id
            == SizeMaterialStorage.size_material_storage_id,
        )
        .join(Color, Color.color_id == SizeMaterialStorage.size_material_color)
        .filter(
            OutsourceInfo.outsource_info_id == outsource_info_id,
        )
    )
    response = query1.union(query2).all()
    result = []
    for row in response:
        (
            outsource_info,
            material_outsource_status,
            current_amount,
            material,
            material_type,
            record,
            color,
        ) = row
        obj = {
            "materialType": material_type.material_type_name,
            "materialName": material.material_name,
            "materialUnit": material.material_unit,
            "outsourceStatus": material_outsource_status,
            "outboundAmount": current_amount,
            "materialEstimateOutboundDate": outsource_info.material_estimated_outbound_date,
            "outboundDatetime": record.outbound_datetime,
            "colorName": color.color_name,
        }
        result.append(obj)
    return result


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
            func.sum(QuantityReportItem.amount).label("amount"),
        )
        .join(QuantityReport, QuantityReport.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            QuantityReportItem, QuantityReportItem.report_id == QuantityReport.report_id
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
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    amount_map = {}
    for row in response:
        order, order_shoe, shoe, team, amount = row
        if order_shoe.order_shoe_id not in amount_map:
            obj = {
                "orderRId": order.order_rid,
                "orderStartDate": order.start_date.strftime("%Y-%m-%d"),
                "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
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
    response = query.limit(page_size).offset((page - 1) * page_size).all()
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
            "creationDate": report.creation_date.strftime("%Y-%m-%d"),
            "submissionDate": report.submission_date.strftime("%Y-%m-%d"),
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
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
        db.session.query(QuantityReportItem, OrderShoeBatchInfo)
        .join(
            OrderShoeBatchInfo,
            QuantityReportItem.order_shoe_batch_info_id
            == OrderShoeBatchInfo.order_shoe_batch_info_id,
        )
        .filter(QuantityReportItem.report_id == data["reportId"])
        .all()
    )
    for row in response:
        report_item, batch_info = row
        if report_item.amount:
            if report.team == "裁断":
                batch_info.cutting_amount += report_item.amount
            elif report.team == "针车预备":
                batch_info.pre_sewing_amount += report_item.amount
            elif report.team == "针车":
                batch_info.sewing_amount += report_item.amount
            elif report.team == "成型":
                batch_info.molding_amount += report_item.amount
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
    response = query.limit(page_size).offset((page - 1) * page_size).all()
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
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
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
            "productionStartDate": start_date.strftime("%Y-%m-%d"),
            "productionEndDate": end_date.strftime("%Y-%m-%d"),
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
    report.status = 2
    report.rejection_reason = None
    if flag:
        # find order shoe current status
        current_status_str = (
            db.session.query(
                func.group_concat(OrderShoeStatus.current_status).label(
                    "current_status_str"
                ),
            )
            .filter_by(order_shoe_id=order_shoe_id)
            .group_by(OrderShoeStatus.order_shoe_id)
            .first()
        )
        current_status_arr = current_status_str[0].split(",")
        processor: EventProcessor = current_app.config["event_processor"]
        if "22" in current_status_arr:
            operation_arr = [82, 83]
        elif "29" in current_status_arr:
            operation_arr = [96, 97]
        elif "39" in current_status_arr:
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
