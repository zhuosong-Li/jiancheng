import datetime
from decimal import Decimal
from app_config import db
from constants import (
    END_OF_PRODUCTION_NUMBER,
    IN_PRODUCTION_ORDER_NUMBER,
    PRODUCTION_LINE_REFERENCE,
    SHOESIZEINFO,
)
from event_processor import EventProcessor
from flask import Blueprint, current_app, jsonify, request
from models import *
from sqlalchemy import func, or_, and_, asc, desc

material_storage_bp = Blueprint("material_storage_bp", __name__)


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
            Material.material_name,
            Material.material_unit,
            MaterialType.material_type_name,
            Material.material_category,
            Supplier.supplier_name,
            Color,
            PurchaseDivideOrder.purchase_divide_order_rid,
            PurchaseOrder.purchase_order_issue_date
        )
        .join(Material, Material.material_id == MaterialStorage.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Supplier.supplier_id == Material.material_supplier)
        .join(Color, Color.color_id == MaterialStorage.material_storage_color)
        .join(PurchaseDivideOrder, PurchaseDivideOrder.purchase_divide_order_id == MaterialStorage.purchase_divide_order_id)
        .join(PurchaseOrder, PurchaseOrder.purchase_order_id == PurchaseDivideOrder.purchase_order_id)
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
            Material.material_name,
            Material.material_unit,
            MaterialType.material_type_name,
            Material.material_category,
            Supplier.supplier_name,
            Color,
            PurchaseDivideOrder.purchase_divide_order_rid,
            PurchaseOrder.purchase_order_issue_date
        )
        .join(Material, Material.material_id == SizeMaterialStorage.material_id)
        .join(MaterialType, MaterialType.material_type_id == Material.material_type_id)
        .join(Supplier, Supplier.supplier_id == Material.material_supplier)
        .join(Color, Color.color_id == SizeMaterialStorage.size_material_color)
        .join(PurchaseDivideOrder, PurchaseDivideOrder.purchase_divide_order_id == SizeMaterialStorage.purchase_divide_order_id)
        .join(PurchaseOrder, PurchaseOrder.purchase_order_id == PurchaseDivideOrder.purchase_order_id)
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
        if sort_order == 'ascending':
            union_query = union_query.order_by(asc(PurchaseOrder.purchase_order_issue_date))
        elif sort_order == 'descending':
            union_query = union_query.order_by(desc(PurchaseOrder.purchase_order_issue_date))
    count_result = (
        db.session.query(func.count()).select_from(union_query.subquery()).scalar()
    )
    response = union_query.limit(number).offset((page - 1) * number).all()
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
            material_name,
            material_unit,
            material_type_name,
            material_category,
            supplier_name,
            color,
            purchase_divide_order_rid,
            purchase_order_issue_date,
        ) = row
        if actual_inbound_amount >= estimated_inbound_amount:
            status = "已完成入库"
        else:
            status = "未完成入库"
        if not material_estimated_arrival_date:
            date_value = ""
        else:
            date_value = material_estimated_arrival_date.strftime("%Y-%m-%d")
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
            "colorName": color.color_name,
            "materialArrivalDate": date_value,
            "purchaseDivideOrderRId": purchase_divide_order_rid,
            "purchaseOrderIssueDate": purchase_order_issue_date.strftime("%Y-%m-%d")
        }
        result.append(obj)
    return {"result": result, "total": count_result}


@material_storage_bp.route(
    "/warehouse/warehousemanager/checkinboundoptions", methods=["GET"]
)
def check_inbound_options():
    """
    1: 采购入库
    2: 生产剩余
    """
    order_shoe_id = request.args.get("orderShoeId")
    if not order_shoe_id:
        return {1: True, 2: True}
    status_list = (
        db.session.query(OrderShoeStatus)
        .filter(OrderShoeStatus.order_shoe_id == order_shoe_id)
        .all()
    )
    result = {1: False, 2: True}
    for status_obj in status_list:
        if status_obj.current_status in [8, 15] and status_obj.current_status_value in [
            0,
            1,
        ]:
            result[1] = True
            break
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/getsizematerialbyid", methods=["GET"]
)
def get_size_material_info_by_id():
    id = request.args.get("sizeMaterialStorageId")
    response = SizeMaterialStorage.query.get(id)
    result = []
    for info in SHOESIZEINFO:
        obj = {
            "shoeSize": info["shoe_size"],
            "internalSize": info["internal_size"],
            "externalSize": info["external_size"],
            "predictQuantity": getattr(
                response, f"size_{info['shoe_size']}_estimated_inbound_amount"
            ),
            "actualQuantity": getattr(
                response, f"size_{info['shoe_size']}_actual_inbound_amount"
            ),
            "currentQuantity": getattr(
                response, f"size_{info['shoe_size']}_current_amount"
            ),
        }
        result.append(obj)
    return result


@material_storage_bp.route(
    "/warehouse/warehousemanager/inboundmaterial", methods=["PATCH"]
)
def inbound_material():
    data = request.get_json()
    storage = MaterialStorage.query.get(data["materialStorageId"])
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
    rid = "IR" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(record.inbound_record_id)
    record.inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


# check whether materials for order_shoe has inbounded
@material_storage_bp.route(
    "/warehouse/warehousemanager/notifyrequiredmaterialarrival", methods=["GET"]
)
def notify_required_material_arrival():
    order_id = request.args.get("orderId")
    order_shoe_id = request.args.get("orderShoeId")
    print(order_id, order_shoe_id)
    obj = OrderShoeProductionInfo.query.filter(
        OrderShoeProductionInfo.order_shoe_id == order_shoe_id
    ).first()
    is_material_arrived = obj.is_material_arrived
    if is_material_arrived:
        return jsonify({"message": "no"})

    query1 = db.session.query(
        MaterialStorage.estimated_inbound_amount, MaterialStorage.actual_inbound_amount
    ).filter(MaterialStorage.order_shoe_id == order_shoe_id)
    query2 = db.session.query(
        SizeMaterialStorage.total_estimated_inbound_amount.label(
            "estimated_inbound_amount"
        ),
        SizeMaterialStorage.total_actual_inbound_amount.label("actual_inbound_amount"),
    ).filter(SizeMaterialStorage.order_shoe_id == order_shoe_id)
    response = query1.union(query2).all()
    notify = True
    for row in response:
        estimated_inbound_amount, actual_inbound_amount = row
        if actual_inbound_amount < estimated_inbound_amount:
            notify = False

    if notify:
        # set is_material_arrived to true
        obj.is_material_arrived = True
        # process event
        processor: EventProcessor = current_app.config["event_processor"]
        try:
            event = Event(
                staff_id=1,
                handle_time=datetime.datetime.now(),
                operation_id=54,
                event_order_id=order_id,
                event_order_shoe_id=order_shoe_id,
            )
            result = processor.processEvent(event)
            event = Event(
                staff_id=1,
                handle_time=datetime.datetime.now(),
                operation_id=55,
                event_order_id=order_id,
                event_order_shoe_id=order_shoe_id,
            )
            result = processor.processEvent(event)

            event = Event(
                staff_id=1,
                handle_time=datetime.datetime.now(),
                operation_id=68,
                event_order_id=order_id,
                event_order_shoe_id=order_shoe_id,
            )
            result = processor.processEvent(event)
            event = Event(
                staff_id=1,
                handle_time=datetime.datetime.now(),
                operation_id=69,
                event_order_id=order_id,
                event_order_shoe_id=order_shoe_id,
            )
            result = processor.processEvent(event)
        except Exception as e:
            print(e)
        if not result:
            return jsonify({"message": "failed"}), 500
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
    for info in SHOESIZEINFO:
        # actual inbound amount
        column_name = f"size_{info['shoe_size']}_actual_inbound_amount"
        current_value = getattr(storage, column_name)
        new_value = current_value + int(data[f"size{info['shoe_size']}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_actual_inbound_amount += new_value

        # current_amount
        column_name = f"size_{info['shoe_size']}_current_amount"
        current_value = getattr(storage, column_name)
        new_value = current_value + int(data[f"size{info['shoe_size']}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_current_amount += new_value
    record = InboundRecord(
        inbound_datetime=data["date"],
        inbound_type=data["type"],
        size_material_storage_id=data["sizeMaterialStorageId"],
    )
    for info in SHOESIZEINFO:
        column_name = f"size_{info['shoe_size']}_inbound_amount"
        setattr(record, column_name, int(data[f"size{info['shoe_size']}Amount"]))
    db.session.add(record)
    db.session.flush()
    rid = "IR" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(record.inbound_record_id)
    record.inbound_rid = rid
    db.session.commit()
    return jsonify({"message": "success"})


@material_storage_bp.route(
    "/warehouse/warehousemanager/outboundmaterial", methods=["PATCH"]
)
def outbound_material():
    data = request.get_json()
    storage = MaterialStorage.query.get(data["materialStorageId"])
    if storage.current_amount < Decimal(data["amount"]):
        return jsonify({"message": "invalid outbound amount"}), 400
    storage.current_amount -= Decimal(data["amount"])
    record = OutboundRecord(
        outbound_amount=data["amount"],
        outbound_datetime=data["date"],
        outbound_type=data["type"],
        material_storage_id=data["materialStorageId"],
    )
    if data["type"] == "1":
        if data["outboundDepartment"] not in PRODUCTION_LINE_REFERENCE:
            return jsonify({"message": "failed"}), 400
        record.outbound_department = data["outboundDepartment"]
        record.picker = data["picker"]
    elif data == "2":
        record.outbound_address = data["outboundAddress"]
    db.session.add(record)
    db.session.flush()
    rid = (
        "OR" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(record.outbound_record_id)
    )
    record.outbound_rid = rid
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
    for info in SHOESIZEINFO:
        column_name = f"size_{info['shoe_size']}_current_amount"
        current_value = getattr(storage, column_name)
        if current_value < int(data[f"size{info['shoe_size']}Amount"]):
            return jsonify({"message": "invalid outbound amount"}), 400
        new_value = current_value - int(data[f"size{info['shoe_size']}Amount"])
        setattr(storage, column_name, new_value)
        storage.total_current_amount -= int(data[f"size{info['shoe_size']}Amount"])
    record = OutboundRecord(
        outbound_datetime=data["date"],
        outbound_type=data["type"],
        size_material_storage_id=data["sizeMaterialStorageId"],
    )
    for info in SHOESIZEINFO:
        column_name = f"size_{info['shoe_size']}_outbound_amount"
        setattr(record, column_name, int(data[f"size{info['shoe_size']}Amount"]))
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
        "OR" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(record.outbound_record_id)
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
        obj = {"opType": "入库", "date": row.inbound_datetime}
        if name == "sizeMaterial":
            for info in SHOESIZEINFO:
                column_name = f"size_{info['shoe_size']}_inbound_amount"
                obj[f"size{info['shoe_size']}Amount"] = getattr(row, column_name)
        else:
            obj["amount"] = row.inbound_amount
        result.append(obj)

    for row in outbound_response:
        obj = {"opType": "出库", "date": row.outbound_datetime}
        if name == "sizeMaterial":
            for info in SHOESIZEINFO:
                column_name = f"size_{info['shoe_size']}_outbound_amount"
                obj[f"size{info['shoe_size']}Amount"] = getattr(row, column_name)
        else:
            obj["amount"] = row.outbound_amount
        result.append(obj)
    return result
