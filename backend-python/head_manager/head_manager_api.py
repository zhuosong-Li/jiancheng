from flask import Blueprint, jsonify, request
from models import *

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


@head_manager_bp.route("/headmanager/getorderstatusinfo", methods=["GET"])
def get_order_status_info():
    """Get the status information of the orders."""
    order_rid = request.args.get("orderRid", None)
    status_symbol = request.args.get("statusSymbol", None)
    if not order_rid:
        orders = Order.query.all()
    else:
        orders = Order.query.filter(Order.order_rid == order_rid).all()
    if not orders:
        return jsonify({"msg": "No order found."}), 404
    order_status_info = []
    for o in orders:
        order_shoes = (
            db.session.query(OrderShoe, Shoe)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(OrderShoe.order_id == o.order_id)
            .all()
        )
        order_status_list = []
        for os in order_shoes:
            events = (
                db.session.query(
                    Event,
                    Operation,
                    OrderShoeStatus,
                    OrderShoe,
                    OrderShoeStatusReference,
                )
                .join(Operation, Event.operation_id == Operation.operation_id)
                .join(
                    OrderShoeStatus,
                    Operation.operation_modified_status
                    == OrderShoeStatus.order_shoe_status_id,
                )
                .join(
                    OrderShoe, OrderShoeStatus.order_shoe_id == OrderShoe.order_shoe_id
                )
                .join(
                    OrderShoeStatusReference,
                    OrderShoeStatus.current_status
                    == OrderShoeStatusReference.status_id,
                )
                .filter(OrderShoeStatus.order_shoe_id == os.OrderShoe.order_shoe_id)
                .filter(Operation.operation_modified_value == 2)
                .all()
            )
            print(events)
            event_list = []
            for e in events:
                event_list.append(
                    {
                        "ordershoeId": e.OrderShoe.order_shoe_id,
                        "eventTime": e.Event.handle_time,
                        "operationName": e.Operation.operation_name,
                    }
                )
            order_status_list.append(
                {
                    "shoeRId": os.Shoe.shoe_rid,
                    "shoeName": os.OrderShoe.customer_product_name,
                    "status": event_list,
                }
            )
            order_info = {
                "orderId": o.order_id,
                "orderRid": o.order_rid,
                "orderShoes": order_status_list,
            }
        order_status_info.append(order_info)
    return jsonify(order_status_info)


@head_manager_bp.route("/headmanager/getmaterialpriceinfo", methods=["GET"])
def get_material_price_info():
    """Get the price information of the materials."""
    material_name = request.args.get("materialName", None)
    material_model = request.args.get("materialModel", None)
    material_specification = request.args.get("materialSpecification", None)
    supplier_name = request.args.get("supplierName", None)
    material_storage = (
        db.session.query(MaterialStorage, Material, Supplier)
        .join(Material, MaterialStorage.material_id == Material.material_id)
        .join(Supplier, Material.material_supplier == Supplier.supplier_id)
        .all()
    )
    print(material_storage)
