from flask import Blueprint, jsonify, request, send_file
from sqlalchemy.dialects.mysql import insert
import pandas as pd
import datetime
import time
from werkzeug.utils import secure_filename
import os
import json
import shutil
from models import *
from constants import FILE_STORAGE_PATH, IMAGE_STORAGE_PATH


from app_config import app, db

order_create_bp = Blueprint("order_create_bp", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"xls", "xlsx"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




@order_create_bp.route("/ordercreate/createneworder", methods=["POST"])
def create_new_order():
	time_s = time.time()
	order_info = request.json.get("orderInfo")
	print(order_info)
	if not order_info:
		return jsonify({'error': 'invalid request'}),400
	order_rid = order_info["orderRId"]
	order_cid = order_info["orderCid"]
	batch_info_type_id = order_info["batchInfoTypeId"]
	customer_id = order_info["customerId"]
	order_start_date = order_info["orderStartDate"]
	order_end_date = order_info["orderEndDate"]
	order_status = order_info["status"]
	order_salesman = order_info["salesman"]
	order_shoe_type_list = order_info["orderShoeTypes"]
	customer_shoe_names = order_info["customerShoeName"]
	

	exist_order = Order.query.filter_by(order_rid = order_rid).first()
	if exist_order:
		return jsonify({'error':'invalid request'}), 400

	new_order = Order(
    	order_rid = order_rid,
    	order_cid = order_cid,
		batch_info_type_id = batch_info_type_id,
    	customer_id = customer_id,
    	start_date = order_start_date,
    	end_date = order_end_date,
    	salesman = order_salesman,
    	production_list_upload_status="0",
    	amount_list_upload_status="0"
    	)

	db.session.add(new_order)
	db.session.flush()
	### os mkdir 
	os.mkdir(os.path.join(FILE_STORAGE_PATH, order_rid))

	new_order_id = Order.query.filter_by(order_rid = order_rid).first().order_id
	new_order_status = OrderStatus(
		order_id = new_order_id,
		order_current_status = order_status,
		order_status_value = 1,)
	db.session.add(new_order_status)
	db.session.flush()

	shoe_type_id_to_shoe_type = {shoe_type['shoeTypeId']:shoe_type for shoe_type in order_shoe_type_list}
	shoe_type_ids = shoe_type_id_to_shoe_type.keys()
	shoe_id_to_rid = {}
	shoe_type_id_to_shoe_id = {}
	for shoe_type_id in shoe_type_ids:
		db_shoe_entity = ShoeType.query.filter_by(shoe_type_id = shoe_type_id).first()
		shoe_type_id_to_shoe_id[shoe_type_id] = db_shoe_entity.shoe_id
		shoe_id_to_rid[db_shoe_entity.shoe_id] = shoe_type_id_to_shoe_type[shoe_type_id]["shoeRId"] 

	shoe_id_to_order_shoe_id = {}

	### for every shoe
	for shoe_id in shoe_id_to_rid.keys():
		existing_order_shoe = OrderShoe.query.filter_by(
			order_id = new_order_id, shoe_id = shoe_id
		).first()
		if not existing_order_shoe:
			customer_product_name = customer_shoe_names[shoe_id_to_rid[shoe_id]]
			new_order_shoe_entity = OrderShoe(
				order_id = new_order_id,
				shoe_id = shoe_id,
				customer_product_name = customer_product_name,
				production_order_upload_status = "0",
				process_sheet_upload_status = "0",
				adjust_staff = "",
				business_material_remark = "",
				business_technical_remark = "")
			db.session.add(new_order_shoe_entity)
			db.session.flush()

			os.mkdir(os.path.join(FILE_STORAGE_PATH, order_rid, shoe_id_to_rid[shoe_id]))

			new_order_shoe_status_entity = OrderShoeStatus(
				order_shoe_id = new_order_shoe_entity.order_shoe_id,
				current_status = 0,
				current_status_value = 0,)
			db.session.add(new_order_shoe_status_entity)
			db.session.flush()

			new_order_shoe_production_info_entity = OrderShoeProductionInfo(
				is_cutting_outsourced = 0,
				is_sewing_outsourced = 0,
				is_molding_outsourced = 0,
				is_material_arrived = 0,
				order_shoe_id = new_order_shoe_entity.order_shoe_id)
			
			db.session.add(new_order_shoe_production_info_entity)
			db.session.flush()
			shoe_id_to_order_shoe_id[shoe_id] = new_order_shoe_entity.order_shoe_id

	### for every shoe_type
	print(shoe_id_to_rid)
	print(shoe_id_to_order_shoe_id)
	for shoe_type_id in shoe_type_ids:
		## create ordershoetype
		shoe_type = shoe_type_id_to_shoe_type[shoe_type_id]
		shoe_id = shoe_type_id_to_shoe_id[shoe_type_id]
		order_shoe_id = shoe_id_to_order_shoe_id[shoe_id]
		quantity_mapping = shoe_type["quantityMapping"]
		batch_info = shoe_type["orderShoeTypeBatchInfo"]
		existing_entity = OrderShoeType.query.filter_by(
			order_shoe_id = order_shoe_id,
			shoe_type_id = shoe_type_id).first()
		if not existing_entity:
			new_entity = OrderShoeType(
				order_shoe_id = order_shoe_id,
				shoe_type_id = shoe_type_id)
			db.session.add(new_entity)
			db.session.flush()
		else:
			new_entity = existing_entity
		batch_info_entity_array = []
		for batch in batch_info:
			print(batch)
			quantity_per_ratio = int(quantity_mapping[str(batch['packagingInfoId'])])
			new_entity = OrderShoeBatchInfo(
				order_shoe_type_id = new_entity.order_shoe_type_id,
				name = batch['packagingInfoName'],
				size_34_amount = batch['size34Ratio']*quantity_per_ratio,
				size_35_amount = batch['size35Ratio']*quantity_per_ratio,
				size_36_amount = batch['size36Ratio']*quantity_per_ratio,
				size_37_amount = batch['size37Ratio']*quantity_per_ratio,
				size_38_amount = batch['size38Ratio']*quantity_per_ratio,
				size_39_amount = batch['size39Ratio']*quantity_per_ratio,
				size_40_amount = batch['size40Ratio']*quantity_per_ratio,
				size_41_amount = batch['size41Ratio']*quantity_per_ratio,
				size_42_amount = batch['size42Ratio']*quantity_per_ratio,
				size_43_amount = batch['size43Ratio']*quantity_per_ratio,
				size_44_amount = batch['size44Ratio']*quantity_per_ratio,
				size_45_amount = batch['size45Ratio']*quantity_per_ratio,
				size_46_amount = batch['size46Ratio']*quantity_per_ratio,
				price_per_pair = 0,
				total_price = 0,
				currency_type = "",
				total_amount = batch['totalQuantityRatio']*quantity_per_ratio,
				packaging_info_id = batch['packagingInfoId'],
				packaging_info_quantity = quantity_per_ratio)
			print(new_entity.size_34_amount)
			batch_info_entity_array.append(new_entity)
		db.session.add_all(batch_info_entity_array)
	db.session.commit()
	result = jsonify({"message": "Order imported successfully"}), 200
	# except Exception as e:
	# 	result = jsonify({"message": str(e)}, 500)
	time_t = time.time()
	print("time taken is " + str(time_t - time_s))
	return result

    # order_shoe_type_id = order_shoe_type.order_shoe_type_id  # Use order_shoe_type_id for the batch info

    # for item in items:
    #     order_shoe_batch = OrderShoeBatchInfo(
    #         order_shoe_type_id=order_shoe_type_id,  # Use the newly created or found order_shoe_type_id
    #         name=item["sizeId"],
    #         total_amount=item["pairCount"],
    #         cutting_amount=0,
    #         sewing_amount=0,
    #         pre_sewing_amount=0,
    #         molding_amount=0,
    #         size_34_amount=0,
    #         size_35_amount=item["7/35"],
    #         size_36_amount=item["7.5/36"],
    #         size_37_amount=item["8/37"],
    #         size_38_amount=item["8.5/38"],
    #         size_39_amount=item["9/39"],
    #         size_40_amount=item["9.5/40"],
    #         size_41_amount=item["10/41"],
    #         size_42_amount=item["10.5/42"],
    #         size_43_amount=item["11/43"],
    #         size_44_amount=item["12/44"],
    #         size_45_amount=item["13/45"],
    #         price_per_pair=item["pricePerPair"],
    #         total_price=item["totalPrice"],
    #         currency_type=item["currencyType"],
    #     )
    #     arr.append(order_shoe_batch)

    # db.session.add_all(arr)
    # db.session.commit()
@order_create_bp.route("/ordercreate/updateprice", methods=["POST"])
def order_price_update():
	unit_price_form = request.json.get('unitPriceForm')
	currency_type_form = request.json.get('currencyTypeForm')
	print(currency_type_form)
	for order_shoe_type_id in unit_price_form.keys():
		unit_price = float(unit_price_form[order_shoe_type_id])
		entities = (db.session.query(OrderShoeBatchInfo)
			.filter(OrderShoeBatchInfo.order_shoe_type_id == order_shoe_type_id)
			.all())
		for entity in entities:
			entity.price_per_pair = unit_price
			entity.total_price = unit_price * entity.total_amount
			db.session.commit()

	for order_shoe_type_id in currency_type_form.keys():
		currency_type = str(currency_type_form[order_shoe_type_id])
		entities = (db.session.query(OrderShoeBatchInfo)
			.filter(OrderShoeBatchInfo.order_shoe_type_id == order_shoe_type_id)
			.all())
		for entity in entities:
			entity.currency_type = currency_type
			db.session.commit()

	return jsonify({'msg':"ok"}), 200


@order_create_bp.route("/ordercreate/updateremark", methods=['POST'])
def order_remark_update():
	print(request.json)
	remark_form = request.json.get('orderShoeRemarkForm')
	order_shoe_id = remark_form['orderShoeId']
	business_technical_remark = remark_form['technicalRemark']
	business_material_remark = remark_form['materialRemark']
	order_shoe_entity = (db.session.query(OrderShoe)
		.filter(OrderShoe.order_shoe_id == order_shoe_id)
		.first())
	order_shoe_entity.business_material_remark = business_material_remark
	order_shoe_entity.business_technical_remark = business_technical_remark
	db.session.commit()

	return jsonify({'msg':"ok"}), 200