from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert

from app_config import app, db
from models import *

logistics_home_page_bp = Blueprint("logistics_home_page_bp", __name__)


@logistics_home_page_bp.route("/logistics/task", methods=["GET"])
def get_task():
    tastStatus = request.args.get("taskstatus")
    shoeStatus = request.args.get("shoestatus")
    taskName = ""
    
    query = (
        db.session.query(Order, OrderShoe, OrderShoeStatus, OrderShoeStatusReference)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(OrderShoeStatus, OrderShoe.order_shoe_id == OrderShoeStatus.order_shoe_id)
        .join(
            OrderShoeStatusReference,
            OrderShoeStatus.current_status == OrderShoeStatusReference.status_id,
        )
        .filter(OrderShoeStatus.current_status_value == tastStatus)
    )

    if shoeStatus != "all":
        query = query.filter(OrderShoeStatus.current_status == int(shoeStatus))
    else:
        # If "all", we need to check for statuses 6 or 13
        query = query.filter(OrderShoeStatus.current_status.in_([6, 13]))

    response = query.distinct(Order.order_id).all()

    unique_orders = {}
    
    for row in response:
        order_id = row.Order.order_id
        
        # Determine taskName based on current_status if not already set for this order
        if order_id not in unique_orders:
            if row.OrderShoeStatus.current_status == 6:
                taskName = "一次采购订单生成"
            elif row.OrderShoeStatus.current_status == 13:
                taskName = "二次采购订单生成"
            else:
                taskName = ""  # Default or any other logic
            
            unique_orders[order_id] = {
                "taskName": taskName,
                "orderId": row.Order.order_rid,
                "createTime": row.Order.start_date.isoformat(),
            }
    
    result = list(unique_orders.values())
    
    print(result)

    return jsonify(result)


