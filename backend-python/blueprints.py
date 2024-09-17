from app_config import app
from production.price_report import price_report_bp
from shared_apis.order import order_bp
from production.quantity_report import quantity_report_bp
from logistics.logistics_home_page import logistics_home_page_bp
from logistics.supplier_page import supplier_page_bp
from logistics.warehouse_page import warehouse_page_bp
from logistics.material_page import material_page_bp
from production.production_manager import production_manager_bp
from logistics.assets_purchase_page import assets_purchase_page_bp
from shared_apis.color import color_bp
from logistics.first_bom import first_bom_bp
from shared_apis.department import department_bp
from usage_calculation.usage_calculation import usage_calculation_bp
from bussiness.order_import import order_import_bp
from shared_apis.customer import customer_bp
from shared_apis.shoe import shoe_bp
from development.shoe_manage import shoe_manage_bp
from development.dev_producion_order import dev_producion_order_bp
from warehouse.material_storage import material_storage_bp
from warehouse.semifinished_storage import semifinished_storage_bp
from warehouse.finished_storage import finished_storage_bp
from shared_apis.message import message_bp
from login.login import login_bp
from human_resources.user_manage import user_manage_bp
from shared_apis.user import user_bp
from logistics.first_purchase import first_purchase_bp


def register_blueprints():
    app.register_blueprint(price_report_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(quantity_report_bp)
    app.register_blueprint(logistics_home_page_bp)
    app.register_blueprint(supplier_page_bp)
    app.register_blueprint(warehouse_page_bp)
    app.register_blueprint(material_page_bp)
    app.register_blueprint(production_manager_bp)
    app.register_blueprint(assets_purchase_page_bp)
    app.register_blueprint(color_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(first_bom_bp)
    app.register_blueprint(usage_calculation_bp)
    app.register_blueprint(order_import_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(shoe_bp)
    app.register_blueprint(shoe_manage_bp)
    app.register_blueprint(dev_producion_order_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_manage_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(first_purchase_bp)
    app.register_blueprint(material_storage_bp)
    app.register_blueprint(semifinished_storage_bp)
    app.register_blueprint(finished_storage_bp)
    app.register_blueprint(message_bp)
