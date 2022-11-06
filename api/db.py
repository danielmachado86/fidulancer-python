"""Configure Database
"""
import datetime
import json
from flask import Flask
from pymongo import MongoClient
from bson import ObjectId
from pymongo import ASCENDING



class JSONEncoder(json.JSONEncoder):
    """_summary_

    Args:
        json (_type_): _description_
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Store:
    """Create database"""

    def __init__(self, vendor: str, collection_name: str) -> None:
        self.vendor = vendor.lower()
        self.client = None
        self.database = None
        self.collection = None
        self.collection_name = collection_name

    def init_app(self, app: Flask) -> None:
        """_summary_

        Args:
            app (Flask): _description_
        """
        if self.vendor == "mongodb":

            self.client = MongoClient(
                host=app.config.get("MONGO_URL"),
                port=app.config.get("MONGO_PORT"),
                username=app.config.get("MONGO_USER"),
                password=app.config.get("MONGO_PASSWORD"),
                connect=False,
            )

            database_name = app.config.get("MONGO_DATABASE")
            self.database = self.client[database_name]
            
            self.collection = self.database.get_collection(self.collection_name)

            app.json_encoder = JSONEncoder


    def create_index(self, attribute: str):
        """_summary_

        Args:
            attribute (str): _description_
        """
        self.collection.create_index([(attribute, ASCENDING)], unique=True)
        
    
    def get_user(self, username):
        """Get user

        Returns:
            json: response
            int: http status code
        """

        user = self.collection.find_one({"username": username})
        return user

    def insert_user(self, data):
        """Get user

        Returns:
            json: response
            int: http status code
        """

        result = self.collection.insert_one(data)
        return result

    def update_user(self, username, data):
        """Update user

        Returns:
            json: response
            int: http status code
        """
        newvalues = { "$set": data }
        user_filter = { 'username': username }

        result = self.collection.update_one(user_filter, newvalues)
        return result

    def add_to_list(self, username, data):
        """Update user

        Returns:
            json: response
            int: http status code
        """
        newvalues = { "$push": data }
        user_filter = { 'username': username }

        result = self.collection.update_one(user_filter, newvalues)
        return result
