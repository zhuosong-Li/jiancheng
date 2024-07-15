#from ..app_config import app, db

from api_utility import *
from models import *
import os
import pandas as pd
from app_config import db
from sqlalchemy import text


constant_layer = [ProcedureReference, OrderStatusReference, OrderShoeStatusReference]
outer_layer = [Department, Character, Operation, Customer, Shoe, Color, MaterialWarehouse, Supplier, ShoePart]
middle_first_layer = [Staff, Order, Material]
middle_second_layer = [Event, OrderStatus, OrderShoe]
middle_third_layer = [OrderShoeBatchInfo, Bom, OrderShoeStatus, MaterialStorage]
middle_fourth_layer = [BomItem, PurchaseOrder]
fifth_layer = [PurchaseDivideOrder]
Inner_layer = [PurchaseOrderItem]
structure_list = [constant_layer,outer_layer, middle_first_layer, middle_second_layer,
                    middle_third_layer, middle_fourth_layer, fifth_layer,
                    Inner_layer]


def getTypename(obj):
    return type(obj()).__name__


def toDBname(obj_name):
    result = ''
    for i in range (len( obj_name)):
        if obj_name[i].isupper():
            result += ("_" + obj_name[i].lower())
        else:
            result += obj_name[i]
    result = result [1:]
    return result


class MockDataGenerator():

    def __init__(self, database):
        self.layers = structure_list
        self.path_to_data = ""
        self.total_entity_list = []
        self.entity_list_to_push = []
        self.entity_to_path = {}
        self.db = database
        self.constant_layer = structure_list[0]
        self.entity_layers_list = structure_list[0:]

    def initializeEntityDataPath(self, path_to_data = "/mock_data/"):
        self.path_to_data = os.getcwd() + path_to_data
        layer_num = 0
        print("initializing DB")
        for layer in self.layers:
            print("Current Layer = " + str(layer_num))
            print("Entities are " + str(layer))
            for entity_class in layer:
                typeName = getTypename(entity_class)
                entity_path = self.path_to_data + toDBname(typeName) + ".csv"
                self.entity_to_path[typeName] = entity_path 
            layer_num += 1
    

    def setupDBLocalData(self, terminating_layer = None):
        print("Inserting into DB")
        if terminating_layer:
            print("Terminating at layer number " + str(terminating_layer))
        else:
            print("No Terminating Layer is set")
        layer_num = 0
        for layer in self.layers:
            print("Current layer is " + str(layer_num))
            print("should terminate at " + str(terminating_layer))
            if layer_num == terminating_layer:
                break
            else:
                for entity_class in layer:
                    data_path = self.entity_to_path[getTypename(entity_class)]
                    df = pd.read_csv(data_path)
                    column_list = df.columns.values.tolist()
                    for row in df.itertuples():
                        entity_object = entity_class()
                        for attribute in column_list:
                            setattr(entity_object, attribute , getattr(row, attribute))
                        self.entity_list_to_push.append(entity_object)
                    self.pushEntityObjectsDB(self.entity_list_to_push)
                    self.total_entity_list.append(self.entity_list_to_push)
                    self.entity_list_to_push = []
            layer_num += 1
    ### create entity list for all the layers 
    ### and insert into db
    def cleanAndSetup(self):
        print("layers before reversing")
        #print(self.layers)
        self.layers.reverse()
        #print("layers after reversing")
        #print(self.layers)
        for layer in self.layers:
            for entity_class in layer:
                table_name = toDBname(getTypename(entity_class))
                db.session.query(entity_class).delete()
                db.session.commit()
                # sql = text('ALTER TABLE `{}` auto_increment=1'.format(entity_class.__tablename__))
                # db.session.execute(sql)
        #print("reversing layers back")
        self.layers.reverse()
        #print(self.layers)

    def pushEntityObjectsDB(self, list_to_push):
        print("this is the list to push")
        print(list_to_push)
        self.db.session.add_all(list_to_push)
        self.db.session.commit()

    def setupDBwithmock(self):
        self.setupDBLocalData(terminating_layer=1)
        for layer in self.entity_layers_list:
            break
        return 
        
def TestPopulateEndEntityDB(shoes_rid_for_Shoes, customer_name_for_Customers):
        ### creating customers and shoes with rid
        for i in customer_name_for_Customers:
            if not check_customerName_exists(i):
                dbcreateCustomer(i)
                print("customer with name %s added", i)

        return True

def TestPopulateOrdersDB(firstTime = False, reset = False):
    order_starts_with = "K99-"
    test_customer = "Spain Customer 99"
    if firstTime:
        ### check if user exists
        if not check_customerName_exists(test_customer):
            dbcreateCustomer(test_customer)
        test_customer_id = get_customerId(test_customer)
        for i in range(42):
            dbcreateOrder("K99-" + str(i), "2024-01-01", test_customer_id)
            dbcreateOrder("K89-" + str(i) , "2024-01-01", test_customer_id)
        print("mock orders inserted") 
    elif reset == True:
        test_customer_id = get_customerId(test_customer)
        db.session.execute(db.delete(Order).filter_by(order_customer = test_customer_id))
        db.session.commit()
        print("mock orders deleted")
    return True
def testPopulateOrderDataDB():
    return



def populateConstantDB():
    return