from flask import Blueprint, jsonify, request, send_file
import os
import datetime
from app_config import app, db
from models import *
from event_processor import EventProcessor
from constants import FILE_STORAGE_PATH, IMAGE_STORAGE_PATH
from api_utility import randomIdGenerater

dev_producion_order_bp = Blueprint("dev_producion_order_bp", __name__)


@dev_producion_order_bp.route("/devproductionorder/getordershoelist", methods=["GET"])
def get_order_list():
    order_id = request.args.get("orderid")
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
        .outerjoin(
            TotalBom, Bom.total_bom_id == TotalBom.total_bom_id
        )  # Assuming TotalBom is optional
        .outerjoin(PurchaseOrder, PurchaseOrder.bom_id == TotalBom.total_bom_id)
        .filter(Order.order_id == order_id)  # Assuming PurchaseOrder is optional
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
        if order_shoe.production_order_upload_status == "0":
            status = "未上传"
        elif order_shoe.production_order_upload_status == "1":
            status = "已上传"
        elif order_shoe.production_order_upload_status == "2":
            status = "已下发"
        if shoe.shoe_rid not in result_dict:
            result_dict[shoe.shoe_rid] = {
                "inheritId": shoe.shoe_rid,
                "customerId": order_shoe.customer_product_name,
                "designer": shoe.shoe_designer,
                "status": status,
                "typeInfos": [],  # Initialize empty list for colors
                "colorSet": set(),  # Initialize a set to track colors for each shoe
            }

        # Check if the color is already added for this shoe
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
                    first_bom_status = "已保存"
                elif bom.bom_status == "2":
                    first_bom_status = "已提交"
                elif bom.bom_status == "3":
                    first_bom_status = "已下发"

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


@dev_producion_order_bp.route(
    "/devproductionorder/getnewproductioninstructionid", methods=["GET"]
)
def get_new_production_instruction_id():
    current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
    random_string = randomIdGenerater(6)
    production_instruction_id = current_time_stamp + random_string + "PI"
    return jsonify({"productionInstructionId": production_instruction_id})


@dev_producion_order_bp.route("/devproductionorder/getordershoeinfo", methods=["GET"])
def get_order_shoe_info():
    order_id = request.args.get("orderid")
    order_shoe_rid = request.args.get("ordershoeid")
    order_shoe = (
        db.session.query(Order, Customer, OrderShoe, Shoe)
        .join(Customer, Order.customer_id == Customer.customer_id)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, Shoe.shoe_id == OrderShoe.shoe_id)
        .filter(Order.order_id == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    customer_name = order_shoe.Customer.customer_name
    customer_product_name = order_shoe.OrderShoe.customer_product_name
    shoe_designer = order_shoe.Shoe.shoe_designer
    brand_name = order_shoe.Customer.customer_brand
    shoe_adjuster = order_shoe.OrderShoe.adjust_staff
    order_shoe_type = (
        db.session.query(OrderShoeType, ShoeType, Color)
        .join(ShoeType, OrderShoeType.shoe_type_id == ShoeType.shoe_type_id)
        .join(Color, ShoeType.color_id == Color.color_id)
        .filter(OrderShoeType.order_shoe_id == order_shoe.OrderShoe.order_shoe_id)
        .all()
    )
    color_list = []
    for shoe_type in order_shoe_type:
        color_list.append(shoe_type.Color.color_name)
    color_str = ", ".join(color_list)
    result = {
        "customerName": customer_name,
        "customerProductName": customer_product_name,
        "shoeDesigner": shoe_designer,
        "brandName": brand_name,
        "shoeAdjuster": shoe_adjuster,
        "color": color_str,
    }
    return jsonify(result)



@dev_producion_order_bp.route(
    "/devproductionorder/saveproductioninstruction", methods=["POST"]
)
def save_production_instruction():
    order_id = request.json.get("orderId")
    order_shoe_rid = request.json.get("orderShoeId")
    production_instruction_rid = request.json.get("productionInstructionId")
    upload_data = request.json.get("uploadData")
    order_shoe_id = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
        .OrderShoe.order_shoe_id
    )
    production_instruction = ProductionInstruction(
        production_instruction_rid=production_instruction_rid,
        order_shoe_id=order_shoe_id,
        production_instruction_status="1",
    )
    db.session.add(production_instruction)
    db.session.flush()
    production_instruction_id = production_instruction.production_instruction_id
    for data in upload_data:
        shoe_color = data.get("color")
        print(shoe_color)
        shoe_type_id = (
            db.session.query(Shoe, ShoeType, Color)
            .join(ShoeType, Shoe.shoe_id == ShoeType.shoe_id)
            .join(Color, ShoeType.color_id == Color.color_id)
            .filter(Shoe.shoe_rid == order_shoe_rid, Color.color_name == shoe_color)
            .first()
            .ShoeType.shoe_type_id
        )
        order_shoe_type_id = (
            db.session.query(OrderShoeType)
            .filter(
                OrderShoeType.order_shoe_id == order_shoe_id,
                OrderShoeType.shoe_type_id == shoe_type_id,
            )
            .first()
            .order_shoe_type_id
        )
        if len(data.get("surfaceMaterialData")) > 0:
            for material_data in data.get("surfaceMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "S"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)

        if len(data.get("insideMaterialData")) > 0:
            for material_data in data.get("insideMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "I"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("accessoryMaterialData")) > 0:
            for material_data in data.get("accessoryMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "A"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("outsoleMaterialData")) > 0:
            for material_data in data.get("outsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "O"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("midsoleMaterialData")) > 0:
            for material_data in data.get("midsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "M"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("lastMaterialData")) > 0:
            for material_data in data.get("lastMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "L"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("hotsoleMaterialData")) > 0:
            for material_data in data.get("hotsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "H"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)

    print(order_id, order_shoe_rid, production_instruction_id, upload_data)
    db.session.commit()
    order_shoe = (
        db.session.query(OrderShoe)
        .filter(OrderShoe.order_shoe_id == order_shoe_id)
        .first()
    )
    order_shoe.production_order_upload_status = "1"
    db.session.commit()

    return jsonify({"message": "Production order uploaded successfully"})


@dev_producion_order_bp.route(
    "/devproductionorder/getproductioninstruction", methods=["GET"]
)
def get_production_instruction():
    order_id = request.args.get("orderid")
    order_shoe_rid = request.args.get("ordershoeid")

    # Fetch order_shoe_id based on order_id and order_shoe_rid
    order_shoe_id = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
        .OrderShoe.order_shoe_id
    )

    # Get the production instruction
    production_instruction = (
        db.session.query(ProductionInstruction)
        .filter(ProductionInstruction.order_shoe_id == order_shoe_id)
        .first()
    )

    if not production_instruction:
        return jsonify({"message": "No production instruction found"}), 404

    production_instruction_id = production_instruction.production_instruction_id
    production_instruction_rid = production_instruction.production_instruction_rid

    # Fetch all items related to the production instruction
    production_instruction_items = (
        db.session.query(ProductionInstructionItem)
        .filter(
            ProductionInstructionItem.production_instruction_id
            == production_instruction_id
        )
        .all()
    )

    # Dictionary to hold the organized data by color
    result_dict = {}

    for item in production_instruction_items:
        # Retrieve color based on order_shoe_type_id
        order_shoe_type = (
            db.session.query(OrderShoeType, ShoeType, Color)
            .join(ShoeType, OrderShoeType.shoe_type_id == ShoeType.shoe_type_id)
            .join(Color, ShoeType.color_id == Color.color_id)
            .filter(OrderShoeType.order_shoe_type_id == item.order_shoe_type_id)
            .first()
        )

        # Skip if color information is not found
        if not order_shoe_type:
            continue

        color_name = order_shoe_type.Color.color_name

        # Initialize color entry if it doesn't exist
        if color_name not in result_dict:
            result_dict[color_name] = {
                "color": color_name,
                "surfaceMaterialData": [],
                "insideMaterialData": [],
                "accessoryMaterialData": [],
                "outsoleMaterialData": [],
                "midsoleMaterialData": [],
                "lastMaterialData": [],
                "hotsoleMaterialData": [],
            }
        material = (
            db.session.query(Material, MaterialType, Supplier)
            .join(
                MaterialType, Material.material_type_id == MaterialType.material_type_id
            )
            .join(Supplier, Material.material_supplier == Supplier.supplier_id)
            .filter(Material.material_id == item.material_id)
            .first()
        )

        # Map material type to the appropriate array in the dictionary
        material_data = {
            "materialId": item.material_id,
            "materialType": material.MaterialType.material_type_name,
            "materialName": material.Material.material_name,
            "materialModel": item.material_model,
            "materialSpecification": item.material_specification,
            "color": item.color,
            "unit": material.Material.material_unit,
            "supplierName": material.Supplier.supplier_name,
            "comment": item.remark,
            "useDepart": item.department_id,
            "isPurchase": item.is_pre_purchase,
        }

        if item.material_type == "S":
            result_dict[color_name]["surfaceMaterialData"].append(material_data)
        elif item.material_type == "I":
            result_dict[color_name]["insideMaterialData"].append(material_data)
        elif item.material_type == "A":
            result_dict[color_name]["accessoryMaterialData"].append(material_data)
        elif item.material_type == "O":
            result_dict[color_name]["outsoleMaterialData"].append(material_data)
        elif item.material_type == "M":
            result_dict[color_name]["midsoleMaterialData"].append(material_data)
        elif item.material_type == "L":
            result_dict[color_name]["lastMaterialData"].append(material_data)
        elif item.material_type == "H":
            result_dict[color_name]["hotsoleMaterialData"].append(material_data)

    # Convert result dictionary to list for JSON response
    result = list(result_dict.values())
    fin_result = {
        "productionInstructionId": production_instruction_rid,
        "instructionData": result,
    }

    return jsonify(fin_result)


@dev_producion_order_bp.route(
    "/devproductionorder/editproductioninstruction", methods=["POST"]
)
def edit_production_instruction():
    order_id = request.json.get("orderId")
    production_instruction_rid = request.json.get("productionInstructionId")
    order_shoe_rid = request.json.get("orderShoeId")
    upload_data = request.json.get("uploadData")
    order_shoe_id = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
        .OrderShoe.order_shoe_id
    )
    production_instruction = (
        db.session.query(ProductionInstruction)
        .filter(
            ProductionInstruction.production_instruction_rid
            == production_instruction_rid
        )
        .first()
    )
    production_instruction_id = production_instruction.production_instruction_id
    production_instruction_items = (
        db.session.query(ProductionInstructionItem)
        .filter(
            ProductionInstructionItem.production_instruction_id
            == production_instruction_id
        )
        .all()
    )
    for item in production_instruction_items:
        db.session.delete(item)
    for data in upload_data:
        shoe_color = data.get("color")
        shoe_type_id = (
            db.session.query(Shoe, ShoeType, Color)
            .join(ShoeType, Shoe.shoe_id == ShoeType.shoe_id)
            .join(Color, ShoeType.color_id == Color.color_id)
            .filter(Shoe.shoe_rid == order_shoe_rid, Color.color_name == shoe_color)
            .first()
            .ShoeType.shoe_type_id
        )
        order_shoe_type_id = (
            db.session.query(OrderShoeType)
            .filter(
                OrderShoeType.order_shoe_id == production_instruction.order_shoe_id,
                OrderShoeType.shoe_type_id == shoe_type_id,
            )
            .first()
            .order_shoe_type_id
        )
        if len(data.get("surfaceMaterialData")) > 0:
            for material_data in data.get("surfaceMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "S"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("insideMaterialData")) > 0:
            for material_data in data.get("insideMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "I"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("accessoryMaterialData")) > 0:
            for material_data in data.get("accessoryMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "A"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("outsoleMaterialData")) > 0:
            for material_data in data.get("outsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "O"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("midsoleMaterialData")) > 0:
            for material_data in data.get("midsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "M"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("lastMaterialData")) > 0:
            for material_data in data.get("lastMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "L"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
        if len(data.get("hotsoleMaterialData")) > 0:
            for material_data in data.get("hotsoleMaterialData"):
                material_id = material_data.get("materialId")
                material_model = (
                    material_data.get("materialModel")
                    if material_data.get("materialModel")
                    else None
                )
                material_spec = (
                    material_data.get("materialSpecification")
                    if material_data.get("materialSpecification")
                    else None
                )
                material_color = (
                    material_data.get("color")
                    if material_data.get("color")
                    else None
                )
                remark = (
                    material_data.get("comment")
                    if material_data.get("comment")
                    else None
                )
                department_id = (
                    material_data.get("useDepart")
                    if material_data.get("useDepart")
                    else None
                )
                is_pre_purchase = (
                    material_data.get("isPurchase")
                    if material_data.get("isPurchase")
                    else None
                )
                material_type = "H"
                order_shoe_type_id = order_shoe_type_id
                production_instruction_item = ProductionInstructionItem(
                    production_instruction_id=production_instruction_id,
                    material_id=material_id,
                    material_model=material_model,
                    material_specification=material_spec,
                    color=material_color,
                    remark=remark,
                    department_id=department_id,
                    is_pre_purchase=is_pre_purchase if is_pre_purchase else False,
                    material_type=material_type,
                    order_shoe_type_id=order_shoe_type_id,
                )
                db.session.add(production_instruction_item)
    db.session.commit()
    return jsonify({"message": "Production instruction updated successfully"}), 200


@dev_producion_order_bp.route("/devproductionorder/upload", methods=["POST"])
def upload_production_order():
    order_shoe_rid = request.form.get("orderShoeRId")
    order_id = request.form.get("orderId")
    print(order_shoe_rid, order_id)
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 500
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 500
    folder_path = os.path.join(FILE_STORAGE_PATH, order_id, order_shoe_rid)
    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)
    file_path = os.path.join(folder_path, "投产指令单.xlsx")
    file.save(file_path)
    order_shoe = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    order_shoe.OrderShoe.production_order_upload_status = "1"
    db.session.commit()

    return jsonify({"message": "Production order uploaded successfully"})


@dev_producion_order_bp.route("/devproductionorder/download", methods=["GET"])
def download_production_order():
    order_shoe_rid = request.args.get("ordershoerid")
    order_id = request.args.get("orderid")
    order_shoe = (
        db.session.query(Order, OrderShoe, Shoe)
        .join(OrderShoe, Order.order_id == OrderShoe.order_id)
        .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
        .filter(Order.order_rid == order_id, Shoe.shoe_rid == order_shoe_rid)
        .first()
    )
    if order_shoe.OrderShoe.production_order_upload_status == "0":
        return jsonify({"error": "Production order not uploaded yet"}), 500
    folder_path = os.path.join(FILE_STORAGE_PATH, order_id, order_shoe_rid)
    file_path = os.path.join(folder_path, "投产指令单.xlsx")
    new_name = order_id + "-" + order_shoe_rid + "_投产指令单.xlsx"
    return send_file(file_path, as_attachment=True, download_name=new_name)


@dev_producion_order_bp.route("/devproductionorder/issue", methods=["POST"])
def issue_production_order():
    order_shoe_rids = request.json.get("orderShoeIds")
    order_rid = request.json.get("orderId")
    for order_shoe_rid in order_shoe_rids:
        order_shoe = (
            db.session.query(Order, OrderShoe, Shoe)
            .join(OrderShoe, Order.order_id == OrderShoe.order_id)
            .join(Shoe, OrderShoe.shoe_id == Shoe.shoe_id)
            .filter(Order.order_rid == order_rid, Shoe.shoe_rid == order_shoe_rid)
            .first()
        )
        order_id = order_shoe.Order.order_id
        order_shoe_id = order_shoe.OrderShoe.order_shoe_id
        print(order_shoe.OrderShoe.production_order_upload_status)
        if order_shoe.OrderShoe.production_order_upload_status != "1":
            return jsonify({"error": "Production order not uploaded yet"}), 500
        order_shoe.OrderShoe.production_order_upload_status = "2"
        db.session.commit()
        production_instruction = (
            db.session.query(ProductionInstruction)
            .filter(ProductionInstruction.order_shoe_id == order_shoe_id)
            .first()
        )
        production_instruction.production_instruction_status = "2"
        db.session.commit()
        production_instruction_items = (
            db.session.query(ProductionInstructionItem)
            .filter(
                ProductionInstructionItem.production_instruction_id
                == production_instruction.production_instruction_id
            )
            .all()
        )
        order_shoe_types = (
            db.session.query(OrderShoeType)
            .filter(OrderShoeType.order_shoe_id == order_shoe_id)
            .all()
        )
        for order_shoe_type in order_shoe_types:
            order_shoe_type_id = order_shoe_type.order_shoe_type_id
            current_time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-5]
            random_string = randomIdGenerater(6)
            first_bom_rid = current_time_stamp + random_string + "F"
            second_bom_rid = current_time_stamp + random_string + "S"
            first_bom = Bom(
                order_shoe_type_id=order_shoe_type_id,
                bom_rid=first_bom_rid,
                bom_type=0,
                bom_status=3,
            )
            db.session.add(first_bom)
            db.session.flush()
            first_bom_id = first_bom.bom_id
            second_bom = Bom(
                order_shoe_type_id=order_shoe_type_id,
                bom_rid=second_bom_rid,
                bom_type=1,
                bom_status=1,
            )
            db.session.add(second_bom)
            db.session.flush()
            second_bom_id = second_bom.bom_id
            for item in production_instruction_items:
                if item.order_shoe_type_id == order_shoe_type.order_shoe_type_id:
                    if item.is_pre_purchase:
                        first_bom_item = BomItem(
                            bom_id=first_bom_id,
                            material_id=item.material_id,
                            material_model=item.material_model,
                            material_specification=item.material_specification,
                            bom_item_color=item.color,
                            remark=item.remark,
                            department_id=item.department_id,
                            size_type="E",
                            bom_item_add_type="0",
                            total_usage=0,
                        )
                        db.session.add(first_bom_item)
                    else:
                        second_bom_item = BomItem(
                            bom_id=second_bom_id,
                            material_id=item.material_id,
                            material_model=item.material_model,
                            material_specification=item.material_specification,
                            bom_item_color=item.color,
                            remark=item.remark,
                            department_id=item.department_id,
                            size_type="E",
                            bom_item_add_type="1",
                            total_usage=0,
                        )
                        db.session.add(second_bom_item)
        db.session.commit()

        processor = EventProcessor()
        event1 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=38,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result1 = processor.processEvent(event1)
        if not result1:
            return jsonify({"error": "Failed to issue production order"}), 500
        db.session.add(event1)
        db.session.commit()
        event2 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=39,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result2 = processor.processEvent(event2)
        db.session.add(event2)
        db.session.commit()
        event3 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=40,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result3 = processor.processEvent(event3)
        db.session.add(event3)
        db.session.commit()
        event4 = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=41,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result4 = processor.processEvent(event4)
        db.session.add(event4)
        db.session.commit()
        if not result2:
            return jsonify({"error": "Failed to issue production order"}), 500
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=42,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=43,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=44,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()
        processor = EventProcessor()
        event = Event(
            staff_id=1,
            handle_time=datetime.datetime.now(),
            operation_id=45,
            event_order_id=order_id,
            event_order_shoe_id=order_shoe_id,
        )
        result = processor.processEvent(event)
        if not result:
            return jsonify({"message": "failed"}), 400
        db.session.add(event)
        db.session.commit()

    return jsonify({"message": "Production order issued successfully"})
