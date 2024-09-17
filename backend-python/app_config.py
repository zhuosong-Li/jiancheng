import json
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
import redis

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Database configuration
db_username = "jiancheng_dev1"
db_password = "12345678Ab"
db_name = "jiangcheng_test"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{db_username}:{db_password}@rm-wz9lp07aju9k1c1jrvo.mysql.rds.aliyuncs.com/{db_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "EC63AF9BA57B9F20"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

# Serializer for URL-safe tokens
serializer = URLSafeTimedSerializer(app.secret_key)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "EC63AF9BA57B9F20"  # Set your secret key
jwt = JWTManager(app)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Initialize database
db = SQLAlchemy(app)

# List of public routes that do not require authentication
open_routes = ['/login',"/devproductionorder/download", '/orderimport/downloadorderdoc']

@app.before_request
def authenticate():
    # Skip authentication for open routes
    if request.path not in open_routes:
        try:
            # Use the JWT method to verify the token automatically
            verify_jwt_in_request()
        except Exception as e:
            # Handle failed authentication (e.g., invalid or expired token)
            return jsonify({"msg": "Authentication required", "error": str(e)}), 401

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    
    # Check if the `jti` exists in Redis
    token_in_redis = redis_client.get(jti)
    
    # If the token is not found in Redis, it's considered revoked
    return token_in_redis is None


