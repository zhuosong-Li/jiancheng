from models import *

from event_processor import *
import random
import string


### check if a shoe exists in DB
def check_shoe_exists(shoe_rid):
    existance = (
        db.session.query(Shoe.shoe_rid).filter(Shoe.shoe_rid == shoe_rid).first()
    )
    result = existance != None
    return result


### check if customer exists in DB by ID
def check_customerId_exists(customer_id):
    existance = (
        db.session.query(Customer.customer_id)
        .filter(Customer.customer_id == customer_id)
        .first()
    )
    result = existance != None
    return result


### get customer ID by name
def get_customerId(customer_name):
    query_entity = (
        db.session.query(Customer.customer_name, Customer.customer_id)
        .filter(Customer.customer_name == customer_name)
        .first()
    )
    result = query_entity.customer_id
    return result


### check if customer exists in DB by Name
def check_customerName_exists(customer_name):
    existance = (
        db.session.query(Customer.customer_name)
        .filter(Customer.customer_name == customer_name)
        .first()
    )
    result = existance != None
    return result


def check_orderRid_exists(order_rid):
    existance = (
        db.session.query(Order.order_rid).filter(Order.order_rid == order_rid).first()
    )
    result = existance != None
    return result


### create and insert new shoe entity
def dbcreateShoe(shoe_rid, img_url):
    db_entity = Shoe(shoe_rid=shoe_rid, shoe_image_url=img_url)
    db.session.add(db_entity)
    db.session.commit()
    return True


###
def dbcreateCustomer(customer_Name):
    db_entity = Customer(customer_name=customer_Name)
    db.session.add(db_entity)
    db.session.commit()
    return True


def dbcreateOrder(order_Rid, order_createTime, order_Customer):
    db_entity = Order(
        order_rid=order_Rid,
        order_createtime=order_createTime,
        order_customer=order_Customer,
    )
    db.session.add(db_entity)
    db.session.commit()
    return True


def processEvent(event):
    return


def randomIdGenerater(digit):
    random_str = "".join(random.choices(string.digits, k=digit))
    return random_str


def format_date(date_obj):
    if not date_obj:
        return ""
    return date_obj.strftime("%Y-%m-%d")


def format_line_group(line_group_obj):
    if not line_group_obj:
        return []
    return line_group_obj.split(",")
