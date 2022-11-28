import datetime
from unittest.mock import patch

import pytest
from mongomock import MongoClient

import api
from api.app import app_date, create_app
from api.db import CustomJSONProvider

FAKE_TIME = datetime.datetime(2020, 12, 25, 17, 5, 55)


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
        app = create_app()
        app_date.new_date(FAKE_TIME)
        app.config.update({"TESTING": True})
        yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    """_summary_

    Args:
        app (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!
