from datetime import datetime

import os
import shutil
from app_config import db
from flask import Blueprint, jsonify, request
from models import *
from event_processor import EventProcessor
from general_document.bom import generate_excel_file
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH

usage_calculation_bp = Blueprint("usage_calculation_bp", __name__)


@usage_calculation_bp.route("/usagecalculation/getallboms", methods=["GET"])
def get_all_boms():
    order_id = request.args.get("orderid")
    entities = (
        db.session.query(Order, OrderShoe, Shoe, OrderShoeStatus)
        .join(OrderShoe, OrderShoe.order_id == Order.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .join(OrderShoeStatus, OrderShoe.order_shoe_id == OrderShoeStatus.order_shoe_id)
        .filter(Order.order_id == order_id)
        .filter(OrderShoeStatus.current_status == 4)
        .all()
    )
    result = []
    for entity in entities:
        order, order_shoe, shoe, order_shoe_status = entity
        bom = (
            db.session.query(Bom)
            .filter(Bom.order_shoe_id == order_shoe.order_shoe_id)
            .first()
        )
        if bom:
            status = bom.bom_status
        else:
            status = "0"
        if status == "0":
            status = "BOM未填写"
        elif status == "1":
            status = "BOM已保存"
        elif status == "2":
            status = "BOM已提交"
        elif status == "3":
            status = "等待用量填写"
        elif status == "4":
            status = "用量填写已保存"
        elif status == "5":
            status = "用量填写已提交"
        elif status == "6":
            status = "用量填写已下发"
        result.append(
            {
                "orderId": order.order_rid,
                "orderShoeId": order_shoe.order_shoe_id,
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "editter": order_shoe.adjust_staff,
                "bomId": bom.bom_rid if bom else "",
                "status": status,
                "image" : IMAGE_STORAGE_PATH+shoe.shoe_image_url if shoe.shoe_image_url is not None else None,
            }
        )
    return jsonify(result)


@usage_calculation_bp.route("/usagecalculation/getshoebomitems", methods=["GET"])
def get_shoe_bom_items():
    bom_rid = request.args.get("bomrid")
    entities = (
        db.session.query(Bom, BomItem, Material, MaterialType, Supplier, Color)
        .join(BomItem, BomItem.bom_id == Bom.bom_id)
        .join(Material, Material.material_id == BomItem.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(Color, Color.color_id == BomItem.bom_item_color)
        .filter(Bom.bom_rid == bom_rid)
        .all()
    )
    result = []
    for entity in entities:
        bom, bom_item, material, material_type, supplier, color = entity
        sizeInfo = [
            {
                "size": "35",
                "innerSize": "7",
                "outterSize": "7",
                "approvalAmount": (
                    bom_item.size_35_total_usage if bom_item.size_35_total_usage else 0.00
                ),
            },
            {
                "size": "36",
                "innerSize": "7",
                "outterSize": "7.5",
                "approvalAmount": (
                    bom_item.size_36_total_usage if bom_item.size_36_total_usage else 0.00
                ),
            },
            {
                "size": "37",
                "innerSize": "8",
                "outterSize": "8",
                "approvalAmount": (
                    bom_item.size_37_total_usage if bom_item.size_37_total_usage else 0.00
                ),
            },
            {
                "size": "38",
                "innerSize": "8",
                "outterSize": "8.5",
                "approvalAmount": (
                    bom_item.size_38_total_usage if bom_item.size_38_total_usage else 0.00
                ),
            },
            {
                "size": "39",
                "innerSize": "9",
                "outterSize": "9",
                "approvalAmount": (
                    bom_item.size_39_total_usage if bom_item.size_39_total_usage else 0.00
                ),
            },
            {
                "size": "40",
                "innerSize": "9",
                "outterSize": "9.5",
                "approvalAmount": (
                    bom_item.size_40_total_usage if bom_item.size_40_total_usage else 0.00
                ),
            },
            {
                "size": "41",
                "innerSize": "10",
                "outterSize": "10",
                "approvalAmount": (
                    bom_item.size_41_total_usage if bom_item.size_41_total_usage else 0.00
                ),
            },
            {
                "size": "42",
                "innerSize": "10",
                "outterSize": "10.5",
                "approvalAmount": (
                    bom_item.size_42_total_usage if bom_item.size_42_total_usage else 0.00
                ),
            },
            {
                "size": "43",
                "innerSize": "11",
                "outterSize": "11",
                "approvalAmount": (
                    bom_item.size_43_total_usage if bom_item.size_43_total_usage else 0.00
                ),
            },
            {
                "size": "44",
                "innerSize": "12",
                "outterSize": "12",
                "approvalAmount": (
                    bom_item.size_44_total_usage if bom_item.size_44_total_usage else 0.00
                ),
            },
            {
                "size": "45",
                "innerSize": "13",
                "outterSize": "13",
                "approvalAmount": (
                    bom_item.size_45_total_usage if bom_item.size_45_total_usage else 0.00
                ),
            },
        ]

        result.append(
            {
                "bomItemId": bom_item.bom_item_id,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialSpecification": bom_item.material_specification,
                "color": color.color_id if color else "",
                "unit": material.material_unit,
                "unitUsage": bom_item.unit_usage if bom_item.unit_usage else 0.00 if material.material_category == 0 else None,
                "approvalUsage": bom_item.total_usage if bom_item.total_usage else 0.00,
                "useDepart": bom_item.department_id,
                "supplierName": supplier.supplier_name,
                "materialCategory": material.material_category,
                "remark": bom_item.remark,
                "sizeInfo": sizeInfo,
            }
        )
    return jsonify(result)

@usage_calculation_bp.route("/usagecalculation/savebomusage", methods=["POST"])
def save_bom_usage():
    bom_rid = request.json.get("bomRid")
    bom_items = request.json.get("bomItems")
    bom = (
        db.session.query(Bom)
        .filter(Bom.bom_rid == bom_rid)
        .first()
    )
    bom.bom_status = "4"
    db.session.commit()
    print(bom_items)
    for bom_item in bom_items:
        entity = (
            db.session.query(BomItem)
            .filter(BomItem.bom_item_id == bom_item["bomItemId"])
            .first()
        )
        entity.size_35_total_usage = bom_item["sizeInfo"][0]["approvalAmount"]
        entity.size_36_total_usage = bom_item["sizeInfo"][1]["approvalAmount"]
        entity.size_37_total_usage = bom_item["sizeInfo"][2]["approvalAmount"]
        entity.size_38_total_usage = bom_item["sizeInfo"][3]["approvalAmount"]
        entity.size_39_total_usage = bom_item["sizeInfo"][4]["approvalAmount"]
        entity.size_40_total_usage = bom_item["sizeInfo"][5]["approvalAmount"]
        entity.size_41_total_usage = bom_item["sizeInfo"][6]["approvalAmount"]
        entity.size_42_total_usage = bom_item["sizeInfo"][7]["approvalAmount"]
        entity.size_43_total_usage = bom_item["sizeInfo"][8]["approvalAmount"]
        entity.size_44_total_usage = bom_item["sizeInfo"][9]["approvalAmount"]
        entity.size_45_total_usage = bom_item["sizeInfo"][10]["approvalAmount"]
        entity.total_usage = bom_item["approvalUsage"]
        entity.unit_usage = bom_item["unitUsage"]
        entity.remark = bom_item["remark"]
        db.session.commit()
    return jsonify({"status": "success"})

@usage_calculation_bp.route("/usagecalculation/submitbomusage", methods=["POST"])
def submit_bom_usage():
    bom_rid = request.json.get("bomRid")
    bom = (
        db.session.query(Bom)
        .filter(Bom.bom_rid == bom_rid)
        .first()
    )
    order_shoe_id = bom.order_shoe_id
    order_shoe_rid = (
        db.session.query(OrderShoe, Shoe)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
        .first()
        .Shoe.shoe_rid
    )
    order_rid = (
        db.session.query(Order, OrderShoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
        .first()
        .Order.order_rid
    )
    bom_id = bom.bom_id
    bom.bom_status = "5"
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
    if os.path.exists(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "firstbom")) == False:
        os.mkdir(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "firstbom"))
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
                "厂家名称": bom_item.Supplier.supplier_name,
                "单位用量": bom_item.BomItem.unit_usage if bom_item.BomItem.unit_usage else "",
                "核定用量": bom_item.BomItem.total_usage,
                "使用工段": bom_item.Department.department_name,
                "备注": bom_item.BomItem.remark,
            }
        )
        index += 1
    image_save_path = os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "firstbom", "shoe_image.jpg")
    print(image_save_path)
    generate_excel_file(
        FILE_STORAGE_PATH+"/BOM-V1.0-temp.xlsx",
        os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "firstbom", "一次BOM表.xlsx"),
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

@usage_calculation_bp.route("/usagecalculation/issuebomusage", methods=["POST"])
def issue_bom_usage():
    order_rid = request.json.get("orderId")
    order_shoes = request.json.get("orderShoeIds")
    order_id = (
        db.session.query(Order)
        .filter(Order.order_rid == order_rid)
        .first()
        .order_id
    )
    for order_shoe_rid in order_shoes:
        bom = (
            db.session.query(Bom, OrderShoe, Order, Shoe)
            .join(OrderShoe, Bom.order_shoe_id == OrderShoe.order_shoe_id)
            .join(Order, OrderShoe.order_id == Order.order_id)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(Order.order_rid == order_rid, Shoe.shoe_rid == order_shoe_rid)
            .first()
        )
        bom.Bom.bom_status = "6"
        db.session.commit()
        order_shoe_id = bom.OrderShoe.order_shoe_id
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=46,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"status": "failed"})
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=47,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"status": "failed"})
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=48,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"status": "failed"})
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=49,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"status": "failed"})
        db.session.add(event)
        db.session.commit()


    return jsonify({"status": "success"})