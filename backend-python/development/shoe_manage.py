from flask import Blueprint, jsonify, request
import os
from app_config import app, db
from models import *
from file_locations import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH

shoe_manage_bp = Blueprint("shoe_manage_bp", __name__)


@shoe_manage_bp.route("/shoemanage/uploadshoeimage", methods=["POST"])
def upload_shoe_image():
    print(request.form)
    shoe_rid = request.form.get("shoeRId")
    shoe_color = request.form.get("shoeColor")
    print(shoe_rid)
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 500
    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 500

    folder_path = os.path.join(IMAGE_UPLOAD_PATH, "shoe", shoe_rid, shoe_color)
    if os.path.exists(folder_path) == False:
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, "shoe_image.jpg")
    file.save(file_path)
    shoe_type = (
        db.session.query(Shoe, ShoeType, Color)
        .join(ShoeType, Shoe.shoe_id == ShoeType.shoe_id)
        .join(Color, ShoeType.color_id == Color.color_id)
        .filter(Shoe.shoe_rid == shoe_rid)
        .filter(Color.color_name == shoe_color)
        .first()
    )
    db_path = os.path.join("shoe", shoe_rid, shoe_color, "shoe_image.jpg")
    shoe_type.ShoeType.shoe_image_url = db_path
    db.session.commit()
    return jsonify({"message": "Shoe image uploaded successfully"})


@shoe_manage_bp.route("/shoemanage/addnewshoe", methods=["POST"])
def add_new_shoe():
    shoe_rid = request.json.get("shoeRId")
    shoe_designer = request.json.get("shoeDesigner")
    shoe_color = request.json.get("shoeColor")
    try:
        shoe = Shoe(
            shoe_rid=shoe_rid,
            shoe_designer=shoe_designer,
        )
        db.session.add(shoe)
        db.session.commit()
        shoe_type = ShoeType(shoe_id=shoe.shoe_id, color_id=shoe_color)
        db.session.add(shoe_type)
        db.session.commit()
        return jsonify({"message": "Shoe added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@shoe_manage_bp.route("/shoemanage/editshoe", methods=["POST"])
def edit_shoe():
    shoe_id = request.json.get("shoeId")
    shoe_rid = request.json.get("shoeRId")
    shoe_designer = request.json.get("shoeDesigner")
    try:
        shoe = Shoe.query.get(shoe_id)
        shoe.shoe_rid = shoe_rid
        shoe.shoe_designer = shoe_designer
        db.session.commit()
        return jsonify({"message": "Shoe updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
