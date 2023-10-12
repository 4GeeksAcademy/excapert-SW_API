"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planet, Favorites
from api.utils import generate_sitemap, APIException
from datetime import date

api = Blueprint('api', __name__)


@api.route('/users', methods=["GET"])
def get_users():
    return jsonify(
        users=[user.serialize() for user in User.query.all()]
    ), 200



@api.route('/characters', methods=["GET"])
def get_characters():
    return jsonify(
        characters=[character.serialize() for character in Character.query.all()]
    ), 200


@api.route('/characters/<int:id>', methods=["GET"])
def get_character(id):
    """
    This gets a character based on it's ID #
    """
    character = Character.query.filter_by(id=id).first()
    if character:
        return jsonify(character=character.serialize()), 200
    else:
        return jsonify(
            message=f"No character with id {id}",
            character=None
        ), 404


@api.route('/planets', methods=["GET"])
def get_planets():
    return jsonify(
        planets=[planet.serialize() for planet in Planet.query.all()]
    ), 200

@api.route('/planet/<int:id>', methods=["GET"])
def get_planet(id):
    planet = Planet.query.filter_by(id=id).first()
    if planet:
        return jsonify(planet=planet.serialize()), 200
    else:
        return jsonify(
            message=f"No planet found with id {id}",
            planet=None
        ), 404



# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200



@api.route('/users/favorites', methods=["GET"])
def get_users_favorites():

    return jsonify( "This is the favorites GET"), 200


# @api.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
# def handle_favorite_planet(planet_id):

#     if request.method == 'POST':
#         response_data = request.data
#         response_body = {
#         "msg": f"Hello, this is your POST /favorite/planet response {planet_id}",
#         "data": response_data

#         }
    
#         print(jsonify(response_body))
#         return jsonify(response_body), 200
    
#     if request.method == 'DELETE':

#         print("Delete")
#         return jsonify("delete"), 200
    

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_favorite_planet(planet_id):
    favorite_data = request.json
    new_favorite = Favorites(
        user_id=favorite_data.get("user_id"),  
        planet_id=favorite_data.get("planet_id", planet_id),
        character_id=favorite_data.get("character_id")
    )
    db.session.merge(new_favorite)
    db.session.commit()

    return "", 200
    
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_favorite_person(people_id):
    favorite_data = request.json
    new_favorite = Favorites(
        user_id=favorite_data.get("user_id"),  
        planet_id=favorite_data.get("planet_id"),
        character_id=favorite_data.get("character_id", people_id)
    )
    db.session.merge(new_favorite)
    db.session.commit()

    return "", 200
    
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_data = request.json
    delete_favorite = Favorites.query.filter_by(planet_id=planet_id).all()
    for favorite in delete_favorite :
        db.session.delete(favorite)
    db.session.commit()

    return jsonify(delete_favorite), 200


@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    favorite_data = request.json
    delete_favorite = Favorites.query.filter_by(character_id=people_id).all()
    for favorite in delete_favorite :
        db.session.delete(favorite)
    db.session.commit()

    return jsonify(delete_favorite), 200