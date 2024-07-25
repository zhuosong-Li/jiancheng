import json
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
CORS(app, supports_credentials=True)

db_username = "jiancheng_dev1"
db_password = "12345678Ab"
db_name = "jiancheng_test3"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_username}:{db_password}@rm-wz9lp07aju9k1c1jrvo.mysql.rds.aliyuncs.com/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "EC63AF9BA57B9F20"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
serializer = URLSafeTimedSerializer(app.secret_key)
db = SQLAlchemy(app)
