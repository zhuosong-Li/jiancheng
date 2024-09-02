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
    )
    if material_type:
        query = query.filter(MaterialType.material_type_name.like(f"%{material_type}%"))
    if material_name:
        query = query.filter(Material.material_name.like(f"%{material_name}%"))
    if supplier_name:
        query = query.filter(Supplier.supplier_name.like(f"%{supplier_name}%"))
    if material_category:
        query = query.filter(MaterialType.material_type_category == material_category)
    result = []
    for row in query:
        result.append(
            {
                "materialType": row.MaterialType.material_type_name,
                "materialName": row.Material.material_name,
                "warehouseName": row.MaterialWarehouse.material_warehouse_name,
                "unit": row.Material.material_unit,
                "supplierName": row.Supplier.supplier_name,
                "materialCategory": row.MaterialType.material_category,
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
        order_id = (
            material_list[0]["orderId"] if material_list[0]["orderId"] != "" else None
        )
        purchase_order_status = "0"
        print(purchase_order_id, material_list)
        material_list_sorted = sorted(material_list, key=itemgetter("supplierName"))

        # Group the list by 'supplierName'
        grouped_materials = {}
        for supplier_name, items in groupby(
            material_list_sorted, key=itemgetter("supplierName")
        ):
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
        purchase_order_id = (
            db.session.query(PurchaseOrder)
            .filter(PurchaseOrder.purchase_order_rid == purchase_order_rid)
            .first()
            .purchase_order_id
        )

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
                purchase_divide_order_type=purchase_divide_order_type,
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
            if purchase_divide_order_type == "N":
                for item in items:
                    material_name = item["materialName"]
                    material_info = (
                        db.session.query(Material, Supplier)
                        .join(
                            Supplier, Material.material_supplier == Supplier.supplier_id
                        )
                        .filter(
                            Material.material_name == material_name,
                            Supplier.supplier_name == supplier_name,
                        )
                        .first()
                    )
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
            elif purchase_divide_order_type == "S":
                for item in items:
                    material_name = item["materialName"]
                    material_info = (
                        db.session.query(Material, Supplier)
                        .join(
                            Supplier, Material.material_supplier == Supplier.supplier_id
                        )
                        .filter(
                            Material.material_name == material_name,
                            Supplier.supplier_name == supplier_name,
                        )
                        .first()
                    )
                    print(material_info)
                    material_id = material_info.Material.material_id
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
                    material_specification = item["materialSpecification"]
                    color = item["color"]
                    remark = item["comment"]
                    assets_item = AssetsPurchaseOrderItem(
                        purchase_divide_order_id=purchase_divide_order_id,
                        material_id=material_id,
                        purchase_amount=material_quantity,
                        size_35_purchase_amount = material_35_quantity,
                        size_36_purchase_amount = material_36_quantity,
                        size_37_purchase_amount = material_37_quantity,
                        size_38_purchase_amount = material_38_quantity,
                        size_39_purchase_amount = material_39_quantity,
                        size_40_purchase_amount = material_40_quantity,
                        size_41_purchase_amount = material_41_quantity,
                        size_42_purchase_amount = material_42_quantity,
                        size_43_purchase_amount = material_43_quantity,
                        size_44_purchase_amount = material_44_quantity,
                        size_45_purchase_amount = material_45_quantity,
                        material_specification=material_specification,
                        color=color,
                        remark=remark,
                        size_type="E",
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

@assets_purchase_page_bp.route(
    "/logistics/getassetspurchaseorderitems", methods=["GET"]
)
def get_assets_purchase_order_items():
    purchase_order_id = request.args.get("purchaseOrderId")

    # Fetch the data from the database
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            Order,
            AssetsPurchaseOrderItem,
            Material,
            MaterialType,
            MaterialWarehouse,
            Supplier,
            Color,
        )
        .join(
            AssetsPurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == AssetsPurchaseOrderItem.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .outerjoin(Order, PurchaseOrder.order_id == Order.order_id)
        .join(Material, AssetsPurchaseOrderItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(MaterialWarehouse, MaterialType.warehouse_id == MaterialWarehouse.material_warehouse_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .join(Color, AssetsPurchaseOrderItem.color == Color.color_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )

    # Group the results by purchase_divide_order_rid
    for (
        purchase_divide_order,
        purchase_order,
        order,
        assets_item,
        material,
        material_type,
        material_warehouse,
        supplier,
        color,
    ) in query:
        result = []
        purchase_divide_order_type = purchase_divide_order.purchase_divide_order_type
        if purchase_divide_order_type == "N":
            result.append({
                "purchaseDivideOrderId": purchase_divide_order.purchase_divide_order_rid,
                "purchaseOrderId": purchase_divide_order.purchase_order_id,
                "supplierName": supplier.supplier_name,
                "warehouseName": material_warehouse.material_warehouse_name,
                "isPurchaseOrder": purchase_order.purchase_order_type,
                "orderId": order.order_rid if order else None,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialSpecification": assets_item.material_specification,
                "color": color.color_id,
                "unit": material.material_unit,
                "purchaseAmount": assets_item.purchase_amount,
                "comment": assets_item.remark if assets_item.remark else '',
            })
        elif purchase_divide_order_type == "S":
            result.append({
                "purchaseDivideOrderId": purchase_divide_order.purchase_divide_order_rid,
                "purchaseOrderId": purchase_divide_order.purchase_order_id,
                "supplierName": supplier.supplier_name,
                "warehouseName": material_warehouse.material_warehouse_name,
                "isPurchaseOrder": purchase_order.purchase_order_type,
                "orderId": order.order_rid if order else '',
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialSpecification": assets_item.material_specification,
                "color": color.color_id,
                "unit": material.material_unit,
                "comment": assets_item.remark if assets_item.remark else '',
                "sizeInfo": [
                    {
                        "size": "35",
                        "innerSize": "7",
                        "outterSize": "7",
                        "purchaseAmount": assets_item.size_35_purchase_amount,
                    },
                    {
                        "size": "36",
                        "innerSize": "7",
                        "outterSize": "7.5",
                        "purchaseAmount": assets_item.size_36_purchase_amount,
                    },
                    {
                        "size": "37",
                        "innerSize": "8",
                        "outterSize": "8",
                        "purchaseAmount": assets_item.size_37_purchase_amount,
                    },
                    {
                        "size": "38",
                        "innerSize": "8",
                        "outterSize": "8.5",
                        "purchaseAmount": assets_item.size_38_purchase_amount,
                    },
                    {
                        "size": "39",
                        "innerSize": "9",
                        "outterSize": "9",
                        "purchaseAmount": assets_item.size_39_purchase_amount,
                    },
                    {
                        "size": "40",
                        "innerSize": "9",
                        "outterSize": "9.5",
                        "purchaseAmount": assets_item.size_40_purchase_amount,
                    },
                    {
                        "size": "41",
                        "innerSize": "10",
                        "outterSize": "10",
                        "purchaseAmount": assets_item.size_41_purchase_amount,
                    },
                    {
                        "size": "42",
                        "innerSize": "10",
                        "outterSize": "10.5",
                        "purchaseAmount": assets_item.size_42_purchase_amount,
                    },
                    {
                        "size": "43",
                        "innerSize": "11",
                        "outterSize": "11",
                        "purchaseAmount": assets_item.size_43_purchase_amount,
                    },
                    {
                        "size": "44",
                        "innerSize": "12",
                        "outterSize": "12",
                        "purchaseAmount": assets_item.size_44_purchase_amount,
                    },
                    {
                        "size": "45",
                        "innerSize": "13",
                        "outterSize": "13",
                        "purchaseAmount": assets_item.size_45_purchase_amount,
                    },
                ],
            })
    fin_result = {
        "purchaseDivideOrderType": purchase_divide_order_type,
        "data": result,
    }
    return jsonify(fin_result)

@assets_purchase_page_bp.route(
    "/logistics/getassetspurchasedivideorders", methods=["GET"]
)
def get_purchase_divide_orders():
    purchase_order_id = request.args.get("purchaseOrderId")

    # Fetch the data from the database
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            AssetsPurchaseOrderItem,
            Material,
            MaterialType,
            Supplier,
            Color,
        )
        .join(
            AssetsPurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == AssetsPurchaseOrderItem.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .join(Material, AssetsPurchaseOrderItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .join(Color, AssetsPurchaseOrderItem.color == Color.color_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )

    # Group the results by purchase_divide_order_rid
    grouped_results = {}
    for (
        purchase_divide_order,
        purchase_order,
        assets_item,
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
                "materialId": assets_item.material_id,
                "materialType": material_type.material_type_name,
                "materialName": material.material_name,
                "materialSpecification": assets_item.material_specification,
                "color": color.color_name,
                "unit": material.material_unit,
                "purchaseAmount": assets_item.purchase_amount,
                "size35": assets_item.size_35_purchase_amount,
                "size36": assets_item.size_36_purchase_amount,
                "size37": assets_item.size_37_purchase_amount,
                "size38": assets_item.size_38_purchase_amount,
                "size39": assets_item.size_39_purchase_amount,
                "size40": assets_item.size_40_purchase_amount,
                "size41": assets_item.size_41_purchase_amount,
                "size42": assets_item.size_42_purchase_amount,
                "size43": assets_item.size_43_purchase_amount,
                "size44": assets_item.size_44_purchase_amount,
                "size45": assets_item.size_45_purchase_amount,
                "remark": assets_item.remark,
                "sizeType": assets_item.size_type,
            }
        )

    # Convert the grouped results to a list
    result = list(grouped_results.values())

    return jsonify(result)


@assets_purchase_page_bp.route("/logistics/unsubmitpurchaseordersave", methods=["POST"])
def unsubmit_purchase_order_save():
    purchase_divide_order_data = request.json.get("data")
    print(purchase_divide_order_data)
    for item in purchase_divide_order_data:
        purchase_divide_order_rid = item["purchaseDivideOrderId"]
        purchase_order_remark = item["remark"]
        purchase_order_environmental_request = item["evironmentalRequest"]
        shipment_address = item["shipmentAddress"]
        shipment_deadline = item["shipmentDeadline"]
        db.session.query(PurchaseDivideOrder).filter(
            PurchaseDivideOrder.purchase_divide_order_rid == purchase_divide_order_rid
        ).update(
            {
                "purchase_order_remark": purchase_order_remark,
                "purchase_order_environmental_request": purchase_order_environmental_request,
                "shipment_address": shipment_address,
                "shipment_deadline": shipment_deadline,
            }
        )
        db.session.commit()
    return jsonify({"status": "success"})


@assets_purchase_page_bp.route("/logistics/submitpurchaseorder", methods=["POST"])
def submit_purchase_order():
    purchase_order_id = request.json.get("purchaseOrderId")
    print(purchase_order_id)
    purchase_order_status = "1"
    db.session.query(PurchaseOrder).filter(
        PurchaseOrder.purchase_order_rid == purchase_order_id
    ).update(
        {
            "purchase_order_status": purchase_order_status,
        }
    )
    db.session.commit()
    query = (
        db.session.query(
            PurchaseDivideOrder,
            PurchaseOrder,
            AssetsPurchaseOrderItem,
            Material,
            MaterialType,
            Supplier,
            Color,
        )
        .join(
            AssetsPurchaseOrderItem,
            PurchaseDivideOrder.purchase_divide_order_id
            == AssetsPurchaseOrderItem.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseDivideOrder.purchase_order_id == PurchaseOrder.purchase_order_id,
        )
        .join(Material, AssetsPurchaseOrderItem.material_id == Material.material_id)
        .join(MaterialType, Material.material_type_id == MaterialType.material_type_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .join(Color, AssetsPurchaseOrderItem.color == Color.color_id)
        .filter(PurchaseOrder.purchase_order_rid == purchase_order_id)
        .all()
    )
    for (
        purchase_divide_order,
        purchase_order,
        assets_item,
        material,
        material_type,
        supplier,
        color,
    ) in query:
        material_id = assets_item.material_id
        material_quantity = assets_item.purchase_amount
        material_specification = assets_item.material_specification
        color = assets_item.color
        remark = assets_item.remark
        size_type = assets_item.size_type
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
            )
            db.session.add(material_storage)
            db.session.commit()
        elif purchase_divide_order.purchase_divide_order_type == "S":
            size_35_quantity = assets_item.size_35_purchase_amount
            size_36_quantity = assets_item.size_36_purchase_amount
            size_37_quantity = assets_item.size_37_purchase_amount
            size_38_quantity = assets_item.size_38_purchase_amount
            size_39_quantity = assets_item.size_39_purchase_amount
            size_40_quantity = assets_item.size_40_purchase_amount
            size_41_quantity = assets_item.size_41_purchase_amount
            size_42_quantity = assets_item.size_42_purchase_amount
            size_43_quantity = assets_item.size_43_purchase_amount
            size_44_quantity = assets_item.size_44_purchase_amount
            size_45_quantity = assets_item.size_45_purchase_amount

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

            )
            db.session.add(size_material_storage)
    db.session.commit()
    return jsonify({"status": "success"})

@assets_purchase_page_bp.route(
    "/logistics/editsavedpurchaseorderitems", methods=["POST"]
)
def edit_saved_purchase_order_items():
    try:
        purchase_order_id = request.json.get("purchaseOrderId")
        material_list = request.json.get("data")
        purchase_divide_order_type = request.json.get("purchaseDivideOrderType")
        
        # Fetch the corresponding purchase_order
        purchase_order = db.session.query(PurchaseOrder).filter(
            PurchaseOrder.purchase_order_rid == purchase_order_id
        ).first()
        
        if not purchase_order:
            return jsonify({"status": "error", "message": "Purchase order not found"}), 404

        # Delete all related AssetsPurchaseOrderItems and PurchaseDivideOrders
        db.session.query(AssetsPurchaseOrderItem).filter(
            AssetsPurchaseOrderItem.purchase_divide_order_id.in_(
                db.session.query(PurchaseDivideOrder.purchase_divide_order_id).filter(
                    PurchaseDivideOrder.purchase_order_id == purchase_order.purchase_order_id
                )
            )
        ).delete(synchronize_session=False)

        db.session.query(PurchaseDivideOrder).filter(
            PurchaseDivideOrder.purchase_order_id == purchase_order.purchase_order_id
        ).delete(synchronize_session=False)

        # Commit the deletions
        db.session.commit()

        # Add new items as per the new data
        material_list_sorted = sorted(material_list, key=itemgetter("supplierName"))

        # Group the list by 'supplierName'
        grouped_materials = {}
        for supplier_name, items in groupby(
            material_list_sorted, key=itemgetter("supplierName")
        ):
            grouped_materials[supplier_name] = list(items)
        
        for supplier_name, items in grouped_materials.items():
            supplier_id = (
                db.session.query(Supplier)
                .filter(Supplier.supplier_name == supplier_name)
                .first()
                .supplier_id
            )
            supplier_id_str = str(supplier_id).zfill(4)

            purchase_divide_order_rid = purchase_order_id + supplier_id_str
            purchase_divide_order = PurchaseDivideOrder(
                purchase_divide_order_rid=purchase_divide_order_rid,
                purchase_order_id=purchase_order.purchase_order_id,
                purchase_divide_order_type=purchase_divide_order_type,
            )
            db.session.add(purchase_divide_order)
            db.session.commit()

            purchase_divide_order_id = purchase_divide_order.purchase_divide_order_id
            
            # Add assets items
            for item in items:
                material_name = item["materialName"]
                material_info = (
                    db.session.query(Material, Supplier)
                    .join(Supplier, Material.material_supplier == Supplier.supplier_id)
                    .filter(
                        Material.material_name == material_name,
                        Supplier.supplier_name == supplier_name,
                    )
                    .first()
                )
                
                material_id = material_info.Material.material_id
                material_specification = item["materialSpecification"]
                color = item["color"]
                remark = item["comment"]
                
                if purchase_divide_order_type == "N":
                    material_quantity = item["purchaseAmount"]
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
                elif purchase_divide_order_type == "S":
                    material_quantities = [
                        item["sizeInfo"][i]["purchaseAmount"] for i in range(11)
                    ]
                    total_quantity = sum(material_quantities)
                    assets_item = AssetsPurchaseOrderItem(
                        purchase_divide_order_id=purchase_divide_order_id,
                        material_id=material_id,
                        purchase_amount=total_quantity,
                        size_35_purchase_amount=material_quantities[0],
                        size_36_purchase_amount=material_quantities[1],
                        size_37_purchase_amount=material_quantities[2],
                        size_38_purchase_amount=material_quantities[3],
                        size_39_purchase_amount=material_quantities[4],
                        size_40_purchase_amount=material_quantities[5],
                        size_41_purchase_amount=material_quantities[6],
                        size_42_purchase_amount=material_quantities[7],
                        size_43_purchase_amount=material_quantities[8],
                        size_44_purchase_amount=material_quantities[9],
                        size_45_purchase_amount=material_quantities[10],
                        material_specification=material_specification,
                        color=color,
                        remark=remark,
                        size_type="E",
                    )
                    db.session.add(assets_item)
        
        db.session.commit()
        return jsonify({"status": "success"})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.session.close()

@assets_purchase_page_bp.route(
    "/logistics/deleteunsubmitpurchaseorder", methods=["DELETE"]
)
def delete_unsubmit_purchase_order():
    try:
        purchase_order_id = request.args.get("purchaseOrderId")
        
        # Fetch the corresponding purchase_order
        purchase_order = db.session.query(PurchaseOrder).filter(
            PurchaseOrder.purchase_order_rid == purchase_order_id
        ).first()
        
        if not purchase_order:
            return jsonify({"status": "error", "message": "Purchase order not found"}), 404

        # Delete all related AssetsPurchaseOrderItems and PurchaseDivideOrders
        db.session.query(AssetsPurchaseOrderItem).filter(
            AssetsPurchaseOrderItem.purchase_divide_order_id.in_(
                db.session.query(PurchaseDivideOrder.purchase_divide_order_id).filter(
                    PurchaseDivideOrder.purchase_order_id == purchase_order.purchase_order_id
                )
            )
        ).delete(synchronize_session=False)

        db.session.query(PurchaseDivideOrder).filter(
            PurchaseDivideOrder.purchase_order_id == purchase_order.purchase_order_id
        ).delete(synchronize_session=False)

        # Delete the purchase_order
        db.session.delete(purchase_order)

        # Commit the deletions
        db.session.commit()
        return jsonify({"status": "success"})
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        db.session.close()
    


