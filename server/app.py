#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources_by_tag, resources_by_tag

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('dqofnqxij'),
    api_key=os.environ.get('788673843553949'),
    api_secret=os.environ.get('BK11IcZfCYX0NyaxbSQ6XCuoufg')
)

# Initialize Flask application and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://authorizationapis_l2cu_user:DvnSZAkiIGPsmSd9MOD2WE11IBHntvKa@dpg-cooeb3n79t8c73bc7ajg-a.oregon-postgres.render.com/authorizationapis_l2cu'
db = SQLAlchemy(app)
migrate = Migrate(app, db) 
api = Api(app)

# Define database models
class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255))
    hero = db.relationship('Hero', backref='hero_powers')
    power = db.relationship('Power', backref='hero_powers')

# Define resource classes
class HeroList(Resource):
    def get(self):
        heroes = Hero.query.all()
        return [hero.to_dict() for hero in heroes]

class HeroItem(Resource):
    def get(self, hero_id):
        hero = Hero.query.get(hero_id)
        if hero:
            return hero.to_dict()
        else:
            return {"error": "Hero not found"}, 404

class PowerList(Resource):
    def get(self):
        powers = Power.query.all()
        return [power.to_dict() for power in powers]

class PowerItem(Resource):
    def get(self, power_id):
        power = Power.query.get(power_id)
        if power:
            return power.to_dict()
        else:
            return {"error": "Power not found"}, 404

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

class HeroPowerCreate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hero_id', type=int, required=True)
        parser.add_argument('power_id', type=int, required=True)
        parser.add_argument('strength', required=True)
        parser.add_argument('image', type=str, required=True)  # Image URL
        args = parser.parse_args()

        # Upload image to Cloudinary
        image_url = args['image']
        cloudinary_response = upload(image_url)

        # Check if upload was successful
        if 'secure_url' in cloudinary_response:
            # Extract secure URL from Cloudinary response
            image_secure_url = cloudinary_response['secure_url']

            hero_id = args['hero_id']
            power_id = args['power_id']
            strength = args['strength']

            if strength not in ['Strong', 'Weak', 'Average']:
                return {"error": "Invalid strength value"}, 400

            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)

            if not hero or not power:
                return {"error": "Hero or Power not found"}, 404

            hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength, image_url=image_secure_url)
            db.session.add(hero_power)
            db.session.commit()

            return hero_power.to_dict(), 201
        else:
            # Handle upload failure
            return {"error": "Image upload failed"}, 500

# Add resources to API
api.add_resource(HeroList, '/heroes')
api.add_resource(HeroItem, '/heroes/<int:hero_id>')
api.add_resource(PowerList, '/powers')
api.add_resource(PowerItem, '/powers/<int:power_id>')
api.add_resource(PowerUpdate, '/powers/<int:power_id>')
api.add_resource(HeroPowerCreate, '/hero_powers')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=False)
