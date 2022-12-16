"""_summary_

Returns:
    _type_: _description_
"""


import datetime

from bson import ObjectId as bson_ObjectId
from bson import json_util
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_pymongo import PyMongo
from pymongo.command_cursor import CommandCursor

from config import Config
from database.config import Database


def _convert_mongo_objects(obj):
    """Convert objects, related to Mongo database to JSON."""
    converted = None
    if isinstance(obj, CommandCursor):
        converted = json_util._json_convert(obj)  # pylint: disable=protected-access
    elif isinstance(obj, bson_ObjectId):
        converted = str(obj)
    elif isinstance(obj, datetime.datetime):
        converted = obj.isoformat()
    elif isinstance(obj, bytes):
        converted = obj.decode("utf-8")
    return converted


class CustomJSONProvider(DefaultJSONProvider):
    """_summary_

    Args:
        json (_type_): _description_
    """

    def default(self, obj):
        """_summary_

        Args:
            o (_type_): _description_

        Returns:
            _type_: _description_
        """
        base = super().default

        if isinstance(
            obj,
            (CommandCursor, bson_ObjectId, datetime.datetime, bytes),
        ):
            return _convert_mongo_objects(obj)
        return base(self, obj)


app_database = Database()


def get_app_database():
    return app_database.db


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

    driver = PyMongo()
    driver.init_app(app)

    app_database.set_database(database=driver.db)

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
