"""Configure Database
"""
import datetime

from bson import ObjectId, json_util
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_pymongo import PyMongo
from pymongo import ASCENDING, MongoClient
from pymongo.command_cursor import CommandCursor


def _convert_mongo_objects(obj):
    """Convert objects, related to Mongo database to JSON."""
    converted = None
    if isinstance(obj, CommandCursor):
        converted = json_util._json_convert(obj)  # pylint: disable=protected-access
    elif isinstance(obj, ObjectId):
        converted = str(obj)
    elif isinstance(obj, datetime.datetime):
        converted = obj.isoformat()
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
            (CommandCursor, ObjectId, datetime.datetime),
        ):
            return _convert_mongo_objects(obj)
        return base(self, obj)


# class Store:
#     """Create database"""

#     def __init__(self) -> None:
#         self.user = None
#         self.session = None

#     def init_app(self, app: Flask) -> None:
#         """_summary_

#         Args:
#             app (Flask): _description_
#         """

#         client = MongoClient(
#             host=app.config.get("MONGO_URI"),
#             port=app.config.get("MONGO_PORT"),
#             username=app.config.get("MONGO_USER"),
#             password=app.config.get("MONGO_PASSWORD"),
#             connect=False,
#         )

#         database_name = app.config.get("MONGO_DATABASE")
#         database = client[database_name]

#         self.user = database.get_collection("user")
#         self.session = database.get_collection("session")

#         self.create_user_indexes()


#     def create_user_indexes(self):
#         """_summary_

#         Args:
#             attribute (str): _description_
#         """
#         self.user.create_index(
#             [
#                 ("username", ASCENDING),
#                 ("email", ASCENDING),
#                 ("mobile", ASCENDING),
#             ],
#             unique=True,
#         )

#     def get_user(self, username):
#         """Get user

#         Returns:
#             json: response
#             int: http status code
#         """

#         user = self.user.find_one({"username": username})
#         return user

#     def update_user(self, username, data):
#         """Update user

#         Returns:
#             json: response
#             int: http status code
#         """
#         newvalues = {"$set": data}
#         user_filter = {"username": username}

#         result = self.user.update_one(user_filter, newvalues)
#         return result

#     def add_to_list(self, username, data):
#         """Update user

#         Returns:
#             json: response
#             int: http status code
#         """
#         newvalues = {"$push": data}
#         user_filter = {"username": username}

#         result = self.user.update_one(user_filter, newvalues)
#         return result


store = PyMongo()


def get_db():
    """_summary_

    Returns:
        _type_: _description_
    """
    return store
