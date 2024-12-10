"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
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

# *****************************************************USER*******************************************************
# ********TRAE TODOS LOS USER**********
@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        # BUSCA DENTRO DEL MODELADO UNA TABLA QUE SE LLAME USER.
        users = User.query.all()
        # SI TAMAÑO DE users ES MENOR QUE 1 (no hay usuarios) tendría que decir que no se encuentran:
        if len(users)<1:
            return jsonify({"msg": "There are no users on the list"}), 404
        serialize_users = list (map(lambda x: x.serialize(), users))
        return serialize_users, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********TRAE 1 USER POR ID**********
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify ({"msg":f"user {user_id} not found"}), 404
        serialize_user = user.serialize()
        return serialize_user, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500

# ********CREAR USER**********
@app.route('/user', methods=['POST'])
def create_one_user():
    try:
        body = json.loads(request.data)
        new_user = User (
            email = body["email"],
            password = body["password"],
            is_active = True
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "User has been created successfully"}), 201
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500

# *****************************************************PEOPLE*******************************************************
# ********TRAE TODOS LOS PERSONAJES**********
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        # BUSCA DENTRO DEL MODELADO UNA TABLA QUE SE LLAME USERS.
        people = People.query.all()
        # SI TAMAÑO DE users ES MENOR QUE 1 (no hay usuarios) tendría que decir que no se encuentran:
        if len(people)<1:
            return jsonify({"msg": "There are no characters on the list"}), 404
        serialize_people = list (map(lambda x: x.serialize(), people))
        return serialize_people, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********TRAE 1 PERSONAJE POR ID**********
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    try:
        people = People.query.get(people_id)
        if people is None:
            return jsonify ({"msg":f"Character {people_id} not found"}), 404
        serialize_people = people.serialize()
        return serialize_people, 200
    except Exception as error:
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********CREAR PERSONAJE**********
@app.route('/people', methods=['POST'])
def create_one_people():
    try:
        body = json.loads(request.data)
        new_people = People (
            name = body["name"],
            gender = body["gender"],
            hair_color = body["hair_color"]
        )
        db.session.add(new_people)
        db.session.commit()
        return jsonify({"msg": "Character has been created successfully"}), 201
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# *****************************************************PLANET*******************************************************
# ********TRAE TODOS LOS PLANETAS**********
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()
        # SI TAMAÑO DE users ES MENOR QUE 1 (no hay usuarios) tendría que decir que no se encuentran:
        if len(planets)<1:
            return jsonify({"msg": "There are no characters on the list"}), 404
        serialize_planets = list (map(lambda x: x.serialize(), planets))
        return serialize_planets, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********TRAE 1 PLANETA POR ID**********
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify ({"msg":f"Planet {planet_id} not found"}), 404
        serialize_planet = planet.serialize()
        return serialize_planet, 200
    except Exception as error:
        return jsonify ({"msg":"Server error", "error": str(error)}), 500

# ********CREAR PLANETA**********
@app.route('/planets', methods=['POST'])
def create_one_planet():
    try:
        body = json.loads(request.data)
        new_planet = Planet (
            name = body["name"],
            population = body["population"],
            climate = body["climate"]
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify({"msg": "Planet has been created successfully"}), 201
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
# *****************************************************VEHICLE*******************************************************
# *****************************************************FAVORITOS*******************************************************
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
