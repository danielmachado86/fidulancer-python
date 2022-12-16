class Database:
    def __init__(self, database=None) -> None:
        self.db = database

    def set_database(self, database):
        self.db = database


app_database = Database()


def get_app_database():
    return app_database.db


def set_app_database(value):
    return app_database.set_database(value)
