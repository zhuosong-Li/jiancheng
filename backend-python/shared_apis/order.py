import constants
from app_config import db
from flask import Blueprint, jsonify, request

from models import (
    Order,
    OrderShoe,
    OrderShoeStatus,
    OrderShoeStatusReference,
    OrderStatus,
    Customer
)
from sqlalchemy import or_, text
from datetime import datetime

order_bp = Blueprint("order_bp", __name__)


@order_bp.route("/order/getcurrentorders", methods=["GET"])
def get_active_orders():
    order_status_val = request.args.get("orderstatus")
    order_shoe_status_val = request.args.get("ordershoestatus")
    response = (
        db.session.query(
            Order, OrderStatus, OrderShoe, OrderShoeStatus, OrderShoeStatusReference, Customer
        )
        .join(OrderStatus, Order.order_id == OrderStatus.order_id)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(
            OrderShoeStatusReference,
            OrderShoeStatus.current_status == OrderShoeStatusReference.status_id,
        ).join(Customer, Order.customer_id == Customer.customer_id)
        .filter(
            OrderStatus.order_current_status == order_status_val, OrderShoeStatus.current_status == order_shoe_status_val
        )
        .all()
    )

    new_orders, progress_orders = [], []
    for row in response:
        print(row)
        order, _, _, order_shoe_status, order_shoe_status_reference, customer = row
        formatted_date = order.creation_time.strftime("%Y-%m-%d")
        obj = {
            "statusId": order_shoe_status_reference.status_id,
            "taskName": order_shoe_status_reference.status_name,
            "orderId": order.order_id,
            "orderRId": order.order_rid,
            "createTime": formatted_date,
            "customerName": customer.customer_name
        }
        if order_shoe_status.current_status_value == 0:
            new_orders.append(obj)
        elif order_shoe_status.current_status_value == 1:
            progress_orders.append(obj)
    result = {
        "newOrders": new_orders,
        "progressOrders": progress_orders
    }
    return result
