from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from marshmallow.exceptions import ValidationError

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    
    # Creating Flask object
    app = Flask(__name__)

    # Error decorators

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400
    
    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400

    # App Configuration
    app.config.from_object("config.app_config")

    # Creating Database object
    db.init_app(app)

    # Creating Marshmallow for converting datatypes between Python
    ma.init_app(app)

    # Creating bcrypt object within app
    bcrypt.init_app(app)

    # Creating JWT authentication/authorization in app
    jwt.init_app(app)

    # Seed commands configuration

    from commands import db_commands
    app.register_blueprint(db_commands)

    # Importing the controllers and activating the blueprints in a for loop!
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app