"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

# ACÁ SOLO PARA CONFIGURAR LAS RUTAS

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# ACÁ ES DONDE SE AGREGAN ENDPOINTS

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        # BUSCA DENTRO DEL MODELADO UNA TABLA QUE SE LLAME USERS.
        users = User.query.all()
        # SI TAMAÑO DE users ES MENOR QUE 1 (no hay usuarios) tendría que decir que no se encuentran:
        if len(users)<1:
            return jsonify({"msg": "There are no users on the list"}), 404
        serialize_users = list (map(lambda x: x.serialize(), users))
        return serialize_users, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
