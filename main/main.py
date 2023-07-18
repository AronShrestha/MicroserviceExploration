from flask import Flask, jsonify, abort
from dataclasses import dataclass
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
import requests
import socket

from producer import publish


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    id : int
    title : str
    image : str
    id = db.Column(db.Integer, primary_key = True, autoincrement = False)
    #autoincrement is set to False because product will nt be created in this App, rather will 
    #created in the djanog App, and this App will jst cache the event from RabitnQue. So 
    # here id will be diferent than the django app
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    
    db.UniqueConstraint('user_id', 'product_id', name = 'user_product_unique')


# def get_host_ip():
#     """Gets the real host machine IP from inside the container environment."""
#     try:
#         host_ip = socket.gethostbyname("host.docker.internal")
#     except socket.gaierror:
#         host_ip = None
#     return host_ip


@app.route('/api/products')
def index():
    # print('*'*100)
    # print("Host ip is",get_host_ip())
    return jsonify(Product.query.all())

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    print("in like")
    req = requests.get('http://192.168.101.16:8000/api/user')
    # req = requests.get('http://host.docker.internal:8000/api/user')
    # return jsonify(req.json())
    json = req.json()
    try:
        productUser = ProductUser(user_id = json['id'], product_id = id)
        db.session.add(productUser)
        db.session.commit()
        print(f"Liked product {json}")
        publish('producer_liked', id)

    except:
        abort(400, 'You already liked this product',e)
    
    return jsonify({
        'message':'success'
    })


if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')