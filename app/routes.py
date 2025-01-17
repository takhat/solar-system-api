from flask import Blueprint, jsonify, request, abort, make_response
from app import db

'''
class Planet:
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun
planet_items = [
    Planet(1, "Mercury", "Smallest Planet", 0.4),
    Planet(2, "Venus", "Hottest Planet", 0.7),
    Planet(3, "Earth", "Only inhabited Planet", 1),
    Planet(4, "Mars", "Dusty and cold with a thin atmosphere", 1.5),
    Planet(5, "Jupiter", "Twice as massive as other planets combined", 5.2),
    Planet(6, "Saturn", "Has dazzling icy rings",9.5),
    Planet(7, "Uranus","Rotates at 90 degrees",19.8),
    Planet(8, "Neptune","Dark, cold and whipped by supersonic winds", 30.1)
]
'''

planet_bp = Blueprint("planet", __name__, url_prefix="/planet")
from app.models.planet import Planet

@planet_bp.route('', methods=['GET'])
def get_all_planets():
    """converts a list of objects into a list of dictionaries"""
    
    distance_from_sun_query_value = request.args.get("distance_from_sun")
    if distance_from_sun_query_value is not None:
        planets = Planet.query.filter_by(distance_from_sun=distance_from_sun_query_value)
    else:
        planets = Planet.query.all()    
    result = []
    for item in planets:
        result.append(item.to_dict())
    return jsonify(result), 200

@planet_bp.route('/<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    chosen_planet = get_planet_from_id(planet_id)
    return jsonify(chosen_planet.to_dict()), 200

@planet_bp.route("",methods=["POST"])
def create_one_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name = request_body["name"], 
        description = request_body["description"], 
        distance_from_sun = request_body["distance_from_sun"]
        )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(
        {"msg":f"successfully created planet with id: {new_planet.id}"}), 201
        
@planet_bp.route("/<planet_id>",methods=["PUT"])
def update_one_planet(planet_id):
    update_planet = get_planet_from_id(planet_id)
    request_body = request.get_json()
    try:
        update_planet.name = request_body["name"]
        update_planet.description = request_body["description"]
        update_planet.distance_from_sun = request_body["distance_from_sun"]
    # except KeyError as e:
    #     return jsonify({"msg": f"missing needed data {e.args[0]}"}, 400)
    except KeyError:
        return jsonify({"msg": f"missing needed data"}, 400)
    db.session.commit()
    return jsonify({"msg":f"Successfully updated planet with id: {update_planet.id}"}), 200

@planet_bp.route("/<planet_id>",methods=["DELETE"])
def delete_planet(planet_id):
    planet_to_delete = get_planet_from_id(planet_id)
    db.session.delete(planet_to_delete)
    db.session.commit()
    return jsonify({"msg": f"successfully deleted planet with id {planet_to_delete.id}"}), 200
def get_planet_from_id(planet_id):

    try:
        planet_id = int(planet_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {planet_id}"}, 400))
    chosen_planet = Planet.query.get(planet_id)

    if chosen_planet is None:
        return abort(make_response({
            "msg": f"could not find planet item with id: {planet_id}"}, 404))
        
    return chosen_planet