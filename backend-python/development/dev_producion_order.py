from flask import Blueprint, jsonify, request, send_file
import os
import datetime
from app_config import app, db
from models import *
from event_processor import EventProcessor
from constants import FILE_STORAGE_PATH, IMAGE_STORAGE_PATH

dev_producion_order_bp = Blueprint("dev_producion_order_bp", __name__)


@dev_producion_order_bp.route("/devproductionorder/getordershoelist", methods=["GET"])
def get_order_list():
    order_id = request.args.get("orderid")
    order_shoes = (
        db.session.query(OrderShoe, Shoe)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(OrderShoe.order_id == order_id)
        .all()
    )
    result = []
    for order_shoe, shoe in order_shoes:
        if order_shoe.production_order_upload_status == "0":
            status = "未上传"
        elif order_shoe.production_order_upload_status == "1":
            status = "已上传"
        elif order_shoe.production_order_upload_status == "2":
            status = "已下发"
        result.append(
            {
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "image": (
                    IMAGE_STORAGE_PATH + shoe.shoe_image_url
                    if shoe.shoe_image_url is not None
                    else None
                ),
                "designer": shoe.shoe_designer,
                "editter": shoe.shoe_adjuster,
                "status": status,
            }
        )
    return jsonify(result)


@dev_producion_order_bp.route("/devproductionorder/upload", methods=["POST"])
def upload_production_order():
    order_shoe_rid = request.form.get("orderShoeRId")
    order_id = request.form.get("orderId")
    print(order_shoe_rid, order_id)
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 500
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 500
    folder_path = os.path.join(FILE_STORAGE_PATH, order_id, order_shoe_rid)
    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)
    file_path = os.path.join(folder_path, "投产指令单.xlsx")
    file.save(file_path)
    order_shoe = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    order_shoe.OrderShoe.production_order_upload_status = "1"
    db.session.commit()

    return jsonify({"message": "Production order uploaded successfully"})


@dev_producion_order_bp.route("/devproductionorder/download", methods=["GET"])
def download_production_order():
    order_shoe_rid = request.args.get("ordershoerid")
    order_id = request.args.get("orderid")
    order_shoe = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    if order_shoe.OrderShoe.production_order_upload_status == "0":
        return jsonify({"error": "Production order not uploaded yet"}), 500
    folder_path = os.path.join(FILE_STORAGE_PATH, order_id, order_shoe_rid)
    file_path = os.path.join(folder_path, "投产指令单.xlsx")
    new_name = order_id + "-" + order_shoe_rid + "_投产指令单.xlsx"
    return send_file(file_path, as_attachment=True, download_name=new_name)


@dev_producion_order_bp.route("/devproductionorder/issue", methods=["POST"])
def issue_production_order():
    order_shoe_rids = request.json.get("orderShoeIds")
    order_rid = request.json.get("orderId")
    for order_shoe_rid in order_shoe_rids:
        order_shoe = (
            db.session.query(Order, OrderShoe, Shoe)
            .join(OrderShoe, Order.order_id == OrderShoe.order_id)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(Order.order_rid == order_rid, Shoe.shoe_rid == order_shoe_rid)
            .first()
        )
        order_id = order_shoe.Order.order_id
        order_shoe_id = order_shoe.OrderShoe.order_shoe_id
        print(order_shoe.OrderShoe.production_order_upload_status)
        if order_shoe.OrderShoe.production_order_upload_status != "1":
            return jsonify({"error": "Production order not uploaded yet"}), 500
        order_shoe.OrderShoe.production_order_upload_status = "2"
        db.session.commit()
        processor = EventProcessor()
        event1 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=38,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result1 = processor.processEvent(event1)
        if not result1:
            return jsonify({"error": "Failed to issue production order"}), 500
        db.session.add(event1)
        db.session.commit()
        event2 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=39,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result2 = processor.processEvent(event2)
        db.session.add(event2)
        db.session.commit()
        event3 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=40,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result3 = processor.processEvent(event3)
        db.session.add(event3)
        db.session.commit()
        event4 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=41,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result4 = processor.processEvent(event4)
        db.session.add(event4)
        db.session.commit()
        if not result2:
            return jsonify({"error": "Failed to issue production order"}), 500

    return jsonify({"message": "Production order issued successfully"})
