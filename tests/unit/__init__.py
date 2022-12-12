import datetime
from unittest.mock import patch

import pytest
from mongomock import MongoClient

import api
from api.app import app_database, app_date, app_objectid, create_app, get_app_database
from api.db import CustomJSONProvider
from api.models import CreateUserValidator

pytest.register_assert_rewrite("tests.unit.helpers")

FAKE_TIME = datetime.datetime(2022, 12, 25, 17, 5, 55)
FAKE_OID = "6385248afe09c73d411fda0a"


class PyMongoMock(MongoClient):  # pylint: disable=abstract-method
    """_summary_

    Args:
        MongoClient (_type_): _description_
    """

    def init_app(
        self, app
    ):  # pylint: disable=missing-function-docstring,redefined-outer-name,unused-argument
        return super().__init__()


@pytest.fixture()
def app():
    """_summary_

    Yields:
        _type_: _description_
    """
    app = create_app()  # pylint: disable=redefined-outer-name
    app_date.new_value(FAKE_TIME)
    app_objectid.new_value(FAKE_OID)
    fake_db = PyMongoMock()
    app_database.new_value(fake_db)
    app.config.update({"TESTING": True})
    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):  # pylint: disable=redefined-outer-name
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


@pytest.fixture(autouse=True)
def add_users(app):  # pylint: disable=redefined-outer-name
    """_summary_

    Args:
        app (_type_): _description_
    """
    user_data = {
        "name": "Jimena Lopez",
        "username": "jimenalogo",
        "email": "jimenalogo@gmail.com",
        "mobile": "+573046628057",
        "password": "secret",
    }
    user = CreateUserValidator(**user_data).get_data()
    db = get_app_database().db
    db.get_collection("user").insert_one(user)

    yield
