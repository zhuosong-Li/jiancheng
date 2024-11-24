from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, jwt_required, get_jwt_identity, decode_token
from app_config import app, db, redis_client, jwt
from app_config import app, db
from models import *
from login.login import decrypt_password
import hashlib

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

@user_bp.route("/general/getcurrentstaffandcharacter", methods=["GET"])
def get_current_staff_and_character():
    token = request.headers.get("Authorization")[7:]
    decoded_token = decode_token(token)  # Decode the created token
    jti = decoded_token["jti"]  # Extract the `jti` from the token payload
    for key in redis_client.scan_iter():
        value = redis_client.get(key)
        if value == jti:
            user = db.session.query(User, Staff, Character).join(
                Staff, User.staff_id == Staff.staff_id).join(
                Character, Staff.character_id == Character.character_id
            ).filter(User.user_name == get_jwt_identity()).first()
            result = {
                "staffName": user.Staff.staff_name,
                "characterName": user.Character.character_name,
            }
            return jsonify(result)


    return {"error": "Key not found for given jti"}, 404

@user_bp.route("/user/changepassword", methods=["POST"])
def change_password():
    data = request.get_json()
    old_password = data.get("currentPassword")
    new_password = data.get("newPassword")
    staff_id = data.get("staffId")
    iv = data.get("iv")  # Get the IV from the request
    print(data)
    secret_key = "6f8e6f9178b12c08dce94bcf57b8df22"  # Same key used in the frontend
    decrypt_old_password_result = decrypt_password(old_password, iv, secret_key)
    second_encrypted_password = hashlib.md5(decrypt_old_password_result.encode()).hexdigest()
    decrypt_new_password_result = decrypt_password(new_password, iv, secret_key)
    second_encrypted_new_password = hashlib.md5(decrypt_new_password_result.encode()).hexdigest()

    user = db.session.query(User, Staff, Character).join(
        Staff, User.staff_id == Staff.staff_id).join(
        Character, Staff.character_id == Character.character_id
    ).filter(Staff.staff_id == staff_id).first()
    print(user)

    if user and user.User.user_passwd == second_encrypted_password:
        user.User.user_passwd = second_encrypted_new_password
        db.session.commit()
        return {"success": "Password changed successfully"}, 200
    
    return {"error": "Old password is incorrect"}, 400

