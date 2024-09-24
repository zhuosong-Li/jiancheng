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
    entities = (
        db.session.query(
            Order, OrderShoe, OrderShoeType, Shoe, ShoeType, Color, Bom, TotalBom, PurchaseOrder
        )
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .join(OrderShoeType, OrderShoeType.order_shoe_id == OrderShoe.order_shoe_id)
        .join(ShoeType, ShoeType.shoe_type_id == OrderShoeType.shoe_type_id)
        .join(Color, ShoeType.color_id == Color.color_id)
        .outerjoin(
            Bom, OrderShoeType.order_shoe_type_id == Bom.order_shoe_type_id
        )  # Assuming BOM is optional
        .outerjoin(
            TotalBom, Bom.total_bom_id == TotalBom.total_bom_id
        )  # Assuming TotalBom is optional
        .outerjoin(
            PurchaseOrder, PurchaseOrder.bom_id == TotalBom.total_bom_id
        )  # Assuming PurchaseOrder is optional
        .all()
    )

    print(entities)

    # Initialize the result list
    result_dict = {}

    # Loop through the entities to build the result
    for entity in entities:
        (
            order,
            order_shoe,
            order_shoe_type,
            shoe,
            shoe_type,
            color,
            bom,
            total_bom,
            purchase_order,
        ) = entity
        if order_shoe.production_order_upload_status == "0":
            status = "未上传"
        elif order_shoe.production_order_upload_status == "1":
            status = "已上传"
        elif order_shoe.production_order_upload_status == "2":
            status = "已下发"
        if shoe.shoe_rid not in result_dict:
            result_dict[shoe.shoe_rid] = {
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "status": status,
                "typeInfos": [],  # Initialize empty list for colors
                "colorSet": set(),  # Initialize a set to track colors for each shoe
            }

        # Check if the color is already added for this shoe
        if color.color_name not in result_dict[shoe.shoe_rid]["colorSet"]:
            # Only link BOM information to the color associated with the correct OrderShoeType
            first_bom_id = None
            first_bom_status = None
            first_purchase_order_id = None
            first_purchase_order_status = None
            second_bom_id = None
            second_bom_status = None
            second_purchase_order_id = None
            second_purchase_order_status = None

            # Only attach BOM and PurchaseOrder if it's associated with the correct OrderShoeType
            if bom and bom.bom_type == 0:
                first_bom_id = bom.bom_rid
                if bom.bom_status == "1":
                    first_bom_status = "已保存"
                elif bom.bom_status == "2":
                    first_bom_status = "已提交"
                elif bom.bom_status == "3":
                    first_bom_status = "已下发"

            # Similarly, attach PurchaseOrder if applicable
            if purchase_order and purchase_order.purchase_order_type == "F":
                first_purchase_order_id = purchase_order.purchase_order_rid
                if purchase_order.purchase_order_status == "1":
                    first_purchase_order_status = "已保存"
                elif purchase_order.purchase_order_status == "2":
                    first_purchase_order_status = "已提交"
                elif purchase_order.purchase_order_status == "3":
                    first_purchase_order_status = "已下发"

            # Same logic for second BOM and PurchaseOrder
            if bom and bom.bom_type != 0:
                second_bom_id = bom.bom_rid
                if bom.bom_status == "1":
                    second_bom_status = "已保存"
                elif bom.bom_status == "2":
                    second_bom_status = "已提交"
                elif bom.bom_status == "3":
                    second_bom_status = "已下发"

            if purchase_order and purchase_order.purchase_order_type == "S":
                second_purchase_order_id = purchase_order.purchase_order_rid
                if purchase_order.purchase_order_status == "1":
                    second_purchase_order_status = "已保存"
                elif purchase_order.purchase_order_status == "2":
                    second_purchase_order_status = "已提交"
                elif purchase_order.purchase_order_status == "3":
                    second_purchase_order_status = "已下发"

            # Append the correct BOM and PurchaseOrder data to typeInfos
            result_dict[shoe.shoe_rid]["typeInfos"].append(
                {
                    "orderShoeRid": shoe.shoe_rid,
                    "color": color.color_name,
                    "image": (
                        IMAGE_STORAGE_PATH + shoe_type.shoe_image_url
                        if shoe_type.shoe_image_url
                        else None
                    ),
                    "firstBomId": first_bom_id if first_bom_id else "未填写",
                    "firstBomStatus": first_bom_status if first_bom_id else "未填写",
                    "firstPurchaseOrderId": (
                        first_purchase_order_id if first_purchase_order_id else "未填写"
                    ),
                    "firstPurchaseOrderStatus": (
                        first_purchase_order_status
                        if first_purchase_order_id
                        else "未填写"
                    ),
                    "secondBomId": second_bom_id if second_bom_id else "未填写",
                    "secondBomStatus": second_bom_status if second_bom_id else "未填写",
                    "secondPurchaseOrderId": (
                        second_purchase_order_id
                        if second_purchase_order_id
                        else "未填写"
                    ),
                    "secondPurchaseOrderStatus": (
                        second_purchase_order_status
                        if second_purchase_order_id
                        else "未填写"
                    ),
                }
            )

            # Add the color to the colorSet to prevent future duplicates
            result_dict[shoe.shoe_rid]["colorSet"].add(color.color_name)

    # Remove the colorSet before returning the result
    for shoe_rid in result_dict:
        result_dict[shoe_rid].pop("colorSet")

    # Convert result_dict to a list of values
    result = list(result_dict.values())
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
