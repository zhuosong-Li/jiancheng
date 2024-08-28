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
    OrderStatus,
    Customer,
    Shoe
)
from sqlalchemy import or_, text
from datetime import datetime

order_bp = Blueprint("order_bp", __name__)


@order_bp.route("/ordershoe/getordershoebyorder", methods = ["GET"])
def get_order_shoe_by_order():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(
            OrderShoe, Shoe
        )
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
            Order, Customer,func.count(OrderShoe.order_shoe_id), OrderShoeStatus.current_status_value
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(
            OrderShoeStatus.current_status == status_val
        )
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
            'orderId': order.order_id,
            'orderRid': order.order_rid,
            'customerName':customer.customer_name,
            'orderShoeCount': count,
            'statusValue':status_value,
            'createTime':formatted_start_date,
            'deadlineTime':formatted_deadline_date
        }
        print("current entity has status value of")
        print(status_value)
        if status_value == 0:
            pending_orders.append(response_obj)
        elif status_value == 1:
            in_progress_orders.append(response_obj)

    result = {
        'pendingOrders':pending_orders,
        'inProgressOrders':in_progress_orders
    }
    t_e = time.time()
    print("Time Taken is ")
    print(t_e - t_s)
    return result
@order_bp.route("/order/getordersinproduction", methods=["GET"])
def get_orders_in_production():
    status_val = request.args.get("ordershoestatus")
    response = (
        db.session.query(
            Order, func.max(OrderShoeStatus.current_status_value).label('status_value'), Customer
        )
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(OrderShoeStatus, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(
            OrderShoeStatus.current_status >= status_val,
            OrderShoeStatus.current_status < 42
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
