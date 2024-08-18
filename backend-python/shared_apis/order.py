import constants
from app_config import db
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from constants import IN_PRODUCTION_ORDER_NUMBER

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


@order_bp.route("/order/getordersinproduction", methods=["GET"])
def get_orders_in_production():
    status_vals = request.args.get("ordershoestatus")
    status_arr = [int(number) for number in status_vals.split(",")]
    response = (
        db.session.query(
            Order, func.max(OrderShoeStatus.current_status_value).label('status_value'), Customer
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(
            OrderShoeStatus.current_status.in_(status_arr)
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
            "customerName": customer.customer_name
        }
        if status_val == 0:
            new_orders.append(obj)
        elif status_val == 1:
            progress_orders.append(obj)
    result = {
        "newOrders": new_orders,
        "progressOrders": progress_orders
    }
    return result
