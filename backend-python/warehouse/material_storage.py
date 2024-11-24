import datetime
from decimal import Decimal

from api_utility import format_date
from app_config import db
from business.batch_info_type import get_order_batch_type_helper
from constants import (
    END_OF_PRODUCTION_NUMBER,
    IN_PRODUCTION_ORDER_NUMBER,
    PRODUCTION_LINE_REFERENCE,
    SHOESIZERANGE,
)
from event_processor import EventProcessor
from flask import Blueprint, current_app, jsonify, request
from models import *
from sqlalchemy import and_, asc, desc, exists, func, not_, or_

material_storage_bp = Blueprint("material_storage_bp", __name__)


def outbound_size_material_helper(meta_data, outbound_list):
    for row in outbound_list:
        storage = SizeMaterialStorage.query.get(row["id"])
        for i, obj in enumerate(row["outboundAmounts"]):
            shoe_size = 34 + i
            if "amount" not in obj:
                outbound_amount = 0
                obj["amount"] = 0
            else:
                outbound_amount = obj["amount"]
            column_name = f"size_{shoe_size}_current_amount"
            current_value = getattr(storage, column_name)
            if current_value < int(outbound_amount):
                return jsonify({"message": "invalid outbound amount"}), 400
            new_value = current_value - int(outbound_amount)
            setattr(storage, column_name, new_value)
            storage.total_current_amount -= int(outbound_amount)

        record = OutboundRecord(
            outbound_datetime=meta_data["timestamp"],
            outbound_type=meta_data["type"],
            size_material_storage_id=row["id"],
        )
        for i, obj in enumerate(row["outboundAmounts"]):
            shoe_size = 34 + i
            column_name = f"size_{shoe_size}_outbound_amount"
            setattr(record, column_name, obj["amount"])
        if meta_data["type"] == 0:
            if meta_data["department"] not in PRODUCTION_LINE_REFERENCE:
                return jsonify({"message": "failed"}), 400
            record.outbound_department = meta_data["department"]
            record.picker = meta_data["picker"]
        elif meta_data == 2:
            record.outbound_address = meta_data["address"]
        db.session.add(record)
        db.session.flush()
        rid = (
            "OR"
            + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            + str(record.outbound_record_id)
        )
        record.outbound_rid = rid
        db.session.commit()


@material_storage_bp.route(
    "/warehouse/warehousemanager/getallmaterialtypes", methods=["GET"]
)
def get_all_material_types():
    response = db.session.query(MaterialType.material_type_name).all()
    result = []
    for row in response:
        result.append(row[0])
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/getallsuppliernames", methods=["GET"]
)
def get_all_supplier_names():
    response = db.session.query(Supplier.supplier_name).all()
    result = []
    for row in response:
        result.append(row[0])
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/getallmaterialinfo", methods=["GET"]
)
def get_all_material_info():
    """
    op_type:
        0: show all orders,
        1: means show inbound info,
        2: means show outbound info
    """
    page = request.args.get("page", type=int)
    number = request.args.get("pageSize", type=int)
    op_type = request.args.get("opType", default=0, type=int)
    sort_column = request.args.get("sortColumn")
    sort_order = request.args.get("sortOrder")
    filters = {
        "material_type_name": request.args.get("materialType"),
        "material_name": request.args.get("materialName"),
        "material_spec": request.args.get("materialSpec"),
        "supplier": request.args.get("supplier"),
        "order_rid": request.args.get("orderRId"),
        "shoe_rid": request.args.get("shoeRId"),
    }
    material_filter_map = {
        "material_type_name": MaterialType.material_type_name,
        "material_name": Material.material_name,
        "material_spec": MaterialStorage.material_specification,
        "supplier": Supplier.supplier_name,
        "order_rid": Order.order_rid,
        "shoe_rid": Shoe.shoe_rid,
    }
    size_material_filter_map = {
        "material_type_name": MaterialType.material_type_name,
        "material_name": Material.material_name,
        "material_spec": SizeMaterialStorage.size_material_specification,
        "supplier": Supplier.supplier_name,
        "order_rid": Order.order_rid,
        "shoe_rid": Shoe.shoe_rid,
    }
    query1 = (
        db.session.query(
            Order.order_id,
            Order.order_rid,
            OrderShoe.order_shoe_id,
            Shoe.shoe_rid,
            MaterialStorage.material_storage_id,
            MaterialStorage.estimated_inbound_amount,
            MaterialStorage.actual_inbound_amount,
            MaterialStorage.current_amount,
            MaterialStorage.material_specification,
            MaterialStorage.unit_price,
            MaterialStorage.material_estimated_arrival_date,
            MaterialStorage.material_model,
            MaterialStorage.material_storage_status,
            Material.material_name,
            Material.material_unit,
            MaterialType.material_type_name,
            Material.material_category,
            Supplier.supplier_name,
            PurchaseDivideOrder.purchase_divide_order_rid,
            PurchaseOrder.purchase_order_issue_date,
            MaterialStorage.material_storage_color,
        )
        .join(Material, Material.material_id == MaterialStorage.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Supplier.supplier_id == Material.material_supplier)
        .join(
            PurchaseDivideOrder,
            PurchaseDivideOrder.purchase_divide_order_id
            == MaterialStorage.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseOrder.purchase_order_id == PurchaseDivideOrder.purchase_order_id,
        )
        .outerjoin(OrderShoe, MaterialStorage.order_shoe_id == OrderShoe.order_shoe_id)
        .outerjoin(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .outerjoin(Order, OrderShoe.order_id == Order.order_id)
    )
    query2 = (
        db.session.query(
            Order.order_id,
            Order.order_rid,
            OrderShoe.order_shoe_id,
            Shoe.shoe_rid,
            SizeMaterialStorage.size_material_storage_id.label("material_storage_id"),
            SizeMaterialStorage.total_estimated_inbound_amount.label(
                "estimated_inbound_amount"
            ),
            SizeMaterialStorage.total_actual_inbound_amount.label(
                "actual_inbound_amount"
            ),
            SizeMaterialStorage.total_current_amount.label("current_amount"),
            SizeMaterialStorage.size_material_specification.label(
                "material_specification"
            ),
            SizeMaterialStorage.unit_price,
            SizeMaterialStorage.material_estimated_arrival_date,
            SizeMaterialStorage.size_material_model.label("size_material"),
            SizeMaterialStorage.material_storage_status,
            Material.material_name,
            Material.material_unit,
            MaterialType.material_type_name,
            Material.material_category,
            Supplier.supplier_name,
            PurchaseDivideOrder.purchase_divide_order_rid,
            PurchaseOrder.purchase_order_issue_date,
            SizeMaterialStorage.size_material_color,
        )
        .join(Material, Material.material_id == SizeMaterialStorage.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Supplier.supplier_id == Material.material_supplier)
        .join(
            PurchaseDivideOrder,
            PurchaseDivideOrder.purchase_divide_order_id
            == SizeMaterialStorage.purchase_divide_order_id,
        )
        .join(
            PurchaseOrder,
            PurchaseOrder.purchase_order_id == PurchaseDivideOrder.purchase_order_id,
        )
        .outerjoin(
            OrderShoe, SizeMaterialStorage.order_shoe_id == OrderShoe.order_shoe_id
        )
        .outerjoin(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .outerjoin(Order, OrderShoe.order_id == Order.order_id)
    )
    # allow inbound operation when the order is in production
    # in case of leftover material needs to be inbounded
    if op_type == 1:
        query1 = query1.outerjoin(
            OrderStatus, OrderStatus.order_id == Order.order_id
        ).filter(
            or_(
                OrderShoe.order_shoe_id.is_(None),
                OrderStatus.order_current_status == IN_PRODUCTION_ORDER_NUMBER,
            )
        )
        query2 = query2.outerjoin(
            OrderStatus, OrderStatus.order_id == Order.order_id
        ).filter(
            or_(
                OrderShoe.order_shoe_id.is_(None),
                OrderStatus.order_current_status == IN_PRODUCTION_ORDER_NUMBER,
            )
        )
    # allow outbound operation if material is in stock
    # in case of the material needs to be outbounded as waste
    elif op_type == 2:
        query1 = query1.filter(MaterialStorage.current_amount > 0)
        query2 = query2.filter(SizeMaterialStorage.total_current_amount > 0)
    for key, value in filters.items():
        if value and value != "":
            query1 = query1.filter(material_filter_map[key].ilike(f"%{value}%"))
            query2 = query2.filter(size_material_filter_map[key].ilike(f"%{value}%"))
    union_query = query1.union(query2)
    if sort_column and sort_column == "purchaseOrderIssueDate":
        if sort_order == "ascending":
            union_query = union_query.order_by(
                asc(PurchaseOrder.purchase_order_issue_date)
            )
        elif sort_order == "descending":
            union_query = union_query.order_by(
                desc(PurchaseOrder.purchase_order_issue_date)
            )
    count_result = union_query.distinct().count()
    response = union_query.distinct().limit(number).offset((page - 1) * number).all()
    result = []
    for row in response:
        (
            order_id,
            order_rid,
            order_shoe_id,
            shoe_rid,
            material_storage_id,
            estimated_inbound_amount,
            actual_inbound_amount,
            current_amount,
            material_specification,
            unit_price,
            material_estimated_arrival_date,
            material_model,
            material_storage_status,
            material_name,
            material_unit,
            material_type_name,
            material_category,
            supplier_name,
            purchase_divide_order_rid,
            purchase_order_issue_date,
            color,
        ) = row
        if material_storage_status == 0:
            status = "未完成入库"
        elif material_storage_status == 1:
            status = "已完成入库"
        elif material_storage_status == 2:
            status = "已完成出库"
        if not material_estimated_arrival_date:
            date_value = ""
        else:
            date_value = format_date(material_estimated_arrival_date)
        obj = {
            "materialType": material_type_name,
            "materialName": material_name,
            "materialSpecification": material_specification,
            "materialUnit": material_unit,
            "materialCategory": material_category,
            "estimatedInboundAmount": estimated_inbound_amount,
            "actualInboundAmount": actual_inbound_amount,
            "currentAmount": current_amount,
            "unitPrice": unit_price,
            "totalPrice": round(current_amount * unit_price, 2),
            "supplierName": supplier_name,
            "orderId": order_id,
            "orderRId": order_rid,
            "orderShoeId": order_shoe_id,
            "shoeRId": shoe_rid,
            "materialStorageId": material_storage_id,
            "status": status,
            "colorName": color,
            "materialArrivalDate": date_value,
            "purchaseDivideOrderRId": purchase_divide_order_rid,
            "purchaseOrderIssueDate": format_date(purchase_order_issue_date),
            "materialModel": material_model,
        }
        result.append(obj)
    return {"result": result, "total": count_result}


# @material_storage_bp.route(
#     "/warehouse/warehousemanager/checkinboundoptions", methods=["GET"]
# )
# def check_inbound_options():
#     """
#     1: 采购入库
#     2: 生产剩余
#     """
#     order_shoe_id = request.args.get("orderShoeId")
#     if not order_shoe_id:
#         return {1: True, 2: True}
#     status_list = (
#         db.session.query(OrderShoeStatus)
#         .filter(OrderShoeStatus.order_shoe_id == order_shoe_id)
#         .all()
#     )
#     result = {1: False, 2: True}
#     for status_obj in status_list:
#         if status_obj.current_status in [8, 15] and status_obj.current_status_value in [
#             0,
#             1,
#         ]:
#             result[1] = True
#             break
#     return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/getsizematerialbyid", methods=["GET"]
)
def get_size_material_info_by_id():
    id = request.args.get("sizeMaterialStorageId")
    order_id = request.args.get("orderId")
    response = SizeMaterialStorage.query.get(id)
    result = []
    # get shoe size name
    shoe_size_names = get_order_batch_type_helper(order_id)
    for i, shoe_size in range(len(shoe_size_names)):
        obj = {
            "typeName": shoe_size_names[i]["type"],
            "shoeSizeName": shoe_size_names[i]["label"],
            "predictQuantity": getattr(
                response, f"size_{shoe_size}_estimated_inbound_amount"
            ),
            "actualQuantity": getattr(
                response, f"size_{shoe_size}_actual_inbound_amount"
            ),
            "currentQuantity": getattr(response, f"size_{shoe_size}_current_amount"),
        }
        result.append(obj)
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/inboundmaterial", methods=["PATCH"]
)
def inbound_material():
    data = request.get_json()
    storage = MaterialStorage.query.get(data["materialStorageId"])
    storage.unit_price = data["unitPrice"]
    storage.actual_inbound_amount += Decimal(data["amount"])
    storage.current_amount += Decimal(data["amount"])
    record = InboundRecord(
        inbound_amount=Decimal(data["amount"]),
        inbound_datetime=data["date"],
        inbound_type=data["type"],
        material_storage_id=data["materialStorageId"],
    )
    db.session.add(record)
    db.session.flush()
    rid = (
        "IR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.inbound_record_id)
    )
    record.inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


# check whether materials for order_shoe has inbounded
@material_storage_bp.route(
    "/warehouse/warehousemanager/notifyrequiredmaterialarrival", methods=["GET"]
)
def notify_required_material_arrival():
    order_shoe_id = request.args.get("orderShoeId")
    production_info = OrderShoeProductionInfo.query.filter(
        OrderShoeProductionInfo.order_shoe_id == order_shoe_id
    ).first()
    is_material_arrived = production_info.is_material_arrived
    if is_material_arrived:
        return jsonify({"message": "no"})

    query1 = db.session.query(MaterialStorage.material_storage_status).filter(
        MaterialStorage.order_shoe_id == order_shoe_id
    )
    query2 = db.session.query(SizeMaterialStorage.material_storage_status).filter(
        SizeMaterialStorage.order_shoe_id == order_shoe_id
    )
    response = query1.union(query2).all()
    notify = True
    for row in response:
        if row.material_storage_status == 0:
            notify = False

    if notify:
        # set is_material_arrived to true
        production_info.is_material_arrived = True
        db.session.commit()
        return jsonify({"message": "yes"})
    return jsonify({"message": "no"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/inboundsizematerial", methods=["PATCH"]
)
def inbound_size_material():
    data = request.get_json()
    storage = SizeMaterialStorage.query.get(data["sizeMaterialStorageId"])
    storage.total_actual_inbound_amount = 0
    storage.total_current_amount = 0
    for shoe_size in SHOESIZERANGE:
        # actual inbound amount
        column_name = f"size_{shoe_size}_actual_inbound_amount"
        current_value = getattr(storage, column_name)
        new_value = current_value + int(data[f"size{shoe_size}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_actual_inbound_amount += new_value

        # current_amount
        column_name = f"size_{shoe_size}_current_amount"
        current_value = getattr(storage, column_name)
        new_value = current_value + int(data[f"size{shoe_size}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_current_amount += new_value
    record = InboundRecord(
        inbound_datetime=data["date"],
        inbound_type=data["type"],
        size_material_storage_id=data["sizeMaterialStorageId"],
    )
    for shoe_size in SHOESIZERANGE:
        column_name = f"size_{shoe_size}_inbound_amount"
        setattr(record, column_name, int(data[f"size{shoe_size}Amount"]))
    db.session.add(record)
    db.session.flush()
    rid = (
        "IR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.inbound_record_id)
    )
    record.inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/outboundmaterial", methods=["PATCH"]
)
def outbound_material():
    data = request.get_json()
    # get meta data
    meta_data = {
        "timestamp": data["timestamp"],
        "type": data["type"],
        "department": data["outboundDepartment"],
        "address": data["outboundAddress"],
        "picker": data["picker"],
        "outsource_info_id": data["outsourceInfoId"],
    }
    # material amount info
    material_outbound_list = data["materialOutboundList"]
    size_material_outbound_list = data["sizeMaterialOutboundList"]

    # material
    for row in material_outbound_list:
        storage = db.session.query(MaterialStorage).get(row["id"])
        if not storage:
            return jsonify({"message": "invalid storage id"}), 400
        if storage.current_amount < Decimal(row["amount"]):
            return jsonify({"message": "invalid outbound amount"}), 400
        storage.current_amount -= Decimal(row["amount"])
        record = OutboundRecord(
            outbound_amount=row["amount"],
            outbound_datetime=meta_data["timestamp"],
            outbound_type=meta_data["type"],
            material_storage_id=row["id"],
        )
        if data["type"] == 0:
            if data["outboundDepartment"] not in PRODUCTION_LINE_REFERENCE:
                return jsonify({"message": "failed"}), 400
            record.outbound_department = meta_data["department"]
            record.picker = meta_data["picker"]
        elif data == 2:
            record.outbound_address = meta_data["address"]
            record.outsource_info_id = meta_data["outsource_info_id"]
        db.session.add(record)
        db.session.flush()
        rid = (
            "OR"
            + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            + str(record.outbound_record_id)
        )
        record.outbound_rid = rid

    # size material
    outbound_size_material_helper(meta_data, size_material_outbound_list)
    db.session.commit()
    return jsonify({"message": "success"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/checkoutboundoptions", methods=["GET"]
)
def check_outbound_options():
    """
    1: 自产出库
    2: 废料处理
    3: 外包出库
    """
    order_shoe_id = request.args.get("orderShoeId")
    status_list = (
        db.session.query(OrderShoeStatus)
        .filter(OrderShoeStatus.order_shoe_id == order_shoe_id)
        .all()
    )
    result = {1: False, 2: True, 3: False}
    for status_obj in status_list:
        if status_obj.current_status in [
            23,
            32,
            40,
        ] and status_obj.current_status_value in [0, 1]:
            result[1] = True
            break
        elif status_obj.current_status in [
            17,
            24,
            33,
            41,
        ] and status_obj.current_status_value in [0, 1]:
            result[3] = True
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/outboundsizematerial", methods=["PATCH"]
)
def outbound_size_material():
    data = request.get_json()
    storage = SizeMaterialStorage.query.get(data["sizeMaterialStorageId"])
    for shoe_size in SHOESIZERANGE:
        column_name = f"size_{shoe_size}_current_amount"
        current_value = getattr(storage, column_name)
        if current_value < int(data[f"size{shoe_size}Amount"]):
            return jsonify({"message": "invalid outbound amount"}), 400
        new_value = current_value - int(data[f"size{shoe_size}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_current_amount -= int(data[f"size{shoe_size}Amount"])
    record = OutboundRecord(
        outbound_datetime=data["date"],
        outbound_type=data["type"],
        size_material_storage_id=data["sizeMaterialStorageId"],
    )
    for shoe_size in SHOESIZERANGE:
        column_name = f"size_{shoe_size}_outbound_amount"
        setattr(record, column_name, int(data[f"size{shoe_size}Amount"]))
    if data["type"] == "1":
        record.outbound_department = data["outboundDepartment"]
        if data["outboundDepartment"] not in PRODUCTION_LINE_REFERENCE:
            return jsonify({"message": "failed"}), 400
        record.picker = data["picker"]
    elif data == "2":
        record.outbound_address = data["outboundAddress"]
    db.session.add(record)
    db.session.flush()
    rid = (
        "OR"
        + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        + str(record.outbound_record_id)
    )
    record.outbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/getmaterialinoutboundrecords", methods=["GET"]
)
def get_material_in_out_bound_records():
    db.session.query()
    storage_id = request.args.get("storageId")
    name = request.args.get("storageName")
    if name == "material":
        inbound_response = InboundRecord.query.filter(
            InboundRecord.material_storage_id == storage_id
        ).all()
        outbound_response = OutboundRecord.query.filter(
            OutboundRecord.material_storage_id == storage_id
        ).all()
    elif name == "sizeMaterial":
        inbound_response = InboundRecord.query.filter(
            InboundRecord.size_material_storage_id == storage_id
        ).all()
        outbound_response = OutboundRecord.query.filter(
            OutboundRecord.size_material_storage_id == storage_id
        ).all()
    else:
        return jsonify({"message": "failed"}), 400

    result = []
    for row in inbound_response:
        obj = {
            "opType": "入库",
            "date": row.inbound_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if name == "sizeMaterial":
            for shoe_size in SHOESIZERANGE:
                column_name = f"size_{shoe_size}_inbound_amount"
                obj[f"size{shoe_size}Amount"] = getattr(row, column_name)
        else:
            obj["amount"] = row.inbound_amount
        result.append(obj)

    for row in outbound_response:
        obj = {
            "opType": "出库",
            "date": row.outbound_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        if name == "sizeMaterial":
            for shoe_size in SHOESIZERANGE:
                column_name = f"size_{shoe_size}_outbound_amount"
                obj[f"size{shoe_size}Amount"] = getattr(row, column_name)
        else:
            obj["amount"] = row.outbound_amount
        result.append(obj)
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/finishinboundmaterial", methods=["PATCH"]
)
def finish_inbound_material():
    data = request.get_json()
    unique_order_shoe_ids = set()
    for row in data:
        storage = None
        if row["materialCategory"] == 0:
            storage = MaterialStorage.query.get(row["storageId"])
        elif row["materialCategory"] == 1:
            storage = SizeMaterialStorage.query.get(row["storageId"])
        else:
            return jsonify({"message": "Invalid material category"}), 400
        if not storage:
            return jsonify({"message": "order shoe storage not found"}), 400
        unique_order_shoe_ids.add((row["orderId"], storage.order_shoe_id))
        storage.material_storage_status = 1
    db.session.flush()
    # check if all materials are inbounded for order shoe
    # TODO: join purchase divide order, bom, to find bom type
    for order_id, order_shoe_id in unique_order_shoe_ids:
        material_filter = (MaterialStorage.order_shoe_id == order_shoe_id) & (
            MaterialStorage.material_storage_status != 1
        )
        result1 = db.session.query(
            db.session.query(MaterialStorage).filter(material_filter).exists()
        ).scalar()
        size_material_filter = (SizeMaterialStorage.order_shoe_id == order_shoe_id) & (
            SizeMaterialStorage.material_storage_status != 1
        )
        result2 = db.session.query(
            db.session.query(SizeMaterialStorage).filter(size_material_filter).exists()
        ).scalar()
        # if all material are arrived
        if not result1 and not result2:
            production_info = (
                db.session.query(OrderShoeProductionInfo)
                .filter_by(order_shoe_id=order_shoe_id)
                .first()
            )
            production_info.is_material_arrived = 1
            processor: EventProcessor = current_app.config["event_processor"]
            try:
                for operation_id in [54, 55]:
                    event = Event(
                        staff_id=11,
                        handle_time=datetime.datetime.now(),
                        operation_id=operation_id,
                        event_order_id=order_id,
                        event_order_shoe_id=order_shoe_id,
                    )
                    processor.processEvent(event)
                    db.session.add(event)
            except Exception:
                return jsonify({"message": "event processor error"}), 500

    db.session.commit()
    return jsonify({"message": "success"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/finishoutboundmaterial", methods=["PATCH"]
)
def finish_outbound_material():
    data = request.get_json()
    for row in data:
        storage = None
        if row["materialCategory"] == 0:
            storage = MaterialStorage.query.get(row["storageId"])
        elif row["materialCategory"] == 1:
            storage = SizeMaterialStorage.query.get(row["storageId"])
        else:
            return jsonify({"message": "Invalid material category"}), 400
        if not storage:
            return jsonify({"message": "order shoe storage not found"}), 400
        storage.material_storage_status = 2
    db.session.commit()
    return jsonify({"message": "success"})
