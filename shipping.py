#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)


@app.route("/shipping_record", methods=['POST'])
def receiveOrder():
    # Check if the order contains valid JSON
    order = None
    if request.is_json:
        order = request.get_json()
        result = processOrder(order)
        return jsonify(result), result["code"]
    else:
        data = request.get_data()
        print("Received an invalid order:")
        print(data)
        return jsonify({"code": 400,
                        # make the data string as we dunno what could be the actual format
                        "data": str(data),
                        "message": "Order should be in JSON."}), 400  # Bad Request input


def processOrder(order):
    print("Processing an order for shipping:")
    print(order)
    
    # Check if order contains all required fields
    if 'order_id' not in order or 'customer_id' not in order or 'order_item' not in order:
        return {
            'code': 400,
            'data': None,
            'message': 'Order is missing required fields.'
        }
    
    # Check if any field has null value
    if order['order_id'] is None or \
        order['customer_id'] is None or \
        order['order_item'] is None or \
        order['cart_amt'] is None or \
        order['payment_id'] is None or \
        order['shipping_id'] is None:
        return {
            'code': 400,
            'data': None,
            'message': 'Order contains errors. Please check the fields and try again.'
        }
    
    def calculate_shipping_time():
        current_date = datetime.date.today()
        shipping_time = current_date + datetime.timedelta(days=5)
        return shipping_time

    # Added shipping time which is 5 days after current date of order processing
    shipping_time = calculate_shipping_time()
    order['shipping_time'] = shipping_time

    return {
        'code': 200,
        'data': order,
        'message': 'Order is processed successfully.'
    }

# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5002, debug=True)
