import constants
import time
from app_config import db
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from constants import IN_PRODUCTION_ORDER_NUMBER

from models import (
    Order,
    OrderShoe,
    OrderShoeStatus,
    OrderShoeStatusReference,
    OrderShoeBatchInfo,
    OrderStatus,
    OrderStatusReference,
    PurchaseOrder,
    Customer,
    Shoe,
    Color,
    Bom,
)
from sqlalchemy import or_, text
from datetime import datetime

order_bp = Blueprint("order_bp", __name__)


@order_bp.route("/ordershoe/getordershoebyorder", methods=["GET"])
def get_order_shoe_by_order():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(OrderShoe, Shoe)
        .filter(OrderShoe.order_id == order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .all()
    )
    print(entities)
    return


@order_bp.route("/order/getorderbystatus", methods=["GET"])
def get_orders_by_status():
    t_s = time.time()
    print("ORDERSHOESTATUS GET REQUEST WITH STATUS OF")
    status_val = request.args.get("ordershoestatus")
    print(status_val)
    entities = (
        db.session.query(
            Order,
            Customer,
            func.count(OrderShoe.order_shoe_id),
            OrderShoeStatus.current_status_value,
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(OrderShoeStatus.current_status == status_val)
        .group_by(Order.order_id, OrderShoeStatus.current_status_value)
        .all()
    )
    print(entities)
    pending_orders, in_progress_orders = [], []
    for entity in entities:
        order, customer, count, status_value = entity
        formatted_start_date = order.start_date.strftime("%Y-%m-%d")
        formatted_deadline_date = order.end_date.strftime("%Y-%m-%d")
        response_obj = {
            "orderId": order.order_id,
            "orderRid": order.order_rid,
            "customerName": customer.customer_name,
            "orderShoeCount": count,
            "statusValue": status_value,
            "createTime": formatted_start_date,
            "deadlineTime": formatted_deadline_date,
        }
        print("current entity has status value of")
        print(status_value)
        if status_value == 0:
            pending_orders.append(response_obj)
        elif status_value == 1:
            in_progress_orders.append(response_obj)

    result = {"pendingOrders": pending_orders, "inProgressOrders": in_progress_orders}
    t_e = time.time()
    print("Time Taken is ")
    print(t_e - t_s)
    return result


@order_bp.route("/order/getordersinproduction", methods=["GET"])
def get_orders_in_production():
    status_val = request.args.get("ordershoestatus")
    response = (
        db.session.query(
            Order,
            func.max(OrderShoeStatus.current_status_value).label("status_value"),
            Customer,
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(
            OrderShoeStatus.current_status >= status_val,
            OrderShoeStatus.current_status < 42,
        )
        .group_by(Order.order_id)
        .all()
    )

    new_orders, progress_orders = [], []
    for row in response:
        order, status_val, customer = row
        formatted_date = order.start_date.strftime("%Y-%m-%d")
        obj = {
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "createTime": formatted_date,
            "customerName": customer.customer_name,
        }
        if status_val == 0:
            new_orders.append(obj)
        elif status_val == 1:
            progress_orders.append(obj)
    result = {"newOrders": new_orders, "progressOrders": progress_orders}
    return result


@order_bp.route("/order/getorderInfo", methods=["GET"])
def get_order_info():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(Order, Customer, OrderStatus)
        .filter(Order.order_id == order_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .outerjoin(OrderStatus, OrderStatus.order_id == Order.order_id)
        .first()
    )
    print(entities)
    formatted_start_date = entities.Order.start_date.strftime("%Y-%m-%d")
    formatted_end_date = entities.Order.end_date.strftime("%Y-%m-%d")
    result = {
        "orderId": entities.Order.order_rid,
        "customerName": entities.Customer.customer_name,
        "createTime": formatted_start_date,
        "deadlineTime": formatted_end_date,
        "status": entities.OrderStatus.order_current_status if entities.OrderStatus else "N/A",
    }
    return jsonify(result)


@order_bp.route("/order/getordershoesizesinfo", methods=["GET"])
def get_order_shoe_sizes_info():
    order_id = request.args.get("orderid")
    order_shoe_id = request.args.get("ordershoeid")
    entities = (
        db.session.query(Order, OrderShoe, Shoe, OrderShoeBatchInfo, Color)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .outerjoin(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(Color, Color.color_id == OrderShoeBatchInfo.color_id)
        .filter(Order.order_rid == order_id)
        .filter(Shoe.shoe_rid == order_shoe_id)
        .all()
    )

    # Dictionary to accumulate total amounts by color
    color_totals = {}

    # First loop to accumulate total amounts for each color
    for entity in entities:
        order, order_shoe, shoe, order_shoe_batch_info, color = entity
        if color.color_name not in color_totals:
            color_totals[color.color_name] = 0
        color_totals[color.color_name] += order_shoe_batch_info.total_amount

    # Second loop to build the result list and include the color totals
    result = []
    for entity in entities:
        order, order_shoe, shoe, order_shoe_batch_info, color = entity
        result.append(
            {
                "size": order_shoe_batch_info.name,
                "35": order_shoe_batch_info.size_35_amount,
                "36": order_shoe_batch_info.size_36_amount,
                "37": order_shoe_batch_info.size_37_amount,
                "38": order_shoe_batch_info.size_38_amount,
                "39": order_shoe_batch_info.size_39_amount,
                "40": order_shoe_batch_info.size_40_amount,
                "41": order_shoe_batch_info.size_41_amount,
                "42": order_shoe_batch_info.size_42_amount,
                "43": order_shoe_batch_info.size_43_amount,
                "44": order_shoe_batch_info.size_44_amount,
                "45": order_shoe_batch_info.size_45_amount,
                "color": color.color_name,
                "pairAmount": order_shoe_batch_info.total_amount,
                "total": color_totals[
                    color.color_name
                ],  # Add total amount for the color
            }
        )

    return jsonify(result)


@order_bp.route("/order/getallorders", methods=["GET"])
def get_all_orders():
    entities = (
        db.session.query(Order, Customer, OrderStatus, OrderStatusReference)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .outerjoin(OrderStatus, OrderStatus.order_id == Order.order_id)
        .outerjoin(
            OrderStatusReference,
            OrderStatus.order_current_status == OrderStatusReference.order_status_id,
        )
        .all()
    )
    print(entities)
    result = []
    for entity in entities:
        order, customer, order_status, order_status_reference = entity
        formatted_start_date = order.start_date.strftime("%Y-%m-%d")
        formatted_end_date = order.end_date.strftime("%Y-%m-%d")
        result.append(
            {
                "orderRid": order.order_rid,
                "customerName": customer.customer_name,
                "orderStartDate": formatted_start_date,
                "orderEndDate": formatted_end_date,
                "orderStatus": (
                    order_status_reference.order_status_name
                    if order_status_reference
                    else "N/A"
                ),
            }
        )
    return jsonify(result)


@order_bp.route("/order/getallorderstatus", methods=["GET"])
def get_all_order_status():
    entities = db.session.query(OrderStatusReference).all()
    result = []
    for entity in entities:
        result.append(
            {"value": entity.order_status_id, "label": entity.order_status_name}
        )
    return jsonify(result)


@order_bp.route("/order/getordershoeinfo", methods=["GET"])
def get_order_shoe_info():
    order_id = request.args.get("orderrid")
    entities = (
        db.session.query(
            Order,
            OrderShoe,
            Shoe,
            OrderShoeBatchInfo,
            Color,
            func.group_concat(OrderShoeStatusReference.status_name).label(
                "combined_statuses"
            ),
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeStatusReference,
            OrderShoeStatus.current_status == OrderShoeStatusReference.status_id,
        )
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .join(
            OrderShoeBatchInfo,
            OrderShoeBatchInfo.order_shoe_id == OrderShoe.order_shoe_id,
        )
        .join(Color, OrderShoeBatchInfo.color_id == Color.color_id)
        .filter(Order.order_rid == order_id)
        .group_by(
            Order.order_id,
            OrderShoe.order_shoe_id,
            Shoe.shoe_id,
            OrderShoeBatchInfo.order_shoe_batch_info_id,
            Color.color_id,
        )  # Group by necessary fields
        .all()
    )
    print(entities)
    result = []
    for entity in entities:
        order, order_shoe, shoe, order_shoe_batch_info, color, combined_statuses = (
            entity
        )
        formatted_start_date = order.start_date.strftime("%Y-%m-%d")
        formatted_end_date = order.end_date.strftime("%Y-%m-%d")
        result.append(
            {
                "orderRid": order.order_rid,
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "colorCN": color.color_name,
                "colorEN": color.color_en_name,
                "sizeId": order_shoe_batch_info.name,
                "7/35": order_shoe_batch_info.size_35_amount,
                "7.5/36": order_shoe_batch_info.size_36_amount,
                "8/37": order_shoe_batch_info.size_37_amount,
                "8.5/38": order_shoe_batch_info.size_38_amount,
                "9/39": order_shoe_batch_info.size_39_amount,
                "9.5/40": order_shoe_batch_info.size_40_amount,
                "10/41": order_shoe_batch_info.size_41_amount,
                "10.5/42": order_shoe_batch_info.size_42_amount,
                "11/43": order_shoe_batch_info.size_43_amount,
                "12/44": order_shoe_batch_info.size_44_amount,
                "13/45": order_shoe_batch_info.size_45_amount,
                "pairCount": order_shoe_batch_info.total_amount,
                "status": combined_statuses,
            }
        )
    return jsonify(result)


@order_bp.route("/order/getorderdocinfo", methods=["GET"])
def get_order_doc_info():
    order_rid = request.args.get("orderrid")
    entity = db.session.query(Order).filter(Order.order_rid == order_rid).first()
    result = {
        "productionDoc": (
            "未上传" if entity.production_list_upload_status == "0" else "已上传"
        ),
        "amountDoc": "未上传" if entity.amount_list_upload_status == "0" else "已上传",
    }
    return jsonify(result)


@order_bp.route("/order/getorderfullinfo", methods=["GET"])
def get_order_full_info():
    page = request.args.get("page", 1, type=int)
    order_search = request.args.get("orderSearch", "", type=str)
    customer_search = request.args.get("customerSearch", "", type=str)

    # Set the pagination variables
    per_page = 10  # Define how many results per page
    offset = (page - 1) * per_page
    query = (
        db.session.query(
            Order,
            OrderStatus,
            OrderStatusReference,
            OrderShoe,
            OrderShoeStatus,
            OrderShoeStatusReference,
            Customer,
            Shoe,
            PurchaseOrder,
            Bom,
        )
        .outerjoin(OrderStatus, Order.order_id == OrderStatus.order_id)
        .outerjoin(OrderStatusReference, OrderStatus.order_current_status == OrderStatusReference.order_status_id)
        .outerjoin(OrderShoe, OrderShoe.order_id == Order.order_id)
        .outerjoin(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .outerjoin(
            OrderShoeStatusReference,
            OrderShoeStatus.current_status == OrderShoeStatusReference.status_id,
        )
        .outerjoin(Customer, Order.customer_id == Customer.customer_id)
        .outerjoin(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .outerjoin(Bom, Bom.order_shoe_id == OrderShoe.order_shoe_id)
        .outerjoin(PurchaseOrder, PurchaseOrder.bom_id == Bom.bom_id)
        .filter(
            or_(
                Order.order_rid.like(f"%{order_search}%"),
                Customer.customer_name.like(f"%{customer_search}%"),
            )
        )
        .order_by(Order.order_id.desc())
        .all()
    )

    # Initialize a dictionary to group orders
    orders_dict = {}

    # Loop through the query result
    for (
        order,
        order_status,
        order_status_reference,
        order_shoe,
        order_shoe_status,
        order_shoe_status_reference,
        customer,
        shoe,
        purchase_order,
        bom,
    ) in query:
        formatted_start_date = order.start_date.strftime("%Y-%m-%d") if order.start_date else "N/A"
        formatted_end_date = order.end_date.strftime("%Y-%m-%d") if order.end_date else "N/A"
        
        # If the order isn't already in the dictionary, add it
        if order.order_id not in orders_dict:
            orders_dict[order.order_id] = {
                "orderId": order.order_id if order.order_id else "N/A",
                "orderRid": order.order_rid if order.order_rid else "N/A",
                "customerName": customer.customer_name if customer else "N/A",
                "createTime": formatted_start_date,
                "deadlineTime": formatted_end_date,
                "status": order_status_reference.order_status_name if order_status_reference else "N/A",
                "shoes": {}  # Using a dictionary to avoid duplicate shoes
            }

        # Use a unique key for each shoe to avoid duplicates
        shoe_key = order_shoe.order_shoe_id if order_shoe else "N/A"

        if shoe_key not in orders_dict[order.order_id]["shoes"]:
            # Prepare shoe information for the first occurrence
            orders_dict[order.order_id]["shoes"][shoe_key] = {
                "shoeRid": shoe.shoe_rid if shoe else "N/A",
                'customerId': order_shoe.customer_product_name if order_shoe else "N/A",
                "firstBom": "N/A",
                "secondBom": "N/A",
                "firstOrder": "N/A",
                "secondOrder": "N/A",
                "statuses": ""  # To hold the combined statuses as a string
            }

        # Add the status for the current OrderShoe, checking for duplicates
        if order_shoe_status_reference:
            status_string = f"{order_shoe_status_reference.status_name}"
            
            # Ensure the status is only added once
            if status_string not in orders_dict[order.order_id]["shoes"][shoe_key]["statuses"]:
                if orders_dict[order.order_id]["shoes"][shoe_key]["statuses"]:
                    orders_dict[order.order_id]["shoes"][shoe_key]["statuses"] += " | " + status_string
                else:
                    orders_dict[order.order_id]["shoes"][shoe_key]["statuses"] = status_string

        # Assign BOM based on bom_type
        if bom:
            if bom.bom_type == 0:
                orders_dict[order.order_id]["shoes"][shoe_key]["firstBom"] = bom.bom_rid
            elif bom.bom_type == 1:
                orders_dict[order.order_id]["shoes"][shoe_key]["secondBom"] = bom.bom_rid

        # Assign purchase orders based on purchase_order_type
        if purchase_order:
            if purchase_order.purchase_order_type == "F":
                orders_dict[order.order_id]["shoes"][shoe_key]["firstOrder"] = purchase_order.purchase_order_rid
            elif purchase_order.purchase_order_type == "S":
                orders_dict[order.order_id]["shoes"][shoe_key]["secondOrder"] = purchase_order.purchase_order_rid

    # Convert the shoes from dictionary to list and create the final result list
    result = []
    for order_id, order_data in orders_dict.items():
        order_data["shoes"] = list(order_data["shoes"].values())  # Convert shoe dict to list
        result.append(order_data)

    # Apply pagination to the result
    result = result[offset : offset + per_page]

    return jsonify(result)



