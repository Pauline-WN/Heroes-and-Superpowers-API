from flask import Blueprint, jsonify, request
from .models import Hero, Power, HeroPower
from .database import db

hero_routes = Blueprint('hero_routes', __name__)
power_routes = Blueprint('power_routes', __name__)

# GET /heroes
@hero_routes.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    result = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(result)

# GET /heroes/:id
@hero_routes.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = db.session.get(Hero, id)  # Updated to use session.get()
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [
            {
                "id": hp.id,
                "strength": hp.strength,
                "power": {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                }
            }
            for hp in hero.hero_powers
        ]
    }
    return jsonify(hero_data)

# GET /powers
@power_routes.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    result = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(result)

# GET /powers/:id
@power_routes.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = db.session.get(Power, id)  # Updated to use session.get()
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    })

# PATCH /powers/:id
@power_routes.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = db.session.get(Power, id)  # Updated to use session.get()
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()

    # Validation: description must be at least 20 characters long
    if 'description' in data and len(data['description']) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters long"]}), 400

    # Update power's description if valid
    if 'description' in data:
        power.description = data['description']

    db.session.commit()

    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    })

# POST /hero_powers
@hero_routes.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    # Validation: strength must be 'Strong', 'Weak', or 'Average'
    if data.get('strength') not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 400

    hero = db.session.get(Hero, data['hero_id'])  # Updated to use session.get()
    power = db.session.get(Power, data['power_id'])  # Updated to use session.get()

    if not hero or not power:
        return jsonify({"errors": ["Invalid hero_id or power_id"]}), 400

    new_hero_power = HeroPower(
        hero_id=data['hero_id'],
        power_id=data['power_id'],
        strength=data['strength']
    )

    db.session.add(new_hero_power)
    db.session.commit()

    return jsonify({
        "id": new_hero_power.id,
        "hero_id": new_hero_power.hero_id,
        "power_id": new_hero_power.power_id,
        "strength": new_hero_power.strength,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }), 201
