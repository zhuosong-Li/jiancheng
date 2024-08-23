from flask import Blueprint, jsonify, request

from app_config import app, db
from models import *

material_page_bp = Blueprint("material_page_bp", __name__)


@material_page_bp.route("/logistics/allmaterialtypes", methods=["GET"])
def get_all_materials():
    materials = (
        db.session.query(Material, MaterialWarehouse)
        .join(
            MaterialWarehouse,
            Material.warehouse_id == MaterialWarehouse.material_warehouse_id,
        )
    )
    result = []
    for material in materials:
        result.append(
            {
                "materialId": material.Material.material_id,
                "materialName": material.Material.material_name,
                "materialType": material.Material.material_type,
                "unit": material.Material.material_unit,
                "warehouseName": material.MaterialWarehouse.material_warehouse_name,
                "addDate": material.Material.material_creation_date.isoformat(),
            }
        )
    return jsonify(result)
