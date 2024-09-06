from flask import Blueprint, jsonify, request
import os
from app_config import app, db
from models import *
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH

shoe_manage_bp = Blueprint("shoe_manage_bp", __name__)

@shoe_manage_bp.route("/shoemanage/uploadshoeimage", methods=["POST"])
def upload_shoe_image():
    print(request.form)
    shoe_rid = request.form.get("shoeRId")
    print(shoe_rid)
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 500
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 500
    folder_path = os.path.join(IMAGE_UPLOAD_PATH, "shoe", shoe_rid)
    if os.path.exists(folder_path) == False:
        os.mkdir(folder_path)
    file_path = os.path.join(folder_path, "shoe_image.jpg")
    file.save(file_path)
    shoe = Shoe.query.filter_by(shoe_rid=shoe_rid).first()
    db_path = os.path.join("shoe", shoe_rid, "shoe_image.jpg")
    shoe.shoe_image_url = db_path
    db.session.commit()
    return jsonify({"message": "Shoe image uploaded successfully"})

@shoe_manage_bp.route("/shoemanage/addnewshoe", methods=["POST"])
def add_new_shoe():
    shoe_rid = request.json.get("shoeRId")
    shoe_designer = request.json.get("shoeDesigner")
    shoe_adjuster = request.json.get("shoeAdjuster")
    try:
        shoe = Shoe(
            shoe_rid=shoe_rid,
            shoe_designer=shoe_designer,
            shoe_adjuster=shoe_adjuster,
        )
        db.session.add(shoe)
        db.session.commit()
        return jsonify({"message": "Shoe added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@shoe_manage_bp.route("/shoemanage/editshoe", methods=["POST"])
def edit_shoe():
    shoe_rid = request.json.get("shoeRId")
    shoe_designer = request.json.get("shoeDesigner")
    shoe_adjuster = request.json.get("shoeAdjuster")
    try:
        shoe = Shoe.query.filter_by(shoe_rid=shoe_rid).first()
        shoe.shoe_designer = shoe_designer
        shoe.shoe_adjuster = shoe_adjuster
        db.session.commit()
        return jsonify({"message": "Shoe updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

