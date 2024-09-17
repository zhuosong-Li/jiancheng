from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/general/getallcharacters", methods=["GET"])
def get_all_characters():
    characters = Character.query.all()
    result = []
    for character in characters:
        result.append(
            {
                "value": character.character_id,
                "label": character.character_name,
            }
        )
    return jsonify(result)

@user_bp.route("/general/getallstaffs", methods=["GET"])
def get_all_staffs():
    staffs = Staff.query.all()
    result = []
    for staff in staffs:
        result.append(
            {
                "value": staff.staff_id,
                "label": staff.staff_name,
            }
        )
    return jsonify(result)