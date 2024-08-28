import constants
import time
from app_config import db
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from constants import IN_PRODUCTION_ORDER_NUMBER

from models import *
from sqlalchemy import or_, text
from datetime import datetime

message_bp = Blueprint("message_bp", __name__)

@message_bp.route("/message/sendmessage", methods=["POST"])
def send_message():
    data = request.get_json()
    sender_id = data["senderId"]
    receiver_ids = data["receiverIds"]
    content = data["content"]
    arr = []
    for receiver_id in receiver_ids:
        message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content, send_datetime=datetime.now())
        arr.append(message)
    db.session.add_all(arr)
    db.session.commit()
    return jsonify({"message": "success"})

@message_bp.route("/message/getmessages", methods=["GET"])
def get_messages():
    receiver_id = request.args.get("receiver_id")
    result = []
    response = Message.query.filter(Message.receiver_id == receiver_id).all()
    for row in response:
        obj = {
            "content": row.content,
            "isViewed": row.is_viewed
        }
        result.append(obj)
    return result