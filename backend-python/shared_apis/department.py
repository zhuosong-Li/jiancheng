from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

department_bp = Blueprint("department_bp", __name__)

@department_bp.route("/general/getalldepartments", methods=["GET"])
def get_all_departments():
    departments = Department.query.all()
    result = []
    for department in departments:
        result.append(
            {
                "value": department.department_id,
                "label": department.department_name,
            }
        )
    return jsonify(result)