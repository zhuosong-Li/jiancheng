from flask import Blueprint, jsonify, request, send_file
from sqlalchemy.dialects.mysql import insert
import datetime
from app_config import app, db
from models import *
import os
from api_utility import randomIdGenerater
from event_processor import EventProcessor
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH
from general_document.bom import generate_excel_file

second_bom_bp = Blueprint("second_bom_bp", __name__)


@second_bom_bp.route("/secondbom/getnewbomid", methods=["GET"])
def get_new_bom_id():
    current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    bom_id = current_time_stamp + random_string + "F"
    return jsonify({"bomId": bom_id})


@second_bom_bp.route("/secondbom/getordershoes", methods=["GET"])
def get_order_second_bom():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(Order, OrderShoe, Shoe, OrderShoeStatus)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeStatus, OrderShoe.order_shoe_id == OrderShoeStatus.order_shoe_id)
        .filter(Order.order_id == order_id)
        .filter(OrderShoeStatus.current_status == 11)
        .all()
    )
    result = []
    for entity in entities:
        order, order_shoe, shoe, order_shoe_status = entity
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
                "editter": order_shoe.adjust_staff,
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
            unit_usage=item["unitUsage"],
            total_usage=item["approvalUsage"],
            department_id=item["useDepart"],
            remark=item["comment"],
            material_specification=item["materialSpecification"],
            bom_item_add_type=1,
            bom_item_color=item["color"],
            size_35_total_usage=item["sizeInfo"][0]["approvalAmount"],
            size_36_total_usage=item["sizeInfo"][1]["approvalAmount"],
            size_37_total_usage=item["sizeInfo"][2]["approvalAmount"],
            size_38_total_usage=item["sizeInfo"][3]["approvalAmount"],
            size_39_total_usage=item["sizeInfo"][4]["approvalAmount"],
            size_40_total_usage=item["sizeInfo"][5]["approvalAmount"],
            size_41_total_usage=item["sizeInfo"][6]["approvalAmount"],
            size_42_total_usage=item["sizeInfo"][7]["approvalAmount"],
            size_43_total_usage=item["sizeInfo"][8]["approvalAmount"],
            size_44_total_usage=item["sizeInfo"][9]["approvalAmount"],
            size_45_total_usage=item["sizeInfo"][10]["approvalAmount"],
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
        sizeInfo = [
            {
                "size": "35",
                "innerSize": "7",
                "outterSize": "7",
                "approvalAmount": (
                    item.size_35_total_usage if item.size_35_total_usage else 0.00
                ),
            },
            {
                "size": "36",
                "innerSize": "7",
                "outterSize": "7.5",
                "approvalAmount": (
                    item.size_36_total_usage if item.size_36_total_usage else 0.00
                ),
            },
            {
                "size": "37",
                "innerSize": "8",
                "outterSize": "8",
                "approvalAmount": (
                    item.size_37_total_usage if item.size_37_total_usage else 0.00
                ),
            },
            {
                "size": "38",
                "innerSize": "8",
                "outterSize": "8.5",
                "approvalAmount": (
                    item.size_38_total_usage if item.size_38_total_usage else 0.00
                ),
            },
            {
                "size": "39",
                "innerSize": "9",
                "outterSize": "9",
                "approvalAmount": (
                    item.size_39_total_usage if item.size_39_total_usage else 0.00
                ),
            },
            {
                "size": "40",
                "innerSize": "9",
                "outterSize": "9.5",
                "approvalAmount": (
                    item.size_40_total_usage if item.size_40_total_usage else 0.00
                ),
            },
            {
                "size": "41",
                "innerSize": "10",
                "outterSize": "10",
                "approvalAmount": (
                    item.size_41_total_usage if item.size_41_total_usage else 0.00
                ),
            },
            {
                "size": "42",
                "innerSize": "10",
                "outterSize": "10.5",
                "approvalAmount": (
                    item.size_42_total_usage if item.size_42_total_usage else 0.00
                ),
            },
            {
                "size": "43",
                "innerSize": "11",
                "outterSize": "11",
                "approvalAmount": (
                    item.size_43_total_usage if item.size_43_total_usage else 0.00
                ),
            },
            {
                "size": "44",
                "innerSize": "12",
                "outterSize": "12",
                "approvalAmount": (
                    item.size_44_total_usage if item.size_44_total_usage else 0.00
                ),
            },
            {
                "size": "45",
                "innerSize": "13",
                "outterSize": "13",
                "approvalAmount": (
                    item.size_45_total_usage if item.size_45_total_usage else 0.00
                ),
            },
        ]
        result.append(
            {
                "materialName": material.material_name,
                "materialType": material_type.material_type_name,
                "materialSpecification": item.material_specification,
                "supplierName": supplier.supplier_name,
                "useDepart": department.department_id,
                "unitUsage": item.unit_usage if item.unit_usage else 0.00 if material.material_category == 0 else None,
                "approvalUsage": item.total_usage if item.total_usage else 0.00,
                "unit": material.material_unit,
                "color": item.bom_item_color,
                "comment": item.remark,
                "materialCategory": material.material_category,
                "sizeInfo": sizeInfo,
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
            unit_usage=item["unitUsage"],
            total_usage=item["approvalUsage"],
            department_id=item["useDepart"],
            remark=item["comment"],
            material_specification=item["materialSpecification"],
            bom_item_add_type=1,
            bom_item_color=item["color"],
            size_35_total_usage=item["sizeInfo"][0]["approvalAmount"],
            size_36_total_usage=item["sizeInfo"][1]["approvalAmount"],
            size_37_total_usage=item["sizeInfo"][2]["approvalAmount"],
            size_38_total_usage=item["sizeInfo"][3]["approvalAmount"],
            size_39_total_usage=item["sizeInfo"][4]["approvalAmount"],
            size_40_total_usage=item["sizeInfo"][5]["approvalAmount"],
            size_41_total_usage=item["sizeInfo"][6]["approvalAmount"],
            size_42_total_usage=item["sizeInfo"][7]["approvalAmount"],
            size_43_total_usage=item["sizeInfo"][8]["approvalAmount"],
            size_44_total_usage=item["sizeInfo"][9]["approvalAmount"],
            size_45_total_usage=item["sizeInfo"][10]["approvalAmount"],
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
    order_shoe_id = bom.OrderShoe.order_shoe_id
    bom_id = bom.Bom.bom_id
    bom.Bom.bom_status = 2
    db.session.commit()
    bom_items = (
        db.session.query(BomItem, Material, MaterialType, Supplier, Color, Department)
        .join(Material, Material.material_id == BomItem.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(Color, Color.color_id == BomItem.bom_item_color)
        .outerjoin(Department, Department.department_id == BomItem.department_id)
        .filter(BomItem.bom_id == bom_id)
        .all()
    )
    if os.path.exists(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "secondbom")) == False:
        os.mkdir(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "secondbom"))
    series_data = []
    for bom_item in bom_items:
        index = 1
        series_data.append(
            {
                "序号": index,
                "材料类型": bom_item.MaterialType.material_type_name,
                "材料名称": bom_item.Material.material_name,
                "材料规格": bom_item.BomItem.material_specification,
                "颜色": bom_item.Color.color_name if bom_item.Color else "",
                "单位": bom_item.Material.material_unit,
                "厂家名称": bom_item.Material.material_supplier,
                "单位用量": bom_item.BomItem.unit_usage if bom_item.BomItem.unit_usage else "",
                "核定用量": bom_item.BomItem.total_usage,
                "使用工段": bom_item.Department.department_name,
                "备注": bom_item.BomItem.remark,
            }
        )
        index += 1
    image_save_path = os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "secondbom", "shoe_image.jpg")
    print(image_save_path)
    generate_excel_file(
        FILE_STORAGE_PATH+"/BOM-V1.0-temp.xlsx",
        os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "secondbom", "二次BOM表.xlsx"),
        {
            "order_id": order_rid,
            "last_type": "",
            "input_person": "",
            "order_finish_time": db.session.query(Order).filter(Order.order_rid == order_rid).first().end_date,
            "inherit_id": order_shoe_rid,
            "customer_id": db.session.query(OrderShoe).filter(OrderShoe.order_shoe_id == order_shoe_id).first().customer_product_name,


        },
        series_data,
        IMAGE_STORAGE_PATH + "shoe/" + order_shoe_rid+"/shoe_image.jpg",
        image_save_path,
    )
    
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

@second_bom_bp.route("/secondbom/download", methods=["GET"])
def download_bom():
    order_shoe_rid = request.args.get("ordershoerid")
    order_id = request.args.get("orderid")
    order_shoe = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    folder_path = os.path.join(FILE_STORAGE_PATH, order_id, order_shoe_rid)
    file_path = os.path.join(folder_path,'secondbom', "二次BOM表.xlsx")
    new_name = order_id + "-" + order_shoe_rid + "_二次BOM表.xlsx"
    return send_file(file_path, as_attachment=True, download_name=new_name)
