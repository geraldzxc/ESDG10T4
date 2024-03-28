import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#payment is the database table
#port 3306 is the default port for listening to sql connections 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # by default, sqlalchemy would track modifications to the database, 
# but we would do that manually
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299} # reset connection to db after 299 seconds

# Initializes a SQLAlchemy object with the Flask application, enabling integration between Flask and SQLAlchemy.
db = SQLAlchemy(app)

# Defines a SQLAlchemy model named Payment which corresponds to a table in the database.
class Payment(db.Model):
    __tablename__ = 'payment' # Specifies the table name as "payment".

    payment_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    payment_success = db.Column(db.Boolean, nullable=False)
    cust_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)

    def json(self):
        return {'payment_id': self.payment_id, 'price': self.price, 'payment_success': self.payment_success, 
                'cust_id': self.cust_id, 'order_id': self.order_id}

with app.app_context():
    db.create_all()

# Display all payment records for a specific customer
# customer_id column matches customer_id passed in parameter
@app.route("/payment/<int:customer_id>")
def find_by_customer_id(customer_id):
    payment = db.session.scalars(
        db.select(Payment).filter_by(cust_id=customer_id).limit(1)).first() # Limit to 1 and the first record found
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
            "message": "Payment record not found."
        }
    ), 404

# Create a new payment record, must specify method as POST
# Customer type url: http://url.com/payment
@app.route("/payment", methods=['POST'])
def create_payment():
    customer_id = request.json.get('customer_id', None) # Retrieve customer id from POST request
    payment = Payment(customer_id=customer_id, status='NEW')

    try:
        db.session.add(payment)
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
            "data": payment.json()
        }
    ), 201

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": managing payments ...")
    app.run(host='0.0.0.0', port=5003, debug=True)
