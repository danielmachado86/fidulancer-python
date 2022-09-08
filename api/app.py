
from flask import Flask
from flask_pymongo import PyMongo

from config import Config


db = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from api.errors import errors
    app.register_blueprint(errors)
    from api.users import users
    app.register_blueprint(users, url_prefix='/v1')

    return app
