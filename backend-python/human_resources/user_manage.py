from flask import Blueprint, jsonify, request
import os
from app_config import app, db
from models import *
from constants import IMAGE_STORAGE_PATH, FILE_STORAGE_PATH, IMAGE_UPLOAD_PATH
from Crypto.Cipher import AES
import base64
import hashlib

user_manage_bp = Blueprint("user_manage_bp", __name__)


@user_manage_bp.route("/usermanage/getallusers", methods=["GET"])
def get_all_users():
    entities = (
        db.session.query(User, Staff, Character, Department)
        .join(Staff, User.staff_id == Staff.staff_id)
        .join(Character, Staff.character_id == Character.character_id)
        .join(Department, Staff.department_id == Department.department_id)
        .all()
    )
    result = []
    for entity in entities:
        result.append(
            {
                "userName": entity.User.user_name,
                "staffName": entity.Staff.staff_name,
                "characterName": entity.Character.character_name,
                "departmentName": entity.Department.department_name,
            }
        )
    return jsonify(result)

@user_manage_bp.route("/usermanage/createuser", methods=["POST"])
def create_user():
    user_name = request.json.get("userName")
    staff_name = request.json.get("staffName")
    character_id = request.json.get("characterId")
    department_id = request.json.get("departmentId")
    try:
        character = Character.query.filter_by(character_id=character_id).first()
        department = Department.query.filter_by(department_id=department_id).first()
        existing_staff = Staff.query.filter_by(staff_name=staff_name).first()
        if not existing_staff:
            staff = Staff(staff_name=staff_name, character_id=character.character_id, department_id=department.department_id)
            db.session.add(staff)
            db.session.commit()
        staff_id = Staff.query.filter_by(staff_name=staff_name).first().staff_id
        default_password = hashlib.md5("admin".encode()).hexdigest()
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            return jsonify({"error": "User name already exists"}), 400
        user = User(user_name=user_name, staff_id=staff_id, user_passwd=default_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
