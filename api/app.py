
from flask import Flask
from flask_mongoengine import MongoEngine

from config import Config


db = MongoEngine()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['MONGODB_SETTINGS'] = {
        "db": "fidulancer_db",
        "host": "mongodb",
        "port": 27017,
        "username": "root",
        "password": "example",
        "alias": "default",
    }
    
    db.init_app(app)

    from api.errors import errors
    app.register_blueprint(errors)
    from api.users import users
    app.register_blueprint(users, url_prefix='/v1')

    return app
