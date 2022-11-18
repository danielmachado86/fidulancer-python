from unittest.mock import patch

import pytest
from mongomock import MongoClient

import api
from api.app import create_app
from api.db import CustomJSONProvider


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture()
def app():
    """_summary_

    Yields:
        _type_: _description_
    """
    with patch.object(
        api.db,
        "store",
        PyMongoMock(),
    ):
        yield create_app()

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    """_summary_

    Args:
        app (_type_): _description_

    Returns:
        _type_: _description_
    """
    return app.test_client()
