from app_config import app
from production.price_report import price_report_bp
from shared_apis.order import order_bp
from production.quantity_report import quantity_report_bp
from production.production_manager import production_manager_bp


def register_blueprints():
    app.register_blueprint(price_report_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(quantity_report_bp)
    app.register_blueprint(production_manager_bp)
