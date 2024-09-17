from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert
import datetime
from app_config import app, db
from models import *
from api_utility import randomIdGenerater
from event_processor import EventProcessor
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH

second_bom_bp = Blueprint("second_bom_bp", __name__)


@second_bom_bp.route("/secondbom/getnewbomid", methods=["GET"])
def get_new_bom_id():
    current_time_stamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    bom_id = current_time_stamp + random_string + "F"
    return jsonify({"bomId": bom_id})


@second_bom_bp.route("/secondbom/getordershoes", methods=["GET"])
def get_order_second_bom():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(Order.order_id == order_id)
        .all()
    )
    result = []
    for entity in entities:
        order, order_shoe, shoe = entity
        bom = (
            db.session.query(Bom)
            .filter(Bom.order_shoe_id == order_shoe.order_shoe_id,
                    Bom.bom_type == 1)
            .first()
        )
        if bom:
            status = bom.bom_status
        else:
            status = "0"
        if status == "0":
            status = "未填写"
        elif status == "1":
            status = "已保存"
        elif status == "2":
            status = "已提交"
        elif status == "3":
            status = "已下发"
        elif status == "4":
            status = "等待用量填写"
        elif status == "5":
            status = "已用量填写"
        elif status == "6":
            status = "BOM完成"
        result.append(
            {
                "orderId": order.order_rid,
                "orderShoeId": order_shoe.order_shoe_id,
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "editter": shoe.shoe_adjuster,
                "image" : IMAGE_STORAGE_PATH+shoe.shoe_image_url if shoe.shoe_image_url is not None else None,
                "status": status,
            }
        )
    return jsonify(result)


@second_bom_bp.route("/secondbom/savebom", methods=["POST"])
def save_bom():
    bom_rid = request.json.get("bomId")
    order_id = request.json.get("orderId")
    order_shoe_rid = request.json.get("orderShoeId")
    bom_data = request.json.get("bomData")
    print(order_id, order_shoe_rid, bom_data)
    order_shoe_id = (
        db.session.query(OrderShoe, Shoe, Order)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(Order, OrderShoe.order_id == Order.order_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
        .OrderShoe.order_shoe_id
    )
    bom = Bom(bom_rid=bom_rid, order_shoe_id=order_shoe_id, bom_status=1, bom_type=1)
    db.session.add(bom)
    db.session.commit()
    bom_id = db.session.query(Bom).filter(Bom.bom_rid == bom_rid).first().bom_id
    for item in bom_data:
        material_id = (
            db.session.query(Material, Supplier)
            .join(Supplier, Material.material_supplier == Supplier.supplier_id)
            .filter(
                Material.material_name == item["materialName"],
                Supplier.supplier_name == item["supplierName"],
            )
            .first()
            .Material.material_id
        )
        bom_item = BomItem(
            bom_id=bom_id,
            material_id=material_id,
            total_usage=0,
            department_id=item["useDepart"],
            remark=item["comment"],
            material_specification=item["materialSpecification"],
            bom_item_add_type=1,
            bom_item_color=item["color"],
        )
        db.session.add(bom_item)
    db.session.commit()

    return jsonify({"status": "success"})


@second_bom_bp.route("/secondbom/getbomdetails", methods=["GET"])
def get_bom_details():
    order_id = request.args.get("orderid")
    order_shoe_id = request.args.get("ordershoeid")
    bom_id = (
        db.session.query(Bom, OrderShoe, Order, Shoe)
        .join(OrderShoe, Bom.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Order, OrderShoe.order_id == Order.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_id,Bom.bom_type == 1)
        .first()
        .Bom.bom_id
    )
    print(bom_id)
    bom_rid = db.session.query(Bom).filter(Bom.bom_id == bom_id).first().bom_rid
    bom_items = (
        db.session.query(BomItem, Material, MaterialType, Department, Supplier)
        .join(Material, BomItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(Department, BomItem.department_id == Department.department_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .filter(BomItem.bom_id == bom_id)
        .all()
    )
    result = []
    for bom_item in bom_items:
        item, material, material_type, department, supplier = bom_item
        result.append(
            {
                "materialName": material.material_name,
                "materialType": material_type.material_type_name,
                "materialSpecification": item.material_specification,
                "supplierName": supplier.supplier_name,
                "useDepart": department.department_id,
                "unit": material.material_unit,
                "color": item.bom_item_color,
                "comment": item.remark,
            }
        )
    fin_result = {"bomId": bom_rid, "bomData": result}
    print(fin_result)
    return jsonify(fin_result)

@second_bom_bp.route("/secondbom/editbom", methods=["POST"])
def edit_bom():
    bom_rid = request.json.get("bomId")
    order_id = request.json.get("orderId")
    order_shoe_rid = request.json.get("orderShoeId")
    bom_data = request.json.get("bomData")
    print(order_id, order_shoe_rid, bom_data)
    order_shoe_id = (
        db.session.query(OrderShoe, Shoe, Order)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(Order, OrderShoe.order_id == Order.order_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
        .OrderShoe.order_shoe_id
    )
    bom_id = Bom.query.filter(Bom.bom_rid == bom_rid,Bom.bom_type == 1).first().bom_id
    db.session.query(BomItem).filter(BomItem.bom_id == bom_id).delete()
    db.session.commit()

    for item in bom_data:
        material_id = (
            db.session.query(Material, Supplier)
            .join(Supplier, Material.material_supplier == Supplier.supplier_id)
            .filter(
                Material.material_name == item["materialName"],
                Supplier.supplier_name == item["supplierName"],
            )
            .first()
            .Material.material_id
        )
        bom_item = BomItem(
            bom_id=bom_id,
            material_id=material_id,
            total_usage=0,
            department_id=item["useDepart"],
            remark=item["comment"],
            material_specification=item["materialSpecification"],
            bom_item_add_type=1,
            bom_item_color=item["color"],
        )
        db.session.add(bom_item)
    db.session.commit()

    return jsonify({"status": "success"})

@second_bom_bp.route("/secondbom/submitbom", methods=["POST"])
def submit_bom():
    order_shoe_rid = request.json.get("orderShoeId")
    order_rid = request.json.get("orderId")
    bom = (
        db.session.query(Bom, OrderShoe, Order, Shoe)
        .join(OrderShoe, Bom.order_shoe_id == OrderShoe.order_shoe_id)
        .join(Order, OrderShoe.order_id == Order.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_rid, Shoe.shoe_rid == order_shoe_rid,Bom.bom_type == 1)
        .first()
    )
    bom.Bom.bom_status = 2
    db.session.commit()
    
    return jsonify({"status": "success"})

@second_bom_bp.route("/secondbom/issueboms", methods=["POST"])
def issue_boms():
    order_rid = request.json.get("orderId")
    order_shoe_rids = request.json.get("orderShoeIds")
    order_id = (
        db.session.query(Order)
        .filter(Order.order_rid == order_rid)
        .first()
        .order_id
    )
    for order_shoe_rid in order_shoe_rids:
        bom = (
            db.session.query(Bom, OrderShoe, Order, Shoe)
            .join(OrderShoe, Bom.order_shoe_id == OrderShoe.order_shoe_id)
            .join(Order, OrderShoe.order_id == Order.order_id)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(Order.order_rid == order_rid, Shoe.shoe_rid == order_shoe_rid,Bom.bom_type == 1)
            .first()
        )
        bom.Bom.bom_status = 3
        order_shoe_id = bom.OrderShoe.order_shoe_id
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=60,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=61,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=62,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=63,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
    return jsonify({"status": "success"})
