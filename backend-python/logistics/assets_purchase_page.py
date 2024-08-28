from flask import Blueprint, jsonify, request
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from app_config import app, db
from api_utility import randomIdGenerater
import datetime
from itertools import groupby
from operator import itemgetter
from models import *

assets_purchase_page_bp = Blueprint("assets_purchase_page_bp", __name__)


@assets_purchase_page_bp.route(
    "/logistics/assetsmaterialpurchaseorder", methods=["GET"]
)
def get_assets_material_purchase_order():
    purchase_order_status = str(request.args.get("purchaseorderstatus"))
    print(purchase_order_status)
    query = (
        db.session.query(PurchaseOrder, Order)
        .outerjoin(Order, PurchaseOrder.order_id == Order.order_id)
        .filter(
            or_(
                PurchaseOrder.purchase_order_type == "G",
                PurchaseOrder.purchase_order_type == "O",
            )
        )
        .filter(PurchaseOrder.purchase_order_status == purchase_order_status)
    )

    response = query.all()
    print(response)

    result = []

    for row in response:
        order_type = ""
        if row.PurchaseOrder.purchase_order_type == "G":
            order_type = "独立采购"

        elif row.PurchaseOrder.purchase_order_type == "O":
            order_type = "随订单采购"
        result.append(
            {
                "materialPurchaseOrderId": row.PurchaseOrder.purchase_order_rid,
                "createDate": row.PurchaseOrder.purchase_order_issue_date.isoformat(),
                "orderType": order_type,
                "orderId": row.Order.order_rid if row.Order else None,
            }
        )

    return jsonify(result)


@assets_purchase_page_bp.route(
    "/logistics/getassetsnewpurchaseorderid", methods=["POST"]
)
def get_assets_new_purchase_order_id():
    department = request.json.get("department")
    print(department)
    current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    new_id = department + current_time_stamp + random_string
    return jsonify({"newId": new_id})


@assets_purchase_page_bp.route("/logistics/getmaterialtypeandname", methods=["GET"])
def get_material_type_and_name():
    material_type = request.args.get("materialtype")
    material_name = request.args.get("materialname")
    supplier_name = request.args.get("suppliername")
    material_category = request.args.get("materialcategory")
    print(material_type, material_name, supplier_name)
    query = (
        db.session.query(Material, MaterialType, MaterialWarehouse, Supplier)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(
            MaterialWarehouse,
            MaterialType.warehouse_id == MaterialWarehouse.material_warehouse_id,
        )
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .filter(MaterialType.material_category == material_category)
    )
    if material_type:
        query = query.filter(MaterialType.material_type_name.like(f"%{material_type}%"))
    if material_name:
        query = query.filter(Material.material_name.like(f"%{material_name}%"))
    if supplier_name:
        query = query.filter(Supplier.supplier_name.like(f"%{supplier_name}%"))
    result = []
    for row in query:
        result.append(
            {
                "materialType": row.MaterialType.material_type_name,
                "materialName": row.Material.material_name,
                "warehouseName": row.MaterialWarehouse.material_warehouse_name,
                "unit": row.Material.material_unit,
                "supplierName": row.Supplier.supplier_name
            }
        )
    return jsonify(result)


@assets_purchase_page_bp.route("/logistics/newpurchaseordersave", methods=["POST"])
def new_purchase_order_save():
    try:
        purchase_order_id = request.json.get("purchaseOrderId")
        material_list = request.json.get("data")
        purchase_order_type = material_list[0]["isPurchaseOrder"]
        purchase_divide_order_type = request.json.get("purchaseDivideOrderType")
        purchase_order_rid = purchase_order_id + purchase_order_type
        purchase_order_issue_date = datetime.datetime.now().strftime("%Y%m%d")
        order_id = material_list[0]["orderId"] if material_list[0]["orderId"]!="" else None
        purchase_order_status = "0"
        print(purchase_order_id, material_list)
        material_list_sorted = sorted(material_list, key=itemgetter('supplierName'))

        # Group the list by 'supplierName'
        grouped_materials = {}
        for supplier_name, items in groupby(material_list_sorted, key=itemgetter('supplierName')):
            grouped_materials[supplier_name] = list(items)
        print(grouped_materials)

        purchase_order = PurchaseOrder(
            purchase_order_rid=purchase_order_rid,
            purchase_order_type=purchase_order_type,
            purchase_order_issue_date=purchase_order_issue_date,
            order_id=order_id,
            purchase_order_status=purchase_order_status,
        )
        db.session.add(purchase_order)
        db.session.commit()
        purchase_order_id = db.session.query(PurchaseOrder).filter(PurchaseOrder.purchase_order_rid == purchase_order_rid).first().purchase_order_id

        for supplier_name, items in grouped_materials.items():
            supplier_id = db.session.query(Supplier).filter(Supplier.supplier_name == supplier_name).first().supplier_id
            supplier_id_str = str(supplier_id).zfill(4)

            purchase_divide_order_rid = purchase_order_rid + supplier_id_str
            purchase_divide_order = PurchaseDivideOrder(
                purchase_divide_order_rid=purchase_divide_order_rid,
                purchase_order_id=purchase_order_id,
                purchase_divide_order_type = purchase_divide_order_type,
            )
            db.session.add(purchase_divide_order)
            db.session.commit()
            purchase_divide_order_id = db.session.query(PurchaseDivideOrder).filter(PurchaseDivideOrder.purchase_divide_order_rid == purchase_divide_order_rid).first().purchase_divide_order_id
            for item in items:
                material_name = item["materialName"]
                material_info = db.session.query(Material, Supplier).join(
                    Supplier, Material.material_supplier == Supplier.supplier_id
                ).filter(Material.material_name == material_name, Supplier.supplier_name == supplier_name).first()
                print(material_info)
                material_id = material_info.Material.material_id
                material_quantity = item["purchaseAmount"]
                material_specification = item["materialSpecification"]
                color = item["color"]
                remark = item["comment"]
                assets_item = AssetsPurchaseOrderItem(
                    purchase_divide_order_id=purchase_divide_order_id,
                    material_id=material_id,
                    purchase_amount=material_quantity,
                    material_specification=material_specification,
                    color=color,
                    remark=remark,
                    size_type="N",
                )
                db.session.add(assets_item)
                db.session.commit()




        return jsonify({"status": "success"})
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback the session to undo changes
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.session.close()  # Close the session to free up resources

@assets_purchase_page_bp.route("/logistics/getassetspurchasedivideorders", methods=["GET"])
def get_purchase_divide_orders():
    purchase_order_id = request.args.get("purchaseOrderId")
    
    # Fetch the data from the database
    query = db.session.query(PurchaseDivideOrder, PurchaseOrder, AssetsPurchaseOrderItem, Material, MaterialType, Supplier).join(
        AssetsPurchaseOrderItem, PurchaseDivideOrder.purchase_divide_order_id == AssetsPurchaseOrderItem.purchase_divide_order_id
    ).join(
        PurchaseOrder, PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id
    ).join(
        Material, AssetsPurchaseOrderItem.material_id == Material.material_id
    ).join(
        MaterialType, Material.material_type_id == MaterialType.material_type_id
    ).join(
        Supplier, Material.material_supplier == Supplier.supplier_id
    ).filter(PurchaseOrder.purchase_order_rid == purchase_order_id).all()

    # Group the results by purchase_divide_order_rid
    grouped_results = {}
    for purchase_divide_order, purchase_order, assets_item, material, material_type, supplier in query:
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
        grouped_results[divide_order_rid]["assetsItems"].append({
            "materialId": assets_item.material_id,
            "materialType": material_type.material_type_name,
            "materialName" : material.material_name,
            "materialSpecification": assets_item.material_specification,
            "color": assets_item.color,
            "unit": material.material_unit,
            "purchaseAmount": assets_item.purchase_amount,
            "remark": assets_item.remark,
            "sizeType": assets_item.size_type,
        })

    # Convert the grouped results to a list
    result = list(grouped_results.values())

    return jsonify(result)
