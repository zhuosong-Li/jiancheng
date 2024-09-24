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
def get_order_first_bom():
    order_id = request.args.get("orderid")

    # Querying the necessary data with joins and filters
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
        .outerjoin(TotalBom, Bom.total_bom_id == TotalBom.total_bom_id)
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
        status_string = ""
        statuses = (
            db.session.query(OrderShoeStatus, OrderShoeStatusReference)
            .join(
                OrderShoeStatusReference,
                OrderShoeStatus.current_status == OrderShoeStatusReference.status_id,
            )
            .filter(OrderShoeStatus.order_shoe_id == order_shoe.order_shoe_id)
            .all()
        )
        for status in statuses:
            status_string = (
                status_string + status.OrderShoeStatusReference.status_name + " "
            )

        # Grouping by shoe_rid (inheritId) to avoid duplicate shoes
        if shoe.shoe_rid not in result_dict:
            result_dict[shoe.shoe_rid] = {
                "orderId": order.order_rid,
                "orderShoeId": order_shoe.order_shoe_id,
                "inheritId": shoe.shoe_rid,
                "status": status_string,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "editter": order_shoe.adjust_staff,
                "typeInfos": [],  # Initialize list for type info (colors, etc.)
                "colorSet": set(),  # Initialize a set to track colors for each shoe
            }

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
                    first_bom_status = "材料已保存"
                elif bom.bom_status == "2":
                    first_bom_status = "材料已提交"
                elif bom.bom_status == "3":
                    first_bom_status = "等待用量填写"
                elif bom.bom_status == "4":
                    first_bom_status = "用量填写已保存"
                elif bom.bom_status == "5":
                    first_bom_status = "用量填写已提交"
                elif bom.bom_status == "6":
                    first_bom_status = "用量填写已下发"

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


@usage_calculation_bp.route("/usagecalculation/getshoebomitems", methods=["GET"])
def get_shoe_bom_items():
    bom_rid = request.args.get("bomrid")
    entities = (
        db.session.query(Bom, BomItem, Material, MaterialType, Supplier)
        .join(BomItem, Bom.bom_id == BomItem.bom_id)
        .join(Material, Material.material_id == BomItem.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Supplier.supplier_id == Material.material_supplier)
        .filter(Bom.bom_rid == bom_rid)
        .all()
    )
    result = []
    for entity in entities:
        bom, bom_item, material, material_type, supplier = entity
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
                "materialModel": bom_item.material_model,
                "materialSpecification": bom_item.material_specification,
                "color": bom_item.bom_item_color,
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
    bom.bom_status = "5"
    db.session.commit()

    return jsonify({"status": "success"})

@usage_calculation_bp.route("/usagecalculation/issuebomusage", methods=["POST"])
def issue_bom_usage():
    order_rid = request.json.get("orderId")
    order_shoes = request.json.get("orderShoeIds")
    colors = request.json.get("colors")
    order_id = (
        db.session.query(Order)
        .filter(Order.order_rid == order_rid)
        .first()
        .order_id
    )
    for order_shoe_rid in order_shoes:
        index = order_shoe_rids.index(order_shoe_rid)
        color = colors[index]
        for color_item in color:
            order_shoe_type_id = (
                db.session.query(Order, OrderShoe, Shoe, ShoeType, OrderShoeType, Color)
                .join(OrderShoe, Order.order_id == OrderShoe.order_id)
                .join(OrderShoeType, OrderShoe.order_shoe_id == OrderShoeType.order_shoe_id)
                .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
                .join(ShoeType, OrderShoeType.shoe_type_id == ShoeType.shoe_type_id)
                .join(Color, ShoeType.color_id == Color.color_id)
                .filter(
                    Order.order_rid == order_rid,
                    Shoe.shoe_rid == order_shoe_rid,
                )
                .filter(Color.color_name == color_item)
                .first()
                .OrderShoeType.order_shoe_type_id
            )
            bom = (
                db.session.query(Bom)
                .filter(
                    Bom.order_shoe_type_id == order_shoe_type_id, Bom.bom_type == 0
                )
                .first()
            )
            bom.Bom.bom_status = "6"
            db.session.commit()
        order_shoe_id = (
            db.session.query(OrderShoe, Shoe)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(OrderShoe.order_id == order_id, Shoe.shoe_rid == order_shoe_rid)
            .first()
            .OrderShoe.order_shoe_id
        )
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