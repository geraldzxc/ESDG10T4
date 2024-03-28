from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/inventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Inventory(db.Model):
    __tablename__ = 'inventory'


    ID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.VARCHAR(64), nullable=False)
    ModelName = db.Column(db.VARCHAR(64), nullable=False)
    StockCount = db.Column(db.Integer, nullable=False)
    ProductPrice = db.Column(db.DECIMAL(10,2), nullable=False)


    def __init__(self, ID, ProductName, ModelName, StockCount, ProductPrice):
        self.ID = ID
        self.ProductName = ProductName
        self.ModelName = ModelName
        self.StockCount = StockCount
        self.ProductPrice = ProductPrice


    def json(self):
        return {"ID": self.ID, "ProductName": self.ProductName, "ModelName": self.ModelName, "StockCount": self.StockCount, "ProductPrice": self.ProductPrice}



@app.route("/inventory")
def get_all():
    inventorylist = db.session.scalars(db.select(Inventory)).all()


    if len(inventorylist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [inventory.json() for inventory in inventorylist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no items."
        }
    ), 404

@app.route('/inventory/<int:ID>', methods=['GET'])
def get_item(ID):
    inventory = db.session.scalars(
    db.select(Inventory).filter_by(ID=ID).
    limit(1)
    ).first()

    if inventory:
        return jsonify(
            {
                "code": 200,
                "data": inventory.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item not found."
        }
    ), 404
    


@app.route('/inventory/<int:ID>', methods=['PUT'])
def update_item(ID):
    inventory = db.session.scalars(
    db.select(Inventory).filter_by(ID=ID).
    limit(1)
    ).first()
    data = request.json

    if inventory:
        inventory.ID = data['ID']
        inventory.ProductName = data['ProductName']
        inventory.ModelName = data['ModelName']
        inventory.StockCount = data['StockCount']
        inventory.ProductPrice = data['ProductPrice']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": inventory.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Item not found."
        }
    ), 404
   

if __name__ == '__main__':
    app.run(port=5000, debug=True)
