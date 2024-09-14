import traceback
from datetime import datetime, timedelta

from app_config import db
from constants import *
from event_processor import EventProcessor
from flask import Blueprint, jsonify, request, current_app
from models import *
from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert

production_manager_bp = Blueprint("production_manager_bp", __name__)


@production_manager_bp.route(
    "/production/productionmanager/getinprogressorders", methods=["GET"]
)
def get_in_progress_orders():
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
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
        .join(
            OrderShoeBatchInfo,
            OrderShoe.order_shoe_id == OrderShoeBatchInfo.order_shoe_id,
        )
        .join(OrderStatus, OrderStatus.order_id == Order.order_id)
        .group_by(Order.order_id)
        .filter(OrderStatus.order_current_status == 9)
    )
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
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
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "customerName": customer.customer_name,
            "startDate": cutting_start_date.strftime("%Y-%m-%d"),
            "endDate": molding_end_date.strftime("%Y-%m-%d"),
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
    result = {
        "cuttingLineNumbers": response.cutting_line_group,
        "preSewingLineNumbers": response.pre_sewing_line_group,
        "sewingLineNumbers": response.sewing_line_group,
        "moldingLineNumbers": response.molding_line_group,
        "cuttingStartDate": response.cutting_start_date,
        "cuttingEndDate": response.cutting_end_date,
        "preSewingStartDate": response.pre_sewing_start_date,
        "preSewingEndDate": response.pre_sewing_end_date,
        "sewingStartDate": response.sewing_start_date,
        "sewingEndDate": response.sewing_end_date,
        "moldingStartDate": response.molding_start_date,
        "moldingEndDate": response.molding_end_date,
        "isCuttingOutsourced": response.is_cutting_outsourced,
        "isSewingOutsourced": response.is_sewing_outsourced,
        "isMoldingOutsourced": response.is_molding_outsourced,
    }
    return result


@production_manager_bp.route(
    "/production/productionmanager/getproductioninfo", methods=["GET"]
)
def get_production_info():
    # 参考scheduleView.vue 441行
    team = request.args.get("team")
    # 成型号
    number = request.args.get("number")
    if team == "cutting":
        status = 23
        line_usage = OrderShoeProductionInfo.cutting_line_group
        start_date = OrderShoeProductionInfo.cutting_start_date
        end_date = OrderShoeProductionInfo.cutting_end_date
    elif team == "preSewing":
        status = 29
        line_usage = OrderShoeProductionInfo.pre_sewing_line_group
        start_date = OrderShoeProductionInfo.pre_sewing_start_date
        end_date = OrderShoeProductionInfo.pre_sewing_end_date
    elif team == "sewing":
        status = 31
        line_usage = OrderShoeProductionInfo.sewing_line_group
        start_date = OrderShoeProductionInfo.sewing_start_date
        end_date = OrderShoeProductionInfo.sewing_end_date
    elif team == "molding":
        status = 39
        line_usage = OrderShoeProductionInfo.molding_line_group
        start_date = OrderShoeProductionInfo.molding_start_date
        end_date = OrderShoeProductionInfo.molding_end_date
    else:
        return {"message": "failed"}, 400
    response = (
        db.session.query(
            Order,
            Shoe,
            func.sum(OrderShoeBatchInfo.total_amount),
            line_usage,
            start_date,
            end_date,
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .filter(OrderShoeStatus.current_status == status)
        .group_by(Order.order_id, OrderShoe.order_shoe_id)
        .all()
    )

    result = []
    for row in response:
        (
            order,
            shoe,
            total_amount,
            line_usage_info,
            start_date_val,
            end_date_val,
        ) = row
        val = len(line_usage_info.split(","))
        obj = {
            "startDate": start_date_val,
            "endDate": end_date_val,
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "shoeRId": shoe.shoe_rid,
            "number": total_amount,
            "lineUsage": val,
        }
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/editproductionschedule", methods=["PATCH"]
)
def edit_production_schedule():
    data = request.get_json()
    entity = OrderShoeProductionInfo.query.filter(
        OrderShoeProductionInfo.order_shoe_id == data["orderShoeId"]
    ).first()
    entity.cutting_line_numbers = data["cuttingInfo"]["line_numbers"]
    entity.is_cutting_outsourced = data["cuttingInfo"]["isOutsourced"]
    entity.start_date = data["cuttingInfo"]["startDate"]
    entity.end_date = data["cuttingInfo"]["endDate"]

    entity.cutting_line_numbers = data["sewingInfo"]["line_numbers"]
    entity.is_cutting_outsourced = data["sewingInfo"]["isOutsourced"]
    entity.start_date = data["sewingInfo"]["startDate"]
    entity.end_date = data["sewingInfo"]["endDate"]

    entity.cutting_line_numbers = data["moldingInfo"]["line_numbers"]
    entity.is_cutting_outsourced = data["moldingInfo"]["isOutsourced"]
    entity.start_date = data["moldingInfo"]["startDate"]
    entity.end_date = data["moldingInfo"]["endDate"]
    db.session.commit()
    return jsonify({"message": "success"})


# TODO
@production_manager_bp.route(
    "/production/productionmanager/submitproductionschedule", methods=["PATCH"]
)
def submit_production_schedule():
    # pass to event processor
    return "hello world"


@production_manager_bp.route(
    "/production/productionmanager/getorderproductiondetail", methods=["GET"]
)
def get_order_production_detail():
    order_id = request.args.get("orderId")
    response = (
        db.session.query(OrderShoe, Shoe)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(OrderShoe.order_id == order_id)
        .all()
    )
    result = []
    order_shoe_list = []
    for row in response:
        order_shoe, shoe = row
        order_shoe_list.append(order_shoe.order_shoe_id)
        obj = {
            "orderShoeId": order_shoe.order_shoe_id,
            "imgUrl": shoe.shoe_image_url,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "totalShoes": 0,
            "detail": [],
        }
        # 加鞋型详情，只返回进度
        response = (
            db.session.query(OrderShoeBatchInfo, Color)
            .join(Color, Color.color_id == OrderShoeBatchInfo.color_id)
            .filter(OrderShoeBatchInfo.order_shoe_id == order_shoe.order_shoe_id)
            .all()
        )
        for row in response:
            batch_info, color = row
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
                }
            )
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/getordershoebatchinfo", methods=["GET"]
)
def get_order_shoe_batch_info():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        db.session.query(OrderShoeBatchInfo, Color)
        .join(Color, OrderShoeBatchInfo.color_id == Color.color_id)
        .filter(OrderShoeBatchInfo.order_shoe_id == order_shoe_id)
    ).all()
    result = []
    for row in response:
        batch_info, color = row
        obj = {
            "colorName": color.color_name,
            "batchName": batch_info.name,
            "totalAmount": batch_info.total_amount,
        }
        for info in SHOESIZEINFO:
            key = f"size{info['shoe_size']}"
            value = getattr(batch_info, f"size_{info['shoe_size']}_amount")
            if not value:
                value = 0
            obj[key] = value
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
        .join(Shoe, Shoe.shoe_id == OrderShoe.order_shoe_id)
        .filter(OrderStatus.order_current_status == IN_PRODUCTION_ORDER_NUMBER)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"{shoe_rid}%"))
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
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
    status_point = request.args.get("statusPoint")
    query = (
        db.session.query(Order, OrderShoe, Shoe, OrderShoeStatusReference)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(
            OrderShoeStatusReference,
            OrderShoeStatusReference.status_id == OrderShoeStatus.current_status,
        )
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"{shoe_rid}%"))
    if status_point and ORDER_SHOE_STATUS_REFERENCE[status_point]:
        query = query.filter(
            OrderShoeStatus.current_status == ORDER_SHOE_STATUS_REFERENCE[status_point]
        )
    else:
        query = query.filter(
            OrderShoeStatus.current_status.in_([18, 24, 31, 33, 41, 42])
        )
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, shoe, reference = row
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "statusPoint": reference.status_name,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


# @production_manager_bp.route(
#     "/production/productionmanager/getordershoebatchinfo", methods=["GET"]
# )
# def get_order_shoe_batch_info():
#     order_shoe_id = request.args.get("orderShoeId")
#     node_name = request.args.get("nodeName")
#     response = (
#         db.session.query(Color, OrderShoeBatchInfo)
#         .join(OrderShoe, OrderShoe.order_shoe_id == OrderShoeBatchInfo.order_shoe_id)
#         .join(Color, Color.color_id == OrderShoeBatchInfo.color_id)
#         .filter(OrderShoe.order_shoe_id == order_shoe_id)
#         .all()
#     )
#     result = []
#     for row in response:
#         color, batch_info = row
#         amount = 0
#         # 分状态
#         if node_name == "裁断完成":
#             amount = batch_info.cutting_amount
#         elif node_name == "针车预备完成":
#             amount = batch_info.pre_sewing_amount
#         elif node_name == "针车完成":
#             amount = batch_info.sewing_amount
#         elif node_name == "成型完成" or node_name == "生产完成":
#             amount = batch_info.molding_amount
#         obj = {
#             "color": color.color_name,
#             "batchInfoName": batch_info.name,
#             "totalAmount": batch_info.total_amount,
#             "finishedAmount": amount,
#         }
#         result.append(obj)
#     return result


# TODO
@production_manager_bp.route(
    "/production/productionmanager/checkdateproductionstatus", methods=["GET"]
)
def check_date_production_status():
    start_date_str = request.args.get("startDate")
    end_date_str = request.args.get("endDate")
    # Convert the date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    response = (
        db.session.query(Order, OrderShoe, OrderShoeProductionInfo)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(
            OrderShoeProductionInfo,
            OrderShoeProductionInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .filter(
            OrderShoeProductionInfo.cutting_start_date >= start_date,
            OrderShoeProductionInfo.molding_end_date <= end_date,
        )
        .all()
    )
    result = []

    # Define the step size (1 day)
    delta = timedelta(days=1)

    # Loop through the date range
    current_date = start_date
    while current_date <= end_date:
        result.append({"date": current_date.strftime("%Y-%m-%d")})
        current_date += delta

    return result


@production_manager_bp.route(
    "/production/productionmanager/editordershoestatus", methods=["PATCH"]
)
def edit_order_shoe_status():
    data = request.get_json()
    status_name = data["statusName"]
    report = None
    if status_name == "生产开始":
        report = UnitPriceReport(
            order_shoe_id=data["orderShoeId"], team="裁断", status=0
        )
    elif status_name == "裁断结束":
        report = UnitPriceReport(
            order_shoe_id=data["orderShoeId"], team="针车", status=0
        )
    elif status_name == "针车结束":
        report = UnitPriceReport(
            order_shoe_id=data["orderShoeId"], team="成型", status=0
        )
    if report:
        db.session.add(report)
    try:
        processor: EventProcessor = current_app.config["event_processor"]
        next_operations = {
            "生产开始": [74, 75],
            "裁断结束": [84, 85],
            "针车预备结束": [98, 99],
            "针车结束": [102, 103],
            "成型结束": [118, 119],
            "生产结束": [19],
        }
        for op in next_operations[status_name]:
            event = Event(
                staff_id=1,
                handle_time=datetime.now(),
                operation_id=op,
                event_order_id=data["orderId"],
                event_order_shoe_id=data["orderShoeId"],
            )
            processor.processEvent(event)
    except Exception as e:
        print(e)
        return jsonify({"message": "failed"}), 400
    db.session.commit()
    return jsonify({"message": "succeed"})


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
        query = query.filter(Order.order_rid.ilike(f"{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"{shoe_rid}%"))
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
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
            "ShoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "isCuttingOutsourced": is_cutting_outsourced,
            "isSewingOutsourced": is_sewing_outsourced,
            "isMoldingOutsourced": is_molding_outsourced,
        }
        result.append(obj)
    return {"result": result, "totalLength": count_result}


@production_manager_bp.route(
    "/production/productionmanager/getordershoebatchinfoforoutsource", methods=["GET"]
)
def get_order_shoe_batch_info_for_outsource():
    order_shoe_id = request.args.get("orderShoeId")
    response = (
        db.session.query(OrderShoeBatchInfo, Color)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(Color, Color.color_id == OrderShoeBatchInfo.color_id)
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
    )
    result = []
    for row in response:
        batch_info, color = row
        obj = {
            "color": color.color_name,
            "batch_name": batch_info.name,
            "size34Amount": batch_info.size_34_amount,
            "size35Amount": batch_info.size_35_amount,
            "size36Amount": batch_info.size_36_amount,
            "size37Amount": batch_info.size_37_amount,
            "size38Amount": batch_info.size_38_amount,
            "size39Amount": batch_info.size_39_amount,
            "size40Amount": batch_info.size_40_amount,
            "size41Amount": batch_info.size_41_amount,
            "size42Amount": batch_info.size_42_amount,
            "size43Amount": batch_info.size_43_amount,
            "size44Amount": batch_info.size_44_amount,
            "size45Amount": batch_info.size_45_amount,
            "size46Amount": batch_info.size_46_amount,
        }
        result.append(obj)
    return result


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
        obj = {
            "outsourceInfoId": outsource_info.outsource_info_id,
            "outsourceType": outsource_info.outsource_type,
            "outsourceFactory": factory.factory_name,
            "outsourceAmount": outsource_info.outsource_amount,
            "outsourceStartDate": outsource_info.outsource_start_date.strftime(
                "%Y-%m-%d"
            ),
            "outsourceEndDate": outsource_info.outsource_end_date.strftime("%Y-%m-%d"),
            "approvalStatus": outsource_info.approval_status,
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
    "/production/productionmanager/storeoutsourceforordershoe", methods=["PUT"]
)
def store_outsource_for_order_shoe():
    data = request.get_json()
    departments = ""
    for line in data["type"]:
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
        "factory_id": data["factoryId"],
        "outsource_start_date": data["outsourceStartDate"],
        "outsource_end_date": data["outsourceEndDate"],
        "semifinished_required": data["semifinishedRequired"],
        "deadline_date": data["deadlineDate"],
        "material_estimated_outbound_date": data["materialEstimatedOutboundDate"],
        "outsource_amount": data["outsourceAmount"],
        "approval_status": False,
        "order_shoe_id": data["orderShoeId"],
    }
    if data["semifinishedRequired"]:
        obj["semifinished_estimated_outboundDate"] = data[
            "semifinishedEstimatedOutboundDate"
        ]
    stmt = insert(OutsourceInfo).values(**obj)
    stmt = stmt.on_duplicate_key_update(
        outsource_type=departments,
        factory_id=data["factoryId"],
        outsource_start_date=data["outsourceStartDate"],
        outsource_end_date=data["outsourceEndDate"],
        semifinished_required=data["semifinishedRequired"],
        semifinished_estimated_outbound_date=data["semifinishedEstimatedOutboundDate"],
        deadline_date=data["deadlineDate"],
        material_estimated_outbound_date=data["materialEstimatedOutboundDate"],
    )
    # set production info
    production_obj = OrderShoeProductionInfo.query.filter_by(
        order_shoe_id=data["orderShoeId"]
    ).first()
    for line in data["type"]:
        if line == "裁断":
            production_obj.is_cutting_outsourced = True
        elif line == "针车":
            production_obj.is_sewing_outsourced = True
        elif line == "成型":
            production_obj.is_molding_outsourced = True

    db.session.execute(stmt)
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/submitoutsourceinfo", methods=["PATCH"]
)
# TODO
def submit_outsource_info():
    data = request.get_json()
    # create event, pass to event processor

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
        .join(
            MaterialStorage,
            MaterialStorage.order_shoe_id == OutsourceInfo.order_shoe_id,
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
        .join(
            SizeMaterialStorage,
            SizeMaterialStorage.order_shoe_id == OutsourceInfo.order_shoe_id,
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
    query = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            QuantityReport.team,
            func.sum(QuantityReportItem.amount),
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(QuantityReport, QuantityReport.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            QuantityReportItem, QuantityReportItem.report_id == QuantityReport.report_id
        )
        .filter(
            OrderShoeStatus.current_status.in_([23, 29, 31, 39]),
        )
        .group_by(Order.order_id, OrderShoe.order_shoe_id, QuantityReport.team)
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"{shoe_rid}%"))
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, shoe, team, amount = row
        amounts = {"cutting_amount": 0, "sewing_amount": 0, "molding_amount": 0}
        if team == "裁断":
            amounts["cutting_amount"] = amount
        elif team == "针车":
            amounts["sewing_amount"] = amount
        elif team == "成型":
            amounts["molding_amount"] = amount
        obj = {
            "orderRId": order.order_rid,
            "orderStartDate": order.start_date.strftime("%Y-%m-%d"),
            "orderEndDate": order.end_date.strftime("%Y-%m-%d"),
            "orderShoeId": order_shoe.order_shoe_id,
            "shoeRId": shoe.shoe_rid,
            "customerProductName": order_shoe.customer_product_name,
            "yesterdayCuttingAmount": amounts["cutting_amount"],
            "yesterdaySewingAmount": amounts["sewing_amount"],
            "yesterdayMoldingAmount": amounts["molding_amount"],
        }
        result.append(obj)
    print(result)
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
        .filter(QuantityReport.status.in_([1, 2]))
    )
    if search_start_date and search_end_date:
        try:
            datetime.strptime(search_start_date, "%Y-%m-%d")
            datetime.strptime(search_end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "invalid date range"}), 400
        query = query.filter(
            QuantityReport.submission_date >= search_start_date,
            QuantityReport.submission_date <= search_end_date,
        )
    if team and team in ["裁断", '针车预备', '针车', '成型']:
        query = query.filter(QuantityReport.team == team)
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
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
        else:
            report_status = '已审批'
        obj = {
            "reportId": report.report_id,
            "reportDate": report.submission_date.strftime("%Y-%m-%d"),
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "team": report.team,
            "reportStatus": report_status
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
    db.session.commit()
    return jsonify({"message": "success"})


@production_manager_bp.route(
    "/production/productionmanager/rejectquantityreport", methods=["PATCH"]
)
def reject_quantity_report():
    data = request.get_json()
    report = db.session.query(QuantityReport).get(data["reportId"])
    report.status = 0
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
        )
    )
    if order_rid and order_rid != "":
        query = query.filter(Order.order_rid.ilike(f"{order_rid}%"))
    if shoe_rid and shoe_rid != "":
        query = query.filter(Shoe.shoe_rid.ilike(f"{shoe_rid}%"))
    if team and team != '':
        if team == "裁断":
            query = query.filter(OrderShoeStatus.current_status == 22)
        elif team == "针车":
            query = query.filter(OrderShoeStatus.current_status == 29)
        elif team == "成型":
            query = query.filter(OrderShoeStatus.current_status == 39)
        else:
            return jsonify({"message": "invalid team name"}), 400
    count_result = db.session.query(func.count()).select_from(query.subquery()).scalar()
    response = query.limit(page_size).offset((page - 1) * page_size).all()
    result = []
    for row in response:
        order, order_shoe, customer, shoe, status_obj = row
        if status_obj.current_status == 20:
            team = "裁断"
        elif status_obj.current_status == 27:
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
    return {'result': result, 'totalLength': count_result}


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
            UnitPriceReport.status.in_([1, 2])
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
        else:
            status = "已审批"
        obj = {
            "productionStartDate": start_date.strftime("%Y-%m-%d"),
            "productionEndDate": end_date.strftime("%Y-%m-%d"),
            "reportId": report.report_id,
            "reportStatus": status,
            "team": report.team
        }
        result.append(obj)
    return result


@production_manager_bp.route(
    "/production/productionmanager/approvepricereport", methods=["PATCH"]
)
def approve_price_report():
    data = request.get_json()
    report_id = data["reportId"]
    processor: EventProcessor = current_app.config["event_processor"]
    report = db.session.query(UnitPriceReport).get(report_id)
    print(data)
    report.status = 2
    try:
        for operation in [116, 117]:
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
# TODO
def reject_price_report():
    data = request.get_json()
    report_id_arr = data["reportIdArr"]
    for report_id in report_id_arr:
        report = db.session.query(UnitPriceReport).get(report_id)
        report.status = 0
        report.rejection_reason = data["rejectionReason"]
    db.session.commit()
    return jsonify({"message": "success"})
