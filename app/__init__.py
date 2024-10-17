from flask import Flask
from .database import db
from .routes import hero_routes, power_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register the blueprints
    app.register_blueprint(hero_routes)
    app.register_blueprint(power_routes)

    return app
