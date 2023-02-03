from flask import Flask
from flask_pymongo import PyMongo
from pymongo.database import Database


class MongoDB:
    def __init__(self) -> None:
        self.driver = PyMongo()
        self.db = self.driver.db

    def set_database(self, database: Database):
        self.db = database

    def init_app(self, app: Flask) -> None:
        self.driver.init_app(app)

    def get_app_database(self) -> Database | None:
        return self.db


app_database = MongoDB()
