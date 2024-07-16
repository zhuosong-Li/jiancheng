from flask_cors import CORS
from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Database connection configuration
db_config = {
    'host': 'rm-wz9lp07aju9k1c1jrvo.mysql.rds.aliyuncs.com',
    'user': 'jiancheng_dev3',
    'password': '12345678Ab',
    'database': 'jiancheng_test3'
}

def create_connection():
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    return connection

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/storepricereport', methods=['POST'])
def add_user():
    data = request.get_json()
    print(data)
    connection = create_connection()
    cursor = connection.cursor()

    for row in data:
        order_shoe_id = row['order_shoe_id']
        procedure_id = row['procedure_id']
        note = row['note']

        query = "INSERT INTO unit_price_report (order_shoe_id, procedure_id, note) VALUES \
                ({}, {}, '{}')".format(order_shoe_id, procedure_id, note)

        cursor.execute(query)
    connection.commit()
    
    cursor.close()
    connection.close()
    return jsonify({'message': 'User added successfully!'}), 201


@app.route('/fabriccutting/getorders', methods=['GET'])
def get_orders():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM orders"
    cursor.execute(query)
    rows = cursor.fetchall()

    orders = []
    for row in rows:
        orders.append(
            {'order_id': row[0], 
             'order_rid': row[1], 
             'order_createtime': row[2],
             'order_customer': row[3]
            })

    cursor.close()
    connection.close()

    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)

