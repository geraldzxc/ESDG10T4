#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_type = db.Column(db.String(20), nullable=False)
    # status = db.Column(db.String(10), nullable=False)
    # created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # modified = db.Column(db.DateTime, nullable=False,
    #                      default=datetime.now, onupdate=datetime.now)

    def json(self):
        return {'user_id': self.user_id, 'username': self.username, 'email': self.email}


@app.route('/login', methods=['POST'])
def login():
    try:
        # Get the email and password from the request
        email = request.json['email']
        password = request.json['password']

        # Check if the user exists
        user = User.query.filter_by(email=email, password=password).first()

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


@app.route("/user/create", methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    usertype = data.get('user_type')

    # Check if the user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, password=password, user_type=usertype)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@app.route("/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user.json()), 200

@app.route("/user")
def get_all():
    userlist = db.session.scalars(db.select(User)).all()

    if len(userlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [user.json() for user in userlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404



if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
