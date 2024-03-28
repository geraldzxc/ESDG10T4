from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213:@localhost:3306/login'
db = SQLAlchemy(app)

class Users(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the email and password from the request
        email = request.json['email']
        password = request.json['password']

        # Check if the user exists
        user = Users.query.filter_by(email=email, password=password).first()

        if user:
            # User exists, return a success response
            return jsonify({'message': 'Login successful'})
        else:
            # User does not exist or password is incorrect, return an error response
            return jsonify({'message': 'Username or password is incorrect'}), 401
        
    except Exception as e:
        # Log the exception details
        print(f"An error occurred: {str(e)}")
        # Return an error response
        return jsonify({'message': 'An error occurred on the server'}), 500

if __name__ == '__main__':
    app.run(debug = True)
