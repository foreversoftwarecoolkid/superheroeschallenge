from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db' 
db = SQLAlchemy(app)
api = Api(app)

# Define your models here
class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    hero_powers = db.relationship('HeroPower', backref='hero', lazy=True)

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    hero_powers = db.relationship('HeroPower', backref='power', lazy=True)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

# Define your resources here
class HeroList(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

    def post(self):
        # Implement hero creation logic here
        pass

class HeroDetail(Resource):
    def get(self, id):
        hero = Hero.query.get_or_404(id)
        return jsonify(hero.to_dict())

    def patch(self, id):
        # Implement hero update logic here
        pass

class PowerList(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

    def post(self):
        # Implement power creation logic here
        pass

class PowerDetail(Resource):
    def get(self, id):
        power = Power.query.get_or_404(id)
        return jsonify(power.to_dict())

    def patch(self, id):
        # Implement power update logic here
        pass

class HeroPowerList(Resource):
    def post(self):
        # Implement hero_power creation logic here
        pass

# Add your resources to the API
api.add_resource(HeroList, '/heroes')
api.add_resource(HeroDetail, '/heroes/<int:id>')
api.add_resource(PowerList, '/powers')
api.add_resource(PowerDetail, '/powers/<int:id>')
api.add_resource(HeroPowerList, '/hero_powers')

if __name__ == '__main__':
    db.create_all() # Create the database tables
    app.run(debug=True)
