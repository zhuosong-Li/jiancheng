from flask import Flask, jsonify, request
from mysql.connector.pooling import *
from flask_cors import CORS
from sqlalchemy import Column, Integer, String, Float, text, Engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime

app = Flask(__name__)
CORS(app)
dbconfig = {
    'dialect': 'mysql',
    'driver': 'mysqlconnector',
    'username': 'jiancheng_dev3',
    'password': '12345678Ab',
    'host': 'rm-wz9lp07aju9k1c1jrvo.mysql.rds.aliyuncs.com',
    'port': 3306,
    'database': 'jiancheng_test3'
}
DATABASE_URL = f"{dbconfig['dialect']}+{dbconfig['driver']}://{dbconfig['username']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['database']}"
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,        # The size of the pool to be maintained
    'max_overflow': 20,     # The number of connections to allow in overflow
    'pool_recycle': 1800,   # Number of seconds to recycle a connection
    'pool_timeout': 30      # Number of seconds to wait before giving up on getting a connection from the pool
}

db = SQLAlchemy(app)

class FabricCuttingUnitPrice(db.Model):
    __tablename__ = 'fabriccuttingunitprice'
    name: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    price: Mapped[float] = mapped_column(nullable=False)
    test: Mapped[int] = mapped_column()

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Orders(db.Model):
    __tablename__ = 'orders'
    orderId: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    createdDate: Mapped[date] = mapped_column(nullable=False)
    prevDepartment: Mapped[str] = mapped_column(String(10))
    prevSupervisor: Mapped[str] = mapped_column(String(20))
    prevStepSummitTime: Mapped[datetime] = mapped_column(String(50))
    currentDepartment: Mapped[str] = mapped_column(String(20), nullable=False)
    currentUnit: Mapped[str] = mapped_column(String(20))
    currentStep: Mapped[str] = mapped_column(String(50), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class PriceReportInfo(db.Model):
    __tablename__ = 'pricereportinfo'
    orderId: Mapped[str] = mapped_column(String(50), primary_key=True)
    shoeTypeId: Mapped[str] = mapped_column(String(50), primary_key=True)
    createdDate: Mapped[date] = mapped_column(nullable=False)
    priceReportType: Mapped[str] = mapped_column(String(10), nullable=False)
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class PriceReportContent(db.Model):
    __tablename__ = 'pricereportcontent'
    shoeTypeId: Mapped[str] = mapped_column(String(50), primary_key=True)
    createdDate: Mapped[date] = mapped_column(primary_key=True)
    procedure: Mapped[str] = mapped_column(String(50), primary_key=True)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route('/fabriccutting/getunitprice', methods=['GET'])
def getUnitPrice():
    results: list[FabricCuttingUnitPrice] = FabricCuttingUnitPrice.query.all()
    res = {}
    for row in results:
        res[row.name] = row.price

    return jsonify(res)

@app.route('/fabriccutting/getactiveorders', methods=['GET'])
def getActiveOrders():
    results: list[Orders]
    results = Orders.query.filter(Orders.currentDepartment=='生产部', Orders.currentStep=='工价填报')
    res_list = [row.as_dict() for row in results]
    return jsonify(res_list)

@app.route('/fabriccutting/getallpricereport', methods=['GET'])
def getAllPriceReport():
    orderId = request.args.get('orderId')
    results: list[PriceReportInfo]
    results = PriceReportInfo.query.filter(PriceReportInfo.orderId==orderId)
    res_list = [row.as_dict() for row in results]
    return jsonify(res_list)

@app.route('/fabriccutting/storepricereport', methods=['POST'])
def storePriceReport():
    data = request.json
    for row in data:
        obj = PriceReportContent(shoeTypeId=row["shoeTypeId"], createdDate=row["createdDate"], procedure=row["procedure"])
        db.session.add(obj)
        db.session.commit()
    return jsonify({'message': 'Data received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
