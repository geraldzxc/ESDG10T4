import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment' #payment is the database table
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app) #initialise database instance 

# creating payment class
class Payment(db.Model):
    __tablename__ = 'payment' # the table name can be the same as the class name, no issues

    # defining the columns name for the table
    payment_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable = False)
    payment_success = db.Column(db.Boolean, nullable = False)
    
    # json format for how an instance of payment record would be created
    def json(self):
        return {'payment_id': self.payment_id, 'price': self.price, 'payment_success': self.payment_success}


@app.route("/payment")
# Get all payment records
def get_all(): 
    paymentlist = db.session.scalars(db.select(Payment)).all() #Payment here refers to the class name 
    if len(paymentlist):
        return jsonify(
            {
                # Request success, there are existing payments
                "code": 200,
                "data": {
                    "orders": [payment.json() for payment in paymentlist]
                }
            }
        )
    # No existng payment record in the database
    return jsonify(
        {
            "code": 404,
            "message": "There are no payment record."
        }
    ), 404


# Find a specific payment record using its payment_id
@app.route("/payment/<string:payment_id>")
def find_by_payment_id(payment_id):
    payment = db.session.scalars(
        db.select(Payment).filter_by(payment_id=payment_id).limit(1)).first() # Limit to 1 and the first record foudn 
    if payment:
        # Record exists
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "payment_id": payment_id
            },
            "message": "Payment record not found."
        }
    ), 404

# Create a new payment record 
@app.route("/payment", methods=['POST'])
def create_payment():
    customer_id = request.json.get('customer_id', None)
    order = Order(customer_id=customer_id, status='NEW')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            book_id=item['book_id'], quantity=item['quantity']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": .json()
        }
    ), 201

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
