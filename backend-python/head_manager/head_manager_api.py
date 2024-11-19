from flask import Blueprint, jsonify, request
from models import *
from sqlalchemy import func
from datetime import datetime

head_manager_bp = Blueprint("head_manager_bp", __name__)


@head_manager_bp.route("/headmanager/getcostinfo", methods=["GET"])
def get_cost_info():
    """Get the cost information of the shoes."""
    order_rid = request.args.get("orderRid", None)
    if not order_rid:
        order = Order.query.all()
    else:
        order = Order.query.filter(Order.order_rid == order_rid).all()
    if not order:
        return jsonify({"msg": "No order found."}), 404
    cost_info = []
    for o in order:
        order_shoes = (
            db.session.query(OrderShoe, Shoe)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(OrderShoe.order_id == o.order_id)
            .all()
        )
        order_total_material_cost = 0
        order_total_administrative_expenses = 0
        order_total_logistics_cost = 0
        order_total_outsouce_cost = 0
        order_total_price_of_shoes = 0
        order_total_shoe_amount = 0
        order_total_profit = 0
        order_total_cost = 0

        order_shoe_list = []
        for os in order_shoes:
            material_storage = (
                db.session.query(MaterialStorage)
                .filter(MaterialStorage.order_shoe_id == os.OrderShoe.order_shoe_id)
                .all()
            )
            size_storage = (
                db.session.query(SizeMaterialStorage)
                .filter(SizeMaterialStorage.order_shoe_id == os.OrderShoe.order_shoe_id)
                .all()
            )
            material_cost = 0
            size_cost = 0
            for ms in material_storage:
                if ms.actual_inbound_amount >= ms.estimated_inbound_amount:
                    material_cost += (
                        ms.actual_inbound_amount * ms.unit_price
                        if ms.actual_inbound_amount and ms.unit_price
                        else 0
                    )
                else:
                    material_cost += (
                        ms.estimated_inbound_amount * ms.unit_price
                        if ms.estimated_inbound_amount and ms.unit_price
                        else 0
                    )
            for ss in size_storage:
                if ss.total_actual_inbound_amount >= ss.total_estimated_inbound_amount:
                    size_cost += (
                        ss.total_actual_inbound_amount * ss.unit_price
                        if ss.total_actual_inbound_amount and ss.unit_price
                        else 0
                    )
                else:
                    size_cost += (
                        ss.total_estimated_inbound_amount * ss.unit_price
                        if ss.total_estimated_inbound_amount and ss.unit_price
                        else 0
                    )
            total_material_cost = material_cost + size_cost
            order_total_material_cost += total_material_cost
            administrative_expenses = 0
            order_total_administrative_expenses += administrative_expenses
            logistics_cost = 0
            order_total_logistics_cost += logistics_cost
            outsouce_cost = 0
            order_total_outsouce_cost += outsouce_cost
            price_of_shoes = 0

            shoe_total_amount = 0
            order_shoe_batch_infos = (
                db.session.query(OrderShoe, OrderShoeType, OrderShoeBatchInfo)
                .join(
                    OrderShoeType,
                    OrderShoe.order_shoe_id == OrderShoeType.order_shoe_id,
                )
                .join(
                    OrderShoeBatchInfo,
                    OrderShoeBatchInfo.order_shoe_type_id
                    == OrderShoeType.order_shoe_type_id,
                )
                .filter(OrderShoe.order_shoe_id == os.OrderShoe.order_shoe_id)
                .all()
            )
            cutting_cost = 0
            sewing_cost = 0
            for osbi in order_shoe_batch_infos:
                price_of_shoes += (
                    osbi.OrderShoeBatchInfo.total_price
                    if osbi.OrderShoeBatchInfo.total_price
                    else 0
                )
                shoe_total_amount += (
                    osbi.OrderShoeBatchInfo.total_amount
                    if osbi.OrderShoeBatchInfo.total_amount
                    else 0
                )
            order_total_price_of_shoes += price_of_shoes
            order_total_shoe_amount += shoe_total_amount

            total_cost = (
                total_material_cost
                + administrative_expenses
                + logistics_cost
                + outsouce_cost
            )
            order_total_cost += total_cost
            cost_per_shoe = (
                total_cost / shoe_total_amount if shoe_total_amount != 0 else 0
            )

            profit = (
                price_of_shoes
                - total_material_cost
                - administrative_expenses
                - logistics_cost
                - outsouce_cost
            )
            order_total_profit += profit
            profit_per_shoe = (
                profit / shoe_total_amount if shoe_total_amount != 0 else 0
            )

            order_shoe_list.append(
                {
                    # "orderId": o.order_id,
                    # "orderRid": o.order_rid,
                    "shoeRId": os.Shoe.shoe_rid,
                    "shoeName": os.OrderShoe.customer_product_name,
                    "totalMaterialCost": total_material_cost,
                    "administrativeExpenses": administrative_expenses,
                    "logisticsCost": logistics_cost,
                    "outsouceCost": outsouce_cost,
                    "priceOfShoes": price_of_shoes,
                    "shoeTotalAmount": shoe_total_amount,
                    "profit": profit,
                    "profitPerShoe": profit_per_shoe,
                    "costPerShoe": cost_per_shoe,
                }
            )
        print(order_shoe_list)
        order_total_cost_per_shoe = (
            order_total_cost / order_total_shoe_amount
            if order_total_shoe_amount != 0
            else 0
        )
        order_total_profit_per_shoe = (
            order_total_profit / order_total_shoe_amount
            if order_total_shoe_amount != 0
            else 0
        )
        order_info = {
            "orderId": o.order_id,
            "orderRid": o.order_rid,
            "orderShoes": order_shoe_list,
            "orderTotalMaterialCost": order_total_material_cost,
            "orderTotalAdministrativeExpenses": order_total_administrative_expenses,
            "orderTotalLogisticsCost": order_total_logistics_cost,
            "orderTotalOutsouceCost": order_total_outsouce_cost,
            "orderTotalPriceOfShoes": order_total_price_of_shoes,
            "orderTotalShoeAmount": order_total_shoe_amount,
            "orderTotalProfit": order_total_profit,
            "orderTotalCost": order_total_cost,
            "orderTotalCostPerShoe": order_total_cost_per_shoe,
            "orderTotalProfitPerShoe": order_total_profit_per_shoe,
        }
        cost_info.append(order_info)
    return jsonify(cost_info)


@head_manager_bp.route("/headmanager/getmaterialpriceinfo", methods=["GET"])
def get_material_price_info():
    """Get the price information of the materials."""
    # Get query parameters
    material_name = request.args.get("materialName", None)
    material_model = request.args.get("materialModel", None)
    material_specification = request.args.get("materialSpecification", None)
    supplier_name = request.args.get("supplierName", None)

    # Subquery to get the latest inbound record for each material storage
    latest_material_inbound_subquery = (
        db.session.query(
            InboundRecord.material_storage_id.label("material_storage_id"),
            func.max(InboundRecord.inbound_datetime).label("latest_inbound_date"),
        )
        .group_by(InboundRecord.material_storage_id)
        .subquery()
    )

    # Subquery to get the latest inbound record for each size material storage
    latest_size_inbound_subquery = (
        db.session.query(
            InboundRecord.size_material_storage_id.label("size_material_storage_id"),
            func.max(InboundRecord.inbound_datetime).label("latest_inbound_date"),
        )
        .group_by(InboundRecord.size_material_storage_id)
        .subquery()
    )

    # Main query to get material price info with the newest inbound record
    material_storage = (
        db.session.query(MaterialStorage, Material, Supplier, InboundRecord)
        .join(Material, MaterialStorage.material_id == Material.material_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(
            latest_material_inbound_subquery,
            MaterialStorage.material_storage_id
            == latest_material_inbound_subquery.c.material_storage_id,
        )
        .outerjoin(
            InboundRecord,
            (
                InboundRecord.material_storage_id
                == latest_material_inbound_subquery.c.material_storage_id
            )
            & (
                InboundRecord.inbound_datetime
                == latest_material_inbound_subquery.c.latest_inbound_date
            ),
        )
        .all()
    )

    # Main query to get size material price info with the newest inbound record
    size_material_storage = (
        db.session.query(SizeMaterialStorage, Material, Supplier, InboundRecord)
        .join(Material, SizeMaterialStorage.material_id == Material.material_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .outerjoin(
            latest_size_inbound_subquery,
            SizeMaterialStorage.size_material_storage_id
            == latest_size_inbound_subquery.c.size_material_storage_id,
        )
        .outerjoin(
            InboundRecord,
            (
                InboundRecord.size_material_storage_id
                == latest_size_inbound_subquery.c.size_material_storage_id
            )
            & (
                InboundRecord.inbound_datetime
                == latest_size_inbound_subquery.c.latest_inbound_date
            ),
        )
        .all()
    )

    # Process results for material storage
    material_price_info = []
    for ms in material_storage:
        if (
            (not material_name or ms.Material.material_name == material_name)
            and (not material_model or ms.Material.material_model == material_model)
            and (
                not material_specification
                or ms.Material.material_specification == material_specification
            )
            and (not supplier_name or ms.Supplier.supplier_name == supplier_name)
        ):
            # Handle missing inbound record
            purchase_date = (
                ms.InboundRecord.inbound_datetime.strftime("%Y-%m-%d")
                if ms.InboundRecord and ms.InboundRecord.inbound_datetime
                else "未入库"
            )

            material_price_info.append(
                {
                    "type": "N",
                    "materialStorageId": ms.Material.material_id,
                    "materialName": ms.Material.material_name,
                    "materialModel": ms.MaterialStorage.material_model,
                    "materialSpecification": ms.MaterialStorage.material_specification,
                    "supplierName": ms.Supplier.supplier_name,
                    "unitPrice": ms.MaterialStorage.unit_price,
                    "color": ms.MaterialStorage.material_storage_color,
                    "purchaseAmount": ms.MaterialStorage.actual_inbound_amount,  # Assuming 'amount' is the quantity field
                    "purchaseDate": purchase_date,  # Set to "未入库" if no inbound record exists
                }
            )

    # Process results for size material storage
    for sms in size_material_storage:
        if (
            (not material_name or sms.Material.material_name == material_name)
            and (not material_model or sms.Material.material_model == material_model)
            and (
                not material_specification
                or sms.Material.material_specification == material_specification
            )
            and (not supplier_name or sms.Supplier.supplier_name == supplier_name)
        ):
            # Handle missing inbound record
            purchase_date = (
                sms.InboundRecord.inbound_datetime.strftime("%Y-%m-%d")
                if sms.InboundRecord and sms.InboundRecord.inbound_datetime
                else "未入库"
            )

            material_price_info.append(
                {
                    "type": "S",
                    "materialStorageId": sms.SizeMaterialStorage.size_material_storage_id,
                    "materialName": sms.Material.material_name,
                    "materialModel": sms.SizeMaterialStorage.size_material_model,
                    "materialSpecification": sms.SizeMaterialStorage.size_material_specification,
                    "supplierName": sms.Supplier.supplier_name,
                    "unitPrice": sms.SizeMaterialStorage.unit_price,
                    "color": sms.SizeMaterialStorage.size_material_color,
                    "purchaseAmount": sms.SizeMaterialStorage.total_actual_inbound_amount,  # Assuming 'amount' is the quantity field
                    "purchaseDate": purchase_date,  # Set to "未入库" if no inbound record exists
                }
            )

    return jsonify(material_price_info)


@head_manager_bp.route("/headmanager/getmaterialinboundcurve", methods=["GET"])
def get_material_inbound_curve():
    """Get the inbound curve of the materials."""
    material_type = request.args.get("materialType", None)
    material_storage_id = request.args.get("materialStorageId", None)
    if not material_type or not material_storage_id:
        return jsonify({"msg": "Missing query parameters."}), 400
    curve_data = []
    if material_type == "N":
        material_storage = (
            db.session.query(MaterialStorage, InboundRecord)
            .join(InboundRecord, MaterialStorage.material_storage_id == InboundRecord.material_storage_id)
            .filter(MaterialStorage.material_storage_id == material_storage_id)
            .all()
        )
        for ms in material_storage:
            curve_data.append(
                {
                    "date": ms.InboundRecord.inbound_datetime.strftime("%Y-%m-%d"),
                    "unitPrice": ms.MaterialStorage.unit_price,
                }
            )
        return jsonify(curve_data)
    elif material_type == "S":
        size_material_storage = (
            db.session.query(SizeMaterialStorage, InboundRecord)
            .join(InboundRecord, SizeMaterialStorage.size_material_storage_id == InboundRecord.size_material_storage_id)
            .filter(SizeMaterialStorage.size_material_storage_id == material_storage_id)
            .all()
        )
        for sms in size_material_storage:
            curve_data.append(
                {
                    "date": sms.InboundRecord.inbound_datetime.strftime("%Y-%m-%d"),
                    "unitPrice": sms.SizeMaterialStorage.unit_price,
                }
            )
        return jsonify(curve_data)
    return jsonify({"msg": "Invalid material type."}), 400
    # Get query parameters

@head_manager_bp.route("/headmanager/financialstatus", methods=["GET"])
def get_financial_status():
    order_rid = request.args.get("orderRid", None)
    if not order_rid:
        order = Order.query.all()
    else:
        order = Order.query.filter(Order.order_rid.like(f"%{order_rid}%")).all()
    financial_list = []
    for o in order:
        order_shoes = (
            db.session.query(OrderShoe, Shoe)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(OrderShoe.order_id == o.order_id)
            .all()
        )
        order_price_input_status = '未填写'
        order_status = db.session.query(OrderStatus).filter(OrderStatus.order_id == o.order_id).first().order_current_status
        if order_status >= 7:
            order_price_input_status = '已填写'
        order_shoe_list = []
        for os in order_shoes:
            order_shoe_material_inbound_status = '未填写'
            order_shoe_cutting_input_status = '未填写'
            order_shoe_sewing_input_status = '未填写'
            order_shoe_molding_input_status = '未填写'
            order_shoe_price_input_status = order_price_input_status
            production_info = db.session.query(OrderShoeProductionInfo).filter(OrderShoeProductionInfo.order_shoe_id == os.OrderShoe.order_shoe_id).first()
            is_arrived = production_info.is_material_arrived if production_info else False
            if is_arrived:
                order_shoe_material_inbound_status = '已填写'
            cutting_price_report = db.session.query(UnitPriceReport).filter(UnitPriceReport.order_shoe_id == os.OrderShoe.order_shoe_id, UnitPriceReport.team == '裁断').first()
            if cutting_price_report:
                if cutting_price_report.status == 1:
                    order_shoe_cutting_input_status = '未审核'
                if cutting_price_report.status == 2:
                    order_shoe_cutting_input_status = '已填写'
            sewing_price_report = db.session.query(UnitPriceReport).filter(UnitPriceReport.order_shoe_id == os.OrderShoe.order_shoe_id, UnitPriceReport.team == '针车').first()
            if sewing_price_report:
                if sewing_price_report.status == 1:
                    order_shoe_sewing_input_status = '未审核'
                if sewing_price_report.status == 2:
                    order_shoe_sewing_input_status = '已填写'
            order_shoe_list.append(
                {
                    "shoeRId": os.Shoe.shoe_rid,
                    "shoeName": os.OrderShoe.customer_product_name,
                    "materialInboundStatus": order_shoe_material_inbound_status,
                    "cuttingInputStatus": order_shoe_cutting_input_status,
                    "sewingInputStatus": order_shoe_sewing_input_status,
                    "moldingInputStatus": order_shoe_molding_input_status,
                    "priceInputStatus": order_shoe_price_input_status,
                }
            )
        order_info = {
            "orderId": o.order_id,
            "orderRid": o.order_rid,
            "orderShoes": order_shoe_list,
        }
        financial_list.append(order_info)
    return jsonify(financial_list)
        
        

    

    # Get the total number of shoes in transit
