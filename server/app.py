#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

# Resource for getting all heroes
class HeroList(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict() for hero in heroes]

# Resource for getting a specific hero by ID
class HeroItem(Resource):
    def get(self, hero_id):
        hero = Hero.query.get(hero_id)
        if hero:
            return hero.to_dict()
        else:
            return {"error": "Hero not found"}, 404

# Resource for getting all powers
class PowerList(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict() for power in powers]

# Resource for getting a specific power by ID
class PowerItem(Resource):
    def get(self, power_id):
        power = Power.query.get(power_id)
        if power:
            return power.to_dict()
        else:
            return {"error": "Power not found"}, 404

# Resource for updating a power by ID
class PowerUpdate(Resource):
    def patch(self, power_id):
        parser = reqparse.RequestParser()
        parser.add_argument('description', required=True)
        args = parser.parse_args()
        
        power = Power.query.get(power_id)
        if not power:
            return {"error": "Power not found"}, 404

        description = args['description']
        if len(description) < 20:
            return {"error": "Description must be at least 20 characters long"}, 400
        
        power.description = description
        db.session.commit()

        return power.to_dict()

# Resource for creating a hero power
class HeroPowerCreate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hero_id', type=int, required=True)
        parser.add_argument('power_id', type=int, required=True)
        parser.add_argument('strength', required=True)
        args = parser.parse_args()

        hero_id = args['hero_id']
        power_id = args['power_id']
        strength = args['strength']

        if strength not in ['Strong', 'Weak', 'Average']:
            return {"error": "Invalid strength value"}, 400

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return {"error": "Hero or Power not found"}, 404

        hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(hero_power)
        db.session.commit()

        return hero_power.to_dict(), 201

# Add resources to API
api.add_resource(HeroList, '/heroes')
api.add_resource(HeroItem, '/heroes/<int:hero_id>')
api.add_resource(PowerList, '/powers')
api.add_resource(PowerItem, '/powers/<int:power_id>')
api.add_resource(PowerUpdate, '/powers/<int:power_id>')
api.add_resource(HeroPowerCreate, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
