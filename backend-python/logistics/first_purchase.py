from flask import Blueprint, jsonify, request, send_file
from sqlalchemy.dialects.mysql import insert
import datetime
from app_config import app, db
from models import *
from api_utility import randomIdGenerater
from event_processor import EventProcessor
from file_locations import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH
from itertools import groupby
from operator import itemgetter
from general_document.purchase_divide_order import generate_excel_file
from general_document.size_purchase_divide_order import generate_size_excel_file
from general_document.material_statistics import generate_material_statistics_file
import os
import zipfile

first_purchase_bp = Blueprint("first_purrchase_bp", __name__)


@first_purchase_bp.route("/firstpurchase/getordershoelist", methods=["GET"])
def get_order_shoe_list():
    order_id = request.args.get("orderid")

    # Querying the necessary data with joins and filters
    entities = (
        db.session.query(
            Order,
            OrderShoe,
            OrderShoeType,
            Shoe,
            ShoeType,
            Color,
            Bom,
            TotalBom,
            PurchaseOrder,
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
        .outerjoin(PurchaseOrder, PurchaseOrder.bom_id == TotalBom.total_bom_id)
        .filter(Order.order_id == order_id)
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
        if purchase_order:
            if purchase_order.purchase_order_status == "1":
                current_status = "已保存"
            elif purchase_order.purchase_order_status == "2":
                current_status = "已提交"
        else:
            current_status = "未填写"
        # Grouping by shoe_rid (inheritId) to avoid duplicate shoes
        # Initialize the result dictionary for the shoe if not already present
        if shoe.shoe_rid not in result_dict:
            result_dict[shoe.shoe_rid] = {
                "orderId": order.order_rid,
                "orderShoeId": order_shoe.order_shoe_id,
                "inheritId": shoe.shoe_rid,
                "currentStatus": current_status,
                "totalBomId": total_bom.total_bom_rid if total_bom else "未填写",
                "purchaseOrderId": (
                    purchase_order.purchase_order_rid if purchase_order else "未填写"
                ),
                "status": status_string,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "editter": order_shoe.adjust_staff,
                "typeInfos": [],  # Initialize list for type info (colors, etc.)
                "colorSet": set(),  # Initialize set to track colors and prevent duplicate entries
            }

        # Check if this color already exists in typeInfos
        existing_entry = next(
            (
                info
                for info in result_dict[shoe.shoe_rid]["typeInfos"]
                if info["color"] == color.color_name
            ),
            None,
        )

        # Prepare BOM and PurchaseOrder details
        first_bom_id = None
        first_bom_status = "未填写"
        first_purchase_order_id = None
        first_purchase_order_status = "未填写"
        second_bom_id = None
        second_bom_status = "未填写"
        second_purchase_order_id = None
        second_purchase_order_status = "未填写"

        # Set BOM details based on bom_type
        if bom:
            if bom.bom_type == 0:
                first_bom_id = bom.bom_rid
                first_bom_status = {
                    "1": "材料已保存",
                    "2": "材料已提交",
                    "3": "等待用量填写",
                    "4": "用量填写已保存",
                    "5": "用量填写已提交",
                    "6": "用量填写已下发",
                }.get(bom.bom_status, "未填写")
            elif bom.bom_type == 1:
                second_bom_id = bom.bom_rid
                second_bom_status = {"1": "已保存", "2": "已提交", "3": "已下发"}.get(
                    bom.bom_status, "未填写"
                )

        # Set PurchaseOrder details based on purchase_order_type
        if purchase_order:
            if purchase_order.purchase_order_type == "F":
                first_purchase_order_id = purchase_order.purchase_order_rid
                first_purchase_order_status = {
                    "1": "已保存",
                    "2": "已提交",
                    "3": "已下发",
                }.get(purchase_order.purchase_order_status, "未填写")
            elif purchase_order.purchase_order_type == "S":
                second_purchase_order_id = purchase_order.purchase_order_rid
                second_purchase_order_status = {
                    "1": "已保存",
                    "2": "已提交",
                    "3": "已下发",
                }.get(purchase_order.purchase_order_status, "未填写")

        # If the color entry already exists, update it with BOM details
        if existing_entry:
            print(existing_entry)
            # Update only if fields are not already filled to prevent overwriting
            if first_bom_id and existing_entry.get("firstBomId") == "未填写":
                existing_entry["firstBomId"] = first_bom_id
                existing_entry["firstBomStatus"] = first_bom_status
                existing_entry["firstPurchaseOrderId"] = first_purchase_order_id
                existing_entry["firstPurchaseOrderStatus"] = first_purchase_order_status

            if second_bom_id and existing_entry.get("secondBomId") == "未填写":
                existing_entry["secondBomId"] = second_bom_id
                existing_entry["secondBomStatus"] = second_bom_status
                existing_entry["secondPurchaseOrderId"] = second_purchase_order_id
                existing_entry["secondPurchaseOrderStatus"] = (
                    second_purchase_order_status
                )
        else:
            # If the color doesn't exist, create a new entry in typeInfos
            result_dict[shoe.shoe_rid]["typeInfos"].append(
                {
                    "orderShoeTypeId": order_shoe_type.order_shoe_type_id,
                    "orderShoeRid": shoe.shoe_rid,
                    "color": color.color_name,
                    "image": (
                        IMAGE_STORAGE_PATH + shoe_type.shoe_image_url
                        if shoe_type.shoe_image_url
                        else None
                    ),
                    "firstBomId": first_bom_id if first_bom_id else "未填写",
                    "firstBomStatus": first_bom_status,
                    "firstPurchaseOrderId": (
                        first_purchase_order_id if first_purchase_order_id else "未填写"
                    ),
                    "firstPurchaseOrderStatus": first_purchase_order_status,
                    "secondBomId": second_bom_id if second_bom_id else "未填写",
                    "secondBomStatus": second_bom_status,
                    "secondPurchaseOrderId": (
                        second_purchase_order_id
                        if second_purchase_order_id
                        else "未填写"
                    ),
                    "secondPurchaseOrderStatus": second_purchase_order_status,
                }
            )

        # Add the color to colorSet to prevent future duplicates
        result_dict[shoe.shoe_rid]["colorSet"].add(color.color_name)

    # Remove the colorSet before returning the result
    for shoe_rid in result_dict:
        result_dict[shoe_rid].pop("colorSet")

    # Convert result_dict to a list of values
    result = list(result_dict.values())

    return jsonify(result)


@first_purchase_bp.route("/firstpurchase/getnewpurchaseorderid", methods=["GET"])
def get_new_purchase_order_id():
    department_id = "01"
    current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    purchase_order_id = department_id + current_time_stamp + random_string + "F"
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
        .filter(Bom.bom_type == "0")
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
                status = purchase_order.purchase_order_status
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
                    "editter": order_shoe.adjust_staff,
                    "bomId": bom.bom_rid if bom else "",
                    "purchaseOrderId": (
                        purchase_order.purchase_order_rid if purchase_order else ""
                    ),
                    "status": status,
                    "image": (
                        IMAGE_STORAGE_PATH + shoe.shoe_image_url
                        if shoe.shoe_image_url is not None
                        else None
                    ),
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
                    "image": (
                        IMAGE_STORAGE_PATH + shoe.shoe_image_url
                        if shoe.shoe_image_url is not None
                        else None
                    ),
                }
            )
    return jsonify(result)


import copy


@first_purchase_bp.route("/firstpurchase/getshoebomitems", methods=["GET"])
def get_shoe_bom_items():
    bom_rid = request.args.get("bomrid")

    # Define size-specific inner and outer sizes
    size_mappings = {
        "35": {"innerSize": "7", "outterSize": "7"},
        "36": {"innerSize": "7", "outterSize": "7.5"},
        "37": {"innerSize": "8", "outterSize": "8"},
        "38": {"innerSize": "8", "outterSize": "8.5"},
        "39": {"innerSize": "9", "outterSize": "9"},
        "40": {"innerSize": "9", "outterSize": "9.5"},
        "41": {"innerSize": "10", "outterSize": "10"},
        "42": {"innerSize": "10", "outterSize": "10.5"},
        "43": {"innerSize": "11", "outterSize": "11"},
        "44": {"innerSize": "12", "outterSize": "12"},
        "45": {"innerSize": "13", "outterSize": "13"},
    }

    # Query all Bom items under the given TotalBom, based on the bom_rid
    entities = (
        db.session.query(
            Bom,
            TotalBom,
            BomItem,
            Material,
            MaterialType,
            Supplier,
            Color,
            PurchaseOrderItem,
        )
        .join(TotalBom, Bom.total_bom_id == TotalBom.total_bom_id)
        .join(BomItem, BomItem.bom_id == Bom.bom_id)
        .join(Material, Material.material_id == BomItem.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(
            PurchaseOrderItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id
        )
        .filter(TotalBom.total_bom_rid == bom_rid)
        .all()
    )

    # Dictionary to combine duplicated items
    combined_items = {}

    for entity in entities:
        (
            bom,
            total_bom,
            bom_item,
            material,
            material_type,
            supplier,
            color,
            purchase_order_item,
        ) = entity

        # Create a unique key for each item based on essential attributes
        key = (
            material_type.material_type_name,
            material.material_name,
            bom_item.material_specification,
            bom_item.bom_item_color if bom_item.bom_item_color else "",
            supplier.supplier_name,
        )

        # Initialize sizeInfo structure for this item
        size_info_template = {
            size: {"approvalAmount": 0.00, "purchaseAmount": 0.00}
            for size in size_mappings.keys()
        }

        # If key already exists, accumulate the data; otherwise, initialize
        if key not in combined_items:
            combined_items[key] = {
                "bomItemId": bom_item.bom_item_id,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialModel": bom_item.material_model,
                "materialSpecification": bom_item.material_specification,
                "color": bom_item.bom_item_color if bom_item.bom_item_color else "",
                "unit": material.material_unit,
                "unitUsage": bom_item.unit_usage
                or (0.00 if material.material_category == 0 else None),
                "approvalUsage": bom_item.total_usage or 0.00,
                "useDepart": bom_item.department_id,
                "purchaseAmount": (
                    purchase_order_item.purchase_amount if purchase_order_item else 0.00
                ),
                "supplierName": supplier.supplier_name,
                "materialCategory": material.material_category,
                "remark": bom_item.remark,
                "sizeInfo": copy.deepcopy(
                    size_info_template
                ),  # Deep copy to ensure independence
            }

        # Accumulate data for each size in sizeInfo
        for size, sizes in size_mappings.items():
            size_field = f"size_{size}_total_usage"
            purchase_field = f"size_{size}_purchase_amount"

            approval_amount = getattr(bom_item, size_field, 0.00) or 0.00
            purchase_amount = (
                getattr(purchase_order_item, purchase_field, 0.00)
                if purchase_order_item
                else 0.00
            )
            approval_amount = approval_amount if approval_amount is not None else 0.00
            purchase_amount = purchase_amount if purchase_amount is not None else 0.00

            combined_items[key]["sizeInfo"][size]["approvalAmount"] += approval_amount
            combined_items[key]["sizeInfo"][size]["purchaseAmount"] += purchase_amount

    # Format result for JSON response
    result = [
        {
            **value,
            "sizeInfo": [
                {
                    "size": size,
                    "innerSize": size_mappings[size]["innerSize"],
                    "outterSize": size_mappings[size]["outterSize"],
                    "approvalAmount": info["approvalAmount"],
                    "purchaseAmount": info["purchaseAmount"],
                }
                for size, info in value["sizeInfo"].items()
            ],
        }
        for value in combined_items.values()
    ]

    return jsonify(result)


@first_purchase_bp.route("/firstpurchase/savepurchase", methods=["POST"])
def save_purchase():
    bom_rid = request.json.get("bomRid")
    purchase_order_items = request.json.get("purchaseItems")
    purchase_order_rid = request.json.get("purchaseRid")
    total_bom_id = (
        db.session.query(TotalBom)
        .filter(TotalBom.total_bom_rid == bom_rid)
        .first()
        .total_bom_id
    )
    purchase_order = PurchaseOrder(
        purchase_order_rid=purchase_order_rid,
        bom_id=total_bom_id,
        purchase_order_issue_date=datetime.datetime.now().strftime("%Y%m%d"),
        purchase_order_type="F",
        purchase_order_status="1",
    )
    db.session.add(purchase_order)
    db.session.commit()
    purchase_order_id = (
        db.session.query(PurchaseOrder)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_rid)
        .first()
        .purchase_order_id
    )
    material_list_sorted = sorted(purchase_order_items, key=itemgetter("supplierName"))
    grouped_materials = {}
    for supplier_name, items in groupby(
        material_list_sorted, key=itemgetter("supplierName")
    ):
        grouped_materials[supplier_name] = list(items)
    print(grouped_materials)
    for supplier_name, items in grouped_materials.items():
        supplier_id = (
            db.session.query(Supplier)
            .filter(Supplier.supplier_name == supplier_name)
            .first()
            .supplier_id
        )
        supplier_id_str = str(supplier_id).zfill(4)

        purchase_divide_order_rid = purchase_order_rid + supplier_id_str
        purchase_divide_order = PurchaseDivideOrder(
            purchase_divide_order_rid=purchase_divide_order_rid,
            purchase_order_id=purchase_order_id,
            purchase_divide_order_type=(
                "N" if items[0]["materialCategory"] == 0 else "S"
            ),
            purchase_order_remark="",
            purchase_order_environmental_request="",
            shipment_address="温州市瓯海区梧田工业基地镇南路8号（健诚集团）",
            shipment_deadline="请在7-10日内交货",
        )
        db.session.add(purchase_divide_order)
        db.session.commit()
        purchase_divide_order_id = (
            db.session.query(PurchaseDivideOrder)
            .filter(
                PurchaseDivideOrder.purchase_divide_order_rid
                == purchase_divide_order_rid
            )
            .first()
            .purchase_divide_order_id
        )
        if items[0]["materialCategory"] == 0:
            for item in items:
                material_quantity = item["purchaseAmount"]
                purchase_order_item = PurchaseOrderItem(
                    purchase_divide_order_id=purchase_divide_order_id,
                    bom_item_id=item["bomItemId"],
                    purchase_amount=material_quantity,
                )
                db.session.add(purchase_order_item)
                db.session.commit()
        elif items[0]["materialCategory"] == 1:
            for item in items:
                material_35_quantity = item["sizeInfo"][0]["purchaseAmount"]
                material_36_quantity = item["sizeInfo"][1]["purchaseAmount"]
                material_37_quantity = item["sizeInfo"][2]["purchaseAmount"]
                material_38_quantity = item["sizeInfo"][3]["purchaseAmount"]
                material_39_quantity = item["sizeInfo"][4]["purchaseAmount"]
                material_40_quantity = item["sizeInfo"][5]["purchaseAmount"]
                material_41_quantity = item["sizeInfo"][6]["purchaseAmount"]
                material_42_quantity = item["sizeInfo"][7]["purchaseAmount"]
                material_43_quantity = item["sizeInfo"][8]["purchaseAmount"]
                material_44_quantity = item["sizeInfo"][9]["purchaseAmount"]
                material_45_quantity = item["sizeInfo"][10]["purchaseAmount"]
                material_quantity = (
                    material_35_quantity
                    + material_36_quantity
                    + material_37_quantity
                    + material_38_quantity
                    + material_39_quantity
                    + material_40_quantity
                    + material_41_quantity
                    + material_42_quantity
                    + material_43_quantity
                    + material_44_quantity
                    + material_45_quantity
                )
                purchase_order_item = PurchaseOrderItem(
                    purchase_divide_order_id=purchase_divide_order_id,
                    bom_item_id=item["bomItemId"],
                    purchase_amount=material_quantity,
                    size_35_purchase_amount=material_35_quantity,
                    size_36_purchase_amount=material_36_quantity,
                    size_37_purchase_amount=material_37_quantity,
                    size_38_purchase_amount=material_38_quantity,
                    size_39_purchase_amount=material_39_quantity,
                    size_40_purchase_amount=material_40_quantity,
                    size_41_purchase_amount=material_41_quantity,
                    size_42_purchase_amount=material_42_quantity,
                    size_43_purchase_amount=material_43_quantity,
                    size_44_purchase_amount=material_44_quantity,
                    size_45_purchase_amount=material_45_quantity,
                )
                db.session.add(purchase_order_item)
                db.session.commit()
    return jsonify({"status": "success"})


@first_purchase_bp.route("/firstpurchase/getpurchasedivideorders", methods=["GET"])
def get_purchase_divide_orders():
    purchase_order_id = request.args.get("purchaseOrderId")

    # Fetch the data from the database
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            PurchaseOrderItem,
            BomItem,
            Material,
            MaterialType,
            Supplier,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .join(
            PurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == PurchaseOrderItem.purchase_divide_order_id,
        )
        .join(BomItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id)
        .join(Material, BomItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )

    # Group the results by purchase_divide_order_rid
    grouped_results = {}
    for (
        purchase_divide_order,
        purchase_order,
        purchase_order_item,
        bom_item,
        material,
        material_type,
        supplier,
    ) in query:
        divide_order_rid = purchase_divide_order.purchase_divide_order_rid
        if divide_order_rid not in grouped_results:
            grouped_results[divide_order_rid] = {
                "purchaseDivideOrderId": divide_order_rid,
                "purchaseOrderId": purchase_divide_order.purchase_order_id,
                "supplierName": supplier.supplier_name,
                "assetsItems": [],
                "purchaseDivideOrderType": purchase_divide_order.purchase_divide_order_type,
                "remark": purchase_divide_order.purchase_order_remark,
                "evironmentalRequest": purchase_divide_order.purchase_order_environmental_request,
                "shipmentAddress": purchase_divide_order.shipment_address,
                "shipmentDeadline": purchase_divide_order.shipment_deadline,
            }

        # Append the assets item details to the corresponding group
        grouped_results[divide_order_rid]["assetsItems"].append(
            {
                "materialId": bom_item.material_id,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialModel": bom_item.material_model,
                "materialSpecification": bom_item.material_specification,
                "color": bom_item.bom_item_color,
                "unit": material.material_unit,
                "purchaseAmount": purchase_order_item.purchase_amount,
                "size35": purchase_order_item.size_35_purchase_amount,
                "size36": purchase_order_item.size_36_purchase_amount,
                "size37": purchase_order_item.size_37_purchase_amount,
                "size38": purchase_order_item.size_38_purchase_amount,
                "size39": purchase_order_item.size_39_purchase_amount,
                "size40": purchase_order_item.size_40_purchase_amount,
                "size41": purchase_order_item.size_41_purchase_amount,
                "size42": purchase_order_item.size_42_purchase_amount,
                "size43": purchase_order_item.size_43_purchase_amount,
                "size44": purchase_order_item.size_44_purchase_amount,
                "size45": purchase_order_item.size_45_purchase_amount,
                "remark": bom_item.remark,
                "sizeType": bom_item.size_type,
            }
        )

    # Convert the grouped results to a list
    result = list(grouped_results.values())

    return jsonify(result)


@first_purchase_bp.route("/firstpurchase/editpurchaseitems", methods=["POST"])
def edit_purchase_items():
    purchase_order_rid = request.json.get("purchaseOrderId")
    purchase_items = request.json.get("purchaseItems")
    print(purchase_items)
    for item in purchase_items:
        purchase_order_item = (
            db.session.query(PurchaseOrderItem)
            .filter(
                PurchaseOrderItem.purchase_order_item_id == item["purchaseOrderItemId"]
            )
            .first()
        )
        purchase_order_item.purchase_amount = item["purchaseAmount"]
        purchase_order_item.size_35_purchase_amount = item["sizeInfo"][0][
            "purchaseAmount"
        ]
        purchase_order_item.size_36_purchase_amount = item["sizeInfo"][1][
            "purchaseAmount"
        ]
        purchase_order_item.size_37_purchase_amount = item["sizeInfo"][2][
            "purchaseAmount"
        ]
        purchase_order_item.size_38_purchase_amount = item["sizeInfo"][3][
            "purchaseAmount"
        ]
        purchase_order_item.size_39_purchase_amount = item["sizeInfo"][4][
            "purchaseAmount"
        ]
        purchase_order_item.size_40_purchase_amount = item["sizeInfo"][5][
            "purchaseAmount"
        ]
        purchase_order_item.size_41_purchase_amount = item["sizeInfo"][6][
            "purchaseAmount"
        ]
        purchase_order_item.size_42_purchase_amount = item["sizeInfo"][7][
            "purchaseAmount"
        ]
        purchase_order_item.size_43_purchase_amount = item["sizeInfo"][8][
            "purchaseAmount"
        ]
        purchase_order_item.size_44_purchase_amount = item["sizeInfo"][9][
            "purchaseAmount"
        ]
        purchase_order_item.size_45_purchase_amount = item["sizeInfo"][10][
            "purchaseAmount"
        ]
        db.session.commit()
    return jsonify({"status": "success"})


@first_purchase_bp.route("/firstpurchase/savepurchasedivideorders", methods=["POST"])
def save_purchase_divide_orders():
    purchase_divide_orders = request.json.get("purchaseDivideOrders")
    for order in purchase_divide_orders:
        purchase_divide_order = (
            db.session.query(PurchaseDivideOrder)
            .filter(
                PurchaseDivideOrder.purchase_divide_order_rid
                == order["purchaseDivideOrderId"]
            )
            .first()
        )
        purchase_divide_order.purchase_order_remark = order["remark"]
        purchase_divide_order.purchase_order_environmental_request = order[
            "evironmentalRequest"
        ]
        purchase_divide_order.shipment_address = order["shipmentAddress"]
        purchase_divide_order.shipment_deadline = order["shipmentDeadline"]
        db.session.commit()
    return jsonify({"status": "success"})


@first_purchase_bp.route("/firstpurchase/submitpurchasedivideorders", methods=["POST"])
def submit_purchase_divide_orders():
    purchase_order_id = request.json.get("purchaseOrderId")
    order_info = (
        db.session.query(PurchaseOrder, TotalBom, OrderShoe, Order, Shoe)
        .join(TotalBom, TotalBom.total_bom_id == PurchaseOrder.bom_id)
        .join(OrderShoe, OrderShoe.order_shoe_id == TotalBom.order_shoe_id)
        .join(Order, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .first()
    )
    order_id = order_info.Order.order_id
    order_shoe_id = order_info.OrderShoe.order_shoe_id
    order_rid = order_info.Order.order_rid
    order_shoe_rid = order_info.Shoe.shoe_rid
    materials_data = []
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            PurchaseOrderItem,
            BomItem,
            Material,
            MaterialType,
            Supplier,
        )
        .join(
            PurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == PurchaseOrderItem.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .join(BomItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id)
        .join(Material, BomItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )
    for (
        purchase_divide_order,
        purchase_order,
        purchase_order_item,
        bom_item,
        material,
        material_type,
        supplier,
    ) in query:
        materials_data.append(
            {
                "supplier_name": supplier.supplier_name,
                "material_name": material.material_name,
                "model": bom_item.material_model or "",
                "specification": bom_item.material_specification or "",
                "approval_amount": bom_item.total_usage,  # Assuming bom_item has approval quantity
                "purchase_amount": purchase_order_item.purchase_amount,
            }
        )

        material_id = bom_item.material_id
        material_quantity = purchase_order_item.purchase_amount
        material_specification = bom_item.material_specification
        color = bom_item.bom_item_color
        remark = bom_item.remark
        size_type = bom_item.size_type
        if purchase_divide_order.purchase_divide_order_type == "N":
            material_storage = MaterialStorage(
                order_shoe_id=order_shoe_id,
                material_id=material_id,
                estimated_inbound_amount=material_quantity,
                actual_inbound_amount=0,
                current_amount=0,
                unit_price=0,
                material_outsource_status="0",
                material_specification=material_specification,
                material_storage_color=color,
                purchase_divide_order_id=purchase_divide_order.purchase_divide_order_id,
            )
            db.session.add(material_storage)
            db.session.commit()
        elif purchase_divide_order.purchase_divide_order_type == "S":
            size_35_quantity = purchase_order_item.size_35_purchase_amount
            size_36_quantity = purchase_order_item.size_36_purchase_amount
            size_37_quantity = purchase_order_item.size_37_purchase_amount
            size_38_quantity = purchase_order_item.size_38_purchase_amount
            size_39_quantity = purchase_order_item.size_39_purchase_amount
            size_40_quantity = purchase_order_item.size_40_purchase_amount
            size_41_quantity = purchase_order_item.size_41_purchase_amount
            size_42_quantity = purchase_order_item.size_42_purchase_amount
            size_43_quantity = purchase_order_item.size_43_purchase_amount
            size_44_quantity = purchase_order_item.size_44_purchase_amount
            size_45_quantity = purchase_order_item.size_45_purchase_amount

            size_material_storage = SizeMaterialStorage(
                order_shoe_id=order_shoe_id,
                material_id=material_id,
                total_estimated_inbound_amount=material_quantity,
                size_34_estimated_inbound_amount=0,
                size_35_estimated_inbound_amount=size_35_quantity,
                size_36_estimated_inbound_amount=size_36_quantity,
                size_37_estimated_inbound_amount=size_37_quantity,
                size_38_estimated_inbound_amount=size_38_quantity,
                size_39_estimated_inbound_amount=size_39_quantity,
                size_40_estimated_inbound_amount=size_40_quantity,
                size_41_estimated_inbound_amount=size_41_quantity,
                size_42_estimated_inbound_amount=size_42_quantity,
                size_43_estimated_inbound_amount=size_43_quantity,
                size_44_estimated_inbound_amount=size_44_quantity,
                size_45_estimated_inbound_amount=size_45_quantity,
                size_46_estimated_inbound_amount=0,
                total_actual_inbound_amount=0,
                size_34_actual_inbound_amount=0,
                size_35_actual_inbound_amount=0,
                size_36_actual_inbound_amount=0,
                size_37_actual_inbound_amount=0,
                size_38_actual_inbound_amount=0,
                size_39_actual_inbound_amount=0,
                size_40_actual_inbound_amount=0,
                size_41_actual_inbound_amount=0,
                size_42_actual_inbound_amount=0,
                size_43_actual_inbound_amount=0,
                size_44_actual_inbound_amount=0,
                size_45_actual_inbound_amount=0,
                size_46_actual_inbound_amount=0,
                total_current_amount=0,
                size_34_current_amount=0,
                size_35_current_amount=0,
                size_36_current_amount=0,
                size_37_current_amount=0,
                size_38_current_amount=0,
                size_39_current_amount=0,
                size_40_current_amount=0,
                size_41_current_amount=0,
                size_42_current_amount=0,
                size_43_current_amount=0,
                size_44_current_amount=0,
                size_45_current_amount=0,
                size_46_current_amount=0,
                unit_price=0,
                material_outsource_status="0",
                size_material_specification=material_specification,
                size_material_color=color,
                purchase_divide_order_id=purchase_divide_order.purchase_divide_order_id,
                size_storage_type="E",
            )
            db.session.add(size_material_storage)
    db.session.commit()
    purchase_order = (
        db.session.query(PurchaseOrder)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .first()
    )
    purchase_order_status = "2"
    db.session.query(PurchaseOrder).filter(
        PurchaseOrder.purchase_order_rid == purchase_order_id
    ).update({"purchase_order_status": purchase_order_status})
    db.session.commit()
    purchase_divide_orders = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrderItem,
            PurchaseOrder,
            BomItem,
            Material,
            Supplier,
        )
        .join(
            PurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == PurchaseOrderItem.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .join(BomItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id)
        .join(Material, BomItem.material_id == Material.material_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )

    # Dictionary to keep track of processed PurchaseDivideOrders
    purchase_divide_order_dict = {}
    size_purchase_divide_order_dict = {}
    if (
        os.path.exists(
            os.path.join(FILE_STORAGE_PATH, order_rid, order_shoe_rid, "purchase_order")
        )
        == False
    ):
        os.mkdir(
            os.path.join(FILE_STORAGE_PATH, order_rid, order_shoe_rid, "purchase_order")
        )

    # Iterate through the query results and group items by PurchaseDivideOrder
    for (
        purchase_divide_order,
        purchase_order_item,
        purchase_order,
        bom_item,
        material,
        supplier,
    ) in purchase_divide_orders:
        purchase_order_id = purchase_divide_order.purchase_divide_order_rid
        print(purchase_order_id)
        if purchase_divide_order.purchase_divide_order_type == "N":
            if purchase_order_id not in purchase_divide_order_dict:
                purchase_divide_order_dict[purchase_order_id] = {
                    "供应商": supplier.supplier_name,
                    "日期": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "备注": purchase_divide_order.purchase_order_remark,
                    "环保要求": purchase_divide_order.purchase_order_environmental_request,
                    "发货地址": purchase_divide_order.shipment_address,
                    "交货期限": purchase_divide_order.shipment_deadline,
                    "订单信息": order_rid + "-" + order_shoe_rid,
                    "seriesData": [],
                }

            # Append the current PurchaseOrderItem to the 'seriesData' list of the relevant order
            purchase_divide_order_dict[purchase_order_id]["seriesData"].append(
                {
                    "物品名称": (
                        material.material_name
                        + " "
                        + (bom_item.material_model if bom_item.material_model else "")
                        + " "
                        + (
                            bom_item.material_specification
                            if bom_item.material_specification
                            else ""
                        )
                        + " "
                        + (bom_item.bom_item_color if bom_item.bom_item_color else "")
                    ),
                    "数量": purchase_order_item.purchase_amount,
                    "单位": material.material_unit,
                    "备注": bom_item.remark,
                    "用途说明": "",
                }
            )
        elif purchase_divide_order.purchase_divide_order_type == "S":
            if purchase_order_id not in size_purchase_divide_order_dict:
                size_purchase_divide_order_dict[purchase_order_id] = {
                    "供应商": supplier.supplier_name,
                    "日期": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "备注": purchase_divide_order.purchase_order_remark,
                    "环保要求": purchase_divide_order.purchase_order_environmental_request,
                    "发货地址": purchase_divide_order.shipment_address,
                    "交货期限": purchase_divide_order.shipment_deadline,
                    "订单信息": order_rid + "-" + order_shoe_rid,
                    "seriesData": [],
                }

            # Append the current PurchaseOrderItem to the 'seriesData' list of the relevant order
            size_purchase_divide_order_dict[purchase_order_id]["seriesData"].append(
                {
                    "物品名称": (
                        material.material_name
                        + " "
                        + (bom_item.material_model if bom_item.material_model else "")
                        + " "
                        + (
                            bom_item.material_specification
                            if bom_item.material_specification
                            else ""
                        )
                        + " "
                        + (bom_item.bom_item_color if bom_item.bom_item_color else "")
                    ),
                    "34": purchase_order_item.size_34_purchase_amount,
                    "35": purchase_order_item.size_35_purchase_amount,
                    "36": purchase_order_item.size_36_purchase_amount,
                    "37": purchase_order_item.size_37_purchase_amount,
                    "38": purchase_order_item.size_38_purchase_amount,
                    "39": purchase_order_item.size_39_purchase_amount,
                    "40": purchase_order_item.size_40_purchase_amount,
                    "41": purchase_order_item.size_41_purchase_amount,
                    "42": purchase_order_item.size_42_purchase_amount,
                    "43": purchase_order_item.size_43_purchase_amount,
                    "44": purchase_order_item.size_44_purchase_amount,
                    "45": purchase_order_item.size_45_purchase_amount,
                    "46": purchase_order_item.size_46_purchase_amount,
                    "单位": material.material_unit,
                    "备注": bom_item.remark,
                    "用途说明": "",
                }
            )
    customer_name = (
        db.session.query(Order, Customer)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .filter(Order.order_id == order_id)
        .first()
        .Customer.customer_name
    )
    template_path = os.path.join(FILE_STORAGE_PATH, "材料统计表模板.xlsx")

    materials_output_path = os.path.join(
        FILE_STORAGE_PATH,
        order_rid,
        order_shoe_rid,
        "purchase_order",
        "材料统计表.xlsx",
    )

    generate_material_statistics_file(
        template_path=template_path,
        save_path=materials_output_path,
        order_rid=order_rid,
        order_shoe_rid=order_shoe_rid,
        customer_name=customer_name,
        materials_data=materials_data,
    )
    generated_files = []
    # Convert the dictionary to a list
    template_path = os.path.join(FILE_STORAGE_PATH, "标准采购订单.xlsx")
    size_template_path = os.path.join(FILE_STORAGE_PATH, "标准采购订单尺码版.xlsx")
    for purchase_order_id, data in purchase_divide_order_dict.items():
        new_file_path = os.path.join(
            FILE_STORAGE_PATH,
            order_rid,
            order_shoe_rid,
            "purchase_order",
            purchase_order_id + "_" + data["供应商"] + ".xlsx",
        )
        print(new_file_path)
        print(template_path)
        generate_excel_file(template_path, new_file_path, data)
        generated_files.append(new_file_path)
        print(data)
    for purchase_order_id, data in size_purchase_divide_order_dict.items():
        new_file_path = os.path.join(
            FILE_STORAGE_PATH,
            order_rid,
            order_shoe_rid,
            "purchase_order",
            purchase_order_id + "_" + data["供应商"] + ".xlsx",
        )
        generate_size_excel_file(size_template_path, new_file_path, data)
        generated_files.append(new_file_path)
    zip_file_path = os.path.join(
        FILE_STORAGE_PATH,
        order_rid,
        order_shoe_rid,
        "purchase_order",
        "一次采购订单.zip",
    )
    with zipfile.ZipFile(zip_file_path, "w") as zipf:
        for file in generated_files:
            # Extract purchase_order_id from the filename and check if it ends with 'F'
            filename = os.path.basename(file)
            purchase_order_id = filename.split("_")[0]  # Get the part before "_供应商"
            if len(purchase_order_id) >= 5 and purchase_order_id[-5] == "F":
                zipf.write(file, filename)  # Add the file to the zip

    processor = EventProcessor()
    event = Event(
        staff_id=1,
        handle_time=datetime.datetime.now(),
        operation_id=50,
        event_order_id=order_id,
        event_order_shoe_id=order_shoe_id,
    )
    result = processor.processEvent(event)
    if not result:
        return jsonify({"status": "error"})
    db.session.add(event)
    db.session.commit()
    processor = EventProcessor()
    event = Event(
        staff_id=1,
        handle_time=datetime.datetime.now(),
        operation_id=51,
        event_order_id=order_id,
        event_order_shoe_id=order_shoe_id,
    )
    result = processor.processEvent(event)
    if not result:
        return jsonify({"status": "error"})
    db.session.add(event)
    db.session.commit()
    processor = EventProcessor()
    event = Event(
        staff_id=1,
        handle_time=datetime.datetime.now(),
        operation_id=52,
        event_order_id=order_id,
        event_order_shoe_id=order_shoe_id,
    )
    result = processor.processEvent(event)
    if not result:
        return jsonify({"status": "error"})
    db.session.add(event)
    db.session.commit()
    processor = EventProcessor()
    event = Event(
        staff_id=1,
        handle_time=datetime.datetime.now(),
        operation_id=53,
        event_order_id=order_id,
        event_order_shoe_id=order_shoe_id,
    )
    result = processor.processEvent(event)
    if not result:
        return jsonify({"status": "error"})
    db.session.add(event)
    db.session.commit()

    return jsonify({"status": "success"})


@first_purchase_bp.route("/firstpurchase/downloadpurchaseorderzip", methods=["GET"])
def download_purchase_order_zip():
    order_rid = request.args.get("orderrid")
    order_shoe_rid = request.args.get("ordershoerid")
    zip_file_path = os.path.join(
        FILE_STORAGE_PATH,
        order_rid,
        order_shoe_rid,
        "purchase_order",
        "一次采购订单.zip",
    )
    new_name = order_rid + "_" + order_shoe_rid + "_一次采购订单.zip"
    return send_file(zip_file_path, as_attachment=True, download_name=new_name)

@first_purchase_bp.route("/firstpurchase/downloadmaterialstatistics", methods=["GET"])
def download_material_statistics():
    order_rid = request.args.get("orderrid")
    order_shoe_rid = request.args.get("ordershoerid")
    file_path = os.path.join(
        FILE_STORAGE_PATH,
        order_rid,
        order_shoe_rid,
        "purchase_order",
        "材料统计表.xlsx",
    )
    new_name = order_rid + "_" + order_shoe_rid + "_材料统计表.xlsx"
    return send_file(file_path, as_attachment=True, download_name=new_name)
