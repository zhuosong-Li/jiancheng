from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *
from constants import IMAGE_STORAGE_PATH

shoe_bp = Blueprint("shoe_bp", __name__)


@shoe_bp.route("/shoe/getallshoes", methods=["GET"])
def get_all_shoes():
    shoe_rid = request.args.get("shoerid")
    if shoe_rid is None:
        shoes = Shoe.query.all()
    else:
        shoes = db.session.query(Shoe).filter(Shoe.shoe_rid.like(f"%{shoe_rid}%")).all()
    result = []
    for shoe in shoes:
        result.append(
            {
                "shoeRId": shoe.shoe_rid,
                "shoeImage": shoe.shoe_image_url,
                "shoeDesigner": shoe.shoe_designer,
                "shoeAdjuster": shoe.shoe_adjuster,
                "shoeImage": (
                    IMAGE_STORAGE_PATH + shoe.shoe_image_url
                    if shoe.shoe_image_url is not None
                    else None
                ),
            }
        )
    return jsonify(result)
