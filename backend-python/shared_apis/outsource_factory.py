from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

outsource_factory_bp = Blueprint("outsource_factory_bp", __name__)

@outsource_factory_bp.route("/general/getalloutsourcefactories", methods=["GET"])
def get_all_outsource_factories():
    factories = OutsourceFactory.query.all()
    result = []
    for factory in factories:
        result.append(
            {
                "id": factory.factory_id,
                "value": factory.factory_name,
            }
        )
    return jsonify(result)
