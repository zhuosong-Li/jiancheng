from app_config import app
from production.price_report import price_report_bp
from shared_apis.order import order_bp
from production.cutting_quantity_report import cutting_quantity_report_bp


def register_blueprints():
    app.register_blueprint(price_report_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cutting_quantity_report_bp)
