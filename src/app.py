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
from models import db, User, People, Planet, Vehicle, Favoritos
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

# **************************************************************PEOPLE*****************************************************************
# ********TRAE TODOS LOS PERSONAJES**********
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        people = People.query.all()
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
    
# **************************************************************PLANET*********************************************************************
# ********TRAE TODOS LOS PLANETAS**********
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()
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
# *****************************************************************VEHICLE*****************************************************************
# ********TRAE TODOS LOS VEHICULOS**********
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    try:
        vehicles = Vehicle.query.all()
        if len(vehicles)<1:
            return jsonify({"msg": "There are no vehicles on the list"}), 404
        serialize_vehicles = list (map(lambda x: x.serialize(), vehicles))
        return serialize_vehicles, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********TRAE 1 VEHICULO POR ID**********
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    try:
        vehicle = Vehicle.query.get(vehicle_id)
        if vehicle is None:
            return jsonify ({"msg":f"Vehicle {vehicle_id} not found"}), 404
        serialize_vehicle = vehicle.serialize()
        return serialize_vehicle, 200
    except Exception as error:
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ********CREAR VEHICULO**********
@app.route('/vehicles', methods=['POST'])
def create_one_vehicle():
    try:
        body = json.loads(request.data)
        new_vehicle = Vehicle (
            name = body["name"],
            cargo_capacity = body["cargo_capacity"],
            length = body["length"]
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({"msg": "Vehicle has been created successfully"}), 201
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500
    
# ***************************************************************FAVORITOS***********************************************************************
# ********TRAE TODOS LOS FAVORITOS DE UN USUARIO EN ESPECÍFICO**********
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites_of_user_id(user_id):
    try:
        favorites = Favoritos.query.filter_by(user_id = user_id).all()
        if len(favorites)<1:
            return jsonify({"msg": "There are no favorites on the list"}), 404
        serialize_favorites = list (map(lambda x: x.serialize(), favorites))
        return serialize_favorites, 200
    except Exception as error: 
        return jsonify ({"msg":"Server error", "error": str(error)}), 500

# ********CREAR VEHICULO FAVORITO**********
@app.route('/favorite/vehicle/<int:vehicle_id>/<int:user_id>', methods=['POST'])
def create_favorite_vehicle(vehicle_id, user_id):
    try:
        if Favoritos.query.filter_by(user_id = user_id,vehicle_id=vehicle_id).first():
            return jsonify({"msg": f"Vehicle {vehicle_id} ya está agregago a favoritos"}), 404

        new_favorite_vehicle = Favoritos(
            user_id=user_id,
            vehicle_id=vehicle_id
        )
        db.session.add(new_favorite_vehicle)
        db.session.commit()

        return jsonify({"msg": "Favorite Vehicle has been created successfully"}), 201
    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500
    
# ********CREAR PEOPLE FAVORITO**********
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['POST'])
def create_favorite_people(people_id, user_id):
    try:
        if Favoritos.query.filter_by(user_id = user_id,people_id=people_id).first():
            return jsonify({"msg": f"People {people_id} ya está agregago a favoritos"}), 404

        new_favorite_people = Favoritos(
            user_id=user_id,
            people_id=people_id
        )
        db.session.add(new_favorite_people)
        db.session.commit()

        return jsonify({"msg": "Favorite Character has been created successfully"}), 201
    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500

# ********CREAR PLANETA FAVORITO**********
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def create_favorite_planet(planet_id, user_id):
    try:
        if Favoritos.query.filter_by(user_id = user_id,planet_id=planet_id).first():
            return jsonify({"msg": f"Planet {planet_id} ya está agregago a favoritos"}), 404

        new_favorite_planet = Favoritos(
            user_id=user_id,
            planet_id=planet_id
        )
        db.session.add(new_favorite_planet)
        db.session.commit()

        return jsonify({"msg": "Favorite Planet has been created successfully"}), 201
    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500

#****************ELIMINAR VEHICULO FAVORITO POR ID*******************
@app.route('/favorite/vehicle/<int:vehicle_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id, user_id):
    try:
        elimate_favorite_vehicle = Favoritos.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        
        if not elimate_favorite_vehicle:
            return jsonify({"msg": f"Vehicle {vehicle_id} no se encuentra en los favoritos del usuario {user_id}"}), 404

        db.session.delete(elimate_favorite_vehicle)
        db.session.commit()

        return jsonify({"msg": f"Vehicle {vehicle_id} eliminado de los favoritos exitosamente"}), 200

    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500

#****************ELIMINAR PLANETA FAVORITO POR ID*******************
@app.route('/favorite/planets/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id, user_id):
    try:
        elimate_favorite_planet = Favoritos.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        
        if not elimate_favorite_planet:
            return jsonify({"msg": f"Planet {planet_id} no se encuentra en los favoritos del usuario {user_id}"}), 404

        db.session.delete(elimate_favorite_planet)
        db.session.commit()

        return jsonify({"msg": f"Planet {planet_id} eliminado de los favoritos exitosamente"}), 200

    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500

#****************ELIMINAR PEOPLE FAVORITO POR ID*******************
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_people(people_id, user_id):
    try:
        elimate_favorite_people = Favoritos.query.filter_by(user_id=user_id, people_id=people_id).first()
        
        if not elimate_favorite_people:
            return jsonify({"msg": f"People {people_id} no se encuentra en los favoritos del usuario {user_id}"}), 404

        db.session.delete(elimate_favorite_people)
        db.session.commit()

        return jsonify({"msg": f"People {people_id} eliminado de los favoritos exitosamente"}), 200

    except Exception as error:
        return jsonify({"msg": "Server error", "error": str(error)}), 500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)