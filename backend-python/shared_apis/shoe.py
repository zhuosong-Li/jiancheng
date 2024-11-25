from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *
from file_locations import IMAGE_STORAGE_PATH
from api_utility import to_camel, to_snake
shoe_bp = Blueprint("shoe_bp", __name__)

SHOE_TABLE_ATTRNAMES = Shoe.__table__.columns.keys()
SHOETYPE_TABLE_ATTRNAMES = ShoeType.__table__.columns.keys()
@shoe_bp.route("/shoe/getallshoes", methods=["GET"])
def get_all_shoes():
    shoe_rid = request.args.get("shoerid")
    if shoe_rid is None:
        shoes = (
            db.session.query(Shoe, ShoeType, Color)
            .join(ShoeType, Shoe.shoe_id == ShoeType.shoe_id)
            .join(Color, ShoeType.color_id == Color.color_id)
            .all()
        )
    else:
        shoes = (
            db.session.query(Shoe, ShoeType, Color)
            .join(ShoeType, Shoe.shoe_id == ShoeType.shoe_id)
            .join(Color, ShoeType.color_id == Color.color_id)
            .filter(Shoe.shoe_rid.like(f"%{shoe_rid}%"))
            .all()
        )
    result = []
    for shoe, shoe_type, color in shoes:
        result.append(
            {
                "shoeId": shoe.shoe_id,
                "shoeTypeId": shoe_type.shoe_type_id,
                "shoeRId": shoe.shoe_rid,
                "shoeImage": shoe_type.shoe_image_url,
                "shoeDesigner": shoe.shoe_designer,
                "shoeColor": color.color_name,
                "shoeImage": (
                    IMAGE_STORAGE_PATH + shoe_type.shoe_image_url
                    if shoe_type.shoe_image_url is not None
                    else None
                ),
            }
        )
    print(result)
    return jsonify(result)


@shoe_bp.route("/shoe/getallshoesnew", methods=["GET"])
def get_all_shoes_new():
    shoe_entities = (
        db.session.query(Shoe)
    ).all()
    result_data = []
    for shoe in shoe_entities:
        shoe_response_data = dict()
        for attr in SHOE_TABLE_ATTRNAMES:
            shoe_response_data[to_camel(attr)] = getattr(shoe, attr)
        shoe_type_entities = (db.session.query(ShoeType, Color)
                              .join(Color, ShoeType.color_id == Color.color_id)
                              .filter(ShoeType.shoe_id == shoe.shoe_id)
                              .all())
        shoe_type_list = []
        for shoe_type in shoe_type_entities:
            print(shoe_type)
            shoe_type_response_data = dict()
            for attr in SHOETYPE_TABLE_ATTRNAMES:
                shoe_type_response_data[to_camel(attr)] = getattr(shoe_type.ShoeType, attr)
                shoe_type_response_data['colorName'] = shoe_type.Color.color_name
            shoe_type_list.append(shoe_type_response_data)
        shoe_response_data['shoeTypeData'] = shoe_type_list
        print(shoe_response_data)
        result_data.append(shoe_response_data)
    print(result_data)
    return jsonify(result_data), 200


# @shoe_bp.route("/shoe/addnewshoe", methods=["GET"])
# def add_new_shoe():
