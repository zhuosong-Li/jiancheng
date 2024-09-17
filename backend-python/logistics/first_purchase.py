from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert
import datetime
from app_config import app, db
from models import *
from api_utility import randomIdGenerater
from event_processor import EventProcessor
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH

first_purchase_bp = Blueprint("first_purrchase_bp", __name__)

@first_purchase_bp.route("/firstpurchase/getnewpurchaseorderid", methods=["GET"])
def get_new_purchase_order_id():
    department_id = "01"
    current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    purchase_order_id = department_id + current_time_stamp + random_string + 'F'
    return jsonify({"purchaseOrderId": purchase_order_id})


@first_purchase_bp.route("/firstpurchase/getallboms", methods=["GET"])
def get_all_boms():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(Order, OrderShoe, Shoe, Bom)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .outerjoin(Bom, Bom.order_shoe_id == OrderShoe.order_shoe_id)
        .filter(Order.order_id == order_id)
        .all()
    )
    result = []
    for entity in entities:
        order, order_shoe, shoe, bom = entity
        if bom:
            purchase_order = (
                db.session.query(PurchaseOrder)
                .filter(PurchaseOrder.bom_id == bom.bom_id)
                .first()
            )
            if purchase_order:
                status = purchase_order.status
            else:
                status = "0"
            if status == "0":
                status = "一次采购订单未填写"
            elif status == "1":
                status = "一次采购订单已保存"
            elif status == "2":
                status = "一次采购订单已下发"
            result.append(
                {
                    "orderId": order.order_rid,
                    "orderShoeId": order_shoe.order_shoe_id,
                    "inheritId": shoe.shoe_rid,
                    "customerId": order_shoe.customer_product_name,
                    "designer": shoe.shoe_designer,
                    "editter": shoe.shoe_adjuster,
                    "bomId": bom.bom_rid if bom else "",
                    "purchaseOrderId": purchase_order.purchase_order_rid if purchase_order else "",
                    "status": status,
                    "image" : IMAGE_STORAGE_PATH+shoe.shoe_image_url if shoe.shoe_image_url is not None else None,
                }
            )
        else:
            result.append(
                {
                    "orderId": order.order_rid,
                    "orderShoeId": order_shoe.order_shoe_id,
                    "inheritId": shoe.shoe_rid,
                    "customerId": order_shoe.customer_product_name,
                    "designer": shoe.shoe_designer,
                    "editter": shoe.shoe_adjuster,
                    "bomId": "",
                    "purchaseOrderId": "",
                    "status": "无BOM",
                    "image" : IMAGE_STORAGE_PATH+shoe.shoe_image_url if shoe.shoe_image_url is not None else None,
                }
            )
    return jsonify(result)