from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert
import datetime
from app_config import app, db
from models import *
from api_utility import randomIdGenerater
from event_processor import EventProcessor
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH
from itertools import groupby
from operator import itemgetter
from general_document.purchase_divide_order import generate_excel_file
import os
import zipfile

first_purchase_bp = Blueprint("first_purrchase_bp", __name__)


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


@first_purchase_bp.route("/firstpurchase/getshoebomitems", methods=["GET"])
def get_shoe_bom_items():
    bom_rid = request.args.get("bomrid")
    entities = (
        db.session.query(
            Bom, BomItem, Material, MaterialType, Supplier, Color, PurchaseOrderItem
        )
        .join(BomItem, BomItem.bom_id == Bom.bom_id)
        .join(Material, Material.material_id == BomItem.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(Color, Color.color_id == BomItem.bom_item_color)
        .outerjoin(
            PurchaseOrderItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id
        )
        .filter(Bom.bom_rid == bom_rid)
        .all()
    )
    result = []
    for entity in entities:
        bom, bom_item, material, material_type, supplier, color, purchase_order_item = (
            entity
        )
        sizeInfo = [
            {
                "size": "35",
                "innerSize": "7",
                "outterSize": "7",
                "approvalAmount": (
                    bom_item.size_35_total_usage
                    if bom_item.size_35_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_35_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "36",
                "innerSize": "7",
                "outterSize": "7.5",
                "approvalAmount": (
                    bom_item.size_36_total_usage
                    if bom_item.size_36_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_36_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "37",
                "innerSize": "8",
                "outterSize": "8",
                "approvalAmount": (
                    bom_item.size_37_total_usage
                    if bom_item.size_37_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_37_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "38",
                "innerSize": "8",
                "outterSize": "8.5",
                "approvalAmount": (
                    bom_item.size_38_total_usage
                    if bom_item.size_38_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_38_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "39",
                "innerSize": "9",
                "outterSize": "9",
                "approvalAmount": (
                    bom_item.size_39_total_usage
                    if bom_item.size_39_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_39_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "40",
                "innerSize": "9",
                "outterSize": "9.5",
                "approvalAmount": (
                    bom_item.size_40_total_usage
                    if bom_item.size_40_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_40_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "41",
                "innerSize": "10",
                "outterSize": "10",
                "approvalAmount": (
                    bom_item.size_41_total_usage
                    if bom_item.size_41_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_41_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "42",
                "innerSize": "10",
                "outterSize": "10.5",
                "approvalAmount": (
                    bom_item.size_42_total_usage
                    if bom_item.size_42_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_42_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "43",
                "innerSize": "11",
                "outterSize": "11",
                "approvalAmount": (
                    bom_item.size_43_total_usage
                    if bom_item.size_43_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_43_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "44",
                "innerSize": "12",
                "outterSize": "12",
                "approvalAmount": (
                    bom_item.size_44_total_usage
                    if bom_item.size_44_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_44_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
            {
                "size": "45",
                "innerSize": "13",
                "outterSize": "13",
                "approvalAmount": (
                    bom_item.size_45_total_usage
                    if bom_item.size_45_total_usage
                    else 0.00
                ),
                "purchaseAmount": (
                    purchase_order_item.size_45_purchase_amount
                    if purchase_order_item
                    else 0.00
                ),
            },
        ]

        result.append(
            {
                "purchaseOrderItemId": purchase_order_item.purchase_order_item_id if purchase_order_item else "",
                "bomItemId": bom_item.bom_item_id,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialSpecification": bom_item.material_specification,
                "color": color.color_id if color else "",
                "unit": material.material_unit,
                "unitUsage": (
                    bom_item.unit_usage
                    if bom_item.unit_usage
                    else 0.00 if material.material_category == 0 else None
                ),
                "approvalUsage": bom_item.total_usage if bom_item.total_usage else 0.00,
                "useDepart": bom_item.department_id,
                "purchaseAmount": (
                    purchase_order_item.purchase_amount if purchase_order_item else 0.00
                ),
                "supplierName": supplier.supplier_name,
                "materialCategory": material.material_category,
                "remark": bom_item.remark,
                "sizeInfo": sizeInfo,
            }
        )
    return jsonify(result)


@first_purchase_bp.route("/firstpurchase/savepurchase", methods=["POST"])
def save_purchase():
    bom_rid = request.json.get("bomRid")
    purchase_order_items = request.json.get("purchaseItems")
    purchase_order_rid = request.json.get("purchaseRid")
    bom_id = db.session.query(Bom).filter(Bom.bom_rid == bom_rid).first().bom_id
    purchase_order = PurchaseOrder(
        purchase_order_rid=purchase_order_rid,
        bom_id=bom_id,
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
            Color,
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
        .join(Color, BomItem.bom_item_color == Color.color_id)
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
        color,
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
                "materialSpecification": bom_item.material_specification,
                "color": color.color_name,
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
        db.session.query(PurchaseOrder, Bom, OrderShoe, Order, Shoe)
        .join(Bom, Bom.bom_id == PurchaseOrder.bom_id)
        .join(OrderShoe, OrderShoe.order_shoe_id == Bom.order_shoe_id)
        .join(Order, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .first()
    )
    order_id = order_info.Order.order_id
    order_shoe_id = order_info.OrderShoe.order_shoe_id
    order_rid = order_info.Order.order_rid
    order_shoe_rid = order_info.Shoe.shoe_rid
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            PurchaseOrderItem,
            BomItem,
            Material,
            MaterialType,
            Supplier,
            Color,
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
        .join(Color, BomItem.bom_item_color == Color.color_id)
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
        color,
    ) in query:
        material_id = bom_item.material_id
        material_quantity = purchase_order_item.purchase_amount
        material_specification = bom_item.material_specification
        color = bom_item.bom_item_color
        remark = bom_item.remark
        size_type = bom_item.size_type
        if purchase_divide_order.purchase_divide_order_type == "N":
            material_storage = MaterialStorage(
                material_id=material_id,
                estimated_inbound_amount=material_quantity,
                actual_inbound_amount=0,
                current_amount=0,
                unit_price=0,
                material_outsource_status="0",
                material_specification=material_specification,
                material_storage_color=color,
                purchase_divide_order_id=purchase_divide_order.purchase_divide_order_id,
                order_shoe_id=order_shoe_id,
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
                order_shoe_id=order_shoe_id,
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
        db.session.query(PurchaseDivideOrder, PurchaseOrderItem, PurchaseOrder, BomItem, Material, Supplier, Color)
        .join(
            PurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == PurchaseOrderItem.purchase_divide_order_id,
        )
        .join(PurchaseOrder, PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id)
        .join(BomItem, PurchaseOrderItem.bom_item_id == BomItem.bom_item_id)
        .join(Material, BomItem.material_id == Material.material_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .join(Color, BomItem.bom_item_color == Color.color_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )

    # Dictionary to keep track of processed PurchaseDivideOrders
    purchase_divide_order_dict = {}
    if os.path.exists(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "purchase_order")) == False:
        os.mkdir(os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "purchase_order"))

    # Iterate through the query results and group items by PurchaseDivideOrder
    for purchase_divide_order, purchase_order_item, purchase_order ,bom_item, material, supplier, color in purchase_divide_orders:
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
                    "seriesData": []
                }

            # Append the current PurchaseOrderItem to the 'seriesData' list of the relevant order
            purchase_divide_order_dict[purchase_order_id]["seriesData"].append({
                "物品名称": material.material_name + " " + bom_item.material_specification + " " + color.color_name,
                "数量": purchase_order_item.purchase_amount,
                "单位": material.material_unit,
                "备注": bom_item.remark,
                "用途说明": "",


            })
    

    # Convert the dictionary to a list
    template_path = os.path.join(FILE_STORAGE_PATH,"标准采购订单.xlsx")
    for purchase_order_id, data in purchase_divide_order_dict.items():
        new_file_path = os.path.join(FILE_STORAGE_PATH,order_rid, order_shoe_rid, "purchase_order", purchase_order_id + "_" + data["供应商"] + ".xlsx")
        print(new_file_path)
        print(template_path)
        generate_excel_file(template_path, new_file_path, data)      
        print(data)



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
