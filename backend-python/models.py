from app_config import db


class BomItem(db.Model):
    __tablename__ = "bom_item"
    bom_item_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    material_id = db.Column(
        db.BigInteger, db.ForeignKey("material.material_id"), nullable=False
    )
    unit_usage = db.Column(db.Numeric(10, 5), nullable=False)
    total_usage = db.Column(db.Numeric(10, 5), nullable=False)
    department = db.Column(
        db.Integer, db.ForeignKey("department.department_id"), nullable=True
    )
    remark = db.Column(db.String(100), nullable=True)
    bom_id = db.Column(db.BigInteger, db.ForeignKey("bom.bom_id"), nullable=False)

    def __repr__(self):
        return f"<BomItem(bom_item_id={self.bom_item_id})>"


class Bom(db.Model):
    __tablename__ = "bom"
    bom_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    bom_rid = db.Column(db.String(80), nullable=False)
    bom_type = db.Column(db.Integer, nullable=False)
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=False
    )

    def __repr__(self):
        return f"<Bom(bom_id={self.bom_id})>"


class Character(db.Model):
    __tablename__ = "character"
    character_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<Character(character_id={self.character_id})>"


class Color(db.Model):
    __tablename__ = "color"
    color_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    color_name = db.Column(db.String(30), nullable=False)
    color_en_name = db.Column(db.String(50), nullable=True)
    color_sp_name = db.Column(db.String(50), nullable=True)
    color_it_name = db.Column(db.String(40), nullable=True)

    def __repr__(self):
        return f"<Color(color_id={self.color_id})>"


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id})>"


class CuttingQuantityReportItem(db.Model):
    __tablename__ = "cutting_quantity_report_item"
    report_id = db.Column(
        db.BigInteger,
        db.ForeignKey("cutting_quantity_report.report_id"),
        primary_key=True,
        nullable=False,
    )
    order_shoe_batch_info_id = db.Column(
        db.BigInteger,
        db.ForeignKey("order_shoe_batch_info.order_shoe_batch_info_id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<CuttingQuantityReportItem(report_id={self.report_id}, order_shoe_batch_info_id={self.order_shoe_batch_info_id})>"


class CuttingQuantityReport(db.Model):
    __tablename__ = "cutting_quantity_report"
    report_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=True
    )
    creation_date = db.Column(db.Date, nullable=True)
    submission_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)
    rejection_reason = db.Column(db.String(40))

    def __repr__(self):
        return f"<CuttingQuantityReport(report_id={self.report_id})>"


class Department(db.Model):
    __tablename__ = "department"
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Department(department_id={self.department_id})>"


class Material(db.Model):
    __tablename__ = "material"
    material_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String(60), nullable=False)
    material_unit = db.Column(db.String(4), nullable=True)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey("supplier.supplier_id"), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer,
        db.ForeignKey("material_warehouse.material_warehouse_id"),
        nullable=False,
    )
    shoe_part_id = db.Column(
        db.Integer, db.ForeignKey("shoe_part.shoe_part_id"), nullable=False
    )
    material_creation_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Material(material_id={self.material_id})>"


class Event(db.Model):
    __tablename__ = "event"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"), nullable=False)
    handle_time = db.Column(db.DateTime, nullable=False)
    operation_id = db.Column(
        db.Integer, db.ForeignKey("operation.operation_id"), nullable=False
    )
    event_order_id = db.Column(db.BigInteger, nullable=True)
    event_order_shoe_id = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return f"<Event(event_id={self.event_id})>"


class MoldingQuantityReportItem(db.Model):
    __tablename__ = "molding_quantity_report_item"
    report_id = db.Column(
        db.BigInteger,
        db.ForeignKey("molding_quantity_report.report_id"),
        primary_key=True,
        nullable=False,
    )
    order_shoe_batch_info_id = db.Column(
        db.BigInteger,
        db.ForeignKey("order_shoe_batch_info.order_shoe_batch_info_id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<MoldingQuantityReportItem(report_id={self.report_id}, order_shoe_batch_info_id={self.order_shoe_batch_info_id})>"

    def __name__(self):
        return "MoldingQuantityReportInfo"


class MoldingQuantityReport(db.Model):
    __tablename__ = "molding_quantity_report"
    report_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    order_shoe_id = db.Column(
        db.BigInteger,
        db.ForeignKey("order_shoe.order_shoe_id"),
        unique=True,
        nullable=True,
    )
    creation_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)
    rejection_reason = db.Column(db.String(40))

    def __repr__(self):
        return f"<MoldingQuantityReport(report_id={self.report_id})>"

    def __name__(self):
        return "MoldingQuantityReport"


class MaterialStorage(db.Model):
    __tablename__ = "material_storage"
    material_storage_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=True
    )
    material_id = db.Column(
        db.BigInteger, db.ForeignKey("material.material_id"), nullable=False
    )

    def __repr__(self):
        return f"<MaterialStorage(material_storage_id={self.material_storage_id})>"

    def __name__(self):
        return "MaterialStorage"


class Operation(db.Model):
    __tablename__ = "operation"
    operation_id = db.Column(db.Integer, primary_key=True)
    operation_name = db.Column(db.String(40), nullable=False)
    operation_type = db.Column(db.Integer, nullable=False, default=0)
    operation_modified_status = db.Column(db.Integer, nullable=True)
    operation_modified_value = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Operation(operation_id={self.operation_id})>"

    def __name__(self):
        return "Operation"


class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_rid = db.Column(db.String(40), nullable=False, unique=True)
    creation_time = db.Column(db.Date, nullable=False)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customer.customer_id"), nullable=False
    )

    def __repr__(self):
        return f"<Order(order_id={self.order_id})>"

    def __name__(self):
        return "Order"


class OrderShoeStatus(db.Model):
    __tablename__ = "order_shoe_status"
    order_shoe_status_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=False
    )
    current_status = db.Column(
        db.Integer,
        db.ForeignKey("order_shoe_status_reference.status_id"),
        nullable=False,
    )
    current_status_value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<OrderShoeStatus(order_shoe_status_id={self.order_shoe_status_id})>"


class OrderShoeBatchInfo(db.Model):
    __tablename__ = "order_shoe_batch_info"
    order_shoe_batch_info_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    name = db.Column(db.String(20), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey("color.color_id"), nullable=False)
    total_amount = db.Column(db.Integer, nullable=True)
    cutting_amount = db.Column(db.Integer, nullable=True)
    sewing_amount = db.Column(db.Integer, nullable=True)
    molding_amount = db.Column(db.Integer, nullable=True)
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=False
    )

    def __repr__(self):
        return f"<OrderShoeBatchInfo(order_shoe_batch_info_id={self.order_shoe_batch_info_id})>"

    def __name__(self):
        return "OrderShoeBatchInfo"


class OrderShoe(db.Model):
    __tablename__ = "order_shoe"
    order_shoe_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    shoe_id = db.Column(db.Integer, db.ForeignKey("shoe.shoe_id"), nullable=False)
    order_id = db.Column(db.BigInteger, db.ForeignKey("order.order_id"), nullable=False)
    customer_product_name = db.Column(db.String(30), nullable=False)
    cutting_line_number = db.Column(db.Integer, nullable=True)
    sewing_line_number = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<OrderShoe(order_shoe_id={self.order_shoe_id})>"

    def __name__(self):
        return "OrderShoe"


class OrderShoeStatusReference(db.Model):
    __tablename__ = "order_shoe_status_reference"
    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<OrderShoeStatusReference(status_id={self.status_id})>"

    def __name__(self):
        return "OrderShoeStatusReference"


class OrderStatus(db.Model):
    __tablename__ = "order_status"
    order_status_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    order_current_status = db.Column(
        db.Integer,
        db.ForeignKey("order_status_reference.order_status_id"),
        nullable=False,
    )
    order_status_value = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.BigInteger, db.ForeignKey("order.order_id"), nullable=False)

    def __repr__(self):
        return f"<OrderStatus(order_status_id={self.order_status_id})>"

    def __name__(self):
        return "OrderStatus"


class OrderStatusReference(db.Model):
    __tablename__ = "order_status_reference"
    order_status_id = db.Column(db.Integer, primary_key=True)
    order_status_name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<OrderStatusReference(order_status_id={self.order_status_id})>"

    def __name__(self):
        return "OrderStatusReference"


class ProcedureReference(db.Model):
    __tablename__ = "procedure_reference"
    procedure_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    procedure_name = db.Column(db.String(100), nullable=False)
    team = db.Column(db.String(10), nullable=True)
    current_price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<ProcedureReference(procedure_id={self.procedure_id})>"

    def __name__(self):
        return "ProcedureReference"


class PurchaseOrderItem(db.Model):
    __tablename__ = "purchase_order_item"
    purchase_order_item_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    bom_item_id = db.Column(
        db.BigInteger, db.ForeignKey("bom_item.bom_item_id"), nullable=False
    )
    purchase_divide_order_id = db.Column(
        db.BigInteger,
        db.ForeignKey("purchase_divide_order.purchase_divide_order_id"),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"<PurchaseOrderItem(purchase_order_item_id={self.purchase_order_item_id})>"
        )

    def __name__(self):
        return "PurchaseOrderItem"


class PurchaseDivideOrder(db.Model):
    __tablename__ = "purchase_divide_order"
    purchase_divide_order_id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    purchase_order_id = db.Column(
        db.BigInteger, db.ForeignKey("purchase_order.purchase_order_id"), nullable=False
    )

    def __repr__(self):
        return f"<PurchaseDivideOrder(purchase_divide_order_id={self.purchase_divide_order_id})>"


class PurchaseOrder(db.Model):
    __tablename__ = "purchase_order"
    purchase_order_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    bom_id = db.Column(db.BigInteger, db.ForeignKey("bom.bom_id"), nullable=True)
    purchase_order_rid = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<PurchaseOrder(purchase_order_id={self.purchase_order_id})>"


class SewingQuantityReportItem(db.Model):
    __tablename__ = "sewing_quantity_report_item"
    report_id = db.Column(
        db.BigInteger,
        db.ForeignKey("sewing_quantity_report.report_id"),
        primary_key=True,
        nullable=False,
    )
    order_shoe_batch_info_id = db.Column(
        db.BigInteger,
        db.ForeignKey("order_shoe_batch_info.order_shoe_batch_info_id"),
        primary_key=True,
        nullable=False,
    )
    amount = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<SewingQuantityReportItem(report_id={self.report_id}, order_shoe_batch_info_id={self.order_shoe_batch_info_id})>"

    def __name__(self):
        return "SewingQuantityReportInfo"


class SewingQuantityReport(db.Model):
    __tablename__ = "sewing_quantity_report"
    report_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    order_shoe_id = db.Column(
        db.BigInteger,
        db.ForeignKey("order_shoe.order_shoe_id"),
        unique=True,
        nullable=True,
    )
    creation_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.SmallInteger, nullable=True)
    rejection_reason = db.Column(db.String(40))

    def __repr__(self):
        return f"<SewingQuantityReport(report_id={self.report_id})>"

    def __name__(self):
        return "SewingQuantityReport"


class Shoe(db.Model):
    __tablename__ = "shoe"
    shoe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shoe_rid = db.Column(db.String(20), nullable=False)
    shoe_image_url = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<Shoe(shoe_id={self.shoe_id})>"

    def __name__(self):
        return "Shoe"


class ShoePart(db.Model):
    __tablename__ = "shoe_part"
    shoe_part_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shoe_part_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"<ShoePart(shoe_part_id={self.shoe_part_id})>"

    def __name__(self):
        return "ShoePart"


class Staff(db.Model):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_name = db.Column(db.String(20), nullable=False)
    character_id = db.Column(
        db.Integer, db.ForeignKey("character.character_id"), nullable=False
    )
    department_id = db.Column(
        db.Integer, db.ForeignKey("department.department_id"), nullable=False
    )

    def __repr__(self):
        return f"<Staff(staff_id={self.staff_id})>"

    def __name__(self):
        return "Staff"


class Supplier(db.Model):
    __tablename__ = "supplier"
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Supplier(supplier_id={self.supplier_id})>"

    def __name__(self):
        return "Supplier"


class UnitPrice(db.Model):
    __tablename__ = "unit_price"
    procedure_id = db.Column(db.BigInteger, primary_key=True)
    creation_date = db.Column(db.Date, primary_key=True)
    price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<UnitPrice(procedure_id={self.procedure_id}, creation_date={self.creation_date})>"


class UnitPriceReportDetail(db.Model):
    __tablename__ = "unit_price_report_detail"
    report_id = db.Column(
        db.BigInteger,
        db.ForeignKey("unit_price_report.report_id"),
        primary_key=True,
        nullable=False,
    )
    row_id = db.Column(
        db.Integer,
        primary_key=True,
        nullable=False,
    )
    procedure_id = db.Column(
        db.BigInteger,
        db.ForeignKey("procedure_reference.procedure_id"),
        primary_key=True,
        nullable=False,
    )
    price = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(600), nullable=True)

    def __repr__(self):
        return f"<UnitPriceReportDetail(report_id={self.report_id}, row_id={self.row_id}, procedure_id={self.procedure_id}, note={self.note})>"


class UnitPriceReport(db.Model):
    __tablename__ = "unit_price_report"
    report_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=True
    )
    submission_date = db.Column(db.Date, nullable=True)
    team = db.Column(db.String(10), nullable=True)
    status = db.Column(db.SmallInteger, nullable=False)
    rejection_reason = db.Column(db.String(40))

    def __repr__(self):
        return f"<UnitPriceReport(report_id={self.report_id})>"

    def to_dict(obj):
        """Convert SQLAlchemy object to dictionary."""
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class MaterialWarehouse(db.Model):
    __tablename__ = "material_warehouse"
    material_warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_warehouse_name = db.Column(db.String(20), nullable=False)
    material_warehouse_creation_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Warehouse(material_warehouse_id={self.material_warehouse_id})>"


class TransitWarehouseItem(db.Model):
    __tablename__ = "transit_warehouse_item"
    transit_warehouse_item_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    transit_order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=False
    )
    transit_instore_amount = db.Column(db.Integer, nullable=False)
    transit_status = db.Column(db.SmallInteger, nullable=False)
    transit_instore_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return (
            f"<TransitWarehouseItem(transit_warehouse_item_id={self.transit_warehouse_item_id}, "
            f"transit_order_shoe_id={self.transit_order_shoe_id}, "
            f"transit_instore_amount={self.transit_instore_amount}, "
            f"transit_status={self.transit_status}, "
            f"transit_instore_time={self.transit_instore_time})>"
        )


class FinishedWarehouseItem(db.Model):
    __tablename__ = "finished_warehouse_item"
    finished_warehouse_item_id = db.Column(
        db.BigInteger, primary_key=True, nullable=False, autoincrement=True
    )
    finished_order_shoe_id = db.Column(
        db.BigInteger, db.ForeignKey("order_shoe.order_shoe_id"), nullable=False
    )
    finished_instore_amount = db.Column(db.Integer, nullable=False)
    finished_status = db.Column(db.SmallInteger, nullable=False)
    finished_instore_time = db.Column(db.DateTime, nullable=False)

    # Define the relationship to OrderShoe
    order_shoe = db.relationship(
        "OrderShoe", backref=db.backref("finished_warehouse_items", lazy=True)
    )

    def __repr__(self):
        return (
            f"<FinishedWarehouseItem(finished_warehouse_item_id={self.finished_warehouse_item_id}, "
            f"finished_order_shoe_id={self.finished_order_shoe_id}, "
            f"finished_instore_amount={self.finished_instore_amount}, "
            f"finished_status={self.finished_status}, "
            f"finished_instore_time={self.finished_instore_time})>"
        )
