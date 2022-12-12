"""_summary_

Returns:
    _type_: _description_
"""


import datetime

import bson
from flask import Flask
from flask_pymongo import PyMongo

from api.db import CustomJSONProvider
from config import Config


class Date:
    def __init__(self) -> None:
        self.value = datetime.datetime.now()

    def new_value(self, value):
        self.value = value


class ObjectId:
    def __init__(self) -> None:
        self.value = bson.ObjectId()

    def new_value(self, value):
        self.value = bson.ObjectId(value)


class Database:
    def __init__(self) -> None:
        self.value = PyMongo()

    def new_value(self, value):
        self.value = value


app_date = Date()
app_objectid = ObjectId()
app_database = Database()


def get_app_date():
    return app_date.value


def get_app_objectid():
    return app_objectid.value


def get_app_database():
    return app_database.value


def create_app(config_class=Config) -> Flask:
    """_summary_

    Args:
        config_class (_type_, optional): _description_. Defaults to Config.

    Returns:
        _type_: _description_
    """

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json = CustomJSONProvider(app)

    db = get_app_database()

    db.init_app(app)

    from api.errors import errors  # pylint: disable=import-outside-toplevel

    app.register_blueprint(errors)

    from api.users import users  # pylint: disable=import-outside-toplevel

    app.register_blueprint(users, url_prefix="/v1")

    from api.contracts import contracts  # pylint: disable=import-outside-toplevel

    app.register_blueprint(contracts, url_prefix="/v1")

    from api.sessions import sessions  # pylint: disable=import-outside-toplevel

    app.register_blueprint(sessions, url_prefix="/v1")

    from api.payments import funds  # pylint: disable=import-outside-toplevel

    app.register_blueprint(funds, url_prefix="/v1")

    return app
