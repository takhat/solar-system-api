from flask import Blueprint, jsonify

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
planet_bp = Blueprint("planet", __name__, url_prefix="/planet")


@planet_bp.route('', methods=['GET'])
def get_all_planets():
    """converts a list of objects into a list of dictionaries"""
    result = []
    for item in planet_items:
        item_dict = {"id": item.id, 
        "name": item.name,
        "description":item.description,
        "distance_from_sun": item.distance_from_sun}
        result.append(item_dict)
    return jsonify(result), 200

@planet_bp.route('/<planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    
    try:
        planet_id = int(planet_id)
    except ValueError:
        return jsonify({"msg": f"invalid data type: {planet_id}"}), 400
    chosen_planet = None
    for item in planet_items:
        if item.id == planet_id:
            chosen_planet = item
    if chosen_planet is None:
        return({"msg": f"could not find planet item with id: {planet_id}"}), 404
    result = {
        'id': chosen_planet.id,
        "name": chosen_planet.name,
        "description": chosen_planet.description,
        "distance_from_sun": chosen_planet.distance_from_sun
    } 
    
    return jsonify(result), 200