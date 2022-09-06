from config import Config
from flask import Flask
from pymongo import MongoClient

client = MongoClient("mongodb", 27017, username='root', password='example', connect=False)

db = client.fidulancer_db
collection = db.contracts


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from api.errors import errors
    app.register_blueprint(errors)
    from api.users import users
    app.register_blueprint(users, url_prefix='/v1')

    return app
