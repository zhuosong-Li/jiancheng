from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

color_bp = Blueprint("color_bp", __name__)

@color_bp.route("/general/allcolors", methods=["GET"])
def get_all_colors():
    colors = Color.query.all()
    result = []
    for color in colors:
        result.append(
            {
                "value": color.color_id,
                "label": color.color_name,
            }
        )
    return jsonify(result)