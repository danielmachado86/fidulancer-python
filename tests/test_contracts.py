"""_summary_

Returns:
    _type_: _description_
"""
from unittest.mock import patch

import pytest
from mongomock import MongoClient

from api.app import create_app
from api.db import get_db


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture()
def app():
    store = get_db()
    driver = PyMongoMock()
    database = driver.get_database("fidulancer")
    collection = database.get_collection("users")
    app = create_app()
    with patch.object(store, "user", collection):
        app.config.update({"TESTING": True})
    yield app


@pytest.fixture()
def client(app):
    """_summary_

    Args:
        app (_type_): _description_

    Returns:
        _type_: _description_
    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    """_summary_

    Args:
        app (_type_): _description_

    Returns:
        _type_: _description_
    """
    return app.test_cli_runner()
